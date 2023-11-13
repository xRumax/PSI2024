from fastapi import APIRouter
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from .services import AuthorService
from .schemas import AuthorIn, AuthorBase

router = APIRouter()


@router.get("/", tags=["author"])
@inject
def get_list(
    author_service: AuthorService = Depends(Provide[Container.author_service]),
) -> list[AuthorBase]:
    return author_service.get_authors()


@router.get("/{id}", tags=["author"])
@inject
def get_by_id(
    id: int,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
):
    return author_service.get_author_by_id(id)


@router.post("/", tags=["author"])
@inject
def add_author(
    author: AuthorIn,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
):
    return author_service.add_author(author)


@router.delete("/{id}", tags=["author"])
@inject
def delete_author(
    id: int,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
):
    return author_service.delete_author(id)


@router.put("/{id}", tags=["author"])
@inject
def update_author(
    id: int,
    author: AuthorIn,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
):
    return author_service.update_author(id, author)
