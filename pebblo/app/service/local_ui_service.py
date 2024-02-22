import json
import os
from pebblo.app.enums.enums import CacheDir
from pebblo.app.libs.logger import logger
from pebblo.app.utils.utils import get_full_path, read_json_file, update_findings_summary, update_data_source, get_document_with_findings_data
from pebblo.app.models.models import AppListDetails, AppModel


class AppData:
    @staticmethod
    def get_all_apps_details():
        """Returns all necessary app details required for listing."""
        #try:
        dir_full_path = get_full_path(CacheDir.home_dir.value)
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
            # Path to metadata.json
            app_path = f'{CacheDir.home_dir.value}/{app_dir}/{CacheDir.metadata_file_path.value}'
            logger.debug(f'metadata.json path {app_path}')
            app_json = read_json_file(app_path)
            # Condition for handling loadId
            if app_json and app_json.get('load_ids') is not None and len(app_json.get('load_ids')) > 0:
                # Fetching latest loadId
                latest_load_id = app_json.get("load_ids")[-1]
                # Path to report.json
                app_detail_path = f'{CacheDir.home_dir.value}/{app_dir}/{latest_load_id}/{CacheDir.report_data_file_name.value}'
                logger.debug(f'report.json path {app_detail_path}')
                app_detail_json = read_json_file(app_detail_path)
                if app_detail_json:
                    report_summary = app_detail_json.get('reportSummary')
                    app_name = app_json.get('name')
                    app_details = AppListDetails(
                        name=app_json.get('name'),
                        topics=report_summary.get('findingsTopics', 0),
                        entities=report_summary.get('findingsEntities', 0),
                        owner=report_summary.get('owner'),
                        loadId=latest_load_id
                    )

                    # Fetching Details for dashboard tabs
                    data_source_details = app_detail_json.get('dataSources')
                    # Fetching only required values for dashboard pages
                    if data_source_details and len(data_source_details) > 0:
                        for data in data_source_details:
                            # Adding appName in dataSource
                            updated_data_source_dict = update_data_source(data, app_name)
                            data_source_list.append(updated_data_source_dict)
                            # Adding appName in findingsSummary
                            finding_data = update_findings_summary(data, app_name)
                            # appending only required value for dashboard
                            findings_list.append(finding_data)
                            print(f'---FIndind data {findings_list}-----')
                    print(f'---Finffff{findings_list}')
                    # Fetching DocumentWithFindings details from app metadata.json
                    app_metadata_detail_path = f'{CacheDir.home_dir.value}/{app_dir}/{latest_load_id}/{CacheDir.metadata_file_path.value}'
                    app_metadata_json_details = read_json_file(app_metadata_detail_path)
                    # Fetching required data for DocumentWithFindings
                    documents_with_findings_data = get_document_with_findings_data(app_metadata_json_details)
                    document_with_findings_list.append(documents_with_findings_data)

                    # Dashboard Counts
                    findings += report_summary.get('findings', 0)
                    files_findings += report_summary.get('filesWithFindings', 0)
                    data_source += report_summary.get('dataSources', 0)
                    if report_summary.get('findings', 0) > 0:
                        apps_at_risk += 1

                    all_apps.append(app_details.dict())
            else:
                logger.debug('Error: Unable to fetch loadId details')
                logger.debug(f'App Json : {app_json}')

        # Validation
        data = AppModel(
            applicationsAtRiskCount=apps_at_risk,
            findingsCount=findings,
            documentsWithFindingsCount=files_findings,
            dataSourceCount=data_source,
            appList=all_apps,
            findings=findings_list,
            documentsWithFindings=document_with_findings_list,
            dataSource=data_source_list
        )

        print(f'----Data {data.dict()} ----')
        return json.dumps(data.dict(), indent=4)

        #except Exception as ex:
         #   logger.error(f"Error in Dashboard app Listing. Error:{ex}")

    @staticmethod
    def get_app_details(app_dir):
        try:
            # Path to metadata.json
            app_path = f'{CacheDir.home_dir.value}/{app_dir}/{CacheDir.metadata_file_path.value}'
            logger.debug(f'metadata.json path {app_path}')
            # Reading metadata.json
            app_json = read_json_file(app_path)
            # Condition for handling loadId
            if app_json and app_json.get('load_ids') is not None and len(app_json.get('load_ids')) > 0:
                # Fetching latest loadId
                latest_load_id = app_json.get('load_ids')[-1]

                # Path to report.json
                app_detail_path = f'{CacheDir.home_dir.value}/{app_dir}/{latest_load_id}/{CacheDir.report_data_file_name.value}'
                logger.debug(f'metadata.json path {app_detail_path}')

                # Reading report.json
                app_detail_json = read_json_file(app_detail_path)
                if app_detail_json:
                    return json.dumps(app_detail_json, indent=4)
                else:
                    return json.dumps({})

            else:
                logger.debug('Error: Unable to fetch loadId details')
                logger.debug(f'App Json : {app_json}')

        except Exception as ex:
            logger.error(f"Error in app detail. Error:{ex}")