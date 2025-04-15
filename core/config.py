"""
Модуль конфигурации проекта «Бот-2».

Использует config_validator для загрузки и валидации переменных окружения.
Предоставляет глобальный объект `settings` для использования по всему проекту.
"""

from core.config_validator import get_settings
from core.logger import get_logger

logger = get_logger()

try:
    settings = get_settings()
    logger.info("Конфигурация успешно загружена.")
except Exception as e:
    logger.error(f"Ошибка загрузки конфигурации: {e}")
    raise e

__all__ = ["settings"]
