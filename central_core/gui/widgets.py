"""
widgets.py

Компоненты графического интерфейса (виджеты) для проекта «Бот-2».
Содержит панели для логов, метрик и списка модулей с валидацией, логированием и устойчивой обработкой данных.
Логика подготовки/форматирования данных вынесена в модуль central_core/gui/utils.py.
"""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from typing import Any
import os  # Добавляем импорт os
from core.logger import get_logger
from central_core.gui.utils import prepare_status_message  # Импорт функции для форматирования состояния

logger = get_logger()

class LogWindow(tk.Toplevel):
    """
    Окно для отображения логов ошибок в интерфейсе.
    """

    def __init__(self, parent: tk.Tk, log_file="bot_error.log"):
        super().__init__(parent)
        self.title("Логи ошибок")
        self.geometry("600x400")
        
        self.log_file = log_file
        
        # Создаем компонент прокручиваемого текста для отображения логов
        self.log_area = ScrolledText(self, wrap=tk.WORD, width=80, height=20)
        self.log_area.pack(padx=10, pady=10)
        
        # Загружаем логи
        self.load_logs()
        
        # Обновляем логи через регулярный интервал
        self.after(5000, self.update_logs)
    
    def load_logs(self):
        """Загружает последние логи из файла"""
        if os.path.exists(self.log_file):  # Теперь os импортирован
            with open(self.log_file, "r", encoding="utf-8") as f:
                logs = f.readlines()
                # Отображаем последние 100 строк
                for line in logs[-100:]:
                    self.log_area.insert(tk.END, line)
                self.log_area.yview(tk.END)
    
    def update_logs(self):
        """Обновляет логи в реальном времени"""
        self.log_area.delete(1.0, tk.END)  # Очищаем область
        self.load_logs()  # Загружаем новые логи
        self.after(5000, self.update_logs)  # Повторяем обновление каждые 5 секунд

class LogPanel(tk.Frame):
    """
    Панель для отображения логов в интерфейсе.
    """

    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.text_widget = ScrolledText(self, height=15, state='disabled')
        self.text_widget.pack(fill=tk.BOTH, expand=True)

    def append_log(self, message: str) -> None:
        """
        Добавляет строку в лог-панель.

        Args:
            message (str): Сообщение для отображения.
        """
        try:
            if not isinstance(message, str):
                raise ValueError("Ожидалась строка для логирования")

            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, message + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.see(tk.END)
            logger.info("LogPanel обновлён")
        except Exception as e:
            logger.error(f"Ошибка в LogPanel.append_log: {e}")

    def clear(self) -> None:
        """
        Очищает содержимое лог-панели.
        """
        try:
            self.text_widget.configure(state='normal')
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.configure(state='disabled')
        except Exception as e:
            logger.error(f"Ошибка в LogPanel.clear: {e}")

class StatusBar(tk.Frame):
    """
    Строка состояния, отображающая метрики системы.
    """

    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.label = tk.Label(self, text="Статус: Инициализация...", anchor="w")
        self.label.pack(fill=tk.X)

    def update_status(self, metrics: dict[str, Any]) -> None:
        """
        Обновляет строку состояния на основе метрик.
        Форматирование метрик вынесено в модуль утилит (prepare_status_message).

        Args:
            metrics (dict): Словарь с ключами, такими как active_tasks, queue_size, registered_modules, error_count.
        """
        try:
            if not isinstance(metrics, dict):
                raise ValueError("Ожидался словарь метрик")
            # Получаем отформатированное сообщение через функцию из utils.py
            status_text = prepare_status_message(metrics)
            self.label.config(text=status_text)
            logger.info("StatusBar обновлён")
        except Exception as e:
            logger.error(f"Ошибка в StatusBar.update_status: {e}")


class ModuleListWidget(tk.Frame):
    """
    Список зарегистрированных модулей.
    """

    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.label = tk.Label(self, text="Модули:")
        self.label.pack()
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True)

    def update_list(self, modules: list[str]) -> None:
        """
        Обновляет список модулей в listbox.

        Args:
            modules (list): Список названий модулей.
        """
        try:
            if not isinstance(modules, list) or not all(isinstance(m, str) for m in modules):
                raise ValueError("Ожидался список строк для модулей")

            self.listbox.delete(0, tk.END)
            for module in modules:
                self.listbox.insert(tk.END, module)
            logger.info("ModuleListWidget обновлён")
        except Exception as e:
            logger.error(f"Ошибка в ModuleListWidget.update_list: {e}")
