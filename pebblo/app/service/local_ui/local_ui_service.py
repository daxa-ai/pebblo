"""
This module handles business logic for local UI for DB Apps
"""

import json
from typing import Any, Dict, Tuple

from dateutil import parser

from pebblo.app.config.config import var_server_config_dict
from pebblo.app.models.models import (
    RetrievalAppList,
    RetrievalAppListDetails,
)
from pebblo.app.models.sqltables import (
    AiAppTable,
    AiDataLoaderTable,
    AiRetrievalTable,
)
from pebblo.app.storage.sqlite_db import SQLiteClient
from pebblo.app.utils.utils import (
    get_pebblo_server_version,
)
from pebblo.log import get_logger

config_details = var_server_config_dict.get()

logger = get_logger(__name__)


class AppData:
    """
    This class handles business logic for local UI
    """

    def __init__(self):
        self.db = None
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

    def get_all_apps(self):
        _, ai_app_obj = self.db.query(table_obj=AiAppTable)
        _, ai_loader_app_obj = self.db.query(table_obj=AiDataLoaderTable)
        return ai_loader_app_obj, ai_app_obj

    @staticmethod
    def get_db_sorted_users(retrieval_data: list) -> dict:
        """
        This function returns sorted active users per app in sorted descending order
        based on number of times it appeared in retrievals.
        """
        sorted_active_users: dict = {}
        active_users: dict = {}

        # fetch active users wise retrievals
        for data in retrieval_data:
            data = data.data
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

    @staticmethod
    def get_prompt_details(
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
            total_prompt_with_findings(int): Contains prompt findings

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

                        # Get the username from the retrieval data
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

    def get_db_active_users(self, retrieval_data: list) -> dict:
        """
        This function returns active users per app with its metadata in following format:
        {
            "retrievals": [sorted active users],
            "last_accessed_time": "last accessed time",
            "linked_groups": [user groups]
        }
        """
        sorted_active_users = self.get_db_sorted_users(retrieval_data)
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
    def get_vector_dbs(chains: dict) -> list:
        """This function returns vector dbs per app"""
        vector_dbs = []
        for data in chains:
            vector_dbs.extend([db["name"] for db in data["vectorDbs"]])
        return list(set(vector_dbs))

    @staticmethod
    def sort_db_retrievals(retrieval_data: list, search_key: str) -> dict:
        """
        This function returns data based on search key per app in sorted descending order
        based on number of times it appeared in retrievals.
        """
        resp: dict = {}
        sorted_resp: dict = {}
        # fetch data wise retrievals
        for data in retrieval_data:
            data = data.data
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

    def get_all_db_documents(self, retrieval_data: list) -> dict:
        """
        This function returns documents per app with its metadata in following format:
        {
            "retrievals": [sorted active users],
            "last_accessed_time": "last accessed time",
        }
        """

        sorted_document = self.sort_db_retrievals(retrieval_data, "retrieved_from")
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

    def prepare_db_retrieval_response(
        self, retriever_app, prompt_details, total_prompt_with_findings
    ):
        all_retrievals = []
        retriever_data = retriever_app.data
        app_name = retriever_data.get("name")
        prompt_details[app_name] = {}

        # fetch total retrievals
        _, ai_retrievals = self.db.query(
            table_obj=AiRetrievalTable, filter_query={"app_name": app_name}
        )
        for ai_retrieval in ai_retrievals:
            try:
                all_retrievals.append(ai_retrieval.data)
                retrieval_data = {"name": app_name}
                retrieval_data.update(ai_retrieval.data)
                self.total_retrievals.append(retrieval_data)
                prompt_details, total_prompt_with_findings = self.get_prompt_details(
                    prompt_details,
                    ai_retrieval.data,
                    app_name,
                    total_prompt_with_findings,
                )
            except Exception as ex:
                logger.warning(
                    f"[Dashboard]:  Error while iterating retrieval for app {app_name} Error: {ex}"
                )

        # fetch active users per app
        active_users = self.get_db_active_users(ai_retrievals)
        self.add_accumulate_active_users(active_users)

        # fetch vector dbs per app
        vector_dbs = self.get_vector_dbs(retriever_data.get("chains"))
        self.retrieval_vectordbs.extend(vector_dbs)

        # fetch documents name per app
        documents = self.get_all_db_documents(ai_retrievals)

        app_details = RetrievalAppListDetails(
            name=app_name,
            owner=retriever_data.get("owner"),
            retrievals=all_retrievals,
            active_users=list(active_users.keys()),
            vector_dbs=vector_dbs,
            documents=list(documents.keys()),
        )
        return app_details.dict(), prompt_details, total_prompt_with_findings

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

    def get_all_apps_details(self):
        try:
            self.db = SQLiteClient()

            # create session
            self.db.create_session()

            ai_loader_apps, ai_retriever_apps = self.get_all_apps()
            # all_loader_apps: list = []
            all_retrieval_apps: list = []
            prompt_details: dict = {}
            total_prompt_with_findings = 0
            final_prompt_details = []

            # # Preparing all loader apps
            # all_loader_apps: list = []
            # for loader_app in ai_loader_apps:
            #     app_data = loader_app.data
            #     if app_data.get("docEntities") not in [None, {}] or app_data.get(
            #         "docTopics"
            #     ) not in [None, {}]:
            #         self.loader_apps_at_risk += 1
            #         self.get_findings_for_loader_app(app_data)
            #         # TODO: need to clarify
            #         # self.loader_document_with_findings_list = app_data.get('documentsWithFindings')
            #         # self.loader_files_findings = len(self.loader_document_with_findings_list)
            #     print(loader_app)
            #     logger.info(loader_app)
            #
            # # Sort loader apps
            # sorted_loader_apps = self._sort_loader_apps(all_loader_apps)
            #
            # logger.debug("[Dashboard]: Preparing loader app response object")
            # loader_response = LoaderAppModel(
            #     applicationsAtRiskCount=self.loader_apps_at_risk,
            #     findingsCount=self.loader_findings,
            #     documentsWithFindingsCount=self.loader_files_findings,
            #     dataSourceCount=self.loader_data_source,
            #     appList=sorted_loader_apps,
            #     findings=self.loader_findings_list,
            #     documentsWithFindings=self.loader_document_with_findings_list,
            #     dataSource=self.loader_data_source_list,
            # )

            # Preparing all retrieval apps
            for retriever_app in ai_retriever_apps:
                (
                    retrieval_app,
                    prompt_details,
                    total_prompt_with_findings,
                ) = self.prepare_db_retrieval_response(
                    retriever_app,
                    prompt_details,
                    total_prompt_with_findings,
                )
                if retrieval_app:
                    all_retrieval_apps.append(retrieval_app)

                for key, value in prompt_details.items():
                    try:
                        for k1, v1 in value.items():
                            try:
                                prompt_dict = {
                                    "app_name": key,
                                    "entity_name": k1,
                                    "total_prompts": v1["total_prompts"],
                                    "total_entity_count": v1["total_entity_count"],
                                    "users": v1["users"],
                                    "total_users": v1["total_users"],
                                }
                                final_prompt_details.append(prompt_dict)
                            except Exception as ex:
                                logger.warning(
                                    f"[Dashboard]: Error in iterating key value pair in DB retrieval app list. Error: {ex}"
                                )
                    except Exception as ex:
                        logger.warning(
                            f"[Dashboard]: Error in iterating prompt details for all DB retrieval apps: {ex}"
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

            response = {
                "pebbloServerVersion": get_pebblo_server_version(),
                # "loaderApps": loader_response.dict(),
                "retrievalApps": retrieval_response.dict(),
            }
        except Exception as ex:
            logger.error(f"[Dashboard]: Error in app listing. Error:{ex}")
            # Getting error, Rollback everything we did in this run.
            self.db.session.rollback()
        else:
            # Commit will only happen when everything went well.
            message = "Prompt Request Processed Successfully"
            logger.debug(message)
            self.db.session.commit()
            return json.dumps(response, indent=4)
        finally:
            logger.debug("Closing database session for Prompt API.")
            # Closing the session
            self.db.session.close()
            return json.dumps({})
