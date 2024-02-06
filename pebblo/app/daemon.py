import uvicorn
from fastapi import FastAPI
from pebblo.app.routers.routers import router_instance

from pebblo.topic_classifier.topic_classifier import TopicClassifier
from pebblo.entity_classifier.entity_classifier import EntityClassifier

from pebblo.app.config.config import load_config
import sys

from pebblo.app.config.service import Service


def get_config_file_path():
    pass


def start():
    # Init TopicClassifier(This step downloads the models and put in cache)
    _ = TopicClassifier()
    # Init EntityClassifier(This step downloads all necessary training models)
    _ = EntityClassifier

    # CLI input details
    cli_input = sys.argv[1:]
    cli_str = ' '.join(cli_input)
    config_details = {}

    # For loading config file details
    if '--help --config' in cli_str:
        path = cli_input[-1]
        print(f'----Path {path}-----')
        config_details = load_config(path)
        print(config_details)
    else:
        config_details = load_config(None)

    print('Statrting Service')
    svc = Service(config_details)
    svc.start()
    # Initialise app instance
    # app = FastAPI()
    # # Register the router instance with the main app
    # app.include_router(router_instance.router)
    #
    # # running local server
    # uvicorn.run(app, host="localhost", port=8000, log_level="info")
