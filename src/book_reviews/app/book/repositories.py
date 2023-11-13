from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from ..models import Book
from .schemas import BookIn
from sqlalchemy import inspect


class BookRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_all(self) -> list[Book]:
        with self.session_factory() as session:
            return session.query(Book).all()

    def get_by_id(self, id: int) -> Book:
        with self.session_factory() as session:
            book = session.query(Book).filter_by(id=id).first()
            author_name = (
                inspect(book).attrs.author.loaded_value.name if book.author else None
            )
            return book

    def add(self, book: BookIn) -> None:
        with self.session_factory() as session:
            session.add(Book(**book.model_dump()))
            session.commit()

    def delete(self, id: int) -> None:
        with self.session_factory() as session:
            session.query(Book).filter(Book.id == id).delete()
            session.commit()

    def update(self, id: int, book: BookIn) -> None:
        with self.session_factory() as session:
            session.query(Book).filter(Book.id == id).update(
                book.model_dump(exclude_unset=True)
            )
            session.commit()
