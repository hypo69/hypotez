# Module for Working with Arguments in AliExpress API
## Overview

This module contains helper functions for parsing and validating arguments used in the AliExpress API. These functions ensure that arguments passed to the API calls are in the correct format, preventing errors and improving the reliability of API interactions.

## Details

This module is a crucial part of the AliExpress API integration within the `hypotez` project. It plays a vital role in handling arguments that are passed to different API endpoints. The functions within this module ensure that the arguments are validated and formatted correctly before being sent to the API, minimizing the chances of errors and improving the overall stability of the API integration.

## Functions

### `get_list_as_string`
**Purpose**: Преобразует входной аргумент в строку, если он является списком или строкой.

**Parameters**:
- `value`: Значение, которое нужно преобразовать. Может быть списком или строкой.

**Returns**:
- `str`: Строка, полученная из входного значения. Возвращает `None`, если входное значение - `None`.

**Raises Exceptions**:
- `InvalidArgumentException`: Если входное значение не является ни списком, ни строкой.

**How the Function Works**:

- Проверяет тип входного значения. 
- Если значение - строка, возвращает ее без изменений.
- Если значение - список, соединяет элементы списка с помощью запятой и возвращает полученную строку.
- Если значение - `None`, возвращает `None`.
- В случае, если значение не является ни списком, ни строкой, генерирует исключение `InvalidArgumentException`.

**Examples**:

```python
>>> get_list_as_string('hello')
'hello'

>>> get_list_as_string(['hello', 'world'])
'hello,world'

>>> get_list_as_string(None)
>>> get_list_as_string(123)
Traceback (most recent call last):
  ...
InvalidArgumentException: Argument should be a list or string: 123
```

### `get_product_ids`
**Purpose**: Преобразует входной аргумент в список product_ids.

**Parameters**:
- `values`: Значение, которое нужно преобразовать. Может быть строкой или списком строк, содержащих product_ids.

**Returns**:
- `list`: Список product_ids, полученный из входного значения.

**Raises Exceptions**:
- `InvalidArgumentException`: Если входное значение не является ни строкой, ни списком, или если список содержит недопустимые значения.

**How the Function Works**:

- Проверяет тип входного значения.
- Если значение - строка, разбивает ее по запятой и получает список значений.
- Если значение - список, проверяет тип каждого элемента в списке.
- Использует функцию `get_product_id` для преобразования каждого значения в product_id.
- Возвращает список полученных product_ids.

**Examples**:

```python
>>> get_product_ids('1234567890,1234567891')
['1234567890', '1234567891']

>>> get_product_ids(['1234567890', '1234567891'])
['1234567890', '1234567891']

>>> get_product_ids('1234567890')
['1234567890']

>>> get_product_ids(123)
Traceback (most recent call last):
  ...
InvalidArgumentException: Argument product_ids should be a list or string

>>> get_product_ids(['1234567890', 'abc'])
Traceback (most recent call last):
  ...
InvalidArgumentException: Invalid product_id: abc
```

## Parameter Details

- `value` (str | list): Это значение, которое будет преобразовано в строку или список строк.
- `values` (str | list): Это значение, которое будет преобразовано в список product_ids.

## Examples

```python
>>> get_list_as_string('hello')
'hello'

>>> get_list_as_string(['hello', 'world'])
'hello,world'

>>> get_product_ids('1234567890,1234567891')
['1234567890', '1234567891']

>>> get_product_ids(['1234567890', '1234567891'])
['1234567890', '1234567891']
```