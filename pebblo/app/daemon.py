import uvicorn
from fastapi import FastAPI
from pebblo.app.routers.routers import router_instance
from pebblo.app.routers.local_ui_routers import local_ui_router_instance
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pebblo.topic_classifier.topic_classifier import TopicClassifier
from pebblo.entity_classifier.entity_classifier import EntityClassifier


def start():
    # Init TopicClassifier(This step downloads the models and put in cache)
    _ = TopicClassifier()
    # Init EntityClassifier(This step downloads all necessary training models)
    _ = EntityClassifier

    # Initialise app instance
    app = FastAPI()
    # Register the router instance with the main app
    app.include_router(local_ui_router_instance.router)
    app.include_router(router_instance.router)

    app.mount(
    "/app/pebblo-ui",
    StaticFiles(directory=Path(__file__).parent.parent.absolute()/"app/pebblo-ui"),
    name="static",
    )

    # running local server
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
