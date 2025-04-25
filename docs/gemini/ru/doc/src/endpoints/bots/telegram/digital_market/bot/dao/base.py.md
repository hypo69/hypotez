# Модуль `BaseDAO`

## Обзор

Этот модуль предоставляет базовый класс `BaseDAO`, который служит основой для работы с моделями данных в базе данных, используя SQLAlchemy. 
Он предоставляет набор методов для выполнения общих операций с данными, таких как поиск, добавление, обновление и удаление записей.

## Классы

### `BaseDAO`

**Описание**: Базовый класс для работы с моделями данных, реализующий стандартные операции CRUD (Create, Read, Update, Delete). 
**Наследует**: 
  - `Generic[T]`: Используется для создания классов с типом, ограниченным типом `Base` (базовый класс SQLAlchemy).

**Атрибуты**:

- `model (type[T])`: Тип модели данных, с которой работает DAO.

**Методы**:

- `find_one_or_none_by_id(cls, data_id: int, session: AsyncSession)`: Поиск записи по ID.
- `find_one_or_none(cls, session: AsyncSession, filters: BaseModel)`: Поиск одной записи по фильтрам.
- `find_all(cls, session: AsyncSession, filters: BaseModel | None = None)`: Поиск всех записей по фильтрам.
- `add(cls, session: AsyncSession, values: BaseModel)`: Добавление одной записи.
- `add_many(cls, session: AsyncSession, instances: List[BaseModel])`: Добавление нескольких записей.
- `update(cls, session: AsyncSession, filters: BaseModel, values: BaseModel)`: Обновление записей по фильтрам.
- `delete(cls, session: AsyncSession, filters: BaseModel)`: Удаление записей по фильтру.
- `count(cls, session: AsyncSession, filters: BaseModel | None = None)`: Подсчет количества записей.
- `paginate(cls, session: AsyncSession, page: int = 1, page_size: int = 10, filters: BaseModel = None)`: Пагинация записей.
- `find_by_ids(cls, session: AsyncSession, ids: List[int])`: Найти несколько записей по списку ID.
- `upsert(cls, session: AsyncSession, unique_fields: List[str], values: BaseModel)`: Создать запись или обновить существующую.
- `bulk_update(cls, session: AsyncSession, records: List[BaseModel])`: Массовое обновление записей.

## Методы класса

### `find_one_or_none_by_id`

```python
    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession):
        # Найти запись по ID
        logger.info(f"Поиск {cls.model.__name__} с ID: {data_id}")
        try:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info(f"Запись с ID {data_id} найдена.")
            else:
                logger.info(f"Запись с ID {data_id} не найдена.")
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи с ID {data_id}: {e}")
            raise
```

**Назначение**: Поиск записи в базе данных по ID. 

**Параметры**:

- `data_id (int)`: ID записи, которую нужно найти.
- `session (AsyncSession)`: Сессия SQLAlchemy для взаимодействия с базой данных.

**Возвращает**:

- `T | None`: Объект модели данных, найденный по ID, или `None`, если запись не найдена.

**Вызывает исключения**:

- `SQLAlchemyError`: Если происходит ошибка во время выполнения запроса к базе данных.

**Как работает функция**:

- Логирует информацию о начале поиска записи по ID.
- Создает запрос `select` для поиска записи по ID с помощью метода `filter_by`.
- Выполняет запрос с помощью метода `session.execute`.
- Получает результат запроса с помощью метода `scalar_one_or_none`, который возвращает найденную запись или `None`, если запись не найдена.
- Логирует информацию о результате поиска записи.
- Возвращает найденную запись или `None`.

**Примеры**:

```python
# Пример использования метода:
from models import User
from src.database import session

user = await BaseDAO.find_one_or_none_by_id(1, session)
```

### `find_one_or_none`

```python
    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel):
        # Найти одну запись по фильтрам
        filter_dict = filters.model_dump(exclude_unset=True)
        logger.info(f"Поиск одной записи {cls.model.__name__} по фильтрам: {filter_dict}")
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info(f"Запись найдена по фильтрам: {filter_dict}")
            else:
                logger.info(f"Запись не найдена по фильтрам: {filter_dict}")
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи по фильтрам {filter_dict}: {e}")
            raise
```

**Назначение**: Поиск одной записи в базе данных по заданным фильтрам.

**Параметры**:

