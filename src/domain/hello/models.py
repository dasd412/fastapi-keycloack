from sqlmodel import Field

from core.repository.base_model import BaseModel


class Hello(BaseModel, table=True):
    __tablename__ = "hello"

    key: str = Field(nullable=False, unique=True)
    value: str | None = Field(default=None)
