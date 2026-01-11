from pydantic import BaseModel

class SystemSettingRead(BaseModel):
    key: str
    value: str | None = None


class SystemSettingCreate(BaseModel):
    key: str
    value: str | None = None


class SystemSettingUpdate(BaseModel):
    value: str | None = None
