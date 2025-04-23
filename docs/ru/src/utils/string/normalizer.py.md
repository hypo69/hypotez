# Модуль для нормализации строк и числовых данных

## Обзор

Модуль предоставляет функции для нормализации строк, булевых значений, целых чисел и чисел с плавающей точкой.
Он также содержит вспомогательные методы для обработки текста, включая удаление HTML-тегов и специальных символов.

## Подробнее

Этот модуль содержит набор функций для очистки и нормализации различных типов данных, таких как строки, логические значения, целые числа и числа с плавающей точкой. Он предназначен для подготовки данных к дальнейшей обработке или хранению, обеспечивая единообразный формат и удаляя нежелательные символы или теги.

## Классы

В этом модуле нет классов.

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
```

**Назначение**: Преобразует входные данные в логический тип.

**Параметры**:
- `input_data` (Any): Данные, которые могут быть представлены в виде логического значения (например, bool, строка, целое число).

**Возвращает**:
- `bool`: Логическое представление входных данных.

**Как работает функция**:
Функция пытается преобразовать входные данные в логическое значение. Она обрабатывает логические значения, строки (например, 'true', 'yes', '1') и целые числа (0 и 1). Если входные данные не могут быть преобразованы в логическое значение, функция возвращает исходное значение.

**Примеры**:

```python
normalize_boolean('yes')
# True
normalize_boolean(1)
# True
normalize_boolean('no')
# False
normalize_boolean(0)
# False
normalize_boolean(True)
# True
normalize_boolean(False)
# False
```

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
```

**Назначение**: Нормализует строку или список строк.

**Параметры**:
- `input_data` (str | list): Входные данные, которые могут быть строкой или списком строк.

**Возвращает**:
- `str`: Очищенная и нормализованная строка в формате UTF-8.

**Вызывает исключения**:
- `TypeError`: Если `input_data` не является строкой или списком.

**Как работает функция**:
Функция нормализует входные данные, приводя их к строке, удаляя HTML-теги, разрывы строк и специальные символы, а затем нормализует пробелы.
Если входные данные - список, он объединяется в одну строку с пробелами.

**Примеры**:

```python
normalize_string(['Hello', '  World!  '])
# 'Hello World!'
normalize_string(" Пример строки <b>с HTML</b> ")
# 'Пример строки'
```

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
```

**Назначение**: Преобразует входные данные в целое число.

**Параметры**:
- `input_data` (str | int | float | Decimal): Входные данные, которые могут быть числом или его строковым представлением.

**Возвращает**:
- `int`: Целое представление входных данных.

**Как работает функция**:
Функция пытается преобразовать входные данные в целое число. Она обрабатывает строки, целые числа, числа с плавающей точкой и Decimal. Если входные данные не могут быть преобразованы в целое число, функция возвращает исходное значение.

**Примеры**:

```python
normalize_int('42')
# 42
normalize_int(42.5)
# 42
normalize_int(Decimal('42.5'))
# 42
```

### `normalize_float`

```python
def normalize_float(value: Any) -> Optional[float]:
    """
    Безопасно конвертирует входное значение в float или возвращает None,
    если конвертация не удалась. Удаляет распространенные символы валют
    и разделители тысяч перед конвертацией.

    Args:
        value (Any): Входное значение (int, float, str и т.д.).

    Returns:
        Optional[float]: Число float или None, если конвертация не удалась.

    Examples:
        >>> normalize_float(5)
        5.0
        >>> normalize_float("5")
        5.0
        >>> normalize_float("3.14")
        3.14
        >>> normalize_float("abc")
        None
        >>> normalize_float("₪0.00")
        0.0
        >>> normalize_float("$1,234.56")
        1234.56
        >>> normalize_float("  - 7.5 € ")
        -7.5
        >>> normalize_float(None)
        None
        >>> normalize_float(['1'])
        None
        >>> normalize_float('')
        None

    Важно! проверять после вызова этой функции, что она не вернула None
    """
```

**Назначение**: Преобразует входное значение в число с плавающей точкой (float) или возвращает None, если преобразование не удалось.

**Параметры**:
- `value` (Any): Входное значение (int, float, str и т.д.).

**Возвращает**:
- `Optional[float]`: Число типа float или None, если преобразование не удалось.

**Как работает функция**:
Функция пытается преобразовать входное значение в число с плавающей точкой. Если входное значение уже является числом (int или float), оно просто преобразуется в float. Если входное значение является строкой, функция удаляет символы валют и разделители тысяч, а затем пытается преобразовать очищенную строку в float. Если преобразование не удается, функция возвращает None.

**Примеры**:

```python
normalize_float(5)
# 5.0
normalize_float("5")
# 5.0
normalize_float("3.14")
# 3.14
normalize_float("abc")
# None
normalize_float("₪0.00")
# 0.0
normalize_float("$1,234.56")
# 1234.56
normalize_float("  - 7.5 € ")
# -7.5
normalize_float(None)
# None
normalize_float(['1'])
# None
normalize_float('')
# None
```

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
```

