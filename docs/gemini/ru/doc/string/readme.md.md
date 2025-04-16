# Модуль для нормализации строк (src.utils.string)

## Обзор

Этот модуль предоставляет функциональность для нормализации различных типов данных, включая строки, булевы значения, целые числа и числа с плавающей точкой. Он также содержит вспомогательные функции для обработки текста, включая удаление HTML-тегов и специальных символов.

## Подробней

Модуль `src.utils.string` предназначен для предоставления инструментов для очистки и стандартизации данных. В частности, он содержит функции для преобразования строк, числовых значений и дат в определенные форматы, что облегчает их дальнейшую обработку и анализ.

## Функции

### `normalize_boolean`

**Назначение**: Преобразует входное значение в булево.

```python
def normalize_boolean(input_data: Any) -> bool:
    """Normalize data into a boolean.

    Args:
        input_data (Any): Data that can represent a boolean (e.g., bool, string, integer).

    Returns:
        bool: Boolean representation of the input.

    Example:
        >>> normalize_boolean('yes')
        True
    """
    ...
```

**Параметры**:

-   `input_data` (Any): Данные, которые могут быть интерпретированы как булево значение (например, строка, число, булево значение).

**Возвращает**:

-   `bool`: Булево представление входных данных.

**Как работает функция**:

1.  Сохраняет исходное значение входных данных.
2.  Проверяет, является ли входное значение уже булевым. Если да, возвращает его.
3.  Пытается преобразовать входные данные в строку, привести ее к нижнему регистру и удалить пробельные символы.
4.  Проверяет, соответствует ли полученная строка одному из значений, представляющих `True` (`'true'`, `'1'`, `'yes'`, `'y'`, `'on'`, `True`, `1`).
5.  Если строка не соответствует значениям `True`, проверяет, соответствует ли она одному из значений, представляющих `False` (`'false'`, `'0'`, `'no'`, `'n'`, `'off'`, `False`, `0`).
6.  Если строка не соответствует ни одному из известных значений, логирует отладочное сообщение и возвращает исходное значение.

### `normalize_string`

**Назначение**: Нормализует строку или список строк.

```python
def normalize_string(input_data: str | list) -> str:
    """Normalize a string or a list of strings.

    Args:
        input_data (str | list): Input data that can be either a string or a list of strings.

    Returns:
        str: Cleaned and normalized string in UTF-8 encoded format.

    Example:
        >>> normalize_string(['Hello', '  World!  '])
        'Hello World!'

    Raises:
        TypeError: If `input_data` is not of type `str` or `list`.
    """
    ...
```

**Параметры**:

-   `input_data` (str | list): Входные данные, которые могут быть строкой или списком строк.

**Возвращает**:

-   `str`: Очищенная и нормализованная строка в формате UTF-8.

**Как работает функция**:

1.  Проверяет, является ли входное значение пустой строкой или `None`. Если да, возвращает пустую строку.
2.  Сохраняет исходное значение входных данных.
3.  Проверяет тип входных данных. Если это не строка и не список, вызывает `TypeError`.
4.  Если входные данные - список, объединяет строки списка в одну строку, разделяя их пробелами.
5.  Удаляет HTML-теги, переносы строк и специальные символы из строки, используя функции `remove_html_tags`, `remove_line_breaks` и `remove_special_characters`.
6.  Удаляет лишние пробельные символы и возвращает строку в формате UTF-8.
7.  В случае ошибки логирует ошибку и возвращает исходное значение в кодировке UTF-8.

### `normalize_int`

**Назначение**: Преобразует данные в целое число.

```python
def normalize_int(input_data: str | int | float | Decimal) -> int:
    """Normalize data into an integer.

    Args:
        input_data (str | int | float | Decimal): Input data that can be a number or its string representation.

    Returns:
        int: Integer representation of the input.

    Example:
        >>> normalize_int('42')
        42
    """
    ...
```

**Параметры**:

-   `input_data` (str | int | float | Decimal): Входные данные, которые могут быть числом или его строковым представлением.

**Возвращает**:

-   `int`: Целое число, представляющее входные данные.

**Как работает функция**:

