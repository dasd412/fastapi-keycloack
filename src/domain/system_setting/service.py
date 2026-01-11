from uuid import UUID

from domain.system_setting.models import SystemSetting
from domain.system_setting.schemas import SystemSettingCreate, SystemSettingUpdate
from domain.system_setting.unit_of_work import SystemSettingUnitOfWork


class SystemSettingService:
    def __init__(self, uow: SystemSettingUnitOfWork):
        self.uow = uow

    def create(self, data: SystemSettingCreate) -> SystemSetting:
        with self.uow:
            result = self.uow.system_setting.create(data.model_dump())
        return result

    def get_by_id(self, uuid: UUID) -> SystemSetting | None:
        return self.uow.system_setting.get_by_id(uuid)

    def get_list(self, offset: int = 0, limit: int = 10) -> list[SystemSetting]:
        return self.uow.system_setting.get_list(offset=offset, limit=limit)

    def get_by_key(self, key: str) -> SystemSetting | None:
        return self.uow.system_setting.get_by_key(key)

    def update(self, uuid: UUID, data: SystemSettingUpdate) -> SystemSetting | None:
        with self.uow:
            result = self.uow.system_setting.update(uuid, data.model_dump(exclude_unset=True))
        return result

    def delete(self, uuid: UUID) -> bool:
        with self.uow:
            result = self.uow.system_setting.delete(uuid)
        return result
