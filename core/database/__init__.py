"""
Модуль базы данных для проекта «Бот-2».
Экспортирует функции и классы для работы с базой данных:
- get_database: асинхронная функция для получения сессии.
- Base, User, Channel: базовый класс и модели данных.
- CRUD-функции: add_user, get_user, update_user, delete_user, get_all_users,
  add_channel, get_channel, update_channel, delete_channel, get_all_channels.
"""

from .database import get_database
from .models import Base, User, Channel
from .crud import (
    add_user,
    get_user,
    update_user,
    delete_user,
    get_all_users,
    add_channel,
    get_channel,
    update_channel,
    delete_channel,
    get_all_channels
)

__all__ = [
    "get_database",
    "Base",
    "User",
    "Channel",
    "add_user",
    "get_user",
    "update_user",
    "delete_user",
    "get_all_users",
    "add_channel",
    "get_channel",
    "update_channel",
    "delete_channel",
    "get_all_channels"
]
