### **Анализ кода модуля `code2file_for_chat_gpt_but_comments.py`**

## \file hypotez/toolbox/code2file_for_chat_gpt_but_comments.py.md
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

Анализ данного модуля показывает, что он предназначен для рекурсивного чтения файлов различных форматов, объединения их содержимого в один выходной файл, а также для удаления определенных файлов и директорий.

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код выполняет полезную задачу объединения файлов различных форматов в один.
  - Присутствует функциональность удаления нежелательных файлов и директорий.
  - Код достаточно хорошо документирован с описанием назначения и параметров функций.
- **Минусы**:
  - Отсутствуют аннотации типов для параметров и возвращаемых значений функций.
  - Не используются конструкции `try-except` с логированием ошибок в функциях `delete_directory_contents` и `read_text_files`.
  - Не соблюдены некоторые рекомендации PEP8 по форматированию кода (например, отсутствие пробелов вокруг операторов).
  - В коде используются конструкции типа `os.walk`, которые можно заменить на более современные и удобные средства библиотеки `pathlib`.
  - Отсутствуют docstring для модуля.

**Рекомендации по улучшению**:
1. **Добавить аннотации типов**:
   - Необходимо добавить аннотации типов для всех параметров и возвращаемых значений функций. Это улучшит читаемость и поддерживаемость кода.
2. **Улучшить обработку исключений**:
   - Обернуть операции удаления файлов и директорий в блоки `try-except` и логировать возникающие исключения с помощью `logger.error` с указанием `exc_info=True`.
3. **Соблюдать стандарты PEP8**:
   - Проверить и исправить форматирование кода в соответствии со стандартами PEP8 (например, добавить пробелы вокруг операторов присваивания).
4. **Использовать `pathlib` вместо `os.walk`**:
   - Заменить использование `os.walk` на более удобные и современные средства библиотеки `pathlib` для обхода директорий.
5. **Добавить docstring для модуля**:
   - Описать назначение модуля, основные классы и функции, а также примеры использования.
6. **Использовать f-strings для форматирования строк**:
   - Заменить конкатенацию строк на f-strings для улучшения читаемости и производительности.
7. **Перевести docstring на русский язык**:
   - Все комментарии и docstring должны быть на русском языке в формате UTF-8.

**Оптимизированный код**:

