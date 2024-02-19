import json
import os
from pebblo.app.enums.enums import CacheDir
from pebblo.app.libs.logger import logger


def get_all_apps_list():
    dir_path = os.listdir(CacheDir.home_dir.value)
    all_apps = []
    app_risk = 0
    findings = 0
    files_findings = 0
    data_source = 0

    app_details = dict()
    for app_dir in dir_path:
        app_path = f'{CacheDir.home_dir.value}/{app_dir}/{CacheDir.metadata_file_path.value}'
        try:
            with open(app_path, "r") as output:
                app_json = json.load(output)
                app_details = dict()
                app_details['name'] = app_json.get('name')
                app_details['loadId'] = app_json.get('current_load_id')

        except IOError as err:
            logger.error(f"No  file found at {app_path}")

        app_detail_path = f'{CacheDir.home_dir.value}/{app_dir}/{app_json.get("current_load_id")}/{CacheDir.report_data_file_name.value}'
        try:
            with open(app_detail_path, "r") as output:
                app_detail_json = json.load(output)
                report_summary = app_detail_json.get('reportSummary')
                app_details['topics'] = report_summary.get('findingsTopics', 0)
                app_details['entities'] = report_summary.get('findingsEntities', 0)
                app_details['owner'] = report_summary.get('owner')
                findings += report_summary.get('findings', 0)
                files_findings += report_summary.get('filesWithFindings', 0)
                data_source += report_summary.get('dataSources', 0)
                if report_summary.get('findings', 0) > 0:
                    app_risk += 1
                app_details['loadId'] = app_json.get('current_load_id')

        except IOError as err:
            logger.error(f"No  file found at {app_detail_path}")
        all_apps.append(app_details)
        get_per_app_data(app_json.get('name'))
    data = {'applicationAtRisk': app_risk, 'findings': findings, 'filesWithFindings': files_findings,
            'dataSource': data_source, 'appList': all_apps}

    return json.dumps(data, indent=4)


def get_per_app_data(app_dir):
    app_path = f'{CacheDir.home_dir.value}/{app_dir}/{CacheDir.metadata_file_path.value}'

    try:
        with open(app_path, "r") as output:
            app_json = json.load(output)
            load_id = app_json.get('current_load_id')

    except IOError as err:
        logger.error(f"No  file found at {app_path}")

    app_detail_path = f'{CacheDir.home_dir.value}/{app_dir}/{load_id}/{CacheDir.report_data_file_name.value}'
    try:
        with open(app_detail_path, "r") as output:
            app_detail_json = json.load(output)
            return json.dumps(app_detail_json, indent=4)
    except IOError as err:
        logger.error(f"No file found at {app_detail_path}")