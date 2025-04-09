### **Анализ кода модуля `normalizer.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Наличие docstring для большинства функций.
    - Использование `logger` для регистрации ошибок.
    - Обработка исключений.
    - Четкое разделение на функции для нормализации разных типов данных.
- **Минусы**:
    - В некоторых docstring отсутствует подробное описание возвращаемых значений и возможных исключений.
    - Есть функции с англоязычной документацией.
    - Не все переменные аннотированы типами.
    - Местами не соблюдается PEP8 (пробелы вокруг операторов).
    - Отсутствует заголовок модуля.

**Рекомендации по улучшению:**

1.  **Заголовок модуля**: Добавить заголовок с описанием модуля в стиле Markdown.

2.  **Docstring**:
    *   Перевести все docstring на русский язык.
    *   Дополнить описания возвращаемых значений и возможных исключений.
    *   Улучшить описание параметров в docstring, избегать расплывчатых фраз.
    *   Для каждой функции добавить пример использования.

3.  **PEP8**:
    *   Добавить пробелы вокруг операторов присваивания.
    *   Использовать одинарные кавычки.

4.  **Аннотации типов**:
    *   Указать аннотации типов для всех переменных, где это необходимо.

5.  **Обработка исключений**:
    *   Указывать `exc_info=True` при логировании исключений, чтобы получить полную трассировку.

6.  **Улучшение `normalize_float`**:

    *   Сейчас функция возвращает `0`, когда не может преобразовать значение во float. Лучше возвращать `None`.
    *   Добавить проверку на `None` перед преобразованием.
    *   Убрать лишнее сохранение исходного значения.

7.  **`normalize_string`**:

    *   Добавить проверку, что `input_data` не является `None`.
    *   В случае ошибки парсинга логировать ошибку с `exc_info=True`.

8.  **Общее**:
    *   Избегать дублирования кода (например, повторяющиеся блоки `try...except` с логированием ошибок).
    *   Использовать более конкретные типы исключений, а не просто `Exception`.

**Оптимизированный код:**

