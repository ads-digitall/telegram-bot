"""
fsm_manager.py

Модуль управления конечными состояниями (FSM) пользователей проекта «Бот-2».

Обеспечивает:
- асинхронное получение, установку и сброс состояния пользователя
- масштабируемую и расширяемую архитектуру FSM
- базовый класс FSMStates (может быть заменён на Pydantic/enum/aiogram.FSM)

Использует in-memory хранилище и asyncio.Lock.
"""

import asyncio
from typing import Dict, Optional
from core.logger import get_logger

# Хранилище состояний пользователей (user_id -> state str)
state_storage: Dict[int, str] = {}
state_lock = asyncio.Lock()

logger = get_logger(__name__)


class FSMStates:
    """
    Базовые состояния. Можно расширять в fsm_config.py или json/yaml.
    """
    INITIAL = "INITIAL"
    SETTINGS_MAIN = "SETTINGS_MAIN"
    SETTINGS_LANGUAGE = "SETTINGS_LANGUAGE"
    SETTINGS_TAGS = "SETTINGS_TAGS"
    SETTINGS_NOTIFICATIONS = "SETTINGS_NOTIFICATIONS"
    FEED_MODE = "FEED_MODE"
    WAITING_INPUT = "WAITING_INPUT"


async def get_state(user_id: int) -> str:
    """
    Получить текущее состояние пользователя.

    Args:
        user_id (int): Идентификатор пользователя

    Returns:
        str: Состояние или FSMStates.INITIAL
    """
    try:
        async with state_lock:
            state = state_storage.get(user_id, FSMStates.INITIAL)
        logger.debug(f"[FSM] Состояние пользователя {user_id}: {state}")
        return state
    except Exception as e:
        logger.error(f"[FSM] Ошибка получения состояния пользователя {user_id}: {e}")
        return FSMStates.INITIAL


async def set_state(user_id: int, state: str) -> None:
    """
    Установить новое состояние пользователю.

    Args:
        user_id (int): Идентификатор пользователя
        state (str): Новое состояние
    """
    try:
        if not isinstance(user_id, int):
            raise ValueError("user_id должен быть int")
        if not isinstance(state, str):
            raise ValueError("state должен быть str")

        async with state_lock:
            state_storage[user_id] = state
        logger.info(f"[FSM] Установлено состояние {state} для пользователя {user_id}")
    except Exception as e:
        logger.error(f"[FSM] Ошибка при установке состояния пользователя {user_id}: {e}")


async def reset_state(user_id: int) -> None:
    """
    Сбросить состояние пользователя до FSMStates.INITIAL.

    Args:
        user_id (int): Идентификатор пользователя
    """
    await set_state(user_id, FSMStates.INITIAL)
    logger.info(f"[FSM] Состояние пользователя {user_id} сброшено до INITIAL")


__all__ = ["get_state", "set_state", "reset_state", "FSMStates"]
