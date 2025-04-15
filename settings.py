"""
settings.py

Централизованная точка доступа к конфигурации проекта через валидатор Pydantic.
"""

from core.config import settings  # Используем уже готовый объект settings из core.config

# Примеры доступа:
# settings.POSTGRES_USER
# settings.REDIS_HOST
# settings.TELEGRAM_TOKEN
# settings.DEBUG
