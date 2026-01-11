from uuid import UUID

from fastapi import APIRouter, status

from domain.system_setting.schemas import SystemSettingCreate, SystemSettingRead

system_setting_router = APIRouter(prefix="/system_setting")


@system_setting_router.post(
    path="",
    response_model=SystemSettingRead,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
def create(item: SystemSettingCreate):
    pass


@system_setting_router.get(
    path="/{id}",
    response_model=SystemSettingRead,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
def get(uuid: UUID):
    pass


@system_setting_router.get(
    path="",
    response_model=list[SystemSettingRead],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
def get_list():
    pass


@system_setting_router.get(
    path="/{key}",
    response_model=SystemSettingRead,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
def get_by_key(key: str):
    pass


@system_setting_router.patch(
    path="/{id_}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update():
    pass


@system_setting_router.delete(
    path="/{id_}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(uuid: UUID):
    pass
