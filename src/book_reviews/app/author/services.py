from ..models import Author
from .repositories import AuthorRepository
from .schemas import AuthorIn


class AuthorService:
    def __init__(self, author_repository: AuthorRepository) -> None:
        self._repository: AuthorRepository = author_repository

    def get_authors(self) -> list[Author]:
        return self._repository.get_all()

    def add_author(self, author: AuthorIn) -> None:
        self._repository.add(author)

    def get_author_by_id(self, id: int) -> Author:
        return self._repository.get_by_id(id)

    def delete_author(self, id: int) -> None:
        self._repository.delete(id)

    def update_author(self, id: int, author: AuthorIn) -> None:
        self._repository.update(id, author)
