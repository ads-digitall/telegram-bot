from aiogram import Router, types, F
from modules.bot.services.feed_post_service import send_feed_posts
from core.logger import get_logger

logger = get_logger(__name__)
router = Router()

@router.message(F.text == "📢 Лента")
async def handle_feed_command(message: types.Message):
    """
    Обработка кнопки '📢 Лента' — запускает персонализированную ленту.
    """
    try:
        logger.info(f"📥 Пользователь {message.from_user.id} открыл ленту.")
        await send_feed_posts(message, posts_per_page=10)
    except Exception as e:
        logger.error(f"❌ Ошибка при обработке кнопки 'Лента': {e}")
        await message.answer("Произошла ошибка при открытии ленты.")

@router.callback_query(F.data == "more_feed_posts")
async def handle_more_feed_posts(callback: types.CallbackQuery):
    """
    Обработка нажатия кнопки 'Ещё' в ленте.
    """
    try:
        logger.info(f"🔁 Догрузка ленты для пользователя {callback.from_user.id}.")
        await send_feed_posts(callback.message, posts_per_page=10)
        await callback.answer()
    except Exception as e:
        logger.error(f"❌ Ошибка при догрузке ленты: {e}")
        try:
            await callback.answer("Ошибка при загрузке ленты.")
        except:
            pass

def register_handler(dp):
    dp.include_router(router)
