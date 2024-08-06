from pebblo.app.enums.enums import StorageTypes
from pebblo.app.service.service import AppLoaderDoc


class Storage:

    @staticmethod
    def get_object(storage_type, data):
        if storage_type == StorageTypes.FILE.value:
            return AppLoaderDoc(data=data)
            # return object based on a storage type

        if storage_type == StorageTypes.DATABASE.value:
            pass

