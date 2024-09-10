"""
Routes for Pebblo Server
"""

from pebblo.app.api.api import App
from pebblo.app.api.v1 import APIv1

# Create an instance of APp with a specific prefix
router_instance = App(prefix="/v1")
api_v1_router_instance = APIv1(prefix="/api/v1")

# Add routes to the class-based router
router_instance.router.add_api_route(
    "/app/discover", App.discover, methods=["POST"], response_model=dict
)
router_instance.router.add_api_route(
    "/loader/doc",
    App.loader_doc,
    methods=["POST"],
    response_model=dict,
    response_model_exclude_none=True,
)
router_instance.router.add_api_route(
    "/prompt",
    App.prompt,
    methods=["POST"],
    response_model=dict,
    response_model_exclude_none=True,
)
router_instance.router.add_api_route(
    "/prompt/governance",
    App.promptgov,
    methods=["POST"],
    response_model=dict,
    response_model_exclude_none=True,
)

api_v1_router_instance.router.add_api_route(
    "/classify",
    APIv1.classify_data,
    methods=["POST"],
    response_model=dict,
    response_model_exclude_none=True,
)
