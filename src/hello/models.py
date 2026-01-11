from sqlmodel import SQLModel, Field


class Hello(SQLModel, table=True):
    __tablename__ = "hello"

    key: str = Field(nullable=False, unique=True)
    value: str | None = Field(default=None)
