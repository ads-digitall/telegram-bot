"""
id_user.py

Регистрирует пользователя при любом текстовом сообщении,
за исключением /start и кнопок меню, чтобы не мешать другим обработчикам.
Добавлена централизованная обработка ошибок.
"""

from aiogram import Router, types, F
from core.logger import get_logger
from modules.bot.services.user_service import register_user_from_message
from error_handler import handle_error  # Импортируем централизованный обработчик ошибок

logger = get_logger(__name__)
router = Router()

@router.message(
    F.text & 
    ~F.text.in_({"/start", "📢 Лента", "📡 Каналы Новости", "⚙️ Настройки"})
)
async def handle_user_registration(message: types.Message) -> None:
    try:
        # Пытаемся зарегистрировать или обновить пользователя
        await register_user_from_message(message)
        logger.debug(f"Регистрация/обновление пользователя {message.from_user.id} завершено.")
    except Exception as e:
        # Логируем ошибку при регистрации пользователя
        handle_error(e, "UserRegistrationHandler", f"Ошибка при регистрации пользователя {message.from_user.id}")
        logger.error(f"Ошибка при регистрации пользователя {message.from_user.id}: {e}")
        try:
            # Сообщаем пользователю о возникшей ошибке
            await message.answer("Произошла ошибка при регистрации. Пожалуйста, попробуйте позже.")
        except Exception as inner_exception:
            # Логируем ошибку при отправке сообщения об ошибке
            handle_error(inner_exception, "UserRegistrationHandler", f"Ошибка при отправке сообщения об ошибке пользователю {message.from_user.id}")
            logger.error(f"Ошибка при отправке сообщения об ошибке пользователю {message.from_user.id}: {inner_exception}")

def register_handler(dp):
    dp.include_router(router)
