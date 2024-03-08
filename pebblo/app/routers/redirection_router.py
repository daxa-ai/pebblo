from fastapi.responses import RedirectResponse

from pebblo.app.api.redirection_api import App

# Create an instance of APp with a specific prefix
redirect_router_instance = App()

# Add routes to the class-based router
redirect_router_instance.router.add_api_route(
    "/", App.redirect, methods=["GET"], response_class=RedirectResponse
)
