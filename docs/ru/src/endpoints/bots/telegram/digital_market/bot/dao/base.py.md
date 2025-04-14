# Модуль для базового доступа к данным (DAO)
=================================================

Модуль содержит класс `BaseDAO`, который предоставляет базовые операции для доступа к данным в базе данных, такие как поиск, добавление, обновление и удаление записей.

## Обзор

Этот модуль предоставляет абстрактный базовый класс `BaseDAO`, который может быть использован для создания DAO (Data Access Object) для конкретных моделей базы данных. Он включает в себя общие методы для выполнения операций CRUD (Create, Read, Update, Delete) и пагинации.

## Подробнее

`BaseDAO` использует `SQLAlchemy` для взаимодействия с базой данных и предоставляет асинхронные методы для выполнения запросов. Класс является универсальным (Generic) и принимает в качестве параметра тип модели (`T`), которая должна быть наследником класса `Base` из `sqlalchemy`.

## Классы

### `BaseDAO`

**Описание**:
Базовый класс для объектов доступа к данным. Предоставляет общие методы для работы с базой данных, такие как поиск, добавление, обновление и удаление записей.

**Наследует**:
Не наследует никакие классы напрямую.

**Атрибуты**:
- `model` (type[T]): Тип модели, с которой работает DAO.

**Методы**:
- `find_one_or_none_by_id(data_id: int, session: AsyncSession)`: Найти одну запись по ID.
- `find_one_or_none(session: AsyncSession, filters: BaseModel)`: Найти одну запись по фильтрам.
- `find_all(session: AsyncSession, filters: BaseModel | None = None)`: Найти все записи по фильтрам.
- `add(session: AsyncSession, values: BaseModel)`: Добавить одну запись.
- `add_many(session: AsyncSession, instances: List[BaseModel])`: Добавить несколько записей.
- `update(session: AsyncSession, filters: BaseModel, values: BaseModel)`: Обновить записи по фильтрам.
- `delete(session: AsyncSession, filters: BaseModel)`: Удалить записи по фильтру.
- `count(session: AsyncSession, filters: BaseModel | None = None)`: Подсчитать количество записей.
- `paginate(session: AsyncSession, page: int = 1, page_size: int = 10, filters: BaseModel = None)`: Пагинация записей.
- `find_by_ids(session: AsyncSession, ids: List[int]) -> List[Any]`: Найти несколько записей по списку ID.
- `upsert(session: AsyncSession, unique_fields: List[str], values: BaseModel)`: Создать запись или обновить существующую.
- `bulk_update(session: AsyncSession, records: List[BaseModel]) -> int`: Массовое обновление записей.

## Методы класса

### `find_one_or_none_by_id`

```python
@classmethod
async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession):
    """
    Находит запись в базе данных по указанному ID.

    Args:
        data_id (int): ID записи для поиска.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов.

    Returns:
        T | None: Найденная запись или None, если запись не найдена.

    Raises:
        SQLAlchemyError: Если возникает ошибка при выполнении запроса к базе данных.

    Как работает функция:
    - Логирует начало поиска записи по ID.
    - Формирует запрос к базе данных для поиска записи с указанным ID.
    - Выполняет запрос и возвращает найденную запись, если она существует, иначе возвращает None.
    - В случае ошибки логирует ошибку и вызывает исключение SQLAlchemyError.

    Примеры:
    ```python
    # Пример вызова функции
    record = await BaseDAO.find_one_or_none_by_id(data_id=123, session=session)
    if record:
        print(f"Найдена запись: {record}")
    else:
        print("Запись не найдена")
    ```
    """
    ...
```

### `find_one_or_none`

```python
@classmethod
async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel):
    """
    Находит одну запись в базе данных по указанным фильтрам.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов.
        filters (BaseModel): Объект Pydantic BaseModel, содержащий фильтры для поиска.

    Returns:
        T | None: Найденная запись или None, если запись не найдена.

    Raises:
        SQLAlchemyError: Если возникает ошибка при выполнении запроса к базе данных.

    Как работает функция:
    - Преобразует фильтры из объекта BaseModel в словарь.
    - Логирует начало поиска записи по фильтрам.
    - Формирует запрос к базе данных для поиска записи с указанными фильтрами.
    - Выполняет запрос и возвращает найденную запись, если она существует, иначе возвращает None.
    - В случае ошибки логирует ошибку и вызывает исключение SQLAlchemyError.

    Примеры:
    ```python
    # Пример вызова функции
    class MyFilter(BaseModel):
        name: str = "example"
        value: int = 123

    filters = MyFilter(name="test", value=456)
    record = await BaseDAO.find_one_or_none(session=session, filters=filters)
    if record:
        print(f"Найдена запись: {record}")
    else:
        print("Запись не найдена")
    ```
    """
    ...
```

