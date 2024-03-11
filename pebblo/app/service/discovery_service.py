"""
This module handles app discovery business logic.
"""

from datetime import datetime

from fastapi import HTTPException
from pydantic import ValidationError

from pebblo.app.enums.enums import CacheDir
from pebblo.app.libs.logger import logger
from pebblo.app.models.models import AiApp, InstanceDetails, Metadata
from pebblo.app.utils.utils import read_json_file, write_json_to_file


class AppDiscover:
    """
    This class handles app discovery business logic.
    """

    def __init__(self, data: dict):
        self.data = data
        self.load_id = data.get("load_id", None)
        self.run_id = data.get("run_id", None)
        self.application_name = self.data.get("name")

    def _create_ai_apps_model(self, instance_details):
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

    @staticmethod
    def _write_file_content_to_path(file_content, file_path):
        """
        Write content to the specified file path
        """
        # logger.debug(f"Writing content to file path: {file_content}")
        # Writing file content to given file path
        write_json_to_file(file_content, file_path)

    @staticmethod
    def _read_file(file_path):
        """
        Retrieve the content of the specified file.
        """
        # logger.debug(f"Reading content from file: {file_path}")
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
            if self.run_id:
                app_metadata = {"name": self.application_name, "run_ids": {self.run_id: [self.load_id]}}
            else:
                app_metadata = {"name": self.application_name, "load_ids": [self.load_id]}
        else:
            # For multiple loaders support.
            if self.run_id:
                # Already run_id is present
                if "run_ids" in app_metadata.keys():
                    if self.run_id in app_metadata["run_ids"].keys():
                        app_metadata["run_ids"][self.run_id].append(self.load_id)
                    else:
                        app_metadata["run_ids"][self.run_id] = [self.load_id]

                # This is first load of this run_id
                else:
                    app_metadata["run_ids"] = {self.run_id: [self.load_id]}

            # Backward compatibility of multiple loaders support.
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
            self._upsert_app_metadata_file()

            # getting instance details
            instance_details = self._fetch_runtime_instance_details()

            # create AiApps Model
            ai_apps = self._create_ai_apps_model(instance_details)

            # Write file to metadata location
            load_dir_file_path = (
                f"{CacheDir.HOME_DIR.value}/{self.application_name}/{self.load_id}"
                f"/{CacheDir.METADATA_FILE_PATH.value}"
            )
            self._write_file_content_to_path(ai_apps.dict(), load_dir_file_path)

            #TODO: We are writing app metadata to load id metadata.json but what we should write for runId metadata.json same data\
            # or appending the existing values
            # Write file to metadata location
            if self.run_id:
                run_dir_file_path = (
                    f"{CacheDir.HOME_DIR.value}/{self.application_name}/{self.run_id}"
                    f"/{CacheDir.METADATA_FILE_PATH.value}"
                )
                self._write_file_content_to_path(ai_apps.dict(), run_dir_file_path) # content should be change

            logger.debug("AiApp discovery request completed successfully")
            return {"message": "App Discover Request Processed Successfully"}
        except ValidationError as ex:
            logger.error(f"Error in process_request. Error:{ex}")
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            logger.error(f"Error in process_request. Error:{ex}")
            raise HTTPException(status_code=500, detail=str(ex))
