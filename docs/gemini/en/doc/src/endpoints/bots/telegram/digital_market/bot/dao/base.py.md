# Модуль `base.py`

## Обзор

Модуль `base.py` содержит базовый класс `BaseDAO` для работы с базой данных в асинхронном режиме. Он предоставляет набор методов для выполнения операций CRUD (создание, чтение, обновление, удаление) с использованием SQLAlchemy. Класс `BaseDAO` является универсальным и может использоваться с любой моделью, наследующей от `Base`.

## Детали

Модуль содержит класс `BaseDAO`, который предоставляет методы для выполнения основных операций с базой данных, таких как поиск, добавление, обновление и удаление записей. Все методы являются асинхронными и используют `AsyncSession` для взаимодействия с базой данных.

## Классы

### `BaseDAO`

**Описание**:
Базовый класс для доступа к данным. Предоставляет методы для выполнения операций CRUD с использованием SQLAlchemy.

**Наследуется**:
Не наследуется от других классов.

**Атрибуты**:
- `model` (type[T]): Тип модели, с которой работает DAO.

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
- `find_by_ids(cls, session: AsyncSession, ids: List[int]) -> List[Any]`: Находит несколько записей по списку ID.
- `upsert(cls, session: AsyncSession, unique_fields: List[str], values: BaseModel)`: Создает запись или обновляет существующую.
- `bulk_update(cls, session: AsyncSession, records: List[BaseModel]) -> int`: Массовое обновление записей.

## Методы класса `BaseDAO`

### `find_one_or_none_by_id`

```python
@classmethod
async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession):
    """
    Находит запись по ID.

    Args:
        data_id (int): ID записи.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        T | None: Найденная запись или None, если запись не найдена.

    Raises:
        SQLAlchemyError: Если возникает ошибка при поиске записи.

    Как работает функция:
    - Функция формирует запрос на выборку записи из базы данных по указанному ID.
    - Выполняет запрос с использованием асинхронной сессии.
    - Возвращает найденную запись, если она существует, или None, если запись не найдена.
    - Логирует информацию о поиске и результате.
    """
    ...
```

### `find_one_or_none`

```python
@classmethod
async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel):
    """
    Найти одну запись по фильтрам.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        filters (BaseModel): Фильтры для поиска записи.

    Returns:
        T | None: Найденная запись или None, если запись не найдена.

    Raises:
        SQLAlchemyError: Если возникает ошибка при поиске записи.

    Как работает функция:
    - Функция преобразует фильтры из BaseModel в словарь.
    - Формирует запрос на выборку записи из базы данных по указанным фильтрам.
    - Выполняет запрос с использованием асинхронной сессии.
    - Возвращает найденную запись, если она существует, или None, если запись не найдена.
    - Логирует информацию о поиске и результате.
    """
    ...
```

### `find_all`

```python
@classmethod
async def find_all(cls, session: AsyncSession, filters: BaseModel | None = None):
    """
    Найти все записи по фильтрам.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        filters (BaseModel | None, optional): Фильтры для поиска записей. Defaults to None.

    Returns:
        List[T]: Список найденных записей.

    Raises:
        SQLAlchemyError: Если возникает ошибка при поиске записей.

    Как работает функция:
    - Функция преобразует фильтры из BaseModel в словарь.
    - Формирует запрос на выборку всех записей из базы данных по указанным фильтрам.
    - Выполняет запрос с использованием асинхронной сессии.
    - Возвращает список найденных записей.
    - Логирует информацию о поиске и результате.
    """
    ...
```

### `add`

```python
@classmethod
async def add(cls, session: AsyncSession, values: BaseModel):
    """
    Добавить одну запись.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        values (BaseModel): Значения для добавления записи.

    Returns:
        T: Новая запись.

    Raises:
        SQLAlchemyError: Если возникает ошибка при добавлении записи.

    Как работает функция:
    - Функция преобразует значения из BaseModel в словарь.
    - Создает новый экземпляр модели с указанными значениями.
    - Добавляет новую запись в базу данных.
    - Фиксирует изменения в базе данных.
    - Логирует информацию о добавлении записи.
    """
    ...
```

### `add_many`

```python
@classmethod
async def add_many(cls, session: AsyncSession, instances: List[BaseModel]):
    """
    Добавить несколько записей.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        instances (List[BaseModel]): Список экземпляров BaseModel для добавления.

    Returns:
        List[T]: Список новых записей.

    Raises:
        SQLAlchemyError: Если возникает ошибка при добавлении записей.

    Как работает функция:
    - Функция преобразует значения из списка BaseModel в список словарей.
    - Создает новые экземпляры модели с указанными значениями.
    - Добавляет новые записи в базу данных.
    - Фиксирует изменения в базе данных.
    - Логирует информацию о добавлении записей.
    """
    ...
```

### `update`

