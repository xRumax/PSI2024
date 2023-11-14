from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from ..models import Review, User, Book
from .schemas import ReviewIn, ReviewBase
from ..user.schemas import UserBase
from ..book.schemas import BookOut
from ..utils import object_as_dict


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

    def delete(self, id: int) -> None:
        with self.session_factory() as session:
            session.query(Review).filter(Review.id == id).delete()
            session.commit()

    def update(self, id: int, review: ReviewIn) -> None:
        with self.session_factory() as session:
            session.query(Review).filter(Review.id == id).update(
                review.model_dump(exclude_unset=True)
            )
            session.commit()
