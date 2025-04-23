# Документация модуля ToolBox_DataBase

## Обзор

Модуль `ToolBox_DataBase.py` предназначен для работы с базой данных `sqlite3`. Он предоставляет класс `DataBase`, который упрощает создание, чтение, обновление и вставку данных в таблицы базы данных. Модуль также содержит пример использования класса `DataBase` для создания и заполнения данными таблицы пользователей.

## Подробней

Модуль содержит класс для управления базой данных `sqlite3`, включая создание таблиц, вставку и обновление данных, а также загрузку данных в формате словаря.  В нижней части кода находится пример использования класса `DataBase` для создания базы данных пользователей и добавления новых записей. Это может быть использовано для инициализации базы данных или для тестирования функциональности класса `DataBase`.

## Классы

### `DataBase`

**Описание**: Класс для управления базой данных SQLite.

**Атрибуты**:
- `db_name` (str): Имя файла базы данных.
- `table_name` (str): Имя таблицы в базе данных.
- `titles` (dict[str, str]): Словарь, определяющий структуру таблицы, где ключи - это названия столбцов, а значения - типы данных.
- `types` (dict[str, function]): Словарь, сопоставляющий типы данных SQLite с функциями для преобразования значений из базы данных.

**Принцип работы**:
1.  При инициализации класса `DataBase` устанавливаются имя базы данных, имя таблицы и структура таблицы (`titles`).
2.  Словарь `types` определяет, как значения из базы данных преобразуются в Python типы данных.
3.  Метод `create` создает таблицу в базе данных, если она не существует.
4.  Метод `insert_or_update_data` вставляет или обновляет запись в таблице.
5.  Метод `load_data_from_db` загружает данные из таблицы в словарь Python.

**Методы**:

### `__init__`

```python
    def __init__(self, db_name: str, table_name: str, titles: dict[str, str]) -> None:
        """Инициализирует класс DataBase.

        Args:
            db_name (str): Имя файла базы данных.
            table_name (str): Имя таблицы в базе данных.
            titles (dict[str, str]): Словарь, определяющий структуру таблицы.
        """
```

### `create`

```python
    def create(self) -> None:
        """Создает таблицу в базе данных, если она не существует."""
```

### `insert_or_update_data`

```python
    def insert_or_update_data(self, record_id: str, values: dict[str, list[bool|int]|bool|int|str]) -> None:
        """Вставляет или обновляет данные в таблице.

        Args:
            record_id (str): Значение первичного ключа записи.
            values (dict[str, list[bool|int]|bool|int|str]): Словарь значений для вставки или обновления.
        """
```

### `load_data_from_db`

```python
    def load_data_from_db(self) -> dict[str, dict[str, list[bool|int]|bool|int|str]]:
        """Загружает данные из базы данных в словарь.

        Returns:
            dict[str, dict[str, list[bool|int]|bool|int|str]]: Словарь, содержащий данные из базы данных.
        """
```

## Параметры класса

- `db_name` (str): Имя файла базы данных.
- `table_name` (str): Имя таблицы в базе данных.
- `titles` (dict[str, str]): Словарь, определяющий структуру таблицы, где ключи - это названия столбцов, а значения - типы данных.
- `types` (dict[str, function]): Словарь, сопоставляющий типы данных SQLite с функциями для преобразования значений из базы данных.

## Пример использования

```python
base = DataBase(db_name="UsersData.db", table_name="users_data_table", titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]",
                    "sessions_messages": "TEXT[]", "some": "BOOLEAN",
                    "images": "CHAR", "free" : "BOOLEAN", "basic" : "BOOLEAN",
                    "pro" : "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens" : "INTEGER",
                    "free_requests" : "INTEGER", "datetime_sub": "DATETIME", "promocode": "BOOLEAN", "ref": "TEXT"})
base.create()
db = base.load_data_from_db()
uid = input()
if uid != '':
    if "pro" in uid:
        db[uid.split()[0]] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": True, "pro": True, "incoming_tokens": 1.7*10**5, "outgoing_tokens": 5*10**5, "free_requests": 10, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(months=1), "promocode": False, "ref": ""}
    elif 'admin' in uid:
        db[uid.split()[0]] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": True, "pro": True, "incoming_tokens": 100*10**5, "outgoing_tokens": 100*10**5, "free_requests": 1000, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(years=5), "promocode": False, "ref": ""}
    else:
        db[uid] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": False, "pro": False, "incoming_tokens": 0, "outgoing_tokens": 0, "free_requests": 10, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(days=1), "promocode": False, "ref": ""}
    base.insert_or_update_data(uid.split()[0], db[uid.split()[0]])