- `session (AsyncSession)`: Сессия SQLAlchemy для взаимодействия с базой данных.
- `filters (BaseModel)`: Модель Pydantic, содержащая фильтры для поиска записи.

**Возвращает**:

- `T | None`: Объект модели данных, найденный по фильтрам, или `None`, если запись не найдена.

**Вызывает исключения**:

- `SQLAlchemyError`: Если происходит ошибка во время выполнения запроса к базе данных.

**Как работает функция**:

- Преобразует фильтры из модели Pydantic в словарь с помощью метода `model_dump(exclude_unset=True)`.
- Логирует информацию о начале поиска записи по фильтрам.
- Создает запрос `select` для поиска записи по фильтрам с помощью метода `filter_by`.
- Выполняет запрос с помощью метода `session.execute`.
- Получает результат запроса с помощью метода `scalar_one_or_none`, который возвращает найденную запись или `None`, если запись не найдена.
- Логирует информацию о результате поиска записи.
- Возвращает найденную запись или `None`.

**Примеры**:

```python
# Пример использования метода:
from models import User
from src.database import session

user_filter = User(name="John Doe")
user = await BaseDAO.find_one_or_none(session, user_filter)
```

### `find_all`

```python
    @classmethod
    async def find_all(cls, session: AsyncSession, filters: BaseModel | None = None):
        # Найти все записи по фильтрам
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        logger.info(f"Поиск всех записей {cls.model.__name__} по фильтрам: {filter_dict}")
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске всех записей по фильтрам {filter_dict}: {e}")
            raise
```

**Назначение**: Поиск всех записей в базе данных, удовлетворяющих заданным фильтрам.

**Параметры**:

- `session (AsyncSession)`: Сессия SQLAlchemy для взаимодействия с базой данных.
- `filters (BaseModel | None, optional)`: Модель Pydantic, содержащая фильтры для поиска записей. По умолчанию `None` (без фильтров).

**Возвращает**:

- `List[T]`: Список объектов модели данных, найденных по фильтрам.

**Вызывает исключения**:

- `SQLAlchemyError`: Если происходит ошибка во время выполнения запроса к базе данных.

**Как работает функция**:

- Преобразует фильтры из модели Pydantic в словарь с помощью метода `model_dump(exclude_unset=True)`, если фильтры заданы.
- Логирует информацию о начале поиска всех записей по фильтрам.
- Создает запрос `select` для поиска всех записей по фильтрам с помощью метода `filter_by`.
- Выполняет запрос с помощью метода `session.execute`.
- Получает список всех найденных записей с помощью метода `scalars().all()`.
- Логирует информацию о количестве найденных записей.
- Возвращает список найденных записей.

**Примеры**:

```python
# Пример использования метода:
from models import User
from src.database import session

user_filter = User(name="John Doe")
users = await BaseDAO.find_all(session, user_filter)
```

### `add`

```python
    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel):
        # Добавить одну запись
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f"Добавление записи {cls.model.__name__} с параметрами: {values_dict}")
        new_instance = cls.model(**values_dict)
        session.add(new_instance)
        try:
            await session.flush()
            logger.info(f"Запись {cls.model.__name__} успешно добавлена.")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при добавлении записи: {e}")
            raise e
        return new_instance
```

**Назначение**: Добавление новой записи в базу данных.

**Параметры**:

- `session (AsyncSession)`: Сессия SQLAlchemy для взаимодействия с базой данных.
- `values (BaseModel)`: Модель Pydantic, содержащая данные для новой записи.

**Возвращает**:

- `T`: Новый объект модели данных, добавленный в базу данных.

**Вызывает исключения**:

- `SQLAlchemyError`: Если происходит ошибка во время добавления записи в базу данных.

**Как работает функция**:

- Преобразует данные из модели Pydantic в словарь с помощью метода `model_dump(exclude_unset=True)`.
- Логирует информацию о начале добавления записи.
- Создает новый объект модели данных с помощью `cls.model(**values_dict)`.
- Добавляет новый объект в сессию SQLAlchemy с помощью метода `session.add`.
- Выполняет `session.flush` для сохранения изменений в базе данных.
- Логирует информацию об успешном добавлении записи.
- Возвращает добавленный объект.

**Примеры**:

```python
# Пример использования метода:
from models import User
from src.database import session

new_user = User(name="Jane Doe", age=30)
user = await BaseDAO.add(session, new_user)
```

### `add_many`

