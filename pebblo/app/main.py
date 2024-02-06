from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path
from service.local_ui_service import AppLocalUI
import json


app = FastAPI()
templates = Jinja2Templates(directory="pebblo-ui")

app.mount(
    "/app/pebblo-ui",
    StaticFiles(directory=Path(__file__).parent.parent.absolute()/"app/pebblo-ui"),
    name="static",
)



@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
   return templates.TemplateResponse("index.html", {"request": request, "data": AppLocalUI.getData()})   

@app.get("/appDetails", response_class=HTMLResponse)
async def hello(request: Request, id:str):
   # appList = AppLocalUI.getData().get('appList')
   # filteredData = [obj for obj in appList if(obj['id'] == id)]
   return templates.TemplateResponse("index.html", {"request": request, "data":AppLocalUI.getData()})     
    


if(__name__) == '__main__':
        uvicorn.run(
        "app:app",
        host    = "0.0.0.0",
        port    = 8036, 
        reload  = True
)