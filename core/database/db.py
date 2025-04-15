"""
db.py

Модуль для работы с базой данных через SQLAlchemy.
Реализует создание сессий, основные операции CRUD, подключение к базе данных и миграции.
Добавлена централизованная обработка ошибок.
"""

import logging
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from core.config import settings
from error_handler import handle_error  # Импортируем централизованный обработчик ошибок

# Конфигурация базы данных
DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}" \
               f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# Настройка логгера
logger = logging.getLogger(__name__)

# Создание базового класса для моделей
Base = declarative_base()

# Создаем движок SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Фабрика сессий для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Пример модели для пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    subscription_status = Column(String, default="unsubscribed")
    created_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, default=None)

def init_db():
    """
    Создает все таблицы в базе данных, если их еще нет.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Все таблицы успешно созданы.")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при создании таблиц: {e}")
        handle_error(e, "DatabaseModule", "Ошибка при создании таблиц")
        raise

def get_db() -> Session:
    """
    Создает сессию для работы с базой данных.

    :return: сессия для работы с БД.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при работе с сессией: {e}")
        handle_error(e, "DatabaseModule", "Ошибка при работе с сессией")
        raise
    finally:
        db.close()

# Пример CRUD операций

def create_user(db: Session, username: str, email: str) -> User:
    """
    Создает нового пользователя в базе данных.

    :param db: сессия для работы с БД.
    :param username: имя пользователя.
    :param email: email пользователя.
    :return: созданный объект пользователя.
    """
    try:
        db_user = User(username=username, email=email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"Пользователь {username} успешно создан.")
        return db_user
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при создании пользователя {username}: {e}")
        handle_error(e, "DatabaseModule", f"Ошибка при создании пользователя {username}")
        raise

def get_user(db: Session, user_id: int) -> User:
    """
    Получает пользователя по ID.

    :param db: сессия для работы с БД.
    :param user_id: ID пользователя.
    :return: объект пользователя.
    """
    try:
        return db.query(User).filter(User.id == user_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении пользователя с ID {user_id}: {e}")
        handle_error(e, "DatabaseModule", f"Ошибка при получении пользователя с ID {user_id}")
        raise

def update_user(db: Session, user_id: int, update_data: dict) -> User:
    """
    Обновляет данные пользователя.

    :param db: сессия для работы с БД.
    :param user_id: ID пользователя.
    :param update_data: данные для обновления.
    :return: обновленный объект пользователя.
    """
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            for key, value in update_data.items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
            logger.info(f"Пользователь {user_id} успешно обновлен.")
            return db_user
        else:
            logger.warning(f"Пользователь с ID {user_id} не найден.")
            return None
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при обновлении пользователя с ID {user_id}: {e}")
        handle_error(e, "DatabaseModule", f"Ошибка при обновлении пользователя с ID {user_id}")
        raise

def delete_user(db: Session, user_id: int) -> bool:
    """
    Удаляет пользователя по ID.

    :param db: сессия для работы с БД.
    :param user_id: ID пользователя.
    :return: True, если удаление прошло успешно.
    """
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            logger.info(f"Пользователь с ID {user_id} успешно удален.")
            return True
        else:
            logger.warning(f"Пользователь с ID {user_id} не найден.")
            return False
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при удалении пользователя с ID {user_id}: {e}")
        handle_error(e, "DatabaseModule", f"Ошибка при удалении пользователя с ID {user_id}")
        raise
