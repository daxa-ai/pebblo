import uvicorn
from fastapi import FastAPI
from analyzer.app.routers.routers import router_instance

from analyzer.topic_classifier.topic_classifier import TopicClassifier
from analyzer.entity_classifier.entity_classifier import EntityClassifier


def start():
    # Init TopicClassifier(This step downloads the models and put in cache)
    _ = TopicClassifier()
    # Init EntityClassifier(This step downloads all necessary training models)
    _ = EntityClassifier

    # Initialise app instance
    app = FastAPI()

    # Register the router instance with the main app
    app.include_router(router_instance.router)

    # running local server
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
