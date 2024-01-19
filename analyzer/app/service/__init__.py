import uvicorn
from fastapi import FastAPI
from app.routers.routers import router_instance

def start():
    # Initialise app instance
    app = FastAPI()

    # Register the router instance with the main app
    app.include_router(router_instance.router)

    # running local server
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
