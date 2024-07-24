"""
This module handles business logic for local UI
"""

import json
import os

from dateutil import parser
from fastapi import status

from pebblo.app.enums.enums import CacheDir
from pebblo.app.libs.logger import logger
from pebblo.app.models.models import (
    LoaderAppListDetails,
    LoaderAppModel,
    RetrievalAppDetails,
    RetrievalAppList,
    RetrievalAppListDetails,
)
from pebblo.app.utils.utils import (
    delete_directory,
    get_document_with_findings_data,
    get_full_path,
    get_pebblo_server_version,
    read_json_file,
    update_data_source,
    update_findings_summary,
)


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

        return app_details.dict()

    def prepare_retrieval_response(self, app_dir, app_json):
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

        # Sort retrievals data
        retrievals = self.sort_retrievals_data(
            app_metadata_content.get("retrievals", [])
        )
        app_metadata_content["retrievals"] = retrievals

        # fetch total retrievals
        for retrieval in app_metadata_content.get("retrievals", []):
            retrieval_data = {"name": app_json.get("name")}
            retrieval_data.update(retrieval)
            self.total_retrievals.append(retrieval_data)

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
        return app_details.dict()

    def get_all_apps_details(self):
        """
        Returns all necessary app details required for list app functionality.
        """
        try:
            dir_full_path = get_full_path(CacheDir.HOME_DIR.value)
            # List all apps in the directory
            dir_path = os.listdir(dir_full_path)

            all_loader_apps: list = []
            all_retrieval_apps: list = []

            # Iterating through each app in the directory
            for app_dir in dir_path:
                try:
                    # Skip hidden folders
                    if app_dir.startswith("."):
                        logger.debug(f"[Dashboard]: Skipping hidden folder {app_dir}")
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
                        retrieval_app = self.prepare_retrieval_response(
                            app_dir, app_json
                        )
                        if retrieval_app:
                            all_retrieval_apps.append(retrieval_app)

                except Exception as err:
                    logger.warning(
                        f"[Dashboard]: Error processing app {app_dir}: {err}"
                    )

            logger.debug("[Dashboard]: Preparing loader app response object")
            loader_response = LoaderAppModel(
                applicationsAtRiskCount=self.loader_apps_at_risk,
                findingsCount=self.loader_findings,
                documentsWithFindingsCount=self.loader_files_findings,
                dataSourceCount=self.loader_data_source,
                appList=all_loader_apps,
                findings=self.loader_findings_list,
                documentsWithFindings=self.loader_document_with_findings_list,
                dataSource=self.loader_data_source_list,
            )

            logger.debug("[Dashboard]: Preparing retrieval app response object")
            retrieval_response = RetrievalAppList(
                appList=all_retrieval_apps,
                retrievals=self.total_retrievals,
                activeUsers=self.retrieval_active_users,
                violations=[],
            )

            response = {
                "pebbloServerVersion": get_pebblo_server_version(),
                "loaderApps": loader_response.dict(),
                "retrievalApps": retrieval_response.dict(),
            }
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
            logger.error(f"[App Details]: Error in getting app details. Error: {ex}")

    @staticmethod
    def delete_application(app_name):
        """
        Delete an app
        """
        try:
            # Path to application directory
            app_dir_path = f"{CacheDir.HOME_DIR.value}/{app_name}"
            logger.debug(f"[Delete App]: Path: {app_dir_path}")
            response = delete_directory(app_dir_path, app_name)
            return response
        except Exception as ex:
            error_message = f"[Delete App]: Error in delete application. Error: {ex}"
            logger.error(error_message)
            return {
                "message": error_message,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }

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
                # If report is found, proceed with this load_id
                latest_load_id = load_id
                return latest_load_id, app_detail_json

        return None, None

    def get_retrieval_app_details(self, app_content):
        retrieval_data = app_content.get("retrievals", [])

        retrieval_data = self.sort_retrievals_data(retrieval_data)

        active_users = self.get_active_users(retrieval_data)
        documents = self.get_all_documents(retrieval_data)
        vector_dbs = self.get_all_vector_dbs(retrieval_data)

        # prepare app response
        response = RetrievalAppDetails(
            name=app_content["name"],
            description=app_content.get("description"),
            framework=app_content.get("framework"),
            instanceDetails=app_content.get("instanceDetails"),
            pebbloServerVersion=app_content.get("pebbloServerVersion"),
            pebbloClientVersion=app_content.get("pebbloClientVersion"),
            retrievals=retrieval_data,
            activeUsers=active_users,
            vectorDbs=vector_dbs,
            documents=documents,
        )
        return json.dumps(response.dict(), default=str, indent=4)

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
    def _calculate_total_count(item: dict):
        prompt_count = item.get("prompt", {}).get("entityCount") or 0
        response_count = item.get("prompt", {}).get("entityCount") or 0
        return prompt_count + response_count

    def sort_retrievals_data(self, retrieval):
        # Sort the list based on the total count in descending order
        sorted_data = sorted(retrieval, key=self._calculate_total_count, reverse=True)
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
