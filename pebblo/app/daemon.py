from contextlib import redirect_stderr, redirect_stdout
import uvicorn
from fastapi import FastAPI
from io import StringIO
from tqdm import tqdm

p_bar = tqdm(range(10))
p_bar.write("Downloading models if needed...")
with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
    from pebblo.app.routers.routers import router_instance
    from pebblo.topic_classifier.topic_classifier import TopicClassifier
    from pebblo.entity_classifier.entity_classifier import EntityClassifier
p_bar.update(3)

def start():
    p_bar.write("Topic Classifier Initializing.")
    p_bar.update(1)

    # Init TopicClassifier(This step downloads the models and put in cache)
    with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
        _ = TopicClassifier()
    p_bar.write("Topic Classifier Initialized...")
    p_bar.update(1)

    p_bar.write("Entity Classifier Initializing.")
    p_bar.update(1)

    # Init EntityClassifier(This step downloads all necessary training models)
    with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
        _ = EntityClassifier()
    p_bar.write("Entity Classifier Initialized...")
    p_bar.update(1)

    p_bar.write("Pebblo server Starting.")
    # Initialise app instance
    app = FastAPI()
    p_bar.update(2)

    # Register the router instance with the main app
    app.include_router(router_instance.router)
    p_bar.update(1)
    p_bar.write("Pebblo server Running. Hi!")
    p_bar.close()

    # running local server
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
    p_bar.write("Pebblo server Stopped. BYE!")
