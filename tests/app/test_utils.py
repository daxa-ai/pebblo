import toml
import os
from pebblo.app.utils.utils import get_pebblo_server_version, delete_directory, get_full_path


def test_get_pebblo_server_version():
    with open("pyproject.toml", "r") as file:
        data = toml.load(file)
    pebblo_version = data["project"]["version"]

    pebblo_server_version = get_pebblo_server_version()
    assert pebblo_version == pebblo_server_version


def test_delete_directory():
    # make sample directory
    app_name = "test_dir"
    dir_path = ".pebblo/test_dir"
    full_path = get_full_path(dir_path)
    os.mkdir(dir_path)
    response = delete_directory(full_path, app_name)
    assert response == f"Application {app_name} has been deleted."


def test_delete_directory_dir_not_exist():

    app_name = "test_dir"
    dir_path = ".pebblo/test_dir"
    full_path = get_full_path(dir_path)
    response = delete_directory(full_path, app_name)
    assert response == f"Application {app_name} does not exist."
