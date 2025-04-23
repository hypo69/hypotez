### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот код представляет собой скрипт миграции базы данных, использующий Alembic для управления изменениями схемы базы данных. Он поддерживает как онлайн, так и оффлайн режимы миграции, а также асинхронное выполнение миграций.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются необходимые библиотеки, такие как `sys`, `asyncio`, `logging.config`, `sqlalchemy`, `alembic` и модели базы данных (`Product`, `Purchase`, `User`, `Category`).
   - Добавляется путь к директории проекта в `sys.path`, чтобы обеспечить доступ к модулям проекта.

2. **Настройка конфигурации**:
   - Извлекается конфигурация из контекста Alembic и устанавливается URL базы данных.
   - Настраивается файл конфигурации логирования, если он указан.
   - Определяется целевая метадата для миграции (метаданные, определенные в `Base.metadata`).

3. **Определение функций миграции**:
   - `run_migrations_offline()`: Выполняет миграции в оффлайн режиме. В этом режиме не требуется подключение к базе данных.
     - Извлекает URL базы данных из конфигурации.
     - Настраивает контекст Alembic с URL и целевой метадатой.
     - Запускает миграции в транзакции.

   - `do_run_migrations(connection: Connection)`: Выполняет миграции, используя существующее подключение к базе данных.
     - Настраивает контекст Alembic с подключением и целевой метадатой.
     - Запускает миграции в транзакции.

   - `run_async_migrations()`: Асинхронно выполняет миграции.
     - Создает асинхронный движок SQLAlchemy на основе конфигурации.
     - Устанавливает пул подключений `NullPool`, чтобы избежать проблем с управлением подключениями.
     - Выполняет миграции в асинхронной транзакции.
     - Закрывает соединение с базой данных.

   - `run_migrations_online()`: Запускает миграции в онлайн режиме.
     - Вызывает `run_async_migrations()` для выполнения миграций асинхронно.

4. **Выбор режима миграции**:
   - Проверяется, находится ли Alembic в оффлайн режиме (`context.is_offline_mode()`).
   - Если в оффлайн режиме, вызывается `run_migrations_offline()`.
   - Если в онлайн режиме, вызывается `run_migrations_online()`.

Пример использования
-------------------------

```python
# Пример использования в проекте для запуска миграций

from alembic.config import Config
from alembic import command

# Предположим, что alembic.ini находится в корневой директории проекта
alembic_cfg = Config("alembic.ini")

# Запуск миграций до последней версии
command.upgrade(alembic_cfg, "head")
```
```python
# file: src/endpoints/bots/telegram/digital_market/bot/migration/env.py
import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))

import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from bot.dao.database import Base, database_url
from bot.dao.models import Product, Purchase, User, Category


config = context.config
config.set_main_option("sqlalchemy.url", database_url)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
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


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()