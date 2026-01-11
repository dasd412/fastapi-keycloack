import os
from functools import cache

from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class PostgresSettings(BaseSettings):
    pg_host: str
    pg_port: int
    pg_username: str
    pg_password: str
    pg_database: str
    create_tables: bool = False


class Settings(
    PostgresSettings
):
    appname: str = "keycloak-poc"
    uvicorn_reload: bool = False
    uvicorn_port: int = 8000
    model_config = ConfigDict(extra='allow')


@cache
def get_settings() -> Settings:
    envfile = os.environ.get("ENVFILE")
    if envfile is not None:
        return Settings(_env_file=envfile)  # type: ignore[call-arg]

    return Settings()  # type: ignore[call-arg]
