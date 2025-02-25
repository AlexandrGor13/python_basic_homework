from pydantic import BaseModel
import json

from . import schemas


class BookCRUD(BaseModel):
    count: int = 0
    book_by_id: dict[int, schemas.Book] = {}
    book_by_token: dict[str, schemas.Book] = {}

    @property
    def next_id(self) -> int:
        self.count += 1
        return self.count

    def get(self) -> list[schemas.Book]:
        self.read()
        return list(self.book_by_id.values())

    def get_by_id(self, book_id: int) -> schemas.Book | None:
        self.read()
        return self.book_by_id.get(book_id)

    def get_by_token(self, token: str) -> schemas.Book | None:
        self.read()
        return self.book_by_token.get(token)

    def create(self, book_in: schemas.BookCreate) -> schemas.Book:
        self.read()
        book = schemas.Book(
            id=self.next_id,
            **book_in.model_dump()
        )
        self.book_by_id[book.id] = book
        self.book_by_token[book.token] = book
        self.write()
        return book

    def write(self) -> None:
        with open('books.json', 'w', encoding='utf-8') as f:
            json.dump({k: {**v.model_dump()} for k, v in self.book_by_id.items()}, f, ensure_ascii=False, indent=4)

    def read(self) -> None:
        try:
            with open('books.json', 'r', encoding='utf-8') as f:
                dct_book = json.load(f)
                self.book_by_id = {v['id']: schemas.Book(**v) for v in dct_book.values()}
                self.book_by_token = {v['token']: schemas.Book(**v) for v in dct_book.values()}
                self.count = max([book['id'] for book in dct_book.values()])
        except:
            pass


books = BookCRUD()
