from functools import cache

from sqlalchemy.engine import URL
from sqlmodel import Session, SQLModel, create_engine
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


class PGSession:
    def __call__(self):
        with Session(
            bind=get_engine(), autocommit=False, autoflush=False, expire_on_commit=False
        ) as session:
            yield session
