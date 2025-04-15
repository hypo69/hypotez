# Модуль для работы с базой данных (DAO)

## Обзор

Модуль `base.py` предоставляет базовый класс `BaseDAO` для взаимодействия с базой данных с использованием SQLAlchemy. Он включает в себя методы для выполнения основных операций CRUD (создание, чтение, обновление, удаление) и другие полезные функции, такие как пагинация и массовое обновление.

## Подробнее

Этот модуль определяет класс `BaseDAO`, который является базовым классом для всех DAO (Data Access Objects) в проекте. Он предоставляет общие методы для работы с базой данных, такие как поиск, добавление, обновление и удаление записей. Класс использует асинхронные сессии SQLAlchemy для выполнения операций с базой данных.

## Классы

### `BaseDAO`

**Описание**:
Базовый класс для объектов доступа к данным (DAO). Предоставляет методы для выполнения основных операций с базой данных, таких как поиск, добавление, обновление и удаление записей.

**Наследует**:
Не наследует никаких классов.

**Атрибуты**:
- `model` (type[T]): Тип модели SQLAlchemy, с которой работает DAO.

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

## Методы класса

### `find_one_or_none_by_id`

```python
@classmethod
async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession):
    """Найти запись по ID"""
```

**Назначение**:
Метод `find_one_or_none_by_id` предназначен для поиска записи в базе данных по ее уникальному идентификатору (ID).

**Параметры**:
- `cls`: Ссылка на класс `BaseDAO`.
- `data_id` (int): Уникальный идентификатор записи, которую необходимо найти.
- `session` (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций с базой данных.

**Возвращает**:
- `record` (T | None): Возвращает найденную запись типа `T` (наследник `Base`) или `None`, если запись с указанным `data_id` не найдена.

**Вызывает исключения**:
- `SQLAlchemyError`: Если возникает ошибка при выполнении запроса к базе данных.

**Как работает функция**:
1. Логирует начало поиска записи с указанным `data_id`.
2. Формирует запрос `select` к базе данных для поиска записи с указанным `id`.
3. Выполняет запрос с использованием асинхронной сессии `session`.
4. Извлекает результат запроса с помощью `scalar_one_or_none()`, который возвращает либо одну запись, либо `None`, если запись не найдена.
5. Логирует информацию о том, была ли найдена запись.
6. Возвращает найденную запись или `None`.
7. В случае возникновения ошибки `SQLAlchemyError`, логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования метода find_one_or_none_by_id
data_id = 123
session = AsyncSession()  # Предполагается, что AsyncSession уже сконфигурирована
record = await BaseDAO.find_one_or_none_by_id(data_id=data_id, session=session)

if record:
    print(f"Найдена запись: {record}")
else:
    print(f"Запись с ID {data_id} не найдена.")
```

### `find_one_or_none`

```python
@classmethod
async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel):
    """Найти одну запись по фильтрам"""
```

**Назначение**:
Метод `find_one_or_none` предназначен для поиска одной записи в базе данных, соответствующей заданным фильтрам.

**Параметры**:
- `cls`: Ссылка на класс `BaseDAO`.
- `session` (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций с базой данных.
- `filters` (BaseModel): Объект Pydantic `BaseModel`, содержащий фильтры для поиска записи.

**Возвращает**:
- `record` (T | None): Возвращает найденную запись типа `T` (наследник `Base`) или `None`, если запись не найдена.

**Вызывает исключения**:
- `SQLAlchemyError`: Если возникает ошибка при выполнении запроса к базе данных.

**Как работает функция**:
1. Преобразует объект `filters` в словарь, исключая неустановленные значения (значения по умолчанию, которые не были изменены).
2. Логирует начало поиска записи с использованием переданных фильтров.
3. Формирует запрос `select` к базе данных с применением фильтров, переданных в виде словаря.
4. Выполняет запрос с использованием асинхронной сессии `session`.
5. Извлекает результат запроса с помощью `scalar_one_or_none()`, который возвращает либо одну запись, либо `None`, если запись не найдена.
6. Логирует информацию о том, была ли найдена запись.
7. Возвращает найденную запись или `None`.
8. В случае возникновения ошибки `SQLAlchemyError`, логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования метода find_one_or_none
from pydantic import BaseModel

class UserFilter(BaseModel):
    name: str
    age: int

filters = UserFilter(name="John", age=30)
session = AsyncSession()  # Предполагается, что AsyncSession уже сконфигурирована
record = await BaseDAO.find_one_or_none(session=session, filters=filters)

if record:
    print(f"Найдена запись: {record}")
else:
    print(f"Запись с фильтрами {filters} не найдена.")
```

