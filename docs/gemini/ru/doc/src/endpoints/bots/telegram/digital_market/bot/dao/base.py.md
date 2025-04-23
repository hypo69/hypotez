# Модуль `base.py`

## Обзор

Модуль содержит базовый класс `BaseDAO`, который предоставляет набор общих методов для взаимодействия с базой данных. 
Этот класс использует SQLAlchemy для выполнения операций, таких как поиск, добавление, обновление, удаление и подсчет записей.

## Подробнее

Модуль определяет дженерик-класс `BaseDAO`, который параметризуется типом модели, представляющей таблицу в базе данных. 
Он предоставляет методы для выполнения стандартных операций CRUD (Create, Read, Update, Delete) и других полезных запросов, таких как пагинация и массовое обновление.

## Классы

### `BaseDAO`

**Описание**:
Базовый класс для доступа к данным в базе данных. Предоставляет общие методы для выполнения CRUD-операций с использованием SQLAlchemy.

**Атрибуты**:
- `model` (type[T]): Тип модели, представляющей таблицу в базе данных.

**Методы**:
- `find_one_or_none_by_id(cls, data_id: int, session: AsyncSession)`: Находит запись по ID.
- `find_one_or_none(cls, session: AsyncSession, filters: BaseModel)`: Находит одну запись по фильтрам.
- `find_all(cls, session: AsyncSession, filters: BaseModel | None = None)`: Находит все записи по фильтрам.
- `add(cls, session: AsyncSession, values: BaseModel)`: Добавляет одну запись.
- `add_many(cls, session: AsyncSession, instances: List[BaseModel])`: Добавляет несколько записей.
- `update(cls, session: AsyncSession, filters: BaseModel, values: BaseModel)`: Обновляет записи по фильтрам.
- `delete(cls, session: AsyncSession, filters: BaseModel)`: Удаляет записи по фильтру.
- `count(cls, session: AsyncSession, filters: BaseModel | None = None)`: Подсчитывает количество записей.
- `paginate(cls, session: AsyncSession, page: int = 1, page_size: int = 10, filters: BaseModel = None)`: Пагинация записей.
- `find_by_ids(cls, session: AsyncSession, ids: List[int])`: Находит несколько записей по списку ID.
- `upsert(cls, session: AsyncSession, unique_fields: List[str], values: BaseModel)`: Создает запись или обновляет существующую.
- `bulk_update(cls, session: AsyncSession, records: List[BaseModel])`: Массовое обновление записей.

## Методы класса

### `find_one_or_none_by_id`

```python
    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession):
        """Найти запись по ID

        Args:
            data_id (int): ID записи для поиска.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            T | None: Найденная запись или None, если запись не найдена.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении запроса к базе данных.
        """
```

**Назначение**:
Метод выполняет поиск записи в базе данных по указанному ID.

**Как работает функция**:
- Логирует начало поиска записи.
- Формирует запрос к базе данных на выборку записи с указанным ID.
- Выполняет запрос и получает результат.
- Логирует результат поиска (найдена или не найдена).
- В случае ошибки логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования
from sqlalchemy.ext.asyncio import AsyncSession
from bot.dao.database import Base
from bot.dao.base import BaseDAO

class MyModel(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)

class MyModelDAO(BaseDAO[MyModel]):
    model = MyModel

async def example(session: AsyncSession, data_id: int):
    record = await MyModelDAO.find_one_or_none_by_id(data_id=data_id, session=session)
    if record:
        print(f"Запись с ID {data_id} найдена: {record}")
    else:
        print(f"Запись с ID {data_id} не найдена")
```

### `find_one_or_none`

```python
    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel):
        """Найти одну запись по фильтрам

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (BaseModel): Pydantic модель с фильтрами для поиска.

        Returns:
            T | None: Найденная запись или None, если запись не найдена.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении запроса к базе данных.
        """
```

**Назначение**:
Метод выполняет поиск одной записи в базе данных по указанным фильтрам.

**Как работает функция**:
- Преобразует фильтры из Pydantic модели в словарь.
- Логирует начало поиска записи.
- Формирует запрос к базе данных на выборку записи с указанными фильтрами.
- Выполняет запрос и получает результат.
- Логирует результат поиска (найдена или не найдена).
- В случае ошибки логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from bot.dao.base import BaseDAO
from bot.dao.database import Base

class MyModel(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class MyModelFilters(BaseModel):
    name: str

class MyModelDAO(BaseDAO[MyModel]):
    model = MyModel

async def example(session: AsyncSession, name: str):
    filters = MyModelFilters(name=name)
    record = await MyModelDAO.find_one_or_none(session=session, filters=filters)
    if record:
        print(f"Запись найдена: {record}")
    else:
        print(f"Запись не найдена")
```

