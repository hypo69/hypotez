# Модуль log_time

## Обзор

Модуль `log_time` предоставляет набор функций для измерения и логирования времени выполнения других функций. 

## Подробней

Модуль содержит три функции: `log_time_async`, `log_time_yield`, и `log_time`. Каждая функция принимает в качестве аргумента вызываемую функцию (`method`) и произвольные ключевые аргументы, которые передаются в вызываемую функцию. 

Функции `log_time_async` и `log_time_yield` предназначены для асинхронных функций и функций, которые используют генераторы соответственно. Они возвращают результат выполнения вызываемой функции вместе с временем выполнения, измеренным в секундах с точностью до двух знаков после запятой. 

Функция `log_time` предназначена для синхронных функций. Она возвращает результат выполнения вызываемой функции, если результат не равен `None`, иначе возвращает только время выполнения.

##  Функции

### `log_time_async`

```python
async def log_time_async(method: callable, **kwargs):
    """
    Асинхронная функция для измерения и логирования времени выполнения.

    Args:
        method (callable): Вызываемая функция.
        **kwargs: Ключевые аргументы, передаваемые в вызываемую функцию.

    Returns:
        str: Результат выполнения вызываемой функции и время выполнения, измеренное в секундах. 

    Example:
        >>> async def my_async_function(param1: str, param2: int) -> str:
        ...     return f"Async result: {param1}, {param2}"
        >>> result = await log_time_async(my_async_function, param1="test", param2=10)
        >>> print(result)
        Async result: test, 10 0.01 secs 
    """
    start = time()
    result = await method(**kwargs)
    secs = f"{round(time() - start, 2)} secs"
    return " ".join([result, secs]) if result else secs
```
### `log_time_yield`

```python
def log_time_yield(method: callable, **kwargs):
    """
    Функция для измерения и логирования времени выполнения функции, использующей генератор.

    Args:
        method (callable): Вызываемая функция, использующая генератор.
        **kwargs: Ключевые аргументы, передаваемые в вызываемую функцию.

    Returns:
        Generator[str, None, None]: Генератор, который возвращает результат выполнения вызываемой функции и время выполнения.

    Example:
        >>> def my_generator_function(param1: str, param2: int) -> Generator[str, None, None]:
        ...     yield f"Yield result: {param1}, {param2}"
        >>> for result in log_time_yield(my_generator_function, param1="test", param2=10):
        ...     print(result)
        Yield result: test, 10
         0.01 secs
    """
    start = time()
    result = yield from method(**kwargs)
    yield f" {round(time() - start, 2)} secs"
```

### `log_time`

```python
def log_time(method: callable, **kwargs):
    """
    Функция для измерения и логирования времени выполнения.

    Args:
        method (callable): Вызываемая функция.
        **kwargs: Ключевые аргументы, передаваемые в вызываемую функцию.

    Returns:
        str: Результат выполнения вызываемой функции и время выполнения, измеренное в секундах.

    Example:
        >>> def my_function(param1: str, param2: int) -> str:
        ...     return f"Result: {param1}, {param2}"
        >>> result = log_time(my_function, param1="test", param2=10)
        >>> print(result)
        Result: test, 10 0.01 secs
    """
    start = time()
    result = method(**kwargs)
    secs = f"{round(time() - start, 2)} secs"
    return " ".join([result, secs]) if result else secs