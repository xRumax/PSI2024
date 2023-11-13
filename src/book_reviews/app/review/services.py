from ..models import Review
from .repositories import ReviewRepository
from .schemas import ReviewIn


class ReviewService:
    def __init__(self, review_repository: ReviewRepository) -> None:
        self._repository: ReviewRepository = review_repository

    def get_reviews(self) -> list[Review]:
        return self._repository.get_all()

    def add_review(self, review: ReviewIn) -> None:
        self._repository.add(review)

    def get_review_by_id(self, id: int) -> Review:
        return self._repository.get_by_id(id)

    def delete_review(self, id: int) -> None:
        self._repository.delete(id)

    def update_review(self, id: int, review: ReviewIn) -> None:
        self._repository.update(id, review)
