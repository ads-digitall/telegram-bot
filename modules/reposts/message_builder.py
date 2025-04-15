"""
message_builder.py

Генерация содержимого для репоста:
- форматирование текста поста
- генерация inline-кнопок
- шаблоны представления

Вызывается из delivery.py, не зависит от Telegram API напрямую.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional
from modules.common.utils import truncate

MAX_CONTENT_LENGTH = 500  # Максимальная длина текста контента для отображения


def build_post_text(post: dict) -> str:
    """
    Формирует текст поста на основе словаря данных.

    Args:
        post (dict): {
            "title": str,
            "content": str,
            "tag": str,
            "url": str,
        }

    Returns:
        str: Отформатированный HTML-текст для Telegram
    """
    title = post.get("title", "")
    content = truncate(post.get("content", ""), MAX_CONTENT_LENGTH)
    tag = post.get("tag", "")
    url = post.get("url", "")

    text = f"📢 <b>{title}</b>\n\n{content}"
    if tag:
        text += f"\n\n#{tag}"
    if url:
        text += f"\n\n🔗 <a href=\"{url}\">Источник</a>"

    return text


def build_post_buttons(post: dict) -> Optional[InlineKeyboardMarkup]:
    """
    Формирует inline-кнопки для поста, если есть ссылка.

    Args:
        post (dict): словарь с полем 'url'

    Returns:
        InlineKeyboardMarkup | None: клавиатура с одной кнопкой или None
    """
    url = post.get("url")
    if not url:
        return None

    button = InlineKeyboardButton(text="Читать полностью", url=url)
    return InlineKeyboardMarkup(inline_keyboard=[[button]])
