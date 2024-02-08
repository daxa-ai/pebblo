from datetime import datetime
from pebblo.reports.reports import Reports
from pebblo.app.enums.enums import CacheDir
from pebblo.app.utils.utils import write_json_to_file, read_json_file, get_full_path
from pebblo.app.libs.logger import logger
from pebblo.app.models.models import LoaderMetadata, Metadata, AiApp, InstanceDetails
from pebblo.app.service.doc_helper import DocHelper
from pydantic import ValidationError
from fastapi import HTTPException


class AppDiscover:
    def __init__(self, data: dict):
        self.data = data
        self.load_id = data.get('load_id')

    def process_request(self):
        """
            Process AI App discovery Request
            """
        try:
            application_name = self.data.get("name")
            owner = self.data.get("owner")
            logger.debug(f"AI_APP [{application_name}]: Input Data: {self.data}")

            # Writing app metadata file
            file_context = {"name": application_name, "current_load_id": self.load_id}
            file_path = f"{CacheDir.home_dir.value}/{application_name}/{CacheDir.metadata_file_path.value}"
            write_json_to_file(file_context, file_path)

            # getting instance details
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
                osVersion=runtime_dict.get("os_version")
            )
            logger.debug(f"AI_APPS [{application_name}]: Instance Details: {instance_details_model.dict()}")

            last_used = datetime.now()
            metadata = Metadata(
                createdAt=datetime.now(),
                modifiedAt=datetime.now()
            )

            ai_apps_model = AiApp(
                metadata=metadata,
                name=application_name,
                description=self.data.get("description", " "),
                owner=owner,
                pluginVersion=self.data.get("plugin_version"),
                instanceDetails=instance_details_model,
                framework=self.data.get("framework"),
                lastUsed=last_used
            )
            logger.debug(f"Final Output For Discovery Call: {ai_apps_model.dict()}")
            file_path = f"{CacheDir.home_dir.value}/{application_name}/{self.load_id}/{CacheDir.metadata_file_path.value}"
            write_json_to_file(ai_apps_model.dict(), file_path)
            logger.info("App Discover Request Processed Successfully")
            return {"message": "App Discover Request Processed Successfully"}
        except ValidationError as ex:
            logger.error(f"Error in process_request. Error:{ex}")
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            logger.error(f"Error in process_request. Error:{ex}")
            raise HTTPException(status_code=500, detail="Internal Server Error")


class AppLoaderDoc:
    def __init__(self, data):
        self.data = data

    def process_request(self):
        """This process is entrypoint function for loader doc API implementation."""
        logger.debug(f"Loader Doc, Input Data: {self.data}")

        try:
            app_name = self.data.get("name")
            logger.debug(f"AI Loader Doc, AppName: {app_name}")

            # Read metadata file & get current load details
            app_metadata_file_path = f"{CacheDir.home_dir.value}/{app_name}/{CacheDir.metadata_file_path.value}"
            app_metadata = read_json_file(app_metadata_file_path)
            if not app_metadata:
                return {"Message": "App details not present, Please call discovery api first"}

            prev_load_id = app_metadata.get("current_load_id")
            load_id = self.data['load_id']

            # Get current app details from load id
            report_file_path = f"{CacheDir.home_dir.value}/{app_name}/{load_id}/{CacheDir.report_file_name.value}"
            app_load_metadata_file_path = f"{CacheDir.home_dir.value}/{app_name}/{load_id}/{CacheDir.metadata_file_path.value}"
            app_details = read_json_file(app_load_metadata_file_path)
            if not app_details:
                # TODO: Handle the case where discover call did not happen, but loader doc is being called.
                logger.error("Could not read metadata file. Exiting.")
                return

            # Get Loader Details from input
            loader_details = self.data.get("loader_details", {})
            loader_name = loader_details.get('loader', None)
            source_type = loader_details.get('source_type', None)
            source_path = loader_details.get('source_path', None)
            if loader_details.get("source_path_size") is not None:
                source_size = loader_details.get("source_path_size", 0)
            else:
                source_size = loader_details.get("source_aggr_size", 0)

            # Checking for same loader details in app details
            if loader_name and source_type:
                loader_list = app_details.get('loaders', [])
                loader_exist = False
                for loader in loader_list:
                    # If loader exist, update loader SourcePath and SourceType
                    if loader and loader.get('name', "") == loader_name:
                        loader['sourcePath'] = source_path
                        loader['sourceType'] = source_type
                        loader['sourceSize'] = source_size
                        loader['lastModified'] = datetime.now()
                        loader_exist = True

                # If loader does not exist, create new entry
                if not loader_exist:
                    logger.debug("loader not exist in app details")
                    new_loader_data = LoaderMetadata(name=loader_name,
                                                     sourcePath=source_path,
                                                     sourceType=source_type,
                                                     sourceSize=source_size,
                                                     lastModified=datetime.now())
                    loader_list.append(new_loader_data.dict())
                    app_details["loaders"] = loader_list

            # Fetching doc details from input & app details & generate final report
            doc_helper_obj = DocHelper(app_details, self.data, load_id)
            app_details, final_report = doc_helper_obj.process_docs_and_generate_report()
            logger.debug(f"Final Report with doc details: {final_report}")

            # Write current state to the file.
            write_json_to_file(app_details, app_load_metadata_file_path)  # app_details
            # This write will overwrite app_discovery Report
            loading_end = self.data['loading_end']
            if loading_end:
                logger.debug("Loading finished, generating report")
                # writing json report as well for now
                write_json_to_file(final_report, report_file_path)

                logger.debug("Generating report in pdf format")
                report_obj = Reports()

                # Writing pdf report to current load id directory
                load_id = self.data['load_id']
                current_load_report_file_path = (f"{CacheDir.home_dir.value}/{app_name}"
                                                 f"/{load_id}/{CacheDir.pdf_report_file_name.value}")
                full_file_path = get_full_path(current_load_report_file_path)
                report_obj.generate_report(final_report, full_file_path)

                # Writing pdf report file specific to application name, inside app directory
                current_app_report_file_path = (f"{CacheDir.home_dir.value}/{app_name}"
                                                f"/{CacheDir.pdf_report_file_name.value}")
                full_file_path = get_full_path(current_app_report_file_path)
                report_obj.generate_report(final_report, full_file_path)
                logger.info(f"PDF report generated at : {full_file_path}")

            logger.info("Loader Doc request Request processed successfully.")
            return {"message": "Loader Doc API Request processed successfully"}
        except ValidationError as ex:
            logger.error(f"AI_LOADER_DOC Failed. Error:{ex}")
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            logger.error(f"AI_LOADER_DOC Failed. Error:{ex}")
            raise HTTPException(status_code=500, detail="Internal Server Error")