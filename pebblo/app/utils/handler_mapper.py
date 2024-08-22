from pebblo.app.config.config import var_server_config_dict
from pebblo.app.enums.common import StorageTypes
from pebblo.app.service import discovery_service as file_discovery_service
from pebblo.app.service import prompt_service as file_prompt_service
from pebblo.app.service import service as file_loader_doc_service
from pebblo.app.service.discovery import discovery_service as db_discovery_service
from pebblo.app.service.loader import loader_doc_service as db_loader_doc_service
from pebblo.app.service.prompt import prompt_service as db_prompt_service

api_handler_map = {
    "discover": {
        "db": db_discovery_service.AppDiscover,
        "file": file_discovery_service.AppDiscover,
    },
    "loader": {
        "db": db_loader_doc_service.AppLoaderDoc,
        "file": file_loader_doc_service.AppLoaderDoc,
    },
    "prompt": {
        "db": db_prompt_service.Prompt,
        "file": file_prompt_service.Prompt,
    },
}


config_details = var_server_config_dict.get()


def get_handler(handler_name: str):
    try:
        storage_type = config_details.get("storage", {}).get(
            "type", StorageTypes.FILE.value
        )

        handler_class = api_handler_map.get(handler_name, {}).get(storage_type, None)
        if handler_class is None:
            raise ValueError(
                f"{handler_name} handler or {storage_type} storage type not found in dictionary"
            )
        return handler_class()
    except Exception as e:
        print(f"Please pass correct arguments. Exception: {e}")
