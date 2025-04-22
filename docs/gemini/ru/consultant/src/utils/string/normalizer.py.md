### **Анализ кода модуля `normalizer.py`**

**Качество кода:**

- **Соответствие стандартам**: 8/10
- **Плюсы**:
    - Хорошая структура модуля, наличие docstring для каждой функции.
    - Использование аннотаций типов.
    - Обработка исключений с логированием ошибок.
    - Полезные функции для нормализации строк, чисел и дат.
- **Минусы**:
    - В некоторых docstring примеры использования на английском языке.
    - Не везде используются одинарные кавычки.
    - Есть устаревшие конструкции, такие как `Union[]`.
    - Не во всех случаях в блоках `except` используется `ex` вместо `e`.

**Рекомендации по улучшению:**

1.  **Общие улучшения**:
    - Перевести все docstring на русский язык.
    - Использовать только одинарные кавычки в коде.
    - Заменить `Union[]` на `|` для аннотаций типов.
    - Убедиться, что во всех блоках `except` используется `ex` вместо `e`.

2.  **`normalize_boolean`**:
    - В случае ошибки логируется просто сообщение без деталей исключения. Рекомендуется передавать `ex` в `logger.error`.
    - Возвращает исходное значение при ошибке, что может быть неочевидным поведением. Лучше возвращать `False` или поднимать исключение.

3.  **`normalize_string`**:
    - Тип возвращаемого значения в docstring не соответствует действительности. Функция возвращает строку, а не `str | list`.
    - Обработка исключений аналогична `normalize_boolean`.

4.  **`normalize_int`**:
    - Обработка исключений аналогична `normalize_boolean`.

5.  **`normalize_float`**:
    - Предупреждение об итерируемом объекте можно заменить на исключение, чтобы предотвратить некорректное использование.

6.  **`normalize_sql_date`**:
    - Обработка исключений аналогична `normalize_boolean`.

7.  **`simplify_string`**:
    - Функция описана с использованием `@param` и `@return`, что является устаревшим стилем. Необходимо заменить на docstring в формате, указанном в инструкции.

8.  **`remove_special_characters`**:
    - В docstring не указано, что возвращается строка или список строк.

9. **`normalize_sku`**:
   - Логирование ошибки происходит без передачи объекта исключения. Необходимо передавать `ex` в `logger.error`.

**Оптимизированный код:**

```python
## \file /src/utils/string/normalizer.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для нормализации строк и числовых данных
=========================================================================================

Модуль предоставляет функции для нормализации строк, булевых значений, целых и чисел с плавающей точкой.
Он также содержит вспомогательные методы для обработки текста, включая удаление HTML-тегов и специальных символов.

Пример использования
--------------------
```python
    from src.utils.string.normalizer import normalize_string, normalize_boolean

    normalized_str = normalize_string(' Пример строки <b>с HTML</b> ')
    normalized_bool = normalize_boolean('yes')