```python
@classmethod
async def update(cls, session: AsyncSession, filters: BaseModel, values: BaseModel):
    """
    Обновить записи по фильтрам.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        filters (BaseModel): Фильтры для обновления записей.
        values (BaseModel): Значения для обновления записей.

    Returns:
        int: Количество обновленных записей.

    Raises:
        SQLAlchemyError: Если возникает ошибка при обновлении записей.

    Как работает функция:
    - Функция преобразует фильтры и значения из BaseModel в словари.
    - Формирует запрос на обновление записей в базе данных по указанным фильтрам с указанными значениями.
    - Выполняет запрос с использованием асинхронной сессии.
    - Фиксирует изменения в базе данных.
    - Возвращает количество обновленных записей.
    - Логирует информацию об обновлении записей.
    """
    ...
```

### `delete`

```python
@classmethod
async def delete(cls, session: AsyncSession, filters: BaseModel):
    """
    Удалить записи по фильтру.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        filters (BaseModel): Фильтры для удаления записей.

    Returns:
        int: Количество удаленных записей.

    Raises:
        SQLAlchemyError: Если возникает ошибка при удалении записей.
        ValueError: Если не указан ни один фильтр для удаления.

    Как работает функция:
    - Функция преобразует фильтры из BaseModel в словарь.
    - Формирует запрос на удаление записей из базы данных по указанным фильтрам.
    - Выполняет запрос с использованием асинхронной сессии.
    - Фиксирует изменения в базе данных.
    - Возвращает количество удаленных записей.
    - Логирует информацию об удалении записей.
    """
    ...
```

### `count`

```python
@classmethod
async def count(cls, session: AsyncSession, filters: BaseModel | None = None):
    """
    Подсчитать количество записей.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        filters (BaseModel | None, optional): Фильтры для подсчета записей. Defaults to None.

    Returns:
        int: Количество записей.

    Raises:
        SQLAlchemyError: Если возникает ошибка при подсчете записей.

    Как работает функция:
    - Функция преобразует фильтры из BaseModel в словарь.
    - Формирует запрос на подсчет количества записей в базе данных по указанным фильтрам.
    - Выполняет запрос с использованием асинхронной сессии.
    - Возвращает количество записей.
    - Логирует информацию о подсчете записей.
    """
    ...
```

### `paginate`

```python
@classmethod
async def paginate(cls, session: AsyncSession, page: int = 1, page_size: int = 10, filters: BaseModel = None):
    """
    Пагинация записей.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        page (int, optional): Номер страницы. Defaults to 1.
        page_size (int, optional): Размер страницы. Defaults to 10.
        filters (BaseModel, optional): Фильтры для пагинации записей. Defaults to None.

    Returns:
        List[T]: Список записей на странице.

    Raises:
        SQLAlchemyError: Если возникает ошибка при пагинации записей.

    Как работает функция:
    - Функция преобразует фильтры из BaseModel в словарь.
    - Формирует запрос на выборку записей из базы данных с учетом пагинации и фильтров.
    - Выполняет запрос с использованием асинхронной сессии.
    - Возвращает список записей на странице.
    - Логирует информацию о пагинации записей.
    """
    ...
```

### `find_by_ids`

```python
@classmethod
async def find_by_ids(cls, session: AsyncSession, ids: List[int]) -> List[Any]:
    """
    Найти несколько записей по списку ID.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        ids (List[int]): Список ID записей.

    Returns:
        List[Any]: Список найденных записей.

    Raises:
        SQLAlchemyError: Если возникает ошибка при поиске записей по списку ID.

    Как работает функция:
    - Функция формирует запрос на выборку записей из базы данных по списку ID.
    - Выполняет запрос с использованием асинхронной сессии.
    - Возвращает список найденных записей.
    - Логирует информацию о поиске записей.
    """
    ...
```

### `upsert`

```python
@classmethod
async def upsert(cls, session: AsyncSession, unique_fields: List[str], values: BaseModel):
    """
    Создать запись или обновить существующую.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        unique_fields (List[str]): Список уникальных полей для поиска существующей записи.
        values (BaseModel): Значения для создания или обновления записи.

    Returns:
        T: Созданная или обновленная запись.

    Raises:
        SQLAlchemyError: Если возникает ошибка при выполнении операции.

    Как работает функция:
    - Функция ищет существующую запись по уникальным полям.
    - Если запись существует, она обновляется.
    - Если запись не существует, она создается.
    - Логирует информацию о создании или обновлении записи.
    """
    ...
```

### `bulk_update`

```python
@classmethod
async def bulk_update(cls, session: AsyncSession, records: List[BaseModel]) -> int:
    """
    Массовое обновление записей.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        records (List[BaseModel]): Список записей для обновления.

    Returns:
        int: Количество обновленных записей.

    Raises:
        SQLAlchemyError: Если возникает ошибка при массовом обновлении.

    Как работает функция:
    - Функция итерируется по списку записей.
    - Для каждой записи формирует запрос на обновление.
    - Выполняет запросы на обновление.
    - Фиксирует изменения в базе данных.
    - Возвращает количество обновленных записей.
    - Логирует информацию о массовом обновлении.
    """
    ...
```