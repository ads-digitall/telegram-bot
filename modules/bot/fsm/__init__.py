"""
fsm/__init__.py

Регистрация всех FSM-компонентов:
- шагов (fsm_handlers)
- утилит (/cancel, /state)

Подключается один раз в BotModule, чтобы FSM работал в проекте.
"""

from aiogram import Dispatcher
from core.logger import get_logger

from modules.bot.fsm.fsm_handlers import register_fsm_handlers
from modules.bot.fsm.fsm_utils import register_fsm_utils

logger = get_logger(__name__)

def register_fsm(dp: Dispatcher):
    """
    Центральная точка подключения всех FSM-механизмов.
    """
    try:
        register_fsm_handlers(dp)
        logger.info("FSM-шаги зарегистрированы.")
    except Exception as e:
        logger.error(f"Ошибка регистрации FSM-шагов: {e}")

    try:
        register_fsm_utils(dp)
        logger.info("FSM-утилиты зарегистрированы.")
    except Exception as e:
        logger.error(f"Ошибка регистрации FSM-утилит: {e}")
