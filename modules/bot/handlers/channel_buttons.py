"""
channel_buttons.py

Обработка пользовательской кнопки "📡 Каналы Новости"
"""

from aiogram import Router, types, F
from sqlalchemy import select
from core.logger import get_logger
from modules.bot.services.post_service import send_posts
from error_handler import handle_error
from core.database import get_database
from core.database.models import UserState

logger = get_logger(__name__)
router = Router()

@router.message(F.text == "📡 Каналы Новости")
async def handle_channels_news(message: types.Message) -> None:
    try:
        logger.info(f"▶️ Пользователь {message.from_user.id} запросил 'Каналы Новости'")

        async for session in get_database():
            result = await session.execute(select(UserState).where(UserState.user_id == message.from_user.id))
            user_state = result.scalars().first()
            if user_state:
                user_state.last_read_post_id = None
                await session.commit()
            break

        await send_posts(message)

    except Exception as e:
        handle_error(e, "ChannelButtons", f"Ошибка в обработчике 'Каналы Новости' для {message.from_user.id}")
        logger.error(f"❌ Ошибка 'Каналы Новости' для {message.from_user.id}: {e}")
        try:
            await message.answer("Ошибка при обработке запроса. Пожалуйста, попробуйте позже.")
        except Exception as inner_exception:
            handle_error(inner_exception, "ChannelButtons", f"Ошибка при отправке ошибки пользователю {message.from_user.id}")
            logger.error(f"❌ Ошибка отправки сообщения об ошибке: {inner_exception}")

def register_handler(dp):
    dp.include_router(router)
