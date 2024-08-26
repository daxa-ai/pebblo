import hashlib
import json
from datetime import datetime
from os import makedirs, path

from pebblo.app.enums.enums import ApplicationTypes, CacheDir, ClassifierConstants
from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.db_models import (
    AiDataModel,
    AiDataSource,
    LoaderMetadata,
)
from pebblo.app.models.db_response_models import LoaderDocResponseModel, LoaderDocs
from pebblo.app.models.sqltables import (
    AiDataLoaderTable,
    AiDataSourceTable,
)
from pebblo.app.service.discovery.common import get_or_create_app
from pebblo.app.service.loader.document.document import AiDocumentHandler
from pebblo.app.service.local_ui.loader_apps import LoaderApp
from pebblo.app.storage.sqlite_db import SQLiteClient
from pebblo.app.utils.utils import get_current_time, get_full_path, timeit
from pebblo.entity_classifier.entity_classifier import EntityClassifier
from pebblo.log import get_logger
from pebblo.reports.reports import Reports
from pebblo.topic_classifier.topic_classifier import TopicClassifier

logger = get_logger(__name__)

# Init topic classifier
topic_classifier_obj = TopicClassifier()


class AppLoaderDoc:
    def __init__(self):
        self.db = None
        self.data = None
        self.app_name = None
        self.entity_classifier_obj = EntityClassifier()

    @staticmethod
    def _create_return_response(message, output=None, status_code=200):
        if output is None:
            output = []
        response = LoaderDocResponseModel(docs=output, message=message)
        return PebbloJsonResponse.build(
            body=response.dict(exclude_none=True), status_code=status_code
        )

    def _pdf_writer(self, file_path, data):
        try:
            report_obj = Reports()
            report_format = CacheDir.FORMAT.value
            renderer = CacheDir.RENDERER.value

            full_file_path = get_full_path(file_path)

            # Create parent directories if needed
            dir_path = path.dirname(full_file_path)
            makedirs(dir_path, exist_ok=True)

            status, result = report_obj.generate_report(
                data=data,
                output_path=full_file_path,
                format_string=report_format,
                renderer=renderer,
            )
            if status:
                logger.info(
                    f"PDF report generated, please check path : {full_file_path}"
                )
            else:
                raise Exception(result)
        except Exception as err:
            message = f"PDF report is not generated. Error: {err}"
            logger.error(message)
            raise Exception(message)

    @staticmethod
    def _datetime_decoder(dct):
        for key, value in dct.items():
            if isinstance(value, str):
                try:
                    # Attempt to parse the date string
                    dct[key] = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
                except (ValueError, TypeError):
                    # If it fails, print the error and leave the value as is
                    pass
        return dct

    def _write_pdf_report(self, db, app_name, load_id):
        """
        Calling PDF report generator to write a report in PDF format
        """
        try:
            logger.debug("Generating report in pdf format")
            logger.debug(f"Fetching report data for app: {app_name}")
            loader_report = LoaderApp()
            report_data = loader_report.get_loader_app_details(db, app_name)
            final_report = json.loads(report_data, object_hook=self._datetime_decoder)

            # Writing a PDF report to app directory
            app_report_file_path = f"{CacheDir.HOME_DIR.value}/{app_name}/{CacheDir.REPORT_FILE_NAME.value}"
            self._pdf_writer(app_report_file_path, final_report)

            # Writing a PDF report to current load id directory
            current_load_report_file_path = f"{CacheDir.HOME_DIR.value}/{app_name}/{load_id}/{CacheDir.REPORT_FILE_NAME.value}"
            self._pdf_writer(current_load_report_file_path, final_report)
        except Exception as err:
            raise Exception(err)

    @timeit
    def _update_loader_details(self, app_loader_details):
        """
        Update loader details in the application if they already exist;
        otherwise, add loader details to the application.
        """
        logger.debug("Upsert loader details to exiting ai app details")

        # Update loader details if it already exits in app
        loader_details = self.data.get("loader_details", {})
        loader_name = loader_details.get("loader", None)
        source_type = loader_details.get("source_type", None)
        source_path = loader_details.get("source_path", None)
        loader_source_files = loader_details.get("source_files", [])
        if loader_details.get("source_path_size") is not None:
            source_size = loader_details.get("source_path_size", 0)
        else:
            source_size = loader_details.get("source_aggregate_size", 0)

        # Checking for same loader details in app details

        if loader_name and source_type:
            loader_list = app_loader_details.get("loaders", [])
            loader_exist = False
            for loader in loader_list:
                # If loader exist, update loader SourcePath and SourceType
                if loader and loader.get("name", "") == loader_name:
                    loader["sourcePath"] = source_path
                    loader["sourceType"] = source_type
                    loader["sourceSize"] = source_size
                    loader["sourceFiles"].extend(loader_source_files)
                    loader["lastModified"] = get_current_time()
                    loader_exist = True

            # If loader does not exist, create new entry
            if not loader_exist:
                logger.debug(
                    "Loader details does not exist in app details, adding details to app details"
                )
                new_loader_data = LoaderMetadata(
                    name=loader_name,
                    sourcePath=source_path,
                    sourceType=source_type,
                    sourceSize=source_size,
                    sourceFiles=loader_source_files,
                    lastModified=get_current_time(),
                )
                loader_list.append(new_loader_data.dict())
                app_loader_details["loaders"] = loader_list

        # self.db.update_data(table_obj, app_loader_details)
        logger.debug("Loader details Updated successfully.")
        return app_loader_details

    @timeit
    def _get_doc_classification(self, doc):
        logger.debug("Doc classification started.")
        doc_info = AiDataModel(
            data=doc.get("doc", None),
            entities={},
            entityCount=0,
            topics={},
            topicCount=0,
        )
        try:
            if doc_info.data:
                topics, topic_count, topic_details = topic_classifier_obj.predict(
                    doc_info.data
                )
                (
                    entities,
                    entity_count,
                    anonymized_doc,
                    entity_details,
                ) = self.entity_classifier_obj.presidio_entity_classifier_and_anonymizer(
                    doc_info.data,
                    anonymize_snippets=ClassifierConstants.anonymize_snippets.value,
                )
                doc_info.topics = topics
                doc_info.entities = entities
                doc_info.topicCount = topic_count
                doc_info.entityCount = entity_count
                doc_info.data = anonymized_doc
            logger.debug("Doc classification finished.")
            return doc_info
        except Exception as e:
            logger.error(
                f"Get Classifier Response Failed for doc: {doc}, Exception: {e}"
            )
            return doc_info

    @staticmethod
    @timeit
    def _update_doc_details(doc, doc_info):
        """
        Create a doc model and return its object
        """
        logger.debug("Update doc details with classification result")
        doc["entities"] = doc_info.entities
        doc["topics"] = doc_info.topics
        logger.debug("Input doc updated with classification result")

    @timeit
    def _doc_pre_processing(self):
        logger.debug("Input docs pre processing started.")
        input_doc_list = self.data.get("docs", [])
        for doc in input_doc_list:
            doc_info = self._get_doc_classification(doc)
            self._update_doc_details(doc, doc_info)

        # Update input doc with updated one
        logger.debug("Doc pre processing finished.")

    @timeit
    def _get_or_create_data_source(self):
        logger.debug("Getting or Creating Data Source Details.")
        loader_details = self.data.get("loader_details") or {}

        filter_query = {
            "appName": self.app_name,
            "sourcePath": loader_details.get("source_path"),
            "sourceType": loader_details.get("source_type"),
            "loadId": self.data.get("load_id"),
        }
        status, output = self.db.query(AiDataSourceTable, filter_query)
        if status and output and len(output) > 0:
            logger.debug("Data Source details are already existed.")
            data = output[0].data
            return data

        # Data Source details are not present, Creating data source details
        data_source = {
            "appName": self.app_name,
            "loadId": self.data.get("load_id"),
            "metadata": {
                "createdAt": get_current_time(),
                "modifiedAt": get_current_time(),
            },
            "sourcePath": loader_details.get("source_path"),
            "sourceType": loader_details.get("source_type"),
            "loader": loader_details.get("loader"),
        }
        ai_data_source_obj = AiDataSource(**data_source)
        ai_data_source = ai_data_source_obj.dict()
        _, data_source_obj = self.db.insert_data(AiDataSourceTable, ai_data_source)
        logger.debug("Data Source has been created successfully.")
        return data_source_obj.data

    @timeit
    def process_request(self, data):
        try:
            self.db = SQLiteClient()
            self.data = data
            self.app_name = data.get("name")

            # create session
            self.db.create_session()

            loader_obj = get_or_create_app(
                self.db,
                self.app_name,
                AiDataLoaderTable,
                self.data,
                ApplicationTypes.LOADER.value,
            )
            if not loader_obj:
                message = "Unable to get or create loader doc app"
                return self._create_return_response(message=message, status_code=500)

            loader_obj.data = self._update_loader_details(loader_obj.data)

            # Get each doc classification: Pre Processing
            self._doc_pre_processing()

            # Update dataSource Details: AIDataSource
            data_source = self._get_or_create_data_source()

            # Iterate Each doc & Update AIDocument, AISnippets
            document_handler = AiDocumentHandler(self.db, self.data)
            app_loader_details = document_handler.create_or_update_document(
                app_loader_details=loader_obj.data, data_source=data_source
            )
            self.db.update_data(loader_obj, app_loader_details)

            # Creating loader response
            loader_details = self.data.get("loader_details", {})
            docs = self.data.get("docs", [])
            loader_response_output = []
            for doc in docs:
                doc_obj = LoaderDocs(
                    pb_id=doc["pb_id"],
                    pb_checksum=hashlib.md5(doc.get("doc", "").encode()).hexdigest(),
                    source_path=doc.get("source_path"),
                    loader_source_path=loader_details.get("source_path"),
                    entity_count=sum(doc.get("entities", {}).values()),
                    topic_count=sum(doc.get("topics", {}).values()),
                    entities=doc.get("entities"),
                    topics=doc.get("topics"),
                )
                loader_response_output.append(doc_obj)

            # Commit before generating report, so that even if report generation fails then values would be in db.
            self.db.session.commit()

            if self.data.get("loading_end"):
                # Get report data & Write PDF report
                self._write_pdf_report(
                    self.db, app_loader_details["name"], app_loader_details["id"]
                )

        except Exception as err:
            message = f"Loader Doc API Request failed, Error: {err}"
            logger.error(message)
            logger.info("Rollback the changes")
            self.db.session.rollback()
            return self._create_return_response(message, 500)
        else:
            message = "Loader Doc API Request processed successfully"
            return self._create_return_response(message, output=loader_response_output)
        finally:
            self.db.session.close()
