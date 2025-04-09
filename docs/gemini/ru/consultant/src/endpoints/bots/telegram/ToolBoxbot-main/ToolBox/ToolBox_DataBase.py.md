### **Анализ кода модуля `ToolBox_DataBase.py`**

## \file /hypotez/src/endpoints/bots/telegram/ToolBoxbot-main/ToolBox/ToolBox_DataBase.py

**Качество кода**:

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код выполняет основные операции с базой данных SQLite: создание, вставка/обновление и загрузка данных.
    - Использование `literal_eval` и `json.loads` для обработки данных из базы данных.
- **Минусы**:
    - Отсутствует логирование ошибок.
    - Не все переменные и функции аннотированы типами.
    - Использование `Union[]` вместо `|`
    - Плохая читаемость кода из-за отсутствия обработки исключений и излишней краткости в некоторых местах.
    - Не все функции документированы.
    - Использование `input()` в основном блоке кода.

**Рекомендации по улучшению**:

1.  **Добавить логирование**:
    - Добавить логирование для отслеживания ошибок и предупреждений в процессе работы с базой данных.

2.  **Добавить обработку исключений**:
    - Добавить блоки `try-except` для обработки возможных исключений при работе с базой данных.
    - Логировать возникающие исключения с использованием `logger.error`.

3.  **Улучшить аннотации типов**:
    - Добавить аннотации типов для всех переменных и функций, где они отсутствуют.
    - Использовать `|` вместо `Union[]` для объединения типов.

4.  **Улучшить читаемость кода**:
    - Добавить больше комментариев для объяснения сложных участков кода.
    - Разбить длинные строки кода на несколько строк для улучшения читаемости.

5.  **Документировать функции**:
    - Добавить docstring для всех функций, включая описание аргументов, возвращаемых значений и возможных исключений.
    - Описать назначение каждого метода и класса.

6.  **Удалить `input()` из основного блока кода**:
    - Перенести код с использованием `input()` в отдельную функцию или класс для тестирования и демонстрации.

**Оптимизированный код**:

```python
import sqlite3
import json
from re import sub
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ast import literal_eval
from typing import Optional, Dict, List, Any
from src.logger import logger

"""
Модуль для работы с базой данных SQLite
==========================================

Модуль содержит класс :class:`DataBase`, который используется для взаимодействия с базой данных SQLite,
включая создание таблицы, вставку/обновление данных и загрузку данных в словарь.

Пример использования
----------------------

>>> base = DataBase(db_name='UsersData.db', table_name='users_data_table', titles={'id': 'TEXT PRIMARY KEY', 'text': 'INTEGER[]'})
>>> base.create()
>>> data = base.load_data_from_db()
"""


# Database functions class
class DataBase:
    def __init__(self, db_name: str, table_name: str, titles: Dict[str, str]) -> None:
        """
        Инициализирует класс DataBase.

        Args:
            db_name (str): Имя файла базы данных.
            table_name (str): Имя таблицы в базе данных.
            titles (Dict[str, str]): Словарь с названиями столбцов и их типами данных.
        """
        self.db_name = db_name
        self.table_name = table_name
        self.titles = titles
        self.types: Dict[str, Any] = {
            "INTEGER": lambda x: int(x),
            "BOOLEAN": lambda x: bool(x),
            "INTEGER[]": lambda x: [int(el) for el in literal_eval(sub(r"{(.*?)}", r"[\\1]", x))],
            "BOOLEAN[]": lambda x: [bool(el) for el in literal_eval(sub(r"{(.*?)}", r"[\\1]", x))],
            "TEXT[]": lambda x: [json.loads(el) for el in literal_eval(sub(r"^{(.*?)}$", r"[\\1]", x))],
            "DATETIME": lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"),
            "CHAR": lambda x: str(x),
            "TEXT": lambda x: str(x)
        }

    # Database creation function
    def create(self) -> None:
        """
        Создает таблицу в базе данных, если она не существует.
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({',\\n'.join(f'{key} {value}' for key, value in self.titles.items())})")
            conn.close()
        except sqlite3.Error as ex:
            logger.error('Error while creating table', ex, exc_info=True)

    # Function of insert or update data
    def insert_or_update_data(self, record_id: str, values: Dict[str, List[bool | int] | bool | int | str]) -> None:
        """
        Вставляет или обновляет данные в таблице.

        Args:
            record_id (str): Идентификатор записи.
            values (Dict[str, List[bool | int] | bool | int | str]): Словарь со значениями для вставки или обновления.
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            placeholders = ', '.join(['?'] * (len(self.titles)))

            sql = f"REPLACE INTO {self.table_name} ({', '.join(list(self.titles.keys()))}) VALUES ({placeholders})"
            cursor.execute(sql, [record_id] + [sub(r"^\\[(.*?)\\]$", r'{\\1}', str([json.dumps(el) if isinstance(el, dict) else int(el) for el in val])) if isinstance(val, list) else val for val in values.values()])

            conn.commit()
            conn.close()
        except sqlite3.Error as ex:
            logger.error('Error while inserting or updating data', ex, exc_info=True)

    # Function for load data in dictionary
    def load_data_from_db(self) -> Dict[str, Dict[str, List[bool | int] | bool | int | str]]:
        """
        Загружает данные из базы данных в словарь.

        Returns:
            Dict[str, Dict[str, List[bool | int] | bool | int | str]]: Словарь с данными из базы данных.
        """
        loaded_data: Dict[str, Dict[str, List[bool | int] | bool | int | str]] = {}
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(f"SELECT {', '.join(list(self.titles.keys()))} FROM {self.table_name}")
            rows = cursor.fetchall()

            for row in rows:
                record_id = row[0]
                loaded_data[record_id] = {}
                for i, (key, value) in enumerate(list(self.titles.items())[1:], 1):
                    loaded_data[record_id][key] = self.types[value](row[i])
            conn.close()
            return loaded_data
        except sqlite3.Error as ex:
            logger.error('Error while loading data from database', ex, exc_info=True)
            return {}


# Database visualization
if __name__ == "__main__":
    from src.logger import logger

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