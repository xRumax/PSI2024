from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from ..models import User
from .schemas import UserIn
from ..utils import hash_password, verify_password
from ..token.auth import create_access_token
from fastapi import HTTPException


class UserRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_all(self, sort: str, order: str, limit: int, skip: int) -> list[User]:
        with self.session_factory() as session:
            if sort != "id" and sort != "username" and sort:
                raise HTTPException(
                    status_code=400,
                    detail="The sort parameter must be id or username",
                )
            if sort == "id":
                if order == "asc":
                    return (
                        session.query(User)
                        .order_by(User.id.asc())
                        .limit(limit)
                        .offset(skip)
                        .all()
                    )
                return (
                    session.query(User)
                    .order_by(User.id.desc())
                    .limit(limit)
                    .offset(skip)
                    .all()
                )
            if sort == "username":
                if order == "asc":
                    return (
                        session.query(User)
                        .order_by(User.username.asc())
                        .limit(limit)
                        .offset(skip)
                        .all()
                    )
                return (
                    session.query(User)
                    .order_by(User.username.desc())
                    .limit(limit)
                    .offset(skip)
                    .all()
                )
            if order != "asc" and order != "desc":
                raise HTTPException(
                    status_code=400,
                    detail="The order parameter must be asc or desc",
                )
            if not sort:
                return session.query(User).limit(limit).offset(skip).all()

            return session.query(User).all()

    def get_by_id(self, id: int) -> User:
        with self.session_factory() as session:
            return session.query(User).filter(User.id == id).first()

    def add(self, user: UserIn) -> None:
        with self.session_factory() as session:
            user = User(**user.model_dump())
            user.password = hash_password(user.password)
            session.add(user)
            session.commit()

    def delete(self, id: int, token: dict) -> None:
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == id)
            if user.id == token["id"] or token["is_admin"]:
                user.delete()
                session.commit()
                return
            raise HTTPException(
                status_code=401,
                detail="You are not authorized to delete this user",
            )

    def update(self, id: int, user: UserIn, token: dict) -> None:
        with self.session_factory() as session:
            user_ = session.query(User).filter(User.id == id).first()
            if user_.id == token["id"] or token["is_admin"]:
                user_ = User(**user.model_dump())
                user_.password = hash_password(user_.password)
                session.merge(user_)
                session.commit()
                return
            raise HTTPException(
                status_code=401,
                detail="You are not authorized to update this user",
            )

    def login(self, user: UserIn) -> [str, str]:
        with self.session_factory() as session:
            user_ = session.query(User).filter_by(username=user.username).first()
            if user_:
                if verify_password(user.password, user_.password):
                    return create_access_token(
                        {"id": user_.id, "is_admin": user_.is_admin}
                    )
