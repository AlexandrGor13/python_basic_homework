import uuid
from typing import Annotated

from annotated_types import MinLen
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    """
    Base book model
    """
    title: Annotated[str, MinLen(1)]
    author: Annotated[str, MinLen(1)]
    genre: Annotated[str, MinLen(1)]
    price: Annotated[float, Field(gt=0)]
    description: Annotated[str, MinLen(1)] | None = None
    quantity: Annotated[int, Field(ge=0)]


class BookCreate(BookBase):
    """
    Create book
    """


class BookRead(BookBase):
    """
    Read book
    """
    id: int


def generate_token() -> str:
    """
    Generate a unique token for book.
    """
    token = str(uuid.uuid4())
    return token


class Book(BookBase):
    """
    Book model
    """
    id: int
    token: str = Field(default_factory=generate_token)
