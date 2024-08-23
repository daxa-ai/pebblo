"""
This module handles business logic for local UI for Safe Retriever DB Apps
"""

import json
from typing import Any, Dict, List, Tuple

from dateutil import parser
from fastapi import status

from pebblo.app.config.config import var_server_config_dict
from pebblo.app.models.db_response_models import (
    RetrievalAppDetails,
    RetrievalAppList,
    RetrievalAppListDetails,
)
from pebblo.app.models.sqltables import (
    AiAppTable,
    AiRetrievalTable,
    AiUser,
)
from pebblo.app.storage.sqlite_db import SQLiteClient
from pebblo.log import get_logger

config_details = var_server_config_dict.get()

logger = get_logger(__name__)


class RetrieverApp:
    """
    This class handles business logic for local UI Safe Retriever Apps
    """

    def __init__(self):
        self.db = None
        self.retrieval_active_users = {}
        self.retrieval_vectordbs = []
        self.total_retrievals = []

    @staticmethod
    def get_db_sorted_users(retrieval_data: list, all_apps: bool = False) -> dict:
        """
        This function returns sorted active users per app in sorted descending order
        based on number of times it appeared in retrievals.
        """
        sorted_active_users: dict = {}
        active_users: dict = {}

        # fetch active users wise retrievals
        for data in retrieval_data:
            if all_apps:
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

    def get_db_active_users(self, retrieval_data: list, all_apps: bool = False) -> dict:
        """
        This function returns active users per app with its metadata in following format:
        {
            "retrievals": [sorted active users],
            "last_accessed_time": "last accessed time",
            "linked_groups": [user groups]
        }
        """
        sorted_active_users = self.get_db_sorted_users(retrieval_data, all_apps)
        response = {}
        for user_name, user_data in sorted_active_users.items():
            accessed_time = []
            user_groups = []
            for data in user_data:
                accessed_time.append(parser.parse(data.get("promptTime")))
                if data.get("linkedGroups"):
                    user_groups.extend(data.get("linkedGroups"))
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
    def sort_db_retrievals(
        retrieval_data: list, search_key: str, all_apps: bool = False
    ) -> dict:
        """
        This function returns data based on search key per app in sorted descending order
        based on number of times it appeared in retrievals.
        """
        resp: dict = {}
        sorted_resp: dict = {}
        # fetch data wise retrievals
        for data in retrieval_data:
            if all_apps:
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

    def get_all_db_documents(
        self, retrieval_data: list, all_apps: bool = False
    ) -> dict:
        """
        This function returns documents per app with its metadata in following format:
        {
            "retrievals": [sorted active users],
            "last_accessed_time": "last accessed time",
        }
        """

        sorted_document = self.sort_db_retrievals(
            retrieval_data, "retrievedFrom", all_apps
        )
        response = {}
        for user_name, user_data in sorted_document.items():
            accessed_time = []
            for data in user_data:
                accessed_time.append(parser.parse(data.get("promptTime")))
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
            table_obj=AiRetrievalTable, filter_query={"appName": app_name}
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
        active_users = self.get_db_active_users(ai_retrievals, all_apps=True)
        self.add_accumulate_active_users(active_users)

        # fetch vector dbs per app
        vector_dbs = self.get_vector_dbs(retriever_data.get("chains"))
        self.retrieval_vectordbs.extend(vector_dbs)

        # fetch documents name per app
        documents = self.get_all_db_documents(ai_retrievals, all_apps=True)

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
            retrievals, key=lambda item: len(item.get("retrievals", [])), reverse=True
        )
        return sorted_data

    @staticmethod
    def _sort_db_retrievals_data(retrieval: list):
        """
        Sort the retrievals based on prompt_time in descending order
        :param retrieval: retrievals list
        :return: sorted retrievals list
        """
        sorted_data = sorted(retrieval, key=lambda x: x.get("prompt_time", []))
        return sorted_data

    def get_all_vector_dbs(self, retrieval_data: list) -> dict:
        """
        This function returns vector dbs per app in sorted descending order
        based on number of times it appeared in retrievals.
        """
        sorted_vector_dbs = self.sort_db_retrievals(retrieval_data, "vectorDb")
        return sorted_vector_dbs

    @staticmethod
    def get_prompts_with_findings(retrieval_data: List[Dict[str, Any]]) -> int:
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

    def prepare_retrieval_app_response(self, app_data, retrieval_data):
        retrieval_data = self._sort_db_retrievals_data(retrieval_data)

        active_users = self.get_db_active_users(retrieval_data)
        documents = self.get_all_db_documents(retrieval_data)
        vector_dbs = self.get_all_vector_dbs(retrieval_data)
        prompt_with_findings = self.get_prompts_with_findings(retrieval_data)
        # prepare app response
        response = RetrievalAppDetails(
            name=app_data["name"],
            description=app_data.get("description"),
            framework=app_data.get("framework"),
            instanceDetails=app_data.get("instanceDetails"),
            pebbloServerVersion=app_data.get("pebbloServerVersion"),
            pebbloClientVersion=app_data.get("pebbloClientVersion"),
            clientVersion=app_data.get("clientVersion"),
            total_prompt_with_findings=prompt_with_findings,
            retrievals=retrieval_data,
            activeUsers=active_users,
            vectorDbs=vector_dbs,
            documents=documents,
        )
        return json.dumps(response.dict(), default=str, indent=4)

    def get_all_retriever_apps(self):
        try:
            self.db = SQLiteClient()

            # create session
            self.db.create_session()

            _, ai_retriever_apps = self.db.query(table_obj=AiAppTable)
            all_retrieval_apps: list = []
            total_prompt_with_findings = 0
            final_prompt_details = []

            for retriever_app in ai_retriever_apps:
                prompt_details: dict = {}
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

            response = retrieval_response.dict()
            logger.debug(f"RetrievalAppResponse: {response}")
        except Exception as ex:
            logger.error(f"[Dashboard]: Error in all retriever app listing. Error:{ex}")
            # Getting error, Rollback everything we did in this run.
            self.db.session.rollback()
        else:
            message = "All retriever app response prepared successfully"
            logger.debug(message)
            return response
        finally:
            logger.debug("Closing database session for preparing all retriever apps")
            # Closing the session
            self.db.session.close()

    def get_retriever_app_details(self, app_name):
        try:
            retrieval_data = []

            self.db = SQLiteClient()

            # create session
            self.db.create_session()

            _, app_obj = self.db.query(
                table_obj=AiAppTable, filter_query={"name": app_name}
            )

            if app_obj and len(app_obj) > 0:
                app_obj = app_obj[0]
            else:
                pass
            app_data = app_obj.data

            # fetch retrieval data
            _, ai_retrieval_obj = self.db.query(
                table_obj=AiRetrievalTable, filter_query={"appName": app_name}
            )

            if ai_retrieval_obj and len(ai_retrieval_obj) > 0:
                for retrieval_obj in ai_retrieval_obj:
                    retrieval_obj = retrieval_obj.data
                    data = {
                        "prompt": retrieval_obj.get("prompt", {}),
                        "response": retrieval_obj.get("response", {}),
                        "context": retrieval_obj.get("context", []),
                        "promptTime": retrieval_obj.get("promptTime", None),
                        "user": retrieval_obj.get("user", ""),
                        "linkedGroups": retrieval_obj.get("linkedGroups", []),
                    }
                    retrieval_data.append(data)

            # prepare retrieval app response
            response = self.prepare_retrieval_app_response(app_data, retrieval_data)
        except Exception as ex:
            logger.error(f"[Dashboard]: Error in all retriever app listing. Error:{ex}")
            # Getting error, Rollback everything we did in this run.
            self.db.session.rollback()
        else:
            message = "All retriever app response prepared successfully"
            logger.debug(message)
            return response
        finally:
            logger.debug("Closing database session for preparing all retriever apps")
            # Closing the session
            self.db.session.close()

    @staticmethod
    def delete_retrieval_app(db, app_name):
        try:
            _, ai_app_obj = db.query(
                table_obj=AiAppTable, filter_query={"name": app_name}
            )

            # delete entry from AiRetrieval Table
            _, ai_retriever_apps = db.query(
                table_obj=AiRetrievalTable, filter_query={"app_name": app_name}
            )
            if ai_retriever_apps and len(ai_retriever_apps) > 0:
                db.delete(ai_retriever_apps)

            # delete entry from AiUser table if needed
            user_ids = ai_app_obj[0].data.get("users")
            for user_id in user_ids:
                _, ai_user_obj = db.query(
                    table_obj=AiUser, filter_query={"id": user_id}
                )
                if ai_user_obj and len(ai_user_obj) > 0:
                    ai_user_obj = ai_user_obj[0]
                    user_data = ai_user_obj.data
                    if app_name in user_data.get("appName"):
                        if len(user_data.get("appName")) > 1:
                            existing_apps = user_data.get("appName")
                            existing_apps.remove(app_name)
                            user_data["appName"] = existing_apps
                            update_status, message = db.update_data(
                                table_obj=ai_user_obj, data=user_data
                            )
                            if not update_status:
                                message = f"Exception occurred while deleting {app_name} application"
                                logger.exception(message)
                        else:
                            db.delete(ai_user_obj)

            # delete entry from AiApp table
            db.delete(ai_app_obj)

            message = f"Application {app_name} has been deleted."
            logger.info(message)
            result = {"message": message, "status_code": status.HTTP_200_OK}
        except Exception as e:
            message = f"Unable to delete application {app_name}, Error: {e}"
            logger.exception(message)
        else:
            # Commit will only happen when everything went well.
            message = "App deletion processed Successfully"
            logger.debug(message)
            return result
