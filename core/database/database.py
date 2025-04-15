"""
Модуль подключения к базе данных PostgreSQL с использованием SQLAlchemy Async.
Создаёт асинхронный движок, фабрику сессий и генератор сессий.
Все модели вынесены в отдельный модуль `models.py`.
"""

from typing import AsyncGenerator
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from core.config import settings
from core.logger import get_logger
import sqlalchemy.exc
from error_handler import handle_error

logger = get_logger()

# Формирование строки подключения
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

# Глобальные переменные
engine = None
async_session_factory = None
engine_loop = None

def initialize_engine():
    global engine, async_session_factory, engine_loop
    current_loop = asyncio.get_running_loop()

    if engine is None or engine_loop != current_loop:
        try:
            logger.info(f"Создаётся новый движок БД в loop id: {id(current_loop)}")
            engine = create_async_engine(
                DATABASE_URL,
                echo=False,
                future=True,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
            engine_loop = current_loop
            logger.info("Движок базы данных успешно инициализирован.")
        except sqlalchemy.exc.SQLAlchemyError as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            handle_error(e, "DatabaseModule", "Ошибка при подключении к базе данных")
            raise ConnectionError("Не удалось установить соединение с базой данных.")
    else:
        logger.debug(f"Используется существующий движок БД, созданный в loop id: {id(engine_loop)}")

async def get_database() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор сессий для работы с базой данных.
    """
    initialize_engine()
    try:
        async with async_session_factory() as session:
            yield session
    except sqlalchemy.exc.SQLAlchemyError as e:
        logger.error(f"Ошибка работы с сессией базы данных: {e}")
        handle_error(e, "DatabaseModule", "Ошибка при работе с сессией базы данных")
        raise ConnectionError("Ошибка при работе с сессией базы данных.")

# Инициализация таблиц при необходимости
from core.database.models import Base

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Инициализация таблиц завершена.")
    except sqlalchemy.exc.SQLAlchemyError as e:
        logger.error(f"Ошибка при инициализации таблиц: {e}")
        handle_error(e, "DatabaseModule", "Ошибка при инициализации таблиц")
        raise

# ✅ Ленивый безопасный доступ к сессии
def get_async_session():
    initialize_engine()
    return async_session_factory()

if __name__ == "__main__":
    try:
        asyncio.run(init_db())
    except Exception as e:
        logger.error(f"Ошибка при запуске инициализации базы данных: {e}")
        handle_error(e, "DatabaseModule", "Ошибка при запуске инициализации базы данных")
