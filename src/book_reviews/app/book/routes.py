from fastapi import APIRouter
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from .services import BookService
from .schemas import BookIn, BookBase
from ..token.auth import oauth2_scheme
from fastapi import HTTPException

router = APIRouter()


@router.get("/", tags=["book"])
@inject
def get_list(
    sort: str = None,
    order: str = "asc",
    limit: int = 10,
    skip: int = 0,
    book_service: BookService = Depends(Provide[Container.book_service]),
) -> list[BookBase]:
    return book_service.get_books(sort, order, limit, skip)


@router.get("/{id}", tags=["book"])
@inject
def get_by_id(
    id: int,
    book_service: BookService = Depends(Provide[Container.book_service]),
) -> BookBase:
    return book_service.get_book_by_id(id)


@router.post("/", tags=["book"])
@inject
def add_book(
    book: BookIn,
    token: dict = Depends(oauth2_scheme),
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    return book_service.add_book(book)


@router.delete("/{id}", tags=["book"])
@inject
def delete_book(
    id: int,
    book_service: BookService = Depends(Provide[Container.book_service]),
    token: dict = Depends(oauth2_scheme),
):
    if token["is_admin"] == False:
        raise HTTPException(
            status_code=400,
            detail="Not Authorized",
        )
    return book_service.delete_book(id)


@router.put("/{id}", tags=["book"])
@inject
def update_book(
    id: int,
    book: BookIn,
    book_service: BookService = Depends(Provide[Container.book_service]),
    token: dict = Depends(oauth2_scheme),
):
    if token["is_admin"] == False:
        raise HTTPException(
            status_code=400,
            detail="Not Authorized",
        )
    return book_service.update_book(id, book)
