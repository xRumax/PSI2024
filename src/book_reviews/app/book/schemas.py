from pydantic import BaseModel
from datetime import datetime
from ..author.schemas import AuthorBase


class BookIn(BaseModel):
    title: str
    pub: datetime
    author_id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    id: int
    title: str
    pub: datetime
    author: AuthorBase

    class Config:
        from_attributes = True
