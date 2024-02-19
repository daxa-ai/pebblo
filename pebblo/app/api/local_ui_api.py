from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pebblo.app.service.local_ui_service import AppLocalUI

templates = Jinja2Templates(directory="pebblo/app/pebblo-ui")

class App:
    """
        Controller Class for all the api endpoints for local ui.
    """
    def __init__(self):
        self.router = APIRouter()

    @staticmethod
    def dashboard(request: Request):
        return templates.TemplateResponse("index.html", {"request": request, "data":AppLocalUI.get_all_apps_list()})

    @staticmethod
    def appDetails(request: Request, app_name: str, id: str):
        return templates.TemplateResponse("index.html", {"request": request, "data":AppLocalUI.getData(app_name, id)})