```python
    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[BaseModel]):
        # Добавить несколько записей
        values_list = [item.model_dump(exclude_unset=True) for item in instances]
        logger.info(f"Добавление нескольких записей {cls.model.__name__}. Количество: {len(values_list)}")
        new_instances = [cls.model(**values) for values in values_list]
        session.add_all(new_instances)
        try:
            await session.flush()
            logger.info(f"Успешно добавлено {len(new_instances)} записей.")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при добавлении нескольких записей: {e}")
            raise e
        return new_instances
```

**Назначение**: Добавление нескольких новых записей в базу данных.

**Параметры**:

- `session (AsyncSession)`: Сессия SQLAlchemy для взаимодействия с базой данных.
- `instances (List[BaseModel])`: Список моделей Pydantic, содержащих данные для новых записей.

**Возвращает**:

- `List[T]`: Список новых объектов модели данных, добавленных в базу данных.

**Вызывает исключения**:

- `SQLAlchemyError`: Если происходит ошибка во время добавления записей в базу данных.

**Как работает функция**:

- Преобразует данные из каждой модели Pydantic в словарь с помощью метода `model_dump(exclude_unset=True)`.
- Логирует информацию о начале добавления нескольких записей.
- Создает список новых объектов модели данных с помощью `[cls.model(**values) for values in values_list]`.
- Добавляет список новых объектов в сессию SQLAlchemy с помощью метода `session.add_all`.
- Выполняет `session.flush` для сохранения изменений в базе данных.
- Логирует информацию об успешном добавлении нескольких записей.
- Возвращает список добавленных объектов.

**Примеры**:

```python
# Пример использования метода:
from models import User
from src.database import session

new_users = [User(name="Alice", age=25), User(name="Bob", age=35)]
users = await BaseDAO.add_many(session, new_users)
```

### `update`

```python
    @classmethod
    async def update(cls, session: AsyncSession, filters: BaseModel, values: BaseModel):
        # Обновить записи по фильтрам
        filter_dict = filters.model_dump(exclude_unset=True)
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f"Обновление записей {cls.model.__name__} по фильтру: {filter_dict} с параметрами: {values_dict}")
        query = (
            sqlalchemy_update(cls.model)
            .where(*[getattr(cls.model, k) == v for k, v in filter_dict.items()])
            .values(**values_dict)
            .execution_options(synchronize_session="fetch")
        )
        try:
            result = await session.execute(query)
            await session.flush()
            logger.info(f"Обновлено {result.rowcount} записей.")
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при обновлении записей: {e}")
            raise e
```

**Назначение**: Обновление записей в базе данных, удовлетворяющих заданным фильтрам, новыми значениями.

**Параметры**:

- `session (AsyncSession)`: Сессия SQLAlchemy для взаимодействия с базой данных.
- `filters (BaseModel)`: Модель Pydantic, содержащая фильтры для поиска записей, которые нужно обновить.
- `values (BaseModel)`: Модель Pydantic, содержащая новые значения для обновления записей.

**Возвращает**:

- `int`: Количество обновленных записей.

**Вызывает исключения**:

- `SQLAlchemyError`: Если происходит ошибка во время обновления записей в базе данных.

**Как работает функция**:

- Преобразует фильтры и новые значения из моделей Pydantic в словари с помощью метода `model_dump(exclude_unset=True)`.
- Логирует информацию о начале обновления записей по фильтрам.
- Создает запрос `update` для обновления записей по фильтрам с помощью метода `where`.
- Устанавливает новые значения для обновления с помощью метода `values`.
- Выполняет запрос с помощью метода `session.execute`.
- Выполняет `session.flush` для сохранения изменений в базе данных.
- Логирует информацию о количестве обновленных записей.
- Возвращает количество обновленных записей.

**Примеры**:

```python
# Пример использования метода:
from models import User
from src.database import session

user_filter = User(name="John Doe")
update_values = User(age=40)
updated_count = await BaseDAO.update(session, user_filter, update_values)
```

### `delete`

```python
    @classmethod
    async def delete(cls, session: AsyncSession, filters: BaseModel):
        # Удалить записи по фильтру
        filter_dict = filters.model_dump(exclude_unset=True)
        logger.info(f"Удаление записей {cls.model.__name__} по фильтру: {filter_dict}")
        if not filter_dict:
            logger.error("Нужен хотя бы один фильтр для удаления.")
            raise ValueError("Нужен хотя бы один фильтр для удаления.")

        query = sqlalchemy_delete(cls.model).filter_by(**filter_dict)
        try:
            result = await session.execute(query)
            await session.flush()
            logger.info(f"Удалено {result.rowcount} записей.")
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при удалении записей: {e}")
            raise e
```

