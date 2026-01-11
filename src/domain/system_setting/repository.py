from sqlmodel import Session, select

from core.repository.postgres.repository import PostgresRepository
from domain.system_setting.models import SystemSetting


class SystemSettingRepository(PostgresRepository[SystemSetting]):
    def __init__(self, session: Session):
        super().__init__(session, SystemSetting)

    def find_by_key(self, key: str) -> SystemSetting | None:
        """
        커스텀 쿼리 예시 - key로 찾기
        base repository에서 제공 안하는 건 따로 만들 수 있음.
        """
        result = self.session.exec(select(SystemSetting).where(SystemSetting.key == key))
        return result.one_or_none()
