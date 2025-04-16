# Модуль для работы с базой данных

## Обзор

Модуль `src.endpoints.bots.google_drive.plugins.ToolBox.ToolBox_DataBase` предоставляет класс `DataBase` для управления базой данных SQLite.

## Подробней

Модуль содержит класс `DataBase`, который позволяет создавать, вставлять, обновлять и загружать данные из базы данных SQLite.

## Классы

### `DataBase`

**Описание**: Класс для управления базой данных SQLite.

**Атрибуты**:

*   `db_name` (str): Имя файла базы данных.
*   `table_name` (str): Имя таблицы в базе данных.
*   `titles` (dict[str, str]): Словарь, определяющий структуру таблицы (имена столбцов и типы данных).
*    `types` (dict): Словарь лямбда функций для преобразования типов данных

**Методы**:

*   `__init__(self, db_name: str, table_name: str, titles: dict[str, str]) -> None`: Инициализирует объект `DataBase`.
*   `create(self) -> None`: Создает таблицу в базе данных, если она не существует.
*   `insert_or_update_data(self, record_id: str, values: dict[str, list[bool|int]|bool|int|str]) -> None`: Вставляет или обновляет данные в таблице.
*   `load_data_from_db(self) -> dict[str, dict[str, list[bool|int]|bool|int|str]]`: Загружает данные из таблицы в словарь.

## Методы класса `DataBase`

### `__init__`

```python
def __init__(self, db_name: str, table_name: str, titles: dict[str, str]) -> None:
```

**Назначение**: Инициализирует объект `DataBase`.

**Параметры**:

*   `db_name` (str): Имя файла базы данных.
*   `table_name` (str): Имя таблицы в базе данных.
*   `titles` (dict[str, str]): Словарь, определяющий структуру таблицы (имена столбцов и типы данных).

**Как работает функция**:

1.  Сохраняет переданные значения в атрибуты объекта.
2.  Определяет словарь лямбда функций для преобразования типов данных

### `create`

```python
def create(self) -> None:
```

**Назначение**: Создает таблицу в базе данных, если она не существует.

**Как работает функция**:

1.  Подключается к базе данных SQLite.
2.  Выполняет SQL-запрос для создания таблицы с использованием информации из атрибута `titles`.
3.  Закрывает соединение с базой данных.

### `insert_or_update_data`

```python
def insert_or_update_data(self, record_id: str, values: dict[str, list[bool|int]|bool|int|str]) -> None:
```

**Назначение**: Вставляет или обновляет данные в таблице.

**Параметры**:

*   `record_id` (str): ID записи для вставки или обновления.
*   `values` (dict[str, list[bool|int]|bool|int|str]): Словарь со значениями для вставки или обновления.

**Как работает функция**:

1.  Подключается к базе данных SQLite.
2.  Формирует SQL-запрос для вставки или обновления данных, используя команду `REPLACE INTO`.
3.  Выполняет SQL-запрос с использованием переданных значений.
4.  Выполняет коммит и закрывает соединение с базой данных.

### `load_data_from_db`

```python
def load_data_from_db(self) -> dict[str, dict[str, list[bool|int]|bool|int|str]]:
```

**Назначение**: Загружает данные из таблицы в словарь.

**Возвращает**:

*   `dict[str, dict[str, list[bool|int]|bool|int|str]]`: Словарь с загруженными данными.

**Как работает функция**:

1.  Подключается к базе данных SQLite.
2.  Выполняет SQL-запрос для выбора всех данных из таблицы.
3.  Итерируется по строкам результата запроса.
4.  Для каждой строки создает словарь, где ключи - имена столбцов, а значения - значения столбцов.
5.  Возвращает словарь с загруженными данными.

## Использование

Модуль `ToolBox_DataBase` предоставляет простой интерфейс для работы с базой данных SQLite. Это позволяет легко создавать, вставлять, обновлять и загружать данные, что полезно для хранения и управления информацией в Telegram-боте.

**Пример использования:**

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