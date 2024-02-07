from pebblo.topic_classifier.topic_classifier import TopicClassifier
from pebblo.entity_classifier.entity_classifier import EntityClassifier

from pebblo.app.config.config import load_config
import sys
import argparse

from pebblo.app.config.service import Service

config_details = {}


def start():
    # Init TopicClassifier(This step downloads the models and put in cache)
    _ = TopicClassifier()
    # Init EntityClassifier(This step downloads all necessary training models)
    _ = EntityClassifier

    # CLI input details
    cli_input = list(sys.argv)
    cli_str = ' '.join(cli_input)
    global config_details

    # For loading config file details
    parser = argparse.ArgumentParser(description="Pebblo  CLI")
    parser.add_argument('--config', type=str, help="Config file path")
    args = parser.parse_args()
    path = args.config
    config_details = load_config(path)

    # Starting Uvicorn Service Using config details
    svc = Service(config_details)
    svc.start()