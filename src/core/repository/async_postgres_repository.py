from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists as sql_exists
from sqlmodel import select, SQLModel, col

from core.repository.base_model import BaseModel

T = TypeVar("T", bound=BaseModel)


class AsyncPostgresRepository(Generic[T]):
    """
    transaction 처리는 unit of work에서 담당합니다.
    커밋과 롤백은 반드시 unit of work를 활용하세요.
    리포지토리는 flush()만 할 뿐입니다.
    """

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def create(self, data: SQLModel | Dict[str, Any]) -> T:
        if isinstance(data, dict):
            instance = self.model(**data)
        else:
            instance = self.model.model_validate(data)

        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def get_by_id(self, uuid: UUID) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).where(col(self.model.id) == uuid)
        )
        return result.one_or_none()

    async def get_list(
        self,
        offset: int = 0,
        limit: int = 10,
        order_by: Optional[str] = None,
        **filters,
    ) -> List[T]:
        """
        필터링 예시:
        await repo.get_list(offset=0, limit=10, name="John", status="active")
        -> WHERE name='John' AND status='active'
        """
        query = select(self.model)

        for key, value in filters.items():
            if hasattr(self.model, key):
                column = getattr(self.model, key)
                if value is None:
                    query = query.where(column.is_(None))
                else:
                    query = query.where(column == value)

        if order_by and hasattr(self.model, order_by):
            query = query.order_by(getattr(self.model, order_by))

        query = query.offset(offset).limit(limit)

        result = await self.session.execute(query)
        return  list(result.scalars().all())

    async def update(
        self, uuid: UUID, data: SQLModel | Dict[str, Any]
    ) -> Optional[T]:
        db_item = await self.get_by_id(uuid)

        if not db_item:
            return None

        update_data = (
            data if isinstance(data, dict)
            else data.model_dump(exclude_unset=True)
        )
        db_item.sqlmodel_update(update_data)

        await self.session.flush()
        await self.session.refresh(db_item)
        return db_item

    async def delete(self, uuid: UUID) -> bool:
        db_item = await self.get_by_id(uuid)
        if db_item:
            await self.session.delete(db_item)
            await self.session.flush()
            return True
        return False

    async def count(self, **filters) -> int:
        query = select(func.count()).select_from(self.model)

        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)

        result = await self.session.execute(query)
        return result.scalar_one()

    async def exists(self, uuid: UUID) -> bool:
        query = select(
            sql_exists().where(col(self.model.id) == uuid)
        )
        result = await self.session.execute(query)
        return result.scalar()
