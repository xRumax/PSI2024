from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from ..models import Book, Author
from .schemas import BookIn, BookBase
from ..author.schemas import AuthorBase
from ..utils import object_as_dict
from fastapi import HTTPException


class BookRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_all(
        self,
        sort: str = None,
        order: str = "asc",
        limit: int = 10,
        skip: int = 0,
    ) -> list[Book]:
        with self.session_factory() as session:
            if sort != "id" and sort != "title" and sort:
                raise HTTPException(
                    status_code=400,
                    detail="The sort parameter must be id or title",
                )
            if order != "asc" and order != "desc" and order:
                raise HTTPException(
                    status_code=400,
                    detail="The order parameter must be asc or desc",
                )
            if sort == "id":
                if order == "asc":
                    books = (
                        session.query(Book)
                        .order_by(Book.id.asc())
                        .limit(limit)
                        .offset(skip)
                        .all()
                    )
                books = (
                    session.query(Book)
                    .order_by(Book.id.desc())
                    .limit(limit)
                    .offset(skip)
                    .all()
                )
            elif sort == "title":
                if order == "asc":
                    books = (
                        session.query(Book)
                        .order_by(Book.title.asc())
                        .limit(limit)
                        .offset(skip)
                        .all()
                    )
                books = (
                    session.query(Book)
                    .order_by(Book.title.desc())
                    .limit(limit)
                    .offset(skip)
                    .all()
                )
            else:
                books = session.query(Book).limit(limit).offset(skip).all()
            books = [object_as_dict(book) for book in books]
            books_with_author = []
            for book in books:
                author = session.query(Author).filter_by(id=book["author_id"]).first()
                book["author"] = AuthorBase(**object_as_dict(author))
                book = BookBase(**book)
                books_with_author.append(book)
            return books_with_author

    def get_by_id(self, id: int) -> Book:
        with self.session_factory() as session:
            return session.query(Book).filter_by(id=id).first()

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
