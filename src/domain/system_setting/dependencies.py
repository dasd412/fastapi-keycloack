from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from core.repository.postgres.session import PGSession
from domain.system_setting.service import SystemSettingService
from domain.system_setting.unit_of_work import SystemSettingUnitOfWork


def get_system_setting_uow(session: Annotated[Session, Depends(PGSession())]) -> SystemSettingUnitOfWork:
    return SystemSettingUnitOfWork(session)


def get_system_setting_service(uow: Annotated[SystemSettingUnitOfWork, Depends(get_system_setting_uow)]) -> SystemSettingService:
    return SystemSettingService(uow)