**Назначение**: Удаление записей в базе данных, удовлетворяющих заданным фильтрам.

**Параметры**:

- `session (AsyncSession)`: Сессия SQLAlchemy для взаимодействия с базой данных.
- `filters (BaseModel)`: Модель Pydantic, содержащая фильтры для поиска записей, которые нужно удалить.

**Возвращает**:

- `int`: Количество удаленных записей.

**Вызывает исключения**:

- `SQLAlchemyError`: Если происходит ошибка во время удаления записей в базе данных.
- `ValueError`: Если фильтры не заданы.

**Как работает функция**:

- Преобразует фильтры из модели Pydantic в словарь с помощью метода `model_dump(exclude_unset=True)`.
- Проверяет, что фильтры заданы, иначе выводит ошибку и завершает выполнение.
- Логирует информацию о начале удаления записей по фильтрам.
- Создает запрос `delete` для удаления записей по фильтрам с помощью метода `filter_by`.
- Выполняет запрос с помощью метода `session.execute`.
- Выполняет `session.flush` для сохранения изменений в базе данных.
- Логирует информацию о количестве удаленных записей.
- Возвращает количество удаленных записей.

**Примеры**:

```python
# Пример использования метода:
from models import User
from src.database import session

user_filter = User(name="John Doe")
deleted_count = await BaseDAO.delete(session, user_filter)
```

### `count`

```python
    @classmethod
    async def count(cls, session: AsyncSession, filters: BaseModel | None = None):
        # Подсчитать количество записей
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        logger.info(f"Подсчет количества записей {cls.model.__name__} по фильтру: {filter_dict}")
        try:
            query = select(func.count(cls.model.id)).filter_by(**filter_dict)
            result = await session.execute(query)
            count = result.scalar()
            logger.info(f"Найдено {count} записей.")
            return count
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при подсчете записей: {e}")
            raise
```

**Назначение**: Подсчет количества записей в базе данных, удовлетворяющих заданным фильтрам.

**Параметры**:

- `session (AsyncSession)`: Сессия SQLAlchemy для взаимодействия с базой данных.
- `filters (BaseModel | None, optional)`: Модель Pydantic, содержащая фильтры для поиска записей. По умолчанию `None` (без фильтров).

**Возвращает**:

- `int`: Количество записей, удовлетворяющих фильтрам.

**Вызывает исключения**:

- `SQLAlchemyError`: Если происходит ошибка во время выполнения запроса к базе данных.

**Как работает функция**:

- Преобразует фильтры из модели Pydantic в словарь с помощью метода `model_dump(exclude_unset=True)`, если фильтры заданы.
- Логирует информацию о начале подсчета записей по фильтрам.
- Создает запрос `select` для подсчета количества записей по фильтрам с помощью метода `filter_by`.
- Выполняет запрос с помощью метода `session.execute`.
- Получает количество найденных записей с помощью метода `scalar()`.
- Логирует информацию о количестве найденных записей.
- Возвращает количество записей.

**Примеры**:

```python
# Пример использования метода:
from models import User
from src.database import session

user_filter = User(name="John Doe")
count = await BaseDAO.count(session, user_filter)
```

### `paginate`

```python
    @classmethod
    async def paginate(cls, session: AsyncSession, page: int = 1, page_size: int = 10, filters: BaseModel = None):
        # Пагинация записей
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        logger.info(
            f"Пагинация записей {cls.model.__name__} по фильтру: {filter_dict}, страница: {page}, размер страницы: {page_size}")
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query.offset((page - 1) * page_size).limit(page_size))
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей на странице {page}.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при пагинации записей: {e}")
            raise
```

**Назначение**: Получение списка записей из базы данных с учетом пагинации (разбиения на страницы).

**Параметры**:

- `session (AsyncSession)`: Сессия SQLAlchemy для взаимодействия с базой данных.
- `page (int, optional)`: Номер страницы. По умолчанию 1.
- `page_size (int, optional)`: Количество записей на странице. По умолчанию 10.
- `filters (BaseModel, optional)`: Модель Pydantic, содержащая фильтры для поиска записей. По умолчанию `None` (без фильтров).

**Возвращает**:

