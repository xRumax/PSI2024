from pydantic import BaseModel
from ..User.schemas import UserBase 
from ..Book.schemas import BookBase 

class ReviewBase(BaseModel):
    description : str
    rating : bool
    book : BookBase
    creator : UserBase


class ReviewCreate(ReviewBase):
    description : str
    rating : float
    book_id : int


class Review(ReviewBase):
    id : int

    class Config:
        orm_mode = True
