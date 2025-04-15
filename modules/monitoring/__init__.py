"""
Модуль мониторинга проекта «Бот-2».

Этот модуль отвечает за сбор и обновление метрик системы, а также за регистрацию событий,
связанных с производительностью и отказоустойчивостью. Внешний API модуля включает функцию
perform_cleanup, которая выполняет автоматическую очистку данных для неактивных пользователей.
"""

from core.logger import get_logger
from typing import Any

logger = get_logger()

# Попытка импорта функции очистки из модуля cleanup.
try:
    from modules.monitoring.cleanup import perform_cleanup
    logger.info("Функция perform_cleanup успешно импортирована.")
except Exception as e:
    logger.warning(f"Не удалось импортировать perform_cleanup: {e}")

    async def perform_cleanup(*args: Any, **kwargs: Any) -> None:
        """
        Заглушка функции очистки, если основная функция недоступна.
        """
        logger.warning("Заглушка: perform_cleanup недоступна.")

__all__ = ["perform_cleanup"]
