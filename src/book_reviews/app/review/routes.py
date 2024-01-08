from fastapi import APIRouter
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from .services import ReviewService
from .schemas import ReviewIn, ReviewBase
from ..token.auth import oauth2_scheme, decode_token

router = APIRouter()


@router.get("/", tags=["review"])
@inject
def get_list(
    sort: str = None,
    order: str = "asc",
    limit: int = 10,
    skip: int = 0,
    review_service: ReviewService = Depends(Provide[Container.review_service]),
) -> list[ReviewBase]:
    return review_service.get_reviews(sort, order, limit, skip)


@router.get("/{id}", tags=["review"])
@inject
def get_by_id(
    id: int,
    review_service: ReviewService = Depends(Provide[Container.review_service]),
):
    return review_service.get_review_by_id(id)


@router.post(
    "/",
    tags=["review"],
    status_code=201,
)
@inject
def add_review(
    review: ReviewIn,
    token: dict = Depends(oauth2_scheme),
    review_service: ReviewService = Depends(Provide[Container.review_service]),
):
    return review_service.add_review(review, int(decode_token(token)["id"]))


@router.delete("/{id}", tags=["review"])
@inject
def delete_review(
    id: int,
    review_service: ReviewService = Depends(Provide[Container.review_service]),
    token: dict = Depends(oauth2_scheme),
):
    return review_service.delete_review(id, token)


@router.put("/{id}", tags=["review"])
@inject
def update_review(
    id: int,
    review: ReviewIn,
    review_service: ReviewService = Depends(Provide[Container.review_service]),
    token: dict = Depends(oauth2_scheme),
):
    return review_service.update_review(id, review, token)
