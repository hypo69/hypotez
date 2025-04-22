### **Анализ кода модуля `file_counter.py`**

---

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код выполняет поставленную задачу подсчета строк, классов и функций в файлах.
    - Используется рекурсивный обход директорий для обработки всех файлов.
    - Определены функции для проверки бинарных файлов и подсчета элементов кода.
- **Минусы**:
    - Отсутствует подробная документация модуля и функций.
    - Не используются аннотации типов.
    - Переменная `MODE` объявлена, но не используется.
    - Не используется модуль `logger` для логирования ошибок и информации.
    - Много лишних пустых строк

**Рекомендации по улучшению:**

1. **Добавить заголовок модуля и документацию для всех функций и классов.**
    - Описать назначение модуля, параметры функций, возвращаемые значения и возможные исключения.
2. **Использовать аннотации типов для переменных и параметров функций.**
    - Это улучшит читаемость и облегчит отладку кода.
3. **Удалить неиспользуемую переменную `MODE`.**
    - Или использовать ее по назначению.
4. **Заменить `print` на `logger` для логирования информации и ошибок.**
    - Использовать разные уровни логирования (info, error) в зависимости от ситуации.
5. **Удалить лишние пустые строки в коде.**
    - Это улучшит читаемость кода.
6. **Изменить способ определения корневой директории проекта.**
    - Использовать `__file__` для определения пути к текущему файлу и на его основе вычислять корневую директорию.
7. **Добавить обработку исключений при работе с файлами и директориями.**
    - Это позволит избежать неожиданного завершения программы при возникновении ошибок.
8. **Улучшить проверку на бинарные файлы.**
    - Использовать более надежные методы определения типа файла.
9. **Улучшить стиль кодирования в соответствии с PEP8.**
    - Включить пробелы вокруг операторов, использовать понятные имена переменных и функций.

**Оптимизированный код:**

```python
## \file /dev_utils/file_counter.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для подсчета количества строк, классов и функций в файлах проекта.
=======================================================================

Модуль предоставляет функциональность для рекурсивного подсчета количества строк в текстовых файлах,
а также количества классов и функций в указанной директории и ее поддиректориях.

Пример использования:
----------------------
>>> from pathlib import Path
>>> directory_path = Path('./src')
>>> total_lines, total_classes, total_functions = count_lines_in_files(directory_path)
>>> print(f"Всего строк: {total_lines}, классов: {total_classes}, функций: {total_functions}")
"""

import os
import sys
from pathlib import Path
from typing import Tuple
from src.utils.printer import pprint as print
from src.logger import logger

def count_lines_in_files(directory: Path) -> Tuple[int, int, int]:
    """
    Рекурсивно подсчитывает количество строк в текстовых файлах в указанной директории и ее поддиректориях,
    а также количество классов и функций.

    Args:
        directory (Path): Путь к директории.

    Returns:
        Tuple[int, int, int]: Общее количество строк в текстовых файлах, количество классов и количество функций.
    """
    total_lines: int = 0
    total_classes: int = 0
    total_functions: int = 0

    try:
        for filename in os.listdir(directory):
            filepath: Path = Path(directory, filename)

            if filepath.is_file():
                # Проверяем, является ли файл текстовым, не находится ли он в директории __pycache__, и не является ли файлом Jupyter Notebook
                if not is_binary(filepath) and not filename.endswith('.ipynb') and filename != '__init__.py':
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                            lines_in_file, classes_in_file, functions_in_file = count_lines_classes_functions(file)
                            total_lines += lines_in_file
                            total_classes += classes_in_file
                            total_functions += functions_in_file
                    except Exception as ex:
                        logger.error(f"Ошибка при чтении файла '{filepath}': {ex}", ex, exc_info=True)

            elif filepath.is_dir():
                if not filename.startswith('__pycache__') and not filename.startswith('.'):  # Исключаем директории __pycache__
                    # Если это директория, рекурсивно вызываем функцию для подсчета строк, классов и функций в ней
                    nested_lines, nested_classes, nested_functions = count_lines_in_files(filepath)
                    total_lines += nested_lines
                    total_classes += nested_classes
                    total_functions += nested_functions
    except Exception as ex:
        logger.error(f"Ошибка при обработке директории '{directory}': {ex}", ex, exc_info=True)

    return total_lines, total_classes, total_functions


def is_binary(filepath: Path) -> bool:
    """
    Проверяет, является ли файл бинарным.

    Args:
        filepath (Path): Путь к файлу.

    Returns:
        bool: True, если файл бинарный, иначе False.
    """
    try:
        with open(filepath, 'rb') as file:
            # Читаем первые 512 байт файла для проверки наличия нулевых байтов
            chunk = file.read(512)
            return b'\0' in chunk
    except Exception as ex:
        # Если произошла ошибка при чтении файла, считаем его бинарным
        logger.error(f"Ошибка при чтении файла '{filepath}': {ex}", ex, exc_info=True)
        return True


def count_lines_classes_functions(file) -> Tuple[int, int, int]:
    """
    Подсчитывает количество строк, классов и функций в файле.

    Args:
        file: Файловый объект.

    Returns:
        Tuple[int, int, int]: Количество строк, количество классов и количество функций.
    """
    lines: int = 0
    classes_count: int = 0
    functions_count: int = 0

    for line in file:
        line = line.strip()  # Удаляем начальные и конечные пробелы
        if line:  # Проверяем, не является ли строка пустой
            lines += 1
            if line.startswith('class'):
                classes_count += 1
            elif line.startswith('def'):
                functions_count += 1

    return lines, classes_count, functions_count


if __name__ == "__main__":
    dir_root: Path = Path(os.getcwd()[:os.getcwd().rfind('hypotez') + 7])  # Корневая директория проекта
    dir_src: Path = Path(dir_root, 'src')

    logger.info(f"Подсчет строк, классов и функций в файлах в директории: {dir_src}")
    total_lines, total_classes, total_functions = count_lines_in_files(dir_src)
    print(f"Всего строк в текстовых файлах в '{dir_src}': {total_lines}")
    print(f"Всего классов: {total_classes}")
    print(f"Всего функций: {total_functions}")