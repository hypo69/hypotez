# Модуль для работы с базой данных

## Обзор

Модуль `ToolBox_DataBase.py` предоставляет класс `DataBase`, который обеспечивает взаимодействие с базой данных SQLite для хранения и управления данными пользователей. 

## Подробнее

Модуль реализует класс `DataBase`, который позволяет создавать таблицу в базе данных SQLite, вставлять или обновлять записи в таблице, а также загружать данные из таблицы в словарь.  

## Классы

### `DataBase`

**Описание**: Класс для работы с базой данных SQLite.

**Атрибуты**:

- `db_name` (str): Имя файла базы данных.
- `table_name` (str): Имя таблицы в базе данных.
- `titles` (dict[str, str]): Словарь с названиями столбцов таблицы и их типами данных.

**Методы**:

- `create()`: Создает таблицу в базе данных, если она еще не существует.
- `insert_or_update_data(record_id: str, values: dict[str, list[bool|int]|bool|int|str])`: Вставляет новую запись или обновляет существующую запись в таблице.
- `load_data_from_db()`: Загружает все данные из таблицы в словарь.

#### **Метод `create()`**

**Назначение**: Создает таблицу в базе данных, если она еще не существует.

**Параметры**:

-  Отсутствуют

**Возвращает**:

-  `None`

**Как работает метод**:

- Метод `create` устанавливает соединение с базой данных.
- Использует `sqlite3.connect` для подключения к базе данных.
- Создает курсор `cursor`.
- Формирует запрос SQL для создания таблицы `CREATE TABLE IF NOT EXISTS`.
- Выполняет запрос с помощью метода `cursor.execute`.
- Закрывает соединение с помощью метода `conn.close`.

#### **Метод `insert_or_update_data()`**

**Назначение**: Вставляет новую запись или обновляет существующую запись в таблице.

**Параметры**:

- `record_id` (str):  Идентификатор записи.
- `values` (dict[str, list[bool|int]|bool|int|str]): Словарь с данными для записи.

**Возвращает**:

- `None`

**Как работает метод**:

- Метод `insert_or_update_data` устанавливает соединение с базой данных.
- Использует `sqlite3.connect` для подключения к базе данных.
- Создает курсор `cursor`.
- Формирует запрос SQL для вставки или обновления записи.
-  Использует оператор `REPLACE INTO` для обновления записи, если она уже существует.
- Выполняет запрос с помощью метода `cursor.execute`.
- Сохраняет изменения с помощью метода `conn.commit`.
- Закрывает соединение с помощью метода `conn.close`.

#### **Метод `load_data_from_db()`**

**Назначение**: Загружает все данные из таблицы в словарь.

**Параметры**:

-  Отсутствуют.

**Возвращает**:

- `dict[str, dict[str, list[bool|int]|bool|int|str]]`: Словарь, где ключом является идентификатор записи, а значением - словарь с данными записи.

**Как работает метод**:

- Метод `load_data_from_db` устанавливает соединение с базой данных.
- Использует `sqlite3.connect` для подключения к базе данных.
- Создает курсор `cursor`.
- Формирует запрос SQL для выборки всех данных из таблицы.
- Выполняет запрос с помощью метода `cursor.execute`.
- Получает список всех строк из таблицы с помощью метода `cursor.fetchall()`.
- Создает словарь `loaded_data`.
- Перебирает все строки `rows` из таблицы.
- Для каждой строки:
    - Извлекает идентификатор записи `id`.
    - Создает пустой словарь `loaded_data[id]`.
    - Перебирает все столбцы таблицы (кроме столбца `id`).
    - Заполняет словарь `loaded_data[id]` данными из строки `row` с помощью функции `types` для преобразования типов данных.
- Закрывает соединение с помощью метода `conn.close`.
- Возвращает словарь `loaded_data`.

## Примеры

