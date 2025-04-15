"""
Модуль подписок.

Обеспечивает единый API для обработки inline callback-запросов, проверки и получения подписок.
Гарантирует отказоустойчивость при импорте компонентов и предоставляет заглушки при их недоступности.
"""

from typing import Any, List
from core.logger import get_logger

logger = get_logger()

# Импорт callback-обработчика
try:
    from modules.subscriptions.callback import handle_subscription_callback
    logger.info("handle_subscription_callback успешно импортирован.")
except Exception as e:
    logger.warning(f"Не удалось импортировать handle_subscription_callback: {e}")

    async def handle_subscription_callback(*args: Any, **kwargs: Any) -> None:
        """
        Заглушка функции обработки callback-запросов при недоступности модуля callback.
        """
        logger.warning("Заглушка: handle_subscription_callback недоступна.")

# Импорт функций из utils
try:
    from modules.subscriptions.utils import is_user_subscribed, get_user_subscriptions
    logger.info("Функции is_user_subscribed и get_user_subscriptions успешно импортированы.")
except Exception as e:
    logger.warning(f"Не удалось импортировать функции из utils: {e}")

    async def is_user_subscribed(user_id: int) -> bool:
        """
        Заглушка проверки подписки при недоступности модуля utils.

        :param user_id: Идентификатор пользователя
        :return: False
        """
        logger.warning("Заглушка: is_user_subscribed недоступна.")
        return False

    async def get_user_subscriptions(user_id: int) -> List[str]:
        """
        Заглушка получения подписок при недоступности модуля utils.

        :param user_id: Идентификатор пользователя
        :return: Пустой список
        """
        logger.warning("Заглушка: get_user_subscriptions недоступна.")
        return []

__all__ = ["handle_subscription_callback", "is_user_subscribed", "get_user_subscriptions"]
