from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict
from sqlalchemy import func
from sqlmodel import Field, SQLModel, text

class BaseModel(SQLModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: UUID = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )

    created_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={"server_default": text("(NOW() AT TIME ZONE 'UTC')")},
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("(NOW() AT TIME ZONE 'UTC')"),
            "onupdate": func.now(),
        },
    )