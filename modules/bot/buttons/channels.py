"""
channels.py

По кнопке 'Каналы Новости' — отправляет пользователю последние посты.
"""

from aiogram.types import Message
from core.logger import get_logger
from modules.bot.services.post_service import send_posts  # Используем новую логику

logger = get_logger()

async def handle(message: Message, bot):
    """
    Обрабатывает нажатие кнопки 'Каналы Новости' — отправляет посты с фиксацией на первом.
    """
    logger.info("Обработан функционал кнопки 'Каналы Новости'. Запуск отправки постов.")
    await send_posts(message, posts_per_page=10)
