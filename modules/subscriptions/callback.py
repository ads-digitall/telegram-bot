"""
callback.py

Обработчик inline callback-запросов, связанных с подписками пользователей Telegram-бота.
Использует SubscriptionManager для логики, а common.utils — для парсинга callback-data.
"""

from aiogram.types import CallbackQuery
from aiogram import Dispatcher
from core.logger import get_logger

from modules.common.utils import parse_callback_data
from modules.subscriptions.manager import SubscriptionManager

logger = get_logger()

async def handle_subscription_callback(callback: CallbackQuery) -> None:
    """
    Обрабатывает callback-запрос вида 'subscribe:123456', 'unsubscribe:123456', 'toggle:123456'.

    Args:
        callback (CallbackQuery): объект callback от Telegram
    """
    user_id = callback.from_user.id
    raw_data = callback.data or ""

    try:
        logger.info(f"[SUB CALLBACK] от пользователя {user_id}: {raw_data}")

        # Парсим данные
        callback_data = parse_callback_data(raw_data)
        if not callback_data:
            await callback.answer("❌ Неверный формат запроса.")
            return

        # Инициализируем менеджер
        manager = SubscriptionManager()
        await manager.setup()

        # Обработка
        await manager.handle_callback(callback_data, callback.message)

        # Ответ Telegram
        await callback.answer("✅ Выполнено.")
    except Exception as e:
        logger.error(f"Ошибка обработки подписки от пользователя {user_id}: {e}")
        try:
            await callback.answer("⚠️ Ошибка при обработке запроса.")
        except Exception as send_err:
            logger.error(f"Ошибка при отправке сообщения об ошибке: {send_err}")


def register_subscription_callback(dp: Dispatcher) -> None:
    """
    Регистрирует callback-обработчик с фильтрацией по префиксу.
    """
    try:
        dp.callback_query.register(
            handle_subscription_callback,
            lambda c: c.data and c.data.startswith(("subscribe:", "unsubscribe:", "toggle:"))
        )
        logger.info("Обработчик подписок по callback зарегистрирован.")
    except Exception as e:
        logger.warning(f"Ошибка регистрации callback-обработчика подписки: {e}")


# Для автодискавера:
register_handler = register_subscription_callback