```python
# Создание экземпляра класса DataBase
base = DataBase(db_name="UsersData.db", table_name="users_data_table", titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]",\
                        "sessions_messages": "TEXT[]", "some": "BOOLEAN",\
                        "images": "CHAR", "free" : "BOOLEAN", "basic" : "BOOLEAN",\
                        "pro" : "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens" : "INTEGER",\
                        "free_requests" : "INTEGER", "datetime_sub": "DATETIME", "promocode": "BOOLEAN", "ref": "TEXT"})

# Создание таблицы
base.create()

# Загрузка данных из таблицы
db = base.load_data_from_db()

# Вставка или обновление записи
uid = input()
if uid != '':
    if "pro" in uid:
        db[uid.split()[0]] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": True, "pro": True, "incoming_tokens": 1.7*10**5, "outgoing_tokens": 5*10**5, "free_requests": 10, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(months=1), "promocode": False, "ref": ""}
    elif 'admin' in uid:
        db[uid.split()[0]] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": True, "pro": True, "incoming_tokens": 100*10**5, "outgoing_tokens": 100*10**5, "free_requests": 1000, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(years=5), "promocode": False, "ref": ""}
    else:
        db[uid] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": False, "pro": False, "incoming_tokens": 0, "outgoing_tokens": 0, "free_requests": 10, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(days=1), "promocode": False, "ref": ""}
    base.insert_or_update_data(uid.split()[0], db[uid.split()[0]])
```

## Дополнительная информация

- В коде используется словарь `types` для преобразования типов данных из базы данных.
- Для работы с датами используется модуль `datetime` и `dateutil.relativedelta`.
- Для работы с JSON используется модуль `json`.
- Для преобразования строки в список используется функция `literal_eval` из модуля `ast`.
- Для преобразования строки в JSON используется функция `json.loads` из модуля `json`. 
- Для преобразования списка в JSON используется функция `json.dumps` из модуля `json`.
- В коде используется функция `sub` из модуля `re` для замены подстроки в строке.
- В коде используется функция `split` из модуля `str` для разделения строки по пробелу.
-  В коде используется функция `replace` из модуля `datetime` для замены микросекунд в объекте `datetime` на 0.
-  В коде используется функция `now` из модуля `datetime` для получения текущего времени.
-  В коде используется функция `relativedelta` из модуля `dateutil.relativedelta` для добавления к объекту `datetime`  относительного периода времени.
-  В коде используется функция `input` из модуля `builtins` для получения входных данных от пользователя.
-  В коде используется функция `print` из модуля `builtins` для вывода данных на консоль.
-  В коде используется функция `len` из модуля `builtins` для получения длины списка.
-  В коде используется функция `type` из модуля `builtins` для получения типа данных.
-  В коде используется функция `isinstance` из модуля `builtins` для проверки типа данных.

## Потенциальные улучшения:

- Добавьте обработку исключений.
- Добавьте логгирование.
- Добавьте документацию к каждой функции и методу.
- Добавьте тесты.
- Добавьте комментарии для объяснения кода.
-  Проанализируй как реализуется данный код в проекте. 
-  Рассмотри все варианты использования, которые могли быть у данного кода. 
-  Включите возможность подключения к базе данных через URI.

## Замечания

- В примере кода используется `N = 8`.  Проанализируй что обозначает переменная `N`.
- Данный код не содержит обработки ошибок. 
-  Код не содержит логгирование.
-  Все комментарии в коде написаны на английском языке. Переведи комментарии на русский.
-  Код не содержит тестов.
-  Код не содержит документации.
-  Проанализируй как реализуется данный код в проекте. 
-  Рассмотри все варианты использования, которые могли быть у данного кода. 
-  Включите возможность подключения к базе данных через URI.

