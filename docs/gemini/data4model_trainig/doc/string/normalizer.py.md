### Анализ кода модуля `hypotez/src/utils/string/normalizer.py`

## Обзор

Этот модуль предоставляет функции для нормализации строк и числовых данных. Он также содержит вспомогательные методы для обработки текста, включая удаление HTML-тегов и специальных символов.

## Подробнее

Модуль содержит набор функций, предназначенных для очистки и стандартизации данных различных типов (строк, чисел, дат), что может быть полезно для подготовки данных к анализу, хранению или дальнейшей обработке.

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
Преобразует входные данные в логическое значение.

**Параметры**:
- `input_data` (Any): Данные, которые могут представлять логическое значение (например, bool, string, integer).

**Возвращает**:
- `bool`: Логическое представление входных данных.

**Как работает функция**:
1. Сохраняет исходное значение `input_data` в переменную `original_input`.
2. Проверяет, является ли `input_data` уже логическим значением. Если да, возвращает его.
3. Пытается преобразовать `input_data` в строку, удаляет пробелы в начале и конце и приводит к нижнему регистру.
4. Проверяет, соответствует ли полученная строка одному из значений, представляющих `True` (например, 'true', '1', 'yes').
5. Проверяет, соответствует ли полученная строка одному из значений, представляющих `False` (например, 'false', '0', 'no').
6. Если преобразование не удалось, логирует информацию об ошибке и возвращает исходное значение `original_input`.

**Примеры**:

```python
normalize_boolean('yes')  # True
normalize_boolean('0')    # False
normalize_boolean(1)      # True
normalize_boolean(None)   # None (возвращается исходное значение)
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
    ...
```

**Назначение**:
Нормализует строку или список строк.

**Параметры**:
- `input_data` (str | list): Входные данные, которые могут быть либо строкой, либо списком строк.

**Возвращает**:
- `str`: Очищенная и нормализованная строка в формате UTF-8.

**Вызывает исключения**:
- `TypeError`: Если `input_data` не является строкой или списком.

**Как работает функция**:
1. Проверяет, является ли входная строка пустой, и возвращает пустую строку, если это так.
2.  Сохраняет исходное значение `input_data` в переменную `original_input`.
3.  Если входные данные являются списком, объединяет их в одну строку, разделяя пробелами.
4.  Удаляет HTML-теги, переносы строк и специальные символы.
5.  Нормализует пробелы (оставляет только один пробел между словами).
6.  Удаляет пробелы в начале и конце строки.
7.  Кодирует строку в UTF-8 и декодирует обратно, чтобы обеспечить правильную кодировку.

**Примеры**:

```python
normalize_string(['Hello', '  World!  '])  # 'Hello World!'
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
    ...
```

**Назначение**:
Преобразует данные в целое число.

**Параметры**:
- `input_data` (str | int | float | Decimal): Входные данные, которые могут быть числом или его строковым представлением.

**Возвращает**:
- `int`: Целочисленное представление входных данных.

**Как работает функция**:
1. Сохраняет исходное значение `input_data` в переменную `original_input`.
2. Проверяет тип входных данных и преобразует их в целое число.
3. В случае ошибки логирует информацию об ошибке и возвращает исходное значение `original_input`.

**Примеры**:

```python
normalize_int('42')  # 42
```

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
Безопасно преобразует входное значение в число с плавающей запятой (с 3 знаками после запятой) или возвращает None, если преобразование не удалось.

**Параметры**:
- `value` (Any): Входное значение (int, float, str и т. д.).

**Возвращает**:
- `Optional[float]`: Число с плавающей запятой с 3 знаками после запятой (например, 5 → 5.000) или None, если преобразование не удалось.

**Как работает функция**:
1. Проверяет, является ли входное значение None. Если да, возвращает None.
2. Проверяет, является ли входное значение списком или кортежем. Если да, логирует предупреждение и возвращает None.
3. Пытается преобразовать входное значение в float, затем округляет до 3 знаков после запятой.
4. В случае ошибки преобразования логирует предупреждение и возвращает None.

**Примеры**:

```python
normalize_float(5)       # 5.0
normalize_float("5")     # 5.0
normalize_float("3.14")  # 3.14
normalize_float("abc")   # None
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
    ...
```

**Назначение**:
Преобразует данные в формат даты SQL (YYYY-MM-DD).

**Параметры**:
- `input_data` (str): Данные, которые могут представлять дату (например, строка, объект datetime).

**Возвращает**:
- `str`: Нормализованная дата в формате SQL (YYYY-MM-DD) или исходное значение, если преобразование не удалось.

**Как работает функция**:
1. Сохраняет исходное значение `input_data`.
2. Пытается преобразовать входные данные в формат даты SQL (YYYY-MM-DD), используя различные форматы даты.
3. Если входные данные уже являются объектом datetime, преобразует их в формат даты SQL.
4. В случае ошибки логирует информацию об ошибке и возвращает исходное значение.

