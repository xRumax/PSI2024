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
