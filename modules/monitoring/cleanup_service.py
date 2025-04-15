"""
cleanup_service.py

Сервис для периодической очистки устаревших данных:
- неактивные пользователи
- старые посты
- устаревшие Redis-ключи

Вызывается вручную или по расписанию (например, через task_manager).
"""

import datetime
from sqlalchemy import text
from core.logger import get_logger
from core.database import get_database
from core.redis import get_redis_client

logger = get_logger(__name__)


class CleanupService:
    """
    Класс для централизованной очистки данных (БД, Redis и др.)
    """

    def __init__(self):
        self.now = datetime.datetime.utcnow()

    async def delete_inactive_users(self, inactive_days: int = 180) -> int:
        """
        Удаляет пользователей, которые не были активны более inactive_days дней.
        """
        threshold = self.now - datetime.timedelta(days=inactive_days)
        query = text("DELETE FROM users WHERE last_active IS NOT NULL AND last_active < :threshold")
        async for db in get_database():
            result = await db.execute(query, {"threshold": threshold})
            await db.commit()
            count = result.rowcount or 0
            logger.info(f"Удалено {count} неактивных пользователей (более {inactive_days} дней)")
            return count
        return 0

    async def cleanup_old_posts(self, max_age_days: int = 90) -> int:
        """
        Удаляет посты, которым более max_age_days.
        """
        threshold = self.now - datetime.timedelta(days=max_age_days)
        query = text("DELETE FROM posts WHERE date IS NOT NULL AND date < :threshold")
        async for db in get_database():
            result = await db.execute(query, {"threshold": threshold})
            await db.commit()
            count = result.rowcount or 0
            logger.info(f"Удалено {count} старых постов (старше {max_age_days} дней)")
            return count
        return 0

    async def cleanup_redis_keys(self, pattern: str = "cache:*") -> int:
        """
        Удаляет Redis-ключи по шаблону (например, cache:*).
        """
        client = await get_redis_client()
        keys = await client.keys(pattern)
        if keys:
            await client.delete(*keys)
            logger.info(f"Удалено {len(keys)} ключей Redis по шаблону '{pattern}'")
            return len(keys)
        logger.info(f"Ключей по шаблону '{pattern}' не найдено.")
        return 0

    async def run_full_cleanup(self) -> None:
        """
        Запускает полный цикл очистки.
        """
        await self.delete_inactive_users()
        await self.cleanup_old_posts()
        await self.cleanup_redis_keys()