```python
## \file hypotez/toolbox/code2file_for_chat_gpt_but_comments.py.md
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для чтения и объединения текстовых файлов различных форматов в один файл.
==============================================================================

Модуль позволяет рекурсивно читать файлы с различными расширениями (текстовые, JSON, CSV, XML и др.)
из указанного каталога, объединять их содержимое в один файл, а также удалять файлы и директории,
которые начинаются с "_" или содержат символы "(" и ")".

Зависимости:
    - os
    - pathlib
    - json
    - csv
    - xml.etree.ElementTree
    - pandas
    - jupyter_client
    - yaml
    - sqlite3

Пример использования:
    >>> directory_to_search = "src"
    >>> output_file_path = "output.txt"
    >>> read_text_files(directory_to_search, output_file_path)
"""
import os
from pathlib import Path
import json
import csv
import xml.etree.ElementTree as ET
import pandas as pd
from jupyter_client import kernelspec
import yaml
import sqlite3

from src.logger import logger # Используем logger из src.logger
from typing import Optional

def delete_directory_contents(directory: Path) -> None:
    """Рекурсивно удаляет все содержимое указанной директории.
    Args:
        directory (Path): Путь к директории, содержимое которой необходимо удалить.

    Returns:
        None

    Raises:
        Exception: Если происходит ошибка при удалении файла или директории.

    Example:
        >>> from pathlib import Path
        >>> directory_path = Path('../tmp/chat_gpt/test')
        >>> delete_directory_contents(directory_path)
    """
    for item in directory.iterdir(): # Используем iterdir вместо listdir
        if item.is_dir():
            delete_directory_contents(item)
            try:
                item.rmdir()
            except Exception as ex:
                logger.error(f"Ошибка при удалении директории {item}: {ex}", ex, exc_info=True)
        else:
            try:
                item.unlink() # Используем unlink вместо os.remove
            except Exception as ex:
                logger.error(f"Ошибка при удалении файла {item}: {ex}", ex, exc_info=True)


def read_text_files(directory: str, output_file: str) -> None:
    """Читает все указанные текстовые и данные файлы в каталоге и сохраняет объединенный текст в один файл,
    одновременно удаляя файлы и директории, которые начинаются с `_` или содержат `(` и `)`.

    Args:
        directory (str): Каталог для поиска файлов.
        output_file (str): Файл, в который будет сохранен объединенный текст.

    Returns:
        None

    Raises:
        Exception: Если происходит ошибка при обработке файла.

    Example:
        >>> directory_to_search = "src"
        >>> output_file_path = "output.txt"
        >>> read_text_files(directory_to_search, output_file_path)
    """
    output_path = Path(output_file) # Преобразуем в Path
    if not output_path.exists():
        output_path.touch()

    for root, dirs, files in os.walk(directory, topdown=False):
        # Удаление директорий, начинающихся с "_" или содержащих "(" и ")"
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            if dir_name.startswith("_") or ("(" in dir_name and ")" in dir_name):
                delete_directory_contents(dir_path)
                try:
                    dir_path.rmdir()
                except Exception as ex:
                    logger.error(f"Ошибка при удалении директории {dir_path}: {ex}", ex, exc_info=True)

        # Удаление файлов, начинающихся с "_" или содержащих "(" и ")"
        for file_name in files:
            file_path = Path(root) / file_name
            if file_name.startswith("_") or ("(" in file_name and ")" in file_name):
                try:
                    file_path.unlink()
                except Exception as ex:
                    logger.error(f"Ошибка при удалении файла {file_path}: {ex}", ex, exc_info=True)
                continue # Переходим к следующему файлу

            # Чтение и обработка файлов
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
            except Exception as ex:
                logger.error(f"Ошибка при чтении файла {file_path}: {ex}", ex, exc_info=True)
                continue # Переходим к следующему файлу

            file_extension = file_path.suffix.lower()

            try:
                match file_extension:
                    case ".py" | ".txt" | ".css" | ".js" | ".dot" | ".mer" | ".md" | ".ps1" | ".tex" | ".ini" | ".rdf" | ".toml":
                        # Чтение содержимого файла как текст и запись в выходной файл
                        with open(output_path, "a", encoding="utf-8") as output:
                            output.write(file_content + "\n")

                    case ".json":
                        # Чтение содержимого файла как JSON, преобразование в строку с отступами и запись в выходной файл
                        try:
                            json_content = json.loads(file_content)
                            with open(output_path, "a", encoding="utf-8") as output:
                                json.dump(json_content, output, indent=4)
                                output.write("\n")
                        except json.JSONDecodeError as ex:
                            logger.error(f"Ошибка при разборе JSON файла {file_path}: {ex}", ex, exc_info=True)

                    case ".csv":
                        # Чтение содержимого файла как CSV, преобразование в строку и запись в выходной файл
                        try:
                            with open(file_path, 'r', encoding='utf-8') as csvfile:
                                csv_reader = csv.reader(csvfile)
                                csv_string = "\n".join([",".join(row) for row in csv_reader])
                                with open(output_path, "a", encoding="utf-8") as output:
                                    output.write(csv_string + "\n")
                        except Exception as ex:
                            logger.error(f"Ошибка при обработке CSV файла {file_path}: {ex}", ex, exc_info=True)

                    case ".xml":
                        # Чтение содержимого файла как XML, преобразование в строку и запись в выходной файл
                        try:
                            tree = ET.parse(file_path)
                            root_element = tree.getroot()
                            xml_string = ET.tostring(root_element, encoding='utf-8').decode('utf-8')
                            with open(output_path, "a", encoding="utf-8") as output:
                                output.write(xml_string + "\n")
                        except ET.ParseError as ex:
                            logger.error(f"Ошибка при разборе XML файла {file_path}: {ex}", ex, exc_info=True)

                    case ".xls" | ".xlsx":
                        # Чтение содержимого файла как Excel, преобразование каждой таблицы в строку и запись в выходной файл
                        try:
                            excel_data = pd.read_excel(file_path, sheet_name=None)
                            with open(output_path, "a", encoding="utf-8") as output:
                                for sheet_name, df in excel_data.items():
                                    output.write(f"Sheet: {sheet_name}\n")
                                    output.write(df.to_string() + "\n")
                        except Exception as ex:
                            logger.error(f"Ошибка при обработке Excel файла {file_path}: {ex}", ex, exc_info=True)

                    case ".ipynb":
                        # Чтение содержимого файла как Jupyter Notebook, преобразование в строку с отступами и запись в выходной файл
                        try:
                            with open(file_path, 'r', encoding='utf-8') as ipynb_file:
                                notebook_content = json.load(ipynb_file)
                                with open(output_path, "a", encoding="utf-8") as output:
                                    json.dump(notebook_content, output, indent=4)
                                    output.write("\n")
                        except Exception as ex:
                            logger.error(f"Ошибка при обработке Jupyter Notebook файла {file_path}: {ex}", ex, exc_info=True)

                    case ".yaml" | ".yml":
                        # Чтение содержимого файла как YAML, преобразование в строку и запись в выходной файл
                        try:
                            with open(file_path, 'r', encoding='utf-8') as yaml_file:
                                yaml_content = yaml.safe_load(yaml_file)
                                with open(output_path, "a", encoding="utf-8") as output:
                                    yaml.dump(yaml_content, output)
                                    output.write("\n")
                        except Exception as ex:
                            logger.error(f"Ошибка при обработке YAML файла {file_path}: {ex}", ex, exc_info=True)

                    case ".sqlite" | ".db":
                        # Подключение к базе данных SQLite, извлечение имен таблиц и их содержимого, преобразование в строку и запись в выходной файл
                        try:
                            conn = sqlite3.connect(file_path)
                            cursor = conn.cursor()

                            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                            tables = cursor.fetchall()

                            with open(output_path, "a", encoding="utf-8") as output:
                                for table in tables:
                                    table_name = table[0]
                                    output.write(f"Table: {table_name}\n")

                                    cursor.execute(f"SELECT * FROM {table_name};")
                                    table_data = cursor.fetchall()

                                    for row in table_data:
                                        output.write(str(row) + "\n")
                            conn.close()
                        except Exception as ex:
                            logger.error(f"Ошибка при обработке SQLite файла {file_path}: {ex}", ex, exc_info=True)
            except Exception as ex:
                logger.error(f"Произошла общая ошибка при обработке файла {file_path}: {ex}", ex, exc_info=True)