- `List[T]`: Список объектов модели данных, найденных на заданной странице с учетом фильтров.

**Вызывает исключения**:

- `SQLAlchemyError`: Если происходит ошибка во время выполнения запроса к базе данных.

**Как работает функция**:

- Преобразует фильтры из модели Pydantic в словарь с помощью метода `model_dump(exclude_unset=True)`, если фильтры заданы.
- Логирует информацию о начале пагинации записей по фильтрам, странице и размеру страницы.
- Создает запрос `select` для поиска записей по фильтрам с помощью метода `filter_by`.
- Применяет пагинацию с помощью методов `offset` и `limit` к запросу.
- Выполняет запрос с помощью метода `session.execute`.
- Получает список найденных записей с помощью метода `scalars().all()`.
- Логирует информацию о количестве найденных записей на странице.
- Возвращает список найденных записей.

**Примеры**:

```python
# Пример использования метода:
from models import User
from src.database import session

user_filter = User(name="John Doe")
page_1_users = await BaseDAO.paginate(session, page=1, filters=user_filter)
```

### `find_by_ids`

```python
    @classmethod
    async def find_by_ids(cls, session: AsyncSession, ids: List[int]) -> List[Any]:
        """Найти несколько записей по списку ID"""
        logger.info(f"Поиск записей {cls.model.__name__} по списку ID: {ids}")
        try:
            query = select(cls.model).filter(cls.model.id.in_(ids))
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей по списку ID.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записей по списку ID: {e}")
            raise
```

**Назначение**: Поиск нескольких записей в базе данных по списку ID.

**Параметры**:

- `session (AsyncSession)`: Сессия SQLAlchemy для взаимодействия с базой данных.
- `ids (List[int])`: Список ID записей, которые нужно найти.

**Возвращает**:

- `List[T]`: Список объектов модели данных, найденных по списку ID.

**Вызывает исключения**:

- `SQLAlchemyError`: Если происходит ошибка во время выполнения запроса к базе данных.

**Как работает функция**:

- Логирует информацию о начале поиска записей по списку ID.
- Создает запрос `select` для поиска записей по списку ID с помощью метода `filter`.
- Выполняет запрос с помощью метода `session.execute`.
- Получает список найденных записей с помощью метода `scalars().all()`.
- Логирует информацию о количестве найденных записей по списку ID.
- Возвращает список найденных записей.

**Примеры**:

```python
# Пример использования метода:
from models import User
from src.database import session

user_ids = [1, 2, 3]
users = await BaseDAO.find_by_ids(session, user_ids)
```

### `upsert`

```python
    @classmethod
    async def upsert(cls, session: AsyncSession, unique_fields: List[str], values: BaseModel):
        """Создать запись или обновить существующую"""
        values_dict = values.model_dump(exclude_unset=True)
        filter_dict = {field: values_dict[field] for field in unique_fields if field in values_dict}

        logger.info(f"Upsert для {cls.model.__name__}")
        try:
            existing = await cls.find_one_or_none(session, BaseModel.construct(**filter_dict))
            if existing:
                # Обновляем существующую запись
                for key, value in values_dict.items():
                    setattr(existing, key, value)
                await session.flush()
                logger.info(f"Обновлена существующая запись {cls.model.__name__}")
                return existing
            else:
                # Создаем новую запись
                new_instance = cls.model(**values_dict)
                session.add(new_instance)
                await session.flush()
                logger.info(f"Создана новая запись {cls.model.__name__}")
                return new_instance
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при upsert: {e}")
            raise
```

**Назначение**: Создает новую запись или обновляет существующую в базе данных, используя заданные уникальные поля.

**Параметры**:

- `session (AsyncSession)`: Сессия SQLAlchemy для взаимодействия с базой данных.
- `unique_fields (List[str])`: Список имен полей, которые должны быть уникальными для записи.
- `values (BaseModel)`: Модель Pydantic, содержащая данные для новой записи или для обновления существующей.

**Возвращает**:

- `T`: Объект модели данных, добавленный или обновленный в базе данных.

**Вызывает исключения**:

- `SQLAlchemyError`: Если происходит ошибка во время выполнения запроса к базе данных.

**Как работает функция**:

