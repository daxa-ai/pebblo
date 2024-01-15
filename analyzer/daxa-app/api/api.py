# Copyright (c) 2024 Daxa. All rights reserved.
from fastapi import APIRouter
from service.service import AppDiscover, AppLoaderDoc
from utils.utils import get_run_id


class App:
    """
        Controller Class for all the api endpoints for App resource.
    """
    def __init__(self, prefix: str):
        self.router = APIRouter(prefix=prefix)

    @staticmethod
    def discover(data: dict):
        # "/discover" API Entrypoint
        # Get run id
        run_id = get_run_id()
        discovery_obj = AppDiscover(data=data, run_id=run_id)
        response = discovery_obj.process_request()
        return response

    @staticmethod
    def loader_doc(data: dict):
        # "/loader/doc"
        loader_doc_obj = AppLoaderDoc(data=data)
        response = loader_doc_obj.process_request()
        return response
