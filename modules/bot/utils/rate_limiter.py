# modules/bot/utils/rate_limiter.py

"""
Модуль ограничения частоты запросов к Telegram API.

Обеспечивает соблюдение лимита в 29 запросов в секунду на одного бота,
чтобы избежать ошибок 429 (Too Many Requests).
"""

import asyncio
import time
import logging  # ✅ Добавлен логгер

logger = logging.getLogger(__name__)

class TelegramRateLimiter:
    """
    Класс для ограничения количества запросов в секунду.

    Использование:
        rate_limiter = TelegramRateLimiter()
        await rate_limiter.throttle()
        await bot.send_message(...)
    """

    def __init__(self, max_rps: int = 29):
        """
        Инициализация ограничителя.

        :param max_rps: Максимальное количество запросов в секунду.
        """
        self._interval = 1.0 / max_rps
        self._last_time = time.monotonic()

    async def throttle(self):
        """
        Пауза между запросами, чтобы не превысить лимит.
        """
        now = time.monotonic()
        wait_time = self._interval - (now - self._last_time)
        if wait_time > 0:
            if wait_time < self._interval * 0.2:  # менее 20% запаса
                logger.warning(f"⚠️ Почти превышен лимит запросов! Ждём {wait_time:.4f} сек.")
            await asyncio.sleep(wait_time)
        self._last_time = time.monotonic()
