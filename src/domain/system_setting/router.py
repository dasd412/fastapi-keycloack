from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from domain.system_setting.dependencies import get_system_setting_service
from domain.system_setting.schemas import (
    SystemSettingCreate,
    SystemSettingRead,
    SystemSettingUpdate,
)
from domain.system_setting.service import SystemSettingService

system_setting_router = APIRouter(prefix="/system_setting")


@system_setting_router.post(
    path="",
    response_model=SystemSettingRead,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
def create(item: SystemSettingCreate, service: SystemSettingService = Depends(get_system_setting_service)):
    result = service.create(item)
    return result


@system_setting_router.get(
    path="/{uuid}",
    response_model=SystemSettingRead,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
def get_by_id(uuid: UUID, service: SystemSettingService = Depends(get_system_setting_service)):
    result = service.get_by_id(uuid)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SystemSetting not found")
    return result


@system_setting_router.get(
    path="",
    response_model=list[SystemSettingRead],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
def get_list(service: SystemSettingService = Depends(get_system_setting_service), offset: int = 0, limit: int = 10):
    return service.get_list(offset=offset, limit=limit)


@system_setting_router.get(
    path="/by-key/{key}",
    response_model=SystemSettingRead,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
def get_by_key(key: str, service: SystemSettingService = Depends(get_system_setting_service)):
    result = service.get_by_key(key)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SystemSetting not found")
    return result


@system_setting_router.patch(
    path="/{uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update(uuid: UUID, target: SystemSettingUpdate, service: SystemSettingService = Depends(get_system_setting_service)):
    result = service.update(uuid, target)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SystemSetting not found")


@system_setting_router.delete(
    path="/{uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(uuid: UUID, service: SystemSettingService = Depends(get_system_setting_service)):
    result = service.delete(uuid)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SystemSetting not found")
