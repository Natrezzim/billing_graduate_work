import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from sqlmodel import SQLModel
from alembic import context


db_driver: str = os.getenv('DRIVER', 'postgresql')
db_host: str = os.getenv('DB_HOST', 'localhost')
db_port: str = os.getenv('DB_PORT', '5432')
db_name: str = os.getenv('POSTGRES_DB', 'billing_db')
db_user: str = os.getenv('POSTGRES_USER', 'postgres')
db_password: str = os.getenv('POSTGRES_PASSWORD', '11111111')

config = context.config

config.set_main_option('sqlalchemy.url', f'{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
