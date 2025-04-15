"""
settings_service.py

Сервисный слой для работы с пользовательскими настройками:
- обновление языка
- изменение интересов
- включение/отключение уведомлений
"""

from core.logger import get_logger
from core.database import get_database
from core.database.crud import user_crud

logger = get_logger(__name__)


async def update_user_language(user_id: int, lang_code: str) -> bool:
    """
    Обновляет язык пользователя в БД.

    Args:
        user_id (int): ID пользователя
        lang_code (str): Языковой код, например 'ru', 'en'

    Returns:
        bool: True, если успешно обновлено, иначе False
    """
    async for db in get_database():
        await user_crud.update(db, user_id, {"language_code": lang_code})
        logger.info(f"Язык пользователя {user_id} обновлён на {lang_code}")
        return True
    return False


async def update_user_interests(user_id: int, tags: str) -> bool:
    """
    Обновляет интересы пользователя (строка тегов через запятую).

    Args:
        user_id (int): ID пользователя
        tags (str): интересы, например: "спорт,финансы,технологии"

    Returns:
        bool: True, если успешно обновлено, иначе False
    """
    async for db in get_database():
        await user_crud.update(db, user_id, {"interest_tags": tags})
        logger.info(f"Интересы пользователя {user_id} обновлены: {tags}")
        return True
    return False


async def set_user_notifications(user_id: int, enabled: bool) -> bool:
    """
    Включает или отключает уведомления пользователю.

    Args:
        user_id (int): ID пользователя
        enabled (bool): True — включить, False — выключить

    Returns:
        bool: True, если успешно обновлено, иначе False
    """
    async for db in get_database():
        await user_crud.update(db, user_id, {"notifications_enabled": enabled})
        logger.info(f"Уведомления для пользователя {user_id}: {'включены' if enabled else 'отключены'}")
        return True
    return False


async def get_user_settings(user_id: int) -> dict | None:
    """
    Возвращает словарь с текущими настройками пользователя.

    Args:
        user_id (int): ID пользователя

    Returns:
        dict | None: Настройки, либо None, если пользователь не найден
    """
    async for db in get_database():
        user = await user_crud.get(db, user_id)
        if user:
            return {
                "language": user.language_code,
                "tags": user.interest_tags,
                "notifications_enabled": getattr(user, "notifications_enabled", True)
            }
        return None
