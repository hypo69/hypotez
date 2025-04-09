# Модуль для работы с асинхронностью и совместимостью с nest_asyncio

## Обзор

Этот модуль предоставляет набор утилит для работы с асинхронностью в Python, включая функции для получения текущего event loop, обработки асинхронных генераторов и преобразования синхронных итераторов в асинхронные. Он также включает в себя обработку ошибок, связанных с вложенными event loop (nest_asyncio).

## Подробней

Модуль предназначен для обеспечения совместимости и удобства работы с асинхронным кодом в различных средах, особенно там, где требуется обработка вложенных event loop или преобразование между синхронными и асинхронными итераторами. Он также обрабатывает специфические ошибки и обеспечивает корректное завершение event loop.

## Функции

### `get_running_loop`

```python
def get_running_loop(check_nested: bool) -> Optional[AbstractEventLoop]:
    """
    Получает текущий работающий event loop. Если loop отсутствует, возвращает None.

    Args:
        check_nested (bool): Флаг, указывающий, нужно ли проверять поддержку nest_asyncio.

    Returns:
        Optional[AbstractEventLoop]: Текущий работающий event loop или None.

    Raises:
        NestAsyncioError: Если nest_asyncio не установлен и требуется проверка вложенности.

    Как работает функция:
    1. Пытается получить текущий event loop с помощью `asyncio.get_running_loop()`.
    2. Если loop существует и используется `uvloop`, проверяет, является ли loop экземпляром `uvloop.Loop`. Если да, возвращает его.
    3. Если loop не был пропатчен `nest_asyncio`, применяет патч, если `has_nest_asyncio` равен `True`. Если `has_nest_asyncio` равен `False` и `check_nested` равен `True`, поднимает исключение `NestAsyncioError`.
    4. Если исключение `RuntimeError` перехвачено (т.е. loop не существует), функция возвращает `None`.

    Схема работы функции:
    A: Попытка получить текущий event loop
    ↓
    B: Проверка на uvloop
    ├── Да: Возврат uvloop loop
    └── Нет: Проверка на nest_asyncio
        ├── Установлен: Применение патча nest_asyncio
        └── Не установлен: Выброс исключения NestAsyncioError (если check_nested)
    ↓
    C: Возврат текущего event loop
    ↓
    D: Если RuntimeError (loop не существует): Возврат None

    Примеры:
    >>> loop = get_running_loop(check_nested=True)
    >>> if loop:
    ...     print("Event loop найден")
    ... else:
    ...     print("Event loop не найден")
    """
    ...
```

### `await_callback`

```python
async def await_callback(callback: Callable):
    """
    Асинхронно ожидает выполнения переданной callback-функции.

    Args:
        callback (Callable): Асинхронная функция, которую необходимо выполнить.

    Returns:
        Any: Результат выполнения callback-функции.

    Как работает функция:
    1. Асинхронно вызывает переданную callback-функцию и возвращает результат.

    Схема работы функции:
    A: Вызов callback-функции
    ↓
    B: Возврат результата

    Примеры:
    >>> async def my_async_function():
    ...     return "Hello, async world!"
    >>> result = asyncio.run(await_callback(my_async_function))
    >>> print(result)
    Hello, async world!
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
        list: Список элементов, сгенерированных асинхронным генератором.

    Как работает функция:
    1. Собирает все элементы, генерируемые асинхронным генератором, в список.

    Схема работы функции:
    A: Итерация по асинхронному генератору
    ↓
    B: Сбор элементов в список
    ↓
    C: Возврат списка

    Примеры:
    >>> async def my_async_generator():
    ...     yield 1
    ...     yield 2
    ...     yield 3
    >>> result = asyncio.run(async_generator_to_list(my_async_generator()))
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
        stream (bool, optional): Если True, возвращает элементы по мере их генерации.
            Если False, сначала собирает все элементы в список, а затем возвращает их. По умолчанию True.

    Yields:
        Any: Элементы, генерируемые асинхронным генератором.

    Как работает функция:
    1. Получает текущий event loop с помощью `get_running_loop(check_nested=False)`.
    2. Если `stream` равен `False`, собирает все элементы асинхронного генератора в список с помощью `asyncio.run(async_generator_to_list(generator))` и возвращает их.
    3. Если loop не существует, создает новый event loop и устанавливает его как текущий.
    4. Итерируется по асинхронному генератору, вызывая `gen.__anext__()` внутри `loop.run_until_complete(await_callback(...))` для получения каждого элемента.
    5. В случае `StopAsyncIteration` выполняет очистку: отменяет все задачи, завершает асинхронные генераторы и закрывает loop (если он был создан).

    Схема работы функции:
    A: Получение текущего event loop
    ↓
    B: Проверка stream
    ├── True: Итерация по асинхронному генератору
    │   ├── Получение элемента с помощью loop.run_until_complete
    │   └── Возврат элемента
    └── False: Сбор всех элементов в список
        └── Возврат списка
    ↓
    C: Очистка (отмена задач, завершение генераторов, закрытие loop)

    Примеры:
    >>> async def my_async_generator():
    ...     yield 1
    ...     yield 2
    ...     yield 3
    >>> sync_generator = to_sync_generator(my_async_generator())
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
    Преобразует синхронный итератор или корутину в асинхронный итератор.

    Args:
        iterator: Синхронный итератор, асинхронный итератор или корутина.

    Yields:
        Any: Элементы итератора.

    Как работает функция:
    1. Проверяет, является ли `iterator` асинхронным итератором (`hasattr(iterator, '__aiter__')`).
    2. Если да, перебирает его элементы и возвращает каждый элемент.
    3. Если `iterator` является корутиной (`asyncio.iscoroutine(iterator)`), ожидает её выполнения и возвращает результат.
    4. Иначе перебирает элементы синхронного итератора и возвращает каждый элемент.

    Схема работы функции:
    A: Проверка на асинхронный итератор
    ├── Да: Итерация по асинхронному итератору
    │   └── Возврат элемента
    └── Нет: Проверка на корутину
        ├── Да: Ожидание корутины и возврат результата
        └── Нет: Итерация по синхронному итератору
            └── Возврат элемента

    Примеры:
    >>> async def my_async_generator():
    ...     yield 1
    ...     yield 2
    ...     yield 3
    >>> async def print_async_iterator(iterator):
    ...     async for item in iterator:
    ...         print(item)
    >>> asyncio.run(print_async_iterator(to_async_iterator(my_async_generator())))
    1
    2
    3
    """
    ...