"""
Модуль CRUD (Create, Read, Update, Delete) для работы с базой данных проекта «Бот-2».
В этой версии реализован общий класс CRUDBase, который объединяет повторяющийся код для всех моделей.
Миграции схемы базы данных теперь ведутся через Alembic (отдельный каталог с конфигурацией), 
поэтому функциональность миграций в данном файле отсутствует.
"""

from sqlalchemy.future import select
from core.logger import get_logger
from .models import User, Channel, Post  # Импортируем модели базы данных

logger = get_logger(__name__)


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def create(self, session, data: dict):
        try:
            logger.debug(f"Создание объекта {self.model.__name__} с данными: {data}")
            instance = self.model(**data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            logger.debug(f"Объект {self.model.__name__} создан успешно.")
            return instance
        except Exception as e:
            logger.error(f"Ошибка создания объекта {self.model.__name__} с данными {data}: {e}")
            raise

    async def get(self, session, primary_key):
        instance = await session.get(self.model, primary_key)
        return instance

    async def update(self, session, primary_key, update_data: dict):
        try:
            logger.debug(f"Обновление объекта {self.model.__name__} с id {primary_key} данными: {update_data}")
            instance = await self.get(session, primary_key)
            if instance is None:
                logger.debug(f"{self.model.__name__} с id {primary_key} не найден для обновления.")
                return None
            for key, value in update_data.items():
                setattr(instance, key, value)
            await session.commit()
            await session.refresh(instance)
            logger.debug(f"Объект {self.model.__name__} с id {primary_key} успешно обновлен.")
            return instance
        except Exception as e:
            logger.error(f"Ошибка обновления объекта {self.model.__name__} с id {primary_key}: {update_data} | {e}")
            raise

    async def delete(self, session, primary_key):
        try:
            instance = await self.get(session, primary_key)
            if instance:
                await session.delete(instance)
                await session.commit()
                logger.debug(f"Объект {self.model.__name__} с id {primary_key} успешно удален.")
            return instance
        except Exception as e:
            logger.error(f"Ошибка удаления объекта {self.model.__name__} с id {primary_key}: {e}")
            raise

    async def get_all(self, session, limit: int = 100, offset: int = 0):
        stmt = select(self.model).limit(limit).offset(offset)
        result = await session.execute(stmt)
        instances = result.scalars().all()
        logger.debug(f"Получено {len(instances)} объектов модели {self.model.__name__}.")
        return instances


# Создаем экземпляры CRUD для конкретных моделей
user_crud = CRUDBase(User)
channel_crud = CRUDBase(Channel)
post_crud = CRUDBase(Post)


# === Обёртки для USER ===
async def add_user(session, data: dict):
    return await user_crud.create(session, data)

async def get_user(session, item_id):
    return await user_crud.get(session, item_id)

async def update_user(session, item_id, update_data: dict):
    return await user_crud.update(session, item_id, update_data)

async def delete_user(session, item_id):
    return await user_crud.delete(session, item_id)

async def get_all_users(session, limit: int = 100, offset: int = 0):
    return await user_crud.get_all(session, limit=limit, offset=offset)


# === Обёртки для CHANNEL ===
async def add_channel(session, data: dict):
    return await channel_crud.create(session, data)

async def get_channel(session, item_id):
    return await channel_crud.get(session, item_id)

async def update_channel(session, item_id, update_data: dict):
    return await channel_crud.update(session, item_id, update_data)

async def delete_channel(session, item_id):
    return await channel_crud.delete(session, item_id)

async def get_all_channels(session, limit: int = 100, offset: int = 0):
    return await channel_crud.get_all(session, limit=limit, offset=offset)


# === Обёртки для POST ===
async def add_post(session, data: dict):
    return await post_crud.create(session, data)

async def get_post(session, item_id):
    return await post_crud.get(session, item_id)

async def update_post(session, item_id, update_data: dict):
    return await post_crud.update(session, item_id, update_data)

async def delete_post(session, item_id):
    return await post_crud.delete(session, item_id)

async def get_all_posts(session, limit: int = 100, offset: int = 0):
    return await post_crud.get_all(session, limit=limit, offset=offset)


__all__ = [
    "CRUDBase", "user_crud", "channel_crud", "post_crud",

    # User
    "add_user", "get_user", "update_user", "delete_user", "get_all_users",

    # Channel
    "add_channel", "get_channel", "update_channel", "delete_channel", "get_all_channels",

    # Post
    "add_post", "get_post", "update_post", "delete_post", "get_all_posts"
]
