"""
main.py

Графический интерфейс центрального ядра проекта «Бот-2».
Реализует отображение логов, состояния модулей и метрик в реальном времени с использованием Tkinter.
"""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from central_core.gui.widgets import LogPanel, StatusBar, ModuleListWidget, LogWindow  # Импорт нового виджета
from central_core.gui.database_interface import create_database_window  # Новый модуль для работы с базой
from central_core.gui.events import on_button_click  # Импорт обработчиков событий
from core.logger import get_logger

logger = get_logger()

def start_gui(core_manager) -> None:
    """
    Запускает главный GUI интерфейс приложения.
    Интерфейс включает панель логов, статус-бар, список модулей и кнопку для открытия административного окна базы данных.
    
    :param core_manager: Экземпляр центрального ядра, содержащий метрики и список модулей.
    """
    root = tk.Tk()
    root.title("Центральное ядро Bot-2")

    # Панель логов
    log_panel = LogPanel(root)
    log_panel.pack(fill=tk.BOTH, expand=True)

    # Статус-бар
    status_bar = StatusBar(root)
    status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    # Список модулей
    module_list = ModuleListWidget(root)
    module_list.pack(fill=tk.X, side=tk.LEFT)

    # Панель управления
    control_frame = tk.Frame(root)
    control_frame.pack(fill=tk.X)

    start_btn = tk.Button(
        control_frame,
        text="Запустить систему",
        command=lambda: on_button_click(log_panel, "Система запущена")
    )
    stop_btn = tk.Button(
        control_frame,
        text="Остановить систему",
        command=lambda: on_button_click(log_panel, "Система остановлена")
    )
    refresh_btn = tk.Button(
        control_frame,
        text="Обновить данные",
        command=lambda: on_button_click(log_panel, "Обновление метрик...")
    )
    db_btn = tk.Button(
        control_frame,
        text="База данных",
        command=create_database_window,
        width=20
    )
    
    # Кнопка для открытия окна с логами
    log_btn = tk.Button(
        control_frame,
        text="Показать логи ошибок",
        command=lambda: LogWindow(root)  # Открытие окна с логами
    )

    # Располагаем кнопки в одном ряду с отступами
    start_btn.pack(side=tk.LEFT, padx=5, pady=5)
    stop_btn.pack(side=tk.LEFT, padx=5, pady=5)
    refresh_btn.pack(side=tk.LEFT, padx=5, pady=5)
    db_btn.pack(side=tk.LEFT, padx=5, pady=5)
    log_btn.pack(side=tk.LEFT, padx=5, pady=5)  # Добавлена кнопка для открытия окна с логами

    def update_ui() -> None:
        """
        Обновляет интерфейс: статус-бар и список модулей.
        Использует Tkinter.after() для планирования следующего обновления.
        """
        try:
            logger.info("Обновление UI начато.")
            metrics = {
                "active_tasks": core_manager.active_tasks,
                "queue_size": core_manager.queue.qsize() if hasattr(core_manager, "queue") else 0,
                "registered_modules": len(core_manager.modules),
                "error_count": core_manager.error_count,
            }

            if isinstance(metrics, dict):
                status_bar.update_status(metrics)
            else:
                logger.warning("Некорректный формат метрик: ожидался dict")

            module_names = list(core_manager.modules.keys())
            if isinstance(module_names, list) and all(isinstance(m, str) for m in module_names):
                module_list.update_list(module_names)
            else:
                logger.warning("Некорректный формат списка модулей")

            logger.info("Обновление UI завершено.")
        except Exception as e:
            logger.error(f"Ошибка обновления UI: {e}")
        root.after(10000, update_ui)

    update_ui()
    root.mainloop()
