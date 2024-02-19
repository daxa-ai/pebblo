from contextlib import redirect_stderr, redirect_stdout
import uvicorn

from io import StringIO
from tqdm import tqdm
from pebblo.app.config.config import load_config
import argparse


config_details = {}


def start():
    """Entry point for pebblo-server."""
    global config_details
    # For loading config file details
    parser = argparse.ArgumentParser(description="Pebblo  CLI")
    parser.add_argument('--config', type=str, help="config file path")
    args = parser.parse_args()
    path = args.config
    p_bar = tqdm(range(10))
    config_details = load_config(path)
    classifier_init(p_bar)
    server_start(config_details, p_bar)
    print("Pebblo server Stopped. BYE!")

def classifier_init(p_bar):
    """Initialize topic and entity classifier."""
    p_bar.write("Downloading topic, entity classifier models ...")
    with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
        from pebblo.topic_classifier.topic_classifier import TopicClassifier
        from pebblo.entity_classifier.entity_classifier import EntityClassifier
    p_bar.update(3)
    p_bar.write("Initializing topic classifier ...")
    p_bar.update(1)
   
    # Init TopicClassifier(This step downloads the models and put in cache)
    with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
        _ = TopicClassifier()
    p_bar.write("Initializing topic classifier ... done")
    p_bar.update(1)

    p_bar.write("Initializing entity classifier ...")
    p_bar.update(1)

    # Init EntityClassifier(This step downloads all necessary training models)
    with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
        _ = EntityClassifier()
    p_bar.write("Initializing entity classifier ... done")
    p_bar.update(1)


def server_start(config_details, p_bar):
    """Start server."""
    p_bar.write("Pebblo server starting ...")
    # Starting Uvicorn Service Using config details
    from pebblo.app.config.service import Service
    p_bar.update(1)
    svc = Service(config_details)
    p_bar.update(2)
    p_bar.close()
    svc.start()
