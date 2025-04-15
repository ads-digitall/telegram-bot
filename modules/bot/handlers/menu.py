"""
menu.py

Обработчики главного меню Telegram-бота для проекта «Бот-2».
Обрабатывает команду /start и кнопки главного меню: Лента, Каналы Новости, ⚙️Профиль.
Регистрация пользователя вынесена в user_service, визуал — в buttons/.
Добавлена централизованная обработка ошибок.
"""

from aiogram import Bot  
from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from core.logger import get_logger
from modules.bot.buttons import profile_button  # заменено с settings

from modules.bot.services.user_service import register_user_from_message
from modules.bot.handlers.feed import handle_feed_command  # Новая логика
from error_handler import handle_error

logger = get_logger(__name__)
router = Router()

def get_main_menu() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру главного меню.
    """
    try:
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📢 Лента"), KeyboardButton(text="📡 Каналы Новости")],
                [KeyboardButton(text="⚙️ Профиль")]
            ],
            resize_keyboard=True
        )
        return kb
    except Exception as e:
        logger.error(f"Ошибка формирования главного меню: {e}")
        handle_error(e, "MenuHandler", "Ошибка при создании главного меню")
        return ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True)

@router.message(Command("start"))
async def start_menu_handler(message: types.Message) -> None:
    """
    Обрабатывает команду /start: регистрирует пользователя и показывает главное меню.
    """
    logger.info(f"Получена команда /start от пользователя {message.from_user.id}")
    try:
        await register_user_from_message(message)
    except Exception as e:
        handle_error(e, "MenuHandler", f"Ошибка регистрации пользователя {message.from_user.id}")
        logger.error(f"Ошибка регистрации пользователя {message.from_user.id}: {e}")
        await message.answer("Произошла ошибка при регистрации. Пожалуйста, попробуйте позже.")

    try:
        menu = get_main_menu()
        await message.answer("Добро пожаловать! Выберите действие:", reply_markup=menu)
        logger.info("Главное меню успешно отправлено пользователю.")
    except Exception as e:
        handle_error(e, "MenuHandler", "Ошибка при отправке главного меню пользователю")
        logger.error(f"Ошибка в обработчике start_menu_handler: {e}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")

@router.message(F.text == "📢 Лента")
async def handle_feed(message: types.Message) -> None:
    """
    Обрабатывает кнопку '📢 Лента'.
    """
    try:
        await handle_feed_command(message)  # Вызываем новую логику
    except Exception as e:
        handle_error(e, "MenuHandler", "Ошибка при обработке запроса 'Лента'")
        logger.error(f"Ошибка в обработчике handle_feed: {e}")
        await message.answer("Ошибка при обработке запроса.")

@router.message(F.text == "📡 Каналы Новости")
async def handle_channels(message: types.Message) -> None:
    """
    Обрабатывает кнопку '📡 Каналы Новости'.
    """
    try:
        await channels.handle(message, bot=None)
    except Exception as e:
        handle_error(e, "MenuHandler", "Ошибка при обработке запроса 'Каналы Новости'")
        logger.error(f"Ошибка в обработчике handle_channels: {e}")
        await message.answer("Ошибка при обработке запроса.")

@router.message(F.text == "⚙️ Профиль")
async def profile_handler(message: types.Message) -> None:
    """
    Обрабатывает кнопку '⚙️ Профиль'.
    """
    try:
        logger.info(f"▶️ Обработчик профиля сработал для user_id = {message.from_user.id}")
        await profile_button.handle(message, bot=message.bot)
    except Exception as e:
        handle_error(e, "MenuHandler", "Ошибка при обработке запроса 'Профиль'")
        logger.error(f"Ошибка в обработчике profile_handler: {e}")
        await message.answer("Ошибка при обработке запроса.")

    # Для автодискавера:
def register_handler(dp):
    dp.include_router(router)
