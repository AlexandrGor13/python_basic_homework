from fastapi import APIRouter
from api.books.views import router as books_router

router = APIRouter(
    prefix='/api',
    tags=['API'],
)
router.include_router(books_router)