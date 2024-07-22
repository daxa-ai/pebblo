import tempfile

import toml

from pebblo.app.utils.utils import (
    delete_directory,
    get_full_path,
    get_pebblo_server_version,
)


def test_get_pebblo_server_version():
    with open("pyproject.toml", "r") as file:
        data = toml.load(file)
    pebblo_version = data["project"]["version"]

    pebblo_server_version = get_pebblo_server_version()
    assert pebblo_version == pebblo_server_version


def test_delete_directory():
    # make sample directory
    dir_path = tempfile.mkdtemp()
    full_path = get_full_path(dir_path)
    response = delete_directory(full_path, dir_path)
    assert response == {
        "message": f"Application {dir_path} has been deleted.",
        "status_code": 200
    }


def test_delete_directory_dir_not_exist():
    app_name = "test_dir"
    dir_path = ".pebblo/test_dir"
    full_path = get_full_path(dir_path)
    response = delete_directory(full_path, app_name)
    assert response == {
        "message": f"Application {app_name} does not exist.",
        "status_code": 404
    }
