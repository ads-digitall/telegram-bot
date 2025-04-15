from aiogram import types
from core.database.models import User
from core.database import get_database
from core.logger import get_logger

logger = get_logger()

PROFILE_BOT_USERNAME = "lenta_profile_bot"

async def handle(message: types.Message, bot):
    """
    Обрабатывает нажатие кнопки '⚙️Профиль'.
    Перенаправляет пользователя в бот-профиль.
    """
    logger.info("Обработка кнопки '⚙️Профиль' — переадресация в @lenta_profile_bot")

    async for session in get_database():
        user = await session.get(User, message.from_user.id)
        if not user:
            user = User(user_id=message.from_user.id)
            session.add(user)
            await session.commit()

    logger.info(f"➡️ Обработка профиля для user_id = {message.from_user.id}")

    profile_link = f"https://t.me/{PROFILE_BOT_USERNAME}"

    # 🔘 Создаём inline-кнопку со ссылкой
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Открыть профиль", url=profile_link)]
    ])

    await message.answer(
        "👤 Ваш профиль доступен по ссылке ниже:",
        reply_markup=keyboard
    )
