from pebblo.app.enums.enums import StorageTypes
from pebblo.app.service import db_discovery_service, discovery_service
from pebblo.app.service import loader_db, service


class Storage:

    def get_laoder_doc_object(self, storage_type, data):

        # return object based on a storage type
        if storage_type == StorageTypes.FILE.value:
            return service.AppLoaderDoc(data=data)

        if storage_type == StorageTypes.DATABASE.value:
            return loader_db.AppLoaderDoc(data=data)

    def get_discovery_object(self, storage_type, data):
        if storage_type == StorageTypes.FILE.value:
            return discovery_service.AppDiscover(data=data)
        if storage_type == StorageTypes.DATABASE.value:
            return db_discovery_service.AppDiscover(data=data)
