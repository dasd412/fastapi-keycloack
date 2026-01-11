from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy import func
from sqlmodel import Session, select, SQLModel, col
from sqlalchemy import exists as sql_exists

from core.repository.base_model import BaseModel

T = TypeVar('T', bound=BaseModel)  # BaseModel로 제약 추가


class SyncPostgresRepository(Generic[T]):
    """
    transaction 처리는 unit of work에서 담당합니다.
    커밋과 롤백은 반드시 unit of work를 활용하세요. 리포지토리는 flush()만 할 뿐입니다.
    """

    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def create(self, data: SQLModel | Dict[str, Any]) -> T:
        if isinstance(data, dict):
            instance = self.model(**data)
        else:
            instance = self.model.model_validate(data)

        self.session.add(instance)
        self.session.flush()
        self.session.refresh(instance)
        return instance

    def get_by_id(self, uuid: UUID) -> Optional[T]:
        result = self.session.exec(
            select(self.model).where(col(self.model.id) == uuid)
        )
        return result.one_or_none()

    def get_list(self, offset: int = 0, limit: int = 10,  order_by: Optional[str] = None,**filters) -> List[T]:
        """
        필터링 예시:
        repo.get_list(offset=0, limit=10, name="John",status="active")
        -> WHERE name='John' AND status='active'
        """
        query = select(self.model)

        for key, value in filters.items():
            if hasattr(self.model, key):
                column = getattr(self.model, key)
                # None 값 처리
                if value is None:
                    query = query.where(column.is_(None))
                else:
                    query = query.where(column == value)

        # 정렬 옵션
        if order_by and hasattr(self.model, order_by):
            query = query.order_by(getattr(self.model, order_by))

        query = query.offset(offset).limit(limit)

        result = self.session.exec(query)

        return list(result.all())

    def update(self, uuid: UUID, data: SQLModel | Dict[str, Any]) -> Optional[T]:
        db_item = self.get_by_id(uuid)

        if not db_item:
            return None

        # dict 지원
        update_data = data if isinstance(data, dict) else data.model_dump(exclude_unset=True)
        db_item.sqlmodel_update(update_data)

        self.session.flush()
        self.session.refresh(db_item)
        return db_item

    def delete(self, uuid: UUID) -> bool:
        db_item = self.get_by_id(uuid)
        if db_item:
            self.session.delete(db_item)
            self.session.flush()
            return True
        return False


    def count(self, **filters) -> int:
        query = select(func.count()).select_from(self.model)

        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)

        return self.session.exec(query).one()


    def exists(self, uuid: UUID) -> bool:
        query = select(sql_exists().where(col(self.model.id) == uuid))
        return self.session.exec(query).one()