- Преобразует данные из модели Pydantic в словарь с помощью метода `model_dump(exclude_unset=True)`.
- Создает словарь фильтров, используя только значения уникальных полей из данных.
- Логирует информацию о начале `upsert`.
- Использует метод `find_one_or_none` для поиска существующей записи по фильтрам.
- Если запись найдена, обновляет ее поля новыми значениями.
- Если запись не найдена, создает новую запись с данными.
- Выполняет `session.flush` для сохранения изменений в базе данных.
- Логирует информацию о результате `upsert` (создана новая запись или обновлена существующая).
- Возвращает добавленный или обновленный объект.

**Примеры**:

```python
# Пример использования метода:
from models import User
from src.database import session

new_user = User(name="Alice", age=25)
user = await BaseDAO.upsert(session, ["name"], new_user)
```

### `bulk_update`

```python
    @classmethod
    async def bulk_update(cls, session: AsyncSession, records: List[BaseModel]) -> int:
        """Массовое обновление записей"""
        logger.info(f"Массовое обновление записей {cls.model.__name__}")
        try:
            updated_count = 0
            for record in records:
                record_dict = record.model_dump(exclude_unset=True)
                if 'id' not in record_dict:
                    continue

                update_data = {k: v for k, v in record_dict.items() if k != 'id'}
                stmt = (
                    sqlalchemy_update(cls.model)
                    .filter_by(id=record_dict['id'])
                    .values(**update_data)
                )
                result = await session.execute(stmt)
                updated_count += result.rowcount

            await session.flush()
            logger.info(f"Обновлено {updated_count} записей")
            return updated_count
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при массовом обновлении: {e}")
            raise
```

**Назначение**: Массовое обновление записей в базе данных, используя список моделей Pydantic.

**Параметры**:

- `session (AsyncSession)`: Сессия SQLAlchemy для взаимодействия с базой данных.
- `records (List[BaseModel])`: Список моделей Pydantic, содержащих данные для обновления записей.

**Возвращает**:

- `int`: Количество обновленных записей.

**Вызывает исключения**:

- `SQLAlchemyError`: Если происходит ошибка во время обновления записей в базе данных.

**Как работает функция**:

- Логирует информацию о начале массового обновления записей.
- Итерирует по списку записей и выполняет обновление для каждой записи.
- Преобразует данные из каждой модели Pydantic в словарь с помощью метода `model_dump(exclude_unset=True)`.
- Проверяет наличие поля `id` в данных записи.
- Создает запрос `update` для обновления записи по ID с помощью метода `filter_by`.
- Устанавливает новые значения для обновления с помощью метода `values`.
- Выполняет запрос с помощью метода `session.execute`.
- Суммирует количество обновленных записей.
- Выполняет `session.flush` для сохранения изменений в базе данных.
- Логирует информацию о количестве обновленных записей.
- Возвращает количество обновленных записей.

**Примеры**:

```python
# Пример использования метода:
from models import User
from src.database import session

update_records = [
    User(id=1, age=30),
    User(id=2, name="Alice"),
]
updated_count = await BaseDAO.bulk_update(session, update_records)
```

## Параметры класса

- `model (type[T])`: Тип модели данных, с которой работает DAO.

## Примеры

```python
# Пример использования BaseDAO:
from models import User, Product
from src.database import session

# Добавление новой записи
new_user = User(name="John Doe", age=30)
user = await UserDAO.add(session, new_user)

# Поиск записи по ID
user = await UserDAO.find_one_or_none_by_id(user.id, session)

# Поиск всех записей по фильтру
user_filter = User(name="John Doe")
users = await UserDAO.find_all(session, user_filter)

# Обновление записи
update_values = User(age=40)
updated_count = await UserDAO.update(session, user_filter, update_values)

# Удаление записи
deleted_count = await UserDAO.delete(session, user_filter)

# Подсчет количества записей
count = await UserDAO.count(session, user_filter)

# Пагинация записей
page_1_users = await UserDAO.paginate(session, page=1, filters=user_filter)

# Массовое добавление записей
new_users = [User(name="Alice", age=25), User(name="Bob", age=35)]
users = await UserDAO.add_many(session, new_users)

# Поиск по списку ID
user_ids = [1, 2, 3]
users = await UserDAO.find_by_ids(session, user_ids)

# Upsert записи
new_user = User(name="Alice", age=25)
user = await UserDAO.upsert(session, ["name"], new_user)

# Массовое обновление записей
update_records = [
    User(id=1, age=30),
    User(id=2, name="Alice"),
]
updated_count = await UserDAO.bulk_update(session, update_records)
```