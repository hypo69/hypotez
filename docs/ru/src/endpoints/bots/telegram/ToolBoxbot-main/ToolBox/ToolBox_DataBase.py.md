# Модуль для работы с базой данных `ToolBox_DataBase`

## Обзор

Модуль `ToolBox_DataBase.py` предназначен для управления базой данных SQLite, используемой в проекте `ToolBox`. Он включает в себя класс `DataBase`, который предоставляет функциональность для создания таблиц, вставки и обновления данных, а также загрузки данных из базы данных в формате словаря.

## Подробней

Этот модуль обеспечивает абстракцию для работы с базой данных, упрощая взаимодействие с ней и предоставляя удобные методы для выполнения основных операций. Он также содержит код для визуализации базы данных и добавления новых записей через ввод пользователя.

## Классы

### `DataBase`

**Описание**: Класс `DataBase` предоставляет методы для создания, чтения, записи и обновления данных в базе данных SQLite.

**Атрибуты**:

-   `db_name` (str): Имя файла базы данных.
-   `table_name` (str): Имя таблицы в базе данных.
-   `titles` (dict[str, str]): Словарь, определяющий структуру таблицы (имена столбцов и их типы данных).
-   `types` (dict[str, lambda x: ...]): Словарь, содержащий лямбда-функции для преобразования строковых значений, полученных из базы данных, в соответствующие типы данных Python.

**Методы**:

-   `__init__(self, db_name: str, table_name: str, titles: dict[str, str]) -> None`: Инициализирует объект `DataBase` с указанным именем базы данных, именем таблицы и списком заголовков столбцов.
-   `create(self) -> None`: Создает таблицу в базе данных, если она еще не существует.
-   `insert_or_update_data(self, record_id: str, values: dict[str, list[bool|int]|bool|int|str]) -> None`: Вставляет новую запись в таблицу или обновляет существующую запись с указанным `record_id`.
-   `load_data_from_db(self) -> dict[str, dict[str, list[bool|int]|bool|int|str]]`: Загружает все данные из таблицы в словарь, где ключами являются идентификаторы записей, а значениями - словари с данными каждой записи.

## Методы класса

### `__init__`

```python
def __init__(self, db_name: str, table_name: str, titles: dict[str, str]) -> None:
    """
    Инициализирует объект DataBase.

    Args:
        db_name (str): Имя файла базы данных.
        table_name (str): Имя таблицы в базе данных.
        titles (dict[str, str]): Словарь, определяющий структуру таблицы (имена столбцов и их типы данных).

    Returns:
        None
    """
    ...
```

**Параметры**:

-   `db_name` (str): Имя файла базы данных.
-   `table_name` (str): Имя таблицы в базе данных.
-   `titles` (dict[str, str]): Словарь, определяющий структуру таблицы (имена столбцов и их типы данных).

**Как работает функция**:

Сохраняет параметры `db_name`, `table_name` и `titles` в атрибуты экземпляра класса. Также определяет словарь `types`, который содержит лямбда-функции для преобразования строковых значений, полученных из базы данных, в соответствующие типы данных Python.

**Примеры**:

```python
base = DataBase(db_name="UsersData.db", table_name="users_data_table", titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]",
                    "sessions_messages": "TEXT[]", "some": "BOOLEAN",
                    "images": "CHAR", "free" : "BOOLEAN", "basic" : "BOOLEAN",
                    "pro" : "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens" : "INTEGER",
                    "free_requests" : "INTEGER", "datetime_sub": "DATETIME", "promocode": "BOOLEAN", "ref": "TEXT"})
```

### `create`

```python
def create(self) -> None:
    """
    Создает таблицу в базе данных, если она еще не существует.

    Args:
        None

    Returns:
        None
    """
    ...
```

**Как работает функция**:

Функция устанавливает соединение с базой данных SQLite, используя имя базы данных, указанное при инициализации класса (`self.db_name`). Создает объект `cursor`, который позволяет выполнять SQL-запросы.

Затем выполняется SQL-запрос `CREATE TABLE IF NOT EXISTS`, который создает таблицу с именем `self.table_name`, если она еще не существует. Структура таблицы определяется на основе словаря `self.titles`, который содержит имена столбцов и их типы данных.

В конце функция закрывает соединение с базой данных, чтобы освободить ресурсы.

**Примеры**:

```python
base = DataBase(db_name="UsersData.db", table_name="users_data_table", titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]",
                    "sessions_messages": "TEXT[]", "some": "BOOLEAN",
                    "images": "CHAR", "free" : "BOOLEAN", "basic" : "BOOLEAN",
                    "pro" : "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens" : "INTEGER",
                    "free_requests" : "INTEGER", "datetime_sub": "DATETIME", "promocode": "BOOLEAN", "ref": "TEXT"})
base.create()
```

### `insert_or_update_data`

