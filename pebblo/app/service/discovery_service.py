"""
This module handles app discovery business logic.
"""

from datetime import datetime

from pydantic import ValidationError

from pebblo.app.enums.enums import ApplicationTypes, CacheDir
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
from pebblo.app.utils.utils import (
    acquire_lock,
    get_pebblo_server_version,
    read_json_file,
    release_lock,
    write_json_to_file,
)
from pebblo.log import get_logger

logger = get_logger(__name__)


class AppDiscover:
    """
    This class handles app discovery business logic.
    """

    def __init__(self):
        self.data = None
        self.application_name = None

    def _initialize_data(self, data):
        self.data = data
        self.application_name = data.get("name")
        self.load_id = data.get("load_id", None)

    @staticmethod
    def _get_current_datetime():
        """
        Return current datetime
        """
        return datetime.now()

    def _create_ai_apps_model(
        self, instance_details, chain_details, retrievals_details
    ):
        """
        Create an AI App Model and return the corresponding model object
        """
        logger.debug("Creating AI App model")
        # Initialize Variables
        last_used = self._get_current_datetime()
        metadata = Metadata(
            createdAt=self._get_current_datetime(),
            modifiedAt=self._get_current_datetime(),
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
            instanceDetails=instance_details,
            framework=self.data.get("framework"),
            lastUsed=last_used,
            pebbloServerVersion=get_pebblo_server_version(),
            pebbloClientVersion=self.data.get("plugin_version", ""),
            clientVersion=client_version,
            chains=chain_details,
            retrievals=retrievals_details,
        )
        return ai_apps_model.model_dump()

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
            createdAt=self._get_current_datetime(),
        )
        logger.debug(
            f"AI_APPS [{self.application_name}]: Instance Details: {instance_details_model.model_dump()}"
        )
        return instance_details_model

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
            chains.append(chain_obj.model_dump())

        logger.debug(f"Application Name [{self.application_name}]: Chains: {chains}")
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

    @staticmethod
    def _write_file_content_to_path(file_content, file_path):
        """
        Write content to the specified file path
        """
        # Writing file content to given file path
        write_json_to_file(file_content, file_path)

    @staticmethod
    def _read_file(file_path):
        """
        Retrieve the content of the specified file.
        """
        logger.debug(f"Reading content from file: {file_path}")
        file_content = read_json_file(file_path)
        return file_content

    def _upsert_app_metadata_file(self):
        """
        Update/Create app metadata file and write metadata for current run for loader type
        """
        # Read metadata file & get current app metadata
        app_metadata_file_path = (
            f"{CacheDir.HOME_DIR.value}/"
            f"{self.application_name}/{CacheDir.METADATA_FILE_PATH.value}"
        )
        app_metadata = self._read_file(app_metadata_file_path)

        # write metadata file if it is not present
        if not app_metadata:
            # Writing app metadata to metadata file
            app_metadata = {"name": self.application_name, "load_ids": [self.load_id]}
        else:
            if "load_ids" in app_metadata.keys():
                # Metadata file is already present,
                # Appending the current metadata details
                app_metadata.get("load_ids").append(self.load_id)
            else:
                # metadata file is present, but load_ids is not,
                # This is to support backward compatibility
                app_metadata["load_ids"] = [self.load_id]

        app_metadata["app_type"] = ApplicationTypes.LOADER.value
        # Writing metadata file
        self._write_file_content_to_path(app_metadata, app_metadata_file_path)

    def _upsert_metadata_file(self):
        """
        Update/Create app metadata file and write metadata for current run for retrieval type
        :return:
        """
        app_metadata_file_path = (
            f"{CacheDir.HOME_DIR.value}/"
            f"{self.application_name}/{CacheDir.METADATA_FILE_PATH.value}"
        )
        app_metadata = self._read_file(app_metadata_file_path)

        # write metadata file if it is not present
        if not app_metadata:
            # Writing app metadata to metadata file
            app_metadata = {
                "name": self.application_name,
                "app_type": ApplicationTypes.RETRIEVAL.value,
            }
        else:
            app_metadata["app_type"] = ApplicationTypes.RETRIEVAL.value

        # Writing metadata file
        self._write_file_content_to_path(app_metadata, app_metadata_file_path)

    def process_request(self, data):
        """
        Process App discovery Request. This handles discovery for loader as well as retrieval type applications.
        """
        self._initialize_data(data)
        lock_file_path = ""
        chain_details = []
        retrievals_details = []

        try:
            logger.debug("AI App discovery request processing started")
            logger.debug(f"AI_APP [{self.application_name}]: Input Data: {self.data}")

            # Handle loader type application.
            if self.load_id:
                lock_file_path = (
                    f"{CacheDir.HOME_DIR.value}/"
                    f"{self.application_name}/"
                    f"{CacheDir.METADATA_LOCK_FILE_PATH.value}"
                )
                file_path = (
                    f"{CacheDir.HOME_DIR.value}/{self.application_name}/{self.load_id}"
                    f"/{CacheDir.METADATA_FILE_PATH.value}"
                )
                self._upsert_app_metadata_file()

            # Handle retrieval type application.
            else:
                lock_file_path = (
                    f"{CacheDir.HOME_DIR.value}/"
                    f"{self.application_name}/"
                    f"{CacheDir.APPLICATION_METADATA_LOCK_FILE_PATH.value}"
                )
                file_path = (
                    f"{CacheDir.HOME_DIR.value}/{self.application_name}/"
                    f"/{CacheDir.APPLICATION_METADATA_FILE_PATH.value}"
                )
                self._upsert_metadata_file()

                # It's a Retrieval call, Fetching chain & retrievals details
                app_metadata = self._read_file(file_path=file_path)

                # Get chain details
                chain_details = self._fetch_chain_details(app_metadata)

                # get retrievals details
                retrievals_details = self._fetch_retrievals_details(app_metadata)

            acquire_lock(lock_file_path)

            # Get instance details
            instance_details = self._fetch_runtime_instance_details()

            # Create AiApps Model
            ai_apps = self._create_ai_apps_model(
                instance_details, chain_details, retrievals_details
            )

            # Write file to metadata location
            self._write_file_content_to_path(ai_apps, file_path)

            # Prepare response
            message = "App Discover Request Processed Successfully"
            response = DiscoverAIAppsResponseModel(
                pebblo_server_version=ai_apps.get("pebbloServerVersion"),
                message=message,
            )
            return PebbloJsonResponse.build(
                body=response.model_dump(exclude_none=True), status_code=200
            )
        except ValidationError as ex:
            response = DiscoverAIAppsResponseModel(
                pebblo_server_version=None, message=str(ex)
            )
            logger.error(f"Error in Discovery API process_request. Error: {ex}")
            return PebbloJsonResponse.build(
                body=response.model_dump(exclude_none=True), status_code=400
            )
        except Exception as ex:
            response = DiscoverAIAppsResponseModel(
                pebblo_server_version=None, message=str(ex)
            )
            logger.error(f"Error in Discovery API process_request. Error: {ex}")
            return PebbloJsonResponse.build(
                body=response.model_dump(exclude_none=True), status_code=500
            )
        finally:
            release_lock(lock_file_path)
