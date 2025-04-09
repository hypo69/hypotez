# Модуль для нормализации строк и числовых данных

## Обзор

Модуль предоставляет функции для нормализации строк, булевых значений, целых чисел и чисел с плавающей точкой.
Он также содержит вспомогательные методы для обработки текста, включая удаление HTML-тегов и специальных символов.

## Подробнее

Модуль содержит набор функций, предназначенных для очистки и приведения к единообразному виду данных различных типов. Это может быть полезно при обработке данных, поступающих из разных источников, где требуется стандартизация форматов.

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
- `input_data` (Any): Данные, которые могут быть представлены как булево значение (например, `bool`, `string`, `integer`).

**Возвращает**:
- `bool`: Булево представление входных данных.

**Как работает функция**:
1. Функция принимает входные данные любого типа.
2. Проверяет, является ли входное значение уже булевым. Если да, возвращает его без изменений.
3. Пытается преобразовать входные данные в строку, привести к нижнему регистру и удалить пробелы.
4. Проверяет, соответствует ли строка одному из предопределенных строковых представлений `True` (например, 'true', '1', 'yes').
5. Если строка соответствует одному из представлений `True`, возвращает `True`.
6. Аналогично проверяет, соответствует ли строка одному из предопределенных строковых представлений `False` (например, 'false', '0', 'no').
7. Если строка соответствует одному из представлений `False`, возвращает `False`.
8. В случае возникновения исключения при обработке, логирует ошибку и возвращает исходное значение.
9. Если входные данные не соответствуют ни одному из известных булевых представлений, логирует отладочное сообщение и возвращает исходное значение.

**ASII Flowchart**:

```
A (Принятие входных данных)
|
B (Проверка, является ли значение булевым)
|
C (Преобразование в строку и приведение к нижнему регистру)
|
D (Проверка на соответствие значениям True)
|
E (Проверка на соответствие значениям False)
|
F (Логирование ошибки, если не удалось преобразовать)
|
G (Возврат исходного значения)
```

**Примеры**:
```python
>>> normalize_boolean('yes')
True
>>> normalize_boolean(1)
True
>>> normalize_boolean('no')
False
>>> normalize_boolean(0)
False
>>> normalize_boolean(True)
True
>>> normalize_boolean(False)
False
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
1. Функция принимает строку или список строк в качестве входных данных.
2. Если входные данные отсутствуют, возвращает пустую строку.
3. Проверяет, является ли входное значение строкой или списком. Если нет, вызывает исключение `TypeError`.
4. Если входные данные являются списком, объединяет элементы списка в одну строку через пробел.
5. Удаляет HTML-теги из строки.
6. Удаляет символы переноса строк из строки.
7. Удаляет специальные символы из строки.
8. Удаляет лишние пробелы и приводит строку к нормализованному виду.
9. Возвращает очищенную и нормализованную строку в формате UTF-8.
10. В случае возникновения исключения при обработке строки, логирует ошибку и возвращает исходное значение в формате UTF-8.

**ASII Flowchart**:

```
A (Принятие входных данных)
|
B (Проверка на пустую строку)
|
C (Проверка типа данных)
|
D (Объединение списка в строку)
|
E (Удаление HTML-тегов)
|
F (Удаление переносов строк)
|
G (Удаление специальных символов)
|
H (Удаление лишних пробелов)
|
I (Кодирование в UTF-8)
|
J (Возврат нормализованной строки)
```

**Примеры**:
```python
>>> normalize_string(['Hello', '  World!  '])
'Hello World!'
>>> normalize_string(' Пример строки <b>с HTML</b> ')
'Пример строки с HTML'
>>> normalize_string("Hello\nWorld!")
'Hello World!'
```

### `normalize_int`

```python
def normalize_int(input_data: Union[str, int, float, Decimal]) -> int:
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
1. Функция принимает число или его строковое представление в качестве входных данных.
2. Проверяет, является ли входное значение экземпляром класса `Decimal`. Если да, преобразует его в целое число.
3. Пытается преобразовать входные данные в число с плавающей точкой, а затем в целое число.
4. В случае возникновения исключения при обработке, логирует ошибку и возвращает исходное значение.

**ASII Flowchart**:

