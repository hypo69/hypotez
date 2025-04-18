# Модуль для автоматической генерации документации

## Обзор

Модуль предоставляет инструменты для автоматического обновления docstring функций. Он включает декоратор `@autodoc`, который при каждом вызове функции обновляет её docstring, добавляя информацию о времени последнего вызова.

## Подробнее

Этот модуль предназначен для автоматизации процесса документирования функций, особенно в процессе разработки, когда функции часто меняются. Декоратор `@autodoc` позволяет автоматически добавлять информацию о времени последнего вызова функции в её docstring, что может быть полезно для отслеживания изменений и использования функций.

## Функции

### `autodoc`

```python
def autodoc(func):
    """Декоратор для автоматического обновления docstring функции."""
    ...
```

**Назначение**:
Декоратор `autodoc` предназначен для автоматического обновления docstring функции. Он оборачивает функцию, чтобы перед каждым её вызовом обновлять информацию в docstring о времени последнего вызова.

**Параметры**:
- `func` (function): Функция, для которой необходимо обновить docstring.

**Возвращает**:
- `wrapper` (function): Обернутая функция, которая обновляет docstring перед каждым вызовом.

**Как работает функция**:
1. Декоратор принимает функцию `func` в качестве аргумента.
2. Он определяет внутреннюю функцию `wrapper`, которая будет вызываться вместо исходной функции.
3. Функция `wrapper` вызывает функцию `update_docstring(func)` для обновления docstring функции `func`.
4. После обновления docstring вызывается исходная функция `func` с переданными аргументами.
5. Функция `wrapper` возвращает результат вызова исходной функции.

**Примеры**:

```python
@autodoc
def example_function(param1: int, param2: str) -> None:
    """Пример функции.

    Args:
        param1 (int): Первое значение.
        param2 (str): Второе значение.
    """
    print(f"Processing {param1} and {param2}")
```

### `update_docstring`

```python
def update_docstring(func):
    """Обновляет docstring функции."""
    ...
```

**Назначение**:
Функция `update_docstring` обновляет docstring функции, добавляя информацию о времени последнего вызова.

**Параметры**:
- `func` (function): Функция, docstring которой необходимо обновить.

**Возвращает**:
- `None`

**Как работает функция**:
1. Функция принимает функцию `func` в качестве аргумента.
2. Она получает текущее время в формате "год-месяц-день часы:минуты:секунды".
3. Проверяется, существует ли docstring у функции `func`.
4. Если docstring существует, к нему добавляется информация о времени последнего вызова.
5. Если docstring не существует, он создается и устанавливается равным информации о времени последнего вызова.

**Примеры**:

```python
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

## Пример использования

```python
from dev_utils.autodoc import autodoc

@autodoc
def example_function(param1: int, param2: str) -> None:
    """Пример функции.

    Args:
        param1 (int): Первое значение.
        param2 (str): Второе значение.
    """
    print(f"Processing {param1} and {param2}")

# Тестирование функции
example_function(1, "test")
print(example_function.__doc__)  # Вывод обновленного docstring
example_function(2, "another test")
print(example_function.__doc__)  # Вывод обновленного docstring