### `find_all`

```python
    @classmethod
    async def find_all(cls, session: AsyncSession, filters: BaseModel | None = None):
        """Найти все записи по фильтрам

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (BaseModel | None): Pydantic модель с фильтрами для поиска. Может быть None.

        Returns:
            List[T]: Список найденных записей.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении запроса к базе данных.
        """
```

**Назначение**:
Метод выполняет поиск всех записей в базе данных по указанным фильтрам.

**Как работает функция**:
- Преобразует фильтры из Pydantic модели в словарь, если фильтры указаны.
- Логирует начало поиска записей.
- Формирует запрос к базе данных на выборку всех записей с указанными фильтрами.
- Выполняет запрос и получает результат.
- Логирует количество найденных записей.
- В случае ошибки логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from bot.dao.base import BaseDAO
from bot.dao.database import Base

class MyModel(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class MyModelFilters(BaseModel):
    name: str

class MyModelDAO(BaseDAO[MyModel]):
    model = MyModel

async def example(session: AsyncSession, name: str):
    filters = MyModelFilters(name=name)
    records = await MyModelDAO.find_all(session=session, filters=filters)
    print(f"Найдено {len(records)} записей")
    for record in records:
        print(record)
```

### `add`

```python
    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel):
        """Добавить одну запись

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            values (BaseModel): Pydantic модель со значениями для добавления.

        Returns:
            T: Новая запись.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении запроса к базе данных.
        """
```

**Назначение**:
Метод добавляет одну новую запись в базу данных.

**Как работает функция**:
- Преобразует значения из Pydantic модели в словарь.
- Логирует начало добавления записи.
- Создает новый экземпляр модели с указанными значениями.
- Добавляет новый экземпляр в сессию SQLAlchemy.
- Фиксирует изменения в базе данных.
- Логирует успешное добавление записи.
- В случае ошибки откатывает транзакцию, логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from bot.dao.base import BaseDAO
from bot.dao.database import Base

class MyModel(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class MyModelCreate(BaseModel):
    name: str

class MyModelDAO(BaseDAO[MyModel]):
    model = MyModel

async def example(session: AsyncSession, name: str):
    values = MyModelCreate(name=name)
    new_record = await MyModelDAO.add(session=session, values=values)
    print(f"Добавлена запись: {new_record}")
```

### `add_many`

```python
    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[BaseModel]):
        """Добавить несколько записей

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            instances (List[BaseModel]): Список Pydantic моделей со значениями для добавления.

        Returns:
            List[T]: Список новых записей.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении запроса к базе данных.
        """
```

**Назначение**:
Метод добавляет несколько новых записей в базу данных.

**Как работает функция**:
- Преобразует значения из списка Pydantic моделей в список словарей.
- Логирует начало добавления записей.
- Создает новые экземпляры модели с указанными значениями.
- Добавляет новые экземпляры в сессию SQLAlchemy.
- Фиксирует изменения в базе данных.
- Логирует успешное добавление записей.
- В случае ошибки откатывает транзакцию, логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from bot.dao.base import BaseDAO
from bot.dao.database import Base

