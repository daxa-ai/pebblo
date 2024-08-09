from fastapi import APIRouter

from pebblo.app.config.config import var_server_config_dict
from pebblo.app.enums.common import StorageTypes
from pebblo.app.service.prompt_gov import PromptGov
from pebblo.app.storage.storage_config import Storage

config_details = var_server_config_dict.get()


class App:
    """
    Controller Class for all the api endpoints for App resource.
    """

    def __init__(self, prefix: str):
        self.router = APIRouter(prefix=prefix)

    @staticmethod
    def discover(data: dict):
        # "/app/discover" API entrypoint
        # Execute discover object based on a storage type
        storage_type = config_details.get("storage", {}).get(
            "type", StorageTypes.FILE.value
        )

        storage_obj = Storage()
        discovery = storage_obj.get_object("discovery", storage_type)
        discovery_obj = discovery(data)
        response = discovery_obj.process_request()
        return response

    @staticmethod
    def loader_doc(data: dict):
        # "/loader/doc" API entrypoint
        # Execute loader doc object based on a storage type
        storage_type = config_details.get("storage", {}).get(
            "type", StorageTypes.FILE.value
        )

        storage_obj = Storage()
        loader_doc = storage_obj.get_object("storage", storage_type)
        loader_doc_obj = loader_doc(data)
        response = loader_doc_obj.process_request()
        return response

    @staticmethod
    def prompt(data: dict):
        # "/prompt" API entrypoint
        # Execute discover object based on a storage type
        storage_type = config_details.get("storage", {}).get(
            "type", StorageTypes.FILE.value
        )

        storage_obj = Storage()
        prompt_obj = storage_obj.get_prompt_obj(storage_type, data)
        response = prompt_obj.process_request()
        return response

    @staticmethod
    def promptgov(data: dict):
        # "/prompt/governance" API entrypoint
        prompt_obj = PromptGov(data=data)
        response = prompt_obj.process_request()
        return response
