import enum
from pathlib import Path

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(str, enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class StorageType(str, enum.Enum):
    LOCAL = "local"
    S3 = "s3"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix='APP_',
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    server_host: str = "127.0.0.1"
    server_port: int = 8000
    server_reload: bool = True

    log_level: LogLevel = LogLevel.INFO

    openweather_api_key: str

    cache_expiry_minutes: int = 5
    app_root: Path = Path(__file__).parent.parent

    data_dir: Path = Field(default=app_root / "data")
    log_file: Path = Field(default=app_root / "logs" / "weather.log")

    # Storage settings
    storage_type: StorageType = StorageType.LOCAL

    # AWS S3 settings
    aws_s3_bucket: str | None = None
    aws_region: str = "us-east-1"
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None


settings = Settings()
