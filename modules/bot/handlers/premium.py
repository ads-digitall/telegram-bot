"""
premium.py

Обработчик команды /premium для Telegram-бота.
Проверяет статус пользователя через subscription_service.
Добавлена обработка ошибок.
"""

from aiogram import Router, types
from aiogram.filters import Command
from core.logger import get_logger
from modules.bot.services.subscription_service import is_user_premium
from error_handler import handle_error  # Импортируем централизованный обработчик ошибок

logger = get_logger(__name__)
router = Router()

@router.message(Command("premium"))
async def handle_premium(message: types.Message) -> None:
    """
    Обрабатывает команду /premium — проверяет статус пользователя.
    """
    user_id = message.from_user.id
    logger.info(f"Получен запрос /premium от пользователя {user_id}")

    try:
        if await is_user_premium(user_id, message.bot):
            await message.answer(
                "🎉 У вас уже активен Премиум-доступ!\n\nВот ваш эксклюзивный контент: ..."
            )
            logger.info(f"Пользователь {user_id} имеет премиум-доступ.")
        else:
            await message.answer(
                "💎 Премиум-доступ открывает доступ к эксклюзивным возможностям:\n"
                "- Расширенная лента\n"
                "- Уведомления из закрытых источников\n"
                "- Приоритетная поддержка\n\n"
                "Чтобы активировать премиум, перейдите по ссылке: https://t.me/yourbot?start=premium"
            )
            logger.info(f"Пользователь {user_id} не имеет премиум-доступа.")
    except Exception as e:
        # Централизованная обработка ошибки с отправкой уведомлений
        handle_error(e, "PremiumHandler", f"Ошибка при обработке премиум-запроса пользователя {user_id}")
        logger.error(f"Ошибка при обработке премиум-запроса пользователя {user_id}: {e}")
        try:
            # Отправка сообщения о проблемах при обработке запроса
            await message.answer("❗ Произошла ошибка при обработке запроса. Попробуйте позже.")
        except Exception as send_err:
            handle_error(send_err, "PremiumHandler", f"Ошибка при отправке сообщения об ошибке пользователю {user_id}")
            logger.error(f"Ошибка при отправке сообщения об ошибке пользователю {user_id}: {send_err}")

# Для автодискавера:
def register_handler(dp):
    dp.include_router(router)
