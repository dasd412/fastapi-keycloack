from sqlmodel import Session

from core.service.unit_of_work import SyncUnitOfWork
from domain.hello.repository import SyncHelloRepository


class SyncHelloUnitOfWork(SyncUnitOfWork):
    """Hello 도메인 UnitOfWork"""

    def __init__(self, session: Session):
        super().__init__(session)
        self.hello = SyncHelloRepository(self.session)
