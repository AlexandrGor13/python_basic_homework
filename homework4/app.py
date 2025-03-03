import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api import router as api_router
from html.views import router as html_router

app = FastAPI()
app.include_router(api_router)
app.include_router(html_router)

app.mount("/img", StaticFiles(directory="docs/img"))





if __name__ == '__main__':
    uvicorn.run("app:app", reload=True)
