from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from core.repository.postgres.session import PGSession
from domain.system_setting.repository import SystemSettingRepository
from domain.system_setting.service import SystemSettingService
from domain.system_setting.unit_of_work import SystemSettingUnitOfWork


def get_system_setting_repository(session: Annotated[Session, Depends(PGSession())]) -> SystemSettingRepository:
    return SystemSettingRepository(session)


def get_system_setting_uow(
    session: Annotated[Session, Depends(PGSession())],
    system_setting_repo: Annotated[SystemSettingRepository, Depends(get_system_setting_repository)]
) -> SystemSettingUnitOfWork:
    return SystemSettingUnitOfWork(session, system_setting_repo)


def get_system_setting_service(uow: Annotated[SystemSettingUnitOfWork, Depends(get_system_setting_uow)]) -> SystemSettingService:
    return SystemSettingService(uow)
