import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api import router as api_router

app = FastAPI()
app.include_router(api_router)
templates = Jinja2Templates(directory="templates")

# @app.get('/')
# def root():
#     return {"message": "Hello"}

@app.get('/',
         response_class=HTMLResponse
         )
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/about',
         response_class=HTMLResponse
         )
def root(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

if __name__ == '__main__':
    uvicorn.run("app:app", reload=True)