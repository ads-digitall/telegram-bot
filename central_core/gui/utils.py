"""
central_core/gui/utils.py

Модуль утилит для форматирования и подготовки данных для отображения в GUI.
Содержит функции для преобразования метрик, подготовки списков модулей и генерации сообщений об ошибках.
Добавлена функция для отображения ошибок в интерфейсе.
"""

def format_metrics(metrics: dict) -> str:
    """
    Форматирует словарь метрик в строку для отображения.
    
    Args:
        metrics (dict): Словарь с метриками, где ключ – имя параметра, а значение – его текущее состояние.
        
    Returns:
        str: Отформатированная строка, например:
             "active_tasks: 5 | queue_size: 10 | registered_modules: 3 | error_count: 0 | memory_usage: 25"
    """
    formatted = [f"{key}: {value}" for key, value in metrics.items()]
    return " | ".join(formatted)

def prepare_module_list(module_names: list) -> str:
    """
    Подготавливает список модулей для отображения в виде строки.
    
    Args:
        module_names (list): Список имён модулей (строк).
        
    Returns:
        str: Строка с именами модулей, разделёнными запятыми.
    """
    return ", ".join(module_names)

def format_error_message(error: Exception) -> str:
    """
    Форматирует сообщение об ошибке для удобного отображения в интерфейсе.
    
    Args:
        error (Exception): Объект исключения с информацией об ошибке.
        
    Returns:
        str: Строка с подробным описанием ошибки.
    """
    return f"Ошибка: {str(error)}"

def prepare_status_message(metrics: dict) -> str:
    """
    Объединяет отформатированные метрики в единое сообщение для отображения в статус-баре.
    
    Args:
        metrics (dict): Словарь с метриками.
        
    Returns:
        str: Сообщение о состоянии системы.
    """
    formatted_metrics = format_metrics(metrics)
    return f"Состояние системы: {formatted_metrics}"

def display_error_message(gui, error_message: str):
    """
    Отображает сообщение об ошибке в интерфейсе.
    
    Args:
        gui: Объект GUI или контроллер, через который можно обновлять интерфейс.
        error_message (str): Сообщение об ошибке, которое нужно отобразить.
        
    Пример использования:
        display_error_message(main_gui, "Произошла ошибка при обновлении данных.")
    """
    try:
        # Проверяем наличие метода для отображения ошибок в интерфейсе
        if hasattr(gui, "display_error"):
            gui.display_error(error_message)
        else:
            # Если метод не найден, логируем ошибку
            logger.error(f"Ошибка при отображении сообщения в интерфейсе: {error_message}")
    except Exception as e:
        # Логируем ошибку при попытке вывести сообщение об ошибке в GUI
        logger.error(f"Ошибка при выводе ошибки в интерфейс: {e}")
