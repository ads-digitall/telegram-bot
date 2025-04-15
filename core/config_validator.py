"""
core/config_validator.py

Модуль для загрузки и валидации конфигурации проекта.
Содержит класс Settings, который загружает переменные окружения
и предоставляет доступ к ним через pydantic-settings.
"""

from pydantic_settings import BaseSettings
from pydantic import ValidationError
from pydantic import Field



class Settings(BaseSettings):
    BOT_TOKEN: str = Field(alias="TELEGRAM_TOKEN")
    TELEGRAM_TOKEN: str
    TELEGRAM_PROFILE_TOKEN: str  # ← добавлено
    LENTA_BOT_USERNAME: str      # ← добавлено
    PROFILE_BOT_USERNAME: str    # ← добавлено

    API_ID: str
    API_HASH: str

    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str

    PREMIUM_CHANNEL_ID: str

    DEBUG: bool = False

    class Config:
        env_file = "config.env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Игнорировать лишние поля, если они есть в .env, но не в Settings


def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        raise RuntimeError(f"Ошибка валидации конфигурации: {e}")
