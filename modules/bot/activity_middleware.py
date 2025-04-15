from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable, Union
from core.logger import get_logger
from modules.bot.services import post_cache_service  # ✅ заменили redis

logger = get_logger(__name__)

class ActivityMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        try:
            user = event.from_user
            if user:
                await self.update_last_action(user.id)
        except Exception as e:
            logger.error(f"Ошибка в ActivityMiddleware: {e}")
        return await handler(event, data)

    async def update_last_action(self, user_id: int) -> None:
        try:
            post_cache_service.update_activity(user_id)  # ✅ сохраняем активность в post_cache
        except Exception as e:
            logger.error(f"Ошибка при обновлении активности для пользователя {user_id}: {e}")
