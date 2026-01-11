from sqlmodel import Session, select

from core.repository.sync_postgres_repository import SyncPostgresRepository
from domain.hello.models import Hello


class SyncHelloRepository(SyncPostgresRepository[Hello]):

    def __init__(self, session: Session):
        super().__init__(session, Hello)

    def find_by_key(self, key: str) -> Hello | None:
        """
        커스텀 쿼리 예시 - key로 찾기
        base repository에서 제공 안하는 건 따로 만들 수 있음.
        """
        result = self.session.exec(
            select(Hello).where(Hello.key == key)
        )
        return result.one_or_none()
