import json
import os
from pebblo.app.enums.enums import CacheDir
from pebblo.app.libs.logger import logger
from pebblo.app.utils.utils import get_full_path, read_json_file


def get_all_apps_list():
    try:
        dir_full_path = get_full_path(CacheDir.home_dir.value)
        dir_path = os.listdir(dir_full_path)
        data_source_list = []
        all_apps = []
        app_risk = 0
        findings = 0
        files_findings = 0
        data_source = 0

        for app_dir in dir_path:
            app_path = f'{CacheDir.home_dir.value}/{app_dir}/{CacheDir.metadata_file_path.value}'
            app_full_path = get_full_path(app_path)
            app_details = dict()
            app_json = read_json_file(app_full_path)
            if app_json:
                app_details['name'] = app_json.get('name')
                app_details['loadId'] = app_json.get('load_ids')[-1]

                app_detail_path = f'{CacheDir.home_dir.value}/{app_dir}/{app_json.get("load_ids")[-1]}/{CacheDir.report_data_file_name.value}'

                app_detail_full_path = get_full_path(app_detail_path)

                app_detail_json = read_json_file(app_detail_full_path)
                if app_detail_json:
                    report_summary = app_detail_json.get('reportSummary')
                    app_details['topics'] = report_summary.get('findingsTopics', 0)
                    app_details['entities'] = report_summary.get('findingsEntities', 0)
                    app_details['owner'] = report_summary.get('owner')
                    findings += report_summary.get('findings', 0)
                    files_findings += report_summary.get('filesWithFindings', 0)
                    data_source += report_summary.get('dataSources', 0)
                    data_source_list.extend(app_detail_json.get('dataSources'))
                    if report_summary.get('findings', 0) > 0:
                        app_risk += 1
                    app_details['loadId'] = app_json.get('load_ids')[-1]

                    all_apps.append(app_details)
                    get_per_app_data(app_json.get('name'))
        data = {'applicationAtRisk': app_risk, 'findings': findings, 'filesWithFindings': files_findings,
                'dataSource': data_source, 'appList': all_apps, 'dataSourceList': data_source_list}

        return json.dumps(data, indent=4)

    except Exception as ex:
        logger.error(f"Error in process_request. Error:{ex}")


def get_per_app_data(app_dir):
    try:
        app_path = f'{CacheDir.home_dir.value}/{app_dir}/{CacheDir.metadata_file_path.value}'
        app_full_path = get_full_path(app_path)
        app_json = read_json_file(app_full_path)
        if app_json:
            load_id = app_json.get('load_ids')[-1]

            app_detail_path = f'{CacheDir.home_dir.value}/{app_dir}/{load_id}/{CacheDir.report_data_file_name.value}'
            app_detail_full_path = get_full_path(app_detail_path)

            app_detail_json = read_json_file(app_detail_full_path)
            if app_detail_json:
                return json.dumps(app_detail_json, indent=4)
            else:
                return {}

    except Exception as ex:
        logger.error(f"Error in process_request. Error:{ex}")
