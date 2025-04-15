"""
Модуль инициализации для функциональности репостов новостей.
Предоставляет асинхронный API для отправки новостей пользователям.
"""

import logging
from aiogram import Bot
from aiogram.types import Message
from typing import Optional

# Замените на актуальный путь к конфигурации и логированию
try:
    from core.config import settings
    from core.logger import logger
except ImportError:
    logger = logging.getLogger(__name__)

bot: Optional[Bot] = None

def init_reposts_module(telegram_bot: Bot) -> None:
    """
    Инициализирует модуль репостов с переданным ботом.
    :param telegram_bot: Экземпляр бота aiogram
    """
    global bot
    bot = telegram_bot
    logger.info("Модуль репостов инициализирован")

async def repost_news(user_id: int, news: str) -> bool:
    """
    Отправляет новость пользователю.
    :param user_id: Идентификатор Telegram-пользователя
    :param news: Текст новости
    :return: True, если сообщение успешно отправлено, иначе False
    """
    if bot is None:
        logger.error("Бот не инициализирован в модуле reposts.")
        return False
    try:
        await bot.send_message(chat_id=user_id, text=news)
        logger.info(f"Новость успешно отправлена пользователю {user_id}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при отправке новости пользователю {user_id}: {e}")
        return False
