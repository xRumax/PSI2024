from pydantic import BaseModel
from datetime import datetime
from ..Author.schemas import AuthorBase

class BookBase(BaseModel):
    title : str
    pub : datetime
    author : AuthorBase 

class CreateBook(BookBase):
    title : str
    pub : datetime
    author_id : int 


class Book(BookBase):
    id : int

    class Config:
        orm_mode = True