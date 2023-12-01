from pydantic import BaseModel
from datetime import datetime


class AuthorBase(BaseModel):
    name : str
    birth_date : datetime

class CreateAuthor(AuthorBase):
    name : str
    birth_date : datetime

class Author(AuthorBase):
    id : int

    class Config:
        orm_mode = True