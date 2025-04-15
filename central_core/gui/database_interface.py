"""
database_interface.py

Реализует административный интерфейс для работы с базой данных.
Открывает отдельное окно (Toplevel) с вкладками для отображения данных:
- Пользователи (таблица)
- Каналы (таблица)
- Посты (таблица)
Также включает кнопку "Обновить данные" для загрузки свежей информации из базы.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import threading
from core.logger import get_logger
# Импортируем функцию получения сессии напрямую, чтобы избежать циклических импортов
from core.database.database import get_database
from core.database.crud import get_all_users, get_all_channels
from sqlalchemy import text

logger = get_logger()

# Создаем и запускаем единый event loop в отдельном потоке для DB-операций
_loop = asyncio.new_event_loop()
threading.Thread(target=_loop.run_forever, daemon=True).start()

def create_database_window():
    # Создаем новое окно административного интерфейса
    db_window = tk.Toplevel()
    db_window.title("Администрирование базы данных")
    db_window.geometry("900x600")
    
    # Создаем Notebook (вкладки)
    notebook = ttk.Notebook(db_window)
    notebook.pack(expand=True, fill='both', padx=10, pady=10)
    
    # Вкладка для пользователей
    users_frame = ttk.Frame(notebook)
    notebook.add(users_frame, text="Пользователи")
    
    # Вкладка для каналов
    channels_frame = ttk.Frame(notebook)
    notebook.add(channels_frame, text="Каналы")
    
    # Вкладка для постов
    posts_frame = ttk.Frame(notebook)
    notebook.add(posts_frame, text="Посты")
    
    # Создаем таблицу для пользователей
    users_tree = ttk.Treeview(users_frame, columns=("user_id", "username", "first_name", "last_name", "language_code", "registration_date"), show="headings")
    for col in ("user_id", "username", "first_name", "last_name", "language_code", "registration_date"):
        users_tree.heading(col, text=col)
        users_tree.column(col, anchor="center")
    users_tree.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Создаем таблицу для каналов
    channels_tree = ttk.Treeview(channels_frame, columns=("channel_id", "channel_name", "channel_link", "description", "member_count", "creation_date"), show="headings")
    for col in ("channel_id", "channel_name", "channel_link", "description", "member_count", "creation_date"):
        channels_tree.heading(col, text=col)
        channels_tree.column(col, anchor="center")
    channels_tree.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Создаем таблицу для постов с обновленным набором столбцов (используется колонка interests)
    posts_tree = ttk.Treeview(posts_frame, columns=("id", "channel_id", "message_id", "interests", "date", "channel_name"), show="headings")
    for col in ("id", "channel_id", "message_id", "interests", "date", "channel_name"):
        posts_tree.heading(col, text=col)
        posts_tree.column(col, anchor="center")
    posts_tree.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Кнопка обновления данных
    refresh_button = tk.Button(db_window, text="Обновить данные", command=lambda: refresh_data(users_tree, channels_tree, posts_tree))
    refresh_button.pack(pady=5)
    
    # Загружаем данные при открытии окна
    refresh_data(users_tree, channels_tree, posts_tree)

def refresh_data(users_tree, channels_tree, posts_tree):
    async def load_data():
        # Очистка текущих данных в таблицах
        for item in users_tree.get_children():
            users_tree.delete(item)
        for item in channels_tree.get_children():
            channels_tree.delete(item)
        for item in posts_tree.get_children():
            posts_tree.delete(item)
        
        # Получаем данные из базы (используем первую сессию)
        async for db in get_database():
            users = await get_all_users(db)
            channels = await get_all_channels(db)
            # Запрашиваем данные постов напрямую
            result = await db.execute(text("SELECT * FROM posts ORDER BY date DESC"))
            posts = result.fetchall()
            break
        
        # Заполняем таблицу пользователей
        for user in users:
            users_tree.insert("", "end", values=(
                user.user_id,
                user.username,
                user.first_name,
                user.last_name,
                user.language_code,
                user.registration_date.strftime("%Y-%m-%d %H:%M:%S") if user.registration_date else ""
            ))
        
        # Заполняем таблицу каналов
        for channel in channels:
            channels_tree.insert("", "end", values=(
                channel.channel_id,
                channel.channel_name,
                channel.channel_link,
                channel.description,
                channel.member_count,
                channel.creation_date.strftime("%Y-%m-%d %H:%M:%S") if channel.creation_date else ""
            ))
        
        # Заполняем таблицу постов
        for post in posts:
            # Ожидается, что модель Post содержит поля: id, channel_id, message_id, interests, date, channel_name
            posts_tree.insert("", "end", values=(
                post.id,
                post.channel_id,
                post.message_id,
                post.interests,  # выводится колонка interests (на данный момент пустая строка)
                post.date.strftime("%Y-%m-%d %H:%M:%S") if post.date else "",
                post.channel_name
            ))
        logger.info("Данные обновлены в административном окне базы данных.")
    
    try:
        asyncio.run_coroutine_threadsafe(load_data(), _loop)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось обновить данные: {e}")
        logger.error(f"Ошибка обновления данных: {e}")

if __name__ == "__main__":
    # Если модуль запускается напрямую, создаем окно интерфейса базы данных
    root = tk.Tk()
    root.withdraw()  # Скрываем главное окно
    create_database_window()
