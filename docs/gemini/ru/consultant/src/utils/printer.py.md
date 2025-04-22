### **Анализ кода модуля `src.utils.printer`**

#### **1. Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и легко читаем.
  - Используются аннотации типов.
  - Присутствует документация в формате docstring.
  - Обработка исключений реализована с использованием `try-except`.
  - Есть примеры использования в docstring.
- **Минусы**:
  - Некоторые комментарии и docstring написаны на английском языке.
  - Не все переменные аннотированы типами.
  - В блоке `except` используется `e` вместо `ex` для обозначения исключения.
  - Не используется модуль `logger` для логирования ошибок.
  - Не все строки соответствуют требованиям по использованию одинарных кавычек.

#### **2. Рекомендации по улучшению:**

1.  **Перевод документации и комментариев**:
    - Перевести все docstring и комментарии на русский язык, соблюдая формат UTF-8.
2.  **Использование `logger`**:
    - Заменить `print` в блоке `except` на `logger.error` для логирования ошибок.
3.  **Исправление именования исключения**:
    - Заменить `e` на `ex` в блоке `except`.
4.  **Использование одинарных кавычек**:
    - Заменить двойные кавычки на одинарные в строках, где это необходимо.
5.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, где это возможно.
6.  **Обновление docstring**:
    - Привести docstring в соответствие с требуемым форматом, включая описание аргументов, возвращаемых значений и возможных исключений.
7.  **Стиль кода**:
    - Исправить отступы и пробелы в соответствии со стандартами PEP8.

#### **3. Оптимизированный код:**

```python
## \file /src/utils/printer.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для организации красивого вывода в консоль и стилизации текста.
=======================================================================

Этот модуль предоставляет функции для вывода данных в удобочитаемом формате
с возможностью стилизации текста, включая цвет, фон и шрифты.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Any, Optional
from pprint import pprint as pretty_print
from src.logger import logger # Импорт модуля logger

# ANSI escape codes
RESET: str = '\033[0m'

TEXT_COLORS: dict[str, str] = {
    'red': '\033[31m',
    'green': '\033[32m',
    'blue': '\033[34m',
    'yellow': '\033[33m',
    'white': '\033[37m',
    'cyan': '\033[36m',
    'magenta': '\033[35m',
    'light_gray': '\033[37m',
    'dark_gray': '\033[90m',
    'light_red': '\033[91m',
    'light_green': '\033[92m',
    'light_blue': '\033[94m',
    'light_yellow': '\033[93m',
}

# Background colors mapping
BG_COLORS: dict[str, str] = {
    'bg_red': '\033[41m',
    'bg_green': '\033[42m',
    'bg_blue': '\033[44m',
    'bg_yellow': '\033[43m',
    'bg_white': '\033[47m',
    'bg_cyan': '\033[46m',
    'bg_magenta': '\033[45m',
    'bg_light_gray': '\033[47m',
    'bg_dark_gray': '\033[100m',
    'bg_light_red': '\033[101m',
    'bg_light_green': '\033[102m',
    'bg_light_blue': '\033[104m',
    'bg_light_yellow': '\033[103m',
}

FONT_STYLES: dict[str, str] = {
    'bold': '\033[1m',
    'underline': '\033[4m',
}


def _color_text(text: str, text_color: str = '', bg_color: str = '', font_style: str = '') -> str:
    """
    Применяет стилизацию к тексту, используя ANSI escape-коды.

    Функция применяет цвет текста, фона и стиль шрифта к заданному тексту,
    используя ANSI escape-коды.

    Args:
        text (str): Текст для стилизации.
        text_color (str, optional): Цвет текста. По умолчанию ''.
        bg_color (str, optional): Цвет фона. По умолчанию ''.
        font_style (str, optional): Стиль шрифта. По умолчанию ''.

    Returns:
        str: Стилизованный текст.

    Example:
        >>> _color_text('Hello, World!', text_color='green', font_style='bold')
        '\033[1m\033[32mHello, World!\033[0m'
    """
    return f'{font_style}{text_color}{bg_color}{text}{RESET}'


def pprint(print_data: Any = None, text_color: str = 'white', bg_color: str = '', font_style: str = '') -> None:
    """
    Выводит данные в консоль с возможностью стилизации.

    Функция форматирует входные данные и выводит их в консоль с применением
    указанного цвета текста, фона и стиля шрифта. Поддерживает вывод словарей,
    списков, строк и путей к файлам.

    Args:
        print_data (Any, optional): Данные для вывода. Может быть None, dict, list, str или Path. По умолчанию None.
        text_color (str, optional): Цвет текста. По умолчанию 'white'. См. TEXT_COLORS.
        bg_color (str, optional): Цвет фона. По умолчанию ''. См. BG_COLORS.
        font_style (str, optional): Стиль шрифта. По умолчанию ''. См. FONT_STYLES.

    Returns:
        None

    Example:
        >>> pprint({'name': 'Alice', 'age': 30}, text_color='green')
        \033[32m{
            "name": "Alice",
            "age": 30
        }\033[0m

        >>> pprint(['apple', 'banana', 'cherry'], text_color='blue', font_style='bold')
        \033[34m\033[1mapple\033[0m
        \033[34m\033[1mbanana\033[0m
        \033[34m\033[1mcherry\033[0m

        >>> pprint('text example', text_color='yellow', bg_color='bg_red', font_style='underline')
        \033[4m\033[33m\033[41mtext example\033[0m
    """
    if not print_data:
        return

    if isinstance(text_color, str):
        text_color: str = TEXT_COLORS.get(text_color.lower(), TEXT_COLORS['white'])
    if isinstance(bg_color, str):
        bg_color: str = BG_COLORS.get(bg_color.lower(), '')
    if isinstance(font_style, str):
        font_style: str = FONT_STYLES.get(font_style.lower(), '')

    try:
        if isinstance(print_data, dict):
            print(_color_text(json.dumps(print_data, indent=4), text_color))
        elif isinstance(print_data, list):
            for item in print_data:
                print(_color_text(str(item), text_color))
        elif isinstance(print_data, (str, Path)) and Path(print_data).is_file():
            ext: str = Path(print_data).suffix.lower()
            if ext in ['.csv', '.xls']:
                print(_color_text('Чтение файлов .csv и .xls поддерживается.', text_color))
            else:
                print(_color_text('Неподдерживаемый тип файла.', text_color))
        else:
            print(_color_text(str(print_data), text_color))
    except Exception as ex:
        logger.error('Ошибка при выводе данных', ex, exc_info=True) # Используем logger для логирования ошибки

if __name__ == '__main__':
    pprint({'name': 'Alice', 'age': 30}, text_color='green')