class MyModel(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class MyModelCreate(BaseModel):
    name: str

class MyModelDAO(BaseDAO[MyModel]):
    model = MyModel

async def example(session: AsyncSession, names: List[str]):
    instances = [MyModelCreate(name=name) for name in names]
    new_records = await MyModelDAO.add_many(session=session, instances=instances)
    print(f"Добавлено {len(new_records)} записей")
    for record in new_records:
        print(record)
```

### `update`

```python
    @classmethod
    async def update(cls, session: AsyncSession, filters: BaseModel, values: BaseModel):
        """Обновить записи по фильтрам

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (BaseModel): Pydantic модель с фильтрами для обновления.
            values (BaseModel): Pydantic модель со значениями для обновления.

        Returns:
            int: Количество обновленных записей.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении запроса к базе данных.
        """
```

**Назначение**:
Метод обновляет записи в базе данных по указанным фильтрам.

**Как работает функция**:
- Преобразует фильтры и значения из Pydantic моделей в словари.
- Логирует начало обновления записей.
- Формирует запрос к базе данных на обновление записей с указанными фильтрами и значениями.
- Выполняет запрос и получает результат.
- Фиксирует изменения в базе данных.
- Логирует количество обновленных записей.
- В случае ошибки откатывает транзакцию, логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from bot.dao.base import BaseDAO
from bot.dao.database import Base

class MyModel(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class MyModelFilters(BaseModel):
    id: int

class MyModelUpdate(BaseModel):
    name: str

class MyModelDAO(BaseDAO[MyModel]):
    model = MyModel

async def example(session: AsyncSession, record_id: int, new_name: str):
    filters = MyModelFilters(id=record_id)
    values = MyModelUpdate(name=new_name)
    updated_count = await MyModelDAO.update(session=session, filters=filters, values=values)
    print(f"Обновлено {updated_count} записей")
```

### `delete`

```python
    @classmethod
    async def delete(cls, session: AsyncSession, filters: BaseModel):
        """Удалить записи по фильтру

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (BaseModel): Pydantic модель с фильтрами для удаления.

        Returns:
            int: Количество удаленных записей.

        Raises:
            ValueError: Если не указан ни один фильтр для удаления.
            SQLAlchemyError: Если произошла ошибка при выполнении запроса к базе данных.
        """
```

**Назначение**:
Метод удаляет записи из базы данных по указанному фильтру.

**Как работает функция**:
- Преобразует фильтры из Pydantic модели в словарь.
- Логирует начало удаления записей.
- Проверяет, что указан хотя бы один фильтр для удаления.
- Формирует запрос к базе данных на удаление записей с указанным фильтром.
- Выполняет запрос и получает результат.
- Фиксирует изменения в базе данных.
- Логирует количество удаленных записей.
- В случае ошибки откатывает транзакцию, логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from bot.dao.base import BaseDAO
from bot.dao.database import Base

class MyModel(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class MyModelFilters(BaseModel):
    id: int

class MyModelDAO(BaseDAO[MyModel]):
    model = MyModel

async def example(session: AsyncSession, record_id: int):
    filters = MyModelFilters(id=record_id)
    deleted_count = await MyModelDAO.delete(session=session, filters=filters)
    print(f"Удалено {deleted_count} записей")
```

### `count`

```python
    @classmethod
    async def count(cls, session: AsyncSession, filters: BaseModel | None = None):
        """Подсчитать количество записей

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (BaseModel | None): Pydantic модель с фильтрами для подсчета. Может быть None.

        Returns:
            int: Количество записей.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении запроса к базе данных.
        """
```

**Назначение**:
Метод подсчитывает количество записей в базе данных по указанным фильтрам.

**Как работает функция**:
- Преобразует фильтры из Pydantic модели в словарь, если фильтры указаны.
- Логирует начало подсчета записей.
- Формирует запрос к базе данных на подсчет записей с указанными фильтрами.
- Выполняет запрос и получает результат.
- Логирует количество найденных записей.
- В случае ошибки логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from bot.dao.base import BaseDAO
from bot.dao.database import Base

class MyModel(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class MyModelFilters(BaseModel):
    name: str

class MyModelDAO(BaseDAO[MyModel]):
    model = MyModel

async def example(session: AsyncSession, name: str):
    filters = MyModelFilters(name=name)
    count = await MyModelDAO.count(session=session, filters=filters)
    print(f"Найдено {count} записей")
```

### `paginate`

```python
    @classmethod
    async def paginate(cls, session: AsyncSession, page: int = 1, page_size: int = 10, filters: BaseModel = None):
        """Пагинация записей

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            page (int): Номер страницы. По умолчанию 1.
            page_size (int): Размер страницы. По умолчанию 10.
            filters (BaseModel | None): Pydantic модель с фильтрами для поиска. Может быть None.

        Returns:
            List[T]: Список записей на странице.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении запроса к базе данных.
        """
```

**Назначение**:
Метод выполняет пагинацию записей в базе данных по указанным фильтрам.

**Как работает функция**:
- Преобразует фильтры из Pydantic модели в словарь, если фильтры указаны.
- Логирует начало пагинации записей.
- Формирует запрос к базе данных на выборку записей с указанными фильтрами, номером страницы и размером страницы.
- Выполняет запрос и получает результат.
- Логирует количество найденных записей на странице.
- В случае ошибки логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from bot.dao.base import BaseDAO
from bot.dao.database import Base

class MyModel(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class MyModelFilters(BaseModel):
    name: str

class MyModelDAO(BaseDAO[MyModel]):
    model = MyModel

async def example(session: AsyncSession, name: str, page: int, page_size: int):
    filters = MyModelFilters(name=name)
    records = await MyModelDAO.paginate(session=session, page=page, page_size=page_size, filters=filters)
    print(f"Найдено {len(records)} записей на странице {page}")
    for record in records:
        print(record)
```

### `find_by_ids`

```python
    @classmethod
    async def find_by_ids(cls, session: AsyncSession, ids: List[int]) -> List[Any]:
        """Найти несколько записей по списку ID

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            ids (List[int]): Список ID записей для поиска.

        Returns:
            List[Any]: Список найденных записей.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении запроса к базе данных.
        """
```

**Назначение**:
Метод выполняет поиск нескольких записей в базе данных по списку ID.

**Как работает функция**:
- Логирует начало поиска записей.
- Формирует запрос к базе данных на выборку записей с указанными ID.
- Выполняет запрос и получает результат.
- Логирует количество найденных записей.
- В случае ошибки логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования
from sqlalchemy.ext.asyncio import AsyncSession
from bot.dao.base import BaseDAO
from bot.dao.database import Base

class MyModel(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class MyModelDAO(BaseDAO[MyModel]):
    model = MyModel

async def example(session: AsyncSession, ids: List[int]):
    records = await MyModelDAO.find_by_ids(session=session, ids=ids)
    print(f"Найдено {len(records)} записей по списку ID.")
    for record in records:
        print(record)
```

### `upsert`

```python
    @classmethod
    async def upsert(cls, session: AsyncSession, unique_fields: List[str], values: BaseModel):
        """Создать запись или обновить существующую

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            unique_fields (List[str]): Список уникальных полей для поиска существующей записи.
            values (BaseModel): Pydantic модель со значениями для создания или обновления.

        Returns:
            T: Созданная или обновленная запись.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении запроса к базе данных.
        """
```

**Назначение**:
Метод создает новую запись в базе данных или обновляет существующую, если запись с указанными уникальными полями уже существует.

**Как работает функция**:
- Преобразует значения из Pydantic модели в словарь.
- Формирует фильтр на основе уникальных полей.
- Логирует начало операции upsert.
- Пытается найти существующую запись по фильтру.
- Если запись найдена, обновляет ее значения.
- Если запись не найдена, создает новую запись.
- Фиксирует изменения в базе данных.
- Логирует успешное выполнение операции.
- В случае ошибки откатывает транзакцию, логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from bot.dao.base import BaseDAO
from bot.dao.database import Base

class MyModel(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

class MyModelCreate(BaseModel):
    name: str
    email: str

class MyModelDAO(BaseDAO[MyModel]):
    model = MyModel

async def example(session: AsyncSession, name: str, email: str):
    values = MyModelCreate(name=name, email=email)
    unique_fields = ['email']
    record = await MyModelDAO.upsert(session=session, unique_fields=unique_fields, values=values)
    print(f"Создана или обновлена запись: {record}")
```

### `bulk_update`

```python
    @classmethod
    async def bulk_update(cls, session: AsyncSession, records: List[BaseModel]) -> int:
        """Массовое обновление записей

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            records (List[BaseModel]): Список Pydantic моделей со значениями для обновления.

        Returns:
            int: Количество обновленных записей.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении запроса к базе данных.
        """
```

**Назначение**:
Метод выполняет массовое обновление записей в базе данных.

**Как работает функция**:
- Логирует начало массового обновления записей.
- Итерируется по списку записей.
- Для каждой записи формирует запрос на обновление.
- Выполняет запрос и получает результат.
- Фиксирует изменения в базе данных.
- Логирует количество обновленных записей.
- В случае ошибки откатывает транзакцию, логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from bot.dao.base import BaseDAO
from bot.dao.database import Base

class MyModel(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class MyModelUpdate(BaseModel):
    id: int
    name: str

class MyModelDAO(BaseDAO[MyModel]):
    model = MyModel

async def example(session: AsyncSession, updates: List[dict]):
    records = [MyModelUpdate(**data) for data in updates]
    updated_count = await MyModelDAO.bulk_update(session=session, records=records)
    print(f"Обновлено {updated_count} записей")