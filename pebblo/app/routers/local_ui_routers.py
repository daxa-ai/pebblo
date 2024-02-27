from pebblo.app.api.local_ui_api import App
from fastapi.responses import HTMLResponse

# Create an instance of APp with a specific prefix
local_ui_router_instance = App(prefix="/pebblo")

# Add routes to the class-based router
local_ui_router_instance.router.add_api_route(
    "/", App.dashboard, methods=["GET"], response_class=HTMLResponse
)
local_ui_router_instance.router.add_api_route(
    "/app/", App.appDetails, methods=["GET"], response_class=HTMLResponse
)
local_ui_router_instance.router.add_api_route(
    "/report/", App.getReport, methods=["GET"], response_class=dict
)
