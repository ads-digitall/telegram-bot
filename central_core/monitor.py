"""
monitor.py

Модуль мониторинга для центрального ядра проекта «Бот-2».
Периодически собирает метрики, логирует их, проверяет пороговые значения и работает устойчиво даже при ошибках.
При обнаружении превышения пороговых значений вызываются функции из модуля уведомлений.
"""

import asyncio
import psutil
from datetime import datetime
from core.logger import logger
from central_core.core_manager import CoreManager
from central_core.notifications import format_alert, send_notification

# Пороговые значения для мониторинга
THRESHOLDS = {
    "queue_size": 100,
    "active_tasks": 500,
    "error_count": 50,
}

def get_metrics(core_manager: CoreManager) -> dict:
    """
    Получает текущие метрики состояния системы.

    Args:
        core_manager (CoreManager): Менеджер задач центрального ядра.

    Returns:
        dict: Метрики, включая количество задач, ошибок, зарегистрированных модулей и использование памяти.
    """
    memory = psutil.virtual_memory()
    return {
        "queue_size": core_manager.queue.qsize() if hasattr(core_manager, "queue") else 0,
        "active_tasks": getattr(core_manager, "active_tasks", 0),
        "registered_modules": len(core_manager.modules),
        "error_count": getattr(core_manager, "error_count", 0),
        "memory_usage": memory.percent,
    }

def log_metrics(metrics: dict) -> None:
    """
    Логирует текущие метрики.

    Args:
        metrics (dict): Словарь с метриками.
    """
    logger.info(f"[{datetime.now()}] Метрики: {metrics}")

def check_thresholds(metrics: dict) -> None:
    """
    Проверяет превышение пороговых значений по ключевым метрикам.
    При превышении вызывается функция уведомления из модуля notifications.

    Args:
        metrics (dict): Словарь с метриками.
    """
    for key, value in metrics.items():
        if key in THRESHOLDS and value > THRESHOLDS[key]:
            alert_data = {
                "module": "monitor",
                "error": f"Порог превышен по '{key}': {value} > {THRESHOLDS[key]}",
                "info": f"Текущие метрики: {metrics}"
            }
            alert_message = format_alert(alert_data)
            send_notification(alert_message)
            # Дополнительно можно логировать предупреждение
            logger.warning(alert_message)

async def monitor_loop(core_manager: CoreManager, interval: int = 60):
    """
    Асинхронный бесконечный цикл мониторинга.

    Args:
        core_manager (CoreManager): Менеджер задач.
        interval (int): Интервал между итерациями мониторинга (в секундах).
    """
    while True:
        start_time = datetime.now()
        try:
            logger.info("Начало итерации мониторинга.")
            metrics = get_metrics(core_manager)
            log_metrics(metrics)
            check_thresholds(metrics)
        except Exception as e:
            logger.error(f"Ошибка мониторинга: {e}")
        finally:
            end_time = datetime.now()
            iteration_time = (end_time - start_time).total_seconds()
            logger.info(f"Итерация мониторинга завершена. Время выполнения: {iteration_time:.2f} сек.")
            await asyncio.sleep(interval)

def start_monitoring(core_manager: CoreManager) -> None:
    """
    Запускает задачу мониторинга в фоне.

    Args:
        core_manager (CoreManager): Менеджер задач.
    """
    asyncio.create_task(monitor_loop(core_manager))
