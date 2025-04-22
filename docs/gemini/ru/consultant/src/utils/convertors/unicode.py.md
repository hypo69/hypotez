### **Анализ кода модуля `unicode.py`**

## \file hypotez/src/utils/convertors/unicode.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для декодирования unicode-строк
======================================

Модуль предоставляет функцию `decode_unicode_escape`, которая позволяет
декодировать строки, содержащие unicode escape-последовательности, в читаемый вид.
Функция поддерживает обработку словарей, списков и строк, проводя рекурсивную
обработку для сложных структур данных.

Пример использования:

>>> input_dict = {'product_name': r'\\u05de\\u05e7\\"\\u05d8 \\u05d9\\u05e6\\u05e8\\u05df\\nH510M K V2'}
>>> decoded_dict = decode_unicode_escape(input_dict)
>>> print(decoded_dict)
{'product_name': 'מקט\\"יצרן\\nH510M K V2'}

.. module:: src.utils.convertors.unicode
"""

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код выполняет поставленную задачу - декодирование unicode escape-последовательностей.
  - Поддержка различных типов данных (словарь, список, строка).
  - Наличие обработки исключений `UnicodeDecodeError`.
  - Примеры использования в docstring.
- **Минусы**:
  - Отсутствуют аннотации типов для переменных внутри функции.
  - Docstring на английском языке.
  - Не используется модуль `logger` для логирования ошибок.
  - Нет обработки ситуаций, когда `input_data` имеет тип, отличный от `dict`, `list` или `str`.

#### **Рекомендации по улучшению**:
- Добавить аннотации типов для переменных внутри функции, чтобы улучшить читаемость и предотвратить ошибки.
- Перевести docstring на русский язык.
- Использовать модуль `logger` для логирования ошибок вместо `print`.
- Явно обрабатывать случай, когда `input_data` имеет неподдерживаемый тип, и логировать это событие.
- Изменить название переменной `e` на `ex` в блоке `except`.
- Использовать одинарные кавычки (`'`) вместо двойных (`"`) в Python-коде.

#### **Оптимизированный код**:
```python
import re
from typing import Dict, Any

from src.logger import logger


def decode_unicode_escape(input_data: Dict[str, Any] | list | str) -> Dict[str, Any] | list | str:
    """
    Декодирует значения в словаре, списке или строке, содержащие юникодные escape-последовательности, в читаемый текст.

    Args:
        input_data (Dict[str, Any] | list | str): Входные данные - словарь, список или строка,
                                                  которые могут содержать юникодные escape-последовательности.

    Returns:
        Dict[str, Any] | list | str: Преобразованные данные. В случае строки применяется декодирование escape-последовательностей.
                                     В случае словаря или списка рекурсивно обрабатываются все значения.

    Raises:
        TypeError: Если тип входных данных не поддерживается (не словарь, не список и не строка).

    Example:
        >>> input_dict = {
        ...     'product_name': r'\\u05de\\u05e7\\"\\u05d8 \\u05d9\\u05e6\\u05e8\\u05df\\nH510M K V2',
        ...     'category': r'\\u05e2\\u05e8\\u05db\\u05ea \\u05e9\\u05d1\\u05d1\\u05d9\\u05dd',
        ...     'price': 123.45
        ... }
        >>> decoded_dict = decode_unicode_escape(input_dict)
        >>> print(decoded_dict)
        {'product_name': 'מקט\\"יצרן\\nH510M K V2', 'category': 'ערכת שבבים', 'price': 123.45}

        >>> input_list = [r'\\u05e2\\u05e8\\u05db\\u05ea \\u05e9\\u05d1\\u05d1\\u05d9\\u05dd', r'H510M K V2']
        >>> decoded_list = decode_unicode_escape(input_list)
        >>> print(decoded_list)
        ['ערכת שבבים', 'H510M K V2']

        >>> input_string = r'\\u05de\\u05e7\\"\\u05d8 \\u05d9\\u05e6\\u05e8\\u05df\\nH510M K V2'
        >>> decoded_string = decode_unicode_escape(input_string)
        >>> print(decoded_string)
        מקט\\"יצרן\\nH510M K V2
    """
    if isinstance(input_data, dict):
        # Рекурсивная обработка значений словаря
        decoded_data: Dict[str, Any] = {key: decode_unicode_escape(value) for key, value in input_data.items()}
        return decoded_data

    elif isinstance(input_data, list):
        # Рекурсивная обработка элементов списка
        decoded_data: list = [decode_unicode_escape(item) for item in input_data]
        return decoded_data

    elif isinstance(input_data, str):
        # Функция декодирует строку, если она содержит escape-последовательности
        try:
            # Шаг 1: Декодирование строки с escape-последовательностями
            decoded_string: str = input_data.encode('utf-8').decode('unicode_escape')
        except UnicodeDecodeError as ex:
            logger.error('Ошибка при декодировании unicode escape последовательности', ex, exc_info=True)
            decoded_string: str = input_data

        # Шаг 2: Преобразование всех найденных последовательностей \\uXXXX
        unicode_escape_pattern: str = r'\\\\u[0-9a-fA-F]{4}'
        decoded_string: str = re.sub(unicode_escape_pattern, lambda match: match.group(0).encode('utf-8').decode('unicode_escape'), decoded_string)

        return decoded_string

    else:
        # Если тип данных не поддерживается, функция логирует ошибку и возвращает данные без изменений
        logger.error(f'Неподдерживаемый тип данных: {type(input_data)}')
        return input_data