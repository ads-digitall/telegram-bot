"""
Пакет core проекта «Бот-2».

Содержит базовые модули для загрузки конфигурации, логирования, подключения к базе данных и Redis.

Публичные объекты:
    Settings - класс для загрузки конфигурации (из config.py)
    get_settings - функция для получения конфигурации (из config.py)
    get_logger - функция для настройки логирования (из logger.py)
    get_database - функция для получения подключения к БД (из database.py)
    get_redis_client - функция для подключения к Redis (из redis.py)
"""

from .config import settings
from .config import get_settings
from .logger import get_logger
from .database import get_database
from .redis import get_redis_client


__all__ = ["Settings", "get_settings", "get_logger", "get_database", "get_redis_client"]
