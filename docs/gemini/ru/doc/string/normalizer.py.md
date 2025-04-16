### Анализ кода `hypotez/src/utils/string/normalizer.py.md`

## Обзор

Модуль предоставляет функции для нормализации строк и числовых данных.

## Подробнее

Модуль содержит набор утилит для приведения строк, булевых значений, целых чисел, чисел с плавающей точкой и дат к стандартному виду. Он также включает вспомогательные методы для обработки текста, такие как удаление HTML-тегов и специальных символов.

## Функции

### `normalize_boolean`

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

**Назначение**:
Преобразует данные в булевый тип.

**Параметры**:

*   `input_data` (Any): Данные, которые могут быть представлены как булево значение (например, bool, строка, целое число).

**Возвращает**:

*   `bool`: Булево представление входных данных.

**Как работает функция**:

1.  Сохраняет исходное значение входных данных.
2.  Если входные данные уже являются булевым значением, возвращает их без изменений.
3.  Пытается преобразовать входные данные в строку, привести её к нижнему регистру и удалить пробелы в начале и конце.
4.  Если преобразованная строка соответствует одному из значений, представляющих `True` (`'true'`, `'1'`, `'yes'`, `'y'`, `'on'`, `True`, `1`), возвращает `True`.
5.  Если преобразованная строка соответствует одному из значений, представляющих `False` (`'false'`, `'0'`, `'no'`, `'n'`, `'off'`, `False`, `0`), возвращает `False`.
6.  В случае ошибки возвращает исходное значение.
7.  Логирует, если не удалось преобразовать в bool

### `normalize_string`

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

**Назначение**:
Нормализует строку или список строк.

**Параметры**:

*   `input_data` (str | list): Входные данные, которые могут быть либо строкой, либо списком строк.

**Возвращает**:

*   `str`: Очищенная и нормализованная строка в формате UTF-8.

**Вызывает исключения**:

*   `TypeError`: Если `input_data` не является строкой или списком.

**Как работает функция**:

1.  Проверяет входные данные на пустоту и возвращает пустую строку, если они пусты.
2.  Сохраняет исходное значение входных данных.
3.  Проверяет, является ли входной параметр строкой или списком. Если нет, выбрасывает исключение `TypeError`.
4.  Если входные данные являются списком, объединяет их в одну строку, разделяя пробелами.
5.  Удаляет HTML-теги, разрывы строк и специальные символы из строки.
6.  Нормализует пробелы, заменяя множественные пробелы на один.
7.  Удаляет пробелы в начале и конце строки.
8.  Возвращает строку в кодировке UTF-8.
9.  Логирует информацию об ошибках.

### `normalize_int`

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

**Назначение**:
Преобразует данные в целое число.

**Параметры**:

*   `input_data` (str | int | float | Decimal): Входные данные, которые могут быть числом или его строковым представлением.

**Возвращает**:

*   `int`: Целочисленное представление входных данных.

**Как работает функция**:

1.  Сохраняет исходное значение входных данных.
2.  Если входные данные являются экземпляром `Decimal`, преобразует их в целое число.
3.  Если входные данные являются числом или его строковым представлением, пытается преобразовать их в целое число, сначала преобразовав в число с плавающей точкой.
4.  Возвращает преобразованное целое число.
5.  В случае ошибки возвращает исходное значение.
6.  Логирует информацию об ошибках.

### `normalize_float`

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

**Назначение**:
Безопасно преобразует входное значение в число с плавающей точкой (с 3 знаками после запятой) или возвращает `None`, если преобразование не удается.

**Параметры**:

*   `value` (Any): Входное значение (int, float, str и т.д.).

**Возвращает**:

*   `Optional[float]`: Число с плавающей точкой с 3 знаками после запятой (например, 5 → 5.000) или `None`, если преобразование не удалось.

**Как работает функция**:

1.  Проверяет входное значение на `None`.
2.  Если входное значение является списком или кортежем, логирует предупреждение и возвращает `None`.
3.  Пытается преобразовать входное значение в число с плавающей точкой.
4.  В случае успеха возвращает число с плавающей точкой.
5.  В случае ошибки логирует предупреждение и возвращает `None`.

### `normalize_sql_date`

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

**Назначение**:
Нормализует данные в формат даты SQL (YYYY-MM-DD).

**Параметры**:

*   `input_data` (str): Данные, которые могут представлять дату (например, строка, объект datetime).

**Возвращает**:

*   `str`: Нормализованная дата в формате SQL (YYYY-MM-DD) или исходное значение, если преобразование не удалось.

**Как работает функция**:

1.  Сохраняет исходное значение входных данных.
2.  Проверяет, является ли входное значение строкой. Если да, пытается распарсить дату из строки, используя разные форматы (`'%Y-%m-%d'`, `'%m/%d/%Y'`, `'%d/%m/%Y'`).
3.  Если входные данные уже являются объектом `datetime`, преобразует их в формат `YYYY-MM-DD`.
4.  В случае ошибки возвращает исходное значение.
5.  Логирует информацию об ошибках.

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

