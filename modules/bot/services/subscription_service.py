"""
subscription_service.py

Сервисный слой для управления подписками и премиум-доступом пользователя.
Инкапсулирует логику доступа к БД и проверки условий.
"""

from core.logger import get_logger
from core.database import get_database
from core.database.crud import user_crud

# ✅ Импорт ограничителя и моделей
from modules.bot.utils.rate_limiter import TelegramRateLimiter
from core.database.models import User, Channel, PremiumUser
from aiogram import Bot
from core.config import settings

logger = get_logger(__name__)

# ✅ Инициализация ограничителя
rate_limiter = TelegramRateLimiter()

async def is_user_subscribed(user_id: int) -> bool:
    """
    Проверяет, подписан ли пользователь.

    Returns:
        bool: True, если пользователь имеет статус 'subscribed', иначе False.
    """
    async for db in get_database():
        user = await user_crud.get(db, user_id)
        if user and user.subscription_status == "subscribed":
            return True
    return False

async def subscribe_user(user_id: int) -> None:
    """
    Устанавливает статус 'subscribed' для пользователя.
    """
    async for db in get_database():
        await user_crud.update(db, user_id, {"subscription_status": "subscribed"})
        logger.info(f"Пользователь {user_id} подписан.")
        break

async def unsubscribe_user(user_id: int) -> None:
    """
    Устанавливает статус 'unsubscribed' для пользователя.
    """
    async for db in get_database():
        await user_crud.update(db, user_id, {"subscription_status": "unsubscribed"})
        logger.info(f"Пользователь {user_id} отписан.")
        break

async def is_user_premium(user_id: int, bot: Bot) -> bool:
    """
    Проверяет, является ли пользователь премиум-подписчиком
    через участие в премиум-канале.

    Если он подписан, но ещё не добавлен в PremiumUser — добавляет его туда.
    """
    try:
        member = await bot.get_chat_member(settings.PREMIUM_CHANNEL_ID, user_id)
        is_subscribed = member.status in ("member", "administrator", "creator")
    except Exception:
        is_subscribed = False

    if not is_subscribed:
        return False

    async for session in get_database():
        premium_admin = await session.get(PremiumUser, user_id)
        if is_subscribed and not premium_admin:
            new_premium = PremiumUser(user_id=user_id, premium_views=0)
            session.add(new_premium)
            await session.commit()
        return True

# ✅ Новая функция синхронизации каналов и пользователей
async def sync_user_subscriptions(bot: Bot):
    """
    Синхронизирует поле subscribed_channels у пользователей на основе их
    реального участия в каналах, где присутствует бот.
    """
    async for session in get_database():
        channels_result = await session.execute(Channel.__table__.select())
        channels = channels_result.fetchall()

        users_result = await session.execute(User.__table__.select())
        users = users_result.fetchall()

        for channel_row in channels:
            channel_id = channel_row.channel_id
            for user_row in users:
                user_id = user_row.user_id
                try:
                    await rate_limiter.throttle()
                    member = await bot.get_chat_member(channel_id, user_id)
                    if member.status in ["member", "administrator", "creator"]:
                        user = await session.get(User, user_id)
                        if user:
                            if not user.subscribed_channels:
                                user.subscribed_channels = []
                            if channel_id not in user.subscribed_channels:
                                user.subscribed_channels.append(channel_id)
                                await session.commit()
                                logger.info(f"✅ {user_id} подписан на канал {channel_id}")
                except Exception as e:
                    logger.warning(f"⚠️ Ошибка проверки {user_id} в {channel_id}: {e}")

# ✅ Добавлено: синхронизация только одного пользователя
async def update_user_subscriptions(user_id: int, bot: Bot):
    """
    Обновляет список каналов, на которые подписан конкретный пользователь.
    """
    async for session in get_database():
        user = await session.get(User, user_id)
        if not user:
            return

        channels_result = await session.execute(Channel.__table__.select())
        channels = channels_result.fetchall()

        updated_channels = []

        for row in channels:
            channel_id = row.channel_id
            try:
                await rate_limiter.throttle()
                member = await bot.get_chat_member(channel_id, user_id)
                if member.status in ["member", "administrator", "creator"]:
                    if not user.subscribed_channels:
                        user.subscribed_channels = []
                    if channel_id not in user.subscribed_channels:
                        user.subscribed_channels.append(channel_id)
                    if member.status in ["administrator", "creator"]:
                        if not user.managed_channels:
                            user.managed_channels = []
                        if channel_id not in user.managed_channels:
                            user.managed_channels.append(channel_id)
                    updated_channels.append(channel_id)
            except Exception as e:
                logger.warning(f"Проверка {user_id} в {channel_id} не удалась: {e}")

        await session.commit()
        logger.info(f"Обновлены каналы пользователя {user_id}: {updated_channels}")
