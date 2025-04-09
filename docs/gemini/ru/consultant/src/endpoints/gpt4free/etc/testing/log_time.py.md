### **Анализ кода модуля `log_time.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код выполняет полезную функцию измерения времени выполнения переданных методов.
    - Присутствуют асинхронные и синхронные варианты функций.
- **Минусы**:
    - Отсутствует документация (docstrings) для функций.
    - Нет обработки исключений.
    - Не используется модуль `logger` для логирования времени выполнения.
    - Нет аннотаций типов для параметров и возвращаемых значений.

**Рекомендации по улучшению:**

1.  **Добавить docstrings**: Добавить подробные docstrings для каждой функции, описывающие её назначение, параметры, возвращаемое значение и возможные исключения.
2.  **Обработка исключений**: Добавить блоки `try...except` для обработки возможных исключений, которые могут возникнуть при выполнении переданных методов.
3.  **Использовать `logger`**: Использовать модуль `logger` для логирования времени выполнения методов.
4.  **Аннотации типов**: Добавить аннотации типов для параметров и возвращаемых значений функций.
5.  **Улучшить форматирование**: Использовать `f-strings` для более читаемого форматирования времени выполнения.
6. **Соблюдать PEP8**: Проверить код на соответствие стандартам PEP8.
7. **Удалить не используемые импорты**: Если импорт `time` не используется напрямую в коде, его можно удалить. В данном случае он используется и удалять не нужно

**Оптимизированный код:**

```python
from time import time
from typing import Callable, Any
from src.logger import logger


async def log_time_async(method: Callable[..., Any], **kwargs: Any) -> str | None:
    """
    Измеряет время выполнения асинхронного метода и возвращает результат вместе со временем выполнения.

    Args:
        method (Callable[..., Any]): Асинхронный метод для измерения времени выполнения.
        **kwargs (Any): Произвольные аргументы, передаваемые в метод.

    Returns:
        str | None: Результат выполнения метода, объединенный со временем выполнения в секундах, или только время, если результат равен None.

    Raises:
        Exception: Если во время выполнения метода происходит исключение, оно логируется.

    Example:
        >>> async def my_async_method():
        ...     await asyncio.sleep(1)
        ...     return "Async done"
        >>> result = await log_time_async(my_async_method)
        >>> print(result)
        Async done 1.01 secs
    """
    start = time()
    try:
        result = await method(**kwargs)
    except Exception as ex:
        logger.error(f'Error while executing async method {method.__name__}', ex, exc_info=True)
        return None
    secs = f"{round(time() - start, 2)} secs"
    log_message = f"Async method {method.__name__} executed in {secs}"
    logger.info(log_message)
    return " ".join([result, secs]) if result else secs


def log_time_yield(method: Callable[..., Any], **kwargs: Any):
    """
    Измеряет время выполнения метода-генератора и возвращает результат вместе со временем выполнения.

    Args:
        method (Callable[..., Any]): Метод-генератор для измерения времени выполнения.
        **kwargs (Any): Произвольные аргументы, передаваемые в метод.

    Yields:
        Any: Значения, генерируемые методом, и время выполнения в конце.

    Raises:
        Exception: Если во время выполнения метода происходит исключение, оно логируется.

    Example:
        >>> def my_generator_method():
        ...     yield "Yield 1"
        ...     yield "Yield 2"
        >>> for result in log_time_yield(my_generator_method):
        ...     print(result)
        Yield 1
        Yield 2
         0.0 secs
    """
    start = time()
    try:
        result = yield from method(**kwargs)
    except Exception as ex:
        logger.error(f'Error while executing generator method {method.__name__}', ex, exc_info=True)
        yield None
    secs = f"{round(time() - start, 2)} secs"
    log_message = f"Generator method {method.__name__} executed in {secs}"
    logger.info(log_message)
    yield f" {secs}"


def log_time(method: Callable[..., Any], **kwargs: Any) -> str | None:
    """
    Измеряет время выполнения синхронного метода и возвращает результат вместе со временем выполнения.

    Args:
        method (Callable[..., Any]): Синхронный метод для измерения времени выполнения.
        **kwargs (Any): Произвольные аргументы, передаваемые в метод.

    Returns:
        str | None: Результат выполнения метода, объединенный со временем выполнения в секундах, или только время, если результат равен None.

    Raises:
        Exception: Если во время выполнения метода происходит исключение, оно логируется.

    Example:
        >>> def my_sync_method():
        ...     return "Sync done"
        >>> result = log_time(my_sync_method)
        >>> print(result)
        Sync done 0.0 secs
    """
    start = time()
    try:
        result = method(**kwargs)
    except Exception as ex:
        logger.error(f'Error while executing method {method.__name__}', ex, exc_info=True)
        return None
    secs = f"{round(time() - start, 2)} secs"
    log_message = f"Method {method.__name__} executed in {secs}"
    logger.info(log_message)
    return " ".join([str(result), secs]) if result else secs