```python
def insert_or_update_data(self, record_id: str, values: dict[str, list[bool|int]|bool|int|str]) -> None:
    """
    Вставляет новую запись в таблицу или обновляет существующую запись с указанным record_id.

    Args:
        record_id (str): Идентификатор записи.
        values (dict[str, list[bool|int]|bool|int|str]): Словарь со значениями для вставки или обновления.

    Returns:
        None
    """
    ...
```

**Параметры**:

-   `record_id` (str): Идентификатор записи, который будет использоваться для вставки или обновления данных.
-   `values` (dict[str, list[bool|int]|bool|int|str]): Словарь, содержащий имена столбцов и соответствующие значения для вставки или обновления.

**Как работает функция**:

Устанавливает соединение с базой данных SQLite. Формирует SQL-запрос `REPLACE INTO`, который вставляет новую запись в таблицу или обновляет существующую запись, если запись с таким `record_id` уже существует. Значения для вставки или обновления извлекаются из словаря `values`. Преобразует списки в формат, пригодный для хранения в базе данных, используя `json.dumps` для элементов словаря и заменяя символы `[` и `]` на `{` и `}`.

Затем выполняется SQL-запрос с помощью метода `cursor.execute`, которому передается сам SQL-запрос и список значений для вставки или обновления. После выполнения запроса изменения сохраняются в базе данных с помощью метода `conn.commit()`. В конце функция закрывает соединение с базой данных.

**Примеры**:

```python
base = DataBase(db_name="UsersData.db", table_name="users_data_table", titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]",
                    "sessions_messages": "TEXT[]", "some": "BOOLEAN",
                    "images": "CHAR", "free" : "BOOLEAN", "basic" : "BOOLEAN",
                    "pro" : "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens" : "INTEGER",
                    "free_requests" : "INTEGER", "datetime_sub": "DATETIME", "promocode": "BOOLEAN", "ref": "TEXT"})
db = base.load_data_from_db()
N = 8
uid = 'test_user'
db[uid] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": False, "pro": False, "incoming_tokens": 0, "outgoing_tokens": 0, "free_requests": 10, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(days=1), "promocode": False, "ref": ""}
base.insert_or_update_data(uid, db[uid])
```

### `load_data_from_db`

```python
def load_data_from_db(self) -> dict[str, dict[str, list[bool|int]|bool|int|str]]:
    """
    Загружает все данные из таблицы в словарь, где ключами являются идентификаторы записей, а значениями - словари с данными каждой записи.

    Args:
        None

    Returns:
        dict[str, dict[str, list[bool|int]|bool|int|str]]: Словарь, содержащий данные из таблицы.
    """
    ...
```

**Как работает функция**:

Функция устанавливает соединение с базой данных SQLite, используя имя базы данных, указанное при инициализации класса (`self.db_name`). Создает объект `cursor`, который позволяет выполнять SQL-запросы.

Затем выполняется SQL-запрос `SELECT`, который извлекает все данные из таблицы `self.table_name`. Функция получает все строки из результата запроса с помощью метода `cursor.fetchall()`.

Далее функция итерируется по каждой строке, полученной из базы данных. Для каждой строки создается запись в словаре `loaded_data`, где ключом является идентификатор записи (значение первого столбца), а значением - словарь с данными этой записи. Данные каждой записи преобразуются в соответствующие типы данных Python, используя лямбда-функции из словаря `self.types`.

В конце функция закрывает соединение с базой данных и возвращает словарь `loaded_data`.

**Примеры**:

```python
base = DataBase(db_name="UsersData.db", table_name="users_data_table", titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]",
                    "sessions_messages": "TEXT[]", "some": "BOOLEAN",
                    "images": "CHAR", "free" : "BOOLEAN", "basic" : "BOOLEAN",
                    "pro" : "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens" : "INTEGER",
                    "free_requests" : "INTEGER", "datetime_sub": "DATETIME", "promocode": "BOOLEAN", "ref": "TEXT"})
db = base.load_data_from_db()
```

## Database visualization

В блоке `if __name__ == "__main__":` представлен пример использования класса `DataBase` для создания базы данных, загрузки данных и добавления новых записей через ввод пользователя.

-   Создается экземпляр класса `DataBase` с именем базы данных "UsersData.db", именем таблицы "users\_data\_table" и списком заголовков столбцов.
-   Вызывается метод `create()` для создания таблицы в базе данных, если она еще не существует.
-   Вызывается метод `load_data_from_db()` для загрузки данных из таблицы в словарь `db`.
-   Запрашивается ввод пользователя для получения идентификатора новой записи.
-   В зависимости от введенного идентификатора, создается новая запись в словаре `db` с различными значениями для столбцов, включая информацию о подписке, количестве токенов и запросов.
-   Вызывается метод `insert_or_update_data()` для вставки или обновления записи в базе данных.