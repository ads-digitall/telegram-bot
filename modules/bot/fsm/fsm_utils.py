"""
fsm_utils.py

Утилиты для работы с FSM (конечными автоматами состояний).
Позволяет:
- сбрасывать состояние (/cancel)
- просматривать текущее состояние (/state)
"""

from aiogram import types, Router, F
from core.logger import get_logger
from modules.fsm_manager import get_state, reset_state

logger = get_logger(__name__)
router = Router()

async def cancel_fsm(message: types.Message):
    """
    Команда /cancel — сбрасывает состояние пользователя.
    """
    await reset_state(message.from_user.id)
    await message.answer("❌ Вы вышли из режима ввода.")
    logger.info(f"Пользователь {message.from_user.id} отменил FSM.")

async def show_fsm_state(message: types.Message):
    """
    Команда /state — показывает текущее состояние FSM пользователя.
    """
    state = await get_state(message.from_user.id)
    await message.answer(f"ℹ️ Текущее состояние FSM: {state}")
    logger.info(f"Пользователь {message.from_user.id} запросил текущее состояние: {state}")

@router.message(F.text == "/cancel")
async def handle_cancel_fsm(message: types.Message):
    await cancel_fsm(message)

@router.message(F.text == "/state")
async def handle_show_fsm_state(message: types.Message):
    await show_fsm_state(message)

def register_handler(dp):
    dp.include_router(router)
