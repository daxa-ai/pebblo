import json

from fastapi import APIRouter, HTTPException

from pebblo.app.config.config import var_server_config_dict
from pebblo.app.service.data_gov.document_handler import DataGov
from pebblo.app.service.local_ui_service import AppData

config_details = var_server_config_dict.get()


class DataGovApp:
    """
    Controller Class for all the API endpoints for DataGovApp resource.
    """

    def __init__(self, prefix: str):
        self.router = APIRouter(prefix=prefix)

    @staticmethod
    def get_all_apps_details():
        try:
            app_data = AppData()
            data = json.loads(app_data.get_all_apps_details())
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_app_details(app_name):
        try:
            app_data = AppData()
            data = json.loads(app_data.get_app_details(app_name))
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_document_info(app_name):
        try:
            data_gov_obj = DataGov(app_name)
            data = data_gov_obj.get_document_info()
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
