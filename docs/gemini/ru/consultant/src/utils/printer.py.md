### **Анализ кода модуля `src.utils.printer`**

#### **Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Модуль предоставляет функции для стилизации текста в консоли, что может быть полезно для улучшения читаемости вывода.
  - Используются ANSI escape-коды для стилизации текста.
  - Присутствует обработка различных типов данных для печати.
- **Минусы**:
  - Отсутствует логирование ошибок.
  - Не все переменные аннотированы типами.
  - В docstring присутсвует английский язык, необходимо перевести на русский
  - Не хватает обработки исключений с использованием `logger.error`.
  - Используются двойные кавычки.
  - Не указаны типы для констант, таких как `RESET`, `TEXT_COLORS`, `BG_COLORS` и `FONT_STYLES`.

#### **Рекомендации по улучшению**:
- Добавить аннотации типов для всех переменных и констант.
- Использовать одинарные кавычки для строк.
- Добавить логирование ошибок с использованием `logger.error`.
- Перевести docstring на русский язык.
- Добавить docstring к модулю в формате, указанном в инструкции.
- Изменить обработку исключений, чтобы использовать `logger.error`.
- Добавить обработку файлов с расширениями `.csv` и `.xls` с использованием `pandas`.

#### **Оптимизированный код**:

```python
## \file /src/utils/printer.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с утилитами печати и стилизации текста
========================================================

Модуль содержит функции для печати данных в удобочитаемом формате с возможностью стилизации текста,
включая цвет, фон и стили шрифта.
"""

import json
import csv
import pandas as pd
from pathlib import Path
from typing import Any, Dict, Optional

from src.logger import logger  # Добавлен импорт logger

# ANSI escape codes
RESET: str = '\033[0m'

TEXT_COLORS: Dict[str, str] = {
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
BG_COLORS: Dict[str, str] = {
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

FONT_STYLES: Dict[str, str] = {
    'bold': '\033[1m',
    'underline': '\033[4m',
}

def _color_text(text: str, text_color: str = '', bg_color: str = '', font_style: str = '') -> str:
    """Применяет цвет, фон и стиль шрифта к тексту.

    Эта вспомогательная функция применяет указанные стили цвета и шрифта к заданному тексту, используя ANSI escape-коды.

    Args:
        text (str): Текст для стилизации.
        text_color (str, optional): Цвет текста. По умолчанию пустая строка, что означает отсутствие цвета.
        bg_color (str, optional): Цвет фона. По умолчанию пустая строка, что означает отсутствие цвета фона.
        font_style (str, optional): Стиль шрифта. По умолчанию пустая строка, что означает отсутствие стиля шрифта.

    Returns:
        str: Стилизованный текст в виде строки.

    Example:
        >>> _color_text('Hello, World!', text_color='green', font_style='bold')
        '\\033[1m\\033[32mHello, World!\\033[0m'
    """
    return f'{font_style}{text_color}{bg_color}{text}{RESET}'

def pprint(print_data: Any = None, text_color: str = 'white', bg_color: str = '', font_style: str = '') -> None:
    """Печатает данные с применением стилизации.

    Функция форматирует входные данные в зависимости от их типа и выводит их в консоль.
    Данные выводятся с применением указанного цвета текста, цвета фона и стиля шрифта.
    Функция обрабатывает словари, списки, строки и пути к файлам.

    Args:
        print_data (Any, optional): Данные для печати. Может быть типа None, dict, list, str или Path.
        text_color (str, optional): Цвет текста. По умолчанию 'white'. См. TEXT_COLORS.
        bg_color (str, optional): Цвет фона. По умолчанию '' (нет фона). См. BG_COLORS.
        font_style (str, optional): Стиль шрифта. По умолчанию '' (нет стиля). См. FONT_STYLES.

    Returns:
        None

    Raises:
        Exception: Если тип данных не поддерживается или возникает ошибка во время печати.

    Example:
        >>> pprint({'name': 'Alice', 'age': 30}, text_color='green')
        \\033[32m{
            'name': 'Alice',
            'age': 30
        }\\033[0m

        >>> pprint(['apple', 'banana', 'cherry'], text_color='blue', font_style='bold')
        \\033[34m\\033[1mapple\\033[0m
        \\033[34m\\033[1mbanana\\033[0m
        \\033[34m\\033[1mcherry\\033[0m

        >>> pprint('text example', text_color='yellow', bg_color='bg_red', font_style='underline')
        \\033[4m\\033[33m\\033[41mtext example\\033[0m
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
        elif isinstance(print_data, (str, Path)):  # Объединяем проверку типов
            file_path = Path(print_data)
            if file_path.is_file():
                ext = file_path.suffix.lower()
                if ext in ['.csv', '.xls', '.xlsx']:  # Поддержка .xlsx
                    try:
                        if ext == '.csv':
                            df = pd.read_csv(file_path)
                        else:  # .xls или .xlsx
                            df = pd.read_excel(file_path)
                        print(_color_text(df.to_string(), text_color))  # Вывод DataFrame
                    except Exception as ex:
                        logger.error(f'Error reading file {file_path}', ex, exc_info=True)  # Логирование ошибки
                        print(_color_text(f'Error reading file: {ex}', text_color=TEXT_COLORS['red']))
                else:
                    print(_color_text('Unsupported file type.', text_color))
            else:
                print(_color_text(str(print_data), text_color))
        else:
            print(_color_text(str(print_data), text_color))
    except Exception as ex:
        logger.error('Error while processing data', ex, exc_info=True) # Логирование ошибки
        print(_color_text(f'Error: {ex}', text_color=TEXT_COLORS['red']))

if __name__ == '__main__':
    pprint({'name': 'Alice', 'age': 30}, text_color='green')