1.  Сохраняет исходное значение входных данных.
2.  Пытается преобразовать входные данные в число с плавающей точкой, а затем в целое число.
3.  В случае возникновения исключения логирует ошибку и возвращает исходное значение.

### `normalize_float`

**Назначение**: Безопасно преобразует входное значение в число с плавающей точкой (с 3 знаками после запятой) или возвращает `None`, если преобразование не удалось.

```python
def normalize_float(value: Any) -> Optional[float]:
    """Safely convert input value to float (with 3 decimal places) or return None if conversion fails.
    
    Args:
        value (Any): Input value (int, float, str, etc.).
    
    Returns:
        Optional[float]: Float with 3 decimal places (e.g., 5 → 5.000) or None if conversion fails.
    
    Examples:
        >>> normalize_float(5)
        5.0
        >>> normalize_float("5")
        5.0
        >>> normalize_float("3.14")
        3.14
        >>> normalize_float("abc")
        None

    Важно! проверять после вызова этой функции, что она не вернула None
    """
    ...
```

**Параметры**:

-   `value` (Any): Входное значение (int, float, str и т.д.).

**Возвращает**:

-   `Optional[float]`: Число с плавающей точкой с 3 знаками после запятой (например, 5 → 5.000) или `None`, если преобразование не удалось.

**Как работает функция**:

1.  Проверяет, является ли входное значение `None`. Если да, возвращает `None`.
2.  Проверяет, является ли входное значение списком или кортежем. Если да, логирует предупреждение и возвращает `None`.
3.  Пытается преобразовать входное значение в `float`, а затем округлить его до 3 знаков после запятой.
4.  Если преобразование не удалось, логирует предупреждение и возвращает `None`.

### `normalize_sql_date`

**Назначение**: Нормализует данные в формат даты SQL (YYYY-MM-DD).

```python
def normalize_sql_date(input_data: str) -> str:
    """Normalize data into SQL date format (YYYY-MM-DD).

    Args:
        input_data (str): Data that can represent a date (e.g., string, datetime object).

    Returns:
        str: Normalized date in SQL format (YYYY-MM-DD) or original value if conversion fails.

    Example:
        >>> normalize_sql_date('2024-12-06')
        '2024-12-06'
        >>> normalize_sql_date('12/06/2024')
        '2024-12-06'
    """
    ...
```

**Параметры**:

-   `input_data` (str): Данные, которые могут представлять дату (например, строка, объект datetime).

**Возвращает**:

-   `str`: Нормализованная дата в формате SQL (YYYY-MM-DD) или исходное значение, если преобразование не удалось.

**Как работает функция**:

1.  Сохраняет исходное значение входных данных.
2.  Проверяет, является ли входное значение строкой или объектом `datetime`.
3.  Если это строка, пытается распарсить дату из строки, используя несколько форматов (`'%Y-%m-%d'`, `'%m/%d/%Y'`, `'%d/%m/%Y'`).
4.  Если это объект `datetime`, преобразует его в строку в формате ISO (`YYYY-MM-DD`).
5.  В случае ошибки логирует ошибку и возвращает исходное значение.

### `simplify_string`

```python
def simplify_string(input_str: str) -> str:
    """ Simplifies the input string by keeping only letters, digits, and replacing spaces with underscores.

    @param input_str: The string to be simplified.
    @return: The simplified string.
    @code
        example_str = "It's a test string with 'single quotes', numbers 123 and symbols!"
        simplified_str = StringNormalizer.simplify_string(example_str)
        print(simplified_str)  # Output: Its_a_test_string_with_single_quotes_numbers_123_and_symbols
    @endcode
    """
    ...
```

Упрощает входную строку, оставляя только буквы, цифры и заменяя пробелы на подчеркивания.

**Параметры**:

-   `input_str` (str): Строка для упрощения.

**Возвращает**:

-   `str`: Упрощенная строка.

**Как работает функция**:

1.  Удаляет все символы, кроме букв, цифр и пробелов, используя регулярное выражение.
2.  Заменяет пробелы на подчеркивания.
3.  Удаляет повторяющиеся подчеркивания.

### `remove_line_breaks`

**Назначение**: Удаляет переносы строк из входной строки.

