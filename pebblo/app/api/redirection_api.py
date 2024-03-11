from fastapi import APIRouter

from pebblo.app.enums.enums import CacheDir


class App:
    """
    Controller Class for all the api endpoints for redirection."""

    def __init__(self):
        self.router = APIRouter()

    @staticmethod
    def redirect():
        return f"{CacheDir.PROXY.value}/pebblo/"
