# Copyright (c) 2024 Daxa. All rights reserved.

from datetime import datetime
from entity_classifier.entity_classifier import EntityClassifier
from enums.enums import CacheDir
from utils.utils import write_json_to_file, read_json_file
from libs.logger import logger
from models.models import LoaderMetadata, Metadata, AiDataModel, AiDocs, AiApp


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

            runtime_dict = self.data.get("runtime", {})
            instance_details = {
                "language": runtime_dict.get("language"),
                "languageVersion": runtime_dict.get("language_version"),
                "host": runtime_dict.get("host"),
                "ip": runtime_dict.get("ip"),
                "path": runtime_dict.get("path"),
                "runtime": runtime_dict.get("runtime"),

                # Adding New for openSource
                "type": runtime_dict.get("type"),
                "platform": runtime_dict.get("platform"),
                "os": runtime_dict.get("os"),
                "os_version": runtime_dict.get("os_version")

            }
            logger.debug(f"AI_APPS [{application_name}]: Instance Details: {instance_details}")

            last_used = datetime.now()

            metadata = Metadata(
                createdAt=datetime.now(),
                modifiedAt=datetime.now()
            )

            ai_app = {
                "metadata": metadata,
                "name": application_name,
                "owner": owner,
                "pluginVersion": self.data.get("plugin_version"),
                "instanceDetails": instance_details,
                "framework": self.data.get("framework"),
                "lastUsed": last_used
            }
            ai_app_obj = AiApp(**ai_app)
            logger.debug(f"Final Output For Discovery Call: {ai_app_obj.dict()}")
            file_path = f"{CacheDir.home_dir.value}/{application_name}/{self.load_id}/{CacheDir.report_file_name.value}"
            write_json_to_file(ai_app_obj.dict(), file_path)
            # return {"Request Processed Successfully"}
            # TODO: remove below line after testing.
            return ai_app_obj.dict()
        except Exception as ex:
            response = f"Error in process_request. Error:{ex}"
            logger.error(response)
            return response


class AppLoaderDoc:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def _get_classifier_response(doc):
        doc_info = AiDataModel(data=doc.get("doc", None),
                               entities={}, entityCount=0,
                               topics={}, topicCount=0)
        try:
            if doc_info.data:
                classifier_obj = EntityClassifier(doc_info.data)
                topics, topic_count = {}, 0 # classifier_obj.topic_classifier(doc_info.data)
                entities, entity_count = classifier_obj.presidio_entity_classifier()
                secrets, secret_count = {}, 0 # classifier_obj.secret_classifier(doc_info.data)
                entities.update(secrets)
                entity_count += secret_count
                doc_info.topics = topics
                doc_info.entities = entities
                doc_info.topicCount = topic_count
                doc_info.entityCount = entity_count
            return doc_info
        except Exception as e:
            logger.error(f"Get Classifier Response Failed, Exception: {e}")
            return doc_info

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
            load_id = app_metadata.get("current_load_id")

            # Get current app details from load id
            run_file_path = f"{CacheDir.home_dir.value}/{app_name}/{load_id}/{CacheDir.report_file_name.value}"
            app_details = read_json_file(run_file_path)

            # Create Apps Object
            metadata_obj = Metadata(
                    createdAt=datetime.now(),
                    modifiedAt=datetime.now()
                )
            last_used = datetime.now()

            # Get Loader Details
            loader_details = self.data.get("loader_details", {})
            loader_name = loader_details.get('loader', None)
            source_type = loader_details.get('source_type', None)
            source_path = loader_details.get('source_path', None)

            if loader_name and source_type:
                loader_list = app_details.get('loaders', [])
                loader_exist = False
                for loader in loader_list:
                    # If loader exist, update loader SourcePath and SourceType
                    if loader and loader.get('name', "") == loader_name:
                        loader['sourcePath'] = source_path
                        loader['sourceType'] = source_type
                        loader['lastModified'] = last_used
                        loader_exist = True

                # If loader does not exist, create new entry
                if not loader_exist:
                    logger.debug("loader not exist in db")
                    new_loader_data = LoaderMetadata(name=loader_name,
                                                     sourcePath=source_path,
                                                     sourceType=source_type,
                                                     lastModified=last_used)
                    loader_list.append(new_loader_data.dict())

            doc_list = self.data.get('docs', [])
            docs = []
            for doc in doc_list:
                # Get Classifier Response
                doc_info: AiDataModel = self._get_classifier_response(doc)
                if doc:
                    loader_docs_data = AiDocs(
                                              appId=load_id,
                                              metadata=metadata_obj,
                                              doc=doc.get('doc'),
                                              sourcePath=doc.get('source_path'),
                                              loaderSourcePath=source_path,
                                              lastModified=last_used,
                                              entityCount=doc_info.entityCount,
                                              entities=doc_info.entities,
                                              topicCount=doc_info.topicCount,
                                              topics=doc_info.topics
                                              )
                    docs.append(loader_docs_data.dict())

            logger.debug(f"Loader Doc Details: {docs}")
            app_details["docs"] = docs

            # Update modifiedAt & lastUsed timestamp
            app_details["metadata"]["modifiedAt"] = last_used
            app_details["lastUsed"] = last_used
            logger.debug(f"Final Report with doc details: {app_details}")

            # This write will overwrite app_discovery Report
            file_path = f"{CacheDir.home_dir.value}/{app_name}/{load_id}/{CacheDir.report_file_name.value}"
            write_json_to_file(app_details, file_path)
            return {"Loader Doc Response": docs}

        except Exception as ex:
            print(f"AI_LOADER_DOC Failed: Error in process_request. Error:{ex}")
            return {"message": f"Error: {ex}"}
