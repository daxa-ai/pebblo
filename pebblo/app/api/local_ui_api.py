from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from pebblo.app.enums.enums import CacheDir
from pebblo.app.service.local_ui_service import AppData
from pebblo.app.utils.utils import get_full_path

templates = Jinja2Templates(
    directory=Path(__file__).parent.parent.absolute() / "pebblo-ui"
)


class App:
    """
    Controller Class for all the api endpoints for local ui.
    """

    def __init__(self, prefix: str):
        self.router = APIRouter(prefix=prefix)

    @staticmethod
    def dashboard(request: Request):
        app_data = AppData()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "data": app_data.get_all_apps_details(),
                "proxy": CacheDir.PROXY.value,
            },
        )

    @staticmethod
    def app_details(request: Request, app_name: str):
        app_data = AppData()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "data": app_data.get_app_details(app_name),
                "proxy": CacheDir.PROXY.value,
            },
        )

    @staticmethod
    def get_report(app_name: str):
        # File path for app report
        file_path = f"{get_full_path(CacheDir.HOME_DIR.value)}/{app_name}/{CacheDir.REPORT_FILE_NAME.value}"
        # To view the file in the browser, use "inline" for the media_type
        headers = {"Access-Control-Expose-Headers": "Content-Disposition"}
        # Create a FileResponse object with the file path, media type and headers
        response = FileResponse(
            file_path,
            filename="report.pdf",
            media_type="application/pdf",
            headers=headers,
        )
        # Return the FileResponse object
        return response

    @staticmethod
    def delete_app(request: Request, app_name: str):
        app_data = AppData()
        result = app_data.delete_application(app_name)
        return result

    @staticmethod
    def page_not_found(request: Request):
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "data": {},
                "proxy": CacheDir.PROXY.value,
            },
        )
