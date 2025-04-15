"""
central_core/notifications.py

Модуль уведомлений для проекта.
Содержит функции форматирования алертов и отправки уведомлений.
Эти функции могут использоваться для отправки сообщений в GUI или на другие каналы оповещений.
Добавлена отправка уведомлений о критичных ошибках.
"""

import logging
from smtplib import SMTPException
import traceback

logger = logging.getLogger("notifications")

def format_alert(alert_data: dict) -> str:
    """
    Форматирует данные алерта для отправки уведомления.

    Параметры:
        alert_data (dict): Словарь с данными алерта. Ожидается наличие следующих ключей:
            - "module": имя модуля или компонента.
            - "error": описание ошибки или сбоя.
            - "info" (опционально): дополнительные сведения или контекст.

    Возвращает:
        str: Отформатированное строковое сообщение с информацией об алерте.
    """
    module = alert_data.get("module", "Unknown module")
    error = alert_data.get("error", "No error details")
    info = alert_data.get("info", "")
    # Формирование сообщения. Можно добавить более сложное форматирование по необходимости.
    message = f"[ALERT] Module: {module}. Error: {error}."
    if info:
        message += f" Details: {info}"
    return message

def send_notification(message: str) -> None:
    """
    Отправляет уведомление. В данном примере отправка реализована через логирование.
    Этот метод можно адаптировать для интеграции с GUI, email или другими каналами оповещений.

    Параметры:
        message (str): Сообщение, которое будет отправлено.
    """
    try:
        # Пример реализации через логгер:
        logger.info(f"Отправка уведомления: {message}")
        
        # Пример отправки на email (можно адаптировать для других каналов):
        # send_email_to_admins(message)
        # Если потребуется отправка уведомлений в GUI, здесь можно вызвать соответствующий метод:
        # from central_core.gui import gui_manager
        # gui_manager.update_alert_widget(message)
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления: {e}")
        try:
            # Дополнительно можно отправить сообщение через другие каналы
            # например, оповестить администраторов о проблемах с уведомлениями
            # send_email_to_admins(f"Ошибка при отправке уведомления: {e}")
            pass
        except Exception as inner_exception:
            logger.error(f"Ошибка при попытке отправить уведомление администратору: {inner_exception}")

def log_notification(message: str) -> None:
    """
    Дополнительная функция для сохранения истории уведомлений в лог.
    Может быть полезна для аудита или отладки.

    Параметры:
        message (str): Сообщение уведомления.
    """
    logger.debug(f"Лог уведомления: {message}")

def send_error_notification(error: Exception, module_name: str = "Unknown") -> None:
    """
    Отправка уведомлений о критичных ошибках. Может отправляться на почту или в GUI.

    Параметры:
        error (Exception): Исключение, которое нужно уведомить.
        module_name (str): Имя модуля, где произошла ошибка.
    """
    try:
        error_message = format_alert({
            "module": module_name,
            "error": str(error),
            "info": traceback.format_exc()  # Трассировка стека
        })
        send_notification(error_message)
        logger.error(f"Отправлено уведомление о критичной ошибке: {error_message}")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления о критичной ошибке: {e}")
        # В случае ошибки можно логировать или отправлять уведомление на почту о сбое в системе уведомлений
        # send_email_to_admins(f"Ошибка при отправке уведомления о критичной ошибке: {e}")
