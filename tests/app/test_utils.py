import toml

from pebblo.app.utils.utils import get_pebblo_server_version


def test_get_pebblo_server_version():
    with open('../../pyproject.toml', 'r') as file:
        data = toml.load(file)
    pebblo_version = data["project"]["version"]

    pebblo_server_version = get_pebblo_server_version()
    assert pebblo_version == pebblo_server_version
