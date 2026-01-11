from functools import cache

from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool

from core.config.settings import get_settings

settings = get_settings()


@cache
def get_engine():
    url = URL.create(
        drivername="postgresql",
        host=settings.pg_host,
        port=settings.pg_port,
        username=settings.pg_username,
        password=settings.pg_password,
        database=settings.pg_database,
    )
    engine = create_engine(
        url,
        poolclass=StaticPool,
        echo=settings.loglevel == "DEBUG",
    )
    if settings.create_tables:
        SQLModel.metadata.create_all(engine)

    return engine


@cache
def get_session_factory():
    """sessionmaker를 사용하여 Session factory 생성"""
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=get_engine(),
    )


class PGSession:
    def __call__(self):
        SessionLocal = get_session_factory()
        session = SessionLocal()
        print(f"DEBUG: PGSession - Created session: {session}")
        try:
            yield session
        finally:
            print(f"DEBUG: PGSession - Closing session")
            session.close()
            print(f"DEBUG: PGSession - Session closed")
