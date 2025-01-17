import json

from pebblo.app.models.resp_models import RetrievalDetail, RetrievalResp
from pebblo.app.models.sqltables import AiRetrievalTable
from pebblo.app.storage.sqlite_db import SQLiteClient
from pebblo.log import get_logger

logger = get_logger(__name__)


class RetrievalHandler:
    def __init__(self, app_name):
        """
        Constructor for RetrievalHandler class
        :param app_name: App Name
        """
        self.db = SQLiteClient()
        self.app_name = app_name
        self.retrievals_with_concern = 0
        self.retrieval_response = {"retrievals_with_concern": 0, "retrievals": []}

    def get_retrieval_data(self, app_name: str) -> list:
        """
        This function return AiRetrieval data based on app name.
        :param app_name: App Name
        :return: AIRetrieval Data List
        """
        retrieval_data = []
        filter_query = {"appName": app_name}
        _, all_retrieval_data = self.db.query(
            table_obj=AiRetrievalTable, filter_query=filter_query
        )

        if len(all_retrieval_data) == 0:
            raise Exception("Document with this app name does not exists.")

        for data in all_retrieval_data:
            retrieval_data.append(data.data)
        return retrieval_data

    @staticmethod
    def get_prompt_retrieval_finding(data) -> dict:
        data_resp = {
            "data": data["data"],
            "entity_details": data["entities"],
            "topic_details": data["topics"],
        }
        # resp = LabelDetails(**data_resp)
        return data_resp

    def get_retrieval_findings(self, data) -> RetrievalDetail:
        retrieved_data = {
            "with_concern": False,
            "queried_by": data["user"],
            "prompt_time": data["promptTime"],
            "prompt": self.get_prompt_retrieval_finding(data["prompt"]),
            "response": self.get_prompt_retrieval_finding(data["response"]),
        }
        if (
            data["prompt"].get("entities")
            or data["prompt"].get("topics")
            or data["response"].get("entities")
            or data["response"].get("topics")
        ):
            retrieved_data["with_concern"] = True
            self.retrievals_with_concern += 1
        retrieved_data_resp = RetrievalDetail(**retrieved_data)
        return retrieved_data_resp

    def create_retrieval_response(self, retrieval_data: list) -> dict:
        """
        This function return RetrievalResp object based on the doc data.
        :param retrieval_data: AiRetrieval Data List
        :return: Retrieval Info Response List
        """
        for data in retrieval_data:
            doc_data_resp = self.get_retrieval_findings(data)
            self.retrieval_response["retrievals"].append(doc_data_resp.model_dump())
        self.retrieval_response["retrievals_with_concern"] = (
            self.retrievals_with_concern
        )
        resp_dict = RetrievalResp(**self.retrieval_response).model_dump()
        return resp_dict

    def get_retrieval_info(self) -> str:
        """
        This function return retrieval info based on app name
        :return: Retrieval Info
        """
        try:
            # create session
            self.db.create_session()
            retrieval_data = self.get_retrieval_data(self.app_name)
            retrieval_response = self.create_retrieval_response(retrieval_data)
            return json.dumps(retrieval_response, default=str, indent=4)
        except Exception as ex:
            logger.error(
                f"Error in getting retrieval info for {self.app_name}. Error: {ex}"
            )
        finally:
            logger.debug(f"Get retrieval info finished for {self.app_name}")
            # Closing session
            self.db.session.close()
