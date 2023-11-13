from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from ..models import Author
from .schemas import AuthorIn


class AuthorRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_all(self) -> list[Author]:
        with self.session_factory() as session:
            return session.query(Author).all()

    def get_by_id(self, id: int) -> Author:
        with self.session_factory() as session:
            return session.query(Author).filter(Author.id == id).first()

    def add(self, author: AuthorIn) -> None:
        with self.session_factory() as session:
            session.add(Author(**author.dict()))
            session.commit()

    def delete(self, id: int) -> None:
        with self.session_factory() as session:
            session.query(Author).filter(Author.id == id).delete()
            session.commit()

    def update(self, id: int, author: AuthorIn) -> None:
        with self.session_factory() as session:
            session.query(Author).filter(Author.id == id).update(
                author.model_dump(exclude_unset=True)
            )
            session.commit()
