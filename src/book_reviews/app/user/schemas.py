from pydantic import BaseModel


class UserIn(BaseModel):
    usernmae: str
    password: str
    email: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    id: int
    username: str
    password: str
    email: str
    is_admin: bool

    class Config:
        from_attributes = True