**Назначение**: Преобразует входные данные в формат даты SQL (YYYY-MM-DD).

**Параметры**:
- `input_data` (str): Данные, которые могут быть представлены в виде даты (например, строка, объект datetime).

**Возвращает**:
- `str`: Нормализованная дата в формате SQL (YYYY-MM-DD) или исходное значение, если преобразование не удалось.

**Как работает функция**:
Функция пытается преобразовать входные данные в формат даты SQL (YYYY-MM-DD). Она обрабатывает строки в различных форматах (например, 'YYYY-MM-DD', 'MM/DD/YYYY', 'DD/MM/YYYY') и объекты datetime. Если входные данные не могут быть преобразованы в формат даты SQL, функция возвращает исходное значение.

**Примеры**:

```python
normalize_sql_date('2024-12-06')
# '2024-12-06'
normalize_sql_date('12/06/2024')
# '2024-12-06'
normalize_sql_date('06/12/2024')
# '2024-12-06'
```

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
```

**Назначение**: Упрощает входную строку, оставляя только буквы, цифры и заменяя пробелы на подчеркивания.

**Параметры**:
- `input_str` (str): Строка, которую нужно упростить.

**Возвращает**:
- `str`: Упрощенная строка.

**Как работает функция**:
Функция удаляет все символы, кроме букв, цифр и пробелов, заменяет пробелы на подчеркивания и удаляет последовательные подчеркивания.

**Примеры**:

```python
example_str = "It's a test string with 'single quotes', numbers 123 and symbols!"
simplified_str = simplify_string(example_str)
print(simplified_str)
# Its_a_test_string_with_single_quotes_numbers_123_and_symbols
```

### `remove_line_breaks`

```python
def remove_line_breaks(input_str: str) -> str:
    """Remove line breaks from the input string.

    Args:
        input_str (str): Input string.

    Returns:
        str: String without line breaks.
    """
```

**Назначение**: Удаляет разрывы строк из входной строки.

**Параметры**:
- `input_str` (str): Входная строка.

**Возвращает**:
- `str`: Строка без разрывов строк.

**Как работает функция**:
Функция заменяет символы новой строки (`\n`) и возврата каретки (`\r`) на пробелы и удаляет начальные и конечные пробелы.

**Примеры**:

```python
remove_line_breaks("Hello\nWorld!\r")
# "Hello World!"
```

### `remove_html_tags`

```python
def remove_html_tags(input_html: str) -> str:
    """Remove HTML tags from the input string.

    Args:
        input_html (str): Input HTML string.

    Returns:
        str: String without HTML tags.
    """
```

**Назначение**: Удаляет HTML-теги из входной строки.

**Параметры**:
- `input_html` (str): Входная HTML-строка.

**Возвращает**:
- `str`: Строка без HTML-тегов.

**Как работает функция**:
Функция использует регулярное выражение для удаления всех HTML-тегов из входной строки и удаляет начальные и конечные пробелы.

**Примеры**:

```python
remove_html_tags("<p>Hello</p> <b>World!</b>")
# "Hello World!"
```

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
```

**Назначение**: Удаляет указанные специальные символы из строки или списка строк.

**Параметры**:
- `input_str` (str | list): Входная строка или список строк.
- `chars` (list[str], optional): Список символов для удаления. По умолчанию `None`.

**Возвращает**:
- `str | list`: Обработанная строка или список с удаленными указанными символами.

**Как работает функция**:
Функция удаляет специальные символы из входной строки или списка строк. Если список символов для удаления не указан, используется список по умолчанию, содержащий символ '#'.

**Примеры**:

```python
remove_special_characters("Hello#World!", chars=['#', '!'])
# "HelloWorld"
remove_special_characters(["Hello#", "World!"], chars=['#', '!'])
# ["Hello", "World"]
```

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
```

**Назначение**: Нормализует SKU, удаляя определенные ключевые слова на иврите и любые не-буквенно-цифровые символы, кроме дефисов.

**Параметры**:
- `input_str` (str): Входная строка, содержащая SKU.

**Возвращает**:
- `str`: Нормализованная строка SKU.

**Как работает функция**:
Функция удаляет ключевые слова на иврите ("מקט" и "מק''ט") из входной строки, а затем удаляет все не-буквенно-цифровые символы, кроме дефисов.

**Примеры**:

```python
normalize_sku("מקט: 303235-A")
# '303235-A'
normalize_sku("מק''ט: 12345-B")
# '12345-B'
normalize_sku("Some text מקט: 123-456-789 other text")
# 'Some text 123-456-789 other text'