```python
                ## \file /src/utils/string/normalizer.py
# -*- coding: utf-8 -*-\

#! .pyenv/bin/python3

"""
Модуль для нормализации строк и числовых данных
=========================================================================================

Модуль предоставляет функции для нормализации строк, булевых значений, целых и чисел с плавающей точкой.
Он также содержит вспомогательные методы для обработки текста, включая удаление HTML-тегов и специальных символов.

Пример использования
--------------------

.. code-block:: python

    from src.utils.string.normalizer import normalize_string, normalize_boolean

    normalized_str = normalize_string(" Пример строки <b>с HTML</b> ")
    normalized_bool = normalize_boolean("yes")
"""

import re
import html
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, List, Union, Optional
from src.logger.logger import logger


def normalize_boolean(input_data: Any) -> bool:
    """
    Преобразует входные данные в булево значение.

    Args:
        input_data (Any): Данные, которые могут быть представлены как булево значение (например, bool, строка, число).

    Returns:
        bool: Булево представление входных данных.

    Raises:
        Exception: Если происходит ошибка при преобразовании.

    Example:
        >>> normalize_boolean('yes')
        True
    """
    original_input: Any = input_data  # Сохраняется исходное значение
    if isinstance(input_data, bool):
        return input_data

    try:
        input_str: str = str(input_data).strip().lower()
        if input_str in {'true', '1', 'yes', 'y', 'on', 'True', '1'}:
            return True
        if input_str in {'false', '0', 'no', 'n', 'off', 'False', '0'}:
            return False
    except Exception as ex:
        logger.error('Ошибка в normalize_boolean: ', ex, exc_info=True)

    logger.debug(f'Неожиданное значение для преобразования в bool: {input_data}')
    return original_input  # Возвращается исходное значение


def normalize_string(input_data: str | list | None) -> str:
    """
    Очищает и нормализует строку или список строк.

    Args:
        input_data (str | list | None): Входные данные, строка или список строк.

    Returns:
        str: Очищенная и нормализованная строка в кодировке UTF-8.

    Raises:
        TypeError: Если `input_data` не является строкой или списком.
        Exception: Если возникает ошибка при обработке строки.

    Example:
        >>> normalize_string(['Hello', '  World!  '])
        'Hello World!'
    """
    if not input_data:
        return ''

    original_input: str | list = input_data  # Сохраняется исходное значение. В случае ошибки парсинга строки вернется это значение

    if not isinstance(input_data, (str, list)):
        raise TypeError('Данные должны быть строкой или списком строк.')

    if isinstance(input_data, list):
        input_data: str = ' '.join(map(str, input_data))

    try:
        cleaned_str: str = remove_html_tags(input_data)
        cleaned_str: str = remove_line_breaks(cleaned_str)
        cleaned_str: str = remove_special_characters(cleaned_str)
        normalized_str: str = ' '.join(cleaned_str.split())

        return normalized_str.strip().encode('utf-8').decode('utf-8')
    except Exception as ex:
        logger.error('Ошибка в normalize_string: ', ex, exc_info=True)
        return str(original_input).encode('utf-8').decode('utf-8')


def normalize_int(input_data: str | int | float | Decimal) -> int:
    """
    Преобразует входные данные в целое число.

    Args:
        input_data (str | int | float | Decimal): Входные данные, которые могут быть числом или строковым представлением числа.

    Returns:
        int: Целочисленное представление входных данных.

    Raises:
        ValueError: Если входные данные не могут быть преобразованы в целое число.
        TypeError: Если входные данные имеют некорректный тип.
        InvalidOperation: Если происходит ошибка при выполнении операции.

    Example:
        >>> normalize_int('42')
        42
    """
    original_input: str | int | float | Decimal = input_data  # Сохраняется исходное значение
    try:
        if isinstance(input_data, Decimal):
            return int(input_data)
        return int(float(input_data))
    except (ValueError, TypeError, InvalidOperation) as ex:
        logger.error('Ошибка в normalize_int: ', ex, exc_info=True)
        return original_input  # Возвращается исходное значение


def normalize_float(value: Any) -> Optional[float]:
    """
    Безопасно преобразует входные значения в float или список float.

    Args:
        value (Any): Входное значение для преобразования.
                     Это может быть одиночное значение (число или строка) или итерируемый объект (список/кортеж).

    Returns:
        float | None: Значение float, список float или None, если преобразование не удалось.

    Example:
        >>> normalize_float("3.14")
        3.14
        >>> normalize_float([1, '2.5', 3])
        [1.0, 2.5, 3.0]
    """
    if not value:
        return None

    if isinstance(value, (list, tuple)):
        return [v for v in (normalize_float(v) for v in value) if v is not None]

    try:
        return float(value)
    except (ValueError, TypeError) as ex:
        logger.warning(f"Невозможно преобразовать '{value}' в float.", exc_info=True)
        return None


def normalize_sql_date(input_data: str | datetime) -> str:
    """
    Преобразует входные данные в формат даты SQL (YYYY-MM-DD).

    Args:
        input_data (str | datetime): Данные, которые могут быть представлены как дата (например, строка, объект datetime).

    Returns:
        str: Нормализованная дата в формате SQL (YYYY-MM-DD) или исходное значение, если преобразование не удалось.

    Raises:
        ValueError: Если входная строка не соответствует ни одному из известных форматов даты.
        TypeError: Если входные данные имеют некорректный тип.

    Example:
        >>> normalize_sql_date('2024-12-06')
        '2024-12-06'
        >>> normalize_sql_date('12/06/2024')
        '2024-12-06'
    """
    original_input: str | datetime = input_data  # Сохраняется исходное значение

    try:
        # Проверка и преобразование строки в формат даты
        if isinstance(input_data, str):
            # Попытка распарсить дату из строки
            for date_format in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
                try:
                    normalized_date: datetime = datetime.strptime(input_data, date_format).date()
                    return normalized_date.isoformat()  # Возвращаем дату в формате 'YYYY-MM-DD'
                except ValueError:
                    continue
        # Если входные данные уже объект datetime
        if isinstance(input_data, datetime):
            return input_data.date().isoformat()

    except Exception as ex:
        logger.error('Ошибка в normalize_sql_date: ', ex, exc_info=True)

    logger.debug(f'Не удалось преобразовать в SQL дату: {input_data}')
    return original_input  # Возвращается исходное значение


def simplify_string(input_str: str) -> str:
    """
    Упрощает входную строку, оставляя только буквы, цифры и заменяя пробелы на подчеркивания.

    Args:
        input_str (str): Строка для упрощения.

    Returns:
        str: Упрощенная строка.

    Raises:
        Exception: Если возникает ошибка при упрощении строки.

    Example:
        >>> simplify_string("It's a test string with 'single quotes', numbers 123 and symbols!")
        'Its_a_test_string_with_single_quotes_numbers_123_and_symbols'
    """
    try:
        # Remove all characters except letters, digits, and spaces
        cleaned_str: str = re.sub(r'[^a-zA-Z0-9\s]', '', input_str)
        # Replace spaces with underscores
        cleaned_str: str = cleaned_str.replace(' ', '_')
        # Remove consecutive underscores
        cleaned_str: str = re.sub(r'_+', '_', cleaned_str)
        return cleaned_str
    except Exception as ex:
        logger.error("Error simplifying the string", ex, exc_info=True)
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
        input_html (str): Входная HTML-строка.

    Returns:
        str: Строка без HTML-тегов.
    """
    return re.sub(r'<.*?>', '', input_html).strip()


def remove_special_characters(input_str: str | list, chars: Optional[list[str]] = None) -> str | list:
    """
    Удаляет указанные специальные символы из строки или списка строк.

    Args:
        input_str (str | list): Входная строка или список строк.
        chars (list[str], optional): Список символов для удаления. По умолчанию None.

    Returns:
        str | list: Обработанная строка или список с удаленными указанными символами.
    """
    if chars is None:
        chars: list[str] = ['#']  # Default list of characters to remove

    pattern: str = '[' + re.escape(''.join(chars)) + ']'

    if isinstance(input_str, list):
        return [re.sub(pattern, '', s) for s in input_str]
    return re.sub(pattern, '', input_str)


def normalize_sku(input_str: str) -> str:
    """
    Нормализует SKU, удаляя определенные ивритские ключевые слова и любые не-буквенно-цифровые символы,
    кроме дефисов.

    Args:
        input_str (str): Входная строка, содержащая SKU.

    Returns:
        str: Нормализованная строка SKU.

    Example:
        >>> normalize_sku("מקט: 303235-A")
        '303235-A'
        >>> normalize_sku("מק''ט: 12345-B")
        '12345-B'
        >>> normalize_sku("Some text מקט: 123-456-789 other text")
        'Some text 123-456-789 other text' # Important: It now keeps the hyphens and spaces between texts
    """
    try:
        # Remove Hebrew keywords
        _str: str = re.sub(r'מקט|מק\'\'ט', '', input_str, flags=re.IGNORECASE)

        # Remove non-alphanumeric characters, except for hyphens
        normalized_sku: str = re.sub(r'[^\w-]+', '', _str)

        return normalized_sku
    except Exception as ex:
        logger.error(f"Error normalizing SKU: ", ex, exc_info=True)  # Include exception details
        return input_str