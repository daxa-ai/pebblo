"""
This module handles business logic for local UI
"""
import json
import os
from pebblo.app.enums.enums import CacheDir
from pebblo.app.libs.logger import logger
from pebblo.app.utils.utils import (
    get_full_path,
    read_json_file,
    update_findings_summary,
    update_data_source,
    get_document_with_findings_data,
)
from pebblo.app.models.models import AppListDetails, AppModel


class AppData:
    """
    This class handles business logic for local UI
    """
    @staticmethod
    def get_all_apps_details():
        """
        Returns all necessary app details required for list app functionality.
        """
        try:
            dir_full_path = get_full_path(CacheDir.HOME_DIR.value)
            # List all apps in the directory
            dir_path = os.listdir(dir_full_path)

            # Default values
            all_apps = []
            apps_at_risk = 0
            findings = 0
            files_findings = 0
            data_source = 0
            findings_list = []
            data_source_list = []
            document_with_findings_list = []

            # Iterating through each app in the directory
            for app_dir in dir_path:
                try:
                    # Skip hidden folders
                    if app_dir.startswith("."):
                        logger.debug(f"Skipping hidden folder {app_dir}")
                        continue
                    # Path to metadata.json
                    app_path = (f"{CacheDir.HOME_DIR.value}/{app_dir}/"
                                f"{CacheDir.METADATA_FILE_PATH.value}")
                    logger.debug(f"metadata.json path {app_path}")
                    app_json = read_json_file(app_path)

                    # Skip app if unable to fetch load id details
                    if not app_json and not app_json.get("load_ids"):
                        logger.warning(
                            f"Error: Unable to fetch loadId details for {app_dir} app"
                        )
                        logger.debug(f"App Json : {app_json}")
                        continue

                    # Fetch latest loadId
                    latest_load_id = app_json.get("load_ids")[-1]

                    app_detail_path = (f"{CacheDir.HOME_DIR.value}/{app_dir}/"
                                       f"{latest_load_id}/{CacheDir.REPORT_DATA_FILE_NAME.value}")
                    logger.debug(f"report.json path {app_detail_path}")
                    app_detail_json = read_json_file(app_detail_path)

                    # Skip app if report.json is empty for some reason.
                    if not app_detail_json:
                        logger.warning(
                            f"Error: Unable to fetch loadId details for {app_dir} app"
                        )
                        logger.debug(f"App Json : {app_json}")
                        continue

                    report_summary = app_detail_json.get("reportSummary")
                    app_name = app_json.get("name")
                    findings_entities = report_summary.get("findingsEntities", 0)
                    findings_topics = report_summary.get("findingsTopics", 0)
                    app_details = AppListDetails(
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
                        logger.warning(
                            f"Error: Unable to fetch dataSources details for {app_dir} app"
                        )
                        logger.debug(f"App Detail Json : {app_detail_json}")
                        continue

                    # Prepare output data
                    for data in data_source_details:
                        # Add appName in dataSource
                        updated_data_source_dict = update_data_source(
                            data, app_name, findings_entities, findings_topics
                        )
                        data_source_list.append(updated_data_source_dict)

                        # Add appName in findingsSummary
                        finding_data = update_findings_summary(data, app_name)

                        # Append only required value for dashboard
                        findings_list.extend(finding_data)

                    # Fetch document with findings details from app metadata.json file
                    app_metadata_detail_path = (
                        f"{CacheDir.HOME_DIR.value}/{app_dir}/"
                        f"{latest_load_id}/{CacheDir.METADATA_FILE_PATH.value}")
                    app_metadata_json_details = read_json_file(app_metadata_detail_path)

                    # Fetch required data for DocumentWithFindings
                    documents_with_findings_data = get_document_with_findings_data(
                        app_metadata_json_details
                    )
                    document_with_findings_list.extend(documents_with_findings_data)

                    # Prepare counts for dashboard
                    findings += report_summary.get("findings", 0)
                    files_findings += report_summary.get("filesWithFindings", 0)
                    data_source += report_summary.get("dataSources", 0)
                    if report_summary.get("findings", 0) > 0:
                        apps_at_risk += 1

                    all_apps.append(app_details.dict())

                except Exception as err:
                    logger.warning(f"Error processing app {app_dir}: {err}")

            # Prepare response object
            data = AppModel(
                applicationsAtRiskCount=apps_at_risk,
                findingsCount=findings,
                documentsWithFindingsCount=files_findings,
                dataSourceCount=data_source,
                appList=all_apps,
                findings=findings_list,
                documentsWithFindings=document_with_findings_list,
                dataSource=data_source_list,
            )

            return json.dumps(data.dict(), indent=4)

        except Exception as ex:
            logger.error(f"Error in Dashboard app Listing. Error:{ex}")
            return json.dumps({})

    @staticmethod
    def get_app_details(app_dir):
        """
        Returns app details for an app.
        """
        try:
            # Path to metadata.json
            app_path = f"{CacheDir.HOME_DIR.value}/{app_dir}/{CacheDir.METADATA_FILE_PATH.value}"
            logger.debug(f"metadata.json path {app_path}")

            # Read metadata.json
            app_json = read_json_file(app_path)

            # Skip app if unable to fetch load id details
            if not app_json and not app_json.get("load_ids"):
                # Unable to fetch loadId details
                logger.debug("Error: Unable to fetch loadId details")
                logger.debug(f"App Json : {app_json}")
                return json.dumps({})

            # Fetch latest loadId
            latest_load_id = app_json.get("load_ids")[-1]

            # Path to report.json
            app_detail_path = (f"{CacheDir.HOME_DIR.value}/{app_dir}/"
                               f"{latest_load_id}/{CacheDir.REPORT_DATA_FILE_NAME.value}")
            logger.debug(f"metadata.json path {app_detail_path}")

            # Read app details from report.json
            app_detail_json = read_json_file(app_detail_path)

            # Skip app if unable to fetch app details
            if not app_detail_json:
                return json.dumps({})

            return json.dumps(app_detail_json, indent=4)

        except Exception as ex:
            logger.error(f"Error in app detail. Error:{ex}")
            return json.dumps({})