### `find_all`

```python
@classmethod
async def find_all(cls, session: AsyncSession, filters: BaseModel | None = None):
    """
    Находит все записи в базе данных по указанным фильтрам.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов.
        filters (BaseModel | None, optional): Объект Pydantic BaseModel, содержащий фильтры для поиска. По умолчанию None.

    Returns:
        List[T]: Список найденных записей.

    Raises:
        SQLAlchemyError: Если возникает ошибка при выполнении запроса к базе данных.

    Как работает функция:
    - Преобразует фильтры из объекта BaseModel в словарь, если фильтры предоставлены.
    - Логирует начало поиска всех записей по фильтрам.
    - Формирует запрос к базе данных для поиска записей с указанными фильтрами.
    - Выполняет запрос и возвращает список найденных записей.
    - В случае ошибки логирует ошибку и вызывает исключение SQLAlchemyError.

    Примеры:
    ```python
    # Пример вызова функции
    class MyFilter(BaseModel):
        name: str = "example"
        value: int = 123

    filters = MyFilter(name="test")
    records = await BaseDAO.find_all(session=session, filters=filters)
    print(f"Найдено {len(records)} записей")
    ```
    """
    ...
```

### `add`

```python
@classmethod
async def add(cls, session: AsyncSession, values: BaseModel):
    """
    Добавляет одну запись в базу данных.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов.
        values (BaseModel): Объект Pydantic BaseModel, содержащий значения для добавления.

    Returns:
        T: Новая добавленная запись.

    Raises:
        SQLAlchemyError: Если возникает ошибка при добавлении записи в базу данных.

    Как работает функция:
    - Преобразует значения из объекта BaseModel в словарь.
    - Логирует начало добавления записи с указанными параметрами.
    - Создает новый экземпляр модели с указанными значениями.
    - Добавляет новый экземпляр в сессию и выполняет flush для сохранения изменений в базе данных.
    - В случае ошибки выполняет rollback и логирует ошибку, затем вызывает исключение SQLAlchemyError.

    Примеры:
    ```python
    # Пример вызова функции
    class MyValues(BaseModel):
        name: str = "example"
        value: int = 123

    values = MyValues(name="test", value=456)
    new_record = await BaseDAO.add(session=session, values=values)
    print(f"Добавлена запись: {new_record}")
    ```
    """
    ...
```

### `add_many`

```python
@classmethod
async def add_many(cls, session: AsyncSession, instances: List[BaseModel]):
    """
    Добавляет несколько записей в базу данных.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов.
        instances (List[BaseModel]): Список объектов Pydantic BaseModel, содержащих значения для добавления.

    Returns:
        List[T]: Список новых добавленных записей.

    Raises:
        SQLAlchemyError: Если возникает ошибка при добавлении записей в базу данных.

    Как работает функция:
    - Преобразует значения из списка объектов BaseModel в список словарей.
    - Логирует начало добавления нескольких записей.
    - Создает новые экземпляры модели с указанными значениями.
    - Добавляет все новые экземпляры в сессию и выполняет flush для сохранения изменений в базе данных.
    - В случае ошибки выполняет rollback и логирует ошибку, затем вызывает исключение SQLAlchemyError.

    Примеры:
    ```python
    # Пример вызова функции
    class MyValues(BaseModel):
        name: str = "example"
        value: int = 123

    instances = [MyValues(name="test1", value=456), MyValues(name="test2", value=789)]
    new_records = await BaseDAO.add_many(session=session, instances=instances)
    print(f"Добавлено {len(new_records)} записей")
    ```
    """
    ...
```

### `update`

