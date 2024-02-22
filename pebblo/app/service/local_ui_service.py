import json
import os
from pebblo.app.enums.enums import CacheDir
from pebblo.app.libs.logger import logger
from pebblo.app.utils.utils import get_full_path, read_json_file
from pebblo.app.models.models import AppListDetails, AppModel


class AppData:
    @staticmethod
    def get_all_apps_details():
        """Returns all necessary app details required for listing."""
        try:
            dir_full_path = get_full_path(CacheDir.home_dir.value)
            # List all apps in the directory
            dir_path = os.listdir(dir_full_path)

            # Default values
            data_source_list = []
            all_apps = []
            apps_at_risk = 0
            findings = 0
            files_findings = 0
            data_source = 0

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
                        app_details = AppListDetails(
                            name=app_json.get('name'),
                            topics=report_summary.get('findingsTopics', 0),
                            entities=report_summary.get('findingsEntities', 0),
                            owner=report_summary.get('owner'),
                            loadId=latest_load_id
                        )

                        # Fetching dataSources
                        data_source_details = app_detail_json.get('dataSources')
                        # Fetching only required values for dashboard pages
                        if data_source_details and len(data_source_details) > 0:
                            for data in data_source_details:
                                # Deleting findingsSummary from dataSources
                                if data.get('findingsSummary'):
                                    del data['findingsSummary']
                                if data.get('findingsDetails') and len(data.get('findingsDetails')) > 0:
                                    for details in data.get('findingsDetails'):
                                        # Deleting snippet from dataSources
                                        if details.get('snippets') and len(details.get('snippets')) > 0:
                                            for snippet_detail in details.get('snippets'):
                                                if snippet_detail.get('snippet'):
                                                    del snippet_detail['snippet']
                        # appending only required value for dashboard
                        data_source_list.append(data_source_details)
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
                dataSources=data_source_list
            )
            return json.dumps(data.dict(), indent=4)

        except Exception as ex:
            logger.error(f"Error in process_request. Error:{ex}")

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
            logger.error(f"Error in process_request. Error:{ex}")