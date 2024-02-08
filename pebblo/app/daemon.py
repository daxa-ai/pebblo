from contextlib import redirect_stderr, redirect_stdout
import os
import uvicorn
from fastapi import FastAPI
from io import StringIO
from tqdm import tqdm

p_bar = tqdm(range(10))
p_bar.desc = "Downloading models if needed"

with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
    from pebblo.app.routers.routers import router_instance
    from pebblo.topic_classifier.topic_classifier import TopicClassifier
    from pebblo.entity_classifier.entity_classifier import EntityClassifier

p_bar.update(2)
print()
def start():
    p_bar.desc="Initializing Topic Classifier."
    p_bar.update(1)
    print()
    # Init TopicClassifier(This step downloads the models and put in cache)
    with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
        _ = TopicClassifier()
    p_bar.desc = "Topic Classifier Initiated."
    p_bar.update(1)
    print()
    p_bar.desc = "Initializing Entity Classifier."
    p_bar.update(1)
    print()
    # Init EntityClassifier(This step downloads all necessary training models)
    with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
        _ = EntityClassifier
    p_bar.desc = "Entity Classifier Initiated..."
    p_bar.update(1)
    print()
    p_bar.desc = "Starting Pebblo server."
    # Initialise app instance
    app = FastAPI()
    p_bar.update(1)
    print()
    # Register the router instance with the main app
    app.include_router(router_instance.router)
    p_bar.update(2)
    print()
    p_bar.desc = "Pebblo server started."
    p_bar.close()
    print()
    # running local server
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
    print("Pebblo server stopped.")
