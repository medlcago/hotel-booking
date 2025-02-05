import os
from datetime import timedelta
from enum import StrEnum
from functools import lru_cache
from pathlib import Path, PurePath

from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, SecretStr, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Mode(StrEnum):
    DEV = "DEV"
    PROD = "PROD"


class Database(BaseModel):
    driver: str = "asyncpg"
    user: str
    password: str
    host: str
    port: int
    name: str

    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 10
    echo: bool = False

    @property
    def dsn(self) -> str:
        from sqlalchemy.engine.url import URL
        return URL.create(
            drivername=f"postgresql+{self.driver}",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        ).render_as_string(hide_password=False)


class Redis(BaseModel):
    url: RedisDsn


class SmtpServer(BaseModel):
    username: str
    password: str
    host: str
    port: int


class Celery(BaseModel):
    broker_url: str
    backend_url: str


class Yookassa(BaseModel):
    shop_id: str
    secret_key: str
    return_url: str


class Settings(BaseSettings):
    secret_key: SecretStr
    db: Database
    redis: Redis
    smtp_server: SmtpServer
    celery: Celery
    yookassa: Yookassa
    templates: Jinja2Templates = Jinja2Templates(directory=BASE_DIR / "templates")

    base_url: str
    debug: bool = False

    access_token_lifetime: timedelta = timedelta(minutes=30)
    refresh_token_lifetime: timedelta = timedelta(days=1)

    default_throttle_limit: int
    default_throttle_time: int

    log_config: PurePath = BASE_DIR / "log_conf.yaml"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
        extra="ignore",
    )


class DevSettings(Settings):
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env.dev",
        env_nested_delimiter="__",
        extra="ignore",
    )


@lru_cache()
def get_settings(mode: Mode | None = None) -> Settings:
    mode = mode or os.getenv("MODE", Mode.DEV)
    if mode == Mode.DEV:
        return DevSettings()
    return Settings()


settings = get_settings()
