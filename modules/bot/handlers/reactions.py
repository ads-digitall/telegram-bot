from aiogram import Router, types, F
from core.logger import get_logger
from error_handler import handle_error
from modules.bot.services.post_service import update_post_activity, build_inline_buttons
from core.database import get_database
from core.database.models import Post
from sqlalchemy.future import select
from modules.bot.services.post_cache_service import has_recent_reaction, add_recent_reaction

logger = get_logger(__name__)
router = Router()

@router.callback_query(F.data.startswith("reaction:"))
async def handle_reaction_callback(callback: types.CallbackQuery):
    """
    Обработка нажатия на inline-кнопки реакций:
    ❤️ (heart), 👍 (like), 👎 (dislike)
    Формат callback_data: reaction:<post_id>:<reaction_type>
    """
    try:
        parts = callback.data.split(":")
        if len(parts) != 3:
            await callback.answer("⚠️ Некорректная реакция.")
            return

        _, post_id_str, reaction_type = parts
        post_id = int(post_id_str)
        user_id = callback.from_user.id

        if has_recent_reaction(user_id, post_id):
            await callback.answer("⏳ Вы уже голосовали за этот пост недавно.")
            return

        if reaction_type in {"heart", "like", "dislike"}:
            await update_post_activity(post_id, reaction_type, user_id=user_id)
            add_recent_reaction(user_id, post_id)

            async for session in get_database():
                result = await session.execute(select(Post).where(Post.id == post_id))
                post = result.scalars().first()
                break

            short_id = str(post.channel_id)[4:]
            channel_link = f"https://t.me/c/{short_id}"
            stats = (
                f"⬆️ <a href='{channel_link}'>Перейти в канал</a>\n"
                f"❤️ {post.reactions_count_heart}  "
                f"👍 {post.reactions_count_like}  "
                f"👎 {post.reactions_count_dislike}"
            )

            await callback.message.edit_text(
                text=stats,
                reply_markup=build_inline_buttons(post),
                parse_mode="HTML"
            )

            await callback.answer("✅ Реакция учтена!")
        else:
            await callback.answer("⚠️ Неизвестный тип реакции.")

    except Exception as e:
        handle_error(e, "ReactionsHandler", f"Ошибка реакции от пользователя {callback.from_user.id}")
        logger.error(f"❌ Ошибка реакции от пользователя {callback.from_user.id}: {e}")
        try:
            await callback.answer("Произошла ошибка при обработке.")
        except:
            pass

def register_handler(dp):
    dp.include_router(router)
