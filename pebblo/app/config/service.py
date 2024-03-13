import asyncio
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Response, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from pebblo.app.routers.local_ui_routers import local_ui_router_instance
from pebblo.app.routers.redirection_router import redirect_router_instance
from pebblo.app.exceptions.exception_handler import exception_handlers
from starlette.middleware.base import BaseHTTPMiddleware

with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
    from pebblo.app.routers.routers import router_instance


class AddTrailingSlashMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, excluded_extensions: list = None):
        super().__init__(app)
        self.excluded_extensions = excluded_extensions or []

    async def dispatch(self, request: Request, call_next):
        # Check if the request path doesn't end with a trailing slash and the path does not contain any excluded file extensions
        if  not request.url.path.endswith("/") and not any(request.url.path.endswith(ext) for ext in self.excluded_extensions):
            url_with_slash = request.url.replace(path=request.url.path + "/")
            return RedirectResponse(url_with_slash)
        else:
            return await call_next(request)

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
        # List of file extensions to be excluded from trailing slash redirection
        EXCLUDED_EXTENSIONS = [".css", ".js", ".png", ]
        # Register the router instance with the main app
        self.app.include_router(router_instance.router)
        self.app.include_router(local_ui_router_instance.router)
        self.app.include_router(redirect_router_instance.router)
        self.app.add_middleware(AddTrailingSlashMiddleware, excluded_extensions=EXCLUDED_EXTENSIONS)
        # Fetching Details from Config File
        self.config_details = config_details
        self.port = self.config_details.get("daemon", {}).get("port", 8000)
        self.host = self.config_details.get("daemon", {}).get("host", "localhost")
        self.log_level = self.config_details.get("logging", {}).get("level", "info")

    async def create_main_api_server(self):
        self.app.mount(
            path="/static",
            app=NoCacheStaticFiles(
                directory=Path(__file__).parent.parent.absolute() / "pebblo-ui/static"
            ),
            name="_static",
        )
        self.app.mount(
            path="/",
            app=StaticFiles(
                directory=Path(__file__).parent.parent.absolute() / "pebblo-ui"
            ),
            name="_app",
        )

        # Add config Details to Uvicorn
        config = uvicorn.Config(
            app=self.app, host=self.host, port=self.port, log_level=self.log_level
        )
        server = uvicorn.Server(config)
        await server.serve()

    def start(self):
        asyncio.run(self.create_main_api_server())
