from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from pydantic import PositiveInt

from . import schemas
from .crud import books

router = APIRouter(
    prefix='/books',
    tags=['Books'],
)


@router.get(
    "",
    response_model=list[schemas.BookRead],
    status_code=status.HTTP_200_OK,
)
def get_books():
    return books.get()


@router.get(
    "/{book_id}",
    response_model=schemas.BookRead,
    status_code=status.HTTP_200_OK,
)
def get_book(book_id: PositiveInt):
    book = books.get_by_id(book_id=book_id)
    if book:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User #{book_id} not found",
    )


@router.post(
    "",
    response_model=schemas.BookCreate,
    status_code=status.HTTP_201_CREATED
)
def create_book(book_in: schemas.BookCreate):
    books.create(book_in)
    return book_in
