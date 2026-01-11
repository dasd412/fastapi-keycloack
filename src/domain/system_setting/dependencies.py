# # dependencies.py - 여기서 의존성 조립
# from sqlalchemy.ext.asyncio import AsyncSession
#
# async def get_db():
#     async with SessionLocal() as session:
#         yield session
#
# async def get_post_repository(db: AsyncSession = Depends(get_db)):
#     return PostRepository(db)
#
# async def get_post_service(
#     repository: PostRepository = Depends(get_post_repository)
# ):
#     return PostService(repository)