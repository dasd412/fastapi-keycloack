from pydantic import BaseModel

class HelloRead(BaseModel):
    key: str
    value: str | None = None


class HelloCreate(BaseModel):
    key: str
    value: str | None = None


class HelloUpdate(BaseModel):
    value: str | None = None
