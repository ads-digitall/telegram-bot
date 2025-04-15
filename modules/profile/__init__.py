import asyncio
import threading
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from modules.profile import router
from core.logger import get_logger
from modules.profile.config import TELEGRAM_PROFILE_TOKEN

from aiogram.client.default import DefaultBotProperties  # ✅ добавлено

logger = get_logger(__name__)


def register(core_manager):
    thread = threading.Thread(target=start_profile_bot, daemon=True)
    thread.start()
    logger.info("✅ Бот 'Профиль' запущен в отдельном потоке.")


def start_profile_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    storage = MemoryStorage()
    bot = Bot(  # ✅ обновлено
        token=TELEGRAM_PROFILE_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher(storage=storage)
    dp.include_router(router.router)

    try:
        logger.info("🚀 Профиль-бот: запуск поллинга")
        loop.run_until_complete(dp.start_polling(bot))
    except Exception as e:
        logger.exception(f"❌ Ошибка запуска бота 'Профиль': {e}")
