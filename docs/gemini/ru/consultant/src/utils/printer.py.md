### **Анализ кода модуля `src.utils.printer`**

## \file /src/utils/printer.py

Модуль предоставляет утилиты для форматированного вывода текста в консоль, включая стилизацию текста с использованием цветов, фона и шрифтов.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая организация кода, разделение на функции и константы.
    - Использование ANSI escape codes для стилизации текста.
    - Обработка различных типов данных для печати (словари, списки, строки, файлы).
- **Минусы**:
    - Отсутствуют аннотации типов для переменных, что снижает читаемость и поддерживаемость кода.
    - Не используется модуль `logger` для логирования ошибок.
    - Docstring на английском языке, что противоречит требованиям.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех переменных и параметров функций.

2.  **Использовать модуль `logger`**:
    - Заменить `print` на `logger.error` при выводе сообщений об ошибках, чтобы обеспечить централизованное логирование.

3.  **Перевести docstring на русский язык**:
    - Перевести все docstring на русский язык, чтобы соответствовать требованиям.

4.  **Улучшить обработку ошибок**:
    - Использовать более конкретные исключения и предоставлять более информативные сообщения об ошибках.

5.  **Использовать одинарные кавычки**:
    - Заменить двойные кавычки на одинарные.

**Оптимизированный код:**

```python
                ## \file /src/utils/printer.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с форматированным выводом в консоль
====================================================

Модуль содержит утилиты для форматированного вывода текста в консоль,
включая стилизацию текста с использованием цветов, фона и шрифтов.
"""

import json
import csv
import pandas as pd
from pathlib import Path
from typing import Any, Optional
from pprint import pprint as pretty_print
from src.logger import logger  # Import logger module

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
    Применяет стилизацию к тексту, используя ANSI escape codes.

    Args:
        text (str): Текст для стилизации.
        text_color (str, optional): Цвет текста. По умолчанию ''.
        bg_color (str, optional): Цвет фона. По умолчанию ''.
        font_style (str, optional): Стиль шрифта. По умолчанию ''.

    Returns:
        str: Стилизованный текст.
    
    Example:
        >>> _color_text('Hello, World!', text_color='green', font_style='bold')
        '\\033[1m\\033[32mHello, World!\\033[0m'
    """
    return f'{font_style}{text_color}{bg_color}{text}{RESET}'

def pprint(print_data: Any = None, text_color: str = 'white', bg_color: str = '', font_style: str = '') -> None:
    """
    Выводит данные в консоль с применением стилизации.

    Args:
        print_data (Any, optional): Данные для вывода. По умолчанию None.
        text_color (str, optional): Цвет текста. По умолчанию 'white'.
        bg_color (str, optional): Цвет фона. По умолчанию ''.
        font_style (str, optional): Стиль шрифта. По умолчанию ''.

    Returns:
        None

    Raises:
        TypeError: Если тип данных не поддерживается.
        Exception: Если возникает ошибка при выводе данных.
    
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
        text_color = TEXT_COLORS.get(text_color.lower(), TEXT_COLORS['white'])
    if isinstance(bg_color, str):
        bg_color = BG_COLORS.get(bg_color.lower(), '')
    if isinstance(font_style, str):
        font_style = FONT_STYLES.get(font_style.lower(), '')

    try:
        if isinstance(print_data, dict):
            print(_color_text(json.dumps(print_data, indent=4), text_color))
        elif isinstance(print_data, list):
            for item in print_data:
                print(_color_text(str(item), text_color))
        elif isinstance(print_data, (str, Path)) and Path(print_data).is_file():
            ext = Path(print_data).suffix.lower()
            if ext in ['.csv', '.xls']:
                print(_color_text('File reading supported for .csv, .xls only.', text_color))
            else:
                print(_color_text('Unsupported file type.', text_color))
        else:
            print(_color_text(str(print_data), text_color))
    except Exception as ex:
        logger.error('Error while printing data', ex, exc_info=True)  # Use logger for error logging

if __name__ == '__main__':
    pprint({'name': 'Alice', 'age': 30}, text_color='green')