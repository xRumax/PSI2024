from fastapi import APIRouter
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from .services import UserService
from .schemas import UserIn, UserBase
from ..token.auth import oauth2_scheme, decode_token

router = APIRouter()


@router.get("/", tags=["user"])
@inject
def get_list(
    user_service: UserService = Depends(Provide[Container.user_service]),
    token: dict = Depends(oauth2_scheme),
) -> list[UserBase]:
    return user_service.get_users()


@router.get("/{id}", tags=["user"])
@inject
def get_by_id(
    id: int,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.get_user_by_id(id)


@router.post("/", tags=["user"])
@inject
def add_user(
    user: UserIn,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.add_user(user)


@router.delete("/{id}", tags=["user"])
@inject
def delete_user(
    id: int,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.delete_user(id)


@router.put("/{id}", tags=["user"])
@inject
def update_user(
    id: int,
    user: UserIn,
    user_service: UserService = Depends(Provide[Container.user_service]),
    token: dict = Depends(oauth2_scheme),
):
    return user_service.update_user(id, user, token)


@router.post("/login", tags=["user"])
@inject
def login(
    user: UserIn,
    user_service: UserService = Depends(Provide[Container.user_service]),
    token: dict = Depends(oauth2_scheme),
):
    return user_service.login(user, token)


@router.post("/token", tags=["auth"])
def token(token: str):
    return decode_token(token)
