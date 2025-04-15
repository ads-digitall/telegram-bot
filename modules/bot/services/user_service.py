"""
user_service.py

Сервисный слой для работы с пользователями:
- регистрация
- обновление данных
- обновление активности
- обновление интересов
"""

import time
import datetime
import random
from aiogram import types
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from core.logger import get_logger
from core.database import get_database
from core.database.crud import user_crud
from core.database.models import User

logger = get_logger(__name__)

async def register_user_from_message(message: types.Message) -> None:
    """
    Регистрирует пользователя по сообщению. Если уже существует — обновляет данные.
    """
    user_data = {
        'user_id': message.from_user.id,
        'username': message.from_user.username or "",
        'first_name': message.from_user.first_name or "",
        'last_name': message.from_user.last_name or "",
        'language_code': message.from_user.language_code or "",
        'last_active': None,
        'registration_date': None,
        'interests': []  # Массив интересов
    }

    async for db in get_database():
        try:
            await user_crud.create(db, user_data)
            logger.debug(f"Пользователь {message.from_user.id} добавлен в БД.")
        except IntegrityError:
            await db.rollback()
            logger.debug(f"Пользователь {message.from_user.id} уже существует, обновляем.")
            update_data = {
                'username': user_data["username"],
                'first_name': user_data["first_name"],
                'last_name': user_data["last_name"],
                'language_code': user_data["language_code"]
            }
            await user_crud.update(db, message.from_user.id, update_data)
        except Exception as e:
            logger.error(f"Ошибка регистрации пользователя {message.from_user.id}: {e}")
        finally:
            break

async def update_user_activity(message: types.Message) -> None:
    """
    Обновляет поле last_active у пользователя в базе.
    """
    try:
        user_id = message.from_user.id
        current_time = time.time()
        current_datetime = datetime.datetime.fromtimestamp(current_time)

        async for db in get_database():
            await user_crud.update(db, user_id, {"last_active": current_datetime})
            logger.debug(f"last_active обновлён для {user_id}")
            break
    except Exception as e:
        logger.error(f"Ошибка при обновлении активности пользователя {user_id}: {e}")

async def update_user_interests(user_id: int) -> None:
    """
    Обновляет интересы пользователя на основе случайных данных.
    Этот метод можно адаптировать под внешние источники данных или другие алгоритмы.
    """
    new_interests = ["технологии", "спорт", "политика", "экономика", "культура", "кино", "наука", "мода", "здоровье", "игры"]

    async for session in get_database():
        user = await session.execute(select(User).where(User.user_id == user_id))
        user = user.scalars().first()

        if not user:
            raise Exception(f"Пользователь с ID {user_id} не найден.")

        # Случайным образом выбираем 10 интересов
        user.interests = random.sample(new_interests, 10)
        await session.commit()
        logger.debug(f"Интересы пользователя {user_id} обновлены: {user.interests}")
        break
