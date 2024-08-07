# Discovery API with database implementation.
import datetime

from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.models import (
    AiApp,
    Chain,
    DiscoverAIAppsResponseModel,
    FrameworkInfo,
    InstanceDetails,
    Metadata,
    PackageInfo,
    VectorDB,
)
from pebblo.app.models.sqltable import AiAppsTable
from pebblo.app.storage.sqlite_db import SQLiteClient
from pebblo.app.utils.utils import get_pebblo_server_version
from pebblo.log import get_logger

logger = get_logger(__name__)


class DBAppDiscover:

    def __init__(self, data):
        self.db = SQLiteClient()
        self.data = data
        self.app_name = data.get("name")

    def create_ai_app_model(self):
        """
                Create an AI App Model and return the corresponding model object
                """
        logger.debug("Creating AI App model")
        # Initialize Variables
        last_used = datetime.datetime.now() # self._get_current_datetime()

        metadata = Metadata(
            createdAt=datetime.datetime.now(), # self._get_current_datetime(),
            modifiedAt=datetime.datetime.now() #self._get_current_datetime(),
        )
        client_version = FrameworkInfo(
            name=self.data.get("client_version", {}).get("name"),
            version=self.data.get("client_version", {}).get("version"),
        )
        ai_apps_model = AiApp(
            metadata=metadata,
            name=self.data.get("name"),
            description=self.data.get("description", "-"),
            owner=self.data.get("owner", ""),
            pluginVersion=self.data.get("plugin_version"),
            # instanceDetails=instance_details,
            framework=self.data.get("framework"),
            # lastUsed=last_used,
            pebbloServerVersion=get_pebblo_server_version(),
            pebbloClientVersion=self.data.get("plugin_version", ""),
            clientVersion=client_version,
            # chains=chain_details,
            # retrievals=retrievals_details,
        )
        return ai_apps_model.dict()

    def process_request(self):

        ai_apps = self.create_ai_app_model()
        response = self.db.insert_ai_app(ai_apps)
        print(f"Insert Response: {response}")

        # Fetch ai apps details
        ai_app_coll = AiAppsTable # define in config
        output = self.db.get_ai_apps(ai_app_coll)
        print("Fetch AiApps Data")
        for res in output:
            print(res.data)
            # Prepare response
            message = "App Discover Request Processed Successfully"
            response = DiscoverAIAppsResponseModel(
                pebblo_server_version=ai_apps.get("pebbloServerVersion"),
                message=message,
            )
            return PebbloJsonResponse.build(
                body=response.dict(exclude_none=True), status_code=200
            )
