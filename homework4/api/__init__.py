from fastapi import APIRouter

from api.about import router as about_router
from api.books.views import router as books_router

router = APIRouter(
    prefix='/api',
    tags=['API'],
)
router.include_router(about_router)
router.include_router(books_router)