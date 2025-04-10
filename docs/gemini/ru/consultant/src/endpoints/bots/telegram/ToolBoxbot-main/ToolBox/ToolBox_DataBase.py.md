### **Анализ кода модуля `ToolBox_DataBase.py`**

## \file /hypotez/src/endpoints/bots/telegram/ToolBoxbot-main/ToolBox/ToolBox_DataBase.py

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код выполняет основные функции для работы с базой данных SQLite.
    - Присутствуют функции для создания таблицы, добавления/обновления данных и загрузки данных в словарь.
    - Код достаточно читаемый и структурированный.
- **Минусы**:
    - Отсутствует обработка исключений при работе с базой данных.
    - Использование `literal_eval` может быть небезопасным.
    - Не все переменные аннотированы типами.
    - Не хватает документации в формате docstring для функций и класса.
    - Есть проблемы с форматированием кода (например, отсутствие пробелов вокруг операторов).
    - Использование `sub` с регулярными выражениями выглядит сложным для восприятия, возможно стоит упростить.
    - В функции `insert_or_update_data` используется небезопасное форматирование SQL-запроса (SQL injection).

**Рекомендации по улучшению:**

1.  **Добавить docstring**:
    - Добавить подробное описание класса `DataBase` и всех его методов.
    - Описать назначение каждого аргумента и возвращаемого значения.
    - Указать, какие исключения могут быть выброшены.

2.  **Обработка исключений**:
    - Обернуть операции с базой данных в блоки `try...except` для обработки возможных ошибок (например, `sqlite3.Error`).
    - Логировать возникающие исключения с использованием модуля `logger` из `src.logger`.

3.  **Безопасность**:
    - Использовать параметризованные запросы для предотвращения SQL injection в методе `insert_or_update_data`.
    - Рассмотреть возможность замены `literal_eval` на более безопасные методы десериализации данных.

4.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, где это возможно.
    - Уточнить типы данных в аннотациях (например, использовать `list[int]` вместо `list[bool|int]`).

5.  **Форматирование кода**:
    - Привести код в соответствие со стандартами PEP8.
    - Добавить пробелы вокруг операторов присваивания и других операторов.
    - Использовать более понятные имена переменных.

6.  **Упрощение кода**:
    - Попробовать упростить логику преобразования данных в методах `insert_or_update_data` и `load_data_from_db`.
    - Избегать использования сложных регулярных выражений, если есть более простые альтернативы.

7.  **Логирование**:
    - Добавить логирование важных этапов работы с базой данных (например, создание подключения, выполнение запросов, обработка результатов).

8.  **Использовать `j_loads`**:
    - Если `TEXT[]` содержит JSON, то использовать `j_loads` для десериализации.

**Оптимизированный код:**

