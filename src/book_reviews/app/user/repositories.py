from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from ..models import User
from .schemas import UserIn


class UserRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_all(self) -> list[User]:
        with self.session_factory() as session:
            return session.query(User).all()

    def get_by_id(self, id: int) -> User:
        with self.session_factory() as session:
            return session.query(User).filter(User.id == id).first()

    def add(self, user: UserIn) -> None:
        with self.session_factory() as session:
            session.add(User(**user.model_dump()))
            session.commit()

    def delete(self, id: int) -> None:
        with self.session_factory() as session:
            session.query(User).filter(User.id == id).delete()
            session.commit()

    def update(self, id: int, user: UserIn) -> None:
        with self.session_factory() as session:
            session.query(User).filter(User.id == id).update(
                user.model_dump(exclude_unset=True)
            )
            session.commit()
