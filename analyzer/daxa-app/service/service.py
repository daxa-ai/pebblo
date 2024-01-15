# Copyright (c) 2024 Daxa. All rights reserved.

from datetime import datetime, timezone

from models.models import Chain, LoaderMetadata, Metadata, VectorDb, PackageInfo, AiDataModel, AiDocs, AiApp
from entity_classifier.entity_classifier import EntityClassifier
from utils.utils import write_json_to_file, read_json_file

from libs.logger import logger


class AppDiscover:
    def __init__(self, data: dict, run_id: str):
        self.data = data
        self.run_id = run_id

    def process_request(self):
        """
            Process AI App discovery Request
            """
        try:
            application_name = self.data.get("name")
            logger.debug(f"AI_APP [{application_name}]: Input Data: {self.data}")

            # Writing app metadata file
            file_context = {"name": application_name, "current_run_id": self.run_id}
            file_path = f"{application_name}/metadata/metadata.json"
            write_json_to_file(file_context, file_path)
            # get chain details: Not present in OpenSource Input
            # chains = list()
            # for chain in self.data.get('chains', []):
            #     name = chain["name"]
            #     model = chain['model']
            #     # vector db details
            #     vector_db_details = []
            #     for vector_db in chain.get('vector_dbs', []):
            #         vector_db_obj = VectorDb(name=vector_db.get("name"),
            #                                  version=vector_db.get("version"),
            #                                  location=vector_db.get("location"),
            #                                  embeddingModel=vector_db.get("embedding_model"))
            #
            #         package_info = vector_db.get("pkg_info", {})
            #         if package_info:
            #             pkg_info_obj = PackageInfo(projectHomePage=package_info.get("project_home_page"),
            #                                        documentationUrl=package_info.get("documentation_url"),
            #                                        pypiUrl=package_info.get("pypi_url"),
            #                                        licenceType=package_info.get("liscence_type"),
            #                                        installedVia=package_info.get("installed_via"),
            #                                        location=package_info.get("location"))
            #             vector_db_obj.packageInfo = pkg_info_obj.dict()
            #
            #         vector_db_details.append(vector_db_obj.dict())
            #     chain_obj = Chain(name=name, model=model, vectorDbs=vector_db_details)
            #     chains.append(chain_obj.dict())

            # get loader details: Not present in OpenSource Input
            # loaders = list()
            # for loader in self.data.get('loaders', []):
            #     loader_obj = LoaderMetadata(name=loader.get('loader'),
            #                                 sourcePath=loader.get('source_path'),
            #                                 sourceType=loader.get('source_type'))
            #     loaders.append(loader_obj.dict())

            # logger.debug(f"AI_APPS [{application_name}]: Loaders: {loaders}")

            # instance_dict = self.data.get("instance", {}): Not present in OpenSource Input
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

            last_used = datetime.now(timezone.utc)

            metadata = Metadata(
                createdAt=datetime.utcnow(),
                modifiedAt=datetime.utcnow()
            )

            ai_app = {
                "metadata": metadata,
                "name": application_name,
                "pluginVersion": self.data.get("plugin_version"),
                "instanceDetails": instance_details,
                # "chains": chains,
                # "loaders": loaders,
                "framework": self.data.get("framework"),
                "lastUsed": last_used
            }
            ai_app_obj = AiApp(**ai_app)
            logger.debug(f"Final Output For Discovery Call: {ai_app_obj.dict()}")
            file_path = f"{application_name}/{self.run_id}/report.json"
            write_json_to_file(ai_app_obj.dict(), file_path)
            return ai_app_obj
        except Exception as ex:
            response = f"Error in process_request. Error:{ex}"
            logger.error(response)
            return response


class AppLoaderDoc():
    def __init__(self, data):
        self.data = data

    def process_request(self):
        """This process is entrypoint function for loader doc API implementation."""
        logger.debug(f"Loader Doc, Input Data: {self.data}")

        try:
            app_name = self.data.get("name")
            logger.debug(f"AI Loader Doc, AppName: {app_name}")

            # Read metadata file & get run details
            metadata_file_path = f"{app_name}/metadata/metadata.json"
            app_metadata = read_json_file(metadata_file_path)
            if not app_metadata:
                return {"Message": "App details not present, Please call discovery api first"}
            run_id = app_metadata.get("current_run_id")

            # get current app details from run id
            run_file_path = f"{app_name}/{run_id}/report.json"
            app_details = read_json_file(run_file_path)

            # Creating AiApps Objects
            metadata_obj = Metadata(
                    createdAt=datetime.utcnow(),
                    modifiedAt=datetime.utcnow()
                )
            last_used = datetime.now(timezone.utc)

            # Get Loader Details
            loader_details = self.data.get("loader_details", {})
            loader_name = loader_details.get('loader', None)
            source_type = loader_details.get('source_type', None)
            source_path = loader_details.get('source_path', None)

            if loader_name and source_type:
                loader_list = app_details.get('loaders', [])
                loader_exist = False
                for loader in loader_list:
                    # If loader exist, updating loader SourcePath and SourceType
                    if loader and loader.get('name', "") == loader_name:
                        loader['sourcePath'] = source_path
                        loader['sourceType'] = source_type
                        loader_exist = True

                # If loader does not exist
                if not loader_exist:
                    logger.debug("loader not exist in db")
                    new_loader_data = LoaderMetadata(name=loader_name,
                                                     sourcePath=source_path,
                                                     sourceType=source_type)
                    # Append New Loader Details
                    loader_list.append(new_loader_data.dict())

                # update loader details in app details
                app_details["loader_details"] = loader_list

            doc_list = self.data.get('docs', [])
            doc_report = []
            for doc in doc_list:
                """ Get Classifier Response From Presidio"""
                doc_info: AiDataModel = self._get_classifier_response(doc)
                if doc:
                    # Creating Entry for Ai Docs Collection
                    loader_docs_data = AiDocs(name=self.data.get('name'),
                                              appId=run_id,
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
                    """ Create doc report """
                    doc_report.append(loader_docs_data.dict())

                    """Updating loader Source file in AI APP collection """
                    # run_with_transaction(self.loader_source_file_update_tx, self.db, ai_app_db_output, source_path, doc)

                    """Check policy violations for loader doc {Need to Discuss with shreyas }"""
                    # check_doc_policy_violations(self.db, ai_app_db_output, ai_docs_obj.dict())
                    # res_doc_obj = ai_docs_obj.dict()
                    # self.agg_doc_to_app(res_doc_obj.get('entities', {}), res_doc_obj.get('topics', {}),
                    #                     res_doc_obj.get('id'))
            logger.debug(f"Loader Doc Details: {doc_report}")
            app_details["doc_report"] = doc_report

            logger.debug(f"Final Report with doc details: {app_details}")

            # This write will overwrite app_discovery Report
            file_path = f"{app_name}/{run_id}/report.json"
            write_json_to_file(app_details, file_path)
            return { "Loader Doc Response": doc_report }

        except Exception as ex:
            print(f"AI_LOADER_DOC Failed: Error in process_request. Error:{ex}")
            return {"message": f"Error: {ex}"}

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
