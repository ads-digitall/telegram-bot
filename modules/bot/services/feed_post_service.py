from aiogram import types
from core.database.models import Post
from modules.bot.services.feed_service import generate_user_feed
from modules.bot.services.post_cache_service import get_cached_post_ids, add_posts_to_cache
from error_handler import handle_error
import logging

# ✅ Новый импорт для ограничения запросов
from modules.bot.utils.rate_limiter import TelegramRateLimiter

logger = logging.getLogger(__name__)

user_last_feed = {}

# ✅ Инициализация ограничителя запросов
rate_limiter = TelegramRateLimiter()

def build_inline_buttons(post: Post) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="❤️", callback_data=f"reaction:{post.id}:heart"),
            types.InlineKeyboardButton(text="👍", callback_data=f"reaction:{post.id}:like"),
            types.InlineKeyboardButton(text="👎", callback_data=f"reaction:{post.id}:dislike"),
            types.InlineKeyboardButton(text="💬 Комментировать", url=f"https://t.me/c/{str(post.channel_id)[4:]}/{post.message_id}")
        ]
    ])

def more_feed_button() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="➕ Ещё", callback_data="more_feed_posts")]
    ])

async def send_feed_posts(message: types.Message, posts_per_page: int = 10):
    try:
        user_id = message.from_user.id

        all_posts = await generate_user_feed(user_id, posts_per_page=posts_per_page)

        # Фильтрация: исключаем уже отправленные посты (кеш)
        excluded_ids = set(get_cached_post_ids(user_id))
        posts = [p for p in all_posts if p.id not in excluded_ids]

        if not posts:
            await message.answer("Нет новых постов для ленты.")
            return

        user_last_feed[user_id] = [p.id for p in posts]

        for post in posts:
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

            except Exception as e:
                logger.warning(f"Ошибка при показе поста {post.id}: {e}")
                continue

        add_posts_to_cache(user_id, [p.id for p in posts])

        await rate_limiter.throttle()
        await message.answer("⬇️", reply_markup=more_feed_button())

    except Exception as e:
        handle_error(e, "FeedPostService", "Ошибка при отправке ленты")
        logger.error(f"Ошибка при отправке ленты: {e}")
        await message.answer("Произошла ошибка при загрузке ленты.")
