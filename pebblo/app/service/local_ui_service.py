"""
This module handles business logic for local UI
"""

import json
import os
from typing import Any, Dict, List, Tuple

from dateutil import parser
from fastapi import status

from pebblo.app.config.config import var_server_config_dict
from pebblo.app.enums.common import StorageTypes
from pebblo.app.enums.enums import ApplicationTypes, CacheDir
from pebblo.app.models.models import (
    LoaderAppListDetails,
    LoaderAppModel,
    RetrievalAppDetails,
    RetrievalAppList,
    RetrievalAppListDetails,
)
from pebblo.app.service.local_ui.loader_apps import LoaderApp
from pebblo.app.service.local_ui.retriever_apps import RetrieverApp
from pebblo.app.service.local_ui.utils import get_app_type
from pebblo.app.storage.sqlite_db import SQLiteClient
from pebblo.app.utils.utils import (
    delete_directory,
    get_document_with_findings_data,
    get_full_path,
    get_pebblo_server_version,
    read_json_file,
    update_data_source,
    update_findings_summary,
)
from pebblo.log import get_logger

config_details = var_server_config_dict.get()

logger = get_logger(__name__)


class AppData:
    """
    This class handles business logic for local UI
    """

    def __init__(self):
        self.loader_apps_at_risk = 0
        self.loader_findings = 0
        self.loader_files_findings = 0
        self.loader_data_source = 0
        self.loader_findings_list = []
        self.loader_data_source_list = []
        self.loader_document_with_findings_list = []
        self.retrieval_active_users = {}
        self.retrieval_vectordbs = []
        self.total_retrievals = []
        self.db = None

    def prepare_loader_response(self, app_dir, app_json):
        # Default values
        app_name = app_json["name"]
        load_ids = app_json.get("load_ids", [])

        if not load_ids:
            logger.debug(f"[Dashboard]: No valid loadIds found for app: {app_dir}.")
            logger.warning(
                f"[Dashboard]: No valid loadIs found for the application: {app_name}, skipping application."
            )
            return

        # Fetching latest loadId
        latest_load_id, app_detail_json = self.get_latest_load_id(load_ids, app_dir)

        if not latest_load_id:
            logger.debug(
                f"[Dashboard]: No valid latest loadIds found for app: {app_dir}, skipping application."
            )
            logger.warning(
                f"[Dashboard]: No metadata file is present for any load ids for application: {app_name},"
                f"skipping Application."
            )
            return

        report_summary = app_detail_json.get("reportSummary")
        app_name = app_json.get("name")
        findings_entities = report_summary.get("findingsEntities", 0)
        findings_topics = report_summary.get("findingsTopics", 0)
        app_details = LoaderAppListDetails(
            name=app_json.get("name"),
            topics=findings_topics,
            entities=findings_entities,
            owner=report_summary.get("owner"),
            loadId=latest_load_id,
        )

        # Fetch details for dashboard tabs
        data_source_details = app_detail_json.get("dataSources")

        # Skip app if data source details are not present for some reason.
        if not data_source_details:
            logger.warning(
                f"[Dashboard]: No Data Source details are present for the application: {app_name},"
                f"skipping application."
            )
            return

        # Prepare output data
        for data in data_source_details:
            # Add appName in dataSource
            updated_data_source_dict = update_data_source(
                data, app_name, findings_entities, findings_topics
            )
            self.loader_data_source_list.append(updated_data_source_dict)

            # Add appName in findingsSummary
            finding_data = update_findings_summary(data, app_name)

            # Append only required value for dashboard
            self.loader_findings_list.extend(finding_data)

        # Fetch document with findings details from app metadata.json file
        app_metadata_detail_path = (
            f"{CacheDir.HOME_DIR.value}/{app_dir}/"
            f"{latest_load_id}/{CacheDir.METADATA_FILE_PATH.value}"
        )
        app_metadata_json_details = read_json_file(app_metadata_detail_path)

        # Fetch required data for DocumentWithFindings
        documents_with_findings_data = get_document_with_findings_data(
            app_metadata_json_details
        )
        self.loader_document_with_findings_list.extend(documents_with_findings_data)

        # Prepare counts for dashboard
        self.loader_findings += report_summary.get("findings", 0)
        self.loader_files_findings += report_summary.get("filesWithFindings", 0)
        self.loader_data_source += report_summary.get("dataSources", 0)
        if report_summary.get("findings", 0) > 0:
            self.loader_apps_at_risk += 1

        return app_details.model_dump()

    def get_prompt_details(
        self,
        prompt_details: Dict[str, Any],
        retrieval: Dict[str, Any],
        app_name: str,
        total_prompt_with_findings: int,
    ) -> Tuple[Dict[str, Any], int]:
        """
        Updates the prompt details with information from the retrieval data.

        Args:
            prompt_details (Dict[str, Any]): A dictionary to be updated with the retrieved prompt information.
            retrieval (Dict[str, Any]): A dictionary containing retrieval data, including prompt and user information.
            app_name (str): The name of the application associated with the prompt.

        Returns:
            Dict[str, Any]: The updated prompt details.
        """
        # Extract the prompt data from the retrieval
        prompt = retrieval.get("prompt", {})

        # Get the count of entities detected in the prompt
        count_entity = prompt.get("entityCount", 0)

        if count_entity > 0:
            total_prompt_with_findings += 1
            # If entities are detected, get the list of entities
            entity_detected = prompt.get("entities")

            for key, value in entity_detected.items():
                try:
                    if key in prompt_details[app_name]:
                        # If the entity type already exists in prompt_details, update the existing entry
                        prompt_details[app_name][key]["total_prompts"] += 1
                        prompt_details[app_name][key]["total_entity_count"] += value

                        # Get the user name from the retrieval data
                        user_name = retrieval.get("user", "")

                        if (
                            user_name
                            and user_name not in prompt_details[app_name][key]["users"]
                        ):
                            # Add new user to the user list if not already present
                            prompt_details[app_name][key]["users"].append(user_name)
                            prompt_details[app_name][key]["total_users"] += 1

                    else:
                        # If the entity type does not exist in prompt_details, create a new entry
                        prompt_details[app_name][key] = {
                            "total_prompts": 1,
                            "total_entity_count": value,
                            "users": [],
                            "total_users": 0,
                        }

                        user_name = retrieval.get("user", "")
                        if user_name:
                            prompt_details[app_name][key]["users"].append(user_name)
                            prompt_details[app_name][key]["total_users"] = 1
                except Exception as ex:
                    logger.warning(
                        f"[Dashboard]:  Error while iterating prompts for app {app_name} Error: {ex}"
                    )

        prompt_details[app_name] = dict(
            sorted(
                prompt_details[app_name].items(),
                key=lambda item: item[1]["total_entity_count"],
                reverse=True,
            )
        )
        return prompt_details, total_prompt_with_findings

    def prepare_retrieval_response(
        self, app_dir, app_json, prompt_details, total_prompt_with_findings
    ):
        logger.debug("[Dashboard]: In prepare retrieval response")
        app_name = app_json["name"]

        app_metadata_path = (
            f"{CacheDir.HOME_DIR.value}/{app_dir}/"
            f"{CacheDir.APPLICATION_METADATA_FILE_PATH.value}"
        )
        app_metadata_content = read_json_file(app_metadata_path)

        # Skip app if app_metadata details are not present for some reason.
        if not app_metadata_content:
            logger.debug(
                f"[Dashboard]: Error: Unable to fetch app_metadata.json content for {app_dir} app"
            )
            logger.debug(f"[Dashboard]: App metadata Json : {app_metadata_content}")
            logger.warning(
                f"[Dashboard]: Application metadata file is not present for application: {app_name}, skipping application"
            )
            return

        app_name = app_metadata_content.get("name", "")
        prompt_details[app_name] = {}
        # fetch total retrievals
        for retrieval in app_metadata_content.get("retrievals", []):
            try:
                retrieval_data = {"name": app_json.get("name")}
                retrieval_data.update(retrieval)
                self.total_retrievals.append(retrieval_data)
                prompt_details, total_prompt_with_findings = self.get_prompt_details(
                    prompt_details, retrieval, app_name, total_prompt_with_findings
                )
            except Exception as ex:
                logger.warning(
                    f"[Dashboard]:  Error while iterating retrieval for app {app_name} Error: {ex}"
                )

        # fetch active users per app
        active_users = self.get_active_users(app_metadata_content.get("retrievals", []))
        self.add_accumulate_active_users(active_users)

        # fetch vector dbs per app
        vector_dbs = self.get_vector_dbs(app_metadata_content.get("chains", []))
        self.retrieval_vectordbs.extend(vector_dbs)

        # fetch documents name per app
        documents = self.get_all_documents(app_metadata_content.get("retrievals", []))

        app_details = RetrievalAppListDetails(
            name=app_json.get("name"),
            owner=app_metadata_content.get("owner"),
            retrievals=app_metadata_content.get("retrievals", []),
            active_users=list(active_users.keys()),
            vector_dbs=vector_dbs,
            documents=list(documents.keys()),
        )
        return app_details.model_dump(), prompt_details, total_prompt_with_findings

    def get_all_apps_details(self):
        """
        Returns all necessary app details required for list app functionality.
        """
        response = {
            "pebbloServerVersion": get_pebblo_server_version(),
            "loaderApps": {},
            "retrievalApps": {},
        }
        storage_type = config_details.get("storage", {}).get(
            "type", StorageTypes.DATABASE.value
        )
        if storage_type == StorageTypes.FILE.value:
            try:
                dir_full_path = get_full_path(CacheDir.HOME_DIR.value)
                # List all apps in the directory
                dir_path = os.listdir(dir_full_path)

                all_loader_apps: list = []
                all_retrieval_apps: list = []
                prompt_details: dict = {}
                total_prompt_with_findings = 0
                # Iterating through each app in the directory
                for app_dir in dir_path:
                    try:
                        # Skip hidden folders
                        if app_dir.startswith("."):
                            logger.debug(
                                f"[Dashboard]: Skipping hidden folder {app_dir}"
                            )
                            continue
                        # Path to metadata.json
                        app_path = (
                            f"{CacheDir.HOME_DIR.value}/{app_dir}/"
                            f"{CacheDir.METADATA_FILE_PATH.value}"
                        )

                        logger.debug(f"[Dashboard]: Metadata file path {app_path}")
                        app_json = read_json_file(app_path)

                        if not app_json:
                            # Unable to find json file
                            logger.debug(
                                f"[Dashboard]: Metadata file {CacheDir.METADATA_FILE_PATH.value} "
                                f"not found for app: {app_dir}."
                            )
                            logger.warning(
                                f"[Dashboard]: Metadata file is not present for application: {app_dir},"
                                f"skipping application"
                            )
                            continue

                        app_type = app_json.get("app_type", None)
                        if app_type in ["loader", None]:
                            loader_app = self.prepare_loader_response(app_dir, app_json)
                            if loader_app:
                                all_loader_apps.append(loader_app)
                        elif app_type == "retrieval":
                            (
                                retrieval_app,
                                prompt_details,
                                total_prompt_with_findings,
                            ) = self.prepare_retrieval_response(
                                app_dir,
                                app_json,
                                prompt_details,
                                total_prompt_with_findings,
                            )
                            if retrieval_app:
                                all_retrieval_apps.append(retrieval_app)

                    except Exception as err:
                        logger.warning(
                            f"[Dashboard]: Error processing app {app_dir}: {err}"
                        )
                final_prompt_details = []
                for key, value in prompt_details.items():
                    try:
                        for k1, v1 in value.items():
                            try:
                                prompt_dict = {}
                                prompt_dict = {"app_name": key}
                                prompt_dict["entity_name"] = k1
                                prompt_dict["total_prompts"] = v1["total_prompts"]
                                prompt_dict["total_entity_count"] = v1[
                                    "total_entity_count"
                                ]
                                prompt_dict["users"] = v1["users"]
                                prompt_dict["total_users"] = v1["total_users"]
                                final_prompt_details.append(prompt_dict)
                            except Exception as ex:
                                logger.warning(
                                    f"[Dashboard]: Error in iterating key value pair in retrieval app list. Error: {ex}"
                                )
                    except Exception as ex:
                        logger.warning(
                            f"[Dashboard]: Error in iterating prompt details for all retrieval apps: {ex}"
                        )

                # Sort loader apps
                sorted_loader_apps = self._sort_loader_apps(all_loader_apps)

                logger.debug("[Dashboard]: Preparing loader app response object")
                loader_response = LoaderAppModel(
                    applicationsAtRiskCount=self.loader_apps_at_risk,
                    findingsCount=self.loader_findings,
                    documentsWithFindingsCount=self.loader_files_findings,
                    dataSourceCount=self.loader_data_source,
                    appList=sorted_loader_apps,
                    findings=self.loader_findings_list,
                    documentsWithFindings=self.loader_document_with_findings_list,
                    dataSource=self.loader_data_source_list,
                )

                # Sort retrievals data
                sorted_retrievals_apps = self._sort_retrievals_with_retrieval_count(
                    all_retrieval_apps
                )

                logger.debug("[Dashboard]: Preparing retrieval app response object")
                retrieval_response = RetrievalAppList(
                    appList=sorted_retrievals_apps,
                    retrievals=self.total_retrievals,
                    activeUsers=self.retrieval_active_users,
                    violations=[],
                    promptDetails=final_prompt_details,
                    total_prompt_with_findings=total_prompt_with_findings,
                )

                response.update(
                    {
                        "loaderApps": loader_response.model_dump(),
                        "retrievalApps": retrieval_response.model_dump(),
                    }
                )
                return json.dumps(response, indent=4)
            except Exception as ex:
                logger.error(f"[Dashboard]: Error in app listing. Error:{ex}")
                return json.dumps({})
        elif storage_type == StorageTypes.DATABASE.value:
            try:
                retriever_app_obj = RetrieverApp()
                loader_app_obj = LoaderApp()
                response.update(
                    {
                        "loaderApps": loader_app_obj.get_all_loader_apps(),
                        "retrievalApps": retriever_app_obj.get_all_retriever_apps(),
                    }
                )
                return json.dumps(response, indent=4)
            except Exception as ex:
                logger.error(f"[Dashboard]: Error in app listing. Error:{ex}")
                return json.dumps({})

    def get_loader_app_details(self, app_dir, load_ids):
        # Fetching latest loadId
        latest_load_id, app_detail_json = self.get_latest_load_id(load_ids, app_dir)

        if not latest_load_id:
            logger.debug(f"[App Details]: No valid loadIds found for app {app_dir}.")
            logger.warning(
                f"[App Details]: No valid latest loadIs found for app: {app_dir}, skipping application."
            )
            return json.dumps({})

        if not app_detail_json:
            return json.dumps({})

        return json.dumps(app_detail_json, indent=4)

    def get_app_details(self, app_dir):
        """
        Returns app details for an app.
        """
        storage_type = config_details.get("storage", {}).get(
            "type", StorageTypes.FILE.value
        )
        if storage_type == StorageTypes.FILE.value:
            try:
                # Path to metadata.json
                app_path = f"{CacheDir.HOME_DIR.value}/{app_dir}/{CacheDir.METADATA_FILE_PATH.value}"
                logger.debug(f"[App Details]: Metadata file path: {app_path}")
                # Reading metadata.json
                app_json = read_json_file(app_path)
                # Condition for handling loadId
                if not app_json:
                    # Unable to fetch loadId details
                    logger.debug(
                        f"[App Details]: Error: Report Json {CacheDir.METADATA_FILE_PATH.value}"
                        f"not found for app {app_path}"
                    )
                    logger.warning(
                        f"[App Details]: Metadata file is not present for application: {app_dir}, skipping application"
                    )
                    return json.dumps({})
                app_type = app_json.get("app_type", None)
                app_name = app_json.get("name")
                if app_type in ["loader", None]:
                    load_ids = app_json.get("load_ids", [])
                    if not load_ids:
                        # Unable to fetch loadId details
                        logger.debug(
                            f"[App Details]: Error: Details not found for app {app_path}"
                        )
                        logger.warning(
                            f"[App Details]: No valid loadIs found for the application: {app_name}, skipping application."
                        )
                        return json.dumps({})
                    response = self.get_loader_app_details(app_dir, load_ids)
                    return response
                elif app_type == "retrieval":
                    app_metadata_path = (
                        f"{CacheDir.HOME_DIR.value}/{app_dir}/"
                        f"{CacheDir.APPLICATION_METADATA_FILE_PATH.value}"
                    )
                    app_metadata_content = read_json_file(app_metadata_path)
                    # Skip app if app_metadata details are not present for some reason.
                    if not app_metadata_content:
                        logger.debug(
                            f"[App Details]: Error: Unable to fetch app_metadata.json content for {app_dir} app"
                        )
                        logger.warning(
                            f"[App Details]: Application metadata file is not present for application: {app_name},"
                            f"skipping application."
                        )
                        return json.dumps({})
                    response = self.get_retrieval_app_details(app_metadata_content)
                    return response
            except Exception as ex:
                logger.error(
                    f"[App Details]: Error in getting app details. Error: {ex}"
                )
        elif storage_type == StorageTypes.DATABASE.value:
            try:
                self.db = SQLiteClient()

                # create session
                self.db.create_session()
                app_type = get_app_type(self.db, app_dir)
                response = {}
                if app_type == ApplicationTypes.LOADER.value:
                    loader_app_obj = LoaderApp()
                    response = loader_app_obj.get_loader_app_details(self.db, app_dir)
                elif app_type == ApplicationTypes.RETRIEVAL.value:
                    retriever_app_obj = RetrieverApp()
                    response = retriever_app_obj.get_retriever_app_details(
                        app_name=app_dir
                    )
                return response
            except Exception as ex:
                logger.error(
                    f"[App Details]: Error in getting app details. Error: {ex}"
                )
            finally:
                logger.debug("[App Details] get app details finished.")
                self.db.session.close()

    def delete_application(self, app_name):
        """
        Delete an app
        """
        storage_type = config_details.get("storage", {}).get(
            "type", StorageTypes.FILE.value
        )
        if storage_type == StorageTypes.FILE.value:
            try:
                # Path to application directory
                app_dir_path = f"{CacheDir.HOME_DIR.value}/{app_name}"
                logger.debug(f"[Delete App]: Path: {app_dir_path}")
                response = delete_directory(app_dir_path, app_name)
                return response
            except Exception as ex:
                error_message = (
                    f"[Delete App]: Error in delete application. Error: {ex}"
                )
                logger.error(error_message)
                return {
                    "message": error_message,
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
        elif storage_type == StorageTypes.DATABASE.value:
            try:
                self.db = SQLiteClient()

                # create session
                self.db.create_session()

                app_type = get_app_type(self.db, app_name)
                if app_type == ApplicationTypes.LOADER.value:
                    loader_app_obj = LoaderApp()
                    loader_app_obj.delete_loader_app(self.db, app_name)
                elif app_type == ApplicationTypes.RETRIEVAL.value:
                    retriever_app_obj = RetrieverApp()
                    retriever_app_obj.delete_retrieval_app(self.db, app_name)
            except Exception as ex:
                error_message = (
                    f"[Delete App]: Error in delete application. Error: {ex}"
                )
                logger.error(error_message)
                # Getting error, Rollback everything we did in this run.
                self.db.session.rollback()
                return {
                    "message": error_message,
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            else:
                self.db.session.commit()
                message = f"Application {app_name} has been deleted."
                response = {"message": message, "status_code": status.HTTP_200_OK}
                logger.debug(message)
                return response
            finally:
                logger.debug("Closing database session for delete application")
                # Closing the session
                self.db.session.close()

    @staticmethod
    def get_latest_load_id(load_ids, app_dir):
        """
        Returns app latestLoadId for an app.
        """
        for load_id in reversed(load_ids):
            # Path to report.json
            app_detail_path = f"{CacheDir.HOME_DIR.value}/{app_dir}/{load_id}/{CacheDir.REPORT_DATA_FILE_NAME.value}"
            logger.debug(f"[App Details]: Report File path: {app_detail_path}")
            app_detail_json = read_json_file(app_detail_path)
            if app_detail_json:
                # If a report is found, proceed with this load_id
                latest_load_id = load_id
                return latest_load_id, app_detail_json

        return None, None

    def get_prompts_with_findings(self, retrieval_data: List[Dict[str, Any]]) -> int:
        """
        Counts the number of prompts with findings in the retrieval data.

        Args:
            retrieval_data (List[Dict[str, Any]]): A list of dictionaries containing the retrieval data.
                Each dictionary is expected to have a "prompt" key with another dictionary that contains an "entityCount" key.

        Returns:
            int: The total number of prompts with findings (where "entityCount" > 0).
        """
        return sum(
            1
            for data in retrieval_data
            if data.get("prompt", {}).get("entityCount", 0) > 0
        )

    def get_retrieval_app_details(self, app_content):
        retrieval_data = app_content.get("retrievals", [])

        retrieval_data = self._sort_retrievals_data(retrieval_data)

        active_users = self.get_active_users(retrieval_data)
        documents = self.get_all_documents(retrieval_data)
        vector_dbs = self.get_all_vector_dbs(retrieval_data)
        prompt_with_findings = self.get_prompts_with_findings(retrieval_data)
        # prepare app response
        response = RetrievalAppDetails(
            name=app_content["name"],
            description=app_content.get("description"),
            framework=app_content.get("framework"),
            instanceDetails=app_content.get("instanceDetails"),
            pebbloServerVersion=app_content.get("pebbloServerVersion"),
            pebbloClientVersion=app_content.get("pebbloClientVersion"),
            clientVersion=app_content.get("clientVersion"),
            total_prompt_with_findings=prompt_with_findings,
            retrievals=retrieval_data,
            activeUsers=active_users,
            vectorDbs=vector_dbs,
            documents=documents,
        )
        return json.dumps(response.model_dump(), default=str, indent=4)

    def add_accumulate_active_users(self, active_users):
        """Adding retrieval data for app listing per users"""
        for user_name, data in active_users.items():
            if user_name in self.retrieval_active_users.keys():
                self.retrieval_active_users[user_name].get("retrievals", []).extend(
                    data.get("retrievals", [])
                )
            else:
                self.retrieval_active_users[user_name] = data

    @staticmethod
    def fetch_last_accessed_time(accessed_time: list) -> str:
        """Fetching last accessed time per user"""
        try:
            sorted_time = sorted(accessed_time, reverse=True)
            last_accessed_time = sorted_time[0].isoformat()
            return last_accessed_time
        except Exception as ex:
            logger.error(
                f"[Dashboard]: Error in fetching last accessed time while returning app details response :{ex}"
            )
            return ""

    @staticmethod
    def get_sorted_users(retrieval_data: list) -> dict:
        """
        This function returns sorted active users per app in sorted descending order
        based on number of times it appeared in retrievals.
        """
        sorted_active_users: dict = {}
        active_users: dict = {}

        # fetch active users wise retrievals
        for data in retrieval_data:
            user_name = data.get("user")
            if user_name in active_users.keys():
                active_users[user_name].append(data)
            else:
                active_users.update({user_name: [data]})

        # sorting based on length on retrieval values per documents
        all_sorted_users = sorted(
            active_users.items(), key=lambda kv: (len(kv[1]), kv[0]), reverse=True
        )

        # converting sorted tuples to dictionary
        for user_name, data in all_sorted_users:
            if user_name in sorted_active_users.keys():
                sorted_active_users[user_name].append(data)
            else:
                sorted_active_users.update({user_name: data})

        return sorted_active_users

    def get_active_users(self, retrieval_data: list) -> dict:
        """
        This function returns active users per app with its metadata in following format:
        {
            "retrievals": [sorted active users],
            "last_accessed_time": "last accessed time",
            "linked_groups": [user groups]
        }
        """
        sorted_active_users = self.get_sorted_users(retrieval_data)
        response = {}
        for user_name, user_data in sorted_active_users.items():
            accessed_time = []
            user_groups = []
            for data in user_data:
                accessed_time.append(parser.parse(data.get("prompt_time")))
                if data.get("linked_groups"):
                    user_groups.extend(data.get("linked_groups"))
            response[user_name] = {
                "retrievals": user_data,
                "last_accessed_time": self.fetch_last_accessed_time(accessed_time),
                "linked_groups": list(set(user_groups)),
            }
        return response

    @staticmethod
    def get_vector_dbs(chains: dict) -> list:
        """This function returns vector dbs per app"""
        vector_dbs = []
        for data in chains:
            vector_dbs.extend([db["name"] for db in data["vectorDbs"]])
        return list(set(vector_dbs))

    @staticmethod
    def sort_retrievals(retrieval_data: list, search_key: str) -> dict:
        """
        This function returns data based on search key per app in sorted descending order
        based on number of times it appeared in retrievals.
        """
        resp: dict = {}
        sorted_resp: dict = {}
        # fetch data wise retrievals
        for data in retrieval_data:
            data_context = data.get("context")
            for context in data_context:
                data_name = context[search_key]
                if data_name in resp.keys():
                    resp[data_name].extend([data])
                else:
                    resp[data_name] = [data]

        # sorting based on length on retrieval values per search key
        all_resp_data = sorted(
            resp.items(), key=lambda kv: (len(kv[1]), kv[0]), reverse=True
        )

        # converting sorted tuples to dictionary
        for key_name, data in all_resp_data:
            if key_name in sorted_resp.keys():
                sorted_resp[key_name].extend(data)
            else:
                sorted_resp.update({key_name: data})

        return sorted_resp

    @staticmethod
    def _sort_retrievals_with_retrieval_count(retrievals: list) -> list:
        """
        Sort the list based on the retrieval count in the descending order
        :param retrievals: retrievals list
        :return:  sorted retrievals list
        """
        sorted_data = sorted(
            retrievals, key=lambda item: len(item["retrievals"]), reverse=True
        )
        return sorted_data

    @staticmethod
    def _sort_retrievals_data(retrieval: list):
        """
        Sort the retrievals based on prompt_time in descending order
        :param retrieval: retrievals list
        :return: sorted retrievals list
        """
        sorted_data = sorted(retrieval, key=lambda x: x["prompt_time"])
        return sorted_data

    @staticmethod
    def _calculate_findings(item):
        """Calculate total findings(entities + topics)"""
        return item["topics"] + item["entities"]

    def _sort_loader_apps(self, loader_apps_list: list):
        """Sort the list based on the findings in descending order"""
        sorted_data = sorted(
            loader_apps_list, key=self._calculate_findings, reverse=True
        )
        return sorted_data

    def get_all_documents(self, retrieval_data: list) -> dict:
        """
        This function returns documents per app with its metadata in following format:
        {
            "retrievals": [sorted active users],
            "last_accessed_time": "last accessed time",
        }
        """
        sorted_document = self.sort_retrievals(retrieval_data, "retrieved_from")
        response = {}
        for user_name, user_data in sorted_document.items():
            accessed_time = []
            for data in user_data:
                accessed_time.append(parser.parse(data.get("prompt_time")))
            response[user_name] = {
                "retrievals": user_data,
                "last_accessed_time": self.fetch_last_accessed_time(accessed_time),
            }
        return response

    def get_all_vector_dbs(self, retrieval_data: list) -> dict:
        """
        This function returns vector dbs per app in sorted descending order
        based on number of times it appeared in retrievals.
        """
        sorted_vector_dbs = self.sort_retrievals(retrieval_data, "vector_db")
        return sorted_vector_dbs
