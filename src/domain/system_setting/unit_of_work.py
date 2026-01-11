from sqlmodel import Session

from core.service.unit_of_work import UnitOfWork
from domain.system_setting.repository import SystemSettingRepository


class SystemSettingUnitOfWork(UnitOfWork):

    def __init__(self, session: Session):
        super().__init__(session)
        self.system_setting = SystemSettingRepository(self.session)
