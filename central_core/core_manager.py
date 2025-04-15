import asyncio
from typing import Any
from core.logger import logger
from central_core.task_manager import schedule_task, add_to_queue  # Импорт функций планирования
from modules.monitoring.cleanup_service import CleanupService  # ⏳ Добавлено

class ModuleInterface:
    async def process(self, data: Any) -> Any:
        raise NotImplementedError("Метод process должен быть реализован в модуле.")

class CoreManager:
    def __init__(self):
        # Зарегистрированные модули
        self.modules: dict[str, ModuleInterface] = {}

        # Список активных фоновых задач
        self.active_tasks: list[asyncio.Task] = []

        # ✅ Счётчик ошибок для UI
        self.error_count: int = 0

    def register_module(self, module_name: str, module_api: ModuleInterface):
        """Регистрирует модуль в системе с логированием и обработкой ошибок."""
        logger.info(f"Начало регистрации модуля: {module_name}")
        try:
            self.modules[module_name] = module_api
            logger.info(f"Модуль успешно зарегистрирован: {module_name}")
        except Exception as e:
            self.log_error(f"Ошибка при регистрации модуля {module_name}: {e}")

    def schedule_background_task(self, coro_func, *args, **kwargs):
        """
        Запускает асинхронную задачу и добавляет её в список active_tasks.
        """
        try:
            task = asyncio.create_task(coro_func(*args, **kwargs))
            self.active_tasks.append(task)

            def remove_task(_):
                if task in self.active_tasks:
                    self.active_tasks.remove(task)

            task.add_done_callback(remove_task)
            logger.debug(f"Фоновая задача {coro_func.__name__} запущена.")
            return task
        except Exception as e:
            self.log_error(f"Ошибка запуска фоновой задачи {coro_func}: {e}")

    def increment_error_count(self):
        """Увеличивает внутренний счётчик ошибок."""
        self.error_count += 1
        logger.debug(f"Ошибка зафиксирована. Общее количество: {self.error_count}")

    def log_error(self, message: str):
        """Логирует ошибку и увеличивает счётчик."""
        logger.error(message)
        self.increment_error_count()

    async def run(self):
        """
        Основной цикл работы центрального ядра.
        Здесь можно запускать общую логику приложения, например, интеграцию с GUI или обработку внешних событий.
        """
        logger.info("Запуск основного цикла приложения.")

        # ⏳ Запуск фоновой задачи очистки чатов
        cleanup_service = CleanupService()
        self.schedule_background_task(cleanup_service.run_background_chat_cleanup)

        while True:
            await asyncio.sleep(1)

def initialize_core() -> CoreManager:
    """
    Инициализирует центральное ядро проекта.
    Здесь можно зарегистрировать необходимые модули и выполнить стартовые операции.

    Возвращает:
        CoreManager: Экземпляр центрального ядра.
    """
    logger.info("Инициализация центрального ядра началась.")
    core_manager = CoreManager()

    # Пример регистрации модуля:
    # from modules.example import ExampleModule
    # core_manager.register_module("example", ExampleModule())

    logger.info("Центральное ядро успешно инициализировано.")
    return core_manager
