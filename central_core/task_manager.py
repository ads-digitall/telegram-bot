"""
central_core/task_manager.py

Модуль управления задачами. Используется для планирования, регистрации и запуска
функций, которые должны выполняться асинхронно или по расписанию.
В текущей версии реализована заглушка `schedule_task`, которую можно адаптировать
под очередь задач, asyncio, celery или другие системы.
"""

from core.logger import get_logger

logger = get_logger(__name__)


def schedule_task(task_name: str, *args, **kwargs):
    """
    Заглушка для планирования задачи. Пока только логирует вызов.
    
    Args:
        task_name (str): Название задачи.
        *args: Позиционные аргументы задачи.
        **kwargs: Именованные аргументы задачи.
    
    Returns:
        bool: True — задача принята (для совместимости).
    """
    logger.debug(f"Задача запланирована: {task_name} | args={args} | kwargs={kwargs}")
    return True


def add_to_queue(task_callable, *args, **kwargs):
    """
    Заглушка для добавления функции в очередь задач. Здесь можно встроить логику очередей.
    
    Args:
        task_callable (callable): Функция, которую нужно запустить.
        *args: Позиционные аргументы.
        **kwargs: Именованные аргументы.
    """
    logger.debug(f"Добавление задачи в очередь: {task_callable.__name__} | args={args} | kwargs={kwargs}")
    try:
        task_callable(*args, **kwargs)
    except Exception as e:
        logger.error(f"Ошибка при выполнении задачи {task_callable.__name__}: {e}")


__all__ = ["schedule_task", "add_to_queue"]
