from pydantic import BaseModel


class TokenIn(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    id: int
    is_admin: bool
