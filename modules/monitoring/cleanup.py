"""
cleanup.py

Периодическая очистка:
- неактивных пользователей (in-memory)
- устаревших записей в БД
- Redis-ключей

Запуск через task_manager или вручную.
Добавлена обработка ошибок для повышения устойчивости.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict

from core.logger import get_logger
from modules.monitoring.cleanup_service import CleanupService

logger = get_logger()

# Временное in-memory хранилище активности пользователей
user_activity: Dict[int, datetime] = {}

# Интервалы
CHECK_INTERVAL = 60  # сек
INACTIVITY_THRESHOLD = timedelta(minutes=15)


async def cleanup_user_data(user_id: int) -> None:
    """
    Очистка временных данных пользователя из памяти.
    """
    try:
        logger.info(f"Очистка временных данных для неактивного пользователя {user_id}")
        # Здесь можно очищать сессии, кэш, FSM и т.п.
    except Exception as e:
        logger.error(f"Ошибка при очистке данных пользователя {user_id}: {e}")
        try:
            # Если нужно, отправить уведомление пользователю или администратору
            # await send_error_notification(f"Ошибка при очистке данных пользователя {user_id}")
            pass
        except Exception as inner_exception:
            logger.error(f"Ошибка при уведомлении об ошибке при очистке данных пользователя {user_id}: {inner_exception}")


async def perform_memory_cleanup() -> None:
    """
    Очистка in-memory неактивных пользователей.
    """
    while True:
        try:
            now = datetime.utcnow()
            inactive = [
                user_id for user_id, last_seen in user_activity.items()
                if now - last_seen > INACTIVITY_THRESHOLD
            ]
            for user_id in inactive:
                await cleanup_user_data(user_id)
                user_activity.pop(user_id, None)

            logger.debug(f"Очистка завершена. Неактивных пользователей: {len(inactive)}")
        except Exception as e:
            logger.error(f"Ошибка при очистке in-memory данных: {e}")
            try:
                # Можно отправить уведомление администратору или записать в систему мониторинга
                # await send_error_notification("Ошибка при очистке in-memory.")
                pass
            except Exception as inner_exception:
                logger.error(f"Ошибка при уведомлении об ошибке очистки in-memory: {inner_exception}")

        await asyncio.sleep(CHECK_INTERVAL)


async def run_full_cleanup_cycle() -> None:
    """
    Запуск полной сервисной очистки: база данных + Redis.
    """
    try:
        service = CleanupService()
        await service.run_full_cleanup()
    except Exception as e:
        logger.error(f"Ошибка при запуске полной очистки: {e}")
        try:
            # Возможно, уведомить администратора о проблемах с полным циклом очистки
            # await send_error_notification("Ошибка при запуске полной очистки.")
            pass
        except Exception as inner_exception:
            logger.error(f"Ошибка при отправке уведомления об ошибке очистки: {inner_exception}")


async def perform_cleanup() -> None:
    """
    Функция запуска полного цикла очистки системы:
    - Однократно выполняется полная очистка базы данных и Redis.
    - Запускается непрерывная периодическая очистка in-memory данных.
    """
    try:
        # Запускаем периодическую in-memory очистку в отдельной задаче
        memory_cleanup_task = asyncio.create_task(perform_memory_cleanup())
        # Однократно запускаем полную очистку (БД + Redis)
        await run_full_cleanup_cycle()
        # Если требуется дальнейший контроль, можно дождаться завершения задачи (но perform_memory_cleanup работает бесконечно)
        # await memory_cleanup_task
    except Exception as e:
        logger.error(f"Ошибка при выполнении perform_cleanup: {e}")
