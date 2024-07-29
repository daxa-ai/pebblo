from fastapi import APIRouter, Request

from pebblo.app.daemon import server_version


class App:
    """
    Controller Class for all the api endpoints for redirection."""

    def __init__(self):
        self.router = APIRouter()

    @staticmethod
    def redirect(request: Request):
        return f"{request.base_url}pebblo/"

    @staticmethod
    def health(request: Request):
        return f"Pebblo Server version {server_version} is running"
