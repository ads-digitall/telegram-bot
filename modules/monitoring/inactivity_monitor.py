"""
modules/monitoring/inactivity_monitor.py

Модуль мониторинга бездействия пользователей.
Если пользователь не активен более 60 минут — его история сообщений очищается (кроме приветственного).
Затем происходит переход к логике кнопки "Лента".
"""

from datetime import datetime, timedelta
from core.redis_cache import get_last_action
from modules.bot.utils.bot_instance import bot
from modules.bot.handlers.feed import handle_feed_button
from core.database.crud import get_all_active_users  # Нужно реализовать, если нет
import logging

logger = logging.getLogger("inactivity_monitor")

# Настройка тайм-аута
INACTIVITY_TIMEOUT_MINUTES = 60

async def cleanup_chat_history(user_id: int):
    """
    Удаляет все сообщения пользователя, кроме приветственного.
    Требует реализации хранения ID сообщений (например, в Redis или БД).
    """
    try:
        # Пример логики (нужна своя реализация хранения ID сообщений):
        message_ids = await get_user_message_ids(user_id)  # реализовать
        welcome_id = await get_welcome_message_id(user_id)  # реализовать

        for msg_id in message_ids:
            if msg_id != welcome_id:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except Exception as e:
                    logger.warning(f"Не удалось удалить сообщение {msg_id} для пользователя {user_id}: {e}")
    except Exception as e:
        logger.error(f"Ошибка очистки истории чата для пользователя {user_id}: {e}")


async def check_inactive_users():
    """
    Проверка всех активных пользователей на предмет неактивности.
    Если пользователь бездействует более 60 минут — история очищается и вызывается "лента".
    """
    try:
        users = await get_all_active_users()  # реализация зависит от проекта
        now = datetime.utcnow()

        for user in users:
            user_id = user.id if hasattr(user, 'id') else user  # поддержка разных форматов
            last_action = await get_last_action(user_id)

            if last_action and (now - last_action > timedelta(minutes=INACTIVITY_TIMEOUT_MINUTES)):
                logger.info(f"Пользователь {user_id} не активен > {INACTIVITY_TIMEOUT_MINUTES} мин — выполняем сброс.")
                await cleanup_chat_history(user_id)
                await handle_feed_button(user_id)
    except Exception as e:
        logger.error(f"Ошибка при проверке неактивных пользователей: {e}")