```python
@classmethod
async def update(cls, session: AsyncSession, filters: BaseModel, values: BaseModel):
    """
    Обновляет записи в базе данных по указанным фильтрам.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов.
        filters (BaseModel): Объект Pydantic BaseModel, содержащий фильтры для обновления.
        values (BaseModel): Объект Pydantic BaseModel, содержащий значения для обновления.

    Returns:
        int: Количество обновленных записей.

    Raises:
        SQLAlchemyError: Если возникает ошибка при обновлении записей в базе данных.

    Как работает функция:
    - Преобразует фильтры и значения из объектов BaseModel в словари.
    - Логирует начало обновления записей по фильтру с указанными параметрами.
    - Формирует запрос к базе данных для обновления записей с указанными фильтрами и значениями.
    - Выполняет запрос и возвращает количество обновленных записей.
    - В случае ошибки выполняет rollback и логирует ошибку, затем вызывает исключение SQLAlchemyError.

    Примеры:
    ```python
    # Пример вызова функции
    class MyFilter(BaseModel):
        name: str = "example"

    class MyValues(BaseModel):
        value: int = 123

    filters = MyFilter(name="test")
    values = MyValues(value=456)
    updated_count = await BaseDAO.update(session=session, filters=filters, values=values)
    print(f"Обновлено {updated_count} записей")
    ```
    """
    ...
```

### `delete`

```python
@classmethod
async def delete(cls, session: AsyncSession, filters: BaseModel):
    """
    Удаляет записи из базы данных по указанному фильтру.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов.
        filters (BaseModel): Объект Pydantic BaseModel, содержащий фильтры для удаления.

    Returns:
        int: Количество удаленных записей.

    Raises:
        ValueError: Если не предоставлен ни один фильтр для удаления.
        SQLAlchemyError: Если возникает ошибка при удалении записей из базы данных.

    Как работает функция:
    - Преобразует фильтры из объекта BaseModel в словарь.
    - Логирует начало удаления записей по фильтру.
    - Проверяет, что предоставлен хотя бы один фильтр для удаления, иначе вызывает ValueError.
    - Формирует запрос к базе данных для удаления записей с указанными фильтрами.
    - Выполняет запрос и возвращает количество удаленных записей.
    - В случае ошибки выполняет rollback и логирует ошибку, затем вызывает исключение SQLAlchemyError.

    Примеры:
    ```python
    # Пример вызова функции
    class MyFilter(BaseModel):
        name: str = "example"

    filters = MyFilter(name="test")
    deleted_count = await BaseDAO.delete(session=session, filters=filters)
    print(f"Удалено {deleted_count} записей")
    ```
    """
    ...
```

### `count`

```python
@classmethod
async def count(cls, session: AsyncSession, filters: BaseModel | None = None):
    """
    Подсчитывает количество записей в базе данных по указанным фильтрам.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов.
        filters (BaseModel | None, optional): Объект Pydantic BaseModel, содержащий фильтры для подсчета. По умолчанию None.

    Returns:
        int: Количество записей, соответствующих фильтрам.

    Raises:
        SQLAlchemyError: Если возникает ошибка при выполнении запроса к базе данных.

    Как работает функция:
    - Преобразует фильтры из объекта BaseModel в словарь, если фильтры предоставлены.
    - Логирует начало подсчета количества записей по фильтру.
    - Формирует запрос к базе данных для подсчета записей с указанными фильтрами.
    - Выполняет запрос и возвращает количество записей.
    - В случае ошибки логирует ошибку и вызывает исключение SQLAlchemyError.

    Примеры:
    ```python
    # Пример вызова функции
    class MyFilter(BaseModel):
        name: str = "example"

    filters = MyFilter(name="test")
    count = await BaseDAO.count(session=session, filters=filters)
    print(f"Найдено {count} записей")
    ```
    """
    ...
```

### `paginate`

```python
@classmethod
async def paginate(cls, session: AsyncSession, page: int = 1, page_size: int = 10, filters: BaseModel = None):
    """
    Выполняет пагинацию записей в базе данных по указанным фильтрам.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов.
        page (int, optional): Номер страницы для отображения. По умолчанию 1.
        page_size (int, optional): Количество записей на странице. По умолчанию 10.
        filters (BaseModel | None, optional): Объект Pydantic BaseModel, содержащий фильтры для пагинации. По умолчанию None.

    Returns:
        List[T]: Список записей на указанной странице.

    Raises:
        SQLAlchemyError: Если возникает ошибка при выполнении запроса к базе данных.

    Как работает функция:
    - Преобразует фильтры из объекта BaseModel в словарь, если фильтры предоставлены.
    - Логирует начало пагинации записей по фильтру с указанием страницы и размера страницы.
    - Формирует запрос к базе данных для получения записей с учетом пагинации и фильтров.
    - Выполняет запрос и возвращает список записей на указанной странице.
    - В случае ошибки логирует ошибку и вызывает исключение SQLAlchemyError.

    Примеры:
    ```python
    # Пример вызова функции
    class MyFilter(BaseModel):
        name: str = "example"

    filters = MyFilter(name="test")
    records = await BaseDAO.paginate(session=session, page=2, page_size=20, filters=filters)
    print(f"Найдено {len(records)} записей на странице 2")
    ```
    """
    ...
```

