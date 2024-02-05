from pebblo.app.config.config import load_config
import sys
import os
import argparse


config_details = {}


def start():
    global config_details
    # For loading config file details
    parser = argparse.ArgumentParser(description="Pebblo  CLI")
    parser.add_argument('--config', type=str, help="Config file path")
    args = parser.parse_args()
    path = args.config
    config_details = load_config(path)

    # LazyLoading TopicClassifier and EntityClassifier to avoid circular dependency
    from pebblo.topic_classifier.topic_classifier import TopicClassifier
    from pebblo.entity_classifier.entity_classifier import EntityClassifier
    # Init TopicClassifier(This step downloads the models and put in cache)
    _ = TopicClassifier()
    # Init EntityClassifier(This step downloads all necessary training models)
    _ = EntityClassifier

    # Starting Uvicorn Service Using config details
    from pebblo.app.config.service import Service
    svc = Service(config_details)
    svc.start()