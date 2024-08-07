from pebblo.app.enums.enums import StorageTypes
from pebblo.app.service.db_discovery_service import DBAppDiscover
from pebblo.app.service.discovery_service import AppDiscover
from pebblo.app.service.loader_db import DBLoaderDoc
from pebblo.app.service.service import AppLoaderDoc


class Storage:

    def get_laoder_doc_object(self, storage_type, data):
        if storage_type == StorageTypes.FILE.value:
            return AppLoaderDoc(data=data)
            # return object based on a storage type

        if storage_type == StorageTypes.DATABASE.value:
            return DBLoaderDoc(data=data)

    def get_discovery_object(self, storage_type, data):
        if storage_type == StorageTypes.FILE.value:
            return AppDiscover(data=data)
        if storage_type == StorageTypes.DATABASE.value:
            return DBAppDiscover(data=data)