### `find_by_ids`

```python
@classmethod
async def find_by_ids(cls, session: AsyncSession, ids: List[int]) -> List[Any]:
    """
    Находит несколько записей по списку ID.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов.
        ids (List[int]): Список ID записей для поиска.

    Returns:
        List[Any]: Список найденных записей.

    Raises:
        SQLAlchemyError: Если возникает ошибка при выполнении запроса к базе данных.

    Как работает функция:
    - Логирует начало поиска записей по списку ID.
    - Формирует запрос к базе данных для поиска записей с указанными ID.
    - Выполняет запрос и возвращает список найденных записей.
    - В случае ошибки логирует ошибку и вызывает исключение SQLAlchemyError.

    Примеры:
    ```python
    # Пример вызова функции
    ids = [1, 2, 3]
    records = await BaseDAO.find_by_ids(session=session, ids=ids)
    print(f"Найдено {len(records)} записей")
    ```
    """
    ...
```

### `upsert`

```python
@classmethod
async def upsert(cls, session: AsyncSession, unique_fields: List[str], values: BaseModel):
    """
    Создает запись или обновляет существующую запись на основе уникальных полей.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов.
        unique_fields (List[str]): Список уникальных полей, по которым выполняется поиск существующей записи.
        values (BaseModel): Объект Pydantic BaseModel, содержащий значения для создания или обновления записи.

    Returns:
        T: Созданная или обновленная запись.

    Raises:
        SQLAlchemyError: Если возникает ошибка при выполнении запроса к базе данных.

    Как работает функция:
    - Преобразует значения из объекта BaseModel в словарь.
    - Формирует словарь с фильтрами на основе уникальных полей.
    - Логирует начало операции upsert.
    - Пытается найти существующую запись по уникальным полям.
    - Если запись существует, обновляет ее значениями из `values` и выполняет flush.
    - Если запись не существует, создает новую запись с значениями из `values` и выполняет flush.
    - В случае ошибки выполняет rollback и логирует ошибку, затем вызывает исключение SQLAlchemyError.

    Примеры:
    ```python
    # Пример вызова функции
    class MyValues(BaseModel):
        name: str = "example"
        value: int = 123

    values = MyValues(name="test", value=456)
    unique_fields = ["name"]
    record = await BaseDAO.upsert(session=session, unique_fields=unique_fields, values=values)
    print(f"Создана или обновлена запись: {record}")
    ```
    """
    ...
```

### `bulk_update`

```python
@classmethod
async def bulk_update(cls, session: AsyncSession, records: List[BaseModel]) -> int:
    """
    Массовое обновление записей в базе данных.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов.
        records (List[BaseModel]): Список объектов Pydantic BaseModel, содержащих значения для обновления. Каждый объект должен иметь поле 'id'.

    Returns:
        int: Количество обновленных записей.

    Raises:
        SQLAlchemyError: Если возникает ошибка при выполнении запроса к базе данных.

    Как работает функция:
    - Логирует начало массового обновления записей.
    - Итерируется по списку записей.
    - Для каждой записи проверяет наличие поля 'id'. Если поле отсутствует, запись пропускается.
    - Формирует запрос к базе данных для обновления записи с указанным ID.
    - Выполняет запрос и увеличивает счетчик обновленных записей.
    - После завершения итерации выполняет flush для сохранения изменений в базе данных.
    - В случае ошибки выполняет rollback и логирует ошибку, затем вызывает исключение SQLAlchemyError.

    Примеры:
    ```python
    # Пример вызова функции
    class MyValues(BaseModel):
        id: int
        name: str
        value: int

    records = [
        MyValues(id=1, name="test1", value=456),
        MyValues(id=2, name="test2", value=789),
    ]
    updated_count = await BaseDAO.bulk_update(session=session, records=records)
    print(f"Обновлено {updated_count} записей")
    ```
    """
    ...