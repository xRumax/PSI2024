from pydantic import BaseModel
from datetime import datetime


class BookIn(BaseModel):
    title: str
    pub: datetime
    author: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    id: int
    title: str
    pub: datetime
    author: int

    class Config:
        orm_mode = True
