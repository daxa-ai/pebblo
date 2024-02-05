from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import asyncio
from pebblo.app.routers.routers import router_instance

from pebblo.app.config.config import load_config


class Service:
    def __init__(self, config_details):
        # Initialise app instance
        self.app = FastAPI()
        # Register the router instance with the main app
        self.app.include_router(router_instance.router)
        # Fetching Details from Config File
        print(f'----Config Details {config_details} -----')
        self.config_details = config_details
        self.port = self.config_details.get('daemon', {}).get('port', 8000)
        self.host = self.config_details.get('daemon', {}).get('host', '0.0.0.0')
        # self.origin = ["http://localhost:3000",]

        # main external app/port
        # self.app.add_middleware(
        #     CORSMiddleware,
        #     allow_origins=self.origin,
        #     allow_credentials=True,
        #     allow_methods=["*"],
        #     allow_headers=["*"],
        # )
    async def create_main_api_server(self):
        # Add config Details to Uvicorn
        config = uvicorn.Config(app=self.app, host=self.host, port=self.port)
        server = uvicorn.Server(config)
        await server.serve()

    def start(self):
        asyncio.run(self.create_main_api_server())