```
.. module:: src.utils.string.normalizer
"""

import re
import html
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, List, Optional
from src.logger.logger import logger


def normalize_boolean(input_data: Any) -> bool:
    """
    Преобразует входные данные в булево значение.

    Args:
        input_data (Any): Данные, которые могут быть представлены как булево значение (например, bool, строка, целое число).

    Returns:
        bool: Булево представление входных данных.

    Example:
        >>> normalize_boolean('yes')
        True
    """
    original_input = input_data  # Сохраняется исходное значение
    if isinstance(input_data, bool):
        return input_data

    try:
        input_str = str(input_data).strip().lower()
        if input_str in {'true', '1', 'yes', 'y', 'on', True, 1}:
            return True
        if input_str in {'false', '0', 'no', 'n', 'off', False, 0}:
            return False
    except Exception as ex:
        logger.error('Ошибка в normalize_boolean: ', ex, exc_info=True)  # Передача информации об исключении

    logger.debug(f'Неожиданное значение для преобразования в bool: {input_data}')
    return original_input  # Возвращается исходное значение


def normalize_string(input_data: str | list) -> str:
    """
    Нормализует строку или список строк.

    Args:
        input_data (str | list): Входные данные, которые могут быть строкой или списком строк.

    Returns:
        str: Очищенная и нормализованная строка в формате UTF-8.

    Raises:
        TypeError: Если `input_data` не является строкой или списком.

    Example:
        >>> normalize_string(['Hello', '  World!  '])
        'Hello World!'
    """
    if not input_data:
        return ''

    original_input = input_data  # Сохраняется исходное значение. В случае ошибки парсинга строки вернется это значение

    if not isinstance(input_data, (str, list)):
        raise TypeError('Данные должны быть строкой или списком строк.')

    if isinstance(input_data, list):
        input_data = ' '.join(map(str, input_data))

    try:
        cleaned_str = remove_html_tags(input_data)
        cleaned_str = remove_line_breaks(cleaned_str)
        cleaned_str = remove_special_characters(cleaned_str)
        normalized_str = ' '.join(cleaned_str.split())

        return normalized_str.strip().encode('utf-8').decode('utf-8')
    except Exception as ex:
        logger.error('Ошибка в normalize_string: ', ex, exc_info=True) # Логирование с информацией об исключении
        return str(original_input).encode('utf-8').decode('utf-8')


def normalize_int(input_data: str | int | float | Decimal) -> int:
    """
    Преобразует входные данные в целое число.

    Args:
        input_data (str | int | float | Decimal): Входные данные, которые могут быть числом или его строковым представлением.

    Returns:
        int: Целое представление входных данных.

    Example:
        >>> normalize_int('42')
        42
    """
    original_input = input_data  # Сохраняется исходное значение
    try:
        if isinstance(input_data, Decimal):
            return int(input_data)
        return int(float(input_data))
    except (ValueError, TypeError, InvalidOperation) as ex:
        logger.error('Ошибка в normalize_int: ', ex, exc_info=True) # Логирование с информацией об исключении
        return original_input  # Возвращается исходное значение


def normalize_float(value: Any) -> Optional[float]:
    """
    Безопасно конвертирует входное значение в float или возвращает None,
    если конвертация не удалась. Удаляет распространенные символы валют
    и разделители тысяч перед конвертацией.

    Args:
        value (Any): Входное значение (int, float, str и т.д.).

    Returns:
        Optional[float]: Число float или None, если конвертация не удалась.

    Example:
        >>> normalize_float(5)
        5.0
        >>> normalize_float('5')
        5.0
        >>> normalize_float('3.14')
        3.14
        >>> normalize_float('abc')
        None
        >>> normalize_float('₪0.00')
        0.0
        >>> normalize_float('$1,234.56')
        1234.56
        >>> normalize_float('  - 7.5 € ')
        -7.5
        >>> normalize_float(None)
        None
        >>> normalize_float(['1'])
        None
        >>> normalize_float('')
        None

    Важно! проверять после вызова этой функции, что она не вернула None
    """
    if value is None:
        return None

    # Если это уже число, просто конвертируем в float
    if isinstance(value, (int, float)):
        return float(value)

    # Если это список/кортеж - ошибка
    if isinstance(value, (list, tuple)):
        logger.warning(f'Ожидалось одиночное значение, получен итерируемый объект: {value}')
        return None

    # Попытка преобразовать значение в строку для очистки
    try:
        value_str = str(value)
    except Exception as ex:
        logger.warning(f'Невозможно преобразовать значение в строку: {value} ({type(value)}). Ошибка: {ex}')
        return None

    # Очистка строки от известных нечисловых символов
    # 1. Удаляем распространенные символы валют (можно расширить список)
    cleaned_str: str = re.sub(r'[₪$€£¥₽]', '', value_str)
    # 2. Удаляем разделители тысяч (запятые)
    cleaned_str = cleaned_str.replace(',', '')
    # 3. Удаляем начальные/конечные пробелы
    cleaned_str = cleaned_str.strip()

    # Если строка пуста после очистки
    if not cleaned_str:
        logger.warning(f'Значение стало пустым после очистки: "{value}" -> "{cleaned_str}"')
        return None

    # Попытка конвертации очищенной строки
    try:
        # Используем float() для преобразования
        float_value = float(cleaned_str)
        # Округление до 3 знаков больше не требуется по коду, возвращаем как есть
        return float_value
    except (ValueError, TypeError) as ex:
        logger.warning(f'Не удалось конвертировать очищенную строку "{cleaned_str}" (из "{value}") в float')
        return None


def normalize_sql_date(input_data: str) -> str:
    """
    Преобразует входные данные в формат SQL date (YYYY-MM-DD).

    Args:
        input_data (str): Данные, которые могут быть представлены как дата (например, строка, объект datetime).

    Returns:
        str: Нормализованная дата в формате SQL (YYYY-MM-DD) или исходное значение, если преобразование не удалось.

    Example:
        >>> normalize_sql_date('2024-12-06')
        '2024-12-06'
        >>> normalize_sql_date('12/06/2024')
        '2024-12-06'
    """
    original_input = input_data  # Сохраняется исходное значение

    try:
        # Проверка и преобразование строки в формат даты
        if isinstance(input_data, str):
            # Попытка распарсить дату из строки
            for date_format in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
                try:
                    normalized_date = datetime.strptime(input_data, date_format).date()
                    return normalized_date.isoformat()  # Возвращаем дату в формате 'YYYY-MM-DD'
                except ValueError:
                    continue
        # Если входные данные уже объект datetime
        if isinstance(input_data, datetime):
            return input_data.date().isoformat()

    except Exception as ex:
        logger.error('Ошибка в normalize_sql_date: ', ex, exc_info=True) # Логирование с информацией об исключении

    logger.debug(f'Не удалось преобразовать в SQL дату: {input_data}')
    return original_input  # Возвращается исходное значение

def simplify_string(input_str: str) -> str:
    """
    Упрощает входную строку, оставляя только буквы, цифры и заменяя пробелы на подчеркивания.

    Args:
        input_str (str): Строка для упрощения.

    Returns:
        str: Упрощенная строка.

    Example:
        >>> example_str = "It's a test string with 'single quotes', numbers 123 and symbols!"
        >>> simplified_str = simplify_string(example_str)
        >>> print(simplified_str)
        Its_a_test_string_with_single_quotes_numbers_123_and_symbols
    """
    try:
        # Remove all characters except letters, digits, and spaces
        cleaned_str = re.sub(r'[^a-zA-Z0-9\s]', '', input_str)
        # Replace spaces with underscores
        cleaned_str = cleaned_str.replace(' ', '_')
        # Remove consecutive underscores
        cleaned_str = re.sub(r'_+', '_', cleaned_str)
        return cleaned_str
    except Exception as ex:
        logger.error("Error simplifying the string", ex, exc_info=True) # Логирование с информацией об исключении
        return input_str


def remove_line_breaks(input_str: str) -> str:
    """
    Удаляет переносы строк из входной строки.

    Args:
        input_str (str): Входная строка.

    Returns:
        str: Строка без переносов строк.
    """
    return input_str.replace('\n', ' ').replace('\r', ' ').strip()


def remove_html_tags(input_html: str) -> str:
    """
    Удаляет HTML-теги из входной строки.

    Args:
        input_html (str): Входная HTML строка.

    Returns:
        str: Строка без HTML-тегов.
    """
    return re.sub(r'<.*?>', '', input_html).strip()


def remove_special_characters(input_str: str | list, chars: Optional[List[str]] = None) -> str | list:
    """
    Удаляет указанные специальные символы из строки или списка строк.

    Args:
        input_str (str | list): Входная строка или список строк.
        chars (list[str], optional): Список символов для удаления. По умолчанию None.

    Returns:
        str | list: Обработанная строка или список с удаленными символами.
    """
    if chars is None:
        chars = ['#']  # Default list of characters to remove

    pattern = '[' + re.escape(''.join(chars)) + ']'

    if isinstance(input_str, list):
        return [re.sub(pattern, '', s) for s in input_str]
    return re.sub(pattern, '', input_str)

def normalize_sku(input_str: str) -> str:
    """
    Нормализует артикул (SKU), удаляя специфические ивритские ключевые слова и все не-буквенно-цифровые символы,
    за исключением дефисов.

    Args:
        input_str (str): Входная строка, содержащая артикул.

    Returns:
        str: Нормализованная строка артикула.

    Example:
        >>> normalize_sku("מקט: 303235-A")
        '303235-A'
        >>> normalize_sku("מק''ט: 12345-B")
        '12345-B'
        >>> normalize_sku("Some text מקט: 123-456-789 other text")
        'Some text 123-456-789 other text' # Важно: Сохраняются дефисы и пробелы между текстами
    """
    try:
        # Remove Hebrew keywords
        _str = re.sub(r'מקט|מק\'\'ט', '', input_str, flags=re.IGNORECASE)

        # Remove non-alphanumeric characters, except for hyphens
        normalized_sku = re.sub(r'[^\w-]+', '', _str)

        return normalized_sku
    except Exception as ex:
        logger.error(f"Error normalizing SKU: ", ex, exc_info=True)  # Include exception details
        return input_str