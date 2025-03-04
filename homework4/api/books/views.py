from fastapi import APIRouter, HTTPException, status, Request
from pydantic import PositiveInt
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from . import schemas
from .crud import books

router = APIRouter(
    prefix='/books'
)


@router.get(
    "",
    response_model=list[schemas.BookRead],
    status_code=status.HTTP_200_OK,
)
def get_books(request: Request):
    """
    Get all books.
    """
    return JSONResponse(content=jsonable_encoder(books.get()))


@router.get(
    "/{book_id}",
    response_model=schemas.BookRead,
    status_code=status.HTTP_200_OK
)
def get_book(book_id: PositiveInt, request: Request):
    """
    Get a book by id.
    """
    book = books.get_by_id(book_id=book_id)
    if book:
        return JSONResponse(content=jsonable_encoder(book))

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book #{book_id} not found",
    )


@router.post(
    "",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED
)
def create_book(book_in: schemas.BookCreate):
    """
    Create a new book.
    """
    return JSONResponse(content=jsonable_encoder(books.create(book_in=book_in)))
