from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path
from pebblo.app.service.local_ui_service import AppData
from fastapi.responses import FileResponse
from pebblo.app.enums.enums import CacheDir
from pebblo.app.utils.utils import get_full_path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from typing import Any

templates = Jinja2Templates(directory="pebblo/app/pebblo-ui")


async def not_found_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "index.html", {"request": request}, status_code=404
    )


async def internal_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "index.html", {"request": request}, status_code=500
    )


exception_handlers = {404: not_found_error, 500: internal_error}


class NoCacheStaticFiles(StaticFiles):
    def __init__(self, *args: Any, **kwargs: Any):
        self.cachecontrol = "max-age=0, no-cache, no-store, , must-revalidate"
        self.pragma = "no-cache"
        self.expires = "0"
        super().__init__(*args, **kwargs)

    def file_response(self, *args: Any, **kwargs: Any) -> Response:
        resp = super().file_response(*args, **kwargs)
        resp.headers.setdefault("Cache-Control", self.cachecontrol)
        resp.headers.setdefault("Pragma", self.pragma)
        resp.headers.setdefault("Expires", self.expires)
        return resp


app = FastAPI(exception_handlers=exception_handlers)

app.mount(
    "/pebblo/pebblo/app/pebblo-ui",
    NoCacheStaticFiles(
        directory=Path(__file__).parent.parent.absolute()
        / "pebblo/pebblo/app/pebblo-ui"
    ),
    name="static",
)


@app.get("/", response_class=RedirectResponse)
async def hello():
    return f"{CacheDir.proxy.value}/pebblo"


@app.get("/pebblo/")
async def hello(request: Request, response: Response):
    response.headers["Content-Type"] = "text/html"
    app_data = AppData()
    response = templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"data": app_data.get_all_apps_details()},
    )
    return response


@app.get("/pebblo/app/")
async def hello(request: Request, app_name: str):
    app_data = AppData()
    response = templates.TemplateResponse(
        "index.html", {"request": request, "data": app_data.get_app_details(app_name)}
    )
    return response


@app.get("/pebblo/report/")
async def hello(request: Request, app_name: str):
    # File path for app report
    file_path = f"{get_full_path(CacheDir.home_dir.value)}/{app_name}/pebblo_report.pdf"
    # To view the file in the browser, use "inline" for the media_type
    headers = {"Access-Control-Expose-Headers": "Content-Disposition"}
    # Create a FileResponse object with the file path, media type and headers
    response = FileResponse(
        file_path,
        filename="pebblo_report.pdf",
        media_type="application/pdf",
        headers=headers,
    )
    # Return the FileResponse object
    return response


if (__name__) == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8036,
        reload=True,
    )
