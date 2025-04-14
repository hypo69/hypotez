# Модуль для настройки миграций базы данных Alembic

## Обзор

Этот модуль предназначен для настройки и запуска миграций базы данных с использованием Alembic. Он поддерживает как онлайн, так и оффлайн режимы миграции и использует асинхронные операции для повышения производительности.

## Подробней

Модуль настраивает Alembic для работы с базой данных, используя URL, указанный в `database_url`. Он также определяет, как запускать миграции в зависимости от того, находится ли Alembic в онлайн или оффлайн режиме.

## Функции

### `run_migrations_offline`

```python
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
```

**Назначение**: Запускает миграции в "оффлайн" режиме.

**Как работает функция**:
- Извлекает URL базы данных из конфигурации Alembic.
- Конфигурирует контекст Alembic с использованием URL базы данных и целевой метадаты.
- Запускает миграции в рамках транзакции.

**Примеры**:

```python
run_migrations_offline()
```

### `do_run_migrations`

```python
def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()
```

**Назначение**: Выполняет миграции базы данных, используя предоставленное соединение.

**Параметры**:
- `connection` (Connection): Объект соединения с базой данных.

**Как работает функция**:
- Конфигурирует контекст Alembic с предоставленным соединением и целевой метадатой.
- Запускает миграции в рамках транзакции.

**Примеры**:

```python
# Пример использования внутри асинхронной функции
async def example():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()
```

### `run_async_migrations`

```python
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
```

**Назначение**: Запускает миграции асинхронно.

**Как работает функция**:
- Создает асинхронный движок базы данных из конфигурации.
- Устанавливает соединение с базой данных.
- Запускает миграции с использованием функции `do_run_migrations` в синхронном режиме внутри асинхронного контекста.
- Закрывает соединение.

**Примеры**:

```python
async def main():
    await run_async_migrations()

asyncio.run(main())
```

### `run_migrations_online`

```python
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())
```

**Назначение**: Запускает миграции в "онлайн" режиме.

**Как работает функция**:
- Запускает асинхронные миграции, используя `asyncio.run`.

**Примеры**:

```python
run_migrations_online()