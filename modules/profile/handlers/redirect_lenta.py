# modules/profile/handlers/redirect_lenta.py

from aiogram import Router, types, F
from core.logger import get_logger
from core.config import settings
LENTA_BOT_USERNAME = settings.LENTA_BOT_USERNAME

router = Router()
logger = get_logger(__name__)

@router.message(F.text == "📢 Лента")
async def handle_feed_redirect(message: types.Message):
    """Отправляет ссылку на первый бот с параметром для запуска ленты."""
    url = f"https://t.me/{LENTA_BOT_USERNAME}?start=feed"
    logger.info(f"➡️ Перенаправление на ленту: {url}")
    await message.answer("🔗 Лента доступна здесь:\n" + url)

@router.message(F.text == "📡 Каналы Новости")
async def handle_news_redirect(message: types.Message):
    """Отправляет ссылку на первый бот с параметром для запуска новостей."""
    url = f"https://t.me/{LENTA_BOT_USERNAME}?start=news"
    logger.info(f"➡️ Перенаправление на каналы новости: {url}")
    await message.answer("🔗 Новости каналов доступны здесь:\n" + url)
