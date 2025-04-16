### **Анализ кода модуля `ToolBox_DataBase.py`**

## \file hypotez/src/endpoints/bots/telegram/ToolBoxbot-main/ToolBox/ToolBox_DataBase.py

Модуль содержит класс `DataBase`, который используется для работы с базой данных SQLite. Он предоставляет методы для создания таблицы, вставки или обновления данных, а также загрузки данных из базы данных в словарь.

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код достаточно структурирован и разбит на функции, что облегчает понимание и поддержку.
    - Использование `sqlite3` для работы с базой данных.
    - Наличие базовой обработки типов данных при загрузке из БД.
- **Минусы**:
    - Отсутствует логирование исключений.
    - Плохая читаемость кода в некоторых местах (например, в функции `insert_or_update_data`).
    - Не все переменные и функции аннотированы типами.
    - Отсутствует документация в формате docstring для класса и методов.
    - Не используется `j_loads` для работы с `json`.
    - В сложных выражениях использутется `sub`, что ухудшает читаемость кода.

**Рекомендации по улучшению:**

1.  **Добавить документацию в формате docstring для класса `DataBase` и всех его методов.** Это сделает код более понятным и удобным в использовании.
2.  **Добавить логирование исключений.** Это поможет в отладке и выявлении проблем.
3.  **Улучшить читаемость кода в функции `insert_or_update_data`.** Разбить сложные выражения на несколько простых.
4.  **Добавить аннотации типов для всех переменных и функций.**
5.  **Заменить `sub` на более читаемые методы работы со строками, если это возможно.**
6. **Вместо `Union[]` использовать `|`**
7.  **Изменить способ форматирования строк, чтобы он был более читаемым и соответствовал современным стандартам Python (f-strings).**
8. **Использовать `j_loads` для работы с `json`**

**Оптимизированный код:**

```python
import sqlite3
import json
from re import sub
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ast import literal_eval
from typing import Any, Optional, Dict, List
from src.logger import logger

# Класс для работы с базой данных
class DataBase:
    """
    Класс для работы с базой данных SQLite.

    Предоставляет методы для создания таблицы, вставки или обновления данных,
    а также загрузки данных из базы данных в словарь.
    """
    def __init__(self, db_name: str, table_name: str, titles: Dict[str, str]) -> None:
        """
        Инициализация класса DataBase.

        Args:
            db_name (str): Имя файла базы данных.
            table_name (str): Имя таблицы в базе данных.
            titles (Dict[str, str]): Словарь, определяющий имена столбцов и их типы данных.
                                     Пример: {"id": "TEXT PRIMARY KEY", "text": "INTEGER[]"}
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
        Создает таблицу в базе данных, если она не существует.
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({',\\n'.join(f'{key} {value}' for key, value in self.titles.items())})")
            conn.close()
        except sqlite3.Error as ex:
            logger.error('Ошибка при создании таблицы', ex, exc_info=True)

    # Функция для вставки или обновления данных
    def insert_or_update_data(self, record_id: str, values: Dict[str, list[bool|int]|bool|int|str]) -> None:
        """
        Вставляет новую запись или обновляет существующую запись в таблице.

        Args:
            record_id (str): Идентификатор записи.
            values (Dict[str, list[bool|int]|bool|int|str]): Словарь значений для вставки или обновления.
                                                         Ключи словаря должны соответствовать именам столбцов в таблице.
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            placeholders = ', '.join(['?'] * (len(self.titles)))

            sql = f"REPLACE INTO {self.table_name} ({', '.join(list(self.titles.keys()))}) VALUES ({placeholders})"

            # Подготовка значений для вставки
            prepared_values = []
            for val in values.values():
                if isinstance(val, list):
                    # Преобразование списка в строку, пригодную для хранения в SQLite
                    prepared_val = sub(r"^\[(.*?)\\]$", r'{\1}', str([json.dumps(el) if isinstance(el, dict) else int(el) for el in val]))
                else:
                    prepared_val = val
                prepared_values.append(prepared_val)

            # Выполнение SQL-запроса
            cursor.execute(sql, [record_id] + prepared_values)

            conn.commit()
            conn.close()
        except sqlite3.Error as ex:
            logger.error('Ошибка при вставке или обновлении данных', ex, exc_info=True)
        except json.JSONDecodeError as ex:
            logger.error('Ошибка при кодировании JSON', ex, exc_info=True)
        except Exception as ex:
            logger.error('Непредвиденная ошибка', ex, exc_info=True)

    # Функция для загрузки данных в словарь
    def load_data_from_db(self) -> Dict[str, Dict[str, list[bool|int]|bool|int|str]]:
        """
        Загружает данные из таблицы базы данных в словарь.

        Returns:
            Dict[str, Dict[str, list[bool|int]|bool|int|str]]: Словарь, где ключи - это идентификаторы записей,
                                                           а значения - словари с данными для каждой записи.
        """
        loaded_data = {}
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
        except sqlite3.Error as ex:
            logger.error('Ошибка при загрузке данных из базы данных', ex, exc_info=True)
        except Exception as ex:
            logger.error('Непредвиденная ошибка', ex, exc_info=True)
        return loaded_data

# Визуализация базы данных
if __name__ == "__main__":
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