```python
import sqlite3
import json
from re import sub
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ast import literal_eval
from typing import Optional, List, Dict, Any
from src.logger import logger #  Используй модуль logger из src.logger.logger.

# Класс для работы с базой данных
class DataBase:
    """
    Класс для управления базой данных SQLite.

    Позволяет создавать таблицы, добавлять, обновлять и загружать данные.
    """

    def __init__(self, db_name: str, table_name: str, titles: Dict[str, str]) -> None:
        """
        Инициализирует экземпляр класса DataBase.

        Args:
            db_name (str): Имя файла базы данных.
            table_name (str): Имя таблицы в базе данных.
            titles (Dict[str, str]): Словарь, содержащий названия столбцов и их типы данных.
        """
        self.db_name = db_name
        self.table_name = table_name
        self.titles = titles
        self.types = {
            "INTEGER": lambda x: int(x),
            "BOOLEAN": lambda x: bool(x),
            "INTEGER[]": lambda x: [int(el) for el in literal_eval(sub(r"{(.*?)}", r"[\\1]", x))],
            "BOOLEAN[]": lambda x: [bool(el) for el in literal_eval(sub(r"{(.*?)}", r"[\\1]", x))],
            "TEXT[]": lambda x: [json.loads(el) for el in literal_eval(sub(r"^{(.*?)}$", r"[\\1]", x))],
            "DATETIME": lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"),
            "CHAR": lambda x: str(x),
            "TEXT": lambda x: str(x)
        }

    # Функция создания базы данных
    def create(self) -> None:
        """
        Создает таблицу в базе данных, если она не существует.
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({',\\n'.join(f'{key} {value}' for key, value in self.titles.items())})")
            conn.commit() #  Подтверждаем изменения
            logger.info(f'Table {self.table_name} created successfully in {self.db_name}') #  Логируем успешное создание таблицы
        except sqlite3.Error as ex:
            logger.error(f'Error creating table {self.table_name} in {self.db_name}', ex, exc_info=True) #  Логируем ошибку при создании таблицы
        finally:
            if conn:
                conn.close() #  Закрываем соединение с базой данных

    # Функция для вставки или обновления данных
    def insert_or_update_data(self, record_id: str, values: Dict[str, list[bool | int] | bool | int | str]) -> None:
        """
        Вставляет или обновляет данные в таблице.

        Args:
            record_id (str): Идентификатор записи.
            values (Dict[str, list[bool | int] | bool | int | str]): Словарь со значениями для вставки или обновления.
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            placeholders = ', '.join(['?'] * (len(self.titles)))

            sql = f"REPLACE INTO {self.table_name} ({', '.join(list(self.titles.keys()))}) VALUES ({placeholders})"
            # Используем параметризованные запросы для предотвращения SQL injection
            data = [record_id] + [
                sub(r"^\\[(.*?)\\]$", r'{\\1}', str([json.dumps(el) if isinstance(el, dict) else int(el) for el in val]))
                if isinstance(val, list) else val for val in values.values()
            ]
            cursor.execute(sql, data) #  Передаем данные в запрос

            conn.commit()
            logger.info(f'Data inserted or updated successfully for record_id {record_id} in {self.table_name}') #  Логируем успешную вставку или обновление данных
        except sqlite3.Error as ex:
            logger.error(f'Error inserting or updating data for record_id {record_id} in {self.table_name}', ex, exc_info=True) #  Логируем ошибку при вставке или обновлении данных
        finally:
            if conn:
                conn.close() #  Закрываем соединение с базой данных

    # Функция для загрузки данных в словарь
    def load_data_from_db(self) -> Dict[str, Dict[str, list[bool | int] | bool | int | str]]:
        """
        Загружает данные из базы данных в словарь.

        Returns:
            Dict[str, Dict[str, list[bool | int] | bool | int | str]]: Словарь, содержащий данные из базы данных.
        """
        loaded_data: Dict[str, Dict[str, list[bool | int] | bool | int | str]] = {}
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT {', '.join(list(self.titles.keys()))} FROM {self.table_name}")
            rows = cursor.fetchall()
            for row in rows:
                record_id = row[0]
                loaded_data[record_id] = {}
                for i, (key, value) in enumerate(list(self.titles.items())[1:], 1):
                    loaded_data[record_id][key] = self.types[value](row[i])
            logger.info(f'Data loaded successfully from {self.table_name}') #  Логируем успешную загрузку данных
        except sqlite3.Error as ex:
            logger.error(f'Error loading data from {self.table_name}', ex, exc_info=True) #  Логируем ошибку при загрузке данных
        finally:
            conn.close()
        return loaded_data

# Визуализация базы данных
if __name__ == "__main__":
    base = DataBase(db_name="UsersData.db", table_name="users_data_table", titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]",
                        "sessions_messages": "TEXT[]", "some": "BOOLEAN",
                        "images": "CHAR", "free" : "BOOLEAN", "basic" : "BOOLEAN",
                        "pro" : "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens" : "INTEGER",
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