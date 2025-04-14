from fastapi import FastAPI

from api import router as api_router
from create_fastapi_app import create_app


app: FastAPI = create_app(
    create_custom_static_urls=True,
)

app.include_router(api_router)

