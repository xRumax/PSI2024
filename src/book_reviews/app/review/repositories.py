from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from ..models import Review
from .schemas import ReviewIn


class ReviewRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_all(self) -> list[Review]:
        with self.session_factory() as session:
            return session.query(Review).all()

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