```
A (Принятие входных данных)
|
B (Проверка, является ли значение Decimal)
|
C (Преобразование во float, затем в int)
|
D (Логирование ошибки, если не удалось преобразовать)
|
E (Возврат исходного значения)
```

**Примеры**:
```python
>>> normalize_int('42')
42
>>> normalize_int(42.5)
42
>>> normalize_int(Decimal('42.7'))
42
```

### `normalize_float`

```python
def normalize_float(value: Any) -> float | None:
    """Safely convert input values to float or list of floats.

    Args:
        value (Any): The input value to be converted. 
                     It can be a single value (number or string) or an iterable (list/tuple).

    Returns:
        float | List[float] | None: A float value, a list of floats, or None if conversion fails.

    Example:
        >>> normalize_float("3.14")
        3.14
        >>> normalize_float([1, '2.5', 3])
        [1.0, 2.5, 3.0]
    """
```

**Назначение**: Безопасно преобразует входные значения в число с плавающей точкой или список чисел с плавающей точкой.

**Параметры**:
- `value` (Any): Входное значение для преобразования. Может быть одиночным значением (число или строка) или итерируемым объектом (список/кортеж).

**Возвращает**:
- `float | List[float] | None`: Число с плавающей точкой, список чисел с плавающей точкой или `None`, если преобразование не удалось.

**Как работает функция**:
1. Функция принимает значение любого типа.
2. Если значение отсутствует, возвращает 0.
3. Если значение является списком или кортежем, рекурсивно вызывает `normalize_float` для каждого элемента и возвращает список чисел с плавающей точкой (исключая `None`).
4. Пытается преобразовать входное значение в число с плавающей точкой.
5. В случае возникновения исключения при обработке, логирует предупреждение и возвращает исходное значение.

**ASII Flowchart**:

```
A (Принятие входных данных)
|
B (Проверка на отсутствие значения)
|
C (Проверка, является ли значение списком или кортежем)
|
D (Рекурсивный вызов для каждого элемента списка)
|
E (Преобразование в float)
|
F (Логирование предупреждения, если не удалось преобразовать)
|
G (Возврат исходного значения)
```

**Примеры**:
```python
>>> normalize_float("3.14")
3.14
>>> normalize_float([1, '2.5', 3])
[1.0, 2.5, 3.0]
>>> normalize_float("abc")
'abc'
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
- `input_data` (str): Данные, которые могут быть представлены как дата (например, строка, объект `datetime`).

**Возвращает**:
- `str`: Нормализованная дата в формате SQL (YYYY-MM-DD) или исходное значение, если преобразование не удалось.

**Как работает функция**:
1. Функция принимает строку или объект `datetime` в качестве входных данных.
2. Если входные данные являются строкой, пытается распарсить дату из строки, используя различные форматы (YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY).
3. Если входные данные являются объектом `datetime`, преобразует его в формат даты SQL (YYYY-MM-DD).
4. В случае возникновения исключения при обработке, логирует ошибку и возвращает исходное значение.

**ASII Flowchart**:

```
A (Принятие входных данных)
|
B (Проверка типа данных)
|
C (Попытка распарсить дату из строки)
|
D (Преобразование datetime в формат SQL)
|
E (Логирование ошибки, если не удалось преобразовать)
|
F (Возврат исходного значения)
```

**Примеры**:
```python
>>> normalize_sql_date('2024-12-06')
'2024-12-06'
>>> normalize_sql_date('12/06/2024')
'2024-12-06'
>>> normalize_sql_date('06/12/2024')
'2024-12-06'
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

**Назначение**: Упрощает входную строку, сохраняя только буквы, цифры и заменяя пробелы на подчеркивания.

**Параметры**:
- `input_str` (str): Строка для упрощения.

**Возвращает**:
- `str`: Упрощенная строка.

**Как работает функция**:
1. Функция принимает строку в качестве входных данных.
2. Удаляет все символы, кроме букв, цифр и пробелов.
3. Заменяет пробелы на символы подчеркивания.
4. Удаляет повторяющиеся символы подчеркивания.
5. В случае возникновения исключения при обработке, логирует ошибку и возвращает исходную строку.

**ASII Flowchart**:

```
A (Принятие входных данных)
|
B (Удаление символов, кроме букв, цифр и пробелов)
|
C (Замена пробелов на подчеркивания)
|
D (Удаление повторяющихся подчеркиваний)
|
E (Логирование ошибки, если не удалось преобразовать)
|
F (Возврат исходной строки)
```

**Примеры**:
```python
>>> example_str = "It's a test string with 'single quotes', numbers 123 and symbols!"
>>> simplify_string(example_str)
"Its_a_test_string_with_single_quotes_numbers_123_and_symbols"
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

**Назначение**: Удаляет символы переноса строк из входной строки.

**Параметры**:
- `input_str` (str): Входная строка.

**Возвращает**:
- `str`: Строка без символов переноса строк.

**Как работает функция**:
1. Функция принимает строку в качестве входных данных.
2. Заменяет символы `\n` и `\r` на пробелы.
3. Удаляет начальные и конечные пробелы.
4. Возвращает строку без символов переноса строк.

**ASII Flowchart**:

```
A (Принятие входных данных)
|
B (Замена \n на пробелы)
|
C (Замена \r на пробелы)
|
D (Удаление начальных и конечных пробелов)
|
E (Возврат строки)
```

**Примеры**:
```python
>>> remove_line_breaks("Hello\nWorld!")
'Hello World!'
>>> remove_line_breaks("Hello\rWorld!")
'Hello World!'
>>> remove_line_breaks("Hello\n\rWorld!")
'Hello  World!'
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
1. Функция принимает HTML-строку в качестве входных данных.
2. Использует регулярное выражение для удаления всех HTML-тегов.
3. Удаляет начальные и конечные пробелы.
4. Возвращает строку без HTML-тегов.

**ASII Flowchart**:

```
A (Принятие входных данных)
|
B (Удаление HTML-тегов с помощью регулярного выражения)
|
C (Удаление начальных и конечных пробелов)
|
D (Возврат строки)
```

**Примеры**:
```python
>>> remove_html_tags(" Пример строки <b>с HTML</b> ")
'Пример строки с HTML'
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
1. Функция принимает строку или список строк в качестве входных данных.
2. Если список символов для удаления не указан, использует список по умолчанию `['#']`.
3. Формирует регулярное выражение для удаления указанных символов.
4. Если входные данные являются списком, применяет регулярное выражение к каждому элементу списка.
5. Если входные данные являются строкой, применяет регулярное выражение к строке.
6. Возвращает обработанную строку или список.

**ASII Flowchart**:

```
A (Принятие входных данных)
|
B (Проверка, задан ли список символов для удаления)
|
C (Формирование регулярного выражения)
|
D (Проверка типа входных данных)
|
E (Применение регулярного выражения к каждому элементу списка)
|
F (Применение регулярного выражения к строке)
|
G (Возврат обработанных данных)
```

**Примеры**:
```python
>>> remove_special_characters("Hello#World!", chars=['#', '!'])
'HelloWorld'
>>> remove_special_characters(['Hello#', 'World!'], chars=['#', '!'])
['Hello', 'World']
>>> remove_special_characters("Hello#World!")
'HelloWorld!'
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

**Назначение**: Нормализует SKU, удаляя определенные ключевые слова на иврите и все не буквенно-цифровые символы, кроме дефисов.

**Параметры**:
- `input_str` (str): Входная строка, содержащая SKU.

**Возвращает**:
- `str`: Нормализованная строка SKU.

**Как работает функция**:
1. Функция принимает строку, содержащую SKU, в качестве входных данных.
2. Удаляет ключевые слова на иврите "מקט" и "מק''ט" (без учета регистра).
3. Удаляет все не буквенно-цифровые символы, кроме дефисов.
4. В случае возникновения исключения при обработке, логирует ошибку и возвращает исходную строку.

**ASII Flowchart**:

```
A (Принятие входных данных)
|
B (Удаление ключевых слов на иврите)
|
C (Удаление не буквенно-цифровых символов, кроме дефисов)
|
D (Логирование ошибки, если не удалось преобразовать)
|
E (Возврат нормализованной строки)
```

**Примеры**:
```python
>>> normalize_sku("מקט: 303235-A")
'303235-A'
>>> normalize_sku("מק''ט: 12345-B")
'12345-B'
>>> normalize_sku("Some text מקט: 123-456-789 other text")
'Some text 123-456-789 other text'