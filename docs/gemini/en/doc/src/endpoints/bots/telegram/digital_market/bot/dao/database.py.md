# Модуль для работы с базой данных Telegram бота

## Обзор

Этот модуль содержит определение базового класса `Base` для моделирования данных, используемых в Telegram боте. Он также предоставляет настройки для подключения к базе данных и создания сессий.

## Подробности

Этот модуль используется для создания и управления данными, связанными с Telegram ботом. `Base` класс служит основой для создания новых моделей данных, обеспечивая базовые атрибуты, такие как идентификатор, время создания и время обновления.

## Классы

### `Base`

**Описание**:  Базовый класс для моделей данных, используемых в Telegram боте.

**Inherits**: `AsyncAttrs`, `DeclarativeBase`

**Атрибуты**:

- `id` (int):  Идентификатор записи.
- `created_at` (datetime):  Время создания записи.
- `updated_at` (datetime): Время обновления записи.

**Методы**:

- `__tablename__`:  Возвращает название таблицы в базе данных, основанное на названии класса.
- `to_dict`:  Преобразует объект класса в словарь.

## Функции

### `create_async_engine`

**Описание**:  Создает асинхронный движок базы данных.

**Параметры**:

- `url` (str): Строка подключения к базе данных.

**Returns**:  Объект `AsyncEngine`, представляющий асинхронный движок базы данных.

### `async_sessionmaker`

**Описание**:  Создает фабрику асинхронных сессий.

**Параметры**:

- `engine`:  Объект `AsyncEngine` - асинхронный движок базы данных.
- `class_`:  Класс `AsyncSession`, который будет использоваться для создания сессий.

**Returns**:  Фабрика асинхронных сессий.

## Примеры

```python
from bot.dao.database import Base, async_session_maker

class User(Base):
    """
    Модель данных для пользователей.
    """
    username: Mapped[str] = mapped_column(String, nullable=False)
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=False)
    # ... другие атрибуты

async def create_user(session: AsyncSession, username: str, telegram_id: int):
    """
    Создает нового пользователя в базе данных.
    """
    new_user = User(username=username, telegram_id=telegram_id)
    session.add(new_user)
    await session.commit()

async def main():
    async with async_session_maker() as session:
        await create_user(session, 'test_user', 12345)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

## Parameter Details

- `database_url` (str):  Строка подключения к базе данных.

## Examples

```python
from bot.dao.database import Base, engine, async_session_maker

async def main():
    async with async_session_maker() as session:
        # ...  использование сессии для работы с данными
```