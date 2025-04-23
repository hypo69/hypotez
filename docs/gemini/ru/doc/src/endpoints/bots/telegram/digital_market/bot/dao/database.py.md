# Модуль для работы с базой данных
## \file hypotez/src/endpoints/bots/telegram/digital_market/bot/dao/database.py

## Обзор

Модуль определяет базовые классы и настройки для работы с асинхронной базой данных с использованием SQLAlchemy. Он включает в себя конфигурацию подключения к базе данных, базовый класс для моделей и функции для взаимодействия с базой данных.

## Подробнее

Модуль предоставляет абстрактный базовый класс `Base` для определения моделей базы данных, а также утилиты для создания асинхронного движка и сессии базы данных. Это позволяет единообразно и эффективно работать с базой данных в асинхронном режиме.

## Классы

### `Base`

**Описание**:
Абстрактный базовый класс для моделей базы данных.

**Наследует**:
`AsyncAttrs`, `DeclarativeBase` из SQLAlchemy.

**Атрибуты**:

- `id` (int): Уникальный идентификатор записи, первичный ключ, автоинкрементный.
- `created_at` (datetime): Дата и время создания записи, по умолчанию текущее время.
- `updated_at` (datetime): Дата и время последнего обновления записи, по умолчанию текущее время, обновляется при каждом изменении записи.

**Методы**:

- `to_dict()`: Преобразует объект модели в словарь.

**Принцип работы**:

Класс `Base` служит основой для всех моделей базы данных в проекте. Он содержит общие атрибуты, такие как `id`, `created_at` и `updated_at`, а также метод `to_dict` для преобразования объекта в словарь. Класс использует функциональность `AsyncAttrs` и `DeclarativeBase` из SQLAlchemy для упрощения работы с асинхронными базами данных.

## Методы класса

### `to_dict`

```python
def to_dict(self) -> dict:
    """
    Метод для преобразования объекта в словарь.

    Args:
        self: Экземпляр класса.

    Returns:
        dict: Словарь, содержащий имена столбцов и их значения.
    """
```

**Назначение**:
Преобразует объект модели в словарь, где ключами являются имена столбцов, а значениями - соответствующие значения атрибутов объекта.

**Параметры**:
- `self`: Экземпляр класса.

**Возвращает**:
- `dict`: Словарь, содержащий имена столбцов и их значения.

**Как работает функция**:
Функция выполняет итерацию по всем столбцам таблицы, связанной с классом, и создает словарь, в котором ключами являются имена столбцов, а значениями - значения соответствующих атрибутов экземпляра класса.

**Примеры**:

```python
# Пример использования
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

database_url = "sqlite:///:memory:" #  Временная база данных в памяти
engine = create_engine(database_url) #  Использовать синхронный движок для примера
Base = declarative_base()

class Example(Base):
    __tablename__ = 'examples'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

example = Example(name="Test Example")
session.add(example)
session.commit()

example_dict = example.to_dict()
print(example_dict) #  {'id': 1, 'name': 'Test Example', 'created_at': datetime(...)}
session.close()
```

## Переменные

- `engine`: Асинхронный движок SQLAlchemy для подключения к базе данных, созданный на основе URL, указанного в `database_url`.
- `async_session_maker`: Фабрика асинхронных сессий SQLAlchemy, использующая созданный движок.
- `database_url` (str): URL для подключения к базе данных, полученный из `bot.config`.

## Описание переменных
- `database_url` (str): URL для подключения к базе данных, полученный из `bot.config`.
- `engine`: Асинхронный движок SQLAlchemy для подключения к базе данных, созданный на основе URL, указанного в `database_url`.
- `async_session_maker`: Фабрика асинхронных сессий SQLAlchemy, использующая созданный движок.

```python
database_url:str = 'sqlite:///:memory:'
engine = create_async_engine(url=database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)