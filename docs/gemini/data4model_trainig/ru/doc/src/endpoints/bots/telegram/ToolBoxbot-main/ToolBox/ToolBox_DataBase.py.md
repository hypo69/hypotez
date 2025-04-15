# Модуль для работы с базой данных `ToolBox`
=================================================

Модуль содержит класс :class:`DataBase`, который используется для создания, управления и визуализации базы данных для `ToolBox` telegram бота.

Пример использования
----------------------

```python
>>> base = DataBase(db_name="UsersData.db", table_name="users_data_table", titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]",
                        "sessions_messages": "TEXT[]", "some": "BOOLEAN",
                        "images": "CHAR", "free" : "BOOLEAN", "basic" : "BOOLEAN",
                        "pro" : "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens" : "INTEGER",
                        "free_requests" : "INTEGER", "datetime_sub": "DATETIME", "promocode": "BOOLEAN", "ref": "TEXT"})
>>> base.create()
>>> db = base.load_data_from_db()
```

## Оглавление

- [Обзор](#обзор)
- [Подробнее](#подробнее)
- [Классы](#классы)
    - [DataBase](#database)
        - [Методы](#методы)
            - [`__init__`](#__init__)
            - [`create`](#create)
            - [`insert_or_update_data`](#insert_or_update_data)
            - [`load_data_from_db`](#load_data_from_db)

## Обзор

Этот модуль предоставляет класс `DataBase` для взаимодействия с базами данных SQLite. Он включает в себя методы для создания таблиц, вставки и обновления данных, а также загрузки данных из базы данных в словарь.

## Подробнее

Модуль `ToolBox_DataBase.py` предназначен для управления базой данных, используемой в проекте `ToolBox`. Он предоставляет функциональность для создания базы данных, добавления и обновления записей, а также загрузки данных из базы данных для дальнейшего использования в боте.

## Классы

### `DataBase`

**Описание**: Класс для управления базой данных SQLite.

**Атрибуты**:
- `db_name` (str): Имя файла базы данных.
- `table_name` (str): Имя таблицы в базе данных.
- `titles` (dict[str, str]): Словарь, определяющий имена столбцов и их типы данных.
- `types` (dict[str, Callable]): Словарь, содержащий функции для преобразования типов данных из базы данных.

**Методы**:
- [`__init__`](#__init__): Инициализирует объект базы данных.
- [`create`](#create): Создает таблицу в базе данных, если она не существует.
- [`insert_or_update_data`](#insert_or_update_data): Вставляет или обновляет данные в таблице.
- [`load_data_from_db`](#load_data_from_db): Загружает данные из таблицы в словарь.

#### `__init__`

```python
def __init__(self, db_name: str, table_name: str, titles: dict[str, str]) -> None
```

**Назначение**: Инициализирует объект класса `DataBase` с указанными параметрами.

**Параметры**:
- `db_name` (str): Имя файла базы данных.
- `table_name` (str): Имя таблицы в базе данных.
- `titles` (dict[str, str]): Словарь, определяющий структуру таблицы (имена столбцов и их типы данных).

**Как работает функция**:
- Функция сохраняет переданные параметры (`db_name`, `table_name`, `titles`) в качестве атрибутов экземпляра класса.
- Определяет словарь `self.types`, который содержит функции для преобразования типов данных, извлеченных из базы данных, к соответствующим типам Python. В `self.types` лямбда-функции используются для преобразования строк в целые числа, булевы значения, списки целых чисел, списки булевых значений, списки JSON-объектов, объекты datetime и строки.

#### `create`

```python
def create(self) -> None
```

**Назначение**: Создает таблицу в базе данных, если она еще не существует.

**Как работает функция**:
- Устанавливает соединение с базой данных SQLite, используя имя файла, указанное в `self.db_name`.
- Создает объект `cursor`, который используется для выполнения SQL-запросов.
- Выполняет SQL-запрос `CREATE TABLE IF NOT EXISTS`, чтобы создать таблицу с именем `self.table_name`, если она еще не существует. Структура таблицы определяется на основе словаря `self.titles`, где ключи - это имена столбцов, а значения - их типы данных.
- Закрывает соединение с базой данных.

#### `insert_or_update_data`

```python
def insert_or_update_data(self, record_id: str, values: dict[str, list[bool|int]|bool|int|str]) -> None
```

**Назначение**: Вставляет новую запись в таблицу или обновляет существующую запись, если запись с таким `record_id` уже существует.

**Параметры**:
- `record_id` (str): Значение первичного ключа для записи.
- `values` (dict[str, list[bool|int]|bool|int|str]): Словарь, содержащий значения для вставки или обновления.

**Как работает функция**:
- Устанавливает соединение с базой данных SQLite.
- Формирует SQL-запрос `REPLACE INTO`, который либо вставляет новую запись, либо заменяет существующую запись с указанным `record_id`.
- Подготавливает значения для вставки, преобразуя списки в строки в формате, понятном для SQLite.
- Выполняет SQL-запрос с подготовленными значениями.
- Фиксирует изменения и закрывает соединение с базой данных.

#### `load_data_from_db`

```python
def load_data_from_db(self) -> dict[str, dict[str, list[bool|int]|bool|int|str]]
```

**Назначение**: Загружает данные из базы данных и возвращает их в виде словаря.

**Возвращает**:
- `dict[str, dict[str, list[bool|int]|bool|int|str]]`: Словарь, где ключи - это значения `id` (первичные ключи), а значения - это словари, содержащие данные для каждой записи.

**Как работает функция**:
- Устанавливает соединение с базой данных SQLite.
- Выполняет SQL-запрос `SELECT`, чтобы извлечь все данные из таблицы.
- Итерируется по каждой строке результата запроса.
- Для каждой строки создает словарь, где ключи - это имена столбцов (кроме `id`), а значения - это соответствующие значения из строки, преобразованные к нужным типам данных с использованием словаря `self.types`.
- Возвращает словарь, содержащий все загруженные данные.

## Пример использования

```python
base = DataBase(db_name="UsersData.db", table_name="users_data_table", titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]",
                    "sessions_messages": "TEXT[]", "some": "BOOLEAN",
                    "images": "CHAR", "free" : "BOOLEAN", "basic" : "BOOLEAN",
                    "pro" : "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens" : "INTEGER",
                    "free_requests" : "INTEGER", "datetime_sub": "DATETIME", "promocode": "BOOLEAN", "ref": "TEXT"})
base.create()
db = base.load_data_from_db()
N = 8
uid = input()
if uid != '':
    if "pro" in uid:
        db[uid.split()[0]] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": True, "pro": True, "incoming_tokens": 1.7*10**5, "outgoing_tokens": 5*10**5, "free_requests": 10, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(months=1), "promocode": False, "ref": ""}
    elif 'admin' in uid:
        db[uid.split()[0]] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": True, "pro": True, "incoming_tokens": 100*10**5, "outgoing_tokens": 100*10**5, "free_requests": 1000, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(years=5), "promocode": False, "ref": ""}
    else:
        db[uid] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": False, "pro": False, "incoming_tokens": 0, "outgoing_tokens": 0, "free_requests": 10, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(days=1), "promocode": False, "ref": ""}
    base.insert_or_update_data(uid.split()[0], db[uid.split()[0]])