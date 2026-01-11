from uuid import UUID

from fastapi import APIRouter, status, Depends

from domain.system_setting.dependencies import get_system_setting_service
from domain.system_setting.schemas import SystemSettingCreate, SystemSettingRead, SystemSettingUpdate
from domain.system_setting.service import SystemSettingService

system_setting_router = APIRouter(prefix="/system_setting")


@system_setting_router.post(
    path="",
    response_model=SystemSettingRead,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
def create(item: SystemSettingCreate, service: SystemSettingService = Depends(get_system_setting_service)):
    pass


@system_setting_router.get(
    path="/{id}",
    response_model=SystemSettingRead,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
def get(uuid: UUID,  service: SystemSettingService = Depends(get_system_setting_service)):
    pass


@system_setting_router.get(
    path="",
    response_model=list[SystemSettingRead],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
def get_list(service: SystemSettingService = Depends(get_system_setting_service)):
    pass


@system_setting_router.get(
    path="/{key}",
    response_model=SystemSettingRead,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
def get_by_key(key: str, service: SystemSettingService = Depends(get_system_setting_service)):
    pass


@system_setting_router.patch(
    path="/{id_}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update(uuid: UUID, target: SystemSettingUpdate, service: SystemSettingService = Depends(get_system_setting_service)):
    pass


@system_setting_router.delete(
    path="/{id_}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(uuid: UUID, service: SystemSettingService = Depends(get_system_setting_service)):
    pass
