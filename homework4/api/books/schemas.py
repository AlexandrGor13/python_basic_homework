import uuid
from typing import Annotated

from annotated_types import MinLen
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: Annotated[str, MinLen(1)]
    author: Annotated[str, MinLen(1)]
    genre: Annotated[str, MinLen(1)]
    price: Annotated[float, Field(gt=0)]
    description: Annotated[str, MinLen(1)] | None = None
    average_rating: Annotated[float, Field(default=0)]
    quantity: Annotated[int, Field(gt=0)]


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
    token = str(uuid.uuid4())
    return token


class Book(BookBase):
    id: int
    token: str = Field(default_factory=generate_token)
