"""
This is entry point for Pebblo(Pebblo Server and Local UI)
"""

import argparse
import warnings

from tqdm import tqdm

from pebblo.app.config.config import (
    load_config,
    var_server_config,
    var_server_config_dict,
)
from pebblo.app.utils.version import get_pebblo_version

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

server_version = get_pebblo_version()


def start():
    """Entry point for pebblo-server."""

    # For loading config file details
    parser = argparse.ArgumentParser(description="Pebblo  CLI")
    parser.add_argument("-c", "--config", type=str, help="config file path")
    parser.add_argument(
        "-v", "--version", action="store_true", help="display the version"
    )
    args = parser.parse_args()
    if args.version:
        print(f"Pebblo Server version: {server_version}")
        exit(0)

    path = args.config
    p_bar = tqdm(range(10))
    config_details, server_config = load_config(path)
    var_server_config_dict.set(config_details)
    var_server_config.set(server_config)
    server_start(config_details, p_bar)


def classifier_init(p_bar):
    """Initialize topic and entity classifier."""
    p_bar.write("Downloading topic, entity classifier models ...")
    from pebblo.entity_classifier.entity_classifier import EntityClassifier
    from pebblo.topic_classifier.topic_classifier import TopicClassifier

    p_bar.update(3)
    p_bar.write("Initializing topic classifier ...")
    p_bar.update(1)

    # Init TopicClassifier(This step downloads the models and put in cache)
    _ = TopicClassifier()
    p_bar.write("Initializing topic classifier ... done")
    p_bar.update(1)

    p_bar.write("Initializing entity classifier ...")
    p_bar.update(1)

    # Init EntityClassifier(This step downloads all necessary training models)
    _ = EntityClassifier()
    p_bar.write("Initializing entity classifier ... done")
    p_bar.update(1)


def server_start(config: dict, p_bar: tqdm):
    """Start server."""
    p_bar.write(f"Pebblo server version {server_version} starting ...")

    # Initialize Topic and Entity Classifier
    classifier_init(p_bar)

    # Starting Uvicorn Service Using config details
    from pebblo.app.config.service import Service

    p_bar.update(1)
    svc = Service(config_details=config)
    p_bar.update(2)
    p_bar.close()
    svc.start()
    print("Pebblo server stopped. BYE!")


if __name__ == "__main__":
    start()
