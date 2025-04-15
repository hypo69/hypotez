### **Анализ кода модуля `log_time`**

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Функциональность модуля четко определена: измерение времени выполнения функций.
    - Использование `time()` для измерения времени.
- **Минусы**:
    - Отсутствует документация в формате docstring для функций.
    - Не указаны типы параметров и возвращаемых значений в аннотациях.
    - Отсутствует обработка исключений.
    - Не используется модуль `logger` для логирования.

**Рекомендации по улучшению**:

1.  **Добавить Docstring:** Добавить docstring для каждой функции, чтобы описать ее назначение, параметры и возвращаемые значения.
2.  **Добавить аннотации типов:** Добавить аннотации типов для параметров и возвращаемых значений функций.
3.  **Использовать `logger`**: Заменить `print` на `logger.info` для логирования времени выполнения.
4.  **Обработка исключений**: Добавить обработку исключений с использованием `try-except` блоков и логировать ошибки через `logger.error`.
5.  **Улучшить форматирование**: Привести код в соответствие со стандартами PEP8.
6.  **Удалить неиспользуемые импорты**: Проверить и удалить неиспользуемые импорты.
7.  **Изменить способ форматирования**: Изменить способ форматирования времени выполнения, чтобы он был более читаемым и информативным.

**Оптимизированный код**:

```python
from time import time
from typing import Callable, Any
from src.logger import logger


async def log_time_async(method: Callable, **kwargs: Any) -> str | None:
    """
    Измеряет время выполнения асинхронной функции и логирует результат.

    Args:
        method (Callable): Асинхронная функция, время выполнения которой необходимо измерить.
        **kwargs (Any): Произвольные аргументы, передаваемые в функцию.

    Returns:
        str | None: Результат выполнения функции, объединенный со временем выполнения,
                    или только время выполнения, если результат отсутствует.
    
    Raises:
        Exception: Если во время выполнения функции возникает исключение.

    Example:
        >>> async def my_async_function():
        ...     await asyncio.sleep(1)
        ...     return "Async done"
        >>> result = await log_time_async(my_async_function)
        >>> print(result)
        'Async done 1.01 secs'
    """
    start = time()
    try:
        result = await method(**kwargs)
    except Exception as ex:
        logger.error(f"Ошибка при выполнении асинхронной функции {method.__name__}", ex, exc_info=True)
        return None
    secs = f"{round(time() - start, 2)} secs"
    message = f"Асинхронная функция {method.__name__} выполнена за {secs}"
    logger.info(message)
    return " ".join([result, secs]) if result else secs


def log_time_yield(method: Callable, **kwargs: Any):
    """
    Измеряет время выполнения функции-генератора и логирует результат.

    Args:
        method (Callable): Функция-генератор, время выполнения которой необходимо измерить.
        **kwargs (Any): Произвольные аргументы, передаваемые в функцию.

    Yields:
        Any: Значения, генерируемые функцией-генератором.

    Raises:
        Exception: Если во время выполнения функции возникает исключение.

    Example:
        >>> def my_generator_function():
        ...     yield "Yield 1"
        ...     yield "Yield 2"
        >>> for result in log_time_yield(my_generator_function):
        ...     print(result)
        'Yield 1'
        'Yield 2'
        ' 0.0 secs'
    """
    start = time()
    try:
        result = yield from method(**kwargs)
    except Exception as ex:
        logger.error(f"Ошибка при выполнении функции-генератора {method.__name__}", ex, exc_info=True)
        yield None
    secs = f" {round(time() - start, 2)} secs"
    message = f"Функция-генератор {method.__name__} выполнена за {secs}"
    logger.info(message)
    yield secs


def log_time(method: Callable, **kwargs: Any) -> str | None:
    """
    Измеряет время выполнения обычной функции и логирует результат.

    Args:
        method (Callable): Обычная функция, время выполнения которой необходимо измерить.
        **kwargs (Any): Произвольные аргументы, передаваемые в функцию.

    Returns:
        str | None: Результат выполнения функции, объединенный со временем выполнения,
                    или только время выполнения, если результат отсутствует.
    
    Raises:
        Exception: Если во время выполнения функции возникает исключение.

    Example:
        >>> def my_function():
        ...     return "Done"
        >>> result = log_time(my_function)
        >>> print(result)
        'Done 0.0 secs'
    """
    start = time()
    try:
        result = method(**kwargs)
    except Exception as ex:
        logger.error(f"Ошибка при выполнении функции {method.__name__}", ex, exc_info=True)
        return None
    secs = f"{round(time() - start, 2)} secs"
    message = f"Функция {method.__name__} выполнена за {secs}"
    logger.info(message)
    return " ".join([result, secs]) if result else secs