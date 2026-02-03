"""
Alembic migrations environment configuration.

This module configures the migrations environment for async SQLAlchemy 2.0:
- Loads database URL from environment variables
- Supports autogenerate with SQLAlchemy 2.0 models
- Uses synchronous engine for migration operations (alembic requirement)
"""

import os
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from alembic import context

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Import Base from database module for autogenerate
from database import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Configure database URL from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+aiomysql://blog:blog@localhost:3306/blog"
).replace("+aiomysql", "").replace("mysql://", "mysql+pymysql://")  # Use pymysql driver for sync migration

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


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
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
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
