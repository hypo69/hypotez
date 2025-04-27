# Модуль `ToolBox_DataBase`

## Обзор

Модуль `ToolBox_DataBase` предоставляет инструменты для работы с базой данных SQLite, используемой в проекте. Он содержит класс `DataBase`, который позволяет создавать, обновлять и извлекать данные из таблицы базы данных.

## Детали

Данный модуль используется для управления данными пользователей в контексте Telegram-бота. Класс `DataBase` обеспечивает функциональность для хранения информации о пользователе, такой как его ID, количество сессий, сообщения, изображения, статус подписки, использованные токены, дата окончания подписки и другие параметры.

## Классы

### `DataBase`

**Описание**: Класс `DataBase` представляет собой интерфейс для работы с базой данных SQLite. Он предоставляет методы для создания таблицы, вставки или обновления данных, а также загрузки данных из базы данных.

**Атрибуты**:

- `db_name` (str): Имя файла базы данных.
- `table_name` (str): Название таблицы в базе данных.
- `titles` (dict[str, str]): Словарь, содержащий имена столбцов таблицы и их типы данных.

**Методы**:

- `create()`: Создает таблицу в базе данных, если она не существует.
- `insert_or_update_data(record_id: str, values: dict[str, list[bool|int]|bool|int|str])`: Вставляет новую запись в таблицу или обновляет существующую запись, используя заданный ID.
- `load_data_from_db()`: Загружает все данные из таблицы в виде словаря.

## Функции

### `create()`

**Цель**: Создать таблицу в базе данных, если она не существует.

**Параметры**: 
- Отсутствуют.

**Возвращает**: 
- None.

**Использует**:
- `sqlite3.connect()`: Подключается к базе данных.
- `cursor.execute()`: Выполняет SQL-запрос для создания таблицы.

**Пример**:

```python
base = DataBase(db_name="UsersData.db", table_name="users_data_table", titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]", "sessions_messages": "TEXT[]", "some": "BOOLEAN", "images": "CHAR", "free": "BOOLEAN", "basic": "BOOLEAN", "pro": "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens": "INTEGER", "free_requests": "INTEGER", "datetime_sub": "DATETIME", "promocode": "BOOLEAN", "ref": "TEXT"})
base.create()
```

### `insert_or_update_data(record_id: str, values: dict[str, list[bool|int]|bool|int|str])`

**Цель**: Вставить новую запись в таблицу или обновить существующую запись.

**Параметры**:

- `record_id` (str): ID записи, которую нужно вставить или обновить.
- `values` (dict[str, list[bool|int]|bool|int|str]): Словарь, содержащий значения для записи.

**Возвращает**:
- None.

**Использует**:
- `sqlite3.connect()`: Подключается к базе данных.
- `cursor.execute()`: Выполняет SQL-запрос для вставки или обновления записи.

**Пример**:

```python
db = base.load_data_from_db()
db["user_id"] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": False, "pro": False, "incoming_tokens": 0, "outgoing_tokens": 0, "free_requests": 10, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(days=1), "promocode": False, "ref": ""}
base.insert_or_update_data("user_id", db["user_id"])
```

### `load_data_from_db()`

**Цель**: Загрузить все данные из таблицы в виде словаря.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- dict[str, dict[str, list[bool|int]|bool|int|str]]: Словарь, где ключами являются ID записей, а значениями - словари, содержащие данные для каждой записи.

**Использует**:
- `sqlite3.connect()`: Подключается к базе данных.
- `cursor.execute()`: Выполняет SQL-запрос для получения всех записей.

**Пример**:

```python
db = base.load_data_from_db()
print(db)
```

## Примеры

```python
from ToolBox_DataBase import DataBase
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Создание экземпляра класса DataBase
base = DataBase(db_name="UsersData.db", table_name="users_data_table", titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]", "sessions_messages": "TEXT[]", "some": "BOOLEAN", "images": "CHAR", "free": "BOOLEAN", "basic": "BOOLEAN", "pro": "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens": "INTEGER", "free_requests": "INTEGER", "datetime_sub": "DATETIME", "promocode": "BOOLEAN", "ref": "TEXT"})

# Создание таблицы
base.create()

# Загрузка данных из базы данных
db = base.load_data_from_db()

# Вставка или обновление данных
db["user_id"] = {"text": [0]*8, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": False, "pro": False, "incoming_tokens": 0, "outgoing_tokens": 0, "free_requests": 10, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(days=1), "promocode": False, "ref": ""}
base.insert_or_update_data("user_id", db["user_id"])
```