## Как использовать класс DataBase
=========================================================================================

Описание
-------------------------
Класс `DataBase` предоставляет набор функций для работы с базой данных SQLite. Он позволяет создавать таблицы, вставлять или обновлять данные, а также загружать данные в словарь Python.

Шаги выполнения
-------------------------
1. **Инициализация**: Создайте объект класса `DataBase`, передав имя базы данных (`db_name`), имя таблицы (`table_name`) и словарь с названиями столбцов и их типами (`titles`).
2. **Создание таблицы**: Вызовите метод `create()` для создания таблицы с заданными параметрами, если она еще не существует.
3. **Вставка/Обновление данных**: Используйте метод `insert_or_update_data()` для добавления или обновления данных в таблице. Передайте идентификатор записи (`record_id`) и словарь с данными (`values`).
4. **Загрузка данных**: Вызовите метод `load_data_from_db()` для загрузки всех данных из таблицы в словарь Python. Ключом словаря будет идентификатор записи, а значением - словарь с данными этой записи.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.bots.telegram.ToolBoxbot-main.ToolBox.ToolBox_DataBase import DataBase

# Создание объекта DataBase
base = DataBase(db_name="UsersData.db", table_name="users_data_table", titles={
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
    "ref": "TEXT"
})

# Создание таблицы (если она еще не существует)
base.create()

# Вставка/Обновление данных
uid = "1234567890"
db = base.load_data_from_db() 
db[uid] = {"text": [0]*8, "sessions_messages": [], "some": False, "images": "", 
           "free": False, "basic": False, "pro": False, "incoming_tokens": 0, 
           "outgoing_tokens": 0, "free_requests": 10, 
           "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(days=1), 
           "promocode": False, "ref": ""}
base.insert_or_update_data(uid, db[uid])

# Загрузка данных
loaded_data = base.load_data_from_db() 
print(loaded_data) 
```