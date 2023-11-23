from ..models import Review
from .repositories import ReviewRepository
from .schemas import ReviewIn


class ReviewService:
    def __init__(self, review_repository: ReviewRepository) -> None:
        self._repository: ReviewRepository = review_repository

    def get_reviews(self, sort: str, order: str, limit: int, skip: int) -> list[Review]:
        return self._repository.get_all()

    def add_review(self, review: ReviewIn) -> None:
        self._repository.add(review)

    def get_review_by_id(self, id: int) -> Review:
        return self._repository.get_by_id(id)

    def delete_review(self, id: int, token: dict) -> None:
        self._repository.delete(id, token)

    def update_review(self, id: int, review: ReviewIn, token: dict) -> None:
        self._repository.update(id, review, token)
