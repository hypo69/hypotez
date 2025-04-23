# Модуль asyncio

## Обзор

Модуль предоставляет асинхронные утилиты и функции для работы с асинхронным кодом в проекте `hypotez`.
Он включает в себя функции для получения текущего event loop, обработки асинхронных генераторов,
а также преобразования синхронных итераторов в асинхронные.

## Подробнее

Этот модуль содержит функции, которые помогают решать проблемы совместимости и управления асинхронными задачами,
особенно в тех случаях, когда требуется интеграция с синхронным кодом или использование вложенных асинхронных операций.
Код обрабатывает ситуации, когда `nest_asyncio` или `uvloop` установлены или отсутствуют,
а также обеспечивает корректное завершение асинхронных генераторов и event loop.

## Функции

### `get_running_loop`

```python
def get_running_loop(check_nested: bool) -> Optional[AbstractEventLoop]:
    """
    Возвращает текущий event loop, применяя патч nest_asyncio при необходимости.

    Args:
        check_nested (bool): Флаг, указывающий, следует ли проверять необходимость применения nest_asyncio.

    Returns:
        Optional[AbstractEventLoop]: Текущий event loop или None, если event loop не запущен.

    Raises:
        NestAsyncioError: Если `check_nested` равен True и nest_asyncio не установлен.

    Как работает функция:
    - Пытается получить текущий event loop с помощью `asyncio.get_running_loop()`.
    - Если `uvloop` установлен и текущий event loop является экземпляром `uvloop.Loop`, возвращает его без изменений.
    - Проверяет, был ли уже применен патч `nest_asyncio` к текущему event loop.
    - Если `nest_asyncio` не был применен и `check_nested` равен True, пытается применить патч `nest_asyncio`.
    - Если `nest_asyncio` не установлен и `check_nested` равен True, вызывает исключение `NestAsyncioError`.
    - Если event loop не запущен, возвращает None.

    Примеры:
    >>> loop = get_running_loop(check_nested=True)
    >>> if loop:
    ...     print("Event loop получен")
    """
```

### `await_callback`

```python
async def await_callback(callback: Callable):
    """
    Асинхронно ожидает выполнения callback-функции.

    Args:
        callback (Callable): Асинхронная функция, которую нужно выполнить.

    Returns:
        Any: Результат выполнения callback-функции.

    Как работает функция:
    - Асинхронно вызывает предоставленную callback-функцию и возвращает результат.

    Примеры:
    >>> async def my_callback():
    ...     return "Hello, world!"
    >>> result = asyncio.run(await_callback(my_callback))
    >>> print(result)
    """
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
    - Итерируется по асинхронному генератору и собирает все элементы в список.

    Примеры:
    >>> async def my_generator():
    ...     for i in range(3):
    ...         yield i
    >>> result = asyncio.run(async_generator_to_list(my_generator()))
    >>> print(result)
    """
```

### `to_sync_generator`

```python
def to_sync_generator(generator: AsyncIterator, stream: bool = True) -> Iterator:
    """
    Преобразует асинхронный генератор в синхронный генератор.

    Args:
        generator (AsyncIterator): Асинхронный генератор.
        stream (bool, optional): Флаг, указывающий, следует ли использовать потоковую передачу. Defaults to True.

    Returns:
        Iterator: Синхронный генератор, выдающий элементы из асинхронного генератора.

    Как работает функция:
    - Получает текущий event loop или создает новый, если текущего нет.
    - Если `stream` равен False, собирает все элементы из асинхронного генератора в список и возвращает их.
    - Если `stream` равен True, итерируется по асинхронному генератору и возвращает элементы по одному, используя `loop.run_until_complete()`.
    - Корректно завершает event loop после завершения работы.

    Примеры:
    >>> async def my_async_generator():
    ...     for i in range(3):
    ...         yield i
    >>> sync_generator = to_sync_generator(my_async_generator())
    >>> for item in sync_generator:
    ...     print(item)
    """
```

### `to_async_iterator`

```python
async def to_async_iterator(iterator) -> AsyncIterator:
    """
    Преобразует синхронный итератор в асинхронный итератор.

    Args:
        iterator: Синхронный итератор.

    Returns:
        AsyncIterator: Асинхронный итератор, выдающий элементы из синхронного итератора.

    Как работает функция:
    - Проверяет, является ли входной итератор асинхронным итератором или корутиной.
    - Если это асинхронный итератор, итерируется по нему и возвращает элементы.
    - Если это корутина, ожидает ее выполнения и возвращает результат.
    - Если это синхронный итератор, итерируется по нему и возвращает элементы.

    Примеры:
    >>> async def main():
    ...     my_list = [1, 2, 3]
    ...     async_iterator = to_async_iterator(my_list)
    ...     async for item in async_iterator:
    ...         print(item)
    >>> asyncio.run(main())
    """