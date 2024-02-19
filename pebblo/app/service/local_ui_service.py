import json
import os
from pebblo.app.enums.enums import CacheDir
from pebblo.app.libs.logger import logger


def get_all_apps_list():
    dir_path = os.listdir(CacheDir.home_dir.value)
    all_apps = []
    for app_dir in dir_path:
        app_path = f'{CacheDir.home_dir.value}/{app_dir}/{CacheDir.metadata_file_path.value}'
        try:
            with open(app_path, "r") as output:
                cred_json = json.load(output)
                print(cred_json)
                app_details = dict()
                app_details['name'] = cred_json.get('name')
                app_details['loadIds'] = cred_json.get('current_load_id')
                all_apps.append(app_details)

        except IOError as err:
            logger.error(f"no credentials file found at {app_path}")
    return all_apps


def get_per_app_data(app_dir, load_id):
    app_path = f'{CacheDir.home_dir.value}/{app_dir}/{load_id}/{CacheDir.report_data_file_name.value}'
    try:
        with open(app_path, "r") as output:
            cred_json = json.load(output)
            return cred_json
    except IOError as err:
        logger.error(f"no credentials file found at {app_path}")