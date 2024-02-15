from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path
from service.local_ui_service import AppLocalUI
import os
from fastapi.responses import FileResponse


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
   return templates.TemplateResponse("index.html", {"request": request, "data":AppLocalUI.getAppData(id)})     


@app.get("/getReport", response_class=HTMLResponse)
async def hello(request: Request, id:str):
   # file_path = os.path.dirname(os.path.dirname(__file__))+'/reports/'+ id +'.pdf'
   file_path = os.path.dirname(os.path.dirname(__file__))+'/reports/'+id+'.pdf'

   # To view the file in the browser, use "inline" for the media_type
   headers = {
       'Access-Control-Expose-Headers': 'Content-Disposition'
   }  

   # Create a FileResponse object with the file path, media type and headers
   response = FileResponse(file_path, filename="report.pdf", media_type="application/pdf", headers=headers)

   # Return the FileResponse object
   return response
    


if(__name__) == '__main__':
        uvicorn.run(
        "app:app",
        host    = "0.0.0.0",
        port    = 8036, 
        reload  = True
)