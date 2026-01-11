from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from core.repository.postgres.session import PGSession
from domain.system_setting.repository import SystemSettingRepository
from domain.system_setting.service import SystemSettingService


def get_system_setting_repository(session: Annotated[Session, Depends(PGSession())]) -> SystemSettingRepository:
    return SystemSettingRepository(session)


def get_system_setting_service(repository: Annotated[SystemSettingRepository, Depends(get_system_setting_repository)])-> SystemSettingService:
    return SystemSettingService(repository)
