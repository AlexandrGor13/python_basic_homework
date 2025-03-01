import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api import router as api_router

app = FastAPI()
app.include_router(api_router)
templates = Jinja2Templates(directory="templates")
app.mount("/img", StaticFiles(directory="docs/img"))


@app.get('/',
         response_class=HTMLResponse
         )
def root(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request,
    )


@app.get('/about',
         response_class=HTMLResponse
         )
def root(request: Request):
    return templates.TemplateResponse(
        name="about.html",
        request=request,
    )


if __name__ == '__main__':
    uvicorn.run("app:app", reload=True)
