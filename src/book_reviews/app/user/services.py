from ..models import User
from .repositories import UserRepository
from .schemas import UserIn


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    def get_users(self, sort, order, limit, skip) -> list[User]:
        return self._repository.get_all(sort, order, limit, skip)

    def add_user(self, user: UserIn) -> None:
        self._repository.add(user)

    def get_user_by_id(self, id: int) -> User:
        return self._repository.get_by_id(id)

    def delete_user(self, id: int) -> None:
        self._repository.delete(id)

    def update_user(self, id: int, user: UserIn, token: dict) -> None:
        self._repository.update(id, user, token)

    def login(self, user: UserIn, token: dict) -> dict:
        return self._repository.login(user, token)