```python
                import sqlite3, json
from re import sub
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ast import literal_eval

# Класс функций базы данных
class DataBase:
    """
    Класс для работы с базой данных SQLite.

    Атрибуты:
        db_name (str): Имя файла базы данных.
        table_name (str): Имя таблицы в базе данных.
        titles (dict[str, str]): Словарь с названиями столбцов таблицы и их типами данных.

    Методы:
        create(): Создает таблицу в базе данных, если она еще не существует.
        insert_or_update_data(record_id: str, values: dict[str, list[bool|int]|bool|int|str]): Вставляет новую запись или обновляет существующую запись в таблице.
        load_data_from_db(): Загружает все данные из таблицы в словарь.
    """
    def __init__(self, db_name: str, table_name: str, titles: dict[str, str]) -> None:
        """
        Инициализирует объект DataBase.

        Args:
            db_name (str): Имя файла базы данных.
            table_name (str): Имя таблицы в базе данных.
            titles (dict[str, str]): Словарь с названиями столбцов таблицы и их типами данных.
        """
        self.db_name = db_name
        self.table_name = table_name
        self.titles = titles
        self.types = {
                    "INTEGER":   lambda x: int(x),
                    "BOOLEAN":   lambda x: bool(x),
                    "INTEGER[]": lambda x: [int(el) for el in literal_eval(sub(r"{(.*?)}", r"[\\1]", x))],
                    "BOOLEAN[]": lambda x: [bool(el) for el in literal_eval(sub(r"{(.*?)}", r"[\\1]", x))],
                    "TEXT[]":    lambda x: [json.loads(el) for el in literal_eval(sub(r"^{(.*?)}$", r"[\\1]", x))],
                    "DATETIME":  lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"), 
                    "CHAR":      lambda x: str(x),
                    "TEXT":      lambda x: str(x)
                    }
    
    # Функция создания базы данных
    def create(self) -> None:
        """
        Создает таблицу в базе данных, если она еще не существует.
        """
        conn = sqlite3.connect(self.db_name); cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({\',\\n\'.join(f"{key} {value}" for key, value in self.titles.items())})")
        conn.close()
        
    # Функция вставки или обновления данных
    def insert_or_update_data(self, record_id: str, values: dict[str, list[bool|int]|bool|int|str]) -> None:
        """
        Вставляет новую запись или обновляет существующую запись в таблице.

        Args:
            record_id (str): Идентификатор записи.
            values (dict[str, list[bool|int]|bool|int|str]): Словарь с данными для записи.
        """
        conn = sqlite3.connect(self.db_name); cursor = conn.cursor()
        
        placeholders = \', \'.join([\'?\'] * (len(self.titles)))
        
        sql = f"REPLACE INTO {self.table_name} ({\', \'.join(list(self.titles.keys()))}) VALUES ({placeholders})"
        cursor.execute(sql, [record_id] + [ sub(r"^\\[(.*?)\\]$", r\'{\\1}\', str([json.dumps(el) if type(el)==dict else int(el) for el in val ])) if type(val)==list else val for val in values.values() ])
        
        conn.commit(); conn.close()

    # Функция загрузки данных в словарь
    def load_data_from_db(self) -> dict[str, dict[str, list[bool|int]|bool|int|str]]:
        """
        Загружает все данные из таблицы в словарь.

        Returns:
            dict[str, dict[str, list[bool|int]|bool|int|str]]: Словарь, где ключом является идентификатор записи, а значением - словарь с данными записи.
        """
        loaded_data = dict(); conn = sqlite3.connect(self.db_name); cursor = conn.cursor()
        cursor.execute(f"SELECT {\', \'.join(list(self.titles.keys()))} FROM {self.table_name}")
        rows = cursor.fetchall()
        for row in rows:
            id = row[0]; loaded_data[id] = dict()
            for i, (key, value) in enumerate(list(self.titles.items())[1:], 1):
                loaded_data[id][key] = self.types[value](row[i])
        conn.close()
        return loaded_data

# Визуализация базы данных
if __name__ == "__main__":
    base = DataBase(db_name="UsersData.db", table_name="users_data_table", titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]",\
                        "sessions_messages": "TEXT[]", "some": "BOOLEAN",\
                        "images": "CHAR", "free" : "BOOLEAN", "basic" : "BOOLEAN",\
                        "pro" : "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens" : "INTEGER",\
                        "free_requests" : "INTEGER", "datetime_sub": "DATETIME", "promocode": "BOOLEAN", "ref": "TEXT"})
    base.create(); db = base.load_data_from_db(); N = 8
    uid = input()
    if uid != '':
        if "pro" in uid:
            db[uid.split()[0]] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": True, "pro": True, "incoming_tokens": 1.7*10**5, "outgoing_tokens": 5*10**5, "free_requests": 10, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(months=1), "promocode": False, "ref": ""}
        elif 'admin' in uid:
            db[uid.split()[0]] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": True, "pro": True, "incoming_tokens": 100*10**5, "outgoing_tokens": 100*10**5, "free_requests": 1000, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(years=5), "promocode": False, "ref": ""}
        else:
            db[uid] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": False, "pro": False, "incoming_tokens": 0, "outgoing_tokens": 0, "free_requests": 10, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(days=1), "promocode": False, "ref": ""}
        base.insert_or_update_data(uid.split()[0], db[uid.split()[0]])
                ```