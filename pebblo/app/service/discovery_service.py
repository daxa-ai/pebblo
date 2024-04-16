"""
This module handles app discovery business logic.
"""

from datetime import datetime

from pydantic import ValidationError

from pebblo.app.enums.enums import CacheDir
from pebblo.app.libs.logger import logger
from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.models import (
    AiApp,
    Chain,
    DiscoverAIApps,
    DiscoverAIAppsResponseModel,
    InstanceDetails,
    Metadata,
    PackageInfo,
    VectorDB
)
from pebblo.app.utils.utils import (
    get_pebblo_server_version,
    read_json_file,
    write_json_to_file,
    acquire_lock,
    release_lock
)


class AppDiscover:
    """
    This class handles app discovery business logic.
    """

    def __init__(self, data: dict):
        self.data = data
        self.load_id = data.get("load_id")
        self.application_name = self.data.get("name")

    def _create_ai_apps_model(self, instance_details, chain_details):
        """
        Create an AI App Model and return the corresponding model object
        """
        logger.debug("Creating AI App model")
        # Initialize Variables
        last_used = datetime.now()
        metadata = Metadata(createdAt=datetime.now(), modifiedAt=datetime.now())
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
            chains=chain_details,
        )
        return ai_apps_model

    def _fetch_runtime_instance_details(self):
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
            createdAt=datetime.now(),
        )
        logger.debug(
            f"AI_APPS [{self.application_name}]: Instance Details: {instance_details_model.dict()}"
        )
        return instance_details_model

    def _fetch_chain_details(self):
        # get chain details
        chains = list()
        for chain in self.data.get('chains', []):
            name = chain["name"]
            model = chain['model']
            # vector db details
            vector_db_details = []
            for vector_db in chain.get('vector_dbs', []):
                vector_db_obj = VectorDb(name=vector_db.get("name"),
                                         version=vector_db.get("version"),
                                         location=vector_db.get("location"),
                                         embeddingModel=vector_db.get("embedding_model"))

                package_info = vector_db.get("pkg_info")
                if package_info:
                    pkg_info_obj = PackageInfo(projectHomePage=package_info.get("project_home_page"),
                                               documentationUrl=package_info.get("documentation_url"),
                                               pypiUrl=package_info.get("pypi_url"),
                                               licenceType=package_info.get("licence_type"),
                                               installedVia=package_info.get("installed_via"),
                                               location=package_info.get("location"))
                    vector_db_obj.packageInfo = pkg_info_obj.dict()

                vector_db_details.append(vector_db_obj.dict())
            chain_obj = Chain(name=name, model=model, vectorDbs=vector_db_details)
            chains.append(chain_obj.dict())

        logger.debug(f"Application Name [{self.application_name}]: Chains: {chains}")
        return chains

    @staticmethod
    def _write_file_content_to_path(file_content, file_path):
        """
        Write content to the specified file path
        """
        logger.debug(f"Writing content to file path: {file_content}")
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
        Update/Create app metadata file and write metadata for current run
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

        # Writing metadata file
        self._write_file_content_to_path(app_metadata, app_metadata_file_path)

    def process_request(self):
        """
        Process App discovery Request
        """
        try:
            logger.debug("AI App discovery request processing started")
            # Input Data
            logger.debug(f"AI_APP [{self.application_name}]: Input Data: {self.data}")

            # Upset metadata file
            if self.load_id:
                self._upsert_app_metadata_file()

            # getting instance details
            instance_details = self._fetch_runtime_instance_details()

            chain_details = self._fetch_chain_details()

            # create AiApps Model
            ai_apps = self._create_ai_apps_model(instance_details, chain_details)

            # Write file to metadata location
            # loader type application, if load_id is present
            if self.load_id:
                file_path = (
                    f"{CacheDir.HOME_DIR.value}/{self.application_name}/{self.load_id}"
                    f"/{CacheDir.METADATA_FILE_PATH.value}"
                )

            # retrieval type application, if load_id is not present
            else:
                file_path = (
                    f"{CacheDir.HOME_DIR.value}/{self.application_name}/"
                    f"/{CacheDir.APPLICATION_METADATA_FILE_PATH.value}"
                )

            # Lock Implementation
            try:
                acquire_lock(CacheDir.APPLICATION_METADATA_LOCK_FILE_PATH)
                self._write_file_content_to_path(ai_apps.dict(), file_path)
            finally:
                release_lock(CacheDir.APPLICATION_METADATA_LOCK_FILE_PATH)

            ai_apps_data = ai_apps.dict()
            ai_apps_obj = DiscoverAIApps(
                name=ai_apps_data.get("name"),
                description=ai_apps_data.get("description"),
                owner=ai_apps_data.get("owner"),
                instanceDetails=ai_apps_data.get("instanceDetails"),
                framework=ai_apps_data.get("framework"),
                lastUsed=ai_apps_data.get("lastUsed"),
                pebbloServerVersion=ai_apps_data.get("pebbloServerVersion"),
                pebbloClientVersion=ai_apps_data.get("pebbloClientVersion"),
            )
            message = "App Discover Request Processed Successfully"
            logger.debug(message)
            response = DiscoverAIAppsResponseModel(
                ai_apps_data=ai_apps_obj, message=message
            )
            return PebbloJsonResponse.build(
                body=response.dict(exclude_none=True), status_code=200
            )
        except ValidationError as ex:
            response = DiscoverAIAppsResponseModel(ai_apps_data=None, message=str(ex))
            logger.error(f"Error in Discovery API process_request. Error:{ex}")
            return PebbloJsonResponse.build(
                body=response.dict(exclude_none=True), status_code=400
            )
        except Exception as ex:
            response = DiscoverAIAppsResponseModel(ai_apps_data=None, message=str(ex))
            logger.error(f"Error in Discovery API process_request. Error:{ex}")
            return PebbloJsonResponse.build(
                body=response.dict(exclude_none=True), status_code=500
            )
        finally:
            # TODO : Implement release lock
            # Really it is required here ??
            pass
