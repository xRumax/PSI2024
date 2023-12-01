from pydantic import BaseModel

class UserBase(BaseModel):
    user_name : str
    admin : bool

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id : int

    class Config:
        orm_mode = True
