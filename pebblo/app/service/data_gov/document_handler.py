import json

from pebblo.app.models.resp_models import DocResp, DocsFindings
from pebblo.app.models.sqltables import AiDocumentTable
from pebblo.app.storage.sqlite_db import SQLiteClient
from pebblo.log import get_logger

logger = get_logger(__name__)


class DataGov:
    def __init__(self, app_name):
        """
        Constructor for DataGov class
        :param app_name: App Name
        """
        self.db = SQLiteClient()
        self.app_name = app_name
        self.docs_at_risk = 0
        self.doc_response = {"docs_at_risk": 0, "docs_findings": []}

    def get_doc_findings(self, data: dict) -> DocsFindings:
        """
        This function return DocsFindings object based on the data.
        :param data: AiDocument Data
        :return: DocsFindings Object
        """
        doc_data = {
            "doc_name": data["appName"],
            "at_risk": False,
            "topics": [],
            "entities": [],
            "total_snippets": 0,
            "access_groups": data.get("userIdentities", []),
        }
        if data.get("topics"):
            doc_data["at_risk"] = True
            for topics, details in data["topics"].items():
                doc_data["topics"].append(topics)
                doc_data["total_snippets"] += details["count"]
        if data.get("entities"):
            doc_data["at_risk"] = True
            for entities, details in data["entities"].items():
                doc_data["entities"].append(entities)
                doc_data["total_snippets"] += details["count"]
        doc_data_resp = DocsFindings(**doc_data)
        if doc_data["at_risk"]:
            self.docs_at_risk += 1
        return doc_data_resp

    def create_doc_response(self, doc_data: list) -> dict:
        """
        This function return DocResp object based on the doc data.
        :param doc_data: AiDocument Data List
        :return: Document Info Response List
        """
        for data in doc_data:
            doc_data_resp = self.get_doc_findings(data)
            self.doc_response["docs_findings"].append(doc_data_resp.model_dump())
        self.doc_response["docs_at_risk"] = self.docs_at_risk
        resp_dict = DocResp(**self.doc_response).model_dump()
        return resp_dict

    def get_app_doc_data(self, app_name: str) -> list:
        """
        This function return AiDocument data based on app name.
        :param app_name: App Name
        :return: AIDocument Data List
        """
        doc_data = []
        filter_query = {"appName": app_name}
        _, all_doc_data = self.db.query(
            table_obj=AiDocumentTable, filter_query=filter_query
        )

        if len(all_doc_data) == 0:
            raise Exception("Document with this app name does not exists.")

        for data in all_doc_data:
            doc_data.append(data.data)
        return doc_data

    def get_document_info(self) -> str:
        """
        This function return document info based on doc name
        :return: Doc Info
        """
        try:
            # create session
            self.db.create_session()
            doc_data = self.get_app_doc_data(self.app_name)
            doc_response = self.create_doc_response(doc_data)
            return json.dumps(doc_response, default=str, indent=4)
        except Exception as ex:
            logger.error(
                f"Error in getting document info for {self.app_name}. Error: {ex}"
            )
        finally:
            logger.debug(f"Get document info finished for {self.app_name}")
            # Closing session
            self.db.session.close()
