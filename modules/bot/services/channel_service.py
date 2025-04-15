from aiogram import types
from sqlalchemy import text

from core.logger import get_logger
from core.database import get_database
from modules.bot.utils.bot_instance import get_bot
from core.database.models import User  # ✅ добавлено для обновления подписок

logger = get_logger(__name__)


async def process_bot_added_to_channel(event: types.ChatMemberUpdated):
    """
    Обработка события добавления бота в канал.
    """
    channel_id = event.chat.id
    channel_name = event.chat.title
    username = event.chat.username
    channel_link = f"https://t.me/{username}" if username else "Ссылка отсутствует"

    async for db in get_database():
        await db.execute(
            text("""
                INSERT INTO channels (channel_id, channel_name, channel_link)
                VALUES (:id, :name, :link)
                ON CONFLICT (channel_id) DO NOTHING
            """),
            {"id": channel_id, "name": channel_name, "link": channel_link}
        )
        await db.commit()
        break

    logger.info(f"✅ Бот добавлен в канал: {channel_name} ({channel_link})")


async def save_new_post(channel_id: int, message_id: int, post_date: str):
    """
    Сохраняет новый пост в базу данных.
    """
    async for db in get_database():
        await db.execute(
            text("""
                INSERT INTO posts (channel_id, message_id, date)
                VALUES (:channel_id, :message_id, :post_date)
                ON CONFLICT DO NOTHING
            """),
            {"channel_id": channel_id, "message_id": message_id, "post_date": post_date}
        )
        await db.commit()
        break

    logger.info(f"💾 Сохранён пост {message_id} из канала {channel_id} от {post_date}")


# ✅ Новые функции

async def add_user_subscription(user_id: int, channel_id: int):
    """
    Добавляет канал в список подписок пользователя.
    """
    async for db in get_database():
        user = await db.get(User, user_id)
        if user:
            if not user.subscribed_channels:
                user.subscribed_channels = []
            if channel_id not in user.subscribed_channels:
                user.subscribed_channels.append(channel_id)
                await db.commit()
                logger.info(f"➕ Канал {channel_id} добавлен в подписки пользователя {user_id}")
        break


async def remove_user_subscription(user_id: int, channel_id: int):
    """
    Удаляет канал из списка подписок пользователя.
    """
    async for db in get_database():
        user = await db.get(User, user_id)
        if user and user.subscribed_channels and channel_id in user.subscribed_channels:
            user.subscribed_channels.remove(channel_id)
            await db.commit()
            logger.info(f"➖ Канал {channel_id} удалён из подписок пользователя {user_id}")
        break


async def get_user_channels(user_id: int, bot):
    """
    Получает список каналов, на которые пользователь подписан и которыми управляет.
    """
    subscribed_channels = []
    managed_channels = []

    async for db in get_database():
        result = await db.execute(text("SELECT channel_id, channel_name, channel_link FROM channels"))
        channels = result.fetchall()

        for channel in channels:
            channel_id = channel.channel_id
            try:
                member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
                status = member.status

                if status in ["member", "administrator", "creator"]:
                    subscribed_channels.append(channel)

                if status in ["administrator", "creator"]:
                    managed_channels.append(channel)

            except Exception as e:
                logger.warning(f"Не удалось получить статус пользователя {user_id} в канале {channel_id}: {e}")
                continue

        break

    return subscribed_channels, managed_channels
