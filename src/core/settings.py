from datetime import timedelta
from pathlib import Path, PurePath

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


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

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

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
    url: str


class Settings(BaseSettings):
    secret_key: SecretStr
    db: Database
    redis: Redis | None = None

    debug: bool
    access_token_lifetime: timedelta = timedelta(minutes=30)
    refresh_token_lifetime: timedelta = timedelta(days=1)

    log_config: PurePath = BASE_DIR / "log_conf.yaml"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
