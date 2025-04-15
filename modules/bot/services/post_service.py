from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from core.database import get_database
from core.database.models import Post, User, Channel, PremiumUser
from error_handler import handle_error
from modules.bot.services.post_cache_service import get_cached_post_ids, add_posts_to_cache
from aiogram import types

import logging

# ✅ Добавлен импорт ограничителя
from modules.bot.utils.rate_limiter import TelegramRateLimiter

logger = logging.getLogger(__name__)

user_last_posts = {}

# ✅ Инициализация ограничителя
rate_limiter = TelegramRateLimiter()

async def delete_post_from_db(post_id: int):
    async for session in get_database():
        await session.execute(delete(Post).where(Post.id == post_id))
        await session.commit()
        break

async def update_post_activity(post_id: int, action_type: str, user_id: int | None = None) -> None:
    try:
        if user_id and post_id in user_last_posts.get(user_id, []):
            logger.info(f"📩 Пользователь {user_id} активировал пост {post_id}. Догружаем ещё.")
            user_last_posts[user_id] = []

        async for session in get_database():
            post_result = await session.execute(select(Post).where(Post.id == post_id))
            post = post_result.scalars().first()

            if not post:
                logger.warning(f"Пост с ID {post_id} не найден.")
                break

            if action_type == "view":
                post.views_count += 1
            elif action_type == "reaction":
                post.reactions_count += 1
            elif action_type == "click":
                post.clicks_count += 1
            elif action_type == "heart":
                post.reactions_count_heart += 1
            elif action_type == "like":
                post.reactions_count_like += 1
            elif action_type == "dislike":
                post.reactions_count_dislike += 1

            await session.commit()
            break

    except Exception as e:
        handle_error(e, "PostService", f"Ошибка при обновлении активности для поста {post_id}")
        logger.error(f"Ошибка при обновлении активности для поста {post_id}: {e}")
        raise

async def get_next_posts(last_post_id: int | None = None, limit: int = 50):
    async for session in get_database():
        if last_post_id:
            result = await session.execute(
                select(Post).where(Post.id < last_post_id).order_by(Post.id.desc()).limit(limit)
            )
        else:
            result = await session.execute(
                select(Post).order_by(Post.id.desc()).limit(limit)
            )
        posts = result.scalars().all()
        break
    return posts

def build_inline_buttons(post: Post) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="❤️", callback_data=f"reaction:{post.id}:heart"),
            types.InlineKeyboardButton(text="👍", callback_data=f"reaction:{post.id}:like"),
            types.InlineKeyboardButton(text="👎", callback_data=f"reaction:{post.id}:dislike"),
            types.InlineKeyboardButton(text="💬 Комментировать", url=f"https://t.me/c/{str(post.channel_id)[4:]}/{post.message_id}")
        ]
    ])

def more_button() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="➕ Ещё", callback_data="more_posts")]
    ])

async def send_posts(message, posts_per_page: int = 10, context: str = "feed"):
    try:
        user_id = message.from_user.id

        async for session in get_database():
            user = await session.get(User, user_id)
            logger.info(f"DEBUG: user.subscribed_channels = {user.subscribed_channels}")
            if not user or not user.subscribed_channels:
                await rate_limiter.throttle()
                await message.answer("Вы не подписаны ни на один канал.")
                return

            result = await session.execute(
                select(Post).where(Post.channel_id.in_(user.subscribed_channels)).order_by(Post.id.desc()).limit(300)
            )
            all_posts = result.scalars().all()
            break

        excluded_ids = set(get_cached_post_ids(user_id))
        candidate_posts = [p for p in all_posts if p.id not in excluded_ids][:posts_per_page]

        if not candidate_posts:
            await message.answer("Нет новых постов для отображения.")
            return

        posts_to_show = []
        async for session in get_database():
            for post in candidate_posts:
                if len(posts_to_show) >= posts_per_page:
                    break

                allow_post = True

                if context == "feed":
                    channel = await session.get(Channel, post.channel_id)
                    if channel and channel.monthly_views_left > 0:
                        channel.monthly_views_left -= 1
                    else:
                        allow_post = False
                        if channel and channel.admin_user_ids:
                            for admin_id in channel.admin_user_ids:
                                premium_admin = await session.get(PremiumUser, admin_id)
                                if premium_admin:
                                    if premium_admin.premium_views > 0:
                                        premium_admin.premium_views -= 1
                                        allow_post = True
                                        break
                                    elif premium_admin.referral_bonus_views > 0:
                                        premium_admin.referral_bonus_views -= 1
                                        allow_post = True
                                        break
                    await session.commit()

                if not allow_post:
                    logger.info(f"🚫 Пост {post.id} не показан — нет лимитов.")
                    continue

                try:
                    await rate_limiter.throttle()
                    await message.bot.forward_message(
                        chat_id=message.chat.id,
                        from_chat_id=post.channel_id,
                        message_id=post.message_id
                    )

                    short_id = str(post.channel_id)[4:]
                    channel_link = f"https://t.me/c/{short_id}"
                    stats = (
                        f"⬆️ <a href='{channel_link}'>Перейти в канал</a>\n"
                        f"❤️ {post.reactions_count_heart}  "
                        f"👍 {post.reactions_count_like}  "
                        f"👎 {post.reactions_count_dislike}"
                    )

                    await rate_limiter.throttle()
                    await message.bot.send_message(
                        chat_id=message.chat.id,
                        text=stats,
                        reply_markup=build_inline_buttons(post),
                        parse_mode="HTML"
                    )

                    posts_to_show.append(post)

                except Exception as e:
                    logger.warning(f"⚠️ Ошибка при отправке поста {post.id}: {e}")
                    if "message to forward not found" in str(e):
                        await delete_post_from_db(post.id)
                    continue

        if posts_to_show:
            add_posts_to_cache(user_id, [p.id for p in posts_to_show])
            await rate_limiter.throttle()
            await message.answer("⬇️", reply_markup=more_button())

    except Exception as e:
        logger.warning(f"⚠️ Ошибка при загрузке ленты: {e}")
