from pydantic import BaseModel


class Token(BaseModel):
    name: str
    data: str


class Session(BaseModel):
    session: str
    user_id: int
    client: str
