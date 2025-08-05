# Validation Utilities

## Overview

This module provides utility functions for validating and sanitizing data structures, particularly dictionaries and strings. It aims to ensure data integrity and security by preventing invalid characters and excessive nesting in dictionaries.

## Details

The module is primarily designed to be used within the context of handling data received from external sources or APIs. It provides functions to check for valid fields in dictionaries and to sanitize strings and dictionaries by removing potentially harmful characters and controlling nesting depth. These functions are crucial for preventing security vulnerabilities and ensuring the stability of the application.

## Functions

### `check_valid_fields`

**Purpose**: Проверяет, являются ли поля в заданном словаре допустимыми, согласно списку допустимых полей. Если нет, вызывает ValueError.

**Parameters**:

- `obj` (dict): Словарь для проверки.
- `valid_fields` (list): Список допустимых полей.

**Raises Exceptions**:

- `ValueError`: Выбрасывается, если в словаре обнаружено недопустимое поле.

**Example**:

```python
>>> valid_fields = ["name", "age", "city"]
>>> obj = {"name": "John", "age": 30, "country": "USA"}
>>> check_valid_fields(obj, valid_fields)
Traceback (most recent call last):
  ...
ValueError: Invalid key country in dictionary. Valid keys are: ['name', 'age', 'city']
```

### `sanitize_raw_string`

**Purpose**: Очищает заданную строку:
- Удаляет любые недопустимые символы.
- Убеждается, что ее длина не превышает максимальную длину строки Python.

**Parameters**:

- `value` (str): Строка для очистки.

**Returns**:

- `str`: Очищенная строка.

**How the Function Works**:

- Сначала функция пытается преобразовать строку в UTF-8, игнорируя недопустимые байты.
- Затем она использует `unicodedata.normalize` для приведения строки к нормальной форме NFC.
- Наконец, она обрезает строку до максимальной длины строки Python.

**Example**:

```python
>>> value = "This is a string with some invalid characters: \uFFFD"
>>> sanitize_raw_string(value)
'This is a string with some invalid characters: '
```

### `sanitize_dict`

**Purpose**: Очищает заданный словарь:
- Удаляет любые недопустимые символы.
- Убеждается, что словарь не слишком глубоко вложен.

**Parameters**:

- `value` (dict): Словарь для очистки.

**Returns**:

- `dict`: Очищенный словарь.

**How the Function Works**:

- Функция перебирает все пары ключ-значение в словаре.
- Если значение является строкой, она очищает ее с помощью `sanitize_raw_string`.
- Она не проверяет вложенные словари, чтобы избежать чрезмерной рекурсии.

**Example**:

```python
>>> value = {"name": "John", "age": 30, "city": "New York", "address": {"street": "123 Main St", "zip": "10001"}}
>>> sanitize_dict(value)
{'name': 'John', 'age': 30, 'city': 'New York', 'address': {'street': '123 Main St', 'zip': '10001'}}
```