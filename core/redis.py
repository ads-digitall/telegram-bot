"""
Модуль для подключения к Redis с использованием асинхронной библиотеки redis.asyncio.
Предоставляет единый API для получения клиента Redis и управления соединением.
Обработаны ошибки и улучшено логирование.
Добавлена централизованная обработка ошибок.
"""

import redis.asyncio as redis
import logging
from typing import Optional
from core.config import settings
from error_handler import handle_error  # Импортируем централизованный обработчик ошибок

logger = logging.getLogger(__name__)

_redis_client: Optional[redis.Redis] = None

async def get_redis_client() -> redis.Redis:
    """
    Возвращает асинхронного клиента Redis.
    Создаёт нового клиента при первом вызове и переиспользует его при последующих.
    
    :return: redis.Redis — асинхронный клиент Redis
    """
    global _redis_client
    if _redis_client is None:
        try:
            # Создаём нового клиента Redis
            _redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,  # Используем значение из конфигурации
                decode_responses=True
            )
            # Пытаемся подключиться для проверки
            await _redis_client.ping()
            logger.info("Redis client initialized successfully.")
        except redis.exceptions.ConnectionError as e:
            logger.error(f"Redis connection error: {e}")
            handle_error(e, "RedisModule", f"Failed to connect to Redis at {settings.REDIS_HOST}:{settings.REDIS_PORT}")
            raise RuntimeError(f"Failed to connect to Redis at {settings.REDIS_HOST}:{settings.REDIS_PORT}")
        except redis.exceptions.TimeoutError as e:
            logger.error(f"Redis timeout error: {e}")
            handle_error(e, "RedisModule", "Redis connection timed out.")
            raise RuntimeError("Redis connection timed out.")
        except Exception as e:
            logger.error(f"Failed to initialize Redis client: {e}")
            handle_error(e, "RedisModule", "Failed to initialize Redis client due to an unexpected error.")
            raise RuntimeError("Failed to initialize Redis client due to an unexpected error.")
    return _redis_client

async def close_redis_client() -> None:
    """
    Закрывает текущее соединение Redis.
    """
    global _redis_client
    if _redis_client:
        try:
            await _redis_client.close()
            logger.info("Redis client connection closed successfully.")
        except Exception as e:
            logger.error(f"Error while closing Redis client: {e}")
            handle_error(e, "RedisModule", "Error while closing Redis client.")
        finally:
            _redis_client = None

async def set_value(key: str, value: str) -> bool:
    """
    Пример добавления значения в Redis.
    """
    try:
        redis_client = await get_redis_client()
        await redis_client.set(key, value)
        logger.info(f"Set key {key} with value {value}")
        return True
    except Exception as e:
        logger.error(f"Failed to set value for key {key}: {e}")
        handle_error(e, "RedisModule", f"Failed to set value for key {key}")
        return False

async def get_value(key: str) -> Optional[str]:
    """
    Пример получения значения из Redis.
    """
    try:
        redis_client = await get_redis_client()
        value = await redis_client.get(key)
        logger.info(f"Got value {value} for key {key}")
        return value
    except Exception as e:
        logger.error(f"Failed to get value for key {key}: {e}")
        handle_error(e, "RedisModule", f"Failed to get value for key {key}")
        return None
