# Модуль `asyncio.py`

## Обзор

Модуль предоставляет асинхронные утилиты и функции для работы с асинхронным кодом, включая обработку событийных циклов, асинхронных генераторов и итераторов. Он также включает в себя исправления для определенных проблем, таких как `RuntimeError: async generator ignored GeneratorExit`.

## Подробней

Этот модуль содержит функции для получения запущенного цикла событий, преобразования асинхронных генераторов в синхронные и наоборот, а также для обработки исключений, связанных с асинхронными генераторами. Он также учитывает наличие или отсутствие библиотек `nest_asyncio` и `uvloop` для оптимизации работы с асинхронным кодом.

## Функции

### `get_running_loop`

```python
def get_running_loop(check_nested: bool) -> Optional[AbstractEventLoop]:
    """ Функция получает текущий работающий цикл событий.

    Args:
        check_nested (bool): Флаг, указывающий, нужно ли проверять поддержку вложенных циклов событий.

    Returns:
        Optional[AbstractEventLoop]: Возвращает текущий работающий цикл событий, если он есть. В противном случае возвращает `None`.

    Raises:
        NestAsyncioError: Если `check_nested` равен `True` и библиотека `nest_asyncio` не установлена.

    
    - Пытается получить текущий работающий цикл событий с помощью `asyncio.get_running_loop()`.
    - Если цикл работает на базе `uvloop`, он возвращается без изменений.
    - Если `nest_asyncio` установлен, применяет патч к циклу для поддержки вложенности.
    - Если `nest_asyncio` не установлен и `check_nested` равен `True`, вызывает исключение `NestAsyncioError`.
    """
```

### `await_callback`

```python
async def await_callback(callback: Callable):
    """ Асинхронно ожидает выполнения переданной функции обратного вызова.

    Args:
        callback (Callable): Функция обратного вызова, которую нужно выполнить.

    Returns:
        await callback(): Результат выполнения функции обратного вызова.

    
    - Функция принимает функцию обратного вызова в качестве аргумента.
    - Использует `await` для асинхронного выполнения этой функции.
    - Возвращает результат выполнения функции обратного вызова.
    """
```

### `async_generator_to_list`

```python
async def async_generator_to_list(generator: AsyncIterator) -> list:
    """ Преобразует асинхронный генератор в список.

    Args:
        generator (AsyncIterator): Асинхронный генератор, который нужно преобразовать.

    Returns:
        list: Список, содержащий все элементы, сгенерированные асинхронным генератором.

    
    - Использует асинхронное включение списка для итерации по асинхронному генератору.
    - Собирает все элементы, сгенерированные генератором, в список.
    - Возвращает полученный список.
    """
```

### `to_sync_generator`

```python
def to_sync_generator(generator: AsyncIterator, stream: bool = True) -> Iterator:
    """ Преобразует асинхронный генератор в синхронный генератор.

    Args:
        generator (AsyncIterator): Асинхронный генератор, который нужно преобразовать.
        stream (bool, optional): Флаг, определяющий, нужно ли использовать потоковый режим. По умолчанию `True`.

    Returns:
        Iterator: Синхронный генератор, выдающий элементы из асинхронного генератора.

    
    - Проверяет, запущен ли цикл событий. Если нет, создает новый цикл событий.
    - Если `stream` равен `False`, запускает асинхронный генератор до завершения и возвращает все элементы в виде списка.
    - Если `stream` равен `True`, преобразует каждый элемент асинхронного генератора в синхронный, используя `loop.run_until_complete`.
    - В конце закрывает цикл событий, если он был создан внутри функции.

    Внутренние функции:

    """
    loop = get_running_loop(check_nested=False)
    if not stream:
        yield from asyncio.run(async_generator_to_list(generator))
        return
    new_loop = False
    if loop is None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        new_loop = True
    gen = generator.__aiter__()
    try:
        while True:
            yield loop.run_until_complete(await_callback(gen.__anext__))
    except StopAsyncIteration:
        pass
    finally:
        if new_loop:
            try:
                runners._cancel_all_tasks(loop)
                loop.run_until_complete(loop.shutdown_asyncgens())
                if hasattr(loop, "shutdown_default_executor"):
                    loop.run_until_complete(loop.shutdown_default_executor())
            finally:
                asyncio.set_event_loop(None)
                loop.close()
```

### `to_async_iterator`

```python
async def to_async_iterator(iterator) -> AsyncIterator:
    """ Преобразует синхронный итератор или асинхронный итерируемый объект в асинхронный итератор.

    Args:
        iterator: Синхронный итератор или асинхронный итерируемый объект, который нужно преобразовать.

    Returns:
        AsyncIterator: Асинхронный итератор, выдающий элементы из исходного итератора.

    
    - Проверяет, является ли входной итератор асинхронным итерируемым объектом (имеет метод `__aiter__`).
    - Если да, то асинхронно перебирает элементы и выдает их.
    - Если входной итератор является корутиной, то ожидает ее выполнения и выдает результат.
    - В противном случае, перебирает элементы синхронно и выдает их.
    """
```