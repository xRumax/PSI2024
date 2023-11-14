from fastapi import APIRouter
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from .services import UserService
from .schemas import UserIn, UserBase
from typing import Annotated

router = APIRouter()


@router.get("/", tags=["user"])
@inject
def get_list(
    user_service: UserService = Depends(Provide[Container.user_service]),
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
):
    return user_service.update_user(id, user)
