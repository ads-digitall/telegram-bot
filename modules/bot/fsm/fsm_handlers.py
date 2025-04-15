"""
fsm_handlers.py

Обработчики FSM-сценариев:
- Настройка языка
- Настройка интересов
- Переключение уведомлений

Использует FSMManager и FSMStates из fsm_config.py.
"""

from aiogram import types, Router, F
from core.logger import get_logger
from modules.fsm_manager import set_state, get_state, reset_state
from modules.bot.fsm.fsm_config import ExtendedFSM
from modules.bot.services.settings_service import (
    update_user_language,
    update_user_interests,
    set_user_notifications
)

logger = get_logger(__name__)
router = Router()

# ---------- ЯЗЫК ----------

async def prompt_language(message: types.Message):
    await message.answer("Введите желаемый язык (например, ru, en):")
    await set_state(message.from_user.id, ExtendedFSM.SETTINGS_LANGUAGE_INPUT)

async def set_language_from_input(message: types.Message):
    lang = message.text.strip().lower()
    await update_user_language(message.from_user.id, lang)
    await message.answer(f"Язык обновлён на: {lang}")
    await reset_state(message.from_user.id)

# ---------- ИНТЕРЕСЫ ----------

async def prompt_tags(message: types.Message):
    await message.answer("Введите интересы через запятую (например: спорт, технологии, кино):")
    await set_state(message.from_user.id, ExtendedFSM.SETTINGS_INTERESTS_INPUT)

async def set_tags_from_input(message: types.Message):
    tags = message.text.strip()
    await update_user_interests(message.from_user.id, tags)
    await message.answer(f"Интересы обновлены: {tags}")
    await reset_state(message.from_user.id)

# ---------- УВЕДОМЛЕНИЯ ----------

async def toggle_notifications(message: types.Message):
    await message.answer("Уведомления переключены (для примера).")
    await set_user_notifications(message.from_user.id, True)  # или False — зависит от UI
    await reset_state(message.from_user.id)

# ---------- ГЛОБАЛЬНАЯ FSM-МАРШРУТИЗАЦИЯ ----------

async def process_fsm_input(message: types.Message):
    """
    Глобальный обработчик всех пользовательских сообщений в FSM-состояниях.
    """
    user_id = message.from_user.id
    state = await get_state(user_id)

    if state == ExtendedFSM.SETTINGS_LANGUAGE_INPUT:
        await set_language_from_input(message)
    elif state == ExtendedFSM.SETTINGS_INTERESTS_INPUT:
        await set_tags_from_input(message)
    else:
        await message.answer("Неожиданный ввод. Попробуйте снова или используйте /start.")
        await reset_state(user_id)

# ---------- РЕГИСТРАЦИЯ ----------

@router.message(F.text == "🌐 Язык")
async def handle_prompt_language(message: types.Message):
    await prompt_language(message)

@router.message(F.text == "📋 Интересы")
async def handle_prompt_tags(message: types.Message):
    await prompt_tags(message)

@router.message(F.text == "🔔 Уведомления")
async def handle_toggle_notifications(message: types.Message):
    await toggle_notifications(message)

@router.message()
async def handle_process_fsm_input(message: types.Message):
    await process_fsm_input(message)

def register_handler(dp):
    dp.include_router(router)
