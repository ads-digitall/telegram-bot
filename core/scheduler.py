from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from core.config import settings
from modules.bot.services.post_service import send_posts
from modules.bot.services.user_service import update_user_interests
from modules.bot.services.post_cache_service import clean_cache
from core.database import get_database
from error_handler import handle_error
from sqlalchemy.future import select
from core.database.models import Channel, PremiumUser
from modules.monitoring.inactivity_monitor import check_inactive_users

from aiogram import Bot
from modules.profile.config import TELEGRAM_PROFILE_TOKEN

import logging
import asyncio

logger = logging.getLogger("scheduler")

scheduler = AsyncIOScheduler()

async def start_scheduler():
    try:
        scheduler_interval = settings.SCHEDULER_INTERVAL_HOURS

        scheduler.add_job(
            update_interests_for_all_users,
            IntervalTrigger(days=1),
        )

        scheduler.add_job(
            periodic_task,
            IntervalTrigger(hours=scheduler_interval),
        )

        scheduler.add_job(
            clean_cache,
            IntervalTrigger(minutes=5),
        )

        scheduler.add_job(
            check_inactive_users,
            IntervalTrigger(minutes=10),
        )

        scheduler.add_job(
            reset_channel_limits,
            CronTrigger(day=1, hour=0, minute=0),
        )

        scheduler.add_job(
            check_channel_limits,
            IntervalTrigger(hours=6),  # 🔄 проверяем каждые 6 часов
        )

        scheduler.start()
        logger.info("✅ Планировщик запущен.")

    except Exception as e:
        handle_error(e, "SchedulerStartup", "Ошибка при запуске планировщика")
        logger.error(f"Ошибка при запуске планировщика: {e}")

async def periodic_task():
    try:
        async for session in get_database():
            users = await session.execute("SELECT user_id FROM users WHERE is_active = 1")
            users = users.fetchall()
            break

        for row in users:
            user_id = row[0]
            try:
                await send_posts(user_id)
            except Exception as e:
                handle_error(e, "PostDispatch", f"Ошибка при отправке постов пользователю {user_id}")

    except Exception as e:
        handle_error(e, "PeriodicTask", "Ошибка при выполнении задачи рассылки")

async def update_interests_for_all_users():
    try:
        await update_user_interests()
    except Exception as e:
        handle_error(e, "UpdateInterests", "Ошибка при обновлении интересов")

async def reset_channel_limits():
    try:
        async for session in get_database():
            result = await session.execute(select(Channel))
            channels = result.scalars().all()
            for channel in channels:
                channel.monthly_views_left = channel.monthly_limit
            await session.commit()

        logger.info("🔁 Ежемесячные лимиты каналов сброшены.")
    except Exception as e:
        handle_error(e, "ResetLimits", "Ошибка при сбросе лимитов каналов")
        logger.error(f"Ошибка при сбросе лимитов: {e}")

async def check_channel_limits():
    try:
        bot = Bot(token=TELEGRAM_PROFILE_TOKEN)
        async for session in get_database():
            result = await session.execute(select(Channel))
            channels = result.scalars().all()

            for channel in channels:
                if channel.monthly_views_left is not None and channel.monthly_views_left < 100:
                    admins = channel.admin_user_ids or []
                    for admin_id in admins:
                        try:
                            await bot.send_message(
                                chat_id=admin_id,
                                text=(
                                    f"📊 <b>Уведомление</b>\n\n"
                                    f"У канала <b>{channel.channel_name}</b> осталось "
                                    f"<b>{channel.monthly_views_left}</b> бесплатных показов.\n\n"
                                    f"Чтобы продолжить появляться в ленте, вы можете:\n"
                                    f"— Подписаться на премиум\n"
                                    f"— Пригласить друзей по рефералке\n\n"
                                    f"<b>Ваш профиль:</b> /profile"
                                ),
                                parse_mode="HTML"
                            )
                        except Exception as err:
                            logger.warning(f"⚠️ Не удалось отправить уведомление администратору {admin_id}: {err}")

    except Exception as e:
        handle_error(e, "CheckChannelLimits", "Ошибка при проверке лимитов")
        logger.error(f"Ошибка при проверке лимитов каналов: {e}")
