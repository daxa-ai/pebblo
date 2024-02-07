from pebblo.topic_classifier.topic_classifier import TopicClassifier
from pebblo.entity_classifier.entity_classifier import EntityClassifier

from pebblo.app.config.config import load_config
import sys

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
    if '--config' in cli_str:
        path = cli_input[-1]
        if path != '--config':
            config_details = load_config(path)
        else:
            print('Please enter valid config path')
    else:
        config_details = load_config(None)

    # Starting Uvicorn Service Using config details
    svc = Service(config_details)
    svc.start()