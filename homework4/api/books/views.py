from fastapi import APIRouter, HTTPException, status, Request, Form
from typing import Annotated
from pydantic import PositiveInt
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from . import schemas
from .crud import books

router = APIRouter(
    prefix='/books',
    tags=['Books'],
)
templates = Jinja2Templates(directory="templates")


@router.get(
    "",
    response_model=list[schemas.BookRead],
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_books(request: Request):
    """
    Get all books.
    """
    return templates.TemplateResponse(
        name="books.html",
        request=request,
        context={"books": books.get(), "id": None, "status": None}
    )


@router.get(
    "/{book_id}",
    response_model=schemas.BookRead,
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_book(book_id: PositiveInt, request: Request):
    """
    Get a book by id.
    """
    book = books.get_by_id(book_id=book_id)
    if book:
        book_by_id = [books.get_by_id(book_id)]
        return templates.TemplateResponse(
            name="books.html",
            request=request,
            context={"books": book_by_id, "id": book_id, "status": None}
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User #{book_id} not found",
    )


@router.post(
    "",
    response_model=schemas.BookCreate,
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(
        title: Annotated[str, Form()],
        author: Annotated[str, Form()],
        genre: Annotated[str, Form()],
        description: Annotated[str, Form()],
        price: Annotated[float, Form()],
        quantity: Annotated[int, Form()],
        request: Request
):
    """
    Create a new book.
    """
    book = schemas.BookCreate(
        title=title,
        author=author,
        genre=genre,
        description=description,
        price=price,
        quantity=quantity
    )
    if book:
        books.create(book)
        return templates.TemplateResponse(
            name="books.html",
            request=request,
            context={"books": books.get(), "id": None, "status": "created"}
        )
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Validation Error",
    )
