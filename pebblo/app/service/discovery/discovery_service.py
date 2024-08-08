# Discovery API with database implementation.
from datetime import datetime

from sqlalchemy.inspection import inspect

from pebblo.app.models.models import (
    AiApp,
    Chain,
    FrameworkInfo,
    InstanceDetails,
    Metadata,
    PackageInfo,
    VectorDB,
)
from pebblo.app.models.sqltable import AiAppTable, AiDataLoaderTable
from pebblo.app.service.discovery.common import get_or_create_app
from pebblo.app.storage.sqlite_db import SQLiteClient
from pebblo.app.utils.utils import get_pebblo_server_version, return_response
from pebblo.log import get_logger

logger = get_logger(__name__)


class AppDiscover:
    def __init__(self, data):
        self.db = SQLiteClient()
        self.data = data
        self.app_name = data.get("name")

    @staticmethod
    def _get_current_datetime():
        """
        Return current datetime
        """
        return datetime.now().isoformat()

    def _fetch_runtime_instance_details(self) -> InstanceDetails:
        """
        Retrieve instance details from input data and return its corresponding model object.
        """
        logger.debug("Retrieving instance details from input data")
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
            createdAt=self._get_current_datetime()
        )
        logger.debug(
            f"AI_APPS [{self.app_name}]: Instance Details: {instance_details_model.dict()}"
        )
        return instance_details_model

    def create_ai_app_model(
        self, ai_app, instance_details, chain_details, retrievals_details
    ):
        """
        Create an AI App Model and return the corresponding model object
        """
        logger.debug("Creating AI App model")
        # Initialize Variables
        current_time = self._get_current_datetime()
        last_used = current_time

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
            "lastUsed": last_used,
            "pebbloServerVersion": get_pebblo_server_version(),
            "pebbloClientVersion": self.data.get("plugin_version", ""),
            "clientVersion": client_version,
            "chains": chain_details,
            "retrievals": retrievals_details,
        }
        ai_app.update(ai_app_obj)
        ai_apps_model = AiApp(**ai_app)
        return ai_apps_model.dict()

    def _get_app_class(self):
        AppClass = None
        load_id = self.data.get("load_id") or None
        if load_id:
            AppClass = AiDataLoaderTable
        else:
            AppClass = AiAppTable

        return AppClass

    def model_to_dict(self, instance):
        """Convert SQLAlchemy model instance to dictionary."""
        if instance:
            # Use SQLAlchemy's inspection to get the column attributes
            mapper = inspect(instance).mapper
            return {
                column.key: getattr(instance, column.key) for column in mapper.columns
            }
        return {}

    def _fetch_chain_details(self, app_metadata) -> list[Chain]:
        """
        Retrieve chain details from input data and return its corresponding model object.
        """
        # TODO: Discussion on the uniqueness of chains is not done yet,
        #  so for now we are appending chain to existing chains in the file for this app.

        chains = list()

        if app_metadata:
            chains = app_metadata.get("chains", [])
            logger.debug(f"Existing Chains : {chains}")

        logger.debug(f"Input chains : {self.data.get('chains', [])}")
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

        logger.debug(f"Application Name [{self.app_name}]: Chains: {chains}")
        return chains

    def _fetch_retrievals_details(self, app_metadata) -> list:
        """
        Retrieve existing retrievals details from metadata file and append the new retrieval details
        """

        retrievals_details = list()

        if app_metadata:
            retrievals_details = app_metadata.get("retrievals", [])

        input_retrievals_details = self.data.get("retrievals", [])
        logger.debug(f"Input retrievals : {input_retrievals_details}")
        retrievals_details.extend(input_retrievals_details)

        return retrievals_details

    def process_request(self):
        try:
            logger.info("Discovery API Request.")
            chain_details = []
            retrievals_details = []
            load_id = self.data.get("load_id") or None

            AppClass = self._get_app_class()
            if not AppClass:
                message = "No load_id's or run_id's are present, Invalid Request"
                return return_response(message=message, status_code=404)

            # create session
            self.db.create_session()

            # get or create app
            ai_app_obj = get_or_create_app(self.db, self.app_name, AppClass)
            if not ai_app_obj:
                message = "Unable to get or create aiapp details"
                return return_response(message=message, status_code=500)

            ai_app = ai_app_obj.data
            logger.info(f"AiApp data: {ai_app}")
            # Get instance details
            instance_details = self._fetch_runtime_instance_details()

            if load_id is None:
                # its retrieval application

                # Get chain details
                chain_details = self._fetch_chain_details(ai_app)

                # get retrieval details
                retrievals_details = self._fetch_retrievals_details(ai_app)

            # Create AiApp Model
            ai_apps_data = self.create_ai_app_model(
                ai_app,
                instance_details=instance_details,
                chain_details=chain_details,
                retrievals_details=retrievals_details,
            )

            status, message = self.db.update_data(
                table_obj=ai_app_obj, data=ai_apps_data
            )
            if not status:
                logger.error(f"Process request failed: {message}")
                return return_response(message=message, status_code=500)

            # Fetch ai apps details
            # status, output = self.db.get_objects(AiAppTable)
            # if not status:
            #     return return_response(message=output, status_code=500)
            #
            # for response in output:
            #     logger.debug(f"Discovery Response: {response.data}")

        except Exception as err:
            logger.error(f"Discovery api failed, Error: {err}")
            # Getting error, We are rollback everything we did in this run.
            self.db.session.rollback()
            return return_response(
                message=f"Discovery api failed, Error: {err}", status_code=500
            )

        else:
            # Commit will only happen when everything went well.
            message = "App Discover Request Processed Successfully"
            logger.info(message)
            self.db.session.commit()

            return return_response(message=message, status_code=200)
        finally:
            logger.debug("Closing database session.")
            # Closing the session
            self.db.session.close()
