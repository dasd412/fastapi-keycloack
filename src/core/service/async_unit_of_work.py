from sqlalchemy.ext.asyncio import AsyncSession


class AsyncUnitOfWork:
    """
    Async Base UnitOfWork - 비동기 트랜잭션 관리만 담당
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def __aenter__(self):
        return self

    async def close(self):
        await self.session.close()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()