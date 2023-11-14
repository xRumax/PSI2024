from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from ..models import User
from .schemas import TokenIn, TokenData
from ..utils import verify_password
from datetime import datetime, timedelta
from jose import jwt
from ..settings import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)
from fastapi import Depends, HTTPException, status
from typing import Annotated
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def login(self, token: TokenIn):
        with self.session_factory() as session:
            user = session.query(User).filter_by(username=token.username).first()
            if not user:
                return None
            if not verify_password(token.password, user.password):
                return None
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = self.create_access_token(
                data={"id": user.id, "is_admin": user.is_admin},
                expires_delta=access_token_expires,
            )
            return access_token

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            id: int = payload.get("id")
            if id is None:
                raise credentials_exception
            token_data = TokenData(id=id, is_admin=payload.get("is_admin"))
        except JWTError:
            raise credentials_exception
        with self.session_factory() as session:
            user = session.query(User).filter_by(id=token_data.id).first()
            if user is None:
                raise credentials_exception
            return user

    async def get_current_active_user(
        self, current_user: Annotated[User, Depends(get_current_user)]
    ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    def refresh_token(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            id: int = payload.get("id")
            if id is None:
                raise credentials_exception
            token_data = TokenData(id=id, is_admin=payload.get("is_admin"))
        except JWTError:
            raise credentials_exception
        with self.session_factory() as session:
            user = session.query(User).filter_by(username=token_data.username).first()
            if user is None:
                raise credentials_exception
            access_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
            access_token = self.create_access_token(
                data={"id": user.id, "is_admin": user.is_admin},
                expires_delta=access_token_expires,
            )
            return access_token
