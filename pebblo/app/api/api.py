from fastapi import APIRouter, Depends
from pebblo.app.service.service import AppDiscover, AppLoaderDoc
from pebblo.app.config.config import load_config, Config
from functools import lru_cache
from typing import Annotated

creds_details = load_config(None)


@lru_cache
def get_settings():
    return Config()


def info_func(settings: Config = Depends(get_settings)):
    return {settings}

class App:
    """
        Controller Class for all the api endpoints for App resource.
    """
    def __init__(self, prefix: str):
        self.router = APIRouter(prefix=prefix)

    @staticmethod
    def discover(data: dict):
        # "/app/discover" API entrypoint
        discovery_obj = AppDiscover(data=data)
        response = discovery_obj.process_request()
        return response

    @staticmethod
    def loader_doc(data: dict):
        # "/loader/doc" API entrypoint
        loader_doc_obj = AppLoaderDoc(data=data)
        response = loader_doc_obj.process_request()
        return response
