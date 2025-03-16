from fastapi import APIRouter, HTTPException, status, Request, Form
from typing import Annotated
from pydantic import PositiveInt
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.books.schemas import BookRead, BookCreate
from api.books.crud import books

router = APIRouter(
    tags=['HTML']
)
templates = Jinja2Templates(directory="templates")


@router.get(
    '/',
    response_class=HTMLResponse
)
def root(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request,
    )


@router.get(
    '/about',
    response_class=HTMLResponse
)
def about(request: Request):
    return templates.TemplateResponse(
        name="about.html",
        request=request,
    )


@router.get(
    "/books",
    response_model=list[BookRead],
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
    "/books/{book_id}",
    response_model=BookRead,
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
    "/books",
    response_model=BookCreate,
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(book_in: Annotated[BookCreate, Form()], request: Request):
    """
    Create a new book.
    """
    if book_in:
        books.create(book_in)
        return templates.TemplateResponse(
            name="books.html",
            request=request,
            context={"books": books.get(), "id": None, "status": "created"}
        )
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Validation Error",
    )

