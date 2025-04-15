"""
delivery.py

Модуль асинхронной доставки новостных репостов пользователям Telegram.
Отвечает за отправку сообщений и фиксацию событий в базе.
Форматирование контента вынесено в message_builder.py.
Добавлена обработка ошибок при отправке сообщений с централизованной обработкой ошибок.
"""

import asyncio
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from typing import List, Optional
from core.logger import get_logger
from core.database import get_database
from core.database.crud import get_user, update_user
from error_handler import handle_error  # Импортируем централизованный обработчик ошибок

from modules.reposts.message_builder import build_post_text, build_post_buttons

logger = get_logger()

bot: Bot  # должен быть установлен извне при инициализации


async def log_repost_event(user_id: int) -> None:
    """
    Фиксирует событие репоста в базе данных, увеличивая счётчик пользователя.
    """
    try:
        async for db in get_database():
            user = await get_user(db, user_id)
            if user:
                current_count = getattr(user, "repost_count", 0) or 0
                await update_user(db, user_id, {"repost_count": current_count + 1})
                logger.debug(f"Репост-счётчик обновлён: user_id={user_id}, count={current_count + 1}")
            break
    except Exception as e:
        logger.error(f"Ошибка при логировании репоста для user_id={user_id}: {e}")
        handle_error(e, "DeliveryModule", f"Ошибка при логировании репоста для user_id={user_id}")


async def send_repost(user_id: int, post: dict, max_retries: int = 3) -> bool:
    """
    Отправляет пользователю одно сообщение (репост) с текстом и кнопками.

    Args:
        user_id (int): ID пользователя
        post (dict): данные поста (title, content, tag, url)
        max_retries (int): число повторных попыток при ошибках

    Returns:
        bool: успешно ли отправлено
    """
    text = build_post_text(post)
    buttons: Optional[InlineKeyboardMarkup] = build_post_buttons(post)

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Отправка поста пользователю {user_id}, попытка {attempt}")
            await bot.send_message(chat_id=user_id, text=text, reply_markup=buttons, parse_mode="HTML")
            await log_repost_event(user_id)
            logger.info(f"Пост успешно отправлен пользователю {user_id}. Попытка {attempt}.")
            return True
        except Exception as e:
            logger.error(f"Ошибка при отправке поста пользователю {user_id} (попытка {attempt}): {e}")
            handle_error(e, "DeliveryModule", f"Ошибка при отправке поста пользователю {user_id} (попытка {attempt})")
            if attempt < max_retries:
                logger.info(f"Попытка {attempt} не удалась, повтор через {2 ** attempt} секунд.")
                await asyncio.sleep(2 ** attempt)  # экспоненциальная задержка
            else:
                logger.error(f"Не удалось отправить пост пользователю {user_id} после {max_retries} попыток.")
                return False


async def send_reposts(user_id: int, posts: List[dict]) -> List[bool]:
    """
    Отправляет список постов пользователю.

    Args:
        user_id (int): ID пользователя
        posts (List[dict]): список постов (словари)

    Returns:
        List[bool]: список результатов отправки
    """
    logger.info(f"Начало отправки {len(posts)} постов пользователю {user_id}")
    results = []
    for post in posts:
        result = await send_repost(user_id, post)
        results.append(result)
    logger.info(f"Завершена отправка постов пользователю {user_id}")
    return results


__all__ = ["send_repost", "send_reposts"]
