from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from ..models import Review, User, Book
from .schemas import ReviewIn, ReviewBase
from ..user.schemas import UserBase
from ..book.schemas import BookOut
from ..utils import object_as_dict
from fastapi import HTTPException


class ReviewRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_all(self):
        with self.session_factory() as session:
            reviews = session.query(Review).all()
            reviews = [object_as_dict(review) for review in reviews]
            full_reviews = []
            for review in reviews:
                review["user"] = UserBase(
                    **object_as_dict(
                        session.query(User).filter_by(id=review["user_id"]).first()
                    )
                )

                review["book"] = BookOut(
                    **object_as_dict(
                        session.query(Book).filter_by(id=review["book_id"]).first()
                    )
                )
                review = ReviewBase(**review)
                full_reviews.append(review)
            return full_reviews

    def get_by_id(self, id: int) -> Review:
        with self.session_factory() as session:
            return session.query(Review).filter(Review.id == id).first()

    def add(self, review: ReviewIn) -> None:
        with self.session_factory() as session:
            session.add(Review(**review.model_dump()))
            session.commit()

    def delete(self, id: int, token: dict) -> None:
        with self.session_factory() as session:
            review = session.query(Review).filter(Review.id == id).first()
            if review.first.user_id == token["id"] or token["is_admin"]:
                review.delete()
                session.commit()
            raise HTTPException(
                status_code=401,
                detail="You are not authorized to delete this review",
            )

    def update(self, id: int, review: ReviewIn, token: dict) -> None:
        with self.session_factory() as session:
            review_ = session.query(Review).filter(Review.id == id)
            if review_.first.user_id == token["id"] or token["is_admin"]:
                review_.update(review.model_dump())
                session.commit()
            session.commit()
