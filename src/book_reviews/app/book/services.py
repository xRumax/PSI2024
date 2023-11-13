from ..models import Book
from .repositories import BookRepository
from .schemas import BookIn


class BookService:
    def __init__(self, book_repository: BookRepository) -> None:
        self._repository: BookRepository = book_repository

    def get_books(self) -> list[Book]:
        return self._repository.get_all()

    def add_book(self, book: BookIn) -> None:
        self._repository.add(book)

    def get_book_by_id(self, id: int) -> Book:
        return self._repository.get_by_id(id)

    def delete_book(self, id: int) -> None:
        self._repository.delete(id)
