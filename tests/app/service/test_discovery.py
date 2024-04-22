import datetime
import json
from unittest.mock import MagicMock, patch

import pytest
from pebblo.app.service.discovery_service import AppDiscover


# static, datetime.now()
mocked_datetime = datetime.datetime(2024, 1, 1, 0, 0, 5)

data = {
    "metadata": {
        "createdAt": mocked_datetime,
        "modifiedAt": mocked_datetime
    },
    "name": "RetrivalDiscoveryApp17thApr011",
    "description": "",
    "owner": "Shreyas Damle",
    "pluginVersion": "0.1.0",
    "instanceDetails": {
        "type": None,
        "host": "OPLPT118",
        "path": "D:/OpcitoWorkDirectory/CloudDefense/pebblo-langchain/samples/medical-advice/testing_apps",
        "runtime": None,
        "ip": "172.17.128.1",
        "language": "python",
        "languageVersion": "3.11.8",
        "platform": "Windows-10-10.0.19045-SP0",
        "os": "Windows",
        "osVersion": "10.0.19045",
        "createdAt": mocked_datetime
    },
    "framework": {
        "name": "langchain",
        "version": "0.1.37"
    },
    "lastUsed": mocked_datetime,
    "pebbloServerVersion": "0.1.13",
    "pebbloClientVersion": "0.1.0",
    "chains": [
        {
            "name": "RetrievalQA",
            "vectorDbs": [
                {
                    "name": "Chroma",
                    "version": "0.4.7",
                    "location": None,
                    "embeddingModel": "OpenAIEmbeddings",
                    "pkgInfo": None
                }
            ],
            "model": {
                "name": "text-davinci-003",
                "vendor": "openai"
            }
        }
    ]
}



@pytest.fixture
def discovery():
    return AppDiscover(data)


def test_fetch_runtime_instance_details(discovery):
    """
        Testing fetching runtime instance details from discovery service
    :param discovery:
    :return:
    """
    # Mocking datetime.now()
    discovery._get_current_datetime = MagicMock(return_value=mocked_datetime)

    expected_output = {'type': None, 'host': None, 'path': None, 'runtime': None, 'ip': None, 'language': None, 'languageVersion': None, 'platform': None, 'os': None, 'osVersion': None, 'createdAt': mocked_datetime}
    output = discovery._fetch_runtime_instance_details()
    print(f"Output: {output.dict()}")
    assert expected_output == output.dict()


def test_fetch_chain_details(discovery):
    """
        Testing fetching chain details function from discovery service
    :param discovery:
    :return:
    """
    # Mocking datetime.now()
    discovery._get_current_datetime = MagicMock(return_value=mocked_datetime)
    expected_output = [{'name': 'RetrievalQA', 'vectorDbs': [], 'model': {'name': 'text-davinci-003', 'vendor': 'openai'}}]
    output = discovery._fetch_chain_details()
    print(f"Output: {output}")
    assert output == expected_output


def test_create_ai_apps_model(discovery):
    """
        Testing create_ai_apps_model from discovery_service
    :param discovery:
    :return:
    """
    # Mocking datetime.now()
    discovery._get_current_datetime = MagicMock(return_value=mocked_datetime)

    instance_details = {'type': None, 'host': None, 'path': None, 'runtime': None, 'ip': None, 'language': None, 'languageVersion': None, 'platform': None, 'os': None, 'osVersion': None, 'createdAt': mocked_datetime}
    chain_details = [{'name': 'RetrievalQA', 'vectorDbs': [], 'model': {'name': 'text-davinci-003', 'vendor': 'openai'}}]
    expected_output = {'metadata': {'createdAt': mocked_datetime, 'modifiedAt': mocked_datetime}, 'name': 'RetrivalDiscoveryApp17thApr011', 'description': '', 'owner': 'Shreyas Damle', 'pluginVersion': None, 'instanceDetails': {'type': None, 'host': None, 'path': None, 'runtime': None, 'ip': None, 'language': None, 'languageVersion': None, 'platform': None, 'os': None, 'osVersion': None, 'createdAt': mocked_datetime}, 'framework': {'name': 'langchain', 'version': '0.1.37'}, 'lastUsed': mocked_datetime, 'pebbloServerVersion': '0.1.14', 'pebbloClientVersion': '', 'chains': [{'name': 'RetrievalQA', 'vectorDbs': [], 'model': {'name': 'text-davinci-003', 'vendor': 'openai'}}]}
    output = discovery._create_ai_apps_model(instance_details, chain_details)
    print(output)
    assert output == expected_output

