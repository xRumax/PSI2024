from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from ..models import Author
from .schemas import AuthorIn
from fastapi import HTTPException


class AuthorRepository:
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
    ) -> list[Author]:
        with self.session_factory() as session:
            if sort != "id" and sort != "name" and sort:
                raise HTTPException(
                    status_code=400,
                    detail="The sort parameter must be id or name",
                )
            if order != "asc" and order != "desc" and order:
                raise HTTPException(
                    status_code=400,
                    detail="The order parameter must be asc or desc",
                )
            if sort == "id":
                if order == "asc":
                    authors = (
                        session.query(Author)
                        .order_by(Author.id.asc())
                        .limit(limit)
                        .offset(skip)
                        .all()
                    )
                authors = (
                    session.query(Author)
                    .order_by(Author.id.desc())
                    .limit(limit)
                    .offset(skip)
                    .all()
                )
            elif sort == "name":
                if order == "asc":
                    authors = (
                        session.query(Author)
                        .order_by(Author.name.asc())
                        .limit(limit)
                        .offset(skip)
                        .all()
                    )
                authors = (
                    session.query(Author)
                    .order_by(Author.name.desc())
                    .limit(limit)
                    .offset(skip)
                    .all()
                )
            else:
                authors = session.query(Author).limit(limit).offset(skip).all()
            return authors

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
