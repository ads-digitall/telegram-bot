"""
central_core/launcher.py

Этот модуль инициализирует центральное ядро проекта «Бот-2».
Он обеспечивает корректную настройку окружения, загрузку конфигурации, логгера,
инициализацию базы данных, создание экземпляра центрального ядра (core_manager),
динамическую загрузку внешних модулей и запуск основной логики (например, GUI-интерфейса).
"""

import sys
import os
import asyncio
import importlib

# Добавляем корневую директорию проекта в sys.path для корректного импорта модулей
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Первым делом выполняем проверку конфигурации: наличие и валидация config.env
try:
    from core.config import settings  # settings включает в себя валидацию параметров из config.env
except Exception as e:
    # Если конфигурация не загружается, завершаем работу с сообщением об ошибке
    print(f"Ошибка загрузки конфигурации: {e}")
    sys.exit(1)

# Настройка логгера с обработкой ошибок
try:
    from core.logger import setup_logger, get_logger
    logger = setup_logger()
except Exception as e:
    import logging
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger("fallback_logger")
    logger.error(f"Ошибка инициализации логгера: {e}")
    sys.exit(1)

logger.info("Конфигурация успешно загружена. Запуск центрального ядра...")

# Инициализация базы данных: создаем таблицы, если они ещё не существуют
try:
    from core.database.database import init_db
    asyncio.run(init_db())
    logger.info("Таблицы базы данных успешно созданы (если они ещё не существуют).")
except Exception as e:
    logger.error(f"Ошибка инициализации базы данных: {e}")

# Создание экземпляра центрального ядра
try:
    from central_core.core_manager import initialize_core
    core_manager = initialize_core()
    logger.info("Центральное ядро успешно инициализировано.")
except Exception as e:
    logger.error(f"Ошибка инициализации центрального ядра: {e}")
    sys.exit(1)

# Динамическая загрузка внешних модулей с обработкой ошибок
modules_dir = os.path.join(project_root, "modules")
if os.path.isdir(modules_dir):
    for module_name in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, module_name)
        if os.path.isdir(module_path) and "__init__.py" in os.listdir(module_path):
            try:
                importlib.import_module(f"modules.{module_name}")
                logger.info(f"Модуль '{module_name}' загружен.")
            except Exception as e:
                logger.error(f"Ошибка загрузки модуля '{module_name}': {e}")

logger.info("Запуск основного цикла приложения.")
try:
    asyncio.run(core_manager.run())
except Exception as e:
    logger.error(f"Ошибка выполнения основного цикла приложения: {e}")
