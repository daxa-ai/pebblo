from contextlib import redirect_stderr, redirect_stdout
from fastapi import FastAPI
from io import StringIO
import uvicorn
import asyncio

with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
    from pebblo.app.routers.routers import router_instance


class Service:
    def __init__(self, config_details):
        # Initialise app instance
        self.app = FastAPI()
        # Register the router instance with the main app
        self.app.include_router(router_instance.router)
        # Fetching Details from Config File
        self.config_details = config_details
        self.port = self.config_details.get('daemon', {}).get('port', 8000)
        self.host = self.config_details.get('daemon', {}).get('host', 'localhost')
        self.log_level = self.config_details.get('logging', {}).get('level', 'info')

    async def create_main_api_server(self):
        # Add config Details to Uvicorn
        config = uvicorn.Config(app=self.app, host=self.host, port=self.port, log_level=self.log_level)
        server = uvicorn.Server(config)
        await server.serve()

    def start(self):
        asyncio.run(self.create_main_api_server())



