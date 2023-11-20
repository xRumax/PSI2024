from fastapi import APIRouter
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from .services import ReviewService
from .schemas import ReviewIn, ReviewBase
from ..token.auth import oauth2_scheme

router = APIRouter()


def sqlalchemy_object_to_dict(obj):
    """Convert a SQLAlchemy object to a dictionary."""
    if obj is None:
        return None

    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


@router.get("/", tags=["review"])
@inject
def get_list(
    review_service: ReviewService = Depends(Provide[Container.review_service]),
) -> list[ReviewBase]:
    return review_service.get_reviews()


@router.get("/{id}", tags=["review"])
@inject
def get_by_id(
    id: int,
    review_service: ReviewService = Depends(Provide[Container.review_service]),
):
    return review_service.get_review_by_id(id)


@router.post("/", tags=["review"])
@inject
def add_review(
    review: ReviewIn,
    review_service: ReviewService = Depends(Provide[Container.review_service]),
):
    return review_service.add_review(review)


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
