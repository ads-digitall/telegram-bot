from aiogram import Bot  
from aiogram import Router, types, F
from core.logger import get_logger
from error_handler import handle_error
from modules.bot.handlers.feed import handle_feed_command
from modules.bot.buttons import profile_button

logger = get_logger(__name__)
router = Router()

@router.message(F.text)
async def fallback_handler(message: types.Message):
    try:
        logger.debug(f"== Fallback получил текст: {message.text!r}")
        logger.debug(f"⬇️ Получена команда или сообщение: {message.text}")

        if message.text.startswith("/"):
            logger.info(f"➡️ Обрабатываем команду: {message.text}")
            if message.text == "/start":
                await handle_start(message)
            elif message.text == "📢 Лента":
                await handle_feed_command(message)
            elif message.text == "⚙️ Профиль":
                await profile_button.handle(message, bot=message.bot)
            else:
                await message.answer("Неизвестная команда. Пожалуйста, используйте доступные команды.")
                logger.warning(f"Неизвестная команда: {message.text}")

        else:
            if message.text == "📢 Лента":
                await handle_feed_command(message)
            elif message.text == "⚙️ Профиль":
                await profile_button.handle(message, bot=message.bot)
            else:
                await message.answer("Ваше сообщение не распознано. Пожалуйста, используйте доступные команды или кнопки.")
                logger.info(f"Не команда, а текстовое сообщение получено: {message.text}")

    except Exception as e:
        handle_error(e, "FallbackHandler", f"Ошибка при обработке сообщения: {message.text}")
        logger.error(f"❌ Ошибка при обработке сообщения: {message.text}. Ошибка: {e}")
        try:
            await message.answer("Произошла ошибка при обработке вашего сообщения. Попробуйте позже.")
        except Exception as inner_exception:
            handle_error(inner_exception, "FallbackHandler", f"Ошибка при отправке сообщения об ошибке пользователю: {message.from_user.id}")
            logger.error(f"❌ Ошибка при отправке сообщения об ошибке пользователю: {inner_exception}")

async def handle_start(message: types.Message):
    """
    Обрабатывает команду /start.
    """
    try:
        logger.info(f"⬇️ Команда /start обработана для пользователя {message.from_user.id}")
        await message.answer("Добро пожаловать! Выберите действие:", reply_markup=handle_main_menu())
    except Exception as e:
        logger.error(f"Ошибка при обработке команды /start: {e}")
        await message.answer("Ошибка при обработке команды /start.")

def handle_main_menu():
    """
    Формирует клавиатуру для главного меню.
    """
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📢 Лента"), types.KeyboardButton(text="📡 Каналы Новости")],
            [types.KeyboardButton(text="⚙️ Профиль")]
        ],
        resize_keyboard=True
    )

def register_handler(dp):
    dp.include_router(router)
