import os
from datetime import timedelta

from pydantic import BaseSettings, Field, PostgresDsn, RedisDsn

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfig(BaseSettings):
    app_title: str = "File Storage API"
    app_host: str = Field(..., env="APP_HOST")
    app_port: int = Field(..., env="APP_PORT")
    app_query_logging: int = Field(..., env="APP_QUERY_LOGGING")
    postgres_dsn: PostgresDsn = Field(..., env="POSTGRES_DSN")
    redis_dsn: RedisDsn = Field(..., env="REDIS_DSN")

    redis_expire: timedelta = timedelta(minutes=5)
    token_expire: timedelta = timedelta(minutes=15)

    folder_upload: str = Field(..., env="APP_FOLDER_UPLOADS")

    class Config:
        env_file = ".env.example"


config = AppConfig()
