"""
utils.py

Общие вспомогательные функции, используемые в разных модулях проекта.
Включает работу со строками, датами, callback_data и безопасным преобразованием.
"""

import datetime
from typing import Any


def truncate(text: str, max_len: int = 100) -> str:
    """
    Обрезает строку до заданной длины, добавляя "..." при необходимости.

    Args:
        text (str): Исходный текст
        max_len (int): Максимальная длина

    Returns:
        str: Обрезанный текст
    """
    return text if len(text) <= max_len else text[:max_len - 3] + "..."


def format_datetime(dt: datetime.datetime) -> str:
    """
    Форматирует datetime в читабельный вид: "8 апр 2025, 14:20"

    Args:
        dt (datetime): объект даты и времени

    Returns:
        str: Отформатированная строка
    """
    return dt.strftime("%-d %b %Y, %H:%M")


def make_callback_data(prefix: str, *parts: Any) -> str:
    """
    Генерирует безопасную строку callback_data.

    Пример:
        make_callback_data("settings", "lang", "en") → "settings:lang:en"

    Args:
        prefix (str): Префикс (действие или категория)
        *parts (Any): Остальные элементы

    Returns:
        str: Сформированная строка
    """
    return ":".join(map(str, (prefix,) + parts))


def parse_callback_data(data: str, expected_parts: int = 2) -> dict[str, str] | None:
    """
    Разбирает callback_data в словарь. Упрощённая версия, для контролируемых шаблонов.

    Args:
        data (str): строка вида "prefix:action:id"
        expected_parts (int): ожидаемое количество частей (включая prefix)

    Returns:
        dict | None: {'prefix': ..., 'action': ..., 'param': ...}
    """
    try:
        parts = data.split(":")
        if len(parts) < expected_parts:
            return None
        result = {"prefix": parts[0]}
        if expected_parts >= 2:
            result["action"] = parts[1]
        if expected_parts >= 3:
            result["param"] = parts[2]
        return result
    except Exception:
        return None


def safe_int(value: Any, default: int = 0) -> int:
    """
    Преобразует значение в int, возвращая default при ошибке.

    Args:
        value (Any): исходное значение
        default (int): значение по умолчанию

    Returns:
        int: безопасное число
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def list_to_comma_string(items: list[str]) -> str:
    """
    Преобразует список строк в одну строку через запятую.

    Args:
        items (list): список

    Returns:
        str: строка, объединённая через запятую
    """
    return ", ".join(items)
