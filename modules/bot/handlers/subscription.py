"""
subscription.py

Обработчики команд подписки Telegram-бота.
Бизнес-логика подписки вынесена в subscription_service.
Обработчики выполняют только маршрутизацию и ответ пользователю.
Добавлена обработка ошибок.
"""

from aiogram import Router, types
from aiogram.filters import Command
from core.logger import get_logger
from error_handler import handle_error  # Импортируем централизованный обработчик ошибок
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from modules.bot.services.subscription_service import (
    is_user_subscribed,
    subscribe_user,
    unsubscribe_user
)

logger = get_logger(__name__)
router = Router()

# Создаем клавиатуру для подписки и отписки
def get_subscription_menu() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру с кнопками для подписки/отписки.
    """
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Подписаться на новости 📩")],
            [KeyboardButton(text="Отписаться от новостей 🚫")]
        ],
        resize_keyboard=True
    )
    return kb

@router.message(Command("subscribe"))
async def handle_subscription(message: types.Message) -> None:
    """
    Обрабатывает команду /subscribe — подписка пользователя.
    """
    user_id = message.from_user.id
    logger.info(f"Получена команда /subscribe от пользователя {user_id}")

    try:
        if not await is_user_subscribed(user_id):
            await subscribe_user(user_id)
            await message.answer("Вы успешно подписались.", reply_markup=get_subscription_menu())
            logger.info(f"Пользователь {user_id} подписан.")
        else:
            await message.answer("Вы уже подписаны.", reply_markup=get_subscription_menu())
            logger.info(f"Пользователь {user_id} уже подписан.")
    except Exception as e:
        handle_error(e, "SubscriptionHandler", f"Ошибка при подписке пользователя {user_id}")
        logger.error(f"Ошибка при подписке пользователя {user_id}: {e}")
        try:
            await message.answer("Произошла ошибка при подписке. Попробуйте позже.", reply_markup=get_subscription_menu())
        except Exception as inner_exception:
            handle_error(inner_exception, "SubscriptionHandler", f"Ошибка при отправке сообщения об ошибке пользователю {user_id}")
            logger.error(f"Ошибка при отправке сообщения об ошибке пользователю {user_id}: {inner_exception}")

@router.message(Command("unsubscribe"))
async def handle_unsubscription(message: types.Message) -> None:
    """
    Обрабатывает команду /unsubscribe — отписка пользователя.
    """
    user_id = message.from_user.id
    logger.info(f"Получена команда /unsubscribe от пользователя {user_id}")

    try:
        if await is_user_subscribed(user_id):
            await unsubscribe_user(user_id)
            await message.answer("Вы успешно отписались.", reply_markup=get_subscription_menu())
            logger.info(f"Пользователь {user_id} отписан.")
        else:
            await message.answer("Вы ещё не подписаны.", reply_markup=get_subscription_menu())
            logger.info(f"Пользователь {user_id} не был подписан.")
    except Exception as e:
        handle_error(e, "SubscriptionHandler", f"Ошибка при отписке пользователя {user_id}")
        logger.error(f"Ошибка при отписке пользователя {user_id}: {e}")
        try:
            await message.answer("Произошла ошибка при отписке. Попробуйте позже.", reply_markup=get_subscription_menu())
        except Exception as inner_exception:
            handle_error(inner_exception, "SubscriptionHandler", f"Ошибка при отправке сообщения об ошибке пользователю {user_id}")
            logger.error(f"Ошибка при отправке сообщения об ошибке пользователю {user_id}: {inner_exception}")

# Для автодискавера:
def register_handler(dp):
    dp.include_router(router)
