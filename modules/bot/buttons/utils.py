"""
utils.py

Вспомогательные функции для формирования inline-кнопок Telegram.
Используется во всех разделах кнопочного интерфейса (меню, лента, настройки и т.п.).
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List


def build_inline_buttons(data: List[dict], row_width: int = 1) -> InlineKeyboardMarkup:
    """
    Создаёт InlineKeyboardMarkup на основе переданных данных.

    Args:
        data (list[dict]): Список словарей с ключами 'text' и 'callback_data'.
        row_width (int): Количество кнопок в строке.

    Returns:
        InlineKeyboardMarkup: Объект Telegram-клавиатуры.
    """
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    buttons = [
        InlineKeyboardButton(text=item["text"], callback_data=item["callback_data"])
        for item in data
    ]
    keyboard.inline_keyboard = [buttons[i:i + row_width] for i in range(0, len(buttons), row_width)]
    return keyboard
