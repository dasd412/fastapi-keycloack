from sqlmodel import Field

from core.repository.postgres.base_model import BaseModel

class SystemSetting(BaseModel, table=True):
    __tablename__ = "system_setting"

    key: str = Field(nullable=False, unique=True)
    value: str | None = Field(default=None)
