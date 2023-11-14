from pydantic import BaseModel
from ..book.schemas import BookOut
from ..user.schemas import UserBase


class ReviewIn(BaseModel):
    desc: str
    rating: int
    user_id: int
    book_id: int

    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    id: int
    desc: str
    rating: int
    user: UserBase
    book: BookOut

    class Config:
        from_attributes = True
