import logging
from datetime import datetime

from fastapi import HTTPException
from pydantic import ValidationError

from pebblo.reports.reports import Reports
from pebblo.app.enums.enums import CacheDir
from pebblo.app.utils.utils import write_json_to_file, read_json_file, get_full_path
from pebblo.app.libs.logger import logger
from pebblo.app.models.models import LoaderMetadata
from pebblo.app.service.doc_helper import LoaderHelper


class AppLoaderDoc:
    def __init__(self, data):
        self.data = data
        self.app_name = self.data.get("name")

    def _write_pdf_report(self, final_report):
        """
            Calling pdf report generator to write report in pdf format
        """
        logger.debug("Generating report in pdf format")
        report_obj = Reports()
        report_format = CacheDir.format.value
        renderer = CacheDir.renderer.value

        # Writing pdf report to current load id directory
        load_id = self.data['load_id']
        current_load_report_file_path = (f"{CacheDir.home_dir.value}/{self.app_name}"
                                         f"/{load_id}/{CacheDir.report_file_name.value}")
        full_file_path = get_full_path(current_load_report_file_path)
        report_obj.generate_report(data=final_report, outputPath=full_file_path, format=report_format,
                                   renderer=renderer)

        # Writing pdf report file specific to application name, inside app directory
        current_app_report_file_path = (f"{CacheDir.home_dir.value}/{self.app_name}"
                                        f"/{CacheDir.report_file_name.value}")
        full_file_path = get_full_path(current_app_report_file_path)
        report_obj.generate_report(data=final_report, outputPath=full_file_path, format=report_format,
                                   renderer=renderer)
        logger.info(f"PDF report generated, please check path : {full_file_path}")

    def _upsert_loader_details(self, app_details):
        """
            Update loader details in the application if they already exist;
            otherwise, add loader details to the application.
        """
        logger.debug("Upsert loader details to exiting ai app details")
        # Update loader details if it already exits in app
        loader_details = self.data.get("loader_details", {})
        loader_name = loader_details.get('loader', None)
        source_type = loader_details.get('source_type', None)
        source_path = loader_details.get('source_path', None)
        loader_source_files = loader_details.get("source_files", [])
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
                    loader["sourceFiles"].extend(loader_source_files)
                    loader['lastModified'] = datetime.now()
                    loader_exist = True

            # If loader does not exist, create new entry
            if not loader_exist:
                logger.debug("loader details does not exist in app details, adding details to app details")
                new_loader_data = LoaderMetadata(name=loader_name,
                                                 sourcePath=source_path,
                                                 sourceType=source_type,
                                                 sourceSize=source_size,
                                                 sourceFiles=loader_source_files,
                                                 lastModified=datetime.now())
                loader_list.append(new_loader_data.dict())
                app_details["loaders"] = loader_list

    def process_request(self):
        """
            This process is entrypoint function for loader doc API implementation.
        """
        try:
            logger.debug("Loader doc request processing started")
            logger.debug(f"Loader Doc, Application Name: {self.app_name}, Input Data: {self.data}")

            # Read metadata file & get current load details
            app_metadata_file_path = f"{CacheDir.home_dir.value}/{self.app_name}/{CacheDir.metadata_file_path.value}"
            app_metadata = read_json_file(app_metadata_file_path)
            if not app_metadata:
                return {"Message": "App details not present, Please execute discovery api first"}

            # Get current app details from load id
            load_id = self.data['load_id']
            app_load_metadata_file_path = (f"{CacheDir.home_dir.value}/{self.app_name}"
                                           f"/{load_id}/{CacheDir.metadata_file_path.value}")
            app_details = read_json_file(app_load_metadata_file_path)
            if not app_details:
                # TODO: Handle the case where discover call did not happen, but loader doc is being called.
                logger.error(f"Could not read metadata file at {app_load_metadata_file_path}. Exiting.")
                return {"Message": f"Could not read metadata file at {app_load_metadata_file_path}. Exiting"}

            # Add/Update Loader Details with input loader details
            self._upsert_loader_details(app_details)

            # process input docs, app details, and generate final report
            loader_helper_obj = LoaderHelper(app_details, self.data, load_id)
            app_details, final_report = loader_helper_obj.process_docs_and_generate_report()

            logger.debug(f"Final Report with doc details: {final_report}")

            # Write current state to the file, Updating app details
            write_json_to_file(app_details, app_load_metadata_file_path)

            # check whether report generation is necessary
            loading_end = self.data['loading_end']
            if loading_end:
                logger.debug("Loading finished, generating report")

                # writing report file to its load_id directory
                json_report_file_path = (f"{CacheDir.home_dir.value}/{self.app_name}"
                                         f"/{load_id}/{CacheDir.report_data_file_name.value}")
                write_json_to_file(final_report, json_report_file_path)

                # Writing report in pdf format
                self._write_pdf_report(final_report)

            logger.debug("Loader Doc request Request processed successfully.")
            return {"message": "Loader Doc API Request processed successfully"}
        except ValidationError as ex:
            logger.error(f"AI_LOADER_DOC Failed. Error:{ex}")
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            logger.error(f"AI_LOADER_DOC Failed. Error:{ex}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
