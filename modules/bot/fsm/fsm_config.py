"""
fsm_config.py

Централизованное описание состояний (FSM) для Telegram-бота.
Расширяет базовый класс FSMStates из fsm_manager.
Используется для обработки многошаговых сценариев: настройки, профили, подписка и т.д.
"""

from modules.fsm_manager import FSMStates

class ExtendedFSM(FSMStates):
    """
    Дополнительные состояния для многошаговых процессов.
    Наследуется от FSMStates и расширяет его.
    """

    # Настройки
    SETTINGS_MENU = "SETTINGS_MENU"
    SETTINGS_LANGUAGE_INPUT = "SETTINGS_LANGUAGE_INPUT"
    SETTINGS_INTERESTS_INPUT = "SETTINGS_INTERESTS_INPUT"
    SETTINGS_NOTIFICATIONS_TOGGLE = "SETTINGS_NOTIFICATIONS_TOGGLE"

    # Лента / Feed
    FEED_TYPE_SELECT = "FEED_TYPE_SELECT"
    FEED_TAG_FILTERING = "FEED_TAG_FILTERING"

    # Регистрация
    REGISTRATION_STEP_1 = "REGISTRATION_STEP_1"
    REGISTRATION_STEP_2 = "REGISTRATION_STEP_2"
    REGISTRATION_DONE = "REGISTRATION_DONE"

    # Рассылка / опросы
    SURVEY_IN_PROGRESS = "SURVEY_IN_PROGRESS"
    SURVEY_WAITING_ANSWER = "SURVEY_WAITING_ANSWER"

    # Пример произвольного пользовательского FSM
    CUSTOM_FLOW_STEP_1 = "CUSTOM_FLOW_STEP_1"
    CUSTOM_FLOW_STEP_2 = "CUSTOM_FLOW_STEP_2"