**Назначение**:
Упрощает входную строку, оставляя только буквы, цифры и заменяя пробелы символами подчеркивания.

**Параметры**:

*   `input_str` (str): Строка для упрощения.

**Возвращает**:

*   `str`: Упрощенная строка.

**Как работает функция**:

1.  Удаляет все символы, кроме букв, цифр и пробелов.
2.  Заменяет пробелы символами подчеркивания.
3.  Удаляет последовательные символы подчеркивания.
4.  В случае ошибки логирует её и возвращает исходную строку.

### `remove_line_breaks`

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

**Назначение**:
Удаляет символы переноса строки из входной строки.

**Параметры**:

*   `input_str` (str): Входная строка.

**Возвращает**:

*   `str`: Строка без переносов строк.

**Как работает функция**:

1.  Заменяет символы `\n` и `\r` на пробелы.
2.  Удаляет пробелы в начале и конце строки.
3.  Возвращает полученную строку.

### `remove_html_tags`

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

**Назначение**:
Удаляет HTML-теги из входной строки.

**Параметры**:

*   `input_html` (str): Входная HTML-строка.

**Возвращает**:

*   `str`: Строка без HTML-тегов.

**Как работает функция**:

1.  Использует регулярное выражение для удаления всех HTML-тегов из строки.
2.  Удаляет пробелы в начале и конце строки.
3.  Возвращает полученную строку.

### `remove_special_characters`

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

**Назначение**:
Удаляет указанные специальные символы из строки или списка строк.

**Параметры**:

*   `input_str` (str | list): Входная строка или список строк.
*   `chars` (list[str], optional): Список символов для удаления. По умолчанию `None`.

**Возвращает**:

*   `str | list`: Обработанная строка или список строк с удаленными символами.

**Как работает функция**:

1.  Если `chars` не указан, используется список символов по умолчанию `['#']`.
2.  Создает регулярное выражение на основе списка символов для удаления.
3.  Если входные данные - строка, удаляет указанные символы из строки с помощью регулярного выражения.
4.  Если входные данные - список строк, применяет регулярное выражение к каждой строке в списке.
5.  Возвращает обработанную строку или список строк.

### `normalize_sku`

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

**Назначение**:
Нормализует SKU, удаляя определенные ключевые слова на иврите и все не-буквенно-цифровые символы, кроме дефисов.

**Параметры**:

*   `input_str` (str): Входная строка, содержащая SKU.

**Возвращает**:

*   `str`: Нормализованная строка SKU.

**Как работает функция**:

1.  Удаляет ключевые слова на иврите ("מקט" и "מק''ט"), используя регулярное выражение.
2.  Удаляет все символы, не являющиеся буквенно-цифровыми или дефисами, используя регулярное выражение.
3.  Логирует ошибки.

## Константы

*   `RESET`: ANSI escape-код для сброса всех стилей.
*   `TEXT_COLORS`: Словарь, содержащий соответствие между названиями цветов текста и ANSI escape-кодами для этих цветов.
*   `BG_COLORS`: Словарь, содержащий соответствие между названиями цветов фона и ANSI escape-кодами для этих цветов.
*   `FONT_STYLES`: Словарь, содержащий соответствие между названиями стилей шрифта и ANSI escape-кодами для этих стилей.

## Примеры использования

```python
from src.utils.string.normalizer import normalize_string, normalize_boolean, normalize_int, normalize_float, normalize_sql_date

# Пример использования normalize_string
input_str = "  <h1>Hello World!</h1>  "
normalized_str = normalize_string(input_str)
print(normalized_str)  # Hello World!

# Пример использования normalize_boolean
input_bool = "yes"
normalized_bool = normalize_boolean(input_bool)
print(normalized_bool)  # True

# Пример использования normalize_int
input_int = "42"
normalized_int = normalize_int(input_int)
print(normalized_int)  # 42

# Пример использования normalize_float
input_float = "3.14159"
normalized_float = normalize_float(input_float)
print(normalized_float)

# Пример использования normalize_sql_date
input_date = "12/25/2023"
normalized_date = normalize_sql_date(input_date)
print(normalized_date) # 2023-12-25
```

## Зависимости

*   `re`: Для работы с регулярными выражениями.
*   `html`: Для работы с HTML.
*   `datetime`: Для работы с датой и временем.
*   `decimal.Decimal`: Для точной работы с десятичными числами.
*   `typing.Any, typing.List, typing.Optional`: Для аннотаций типов.
*   `src.logger.logger`: Для логирования событий и ошибок.

## Взаимосвязи с другими частями проекта

Модуль `normalizer.py` предоставляет набор утилит для нормализации данных различных типов и может использоваться в других частях проекта `hypotez`, где требуется приведение данных к определенному формату перед их обработкой или сохранением.  Например, при получении данных от пользователя, перед записью их в базу данных или перед отправкой на внешние сервисы.