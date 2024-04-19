"""
This module handles business logic for local UI
"""

import json
import os

from pebblo.app.enums.enums import CacheDir
from pebblo.app.libs.logger import logger
from pebblo.app.models.models import (
    LoaderAppListDetails,
    LoaderAppModel,
    RetrievalAppListDetails,
    RetrievalAppModel,
    RetrievalAppResponse,
)
from pebblo.app.utils.utils import (
    get_active_users,
    get_document_with_findings_data,
    get_full_path,
    get_pebblo_server_version,
    get_vector_dbs,
    read_json_file,
    update_data_source,
    update_findings_summary,
)


class AppData:
    """
    This class handles business logic for local UI
    """

    def __init__(self):
        self.loader_apps_at_risk = 0
        self.loader_findings = 0
        self.loader_files_findings = 0
        self.loader_data_source = 0
        self.loader_findings_list = []
        self.loader_data_source_list = []
        self.loader_document_with_findings_list = []
        self.retrieval_active_users = []
        self.retrieval_vectordbs = []
        self.total_retrievals = []

    def prepare_loader_response(self, app_dir, app_json):
        # Default values
        load_ids = app_json.get("load_ids", [])

        if not load_ids:
            logger.debug(f"No valid loadIds found for app: {app_dir}.")
            logger.warning(f"Skipping app '{app_dir}' due to missing or invalid file")
            return

        # Fetching latest loadId
        latest_load_id, app_detail_json = self.get_latest_load_id(load_ids, app_dir)

        if not latest_load_id:
            logger.debug(f"No valid loadIds found for app: {app_dir}. Skipping.")
            logger.warning(f"Skipping app '{app_dir}' due to missing or invalid file")
            return

        report_summary = app_detail_json.get("reportSummary")
        app_name = app_json.get("name")
        findings_entities = report_summary.get("findingsEntities", 0)
        findings_topics = report_summary.get("findingsTopics", 0)
        app_details = LoaderAppListDetails(
            name=app_json.get("name"),
            topics=findings_topics,
            entities=findings_entities,
            owner=report_summary.get("owner"),
            loadId=latest_load_id,
        )

        # Fetch details for dashboard tabs
        data_source_details = app_detail_json.get("dataSources")

        # Skip app if data source details are not present for some reason.
        if not data_source_details:
            logger.debug(
                f"Error: Unable to fetch dataSources details for {app_dir} app"
            )
            logger.debug(f"App Detail Json : {app_detail_json}")
            logger.warning(f"Skipping app '{app_dir}' due to missing or invalid file")
            return

        # Prepare output data
        for data in data_source_details:
            # Add appName in dataSource
            updated_data_source_dict = update_data_source(
                data, app_name, findings_entities, findings_topics
            )
            self.loader_data_source_list.append(updated_data_source_dict)

            # Add appName in findingsSummary
            finding_data = update_findings_summary(data, app_name)

            # Append only required value for dashboard
            self.loader_findings_list.extend(finding_data)

        # Fetch document with findings details from app metadata.json file
        app_metadata_detail_path = (
            f"{CacheDir.HOME_DIR.value}/{app_dir}/"
            f"{latest_load_id}/{CacheDir.METADATA_FILE_PATH.value}"
        )
        app_metadata_json_details = read_json_file(app_metadata_detail_path)

        # Fetch required data for DocumentWithFindings
        documents_with_findings_data = get_document_with_findings_data(
            app_metadata_json_details
        )
        self.loader_document_with_findings_list.extend(documents_with_findings_data)

        # Prepare counts for dashboard
        self.loader_findings += report_summary.get("findings", 0)
        self.loader_files_findings += report_summary.get("filesWithFindings", 0)
        self.loader_data_source += report_summary.get("dataSources", 0)
        if report_summary.get("findings", 0) > 0:
            self.loader_apps_at_risk += 1

        return app_details.dict()

    def prepare_retrieval_response(self, app_dir, app_json):
        logger.debug("In prepare loader response")

        app_metadata_path = (
            f"{CacheDir.HOME_DIR.value}/{app_dir}/"
            f"{CacheDir.APPLICATION_METADATA_FILE_PATH.value}"
        )
        app_metadata_content = read_json_file(app_metadata_path)

        # Skip app if app_metadata details are not present for some reason.
        if not app_metadata_content:
            logger.debug(
                f"Error: Unable to fetch app_metadata.json content for {app_dir} app"
            )
            logger.debug(f"App metadata Json : {app_metadata_content}")
            logger.warning(f"Skipping app '{app_dir}' due to missing or invalid file")
            return

        # fetch total retrievals
        for retrieval in app_metadata_content.get("retrieval"):
            retrieval_data = {"name": app_json.get("name")}
            retrieval_data.update(retrieval)
            self.total_retrievals.append(retrieval_data)

        # fetch active users per app
        active_users = get_active_users(app_metadata_content["retrieval"])
        self.retrieval_active_users.extend(active_users)

        # fetch vector dbs per app
        vector_dbs = get_vector_dbs(app_metadata_content["chains"])
        self.retrieval_vectordbs.extend(vector_dbs)

        app_details = RetrievalAppListDetails(
            name=app_json.get("name"),
            owner=app_metadata_content.get("owner"),
            retrievals=app_metadata_content.get("retrieval"),
            active_users=active_users,
            vector_dbs=vector_dbs,
        )
        return app_details.dict()

    def get_all_apps_details(self):
        """
        Returns all necessary app details required for list app functionality.
        """
        try:
            dir_full_path = get_full_path(CacheDir.HOME_DIR.value)
            # List all apps in the directory
            dir_path = os.listdir(dir_full_path)

            all_loader_apps = []
            all_retrieval_apps = []

            # Iterating through each app in the directory
            for app_dir in dir_path:
                try:
                    # Skip hidden folders
                    if app_dir.startswith("."):
                        logger.debug(f"Skipping hidden folder {app_dir}")
                        continue
                    # Path to metadata.json
                    app_path = (
                        f"{CacheDir.HOME_DIR.value}/{app_dir}/"
                        f"{CacheDir.METADATA_FILE_PATH.value}"
                    )
                    logger.debug(f"metadata.json path {app_path}")
                    app_json = read_json_file(app_path)

                    if not app_json:
                        # Unable to find json file
                        logger.debug(
                            f"Metadata file ({CacheDir.METADATA_FILE_PATH.value}) not found for app: {app_dir}."
                        )
                        logger.warning(
                            f"Skipping app '{app_dir}' due to missing or invalid file"
                        )
                        continue

                    app_type = app_json.get("app_type", None)
                    if app_type in ["loader", None]:
                        loader_app = self.prepare_loader_response(app_dir, app_json)
                        if loader_app:
                            all_loader_apps.append(loader_app)
                    elif app_type == "retrieval":
                        retrieval_app = self.prepare_retrieval_response(
                            app_dir, app_json
                        )
                        if retrieval_app:
                            all_retrieval_apps.append(retrieval_app)

                except Exception as err:
                    logger.warning(f"Error processing app {app_dir}: {err}")

            logger.debug("Preparing loader app response object")
            loader_response = LoaderAppModel(
                applicationsAtRiskCount=self.loader_apps_at_risk,
                findingsCount=self.loader_findings,
                documentsWithFindingsCount=self.loader_files_findings,
                dataSourceCount=self.loader_data_source,
                appList=all_loader_apps,
                findings=self.loader_findings_list,
                documentsWithFindings=self.loader_document_with_findings_list,
                dataSource=self.loader_data_source_list,
                pebbloServerVersion=get_pebblo_server_version(),
            )

            logger.debug("Preparing retrieval app response object")
            retrieval_response = RetrievalAppModel(
                appList=all_retrieval_apps,
                retrievals=self.total_retrievals,
                activeUsers=list(set(self.retrieval_active_users)),
                violations=[],
            )

            response = {
                "loaderApps": loader_response.dict(),
                "retrievalApps": retrieval_response.dict(),
            }
            return response
        except Exception as ex:
            logger.error(f"Error in Dashboard app Listing. Error:{ex}")
            return json.dumps({})

    def get_loader_app_details(self, app_dir, load_ids):
        # Fetching latest loadId
        latest_load_id, app_detail_json = self.get_latest_load_id(load_ids, app_dir)

        if not latest_load_id:
            logger.debug(f"No valid loadIds found for app {app_dir}.")
            logger.warning(f"Skipping app '{app_dir}' due to missing or invalid file")
            return json.dumps({})

        if not app_detail_json:
            return json.dumps({})

        return json.dumps(app_detail_json, indent=4)

    def get_app_details(self, app_dir):
        """
        Returns app details for an app.
        """
        try:
            # Path to metadata.json
            app_path = f"{CacheDir.HOME_DIR.value}/{app_dir}/{CacheDir.METADATA_FILE_PATH.value}"
            logger.debug(f"Metadata file path: {app_path}")
            # Reading metadata.json
            app_json = read_json_file(app_path)
            # Condition for handling loadId
            if not app_json:
                # Unable to fetch loadId details
                logger.debug(
                    f"Error: Report Json {CacheDir.METADATA_FILE_PATH.value} not found for app {app_path}"
                )
                logger.warning(
                    f"Skipping app '{app_dir}' due to missing or invalid file"
                )
                return json.dumps({})

            app_type = app_json.get("app_type", None)
            if app_type in ["loader", None]:
                load_ids = app_json.get("load_ids", [])
                if not load_ids:
                    # Unable to fetch loadId details
                    logger.debug(f"Error: Details not found for app {app_path}")
                    logger.warning(
                        f"Skipping app '{app_dir}' due to missing or invalid file"
                    )
                    return json.dumps({})
                return self.get_loader_app_details(app_dir, load_ids)
            elif app_type == "retrieval":
                app_metadata_path = (
                    f"{CacheDir.HOME_DIR.value}/{app_dir}/"
                    f"{CacheDir.APPLICATION_METADATA_FILE_PATH.value}"
                )
                app_metadata_content = read_json_file(app_metadata_path)

                # Skip app if app_metadata details are not present for some reason.
                if not app_metadata_content:
                    logger.debug(
                        f"Error: Unable to fetch app_metadata.json content for {app_dir} app"
                    )
                    logger.debug(f"App metadata Json : {app_metadata_content}")
                    logger.warning(
                        f"Skipping app '{app_dir}' due to missing or invalid file"
                    )
                    return json.dumps({})
                return self.get_retrieval_app_details(app_metadata_content)

        except Exception as ex:
            logger.error(f"Error in app detail. Error: {ex}")

    @staticmethod
    def get_latest_load_id(load_ids, app_dir):
        """
        Returns app latestLoadId for an app.
        """
        for load_id in reversed(load_ids):
            # Path to report.json
            app_detail_path = f"{CacheDir.HOME_DIR.value}/{app_dir}/{load_id}/{CacheDir.REPORT_DATA_FILE_NAME.value}"
            logger.debug(f"Report File path: {app_detail_path}")
            app_detail_json = read_json_file(app_detail_path)
            if app_detail_json:
                # If report is found, proceed with this load_id
                latest_load_id = load_id
                return latest_load_id, app_detail_json

        return None, None

    @staticmethod
    def get_retrieval_app_details(app_content):
        retrieval_data = app_content["retrieval"]
        active_users = []
        vector_dbs = []
        documents = []

        # fetch active users, vector dbs and documents names for given app
        for data in retrieval_data:
            active_users.append(data["user"])
            for context in data["context"]:
                vector_dbs.append(context["vector_db"])
                documents.append(context["retrieved_from"])
        active_users = list(set(active_users))
        vector_dbs = list(set(vector_dbs))
        documents = list(set(documents))

        # prepare app response
        response = RetrievalAppResponse(
            retrievals=retrieval_data,
            activeUsers=active_users,
            vectorDbs=vector_dbs,
            documents=documents,
        )
        return response.dict()
