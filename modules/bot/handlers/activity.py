"""
activity.py

Обновляет активность пользователя при любом текстовом сообщении,
кроме /start и кнопок меню — чтобы не мешать другим обработчикам.
Добавлена централизованная обработка ошибок.
Теперь добавлена логика для обновления счетчиков активности постов.
"""

from aiogram import Router, types, F
from core.logger import get_logger
from modules.bot.services.user_service import update_user_activity
from error_handler import handle_error
from modules.bot.services.post_service import update_post_activity

logger = get_logger(__name__)
router = Router()

# Обрабатываем ТОЛЬКО текст, НЕ команды, НЕ кнопки меню
@router.message(
    F.text & 
    ~F.text.in_({"/start", "📢 Лента", "📡 Каналы Новости", "⚙️ Профиль"})
)
async def update_activity_handler(message: types.Message) -> None:
    try:
        await update_user_activity(message)
        logger.debug(f"Активность пользователя {message.from_user.id} обновлена.")

        if message.text.startswith("https://"):
            post_id = extract_post_id_from_link(message.text)
            if post_id:
                await update_post_activity(post_id, "view")
                logger.debug(f"Активность для поста {post_id} обновлена (просмотр).")

    except Exception as e:
        handle_error(e, "ActivityHandler", f"Ошибка при обновлении активности пользователя {message.from_user.id}")
        try:
            await message.answer("Произошла ошибка при обновлении вашей активности. Пожалуйста, попробуйте позже.")
        except Exception as inner_exception:
            handle_error(inner_exception, "ActivityHandler", f"Ошибка при отправке сообщения об ошибке пользователю {message.from_user.id}")

# Функция для извлечения ID поста из URL (примерная)
def extract_post_id_from_link(url: str) -> int:
    if "/post/" in url:
        try:
            post_id = int(url.split("/post/")[1])
            return post_id
        except ValueError:
            return None
    return None

# Обработчик реакций на посты (например, лайки, комментарии)
@router.message(
    F.text.in_({"👍", "❤️", "💬"})
)
async def update_reactions_handler(message: types.Message) -> None:
    try:
        post_id = extract_post_id_from_link(message.text)
        if post_id:
            await update_post_activity(post_id, "reaction")
            logger.debug(f"Реакция для поста {post_id} обновлена (реакция).")
    except Exception as e:
        handle_error(e, "ReactionHandler", f"Ошибка при обработке реакции для пользователя {message.from_user.id}")
        try:
            await message.answer("Произошла ошибка при обработке вашей реакции. Пожалуйста, попробуйте позже.")
        except Exception as inner_exception:
            handle_error(inner_exception, "ReactionHandler", f"Ошибка при отправке сообщения об ошибке пользователю {message.from_user.id}")

# Обработчик кликов по ссылкам
@router.message(
    F.text.contains("https://")
)
async def update_clicks_handler(message: types.Message) -> None:
    try:
        post_id = extract_post_id_from_link(message.text)
        if post_id:
            await update_post_activity(post_id, "click")
            logger.debug(f"Клик для поста {post_id} обновлен (клик).")
    except Exception as e:
        handle_error(e, "ClickHandler", f"Ошибка при обработке клика для пользователя {message.from_user.id}")
        try:
            await message.answer("Произошла ошибка при обработке вашего клика. Пожалуйста, попробуйте позже.")
        except Exception as inner_exception:
            handle_error(inner_exception, "ClickHandler", f"Ошибка при отправке сообщения об ошибке пользователю {message.from_user.id}")

def register_handler(dp):
    dp.include_router(router)
