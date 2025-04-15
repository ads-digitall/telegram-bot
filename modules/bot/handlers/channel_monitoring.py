"""
channel_monitoring.py

Обработка событий, связанных с каналами:
- Добавление / удаление бота
- Появление нового поста
"""

from aiogram import Router, types
from sqlalchemy import text
from core.logger import get_logger
from modules.bot.services.channel_service import (
    process_bot_added_to_channel,
    save_new_post,
    add_user_subscription,
    remove_user_subscription
)
from error_handler import handle_error
from core.database import get_database

logger = get_logger(__name__)
router = Router()

@router.my_chat_member()
async def on_bot_added(event: types.ChatMemberUpdated) -> None:
    try:
        logger.info(f"🔔 Обнаружено событие добавления бота в канал: {event.chat.id}")
        await process_bot_added_to_channel(event)
        logger.info(f"✅ Бот зарегистрирован в канале: {event.chat.id}")

        user_id = event.from_user.id
        status = event.new_chat_member.status
        if status in ["member", "administrator", "creator"]:
            await add_user_subscription(user_id, event.chat.id)
        elif status in ["left", "kicked"]:
            await remove_user_subscription(user_id, event.chat.id)

            async for session in get_database():
                await session.execute(text("DELETE FROM posts WHERE channel_id = :cid"), {"cid": event.chat.id})
                await session.execute(text("DELETE FROM channels WHERE channel_id = :cid"), {"cid": event.chat.id})
                await session.commit()
                logger.info(f"❌ Канал {event.chat.id} и все посты удалены.")
                break

    except Exception as e:
        handle_error(e, "ChannelMonitoring", f"Ошибка регистрации канала {event.chat.id}")
        logger.error(f"❌ Ошибка при регистрации канала {event.chat.id}: {e}")


@router.channel_post()
async def on_new_post(message: types.Message) -> None:
    try:
        logger.info(f"📨 Новый пост в канале {message.chat.id}, message_id={message.message_id}")
        await save_new_post(
            channel_id=message.chat.id,
            message_id=message.message_id,
            post_date=message.date.replace(tzinfo=None)
        )
        logger.info(f"✅ Пост сохранён: {message.message_id}")
    except Exception as e:
        handle_error(e, "ChannelMonitoring", f"Ошибка сохранения поста {message.message_id}")
        logger.error(f"❌ Ошибка сохранения поста {message.message_id}: {e}")


def register_handler(dp):
    dp.include_router(router)
