from ..models import User
from .repositories import UserRepository
from .schemas import UserIn


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    def get_users(self) -> list[User]:
        return self._repository.get_all()

    def add_user(self, user: UserIn) -> None:
        self._repository.add(user)

    def get_user_by_id(self, id: int) -> User:
        return self._repository.get_by_id(id)

    def delete_user(self, id: int) -> None:
        self._repository.delete(id)

    def update_user(self, id: int, user: UserIn) -> None:
        self._repository.update(id, user)