```python
def remove_line_breaks(input_str: str) -> str:
    """Remove line breaks from the input string.

    Args:
        input_str (str): Input string.

    Returns:
        str: String without line breaks.
    """
    ...
```

**Параметры**:

-   `input_str` (str): Входная строка.

**Возвращает**:

-   `str`: Строка без переносов строк.

**Как работает функция**:

1.  Заменяет все символы новой строки (`\n`) и возврата каретки (`\r`) на пробелы.
2.  Удаляет пробельные символы в начале и конце строки.

### `remove_html_tags`

**Назначение**: Удаляет HTML-теги из входной строки.

```python
def remove_html_tags(input_html: str) -> str:
    """Remove HTML tags from the input string.

    Args:
        input_html (str): Input HTML string.

    Returns:
        str: String without HTML tags.
    """
    ...
```

**Параметры**:

-   `input_html` (str): HTML-строка для очистки.

**Возвращает**:

-   `str`: Строка без HTML-тегов.

**Как работает функция**:

1.  Использует регулярное выражение для удаления всех HTML-тегов из строки.
2.  Удаляет пробельные символы в начале и конце строки.

### `remove_special_characters`

**Назначение**: Удаляет указанные специальные символы из строки или списка строк.

```python
def remove_special_characters(input_str: str | list, chars: list[str] = None) -> str | list:
    """Remove specified special characters from a string or list of strings.

    Args:
        input_str (str | list): Input string or list of strings.
        chars (list[str], optional): List of characters to remove. Defaults to None.

    Returns:
        str | list: Processed string or list with specified characters removed.
    """
    ...
```

**Параметры**:

-   `input_str` (str | list): Входная строка или список строк.
-   `chars` (list[str], optional): Список символов для удаления. По умолчанию `None`.

**Возвращает**:

-   `str | list`: Обработанная строка или список строк с удаленными специальными символами.

**Как работает функция**:

1.  Определяет список символов для удаления. Если `chars` не указан, использует список по умолчанию (`['#']`).
2.  Формирует регулярное выражение для поиска указанных символов.
3.  Если входные данные - строка, удаляет все соответствующие символы из строки, используя регулярное выражение.
4.  Если входные данные - список строк, применяет регулярное выражение к каждой строке в списке.

### `normalize_sku`

**Назначение**: Нормализует SKU (Stock Keeping Unit), удаляя определенные ключевые слова и любые не-алфанумерные символы, кроме дефисов.

```python
def normalize_sku(input_str: str) -> str:
    """
    Normalizes the SKU by removing specific Hebrew keywords and any non-alphanumeric characters, 
    except for hyphens.

    Args:
        input_str (str): The input string containing the SKU.

    Returns:
        str: The normalized SKU string.

    Example:
        >>> normalize_sku("מקט: 303235-A")
        '303235-A'
        >>> normalize_sku("מק''ט: 12345-B")
        '12345-B'
        >>> normalize_sku("Some text מקט: 123-456-789 other text")
        'Some text 123-456-789 other text' # Important: It now keeps the hyphens and spaces between texts
    """
    ...
```

**Параметры**:

-   `input_str` (str): Строка, содержащая SKU.

**Возвращает**:

-   `str`: Нормализованная строка SKU.

**Как работает функция**:

1.  Удаляет из входной строки определенные ключевые слова на иврите ("מקט" и "מק''ט"), игнорируя регистр.
2.  Удаляет все не-буквенно-цифровые символы, кроме дефисов, из строки.

## Переменные модуля

-   В данном модуле отсутствуют глобальные переменные, за исключением констант, определенных внутри функций (если бы они были).

## Пример использования

```python
from src.utils.string import normalizer

# Пример использования функций нормализации
text = "  Пример строки <b>с HTML</b>  "
normalized_text = normalizer.normalize_string(text)
print(f"Нормализованная строка: {normalized_text}")

boolean_value = normalizer.normalize_boolean("yes")
print(f"Булево значение: {boolean_value}")

int_value = normalizer.normalize_int("42")
print(f"Целое число: {int_value}")
```

## Взаимосвязь с другими частями проекта

-   Этот модуль предоставляет утилиты для обработки строк и чисел, которые могут использоваться в различных частях проекта `hypotez`.
-   Для логирования ошибок используется модуль `src.logger.logger`.