from fastapi import APIRouter
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from .services import BookService
from .schemas import BookIn, BookBase

router = APIRouter()


@router.get("/", tags=["book"])
@inject
def get_list(
    book_service: BookService = Depends(Provide[Container.book_service]),
) -> list[BookBase]:
    return book_service.get_books()


@router.get("/{id}", tags=["book"])
@inject
def get_by_id(
    id: int,
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    return book_service.get_book_by_id(id)


@router.post("/", tags=["book"])
@inject
def add_book(
    book: BookIn,
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    return book_service.add_book(book)


@router.delete("/{id}", tags=["book"])
@inject
def delete_book(
    id: int,
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    return book_service.delete_book(id)


@router.put("/{id}", tags=["book"])
@inject
def update_book(
    id: int,
    book: BookIn,
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    return book_service.update_book(id, book)
