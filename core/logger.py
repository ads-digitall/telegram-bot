"""
Модуль логирования для проекта Бот-2.

Обеспечивает глобальный доступ к конфигурированным логгерам через функции get_logger() и setup_logger().
Реализована поддержка разных уровней логирования для отдельных модулей,
а также ротация логов через RotatingFileHandler.
Добавлена улучшенная обработка ошибок.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
import traceback

# Конфигурация логирования: уровни для отдельных модулей и параметры ротации логов.
LOGGING_CONFIG = {
    "default_level": logging.DEBUG,
    "module_levels": {  # Уровни логирования можно задавать для отдельных модулей
        "bot": logging.DEBUG,
        # Пример: "module_a": logging.INFO, "module_b": logging.WARNING
    },
    "console_level": logging.DEBUG,
    "file_level": logging.DEBUG,
    "maxBytes": 5_000_000,    # Максимальный размер файла лога в байтах
    "backupCount": 3,         # Количество резервных копий лога
}

# Словарь для кеширования логгеров по именам.
_loggers = {}

def get_logger(name: str = "bot") -> logging.Logger:
    """
    Возвращает настроенный логгер для указанного модуля.
    Если логгер с данным именем уже создан, возвращает его из кеша.
    
    :param name: Имя логгера (например, имя модуля).
    :return: Экземпляр logging.Logger с заданным уровнем логирования и обработчиками.
    """
    if name in _loggers:
        return _loggers[name]

    # Определяем уровень логирования для данного модуля.
    module_level = LOGGING_CONFIG["module_levels"].get(name, LOGGING_CONFIG["default_level"])

    logger = logging.getLogger(name)
    logger.setLevel(module_level)

    # Формат логирования: время, уровень, имя логгера и сообщение
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Обработчик для консоли (StreamHandler)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOGGING_CONFIG["console_level"])
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Обработчик для файла (RotatingFileHandler) для общего лога
    log_dir = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "bot.log")
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=LOGGING_CONFIG["maxBytes"],
        backupCount=LOGGING_CONFIG["backupCount"],
        encoding="utf-8"
    )
    file_handler.setLevel(LOGGING_CONFIG["file_level"])
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Обработчик для файла ошибок (errors.log)
    error_log_file = os.path.join(log_dir, "bot_error.log")
    error_file_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=LOGGING_CONFIG["maxBytes"],
        backupCount=LOGGING_CONFIG["backupCount"],
        encoding="utf-8"
    )
    error_file_handler.setLevel(logging.ERROR)  # Только ошибки
    error_file_handler.setFormatter(formatter)
    logger.addHandler(error_file_handler)

    logger.debug(f"Logger '{name}' инициализирован с уровнем {logging.getLevelName(module_level)}.")

    _loggers[name] = logger
    return logger

def setup_logger() -> logging.Logger:
    """
    Функция-обертка для инициализации логгера по умолчанию с именем 'bot'.
    
    :return: Настроенный логгер.
    """
    return get_logger("bot")

def log_error_with_traceback(exception: Exception, custom_message: str = ""):
    """
    Логирует ошибку с трассировкой стека.
    
    :param exception: Исключение, которое было поймано.
    :param custom_message: Дополнительное сообщение, которое будет добавлено к ошибке.
    """
    logger = get_logger("bot")
    traceback_str = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
    error_message = f"{custom_message}\n{traceback_str}"
    logger.error(error_message)

# Инициализируем основной логгер для проекта
logger = get_logger("bot")

__all__ = ["get_logger", "setup_logger", "logger", "log_error_with_traceback"]
