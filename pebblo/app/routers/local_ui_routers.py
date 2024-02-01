from pebblo.app.api.local_ui_api import App
from fastapi.responses import HTMLResponse

# Create an instance of APp with a specific prefix
local_ui_router_instance =  App()

# Add routes to the class-based router
local_ui_router_instance.router.add_api_route("/", App.dashboard, methods=["GET"],  response_class=HTMLResponse)
local_ui_router_instance.router.add_api_route("/appDetails", App.appDetails, methods=["GET"],  response_class=HTMLResponse)
