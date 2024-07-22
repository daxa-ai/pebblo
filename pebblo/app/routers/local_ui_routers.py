from fastapi.responses import FileResponse, HTMLResponse

from pebblo.app.api.local_ui_api import App

# Create an instance of APp with a specific prefix
local_ui_router_instance = App(prefix="/pebblo")

# Add routes to the class-based router
local_ui_router_instance.router.add_api_route(
    "/", App.dashboard, methods=["GET"], response_class=HTMLResponse
)
local_ui_router_instance.router.add_api_route(
    "/safe_retrieval/", App.dashboard, methods=["GET"], response_class=HTMLResponse
)
local_ui_router_instance.router.add_api_route(
    "/app/", App.app_details, methods=["GET"], response_class=HTMLResponse
)
local_ui_router_instance.router.add_api_route(
    "/safe_retrieval/app/",
    App.app_details,
    methods=["GET"],
    response_class=HTMLResponse,
)
local_ui_router_instance.router.add_api_route(
    "/report/", App.get_report, methods=["GET"], response_class=FileResponse
)
local_ui_router_instance.router.add_api_route(
    "/not-found/", App.page_not_found, methods=["GET"], response_class=HTMLResponse
)
local_ui_router_instance.router.add_api_route(
    "/app/delete/", App.delete_app, methods=["DELETE"]
)
