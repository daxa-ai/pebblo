import datetime
from typing import List
from unittest.mock import MagicMock

import pytest

from pebblo.app.service.discovery_service import AppDiscover

# static, datetime.now()
mocked_datetime = datetime.datetime(2024, 1, 1, 0, 0, 5)

data = {
    "name": "pytest_app",
    "owner": "Shreyas Damle",
    "description": "",
    "load_id": "fcd41d2c-e1af-4e26-abe5-52e539c414b4",
    "runtime": {
        "type": "desktop",
        "host": "OPLPT086.local",
        "path": "/Users/shreyas.damle/Documents/Opcito/CD/pebblo-langchain/samples/medical-advice/testing_apps",
        "ip": "127.0.0.1",
        "platform": "macOS-14.4.1-arm64-arm-64bit",
        "os": "Darwin",
        "os_version": "Darwin Kernel Version 23.4.0: Fri Mar 15 00:19:22 PDT 2024; root:xnu-10063.101.17~1/RELEASE_ARM64_T8112",
        "language": "python",
        "language_version": "3.9.19",
        "runtime": "Mac OSX",
    },
    "chains": [
        {
            "name": "RetrievalQA",
            "model": {"vendor": "openai", "name": "text-davinci-003"},
            "vector_dbs": [
                {
                    "name": "Chroma",
                    "version": "0.4.7",
                    "location": "local",
                    "embedding_model": "OpenAIEmbeddings",
                    "pkg_info": {
                        "project_home_page": "https://github.com/chroma-core/chroma",
                        "documentation_url": "https://docs.trychroma.com",
                        "pypi_url": "https://pypi.org/pypi/chromadb",
                        "licence_type": "OSI Approved :: Apache Software License",
                        "installed_via": "PIP Installation",
                        "location": "/home/ubuntu/denali/rag/langchain/samples/basic-retrieval-qa/.ai_venv/lib/python3.10/site-packages/chromadb",
                    },
                }
            ],
        }
    ],
    "framework": {"name": "langchain", "version": "0.1.45"},
    "plugin_version": "0.1.1",
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

    expected_output = {
        "type": "desktop",
        "host": "OPLPT086.local",
        "path": "/Users/shreyas.damle/Documents/Opcito/CD/pebblo-langchain/samples/medical-advice/testing_apps",
        "ip": "127.0.0.1",
        "platform": "macOS-14.4.1-arm64-arm-64bit",
        "os": "Darwin",
        "osVersion": "Darwin Kernel Version 23.4.0: Fri Mar 15 00:19:22 PDT 2024; root:xnu-10063.101.17~1/RELEASE_ARM64_T8112",
        "language": "python",
        "languageVersion": "3.9.19",
        "runtime": "Mac OSX",
        "createdAt": mocked_datetime,
    }
    output = discovery._fetch_runtime_instance_details()
    assert expected_output == output.dict()


def test_fetch_chain_details(discovery):
    """
        Testing fetching chain details function from discovery service
    :param discovery:
    :return:
    """
    # Mocking datetime.now()
    discovery._get_current_datetime = MagicMock(return_value=mocked_datetime)
    expected_output = [
        {
            "name": "RetrievalQA",
            "vectorDbs": [
                {
                    "name": "Chroma",
                    "version": "0.4.7",
                    "location": "local",
                    "embeddingModel": "OpenAIEmbeddings",
                    "pkgInfo": {
                        "documentationUrl": "https://docs.trychroma.com",
                        "projectHomePage": "https://github.com/chroma-core/chroma",
                        "pypiUrl": "https://pypi.org/pypi/chromadb",
                        "licenceType": "OSI Approved :: Apache Software License",
                        "installedVia": "PIP Installation",
                        "location": "/home/ubuntu/denali/rag/langchain/samples/basic-retrieval-qa/.ai_venv/lib/python3.10/site-packages/chromadb",
                    },
                }
            ],
            "model": {"name": "text-davinci-003", "vendor": "openai"},
        }
    ]
    output = discovery._fetch_chain_details(app_metadata=None)
    assert output == expected_output


def test_create_ai_apps_model(discovery):
    """
        Testing create_ai_apps_model from discovery_service
    :param discovery:
    :return:
    """
    # Mocking datetime.now()
    discovery._get_current_datetime = MagicMock(return_value=mocked_datetime)

    instance_details = {
        "type": "desktop",
        "host": "OPLPT086.local",
        "path": "/Users/shreyas.damle/Documents/Opcito/CD/pebblo-langchain/samples/medical-advice/testing_apps",
        "runtime": "Mac OSX",
        "ip": "127.0.0.1",
        "language": "python",
        "languageVersion": "3.9.19",
        "platform": "macOS-14.4.1-arm64-arm-64bit",
        "os": "Darwin",
        "osVersion": "Darwin Kernel Version 23.4.0: Fri Mar 15 00:19:22 PDT 2024; root:xnu-10063.101.17~1/RELEASE_ARM64_T8112",
        "createdAt": datetime.datetime(2024, 1, 1, 0, 0, 5),
    }
    chain_details = [
        {
            "name": "RetrievalQA",
            "vectorDbs": [
                {
                    "name": "Chroma",
                    "version": "0.4.7",
                    "location": "local",
                    "embeddingModel": "OpenAIEmbeddings",
                    "pkgInfo": {
                        "projectHomePage": "https://github.com/chroma-core/chroma",
                        "documentationUrl": "https://docs.trychroma.com",
                        "pypiUrl": "https://pypi.org/pypi/chromadb",
                        "licenceType": "OSI Approved :: Apache Software License",
                        "installedVia": "PIP Installation",
                        "location": "/home/ubuntu/denali/rag/langchain/samples/basic-retrieval-qa/.ai_venv/lib/python3.10/site-packages/chromadb",
                    },
                }
            ],
            "model": {"name": "text-davinci-003", "vendor": "openai"},
        }
    ]
    expected_output = {
        "metadata": {
            "createdAt": datetime.datetime(2024, 1, 1, 0, 0, 5),
            "modifiedAt": datetime.datetime(2024, 1, 1, 0, 0, 5),
        },
        "name": "pytest_app",
        "description": "",
        "owner": "Shreyas Damle",
        "pluginVersion": "0.1.1",
        "instanceDetails": {
            "type": "desktop",
            "host": "OPLPT086.local",
            "path": "/Users/shreyas.damle/Documents/Opcito/CD/pebblo-langchain/samples/medical-advice/testing_apps",
            "ip": "127.0.0.1",
            "platform": "macOS-14.4.1-arm64-arm-64bit",
            "os": "Darwin",
            "osVersion": "Darwin Kernel Version 23.4.0: Fri Mar 15 00:19:22 PDT 2024; root:xnu-10063.101.17~1/RELEASE_ARM64_T8112",
            "language": "python",
            "languageVersion": "3.9.19",
            "runtime": "Mac OSX",
            "createdAt": mocked_datetime,
        },
        "framework": {"name": "langchain", "version": "0.1.45"},
        "lastUsed": datetime.datetime(2024, 1, 1, 0, 0, 5),
        "pebbloServerVersion": "0.1.15",
        "pebbloClientVersion": "0.1.1",
        "chains": [
            {
                "name": "RetrievalQA",
                "vectorDbs": [
                    {
                        "name": "Chroma",
                        "version": "0.4.7",
                        "location": "local",
                        "embeddingModel": "OpenAIEmbeddings",
                        "pkgInfo": {
                            "projectHomePage": "https://github.com/chroma-core/chroma",
                            "documentationUrl": "https://docs.trychroma.com",
                            "pypiUrl": "https://pypi.org/pypi/chromadb",
                            "licenceType": "OSI Approved :: Apache Software License",
                            "installedVia": "PIP Installation",
                            "location": "/home/ubuntu/denali/rag/langchain/samples/basic-retrieval-qa/.ai_venv/lib/python3.10/site-packages/chromadb",
                        },
                    }
                ],
                "model": {"name": "text-davinci-003", "vendor": "openai"},
            }
        ],
        "retrievals": [],
    }
    retrievals_details: List = []
    output = discovery._create_ai_apps_model(
        instance_details, chain_details, retrievals_details
    )
    assert output == expected_output
