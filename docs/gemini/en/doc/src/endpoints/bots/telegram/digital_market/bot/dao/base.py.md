# Модуль BaseDAO

## Обзор

Модуль `BaseDAO` предоставляет базовый класс для работы с данными в базе данных, используя SQLAlchemy. 
Он содержит набор универсальных методов для выполнения общих операций с данными, таких как 
поиск, добавление, обновление, удаление и подсчет записей. 

## Детали

`BaseDAO` является абстрактным классом, который должен быть расширен для работы со 
конкретными моделями данных. Он использует дженерики для работы с любым типом модели, 
который наследует от `Base`.

## Классы

### `BaseDAO`

**Описание**: Базовый класс для работы с данными в базе данных. 
**Inherits**: `Generic[T]`
**Attributes**:
- `model` (type[T]): Тип модели данных, с которой работает DAO.

**Methods**:

#### `find_one_or_none_by_id(cls, data_id: int, session: AsyncSession)`

**Описание**: Находит запись по ID.

**Параметры**:
- `data_id` (int): ID записи.
- `session` (AsyncSession): Сессия SQLAlchemy.

**Возвращает**:
- `T | None`: Запись с указанным ID или `None`, если запись не найдена.

**Raises**:
- `SQLAlchemyError`: В случае ошибки при выполнении запроса.

#### `find_one_or_none(cls, session: AsyncSession, filters: BaseModel)`

**Описание**: Находит одну запись по фильтрам.

**Параметры**:
- `session` (AsyncSession): Сессия SQLAlchemy.
- `filters` (BaseModel): Объект Pydantic, содержащий фильтры.

**Возвращает**:
- `T | None`: Запись, соответствующая фильтрам, или `None`, если запись не найдена.

**Raises**:
- `SQLAlchemyError`: В случае ошибки при выполнении запроса.

#### `find_all(cls, session: AsyncSession, filters: BaseModel | None = None)`

**Описание**: Находит все записи по фильтрам.

**Параметры**:
- `session` (AsyncSession): Сессия SQLAlchemy.
- `filters` (BaseModel | None, optional): Объект Pydantic, содержащий фильтры. По умолчанию `None`.

**Возвращает**:
- `List[T]`: Список записей, соответствующих фильтрам.

**Raises**:
- `SQLAlchemyError`: В случае ошибки при выполнении запроса.

#### `add(cls, session: AsyncSession, values: BaseModel)`

**Описание**: Добавляет одну запись.

**Параметры**:
- `session` (AsyncSession): Сессия SQLAlchemy.
- `values` (BaseModel): Объект Pydantic, содержащий значения для новой записи.

**Возвращает**:
- `T`: Новая добавленная запись.

**Raises**:
- `SQLAlchemyError`: В случае ошибки при добавлении записи.

#### `add_many(cls, session: AsyncSession, instances: List[BaseModel])`

**Описание**: Добавляет несколько записей.

**Параметры**:
- `session` (AsyncSession): Сессия SQLAlchemy.
- `instances` (List[BaseModel]): Список объектов Pydantic, содержащих значения для новых записей.

**Возвращает**:
- `List[T]`: Список добавленных записей.

**Raises**:
- `SQLAlchemyError`: В случае ошибки при добавлении записей.

#### `update(cls, session: AsyncSession, filters: BaseModel, values: BaseModel)`

**Описание**: Обновляет записи по фильтрам.

**Параметры**:
- `session` (AsyncSession): Сессия SQLAlchemy.
- `filters` (BaseModel): Объект Pydantic, содержащий фильтры.
- `values` (BaseModel): Объект Pydantic, содержащий значения для обновления.

**Возвращает**:
- `int`: Количество обновленных записей.

**Raises**:
- `SQLAlchemyError`: В случае ошибки при обновлении записей.

#### `delete(cls, session: AsyncSession, filters: BaseModel)`

**Описание**: Удаляет записи по фильтру.

**Параметры**:
- `session` (AsyncSession): Сессия SQLAlchemy.
- `filters` (BaseModel): Объект Pydantic, содержащий фильтры.

**Возвращает**:
- `int`: Количество удаленных записей.

**Raises**:
- `SQLAlchemyError`: В случае ошибки при удалении записей.
- `ValueError`: Если не указан хотя бы один фильтр.

#### `count(cls, session: AsyncSession, filters: BaseModel | None = None)`

**Описание**: Подсчитывает количество записей.

**Параметры**:
- `session` (AsyncSession): Сессия SQLAlchemy.
- `filters` (BaseModel | None, optional): Объект Pydantic, содержащий фильтры. По умолчанию `None`.

**Возвращает**:
- `int`: Количество записей, соответствующих фильтрам.

**Raises**:
- `SQLAlchemyError`: В случае ошибки при подсчете записей.

#### `paginate(cls, session: AsyncSession, page: int = 1, page_size: int = 10, filters: BaseModel = None)`

**Описание**: Пагинация записей.

**Параметры**:
- `session` (AsyncSession): Сессия SQLAlchemy.
- `page` (int, optional): Номер страницы. По умолчанию `1`.
- `page_size` (int, optional): Размер страницы. По умолчанию `10`.
- `filters` (BaseModel, optional): Объект Pydantic, содержащий фильтры. По умолчанию `None`.

**Возвращает**:
- `List[T]`: Список записей для текущей страницы.

**Raises**:
- `SQLAlchemyError`: В случае ошибки при пагинации.

#### `find_by_ids(cls, session: AsyncSession, ids: List[int]) -> List[Any]`

**Описание**: Найти несколько записей по списку ID

**Параметры**:
- `session` (AsyncSession): Сессия SQLAlchemy.
- `ids` (List[int]): Список ID записей.

**Возвращает**:
- `List[Any]`: Список записей, соответствующих ID из списка.

**Raises**:
- `SQLAlchemyError`: В случае ошибки при поиске записей по списку ID.

#### `upsert(cls, session: AsyncSession, unique_fields: List[str], values: BaseModel)`

**Описание**: Создать запись или обновить существующую.

**Параметры**:
- `session` (AsyncSession): Сессия SQLAlchemy.
- `unique_fields` (List[str]): Список полей, которые определяют уникальность записи.
- `values` (BaseModel): Объект Pydantic, содержащий значения для записи.

**Возвращает**:
- `T`: Созданная или обновленная запись.

**Raises**:
- `SQLAlchemyError`: В случае ошибки при upsert.

#### `bulk_update(cls, session: AsyncSession, records: List[BaseModel]) -> int`

**Описание**: Массовое обновление записей.

**Параметры**:
- `session` (AsyncSession): Сессия SQLAlchemy.
- `records` (List[BaseModel]): Список объектов Pydantic, содержащих значения для обновления.

**Возвращает**:
- `int`: Количество обновленных записей.

**Raises**:
- `SQLAlchemyError`: В случае ошибки при массовом обновлении записей.

## Примеры

```python
from bot.dao.database import Base
from bot.dao.base import BaseDAO

# Определение модели данных
class MyModel(Base):
    # ... определение полей

# Создание DAO для MyModel
class MyModelDAO(BaseDAO[MyModel]):
    model = MyModel

# ... дальнейшие действия, используя методы BaseDAO
```