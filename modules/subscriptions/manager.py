"""
manager.py

SubscriptionManager — класс, инкапсулирующий логику подписки/отписки пользователей.
Вызывается из callback.py, использует Redis и базу данных (через crud).
Добавлена обработка ошибок и улучшение логирования.
"""

from aiogram.types import Message
from core.logger import get_logger
from core.database import get_database
from core.database.crud import user_crud
from core.redis import get_redis_client
from error_handler import handle_error  # Импортируем централизованный обработчик ошибок

logger = get_logger(__name__)

class SubscriptionManager:
    def __init__(self):
        self.redis = None

    async def setup(self):
        """
        Отдельный метод для инициализации Redis (асинхронно).
        """
        try:
            self.redis = await get_redis_client()
            logger.info("Подключение к Redis установлено.")
        except Exception as e:
            logger.error(f"Ошибка при инициализации Redis: {e}")
            handle_error(e, "SubscriptionManager", "Ошибка при инициализации Redis")
            raise

    async def subscribe_user(self, user_id: int) -> bool:
        """
        Подписка пользователя.
        """
        try:
            async for db in get_database():
                await user_crud.update(db, user_id, {"subscription_status": "subscribed"})
                logger.info(f"Пользователь {user_id} подписан.")
                return True
        except Exception as e:
            logger.error(f"Ошибка при подписке пользователя {user_id}: {e}")
            handle_error(e, "SubscriptionManager", f"Ошибка при подписке пользователя {user_id}")
            return False

    async def unsubscribe_user(self, user_id: int) -> bool:
        """
        Отписка пользователя.
        """
        try:
            async for db in get_database():
                await user_crud.update(db, user_id, {"subscription_status": "unsubscribed"})
                logger.info(f"Пользователь {user_id} отписан.")
                return True
        except Exception as e:
            logger.error(f"Ошибка при отписке пользователя {user_id}: {e}")
            handle_error(e, "SubscriptionManager", f"Ошибка при отписке пользователя {user_id}")
            return False

    async def get_subscription_status(self, user_id: int) -> str:
        """
        Получить статус подписки пользователя.
        """
        try:
            async for db in get_database():
                user = await user_crud.get(db, user_id)
                if user:
                    return user.subscription_status or "unsubscribed"
            return "unsubscribed"
        except Exception as e:
            logger.error(f"Ошибка при получении статуса подписки для пользователя {user_id}: {e}")
            handle_error(e, "SubscriptionManager", f"Ошибка при получении статуса подписки для пользователя {user_id}")
            return "unsubscribed"

    async def toggle_subscription(self, user_id: int) -> str:
        """
        Переключение статуса подписки пользователя.
        """
        try:
            current_status = await self.get_subscription_status(user_id)
            if current_status == "subscribed":
                await self.unsubscribe_user(user_id)
                return "unsubscribed"
            else:
                await self.subscribe_user(user_id)
                return "subscribed"
        except Exception as e:
            logger.error(f"Ошибка при переключении подписки для пользователя {user_id}: {e}")
            handle_error(e, "SubscriptionManager", f"Ошибка при переключении подписки для пользователя {user_id}")
            return "error"

    async def handle_callback(self, callback_data: dict, message: Message):
        """
        Обработка callback от Telegram-кнопки.
        Например: {'action': 'subscribe', 'user_id': 12345}
        """
        try:
            action = callback_data.get("action")
            user_id = int(callback_data.get("user_id", 0))

            if action == "subscribe":
                result = await self.subscribe_user(user_id)
                if result:
                    await message.answer("✅ Вы подписались.")
                else:
                    await message.answer("❌ Не удалось подписаться. Попробуйте позже.")
            elif action == "unsubscribe":
                result = await self.unsubscribe_user(user_id)
                if result:
                    await message.answer("📭 Вы отписались.")
                else:
                    await message.answer("❌ Не удалось отписаться. Попробуйте позже.")
            elif action == "toggle":
                new_status = await self.toggle_subscription(user_id)
                if new_status == "subscribed":
                    await message.answer("🔔 Подписка активна.")
                elif new_status == "unsubscribed":
                    await message.answer("🔕 Подписка отключена.")
                else:
                    await message.answer("❌ Произошла ошибка при переключении подписки.")
            else:
                await message.answer("❌ Неизвестное действие.")
        except Exception as e:
            logger.error(f"Ошибка при обработке callback: {e}")
            handle_error(e, "SubscriptionManager", "Ошибка при обработке callback")
            await message.answer("❌ Произошла ошибка при обработке вашего запроса. Попробуйте позже.")
            

# Для автодискавера:
def register_handler(dp):
    dp.include_router(router)