**Примеры**:

```python
normalize_sql_date('2024-12-06')  # '2024-12-06'
normalize_sql_date('12/06/2024')  # '2024-12-06'
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
    ...
```

**Назначение**:
Упрощает входную строку, оставляя только буквы, цифры и заменяя пробелы на подчеркивания.

**Параметры**:
- `input_str` (str): Строка для упрощения.

**Возвращает**:
- `str`: Упрощенная строка.

**Как работает функция**:
1.  Удаляет все символы, кроме букв, цифр и пробелов, используя регулярное выражение.
2.  Заменяет пробелы на символы подчеркивания.
3.  Удаляет повторяющиеся символы подчеркивания.
4.  Возвращает упрощенную строку.

**Примеры**:

```python
example_str = "It's a test string with 'single quotes', numbers 123 and symbols!"
simplified_str = simplify_string(example_str)
print(simplified_str)
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
    ...
```

**Назначение**:
Удаляет переносы строк из входной строки.

**Параметры**:
- `input_str` (str): Входная строка.

**Возвращает**:
- `str`: Строка без переносов строк.

**Как работает функция**:
1. Заменяет все символы новой строки (`\n`) и возврата каретки (`\r`) на пробелы.
2. Удаляет пробелы в начале и конце строки.
3. Возвращает строку без переносов строк.

**Примеры**:

```python
input_str = "Строка с переносом\\nСтрока 2"
output_str = remove_line_breaks(input_str)
print(output_str)  # Строка с переносом Строка 2
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
    ...
```

**Назначение**:
Удаляет HTML-теги из входной строки.

**Параметры**:
- `input_html` (str): Входная HTML-строка.

**Возвращает**:
- `str`: Строка без HTML-тегов.

**Как работает функция**:
1. Использует регулярное выражение для удаления всех HTML-тегов из строки.
2. Удаляет пробелы в начале и конце строки.
3. Возвращает строку без HTML-тегов.

**Примеры**:

```python
input_html = "<p>Hello, world!</p>"
output_str = remove_html_tags(input_html)
print(output_str)  # Hello, world!
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
    ...
```

**Назначение**:
Удаляет указанные специальные символы из строки или списка строк.

**Параметры**:
- `input_str` (str | list): Входная строка или список строк.
- `chars` (list[str], optional): Список символов для удаления. По умолчанию None (используется список `['#']`).

**Возвращает**:
- `str | list`: Обработанная строка или список с удаленными указанными символами.

**Как работает функция**:
1.  Если список символов для удаления не указан, используется список по умолчанию `['#']`.
2.  Создает регулярное выражение для поиска указанных символов.
3.  Если входные данные являются строкой, удаляет все вхождения указанных символов из строки и возвращает результат.
4.  Если входные данные являются списком, применяет регулярное выражение к каждому элементу списка и возвращает новый список с очищенными строками.

**Примеры**:

```python
input_str = "Hello# world!"
output_str = remove_special_characters(input_str)
print(output_str)  # Hello world!
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
    ...
```

**Назначение**:
Нормализует SKU, удаляя определенные ключевые слова на иврите и все не-буквенно-цифровые символы, кроме дефисов.

**Параметры**:
- `input_str` (str): Входная строка, содержащая SKU.

**Возвращает**:
- `str`: Нормализованная SKU-строка.

**Как работает функция**:
1. Удаляет ключевые слова на иврите ("מקט" и "מק''ט") из входной строки, игнорируя регистр.
2. Удаляет все не-буквенно-цифровые символы, кроме дефисов, из полученной строки.
3. Возвращает нормализованную SKU-строку.

**Примеры**:

```python
normalize_sku("מקט: 303235-A")   # '303235-A'
normalize_sku("מק''ט: 12345-B")   # '12345-B'
normalize_sku("Some text מקט: 123-456-789 other text")   # 'Some text 123-456-789 other text'
```

## Переменные

- `TEXT_COLORS`: Словарь, содержащий коды ANSI для цветов текста.
- `BG_COLORS`: Словарь, содержащий коды ANSI для цветов фона.
- `FONT_STYLES`: Словарь, содержащий коды ANSI для стилей шрифта.

## Запуск

Для использования этого модуля необходимо установить библиотеки `re`, `html`, `datetime`, `decimal` и `src.logger.logger`. Библиотеки `re`, `html`, `datetime`, `decimal` обычно входят в стандартную библиотеку Python и не требуют дополнительной установки.

Пример использования:

```python
from src.utils.string.normalizer import normalize_string, normalize_boolean

normalized_str = normalize_string(" Пример строки <b>с HTML</b> ")
normalized_bool = normalize_boolean("yes")

print(f"Normalized string: {normalized_str}")
print(f"Normalized boolean: {normalized_bool}")