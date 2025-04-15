"""
Главный исполняемый файл проекта «Бот-2».
Регистрирует модули, запускает бот-поллинг в отдельном потоке и GUI в главном потоке.
При этом все асинхронные операции с базой данных выполняются в рамках event loop,
созданного в потоке бот-поллинга.
"""

import sys
import os
import importlib
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Добавление корневой директории проекта в sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Загрузка настроек и логгера с обработкой ошибок
try:
    from core.config import settings
    from core.logger import get_logger
    logger = get_logger()
except Exception as e:
    import logging
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger("fallback_logger")
    logger.error(f"Ошибка инициализации конфигурации или логгера: {e}")
    sys.exit(1)

# Инициализация центрального ядра
try:
    from central_core.core_manager import initialize_core
    core_manager = initialize_core()
    logger.info("Центральное ядро успешно инициализировано.")
except Exception as e:
    logger.error(f"Ошибка инициализации центрального ядра: {e}")
    sys.exit(1)

# Динамическая регистрация модулей
modules_dir = os.path.join(os.path.dirname(__file__), "modules")
if os.path.isdir(modules_dir):
    for module_name in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, module_name)
        if os.path.isdir(module_path) and os.path.exists(os.path.join(module_path, "__init__.py")):
            try:
                mod = importlib.import_module(f"modules.{module_name}")
                logger.info(f"Модуль {module_name} успешно загружен.")
                if hasattr(mod, "register"):
                    mod.register(core_manager)
                    logger.info(f"Модуль {module_name} успешно зарегистрирован.")
            except Exception as e:
                logger.warning(f"Не удалось загрузить модуль {module_name}: {e}")

def start_bot_polling():
    """
    Запускает поллинг Telegram‑бота в отдельном потоке.
    В этом потоке создается свой event loop, и все асинхронные операции (включая операции с базой данных)
    выполняются в рамках этого цикла, что предотвращает ошибки передачи Future между циклами.
    """
    try:
        from modules.bot import bot_module_instance
        if not bot_module_instance:
            logger.error("Глобальный объект бот-модуля не инициализирован, бот не запущен.")
            return
        asyncio.run(bot_module_instance.start())
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

if __name__ == '__main__':
    # Запуск бота в отдельном потоке.
    bot_thread = threading.Thread(target=start_bot_polling, daemon=True)
    bot_thread.start()
    logger.info("Поллинг Telegram‑бота запущен в отдельном потоке.")

    # Запуск GUI в главном потоке.
    # Tkinter требует работы именно в главном потоке.
    try:
        from central_core.gui.main import start_gui
        start_gui(core_manager)
    except Exception as e:
        logger.error(f"Ошибка запуска GUI: {e}")
        input("Произошла ошибка при запуске GUI. Нажмите Enter для выхода...")
        sys.exit(1)
