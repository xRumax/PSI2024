from pydantic import BaseModel
from datetime import datetime


class AuthorIn(BaseModel):
    name: str
    birth_date: datetime


class AuthorBase(BaseModel):
    id: int
    name: str
    birth_date: datetime

    class Config:
        from_attributes = True
        exclude = {"books"}
