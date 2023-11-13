from pydantic import BaseModel


class ReviewIn(BaseModel):
    desc: str
    rating: int
    user: int
    book: int

    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    id: int
    desc: str
    rating: int
    user: int
    book: int

    class Config:
        from_attributes = True
