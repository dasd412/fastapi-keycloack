from domain.system_setting.models import SystemSetting
from domain.system_setting.schemas import SystemSettingCreate
from domain.system_setting.unit_of_work import SystemSettingUnitOfWork


class SystemSettingService:
    def __init__(self, uow: SystemSettingUnitOfWork):
        self.uow = uow

    def create(self, data: SystemSettingCreate) -> SystemSetting:
        with self.uow:
            result = self.uow.system_setting.create(data.model_dump())
        return result

