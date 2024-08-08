from pebblo.app.enums.common import StorageTypes
from pebblo.app.service import discovery_service as file_discovery_service
from pebblo.app.service.discovery import discovery_service as db_discovery_service
from pebblo.app.service import service as file_loader_doc_service
from pebblo.app.service.loader import loader_doc_service as db_loader_doc_service


class Storage:
    @staticmethod
    def get_discovery_object(storage_type, data):
        if storage_type == StorageTypes.FILE.value:
            return file_discovery_service.AppDiscover(data=data)
        if storage_type == StorageTypes.DATABASE.value:
            return db_discovery_service.AppDiscover(data=data)

    @staticmethod
    def get_loader_doc_object(storage_type, data):
        # return object based on a storage type
        if storage_type == StorageTypes.FILE.value:
            return file_loader_doc_service.AppLoaderDoc(data=data)

        if storage_type == StorageTypes.DATABASE.value:
            return db_loader_doc_service.AppLoaderDoc(data=data)