### `find_all`

```python
@classmethod
async def find_all(cls, session: AsyncSession, filters: BaseModel | None = None):
    """Найти все записи по фильтрам"""
```

**Назначение**:
Метод `find_all` предназначен для поиска всех записей в базе данных, соответствующих заданным фильтрам.

**Параметры**:
- `cls`: Ссылка на класс `BaseDAO`.
- `session` (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций с базой данных.
- `filters` (BaseModel | None, optional): Объект Pydantic `BaseModel`, содержащий фильтры для поиска записей. Если `None`, возвращаются все записи. По умолчанию `None`.

**Возвращает**:
- `records` (List[T]): Список найденных записей типа `T` (наследник `Base`).

**Вызывает исключения**:
- `SQLAlchemyError`: Если возникает ошибка при выполнении запроса к базе данных.

**Как работает функция**:
1. Преобразует объект `filters` в словарь, исключая неустановленные значения (значения по умолчанию, которые не были изменены). Если `filters` равен `None`, создается пустой словарь.
2. Логирует начало поиска записей с использованием переданных фильтров.
3. Формирует запрос `select` к базе данных с применением фильтров, переданных в виде словаря.
4. Выполняет запрос с использованием асинхронной сессии `session`.
5. Извлекает результаты запроса с помощью `scalars().all()`, который возвращает список всех найденных записей.
6. Логирует количество найденных записей.
7. Возвращает список найденных записей.
8. В случае возникновения ошибки `SQLAlchemyError`, логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования метода find_all
from pydantic import BaseModel
from typing import Optional

class UserFilter(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

session = AsyncSession()  # Предполагается, что AsyncSession уже сконфигурирована

# Получение всех записей
records = await BaseDAO.find_all(session=session)
print(f"Найдено {len(records)} записей.")

# Получение записей с фильтрами
filters = UserFilter(name="John")
records = await BaseDAO.find_all(session=session, filters=filters)
print(f"Найдено {len(records)} записей с именем John.")
```

### `add`

```python
@classmethod
async def add(cls, session: AsyncSession, values: BaseModel):
    """Добавить одну запись"""
```

**Назначение**:
Метод `add` предназначен для добавления одной новой записи в базу данных.

**Параметры**:
- `cls`: Ссылка на класс `BaseDAO`.
- `session` (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций с базой данных.
- `values` (BaseModel): Объект Pydantic `BaseModel`, содержащий значения для создания новой записи.

**Возвращает**:
- `new_instance` (T): Возвращает созданную запись типа `T` (наследник `Base`).

**Вызывает исключения**:
- `SQLAlchemyError`: Если возникает ошибка при выполнении запроса к базе данных.

**Как работает функция**:
1. Преобразует объект `values` в словарь, исключая неустановленные значения (значения по умолчанию, которые не были изменены).
2. Логирует начало добавления записи с использованием переданных параметров.
3. Создает новый экземпляр модели `cls.model` с использованием значений из словаря.
4. Добавляет новый экземпляр в сессию SQLAlchemy.
5. Пытается выполнить `flush()` для сохранения изменений в базе данных.
6. Логирует информацию об успешном добавлении записи.
7. В случае возникновения ошибки `SQLAlchemyError`, выполняет откат транзакции (`session.rollback()`), логирует ошибку и пробрасывает исключение.
8. Возвращает созданный экземпляр.

**Примеры**:
```python
# Пример использования метода add
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    age: int

values = UserCreate(name="Alice", age=25)
session = AsyncSession()  # Предполагается, что AsyncSession уже сконфигурирована
new_user = await BaseDAO.add(session=session, values=values)
print(f"Добавлен новый пользователь: {new_user}")
```

### `add_many`

```python
@classmethod
async def add_many(cls, session: AsyncSession, instances: List[BaseModel]):
    """Добавить несколько записей"""
```

**Назначение**:
Метод `add_many` предназначен для добавления нескольких новых записей в базу данных за одну операцию.

**Параметры**:
- `cls`: Ссылка на класс `BaseDAO`.
- `session` (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций с базой данных.
- `instances` (List[BaseModel]): Список объектов Pydantic `BaseModel`, содержащих значения для создания новых записей.

**Возвращает**:
- `new_instances` (List[T]): Возвращает список созданных записей типа `T` (наследник `Base`).

**Вызывает исключения**:
- `SQLAlchemyError`: Если возникает ошибка при выполнении запроса к базе данных.

**Как работает функция**:
1. Преобразует каждый объект `BaseModel` в списке `instances` в словарь, исключая неустановленные значения.
2. Логирует начало добавления нескольких записей и их количество.
3. Создает список новых экземпляров модели `cls.model` с использованием значений из словарей.
4. Добавляет все новые экземпляры в сессию SQLAlchemy с помощью `session.add_all()`.
5. Пытается выполнить `flush()` для сохранения изменений в базе данных.
6. Логирует информацию об успешном добавлении записей и их количестве.
7. В случае возникновения ошибки `SQLAlchemyError`, выполняет откат транзакции (`session.rollback()`), логирует ошибку и пробрасывает исключение.
8. Возвращает список созданных экземпляров.

**Примеры**:
```python
# Пример использования метода add_many
from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    name: str
    age: int

users_data = [
    UserCreate(name="Bob", age=30),
    UserCreate(name="Charlie", age=35)
]
session = AsyncSession()  # Предполагается, что AsyncSession уже сконфигурирована
new_users = await BaseDAO.add_many(session=session, instances=users_data)
print(f"Добавлены новые пользователи: {new_users}")
```

### `update`

```python
@classmethod
async def update(cls, session: AsyncSession, filters: BaseModel, values: BaseModel):
    """Обновить записи по фильтрам"""
```

**Назначение**:
Метод `update` предназначен для обновления записей в базе данных, соответствующих заданным фильтрам, новыми значениями.

**Параметры**:
- `cls`: Ссылка на класс `BaseDAO`.
- `session` (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций с базой данных.
- `filters` (BaseModel): Объект Pydantic `BaseModel`, содержащий фильтры для выбора записей для обновления.
- `values` (BaseModel): Объект Pydantic `BaseModel`, содержащий новые значения для обновления записей.

**Возвращает**:
- `rowcount` (int): Количество обновленных записей.

**Вызывает исключения**:
- `SQLAlchemyError`: Если возникает ошибка при выполнении запроса к базе данных.

**Как работает функция**:
1. Преобразует объекты `filters` и `values` в словари, исключая неустановленные значения.
2. Логирует начало обновления записей с использованием переданных фильтров и параметров.
3. Формирует запрос `sqlalchemy_update` к базе данных с применением фильтров и новых значений.
   - Фильтры применяются с использованием атрибутов модели и их сравнения со значениями из `filter_dict`.
   - Новые значения применяются к выбранным записям.
   - `execution_options(synchronize_session="fetch")` указывает SQLAlchemy синхронизировать сессию с результатами обновления.
4. Выполняет запрос с использованием асинхронной сессии `session`.
5. Пытается выполнить `flush()` для сохранения изменений в базе данных.
6. Логирует количество обновленных записей.
7. В случае возникновения ошибки `SQLAlchemyError`, выполняет откат транзакции (`session.rollback()`), логирует ошибку и пробрасывает исключение.
8. Возвращает количество обновленных записей.

**Примеры**:
```python
# Пример использования метода update
from pydantic import BaseModel

class UserFilter(BaseModel):
    name: str

class UserUpdate(BaseModel):
    age: int

filters = UserFilter(name="John")
values = UserUpdate(age=31)
session = AsyncSession()  # Предполагается, что AsyncSession уже сконфигурирована
updated_count = await BaseDAO.update(session=session, filters=filters, values=values)
print(f"Обновлено {updated_count} записей.")
```

### `delete`

```python
@classmethod
async def delete(cls, session: AsyncSession, filters: BaseModel):
    """Удалить записи по фильтру"""
```

**Назначение**:
Метод `delete` предназначен для удаления записей из базы данных, соответствующих заданным фильтрам.

**Параметры**:
- `cls`: Ссылка на класс `BaseDAO`.
- `session` (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций с базой данных.
- `filters` (BaseModel): Объект Pydantic `BaseModel`, содержащий фильтры для выбора записей для удаления.

**Возвращает**:
- `rowcount` (int): Количество удаленных записей.

**Вызывает исключения**:
- `ValueError`: Если не предоставлены фильтры для удаления.
- `SQLAlchemyError`: Если возникает ошибка при выполнении запроса к базе данных.

**Как работает функция**:
1. Преобразует объект `filters` в словарь, исключая неустановленные значения.
2. Логирует начало удаления записей с использованием переданных фильтров.
3. Проверяет, что фильтры не пустые. Если фильтры пустые, вызывает исключение `ValueError` с сообщением о необходимости хотя бы одного фильтра для удаления.
4. Формирует запрос `sqlalchemy_delete` к базе данных с применением фильтров.
5. Выполняет запрос с использованием асинхронной сессии `session`.
6. Пытается выполнить `flush()` для сохранения изменений в базе данных.
7. Логирует количество удаленных записей.
8. В случае возникновения ошибки `SQLAlchemyError`, выполняет откат транзакции (`session.rollback()`), логирует ошибку и пробрасывает исключение.
9. Возвращает количество удаленных записей.

**Примеры**:
```python
# Пример использования метода delete
from pydantic import BaseModel

class UserFilter(BaseModel):
    name: str

filters = UserFilter(name="John")
session = AsyncSession()  # Предполагается, что AsyncSession уже сконфигурирована
deleted_count = await BaseDAO.delete(session=session, filters=filters)
print(f"Удалено {deleted_count} записей.")
```

### `count`

```python
@classmethod
async def count(cls, session: AsyncSession, filters: BaseModel | None = None):
    """Подсчитать количество записей"""
```

**Назначение**:
Метод `count` предназначен для подсчета количества записей в базе данных, соответствующих заданным фильтрам.

**Параметры**:
- `cls`: Ссылка на класс `BaseDAO`.
- `session` (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций с базой данных.
- `filters` (BaseModel | None, optional): Объект Pydantic `BaseModel`, содержащий фильтры для выбора записей для подсчета. Если `None`, подсчитываются все записи. По умолчанию `None`.

**Возвращает**:
- `count` (int): Количество записей, соответствующих фильтрам.

**Вызывает исключения**:
- `SQLAlchemyError`: Если возникает ошибка при выполнении запроса к базе данных.

**Как работает функция**:
1. Преобразует объект `filters` в словарь, исключая неустановленные значения. Если `filters` равен `None`, создается пустой словарь.
2. Логирует начало подсчета записей с использованием переданных фильтров.
3. Формирует запрос `select(func.count(cls.model.id))` к базе данных с применением фильтров.
   - `func.count(cls.model.id)` - функция SQLAlchemy для подсчета количества идентификаторов записей.
4. Выполняет запрос с использованием асинхронной сессии `session`.
5. Извлекает результат запроса с помощью `scalar()`, который возвращает количество записей.
6. Логирует найденное количество записей.
7. Возвращает количество записей.
8. В случае возникновения ошибки `SQLAlchemyError`, логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования метода count
from pydantic import BaseModel
from typing import Optional

class UserFilter(BaseModel):
    name: Optional[str] = None

session = AsyncSession()  # Предполагается, что AsyncSession уже сконфигурирована

# Подсчет всех записей
total_count = await BaseDAO.count(session=session)
print(f"Всего записей: {total_count}")

# Подсчет записей с фильтром
filters = UserFilter(name="John")
john_count = await BaseDAO.count(session=session, filters=filters)
print(f"Записей с именем John: {john_count}")
```

### `paginate`

```python
@classmethod
async def paginate(cls, session: AsyncSession, page: int = 1, page_size: int = 10, filters: BaseModel = None):
    """Пагинация записей"""
```

**Назначение**:
Метод `paginate` предназначен для выполнения пагинации записей в базе данных, соответствующих заданным фильтрам.

**Параметры**:
- `cls`: Ссылка на класс `BaseDAO`.
- `session` (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций с базой данных.
- `page` (int, optional): Номер страницы для отображения. По умолчанию `1`.
- `page_size` (int, optional): Количество записей на странице. По умолчанию `10`.
- `filters` (BaseModel, optional): Объект Pydantic `BaseModel`, содержащий фильтры для выбора записей. Если `None`, выбираются все записи. По умолчанию `None`.

**Возвращает**:
- `records` (List[T]): Список записей типа `T` (наследник `Base`) для указанной страницы.

**Вызывает исключения**:
- `SQLAlchemyError`: Если возникает ошибка при выполнении запроса к базе данных.

**Как работает функция**:
1. Преобразует объект `filters` в словарь, исключая неустановленные значения. Если `filters` равен `None`, создается пустой словарь.
2. Логирует начало пагинации записей с использованием переданных фильтров, номера страницы и размера страницы.
3. Формирует запрос `select(cls.model)` к базе данных с применением фильтров.
4. Добавляет параметры `offset` и `limit` для выполнения пагинации.
   - `offset` - смещение от начала списка записей, вычисляется как `(page - 1) * page_size`.
   - `limit` - максимальное количество записей для извлечения, равно `page_size`.
5. Выполняет запрос с использованием асинхронной сессии `session`.
6. Извлекает результаты запроса с помощью `scalars().all()`, который возвращает список записей для указанной страницы.
7. Логирует количество найденных записей на странице.
8. Возвращает список записей для указанной страницы.
9. В случае возникновения ошибки `SQLAlchemyError`, логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования метода paginate
from pydantic import BaseModel
from typing import Optional

class UserFilter(BaseModel):
    name: Optional[str] = None

session = AsyncSession()  # Предполагается, что AsyncSession уже сконфигурирована

# Получение первой страницы с 10 записями
page_1 = await BaseDAO.paginate(session=session, page=1, page_size=10)
print(f"Найдено {len(page_1)} записей на первой странице.")

# Получение второй страницы с 5 записями и фильтром
filters = UserFilter(name="John")
page_2 = await BaseDAO.paginate(session=session, page=2, page_size=5, filters=filters)
print(f"Найдено {len(page_2)} записей на второй странице с именем John.")
```

### `find_by_ids`

```python
@classmethod
async def find_by_ids(cls, session: AsyncSession, ids: List[int]) -> List[Any]:
    """Найти несколько записей по списку ID"""
```

**Назначение**:
Метод `find_by_ids` предназначен для поиска нескольких записей в базе данных по списку их идентификаторов (ID).

**Параметры**:
- `cls`: Ссылка на класс `BaseDAO`.
- `session` (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций с базой данных.
- `ids` (List[int]): Список уникальных идентификаторов записей, которые необходимо найти.

**Возвращает**:
- `records` (List[Any]): Список найденных записей. Тип записей соответствует типу модели, с которой работает DAO.

**Вызывает исключения**:
- `SQLAlchemyError`: Если возникает ошибка при выполнении запроса к базе данных.

**Как работает функция**:
1. Логирует начало поиска записей по списку ID.
2. Формирует запрос `select` к базе данных для поиска записей, чьи ID находятся в списке `ids`. Использует `cls.model.id.in_(ids)` для фильтрации по списку ID.
3. Выполняет запрос с использованием асинхронной сессии `session`.
4. Извлекает результаты запроса с помощью `scalars().all()`, который возвращает список всех найденных записей.
5. Логирует количество найденных записей.
6. Возвращает список найденных записей.
7. В случае возникновения ошибки `SQLAlchemyError`, логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования метода find_by_ids
ids = [1, 2, 3]
session = AsyncSession()  # Предполагается, что AsyncSession уже сконфигурирована
records = await BaseDAO.find_by_ids(session=session, ids=ids)

if records:
    print(f"Найдены записи: {records}")
else:
    print("Записи не найдены.")
```

### `upsert`

```python
@classmethod
async def upsert(cls, session: AsyncSession, unique_fields: List[str], values: BaseModel):
    """Создать запись или обновить существующую"""
```

**Назначение**:
Метод `upsert` предназначен для создания новой записи в базе данных или обновления существующей записи, если она уже существует. Поиск существующей записи выполняется на основе уникальных полей.

**Параметры**:
- `cls`: Ссылка на класс `BaseDAO`.
- `session` (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций с базой данных.
- `unique_fields` (List[str]): Список имен полей, которые используются для поиска существующей записи.
- `values` (BaseModel): Объект Pydantic `BaseModel`, содержащий значения для создания или обновления записи.

**Возвращает**:
- `existing` (T): Возвращает обновленную существующую запись типа `T` (наследник `Base`) или `new_instance` (T) -  созданную запись.

**Вызывает исключения**:
- `SQLAlchemyError`: Если возникает ошибка при выполнении запроса к базе данных.

**Как работает функция**:
1. Преобразует объект `values` в словарь, исключая неустановленные значения.
2. Формирует словарь `filter_dict` на основе `unique_fields` и значений из `values_dict`. Этот словарь будет использоваться для поиска существующей записи.
3. Логирует начало операции `upsert`.
4. Пытается найти существующую запись с помощью метода `find_one_or_none` и словаря `filter_dict`.
5. Если существующая запись найдена:
   - Обновляет атрибуты существующей записи значениями из `values_dict`.
   - Выполняет `session.flush()` для сохранения изменений в базе данных.
   - Логирует информацию об обновлении существующей записи.
   - Возвращает обновленную существующую запись.
6. Если существующая запись не найдена:
   - Создает новый экземпляр модели `cls.model` с использованием значений из `values_dict`.
   - Добавляет новый экземпляр в сессию SQLAlchemy.
   - Выполняет `session.flush()` для сохранения изменений в базе данных.
   - Логирует информацию о создании новой записи.
   - Возвращает новую запись.
7. В случае возникновения ошибки `SQLAlchemyError`, выполняет откат транзакции (`session.rollback()`), логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования метода upsert
from pydantic import BaseModel
from typing import List

class User(BaseModel):
    email: str
    name: str
    age: int

unique_fields = ["email"]
values = User(email="test@example.com", name="Test User", age=30)
session = AsyncSession()  # Предполагается, что AsyncSession уже сконфигурирована
record = await BaseDAO.upsert(session=session, unique_fields=unique_fields, values=values)

if record:
    print(f"Запись создана или обновлена: {record}")
else:
    print("Ошибка при создании или обновлении записи.")
```

### `bulk_update`

```python
@classmethod
async def bulk_update(cls, session: AsyncSession, records: List[BaseModel]) -> int:
    """Массовое обновление записей"""
```

**Назначение**:
Метод `bulk_update` предназначен для массового обновления записей в базе данных.

**Параметры**:
- `cls`: Ссылка на класс `BaseDAO`.
- `session` (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций с базой данных.
- `records` (List[BaseModel]): Список объектов Pydantic `BaseModel`, содержащих значения для обновления записей. Каждый объект должен иметь поле `id`, чтобы можно было определить, какую запись обновлять.

**Возвращает**:
- `updated_count` (int): Количество обновленных записей.

**Вызывает исключения**:
- `SQLAlchemyError`: Если возникает ошибка при выполнении запроса к базе данных.

**Как работает функция**:
1. Логирует начало массового обновления записей.
2. Инициализирует счетчик обновленных записей `updated_count` значением 0.
3. Перебирает записи в списке `records`.
4. Для каждой записи:
   - Преобразует объект `record` в словарь, исключая неустановленные значения.
   - Проверяет, что в словаре есть поле `id`. Если поля `id` нет, переходит к следующей записи.
   - Формирует словарь `update_data`, содержащий данные для обновления, исключая поле `id`.
   - Формирует запрос `sqlalchemy_update` к базе данных для обновления записи с указанным `id`.
   - Выполняет запрос с использованием асинхронной сессии `session`.
   - Увеличивает счетчик `updated_count` на количество обновленных записей (обычно 0 или 1).
5. После завершения цикла выполняет `session.flush()` для сохранения всех изменений в базе данных.
6. Логирует общее количество обновленных записей.
7. Возвращает общее количество обновленных записей.
8. В случае возникновения ошибки `SQLAlchemyError`, выполняет откат транзакции (`session.rollback()`), логирует ошибку и пробрасывает исключение.

**Примеры**:
```python
# Пример использования метода bulk_update
from pydantic import BaseModel
from typing import List

class UserUpdate(BaseModel):
    id: int
    name: str
    age: int

users_data = [
    UserUpdate(id=1, name="Bob Updated", age=31),
    UserUpdate(id=2, name="Charlie Updated", age=36)
]
session = AsyncSession()  # Предполагается, что AsyncSession уже сконфигурирована
updated_count = await BaseDAO.bulk_update(session=session, records=users_data)
print(f"Обновлено {updated_count} записей.")