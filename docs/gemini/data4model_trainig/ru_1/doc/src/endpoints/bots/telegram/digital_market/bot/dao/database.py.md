# Модуль для работы с базой данных
========================================

Модуль содержит базовый класс `Base` для моделей SQLAlchemy и инструменты для подключения к асинхронной базе данных.

## Обзор

Этот модуль предоставляет основу для взаимодействия с базой данных в асинхронном режиме. Он включает в себя базовый класс `Base` для определения моделей данных, а также функции для создания асинхронного движка и сессий.

## Подробней

Модуль предназначен для упрощения работы с базами данных в проекте `hypotez`. Он предоставляет готовые инструменты для подключения к базе данных и определения моделей данных. Использование асинхронного подхода позволяет избежать блокировок при работе с базой данных, что особенно важно для высоконагруженных приложений.

## Классы

### `Base`

**Описание**: Базовый класс для моделей SQLAlchemy.

**Наследует**:
- `AsyncAttrs`: Предоставляет атрибуты для асинхронной работы с SQLAlchemy.
- `DeclarativeBase`: Базовый класс для декларативного определения моделей SQLAlchemy.

**Атрибуты**:
- `id` (int): Уникальный идентификатор записи, первичный ключ, автоинкремент.
- `created_at` (datetime): Дата и время создания записи, устанавливается автоматически при создании.
- `updated_at` (datetime): Дата и время последнего обновления записи, автоматически обновляется при каждом изменении.

**Методы**:
- `to_dict()`: Преобразует объект модели в словарь.

#### Принцип работы

Класс `Base` наследуется от `AsyncAttrs` и `DeclarativeBase` и определяет общие атрибуты для всех моделей данных в проекте. Атрибуты `id`, `created_at` и `updated_at` являются общими для большинства таблиц и автоматически управляются SQLAlchemy. Метод `to_dict()` позволяет легко преобразовать объект модели в словарь для сериализации или других целей.

### `__tablename__`
```python
    @classmethod
    @property
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'
```

**Назначение**: Формирует имя таблицы в базе данных на основе имени класса.

**Параметры**:
- `cls` (class): Ссылка на класс, для которого вызывается метод.

**Возвращает**:
- `str`: Имя таблицы в нижнем регистре с добавлением суффикса "s".

**Как работает метод**:
- Метод `__tablename__` является методом класса и вызывается для получения имени таблицы в базе данных.
- Он формирует имя таблицы, преобразуя имя класса в нижний регистр и добавляя суффикс "s".
- Например, для класса `User` имя таблицы будет `users`.

**Примеры**:

```python
class User(Base):
    __tablename__ = 'users'  # Имя таблицы будет 'users'
```

### `to_dict`
```python
    def to_dict(self) -> dict:
        # Метод для преобразования объекта в словарь
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
```
**Назначение**: Преобразует объект модели в словарь.

**Параметры**:
- Нет

**Возвращает**:
- `dict`: Словарь, содержащий атрибуты объекта модели.

**Как работает метод**:

- Функция `to_dict` преобразует объект модели в словарь, где ключами являются имена столбцов таблицы, а значениями - соответствующие значения атрибутов объекта.
- Используется генератор словаря для итерации по всем столбцам таблицы и получения значений атрибутов с помощью `getattr`.

**Примеры**:
```python
# from datetime import datetime
# from bot.config import database_url
# from sqlalchemy import func, TIMESTAMP, Integer
# from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
# from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

# from sqlalchemy import Column, String
# from sqlalchemy import Identity

# from sqlalchemy.orm import sessionmaker


# class User(Base):
#     __tablename__ = "users"

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     username: Mapped[str] = mapped_column(String(50), nullable=False)
#     email: Mapped[str] = mapped_column(String(50))

#     def __repr__(self) -> str:
#         return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r})"


# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# async def main():
#     await create_db_and_tables()

#     async with async_session_maker() as session:
#         user1 = User(username="spongebob", email="spongebob@example.com")
#         user2 = User(username="patrick", email="patrick@example.com")

#         session.add_all([user1, user2])

#         await session.commit()

#         our_user = await session.get(User, 2)
#         print(our_user)  # выведет юзера с id=2

#         print(user1.to_dict())  # выведет словарь с данными user1


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(main())
```

## Переменные

- `engine`: Асинхронный движок SQLAlchemy, используемый для подключения к базе данных.
- `async_session_maker`: Фабрика асинхронных сессий, используемая для создания сессий для работы с базой данных.
- `database_url`: URL для подключения к базе данных, берется из файла конфигурации `bot/config.py`.