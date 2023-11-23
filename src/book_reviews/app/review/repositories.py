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

    def get_reviews(self, reviews) -> list[Review]:
        with self.session_factory() as session:
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

    def get_all(self, sort: str, order: str, limit: int, skip: int):
        with self.session_factory() as session:
            if sort != "id" and sort != "rating" and sort:
                raise HTTPException(
                    status_code=400,
                    detail="The sort parameter must be id, user_id or book_id",
                )
            if order != "asc" and order != "desc" and order:
                raise HTTPException(
                    status_code=400,
                    detail="The order parameter must be asc or desc",
                )
            if sort == "id" and order == "asc":
                if order == "asc":
                    reviews = (
                        session.query(Review)
                        .order_by(Review.id.asc())
                        .limit(limit)
                        .offset(skip)
                        .all()
                    )
                reviews = (
                    session.query(Review)
                    .order_by(Review.id.desc())
                    .limit(limit)
                    .offset(skip)
                    .all()
                )
            if sort == "rating":
                if order == "asc":
                    reviews = (
                        session.query(Review)
                        .order_by(Review.rating.asc())
                        .limit(limit)
                        .offset(skip)
                        .all()
                    )
                reviews = (
                    session.query(Review)
                    .order_by(Review.rating.desc())
                    .limit(limit)
                    .offset(skip)
                    .all()
                )
            if not sort:
                reviews = session.query(Review).limit(limit).offset(skip).all()
            reviews = [object_as_dict(review) for review in reviews]
            return self.get_reviews(reviews)

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
