"""
central_core/gui/events.py

Модуль обработчиков событий для GUI.
Содержит функции для обработки пользовательских событий:
– on_button_click: обработка клика по кнопке.
– on_menu_select: обработка выбора пункта меню.
– on_key_press: обработка нажатия клавиш.
– on_close: обработка закрытия окна.
Добавлена обработка ошибок и вывод их в GUI.
"""

def on_button_click(gui, button_id, event=None):
    """
    Обработчик события клика по кнопке.
    
    Args:
        gui: Объект GUI или контроллер, через который можно обновлять интерфейс.
        button_id (str): Идентификатор или имя кнопки.
        event: Событие, связанное с нажатием (если используется, например, в Tkinter).
        
    Пример использования:
        on_button_click(main_gui, "start_button")
    """
    try:
        print(f"Кнопка {button_id} нажата.")
        # Обновление состояния интерфейса, вывод сообщения и выполнение логики, связанной с кнопкой.
        if hasattr(gui, "update_status"):
            gui.update_status(f"Нажата кнопка: {button_id}")
        # Дополнительная логика по обработке нажатия может быть добавлена здесь.
    except Exception as e:
        print(f"Ошибка при обработке клика по кнопке {button_id}: {e}")
        if hasattr(gui, "display_error"):
            gui.display_error(f"Ошибка при обработке клика по кнопке: {e}")
        else:
            # Если в GUI нет метода для отображения ошибки, просто логируем
            print(f"Ошибка при обработке клика по кнопке {button_id}: {e}")

def on_menu_select(gui, menu_item, event=None):
    """
    Обработчик выбора пункта меню.
    
    Args:
        gui: Объект GUI или контроллер.
        menu_item (str): Имя или идентификатор выбранного пункта меню.
        event: Событие, связанное с выбором меню (при наличии).
        
    Пример использования:
        on_menu_select(main_gui, "Настройки")
    """
    try:
        print(f"Выбран пункт меню: {menu_item}")
        if hasattr(gui, "update_status"):
            gui.update_status(f"Выбран пункт меню: {menu_item}")
        # Здесь может выполняться вызов соответствующего метода обработки для выбранного пункта меню.
    except Exception as e:
        print(f"Ошибка при обработке выбора пункта меню {menu_item}: {e}")
        if hasattr(gui, "display_error"):
            gui.display_error(f"Ошибка при обработке выбора пункта меню: {e}")
        else:
            # Логируем ошибку
            print(f"Ошибка при обработке выбора пункта меню {menu_item}: {e}")

def on_key_press(gui, key, event=None):
    """
    Обработчик события нажатия клавиши.
    
    Args:
        gui: Объект GUI или контроллер.
        key (str): Символ или имя нажатой клавиши.
        event: Событие, если используется в рамках системы (например, в Tkinter).
        
    Пример использования:
        on_key_press(main_gui, "Enter")
    """
    try:
        print(f"Нажата клавиша: {key}")
        if hasattr(gui, "update_status"):
            gui.update_status(f"Нажата клавиша: {key}")
        # Дополнительная логика для обработки нажатия клавиш может быть реализована здесь.
    except Exception as e:
        print(f"Ошибка при обработке нажатия клавиши {key}: {e}")
        if hasattr(gui, "display_error"):
            gui.display_error(f"Ошибка при обработке нажатия клавиши: {e}")
        else:
            # Логируем ошибку
            print(f"Ошибка при обработке нажатия клавиши {key}: {e}")

def on_close(gui, event=None):
    """
    Обработчик события закрытия окна.
    
    Args:
        gui: Объект GUI или контроллер.
        event: Событие закрытия (если используется).
        
    Пример использования:
        on_close(main_gui)
    """
    try:
        print("Окно закрывается...")
        if hasattr(gui, "cleanup"):
            gui.cleanup()
        # Здесь можно вызвать дополнительные процедуры завершения работы приложения.
    except Exception as e:
        print(f"Ошибка при закрытии окна: {e}")
        if hasattr(gui, "display_error"):
            gui.display_error(f"Ошибка при закрытии окна: {e}")
        else:
            # Логируем ошибку
            print(f"Ошибка при закрытии окна: {e}")
