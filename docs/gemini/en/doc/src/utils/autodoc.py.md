# Module src.utils.autodoc

## Overview

Модуль `src.utils.autodoc` предоставляет декоратор `autodoc` для автоматического обновления docstring функции с добавлением информации о времени последнего вызова. Это полезно для отслеживания времени выполнения функций и логирования в целях отладки.

## More details

Этот модуль содержит декоратор `autodoc`, который обновляет строку документации функции, добавляя время последнего вызова функции. Декоратор оборачивает функцию, обновляя её docstring перед вызовом, добавляя в него строку с текущим временем. Для получения текущего времени используется библиотека `time`.

## Classes

### `autodoc`

**Description**:
Декоратор для автоматического обновления docstring функции.

**Attributes**:
- Нет атрибутов.

**Methods**:
- `wrapper(*args, **kwargs)`: Обертка для декорируемой функции, которая обновляет docstring перед вызовом функции.

### `update_docstring`

**Description**:
Функция для обновления docstring функции.

**Attributes**:
- Нет атрибутов.

**Methods**:
- Нет методов.

## Functions

### `autodoc(func)`

**Purpose**:
Декоратор для автоматического обновления docstring функции перед её вызовом.

**Parameters**:
- `func` (function): Функция, для которой необходимо обновить docstring.

**Returns**:
- `wrapper`: Обернутая функция, которая обновляет docstring перед вызовом исходной функции.

**How the function works**:
1. Декоратор `autodoc` принимает функцию `func` в качестве аргумента.
2. Внутри декоратора определяется функция `wrapper`, которая будет заменять исходную функцию.
3. Функция `wrapper` вызывает функцию `update_docstring(func)` для обновления docstring исходной функции.
4. Затем `wrapper` вызывает исходную функцию `func` с переданными аргументами и возвращает результат её выполнения.
5. Декоратор `autodoc` возвращает функцию `wrapper`, которая заменяет исходную функцию.

**Examples**:

```python
import functools
import time

def autodoc(func):
    """Декоратор для автоматического обновления docstring функции."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Обновляем docstring перед вызовом функции
        update_docstring(func)
        return func(*args, **kwargs)

    return wrapper

def update_docstring(func):
    """Обновляет docstring функции."""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Проверяем, существует ли docstring
    if func.__doc__:
        # Добавляем информацию о времени последнего вызова
        func.__doc__ += f"\n\nLast called at: {current_time}"
    else:
        func.__doc__ = f"Last called at: {current_time}"

@autodoc
def example_function(param1: int, param2: str) -> None:
    """Пример функции.

    Args:
        param1 (int): Первое значение.
        param2 (str): Второе значение.
    """
    print(f"Processing {param1} and {param2}")

example_function(1, "test")
print(example_function.__doc__)
example_function(2, "another test")
print(example_function.__doc__)
```

### `update_docstring(func)`

**Purpose**:
Обновляет docstring функции, добавляя информацию о времени последнего вызова.

**Parameters**:
- `func` (function): Функция, docstring которой необходимо обновить.

**How the function works**:
1. Функция `update_docstring` принимает функцию `func` в качестве аргумента.
2. Получает текущее время с использованием `time.strftime("%Y-%m-%d %H:%M:%S")`.
3. Проверяет, существует ли у функции docstring.
4. Если docstring существует, добавляет в конец docstring строку с информацией о времени последнего вызова.
5. Если docstring не существует, создает новый docstring с информацией о времени последнего вызова.

**Examples**:

```python
import time

def update_docstring(func):
    """Обновляет docstring функции."""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Проверяем, существует ли docstring
    if func.__doc__:
        # Добавляем информацию о времени последнего вызова
        func.__doc__ += f"\n\nLast called at: {current_time}"
    else:
        func.__doc__ = f"Last called at: {current_time}"

def example_function(param1: int, param2: str) -> None:
    """Пример функции.

    Args:
        param1 (int): Первое значение.
        param2 (str): Второе значение.
    """
    print(f"Processing {param1} and {param2}")

update_docstring(example_function)
print(example_function.__doc__)
```

### `example_function(param1: int, param2: str) -> None`

**Purpose**:
Пример функции, использующей декоратор `autodoc`.

**Parameters**:
- `param1` (int): Первое значение.
- `param2` (str): Второе значение.

**How the function works**:
1. Функция `example_function` принимает два аргумента: `param1` типа `int` и `param2` типа `str`.
2. Функция выводит строку, содержащую значения `param1` и `param2`.
3. Функция не возвращает никакого значения (`None`).
4. Перед вызовом функции декоратор `autodoc` обновляет её docstring, добавляя информацию о времени последнего вызова.

**Examples**:

```python
@autodoc
def example_function(param1: int, param2: str) -> None:
    """Пример функции.

    Args:
        param1 (int): Первое значение.
        param2 (str): Второе значение.
    """
    print(f"Processing {param1} and {param2}")

example_function(1, "test")
# Processing 1 and test
# Пример функции.
#
#     Args:
#         param1 (int): Первое значение.
#         param2 (str): Второе значение.
#
# Last called at: 2024-07-04 15:23:00

example_function(2, "another test")
# Processing 2 and another test
# Пример функции.
#
#     Args:
#         param1 (int): Первое значение.
#         param2 (str): Второе значение.
#
# Last called at: 2024-07-04 15:23:00
#
# Last called at: 2024-07-04 15:23:00