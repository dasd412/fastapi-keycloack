from domain.system_setting.repository import SystemSettingRepository


class SystemSettingService:
    def __init__(self, repository:SystemSettingRepository):
        self.repository = repository
