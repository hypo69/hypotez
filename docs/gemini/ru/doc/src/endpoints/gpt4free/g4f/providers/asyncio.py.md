# Модуль для работы с асинхронными операциями в g4f.providers
==========================================================

Модуль содержит функции для асинхронного выполнения кода, обработки асинхронных генераторов и итераторов,
а также для обеспечения совместимости с `nest_asyncio` и `uvloop`.

## Оглавление

- [Обзор](#обзор)
- [Подробнее](#подробнее)
- [Функции](#функции)
    - [`get_running_loop`](#get_running_loop)
    - [`await_callback`](#await_callback)
    - [`async_generator_to_list`](#async_generator_to_list)
    - [`to_sync_generator`](#to_sync_generator)
    - [`to_async_iterator`](#to_async_iterator)

## Обзор

Данный модуль предоставляет набор утилит для работы с асинхронным кодом, облегчая интеграцию с различными
асинхронными библиотеками и фреймворками. Он также обеспечивает обработку асинхронных генераторов и итераторов,
что позволяет эффективно использовать асинхронные потоки данных.

## Подробнее

Модуль предназначен для решения следующих задач:

- Получение текущего event loop с учетом совместимости с `nest_asyncio` и `uvloop`.
- Преобразование асинхронных генераторов в списки.
- Преобразование асинхронных генераторов в синхронные генераторы.
- Преобразование синхронных и асинхронных итераторов в асинхронные итераторы.

В проекте `hypotez` модуль используется для обеспечения асинхронного выполнения операций, таких как запросы к API и обработка данных,
что позволяет повысить производительность и отзывчивость системы.

## Функции

### `get_running_loop`

```python
def get_running_loop(check_nested: bool) -> Optional[AbstractEventLoop]:
    """
    Возвращает текущий event loop, применяя патч nest_asyncio при необходимости.

    Args:
        check_nested (bool): Флаг, указывающий, следует ли проверять необходимость установки nest_asyncio.

    Returns:
        Optional[AbstractEventLoop]: Текущий event loop или None, если event loop не запущен.

    Raises:
        NestAsyncioError: Если nest_asyncio не установлен и требуется.

    Как работает функция:
    - Пытается получить текущий event loop с помощью asyncio.get_running_loop().
    - Если обнаружен uvloop, возвращает его без изменений.
    - Если nest_asyncio еще не применен к event loop, применяет его, если он установлен.
    - Если nest_asyncio не установлен и требуется, вызывает исключение NestAsyncioError.

    Примеры:
        >>> loop = get_running_loop(check_nested=True)
        >>> if loop:
        ...     print("Event loop получен")
        Event loop получен
    """
    ...
```

### `await_callback`

```python
async def await_callback(callback: Callable):
    """
    Асинхронно ожидает выполнения переданной функции обратного вызова.

    Args:
        callback (Callable): Функция обратного вызова для асинхронного выполнения.

    Returns:
        Any: Результат выполнения функции обратного вызова.

    Как работает функция:
    - Асинхронно вызывает переданную функцию обратного вызова и возвращает результат.

    Примеры:
        >>> async def my_callback():
        ...     return "Hello, world!"
        >>> result = asyncio.run(await_callback(my_callback))
        >>> print(result)
        Hello, world!
    """
    ...
```

### `async_generator_to_list`

```python
async def async_generator_to_list(generator: AsyncIterator) -> list:
    """
    Преобразует асинхронный генератор в список.

    Args:
        generator (AsyncIterator): Асинхронный генератор.

    Returns:
        list: Список, содержащий все элементы, сгенерированные асинхронным генератором.

    Как работает функция:
    - Итерируется по асинхронному генератору и собирает все элементы в список.

    Примеры:
        >>> async def my_generator():
        ...     yield 1
        ...     yield 2
        ...     yield 3
        >>> result = asyncio.run(async_generator_to_list(my_generator()))
        >>> print(result)
        [1, 2, 3]
    """
    ...
```

### `to_sync_generator`

```python
def to_sync_generator(generator: AsyncIterator, stream: bool = True) -> Iterator:
    """
    Преобразует асинхронный генератор в синхронный генератор.

    Args:
        generator (AsyncIterator): Асинхронный генератор.
        stream (bool): Флаг, определяющий, следует ли использовать потоковый режим.

    Returns:
        Iterator: Синхронный генератор, возвращающий элементы из асинхронного генератора.

    Как работает функция:
    - Получает текущий event loop или создает новый, если его нет.
    - Если stream=False, преобразует асинхронный генератор в список и возвращает элементы списка через синхронный генератор.
    - Если stream=True, итерируется по асинхронному генератору и возвращает элементы через синхронный генератор, используя loop.run_until_complete().
    - Корректно закрывает event loop после завершения работы.

    Примеры:
        >>> async def my_generator():
        ...     yield 1
        ...     yield 2
        ...     yield 3
        >>> sync_generator = to_sync_generator(my_generator())
        >>> for item in sync_generator:
        ...     print(item)
        1
        2
        3
    """
    ...
```

### `to_async_iterator`

```python
async def to_async_iterator(iterator) -> AsyncIterator:
    """
    Преобразует синхронный или асинхронный итератор в асинхронный итератор.

    Args:
        iterator: Синхронный или асинхронный итератор.

    Returns:
        AsyncIterator: Асинхронный итератор, возвращающий элементы из исходного итератора.

    Как работает функция:
    - Проверяет, является ли итератор асинхронным. Если да, то просто возвращает его элементы.
    - Если итератор является корутиной, ожидает ее выполнения и возвращает результат.
    - Если итератор синхронный, преобразует его в асинхронный, итерируясь по его элементам.

    Примеры:
        >>> async def my_async_generator():
        ...     yield 1
        ...     yield 2
        ...     yield 3
        >>> async_iterator = to_async_iterator(my_async_generator())
        >>> async for item in async_iterator:
        ...     print(item)
        1
        2
        3
    """
    ...