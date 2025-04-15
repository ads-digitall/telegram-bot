from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from core import get_settings

_bot_instance: Bot | None = None

def get_bot() -> Bot:
    global _bot_instance
    if _bot_instance is None:
        settings = get_settings()
        _bot_instance = Bot(
            token=settings.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode="HTML")
        )
    return _bot_instance
