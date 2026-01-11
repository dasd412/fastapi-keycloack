from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from core.repository.postgres.session import PGSession
from domain.system_setting.repository import SystemSettingRepository
from domain.system_setting.service import SystemSettingService
from domain.system_setting.unit_of_work import SystemSettingUnitOfWork


def get_system_setting_uow(
    session: Annotated[Session, Depends(PGSession())]
) -> SystemSettingUnitOfWork:
    print(f"DEBUG: Creating SystemSettingUnitOfWork with session: {session}")
    # 같은 session으로 repository 생성
    repository = SystemSettingRepository(session)
    print(f"DEBUG: Creating SystemSettingRepository with same session")
    return SystemSettingUnitOfWork(session, repository)


def get_system_setting_service(uow: Annotated[SystemSettingUnitOfWork, Depends(get_system_setting_uow)]) -> SystemSettingService:
    print("DEBUG: Creating SystemSettingService")
    return SystemSettingService(uow)
