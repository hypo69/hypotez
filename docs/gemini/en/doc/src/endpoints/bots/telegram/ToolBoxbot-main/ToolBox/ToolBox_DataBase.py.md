# Модуль ToolBox_DataBase.py

## Обзор

Модуль `ToolBox_DataBase.py` предоставляет класс `DataBase` для работы с базой данных SQLite. Он включает функции для создания таблицы, вставки или обновления данных, а также загрузки данных из базы данных в словарь.

## Более подробная информация

Модуль предназначен для управления данными, хранящимися в базе данных SQLite. Класс `DataBase` предоставляет интерфейс для выполнения основных операций с базой данных, таких как создание таблицы, добавление или обновление записей, а также загрузка данных в удобном формате словаря. Это упрощает взаимодействие с базой данных и позволяет легко интегрировать ее в другие части проекта.

## Классы

### `DataBase`

**Описание**: Класс для управления базой данных SQLite.

**Атрибуты**:
- `db_name` (str): Имя файла базы данных.
- `table_name` (str): Имя таблицы в базе данных.
- `titles` (dict[str, str]): Словарь, определяющий структуру таблицы (имена столбцов и их типы данных).
- `types` (dict[str, function]): Словарь, содержащий функции преобразования типов данных из строк в соответствующие типы Python.

**Методы**:
- `__init__(self, db_name: str, table_name: str, titles: dict[str, str]) -> None`: Инициализирует экземпляр класса `DataBase`.
- `create(self) -> None`: Создает таблицу в базе данных, если она не существует.
- `insert_or_update_data(self, record_id: str, values: dict[str, list[bool|int]|bool|int|str]) -> None`: Вставляет или обновляет данные в таблице.
- `load_data_from_db(self) -> dict[str, dict[str, list[bool|int]|bool|int|str]]`: Загружает данные из базы данных в словарь.

**Принцип работы**:

1.  **Инициализация**:
    *   При создании экземпляра класса `DataBase` задаются имя базы данных (`db_name`), имя таблицы (`table_name`) и структура таблицы (`titles`).
    *   Также определяется словарь `types`, который содержит функции для преобразования типов данных, извлеченных из базы данных.

2.  **Создание таблицы**:
    *   Метод `create` создает таблицу в базе данных, если она еще не существует.
    *   Структура таблицы определяется на основе словаря `titles`, где ключи - это имена столбцов, а значения - типы данных.

3.  **Вставка или обновление данных**:
    *   Метод `insert_or_update_data` вставляет новую запись в таблицу или обновляет существующую, если запись с указанным `record_id` уже существует.
    *   Данные для вставки или обновления передаются в словаре `values`, где ключи - это имена столбцов, а значения - значения, которые нужно вставить или обновить.
    *   Для столбцов, содержащих списки, значения преобразуются в строковый формат, пригодный для хранения в базе данных SQLite.

4.  **Загрузка данных**:
    *   Метод `load_data_from_db` загружает все данные из таблицы в словарь.
    *   Ключами словаря являются значения столбца `id` (первичный ключ), а значениями - словари, содержащие данные для каждой записи.
    *   При загрузке данных выполняется преобразование типов данных с использованием функций, определенных в словаре `types`.

## Методы класса

### `__init__`

```python
def __init__(self, db_name: str, table_name: str, titles: dict[str, str]) -> None:
    """Инициализирует экземпляр класса DataBase.

    Args:
        db_name (str): Имя файла базы данных.
        table_name (str): Имя таблицы в базе данных.
        titles (dict[str, str]): Словарь, определяющий структуру таблицы (имена столбцов и их типы данных).

    """
    ...
```

### `create`

```python
def create(self) -> None:
    """Создает таблицу в базе данных, если она не существует.

    """
    ...
```

### `insert_or_update_data`

```python
def insert_or_update_data(self, record_id: str, values: dict[str, list[bool|int]|bool|int|str]) -> None:
    """Вставляет или обновляет данные в таблице.

    Args:
        record_id (str): Идентификатор записи.
        values (dict[str, list[bool|int]|bool|int|str]): Словарь со значениями для вставки или обновления.

    """
    ...
```

### `load_data_from_db`

```python
def load_data_from_db(self) -> dict[str, dict[str, list[bool|int]|bool|int|str]]:
    """Загружает данные из базы данных в словарь.

    Returns:
        dict[str, dict[str, list[bool|int]|bool|int|str]]: Словарь с данными из базы данных. Ключи - идентификаторы записей, значения - словари с данными.

    """
    ...
```

## Примеры

Пример создания экземпляра класса `DataBase` и выполнения операций с базой данных:

```python
base = DataBase(
    db_name="UsersData.db",
    table_name="users_data_table",
    titles={
        "id": "TEXT PRIMARY KEY",
        "text": "INTEGER[]",
        "sessions_messages": "TEXT[]",
        "some": "BOOLEAN",
        "images": "CHAR",
        "free": "BOOLEAN",
        "basic": "BOOLEAN",
        "pro": "BOOLEAN",
        "incoming_tokens": "INTEGER",
        "outgoing_tokens": "INTEGER",
        "free_requests": "INTEGER",
        "datetime_sub": "DATETIME",
        "promocode": "BOOLEAN",
        "ref": "TEXT",
    },
)
base.create()
db = base.load_data_from_db()
N = 8
uid = input()
if uid != "":
    if "pro" in uid:
        db[uid.split()[0]] = {
            "text": [0] * N,
            "sessions_messages": [],
            "some": False,
            "images": "",
            "free": False,
            "basic": True,
            "pro": True,
            "incoming_tokens": 1.7 * 10**5,
            "outgoing_tokens": 5 * 10**5,
            "free_requests": 10,
            "datetime_sub": datetime.now().replace(microsecond=0) + relativedelta(months=1),
            "promocode": False,
            "ref": "",
        }
    elif "admin" in uid:
        db[uid.split()[0]] = {
            "text": [0] * N,
            "sessions_messages": [],
            "some": False,
            "images": "",
            "free": False,
            "basic": True,
            "pro": True,
            "incoming_tokens": 100 * 10**5,
            "outgoing_tokens": 100 * 10**5,
            "free_requests": 1000,
            "datetime_sub": datetime.now().replace(microsecond=0) + relativedelta(years=5),
            "promocode": False,
            "ref": "",
        }
    else:
        db[uid] = {
            "text": [0] * N,
            "sessions_messages": [],
            "some": False,
            "images": "",
            "free": False,
            "basic": False,
            "pro": False,
            "incoming_tokens": 0,
            "outgoing_tokens": 0,
            "free_requests": 10,
            "datetime_sub": datetime.now().replace(microsecond=0) + relativedelta(days=1),
            "promocode": False,
            "ref": "",
        }
    base.insert_or_update_data(uid.split()[0], db[uid.split()[0]])