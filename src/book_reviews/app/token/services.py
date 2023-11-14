from ..models import User
from .repositories import TokenRepository
from .schemas import TokenIn
from fastapi import Depends, HTTPException, status
from .repositories import oauth2_scheme


class TokenService:
    def __init__(self, token_repository: TokenRepository) -> None:
        self._repository: TokenRepository = token_repository

    def login(self, user: TokenIn) -> User:
        return self._repository.login(user)

    def refresh_token(self, token: str) -> User:
        return self._repository.refresh_token(token)

    def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        return self._repository.get_current_user(token)

    def get_current_active_user(self, current_user: User = Depends(get_current_user)):
        return current_user
