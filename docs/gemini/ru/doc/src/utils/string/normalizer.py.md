# Модуль для нормализации строк и числовых данных

## Обзор

Модуль предоставляет функции для нормализации строк, булевых значений, целых чисел и чисел с плавающей точкой. Он также содержит вспомогательные методы для обработки текста, включая удаление HTML-тегов и специальных символов.

## Подробнее

Этот модуль предоставляет набор функций для очистки и нормализации различных типов данных, таких как строки, булевы значения, целые числа, числа с плавающей точкой и даты. Он полезен для подготовки данных перед их использованием в различных приложениях, таких как базы данных, веб-приложения и т.д.

## Оглавление

- [normalize_boolean](#normalize_boolean)
- [normalize_string](#normalize_string)
- [normalize_int](#normalize_int)
- [normalize_float](#normalize_float)
- [normalize_sql_date](#normalize_sql_date)
- [simplify_string](#simplify_string)
- [remove_line_breaks](#remove_line_breaks)
- [remove_html_tags](#remove_html_tags)
- [remove_special_characters](#remove_special_characters)
- [normalize_sku](#normalize_sku)

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

**Назначение**: Преобразует входные данные в булево значение.

**Параметры**:

- `input_data` (Any): Данные, которые могут быть представлены как булево значение (например, bool, строка, целое число).

**Возвращает**:

- `bool`: Булево представление входных данных.

**Как работает функция**:

Функция `normalize_boolean` принимает любые входные данные и пытается преобразовать их в булево значение. Сначала проверяется, является ли входное значение булевым типом. Если да, оно возвращается без изменений. В противном случае входные данные преобразуются в строку, удаляются пробелы в начале и конце, и приводятся к нижнему регистру. Затем проверяется, соответствует ли строка одному из предопределенных строковых представлений `True` или `False` (например, "true", "1", "yes", "false", "0", "no").  В случае возникновения исключения во время преобразования или если входные данные не соответствуют ни одному из известных булевых представлений, функция возвращает исходное значение.

**Примеры**:

```python
normalize_boolean('yes')  # Возвращает: True
normalize_boolean(1)      # Возвращает: True
normalize_boolean('no')   # Возвращает: False
normalize_boolean(0)      # Возвращает: False
normalize_boolean(True)   # Возвращает: True
normalize_boolean('abc')  # Возвращает: 'abc'
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

Функция `normalize_string` принимает строку или список строк в качестве входных данных. Если входные данные являются списком, они объединяются в одну строку с пробелами между элементами. Затем из строки удаляются HTML-теги, разрывы строк и специальные символы. После этого строка нормализуется путем удаления лишних пробелов и приведения к формату UTF-8.  В случае возникновения ошибки во время обработки, функция возвращает исходное значение, преобразованное в строку и закодированное в UTF-8.

**Примеры**:

```python
normalize_string(['Hello', '  World!  '])  # Возвращает: 'Hello World!'
normalize_string(' Пример строки <b>с HTML</b> ')  # Возвращает: 'Пример строки с HTML'
normalize_string('Hello\nWorld!')  # Возвращает: 'Hello World!'
normalize_string('Hello#World!')  # Возвращает: 'Hello World!'
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

- `int`: Целочисленное представление входных данных.

**Как работает функция**:

Функция `normalize_int` принимает число или его строковое представление и пытается преобразовать его в целое число. Если входные данные являются экземпляром `Decimal`, они сначала преобразуются в `int`. Если входные данные не могут быть преобразованы в целое число, функция возвращает исходное значение. В случае возникновения исключения во время преобразования, функция возвращает исходное значение.

**Примеры**:

```python
normalize_int('42')      # Возвращает: 42
normalize_int(42.5)     # Возвращает: 42
normalize_int(Decimal('42.5'))  # Возвращает: 42
normalize_int('abc')     # Возвращает: 'abc'
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

**Назначение**: Безопасно преобразует входное значение в число с плавающей точкой или возвращает `None`, если преобразование не удалось.

**Параметры**:

- `value` (Any): Входное значение (int, float, str и т.д.).

**Возвращает**:

- `Optional[float]`: Число float или `None`, если преобразование не удалось.

**Как работает функция**:

Функция `normalize_float` принимает любое значение и пытается преобразовать его в число с плавающей точкой. Если входное значение равно `None`, функция возвращает `None`. Если входное значение уже является числом (int или float), оно преобразуется в float и возвращается. Если входное значение является списком или кортежем, функция регистрирует предупреждение и возвращает `None`. В противном случае входное значение преобразуется в строку, из которой удаляются символы валют и разделители тысяч. Затем функция пытается преобразовать очищенную строку в float. Если преобразование успешно, функция возвращает полученное значение float. Если преобразование не удается, функция регистрирует предупреждение и возвращает `None`.

**Примеры**:

```python
normalize_float(5)         # Возвращает: 5.0
normalize_float("5")       # Возвращает: 5.0
normalize_float("3.14")    # Возвращает: 3.14
normalize_float("abc")      # Возвращает: None
normalize_float("₪0.00")    # Возвращает: 0.0
normalize_float("$1,234.56") # Возвращает: 1234.56
normalize_float("  - 7.5 € ")# Возвращает: -7.5
normalize_float(None)      # Возвращает: None
normalize_float(['1'])      # Возвращает: None
normalize_float('')         # Возвращает: None
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

- `input_data` (str): Данные, которые могут быть представлены как дата (например, строка, объект datetime).

**Возвращает**:

- `str`: Нормализованная дата в формате SQL (YYYY-MM-DD) или исходное значение, если преобразование не удалось.

**Как работает функция**:

Функция `normalize_sql_date` принимает строку или объект datetime и пытается преобразовать его в формат даты SQL (YYYY-MM-DD).  Сначала функция проверяет, является ли входное значение строкой. Если да, она пытается распарсить дату из строки, используя различные форматы даты (например, '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y'). Если входные данные уже являются объектом datetime, они преобразуются в строку в формате YYYY-MM-DD. Если входные данные не могут быть преобразованы в дату, функция возвращает исходное значение. В случае возникновения исключения во время преобразования, функция возвращает исходное значение.

**Примеры**:

```python
normalize_sql_date('2024-12-06')  # Возвращает: '2024-12-06'
normalize_sql_date('12/06/2024')  # Возвращает: '2024-12-06'
normalize_sql_date('06/12/2024')  # Возвращает: '2024-12-06'
normalize_sql_date('abc')          # Возвращает: 'abc'
```

### `simplify_string`

```python
def simplify_string(input_str: str) -> str:
    """ Simplifies the input string by keeping only letters, digits, and replacing spaces with underscores.

    @param input_str: The string to be simplified.
    @return: The simplified string.
    @code
        example_str = "It\'s a test string with \'single quotes\', numbers 123 and symbols!"
        simplified_str = StringNormalizer.simplify_string(example_str)
        print(simplified_str)  # Output: Its_a_test_string_with_single_quotes_numbers_123_and_symbols
    @endcode
    """
```

**Назначение**: Упрощает входную строку, оставляя только буквы, цифры и заменяя пробелы на подчеркивания.

**Параметры**:

- `input_str`: Строка для упрощения.

**Возвращает**:

- Упрощенная строка.

**Как работает функция**:

Функция `simplify_string` принимает строку и удаляет из нее все символы, кроме букв, цифр и пробелов. Затем она заменяет пробелы на подчеркивания и удаляет последовательные подчеркивания.

**Примеры**:

```python
example_str = "It's a test string with 'single quotes', numbers 123 and symbols!"
simplified_str = simplify_string(example_str)
print(simplified_str)  # Output: Its_a_test_string_with_single_quotes_numbers_123_and_symbols
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

Функция `remove_line_breaks` принимает строку и удаляет из нее символы новой строки (`\n`) и возврата каретки (`\r`), заменяя их на пробелы.

**Примеры**:

```python
remove_line_breaks("Hello\nWorld!")  # Возвращает: "Hello World!"
remove_line_breaks("Hello\rWorld!")  # Возвращает: "Hello World!"
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

Функция `remove_html_tags` принимает строку, содержащую HTML-теги, и удаляет все теги, используя регулярное выражение.

**Примеры**:

```python
remove_html_tags("<b>Hello</b> World!")  # Возвращает: "Hello World!"
remove_html_tags("<p>This is a paragraph.</p>")  # Возвращает: "This is a paragraph."
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

Функция `remove_special_characters` принимает строку или список строк и удаляет из них указанные специальные символы. Если список символов для удаления не указан, используется список по умолчанию, содержащий символ `#`.

**Примеры**:

```python
remove_special_characters("Hello#World!")       # Возвращает: "Hello World!"
remove_special_characters("Hello#World!", ['#', '!'])  # Возвращает: "HelloWorld"
remove_special_characters(['Hello#', 'World!'], ['#', '!'])  # Возвращает: ['Hello', 'World']
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
        >>> normalize_sku("מק\'\'ט: 12345-B")
        '12345-B'
        >>> normalize_sku("Some text מקט: 123-456-789 other text")
        'Some text 123-456-789 other text' # Important: It now keeps the hyphens and spaces between texts
    """
```

**Назначение**: Нормализует SKU, удаляя определенные ключевые слова на иврите и все не буквенно-цифровые символы, кроме дефисов.

**Параметры**:

- `input_str` (str): Входная строка, содержащая SKU.

**Возвращает**:

- `str`: Нормализованная строка SKU.

**Как работает функция**:

Функция `normalize_sku` принимает строку, содержащую SKU, и выполняет следующие действия:

1.  Удаляет ключевые слова на иврите ("מקט", "מק''ט").
2.  Удаляет все не буквенно-цифровые символы, кроме дефисов.

**Примеры**:

```python
normalize_sku("מקט: 303235-A")  # Возвращает: '303235-A'
normalize_sku("מק''ט: 12345-B")  # Возвращает: '12345-B'
normalize_sku("Some text מקט: 123-456-789 other text")  # Возвращает: 'Some text 123-456-789 other text'