from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    id: int
    username: str
    password: str

    is_admin: bool

    class Config:
        from_attributes = True
