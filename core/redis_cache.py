"""
core/redis_cache.py

Модуль, предоставляющий высокоуровневые операции кеширования с использованием Redis.
Класс RedisCache является обёрткой над низкоуровневым клиентом Redis,
получаемым через функцию get_redis_client() из модуля core/redis.py.
Реализованы методы установки, получения и удаления кешированных значений с автоматической
сериализацией/десериализацией данных.
"""

import json
import logging
from datetime import datetime
from core.redis import get_redis_client

logger = logging.getLogger("redis_cache")


class RedisCache:
    def __init__(self, client=None):
        """
        Инициализирует объект RedisCache.

        Args:
            client: Низкоуровневый клиент Redis. Если не указан, будет создан через get_redis_client().
        """
        self.client = client if client is not None else get_redis_client()

    async def set_cache(self, key: str, value, expire: int = None) -> bool:
        """
        Устанавливает значение в кеш с необязательным временем истечения (TTL).

        Args:
            key (str): Ключ для сохранения значения.
            value: Значение, которое требуется сохранить (будет сериализовано в JSON).
            expire (int, optional): Время жизни кеша в секундах. Если None – без установки TTL.

        Returns:
            bool: True, если операция прошла успешно, иначе False.
        """
        try:
            serialized = json.dumps(value)
            if expire:
                result = await self.client.set(key, serialized, ex=expire)
            else:
                result = await self.client.set(key, serialized)
            logger.debug(f"Кеш для ключа '{key}' установлен. TTL: {expire}")
            return result
        except Exception as e:
            logger.error(f"Ошибка установки кеша для ключа '{key}': {e}")
            return False

    async def get_cache(self, key: str):
        """
        Получает значение из кеша и десериализует его из JSON.

        Args:
            key (str): Ключ, по которому хранится значение.

        Returns:
            Любой тип: Значение, десериализованное из JSON, или None, если ключ не найден.
        """
        try:
            data = await self.client.get(key)
            if data is not None:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Ошибка получения кеша для ключа '{key}': {e}")
            return None

    async def delete_cache(self, key: str) -> bool:
        """
        Удаляет значение из кеша.

        Args:
            key (str): Ключ, который необходимо удалить.

        Returns:
            bool: True, если элемент был удалён, иначе False.
        """
        try:
            result = await self.client.delete(key)
            if result and result > 0:
                logger.debug(f"Кеш для ключа '{key}' успешно удалён.")
                return True
            logger.debug(f"Ключ '{key}' не найден для удаления.")
            return False
        except Exception as e:
            logger.error(f"Ошибка удаления кеша для ключа '{key}': {e}")
            return False

    async def get_ttl(self, key: str) -> int:
        """
        Возвращает оставшееся время жизни (TTL) для указанного ключа.

        Args:
            key (str): Ключ, для которого необходимо получить TTL.

        Returns:
            int: Количество секунд до истечения ключа, -1 если ключ существует без TTL,
                 -2 если ключ не существует.
        """
        try:
            ttl = await self.client.ttl(key)
            logger.debug(f"TTL для ключа '{key}': {ttl} секунд.")
            return ttl
        except Exception as e:
            logger.error(f"Ошибка получения TTL для ключа '{key}': {e}")
            return -2


# === Новые функции для хранения времени последнего действия пользователя ===

async def update_last_action(user_id: int):
    try:
        client = await get_redis_client()
        await client.set(f"last_action:{user_id}", "1", ex=3600)
    except (ConnectionError, TimeoutError) as e:
        print(f"Ошибка Redis при установке ключа активности: {e}")
    value = datetime.utcnow().isoformat()
    await cache.set_cache(key, value)


async def get_last_action(user_id: int) -> datetime | None:
    """
    Получает время последнего действия пользователя.
    """
    cache = RedisCache()
    key = f"last_action:{user_id}"
    value = await cache.get_cache(key)
    if value:
        try:
            return datetime.fromisoformat(value)
        except Exception:
            logger.warning(f"Невозможно разобрать время: {value}")
    return None