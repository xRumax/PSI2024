from ..models import Book
from .repositories import BookRepository
from .schemas import BookIn


class BookService:
    def __init__(self, book_repository: BookRepository) -> None:
        self._repository: BookRepository = book_repository

    def get_books(
        self,
        sort: str = None,
        order: str = "asc",
        limit: int = 10,
        skip: int = 0,
    ) -> list[Book]:
        return self._repository.get_all(sort, order, limit, skip)

    def add_book(self, book: BookIn) -> None:
        self._repository.add(book)

    def get_book_by_id(self, id: int) -> Book:
        return self._repository.get_by_id(id)

    def delete_book(self, id: int) -> None:
        self._repository.delete(id)

    def update_book(self, id: int, book: BookIn) -> None:
        self._repository.update(id, book)
