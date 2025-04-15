from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Импорт моделей
from core.database.models import Base
from core.config import get_settings

# Alembic Config object
config = context.config

# Настройка логирования
fileConfig(config.config_file_name)

# Получение URL БД из настроек
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Целевая метаинформация — база моделей
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Запуск соответствующего режима
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
