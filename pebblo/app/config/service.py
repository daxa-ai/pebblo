import asyncio
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles

from pebblo.app.exceptions.exception_handler import exception_handlers
from pebblo.app.routers.local_ui_routers import local_ui_router_instance
from pebblo.app.routers.redirection_router import redirect_router_instance

with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
    from pebblo.app.routers.routers import router_instance


class NoCacheStaticFiles(StaticFiles):
    def __init__(self, *args: Any, **kwargs: Any):
        self.cachecontrol = "max-age=0, no-cache, no-store, , must-revalidate"
        self.pragma = "no-cache"
        self.expires = "0"
        super().__init__(*args, **kwargs)

    def file_response(self, *args: Any, **kwargs: Any) -> Response:
        resp = super().file_response(*args, **kwargs)
        resp.headers.setdefault("Cache-Control", self.cachecontrol)
        resp.headers.setdefault("Pragma", self.pragma)
        resp.headers.setdefault("Expires", self.expires)
        return resp


class Service:
    def __init__(self, config_details):
        # Initialise app instance
        self.app = FastAPI(exception_handlers=exception_handlers)
        # Register the router instance with the main app
        self.app.include_router(router_instance.router)
        self.app.include_router(local_ui_router_instance.router)
        self.app.include_router(redirect_router_instance.router)
        # Fetching Details from Config File
        self.config_details = config_details
        self.port = self.config_details.get("daemon", {}).get("port", 8000)
        self.host = self.config_details.get("daemon", {}).get("host", "localhost")
        self.log_level = self.config_details.get("logging", {}).get("level", "info")

    async def create_main_api_server(self):
        self.app.mount(
            path="/static",
            app=NoCacheStaticFiles(
                directory=Path(__file__).parent.parent.absolute() / "pebblo-ui"
            ),
            name="static",
        )

        # Add config Details to Uvicorn
        config = uvicorn.Config(
            app=self.app, host=self.host, port=self.port, log_level=self.log_level
        )
        server = uvicorn.Server(config)
        await server.serve()

    def start(self):
        asyncio.run(self.create_main_api_server())
