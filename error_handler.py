"""
error_handler.py

Централизованный обработчик ошибок для проекта.
Содержит функции для логирования ошибок, отправки уведомлений и обработки исключений.
"""

import logging
from central_core.notifications import send_error_notification
import traceback

# Получаем глобальный логгер
logger = logging.getLogger("error_handler")

def handle_error(exception: Exception, module_name: str = "Unknown Module", custom_message: str = "") -> None:
    """
    Централизованная обработка ошибок: логирование и отправка уведомлений.
    
    :param exception: Исключение, которое было поймано.
    :param module_name: Название модуля, в котором произошла ошибка.
    :param custom_message: Дополнительное сообщение для уточнения контекста ошибки.
    """
    try:
        # Логирование ошибки с трассировкой стека
        error_message = f"Ошибка в модуле {module_name}: {str(exception)}\n{traceback.format_exc()}"
        logger.error(f"{custom_message} {error_message}")
        
        # Отправка уведомлений о критичных ошибках
        send_error_notification(exception, module_name)
    except Exception as e:
        # Логирование ошибки в процессе обработки ошибки
        logger.error(f"Ошибка при обработке исключения: {e}")
        # В случае ошибки можно логировать или отправлять уведомление на почту о сбое в системе уведомлений
        # send_email_to_admins(f"Ошибка при обработке исключения: {e}")
