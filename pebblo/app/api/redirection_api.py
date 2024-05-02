from fastapi import APIRouter, Request


class App:
    """
    Controller Class for all the api endpoints for redirection."""

    def __init__(self):
        self.router = APIRouter()

    @staticmethod
    def redirect(request: Request):
        return f"{request.base_url}pebblo/"
