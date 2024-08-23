# Discovery API with database implementation.

from pebblo.app.enums.enums import ApplicationTypes
from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.db_models import (
    AiApp,
    AiDataLoader,
    Chain,
    FrameworkInfo,
    InstanceDetails,
    Metadata,
    PackageInfo,
    VectorDB,
)
from pebblo.app.models.models import DiscoverAIAppsResponseModel
from pebblo.app.models.sqltables import AiAppTable, AiDataLoaderTable
from pebblo.app.service.discovery.common import get_or_create_app
from pebblo.app.storage.sqlite_db import SQLiteClient
from pebblo.app.utils.utils import get_current_time, get_pebblo_server_version, timeit
from pebblo.log import get_logger

logger = get_logger(__name__)


class AppDiscover:
    def __init__(self):
        self.db = None
        self.data = None
        self.app_name = None

    @staticmethod
    def return_response(message, status_code, pebblo_server_version=None):
        response = DiscoverAIAppsResponseModel(
            pebblo_server_version=pebblo_server_version,
            message=str(message),
        )
        return PebbloJsonResponse.build(
            body=response.dict(exclude_none=True), status_code=status_code
        )

    def _fetch_runtime_instance_details(self) -> InstanceDetails:
        """
        Retrieve instance details from input data and return its corresponding model object.
        """
        logger.debug("Retrieving instance details from input data.")
        # Fetching runtime instance details
        runtime_dict = self.data.get("runtime", {})
        instance_details_model = InstanceDetails(
            language=runtime_dict.get("language"),
            languageVersion=runtime_dict.get("language_version"),
            host=runtime_dict.get("host"),
            ip=runtime_dict.get("ip"),
            path=runtime_dict.get("path"),
            runtime=runtime_dict.get("runtime"),
            type=runtime_dict.get("type"),
            platform=runtime_dict.get("platform"),
            os=runtime_dict.get("os"),
            osVersion=runtime_dict.get("os_version"),
            createdAt=get_current_time(),
        )
        logger.debug(f"AiApp Name [{self.app_name}]")
        return instance_details_model

    def create_app_obj(
        self, ai_app, instance_details, chain_details, retrievals_details, app_type
    ):
        """
        Create an AI App Model and return the corresponding model object
        """
        logger.debug("Creating App model object")
        # Initialize Variables
        current_time = get_current_time()

        metadata = Metadata(createdAt=current_time, modifiedAt=current_time)
        client_version = FrameworkInfo(
            name=self.data.get("client_version", {}).get("name"),
            version=self.data.get("client_version", {}).get("version"),
        )
        ai_app_obj = {
            "metadata": metadata,
            "description": self.data.get("description", "-"),
            "owner": self.data.get("owner", ""),
            "pluginVersion": self.data.get("plugin_version"),
            "instanceDetails": instance_details,
            "framework": self.data.get("framework"),
            "lastUsed": current_time,
            "pebbloServerVersion": get_pebblo_server_version(),
            "pebbloClientVersion": self.data.get("plugin_version", ""),
            "clientVersion": client_version,
            "chains": chain_details,
            "retrievals": retrievals_details,
        }
        ai_app.update(ai_app_obj)

        AppModel = None
        if app_type == ApplicationTypes.LOADER.value:
            AppModel = AiDataLoader
        elif app_type == ApplicationTypes.RETRIEVAL.value:
            AppModel = AiApp
        model_obj = AppModel(**ai_app)
        return model_obj.dict()

    def _get_app_type_and_class(self):
        AppClass = None
        app_type = None
        load_id = self.data.get("load_id") or None
        if load_id:
            AppClass = AiDataLoaderTable
            app_type = ApplicationTypes.LOADER.value
        else:
            AppClass = AiAppTable
            app_type = ApplicationTypes.RETRIEVAL.value

        return app_type, AppClass

    def _fetch_chain_details(self, app_metadata) -> list[Chain]:
        """
        Retrieve chain details from input data and return its corresponding model object.
        """
        # TODO: Discussion on the uniqueness of chains is not done yet,
        #  so for now we are appending chain to existing chains in the file for this app.
        logger.debug("Updating app chains details from input chain details")
        chains = list()

        if app_metadata:
            chains = app_metadata.get("chains", [])

        for chain in self.data.get("chains", []):
            name = chain["name"]
            model = chain["model"]
            # vector db details
            vector_db_details = []
            for vector_db in chain.get("vector_dbs", []):
                vector_db_obj = VectorDB(
                    name=vector_db.get("name"),
                    version=vector_db.get("version"),
                    location=vector_db.get("location"),
                    embeddingModel=vector_db.get("embedding_model"),
                    pkgInfo=None,
                )

                package_info = vector_db.get("pkg_info")
                if package_info:
                    pkg_info_obj = PackageInfo(
                        projectHomePage=package_info.get("project_home_page"),
                        documentationUrl=package_info.get("documentation_url"),
                        pypiUrl=package_info.get("pypi_url"),
                        licenceType=package_info.get("licence_type"),
                        installedVia=package_info.get("installed_via"),
                        location=package_info.get("location"),
                    )
                    vector_db_obj.pkgInfo = pkg_info_obj

                vector_db_details.append(vector_db_obj)
            chain_obj = Chain(name=name, model=model, vectorDbs=vector_db_details)
            chains.append(chain_obj.dict())

        logger.debug(f"Application Name [{self.app_name}]")
        return chains

    def _fetch_retrievals_details(self, app_metadata) -> list:
        """
        Retrieve existing retrievals details from metadata file and append the new retrieval details
        """
        logger.debug("Updating app retrievals details with input retrieval details")
        retrievals_details = list()

        if app_metadata:
            retrievals_details = app_metadata.get("retrievals", [])

        input_retrievals_details = self.data.get("retrievals", [])
        retrievals_details.extend(input_retrievals_details)

        return retrievals_details

    @timeit
    def process_request(self, data):
        try:
            self.db = SQLiteClient()
            self.data = data
            self.app_name = data.get("name")

            logger.debug("Discovery API request started")

            # create session
            self.db.create_session()

            chain_details = []
            retrievals_details = []
            app_type, AppClass = self._get_app_type_and_class()
            if not AppClass:
                message = "No load_id's or run_id's are present, Invalid Request"
                return self.return_response(message=message, status_code=404)

            # get or create app
            ai_app_obj = get_or_create_app(
                self.db, self.app_name, AppClass, self.data, app_type
            )
            if not ai_app_obj:
                message = "Unable to get or create aiapp details"
                return self.return_response(message=message, status_code=500)

            ai_app = ai_app_obj.data
            # Get instance details
            instance_details = self._fetch_runtime_instance_details()

            if app_type == ApplicationTypes.RETRIEVAL.value:
                # its retrieval application

                # Get chain details
                chain_details = self._fetch_chain_details(ai_app)

                # get retrieval details
                retrievals_details = self._fetch_retrievals_details(ai_app)

            # Create AiApp Model
            ai_apps_data = self.create_app_obj(
                ai_app,
                instance_details=instance_details,
                chain_details=chain_details,
                retrievals_details=retrievals_details,
                app_type=app_type,
            )

            status, message = self.db.update_data(
                table_obj=ai_app_obj, data=ai_apps_data
            )
            if not status:
                logger.error(f"Process request failed: {message}")
                return self.return_response(message=message, status_code=500)

        except Exception as err:
            logger.error(f"Discovery api failed, Error: {err}")
            # Getting error, We are rollback everything we did in this run.
            self.db.session.rollback()
            return self.return_response(
                message=f"Discovery api failed, Error: {err}", status_code=500
            )

        else:
            # Commit will only happen when everything went well.
            message = "App Discover Request Processed Successfully"

            logger.debug(message)
            self.db.session.commit()

            return self.return_response(
                message=message,
                status_code=200,
                pebblo_server_version=ai_app.get("pebbloServerVersion"),
            )
        finally:
            logger.debug("Closing database session.")
            # Closing the session
            self.db.session.close()
