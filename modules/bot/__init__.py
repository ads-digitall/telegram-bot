"""
modules.bot

Модуль бота для проекта «Бот-2».
"""

import pkgutil
import importlib
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

from core.logger import get_logger
from core.config import settings
from .activity_middleware import ActivityMiddleware

logger = get_logger(__name__)

bot = None
bot_module_instance = None


def autodiscover_handlers(dp: Dispatcher):
    import modules.bot.handlers
    for finder, name, ispkg in pkgutil.iter_modules(modules.bot.handlers.__path__):
        full_module_name = f"modules.bot.handlers.{name}"
        try:
            module = importlib.import_module(full_module_name)
            logger.info(f"Импортирован обработчик: {full_module_name}")
            if hasattr(module, "register_handler"):
                logger.debug(f"Подключение register_handler из {full_module_name}")
                module.register_handler(dp)
                logger.info(f"Обработчик {full_module_name} зарегистрирован.")
            else:
                logger.warning(f"{full_module_name} не содержит register_handler(dp)")
        except Exception as e:
            logger.error(f"Ошибка импорта обработчика {full_module_name}: {e}")


class BotModule:
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=self.token, default=DefaultBotProperties(parse_mode="HTML"))
        self.dp = Dispatcher(storage=MemoryStorage())

        # 🆕 Middleware для логирования активности
        self.dp.message.middleware(ActivityMiddleware())
        self.dp.callback_query.middleware(ActivityMiddleware())

        self.register_handlers()

    def register_handlers(self):
        logger.info("Регистрация всех Telegram-обработчиков...")
        autodiscover_handlers(self.dp)

    async def start(self):
        logger.info("Запуск поллинга Telegram‑бота.")
        await self.dp.start_polling(self.bot)

    async def process(self, data):
        logger.info(f"BotModule обрабатывает данные: {data}")
        return "Ответ от бота"


def register(core_manager):
    global bot, bot_module_instance
    bot_token = settings.TELEGRAM_TOKEN
    bot_module = BotModule(bot_token)
    core_manager.register_module("bot", bot_module)
    logger.info("Модуль bot успешно зарегистрирован.")
    bot = bot_module.bot
    bot_module_instance = bot_module


def get_bot():
    global bot, bot_module_instance
    if bot is None and bot_module_instance is not None:
        bot = bot_module_instance.bot
    return bot


__all__ = ["register", "BotModule", "bot", "bot_module_instance", "get_bot"]
