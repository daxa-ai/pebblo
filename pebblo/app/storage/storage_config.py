from pebblo.app.service import discovery_service as file_discovery_service
from pebblo.app.service import service as file_loader_doc_service
from pebblo.app.service.discovery import discovery_service as db_discovery_service
from pebblo.app.service.loader import loader_doc_service as db_loader_doc_service


class Storage:
    def __init__(self):
        self.obj = {
            "discovery": {
                "db": db_discovery_service.AppDiscover,
                "file": file_discovery_service.AppDiscover,
            },
            "loader": {
                "db": db_loader_doc_service.AppLoaderDoc,
                "file": file_loader_doc_service.AppLoaderDoc,
            },
        }

    def get_object(self, service, storage_type):
        return self.obj[service][storage_type]
