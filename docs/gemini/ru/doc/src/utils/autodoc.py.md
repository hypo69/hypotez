# Модуль `src.utils.autodoc`

## Обзор

Модуль `src.utils.autodoc` содержит декоратор `autodoc`, который обновляет строку документации функции с добавлением времени последнего вызова функции. Декоратор используется для того, чтобы автоматически обновлять docstring функции при её вызове.

## Подробнее

Декоратор `autodoc` оборачивает функцию, обновляя её docstring перед вызовом, добавляя в него строку с текущим временем. Для получения текущего времени используется библиотека `time`.

## Классы

### `autodoc`

**Описание**: Декоратор для автоматического обновления docstring функции.

**Наследует**: 
    - `functools.wraps`

**Атрибуты**: 
    - `func`: Функция, для которой будет обновляться docstring.

**Методы**: 
    - `wrapper`: Внутренняя функция, которая вызывается вместо исходной функции. Обновляет docstring перед вызовом исходной функции.

## Функции

### `update_docstring`

**Назначение**: Обновляет docstring функции.

**Параметры**:
    - `func`: Функция, для которой будет обновляться docstring.

**Возвращает**:
    - `None`

**Вызывает исключения**:
    - `None`

**Как работает функция**:
    - Функция `update_docstring` обновляет docstring функции, добавляя в него информацию о времени последнего вызова.
    - Сначала функция извлекает текущее время с помощью `time.strftime("%Y-%m-%d %H:%M:%S")`.
    - Затем проверяется, существует ли уже docstring у функции.
    - Если docstring существует, то к нему добавляется информация о времени последнего вызова.
    - Если docstring не существует, то создается новый docstring, содержащий только информацию о времени последнего вызова.

**Примеры**:
    ```python
    def example_function(param1: int, param2: str) -> None:
        """Пример функции."""
        print(f"Processing {param1} and {param2}")

    # Вызываем функцию `update_docstring` для обновления docstring функции `example_function`
    update_docstring(example_function)

    # Выводим обновленный docstring
    print(example_function.__doc__)
    ```

### `example_function`

**Назначение**: Пример функции, которая использует декоратор `autodoc`.

**Параметры**:
    - `param1`: Первое значение.
    - `param2`: Второе значение.

**Возвращает**:
    - `None`

**Вызывает исключения**:
    - `None`

**Как работает функция**:
    - Функция `example_function` просто выводит на печать строку с использованием переданных параметров.
    - Декоратор `autodoc` автоматически обновляет docstring функции перед каждым вызовом.

**Примеры**:
    ```python
    # Вызываем функцию `example_function` с разными параметрами.
    example_function(1, "test")
    example_function(2, "another test")

    # Выводим обновленный docstring функции `example_function`
    print(example_function.__doc__)
    ```