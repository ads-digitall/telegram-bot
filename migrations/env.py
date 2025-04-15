from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

from core.config import settings
from core.database.models import Base

# Настройка конфигурации Alembic
config = context.config

# Настройка логирования (если есть ini-файл)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные моделей для Alembic
target_metadata = Base.metadata

# Синхронный URL подключения к базе PostgreSQL
DB_URL = (
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

def run_migrations_offline():
    """Запуск миграций в офлайн-режиме (без подключения к БД)."""
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Запуск миграций в онлайн-режиме (через подключение к БД)."""
    engine = create_engine(DB_URL, poolclass=pool.NullPool)

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# Точка входа: режим офлайн или онлайн
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
