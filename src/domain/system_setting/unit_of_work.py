from sqlmodel import Session

from core.service.unit_of_work import SyncUnitOfWork
from domain.system_setting.repository import SyncSystemSettingRepository


class SyncSystemSettingUnitOfWork(SyncUnitOfWork):

    def __init__(self, session: Session):
        super().__init__(session)
        self.system_setting = SyncSystemSettingRepository(self.session)
