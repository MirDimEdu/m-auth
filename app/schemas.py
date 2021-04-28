from pydantic import BaseModel


class Token(BaseModel):
    name: str
    data: str


class CurrentUser(BaseModel):
    user_id: int
    login: str
    role: str
