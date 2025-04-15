from aiogram import Router, types, F
from modules.bot.services.post_service import send_posts
from core.logger import get_logger
from error_handler import handle_error

logger = get_logger(__name__)
router = Router()

@router.callback_query(F.data == "more_posts")
async def handle_more_posts_callback(callback: types.CallbackQuery):
    """
    Обработка нажатия кнопки 'Ещё' для загрузки новых постов.
    """
    try:
        await callback.answer("Загружаю ещё посты...")

        # Удаляем сообщение с кнопкой "Ещё"
        try:
            await callback.message.delete()
        except Exception as e:
            logger.warning(f"Не удалось удалить сообщение кнопки 'Ещё': {e}")

        # Запускаем загрузку следующих постов
        await send_posts(callback.message, posts_per_page=10)

        logger.info(f"🔄 Пользователь {callback.from_user.id} нажал 'Ещё'")

    except Exception as e:
        handle_error(e, "MoreHandler", f"Ошибка обработки кнопки 'Ещё' для пользователя {callback.from_user.id}")
        logger.error(f"❌ Ошибка обработки кнопки 'Ещё' для пользователя {callback.from_user.id}: {e}")
        try:
            await callback.message.answer("Произошла ошибка при загрузке дополнительных постов.")
        except:
            pass

def register_handler(dp):
    dp.include_router(router)
