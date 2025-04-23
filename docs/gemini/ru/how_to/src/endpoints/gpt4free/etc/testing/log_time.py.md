### **Инструкция по использованию блока кода**

=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет три функции (`log_time_async`, `log_time_yield`, `log_time`), предназначенные для измерения времени выполнения других функций (методов). Каждая функция принимает метод и его аргументы, измеряет время выполнения метода и возвращает результат работы метода вместе с информацией о времени выполнения.

Шаги выполнения
-------------------------
1. **`log_time_async(method: callable, **kwargs)`**:
   - Функция принимает асинхронный метод (`method`) и произвольные аргументы (`**kwargs`).
   - Измеряет время начала выполнения метода (`start = time()`).
   - Вызывает асинхронный метод с переданными аргументами (`result = await method(**kwargs)`).
   - Вычисляет время выполнения в секундах (`secs = f"{round(time() - start, 2)} secs"`).
   - Возвращает результат выполнения метода, объединенный со временем выполнения, или только время выполнения, если результат отсутствует.

2. **`log_time_yield(method: callable, **kwargs)`**:
   - Функция принимает метод-генератор (`method`) и произвольные аргументы (`**kwargs`).
   - Измеряет время начала выполнения метода (`start = time()`).
   - Запускает метод-генератор с использованием `yield from` (`result = yield from method(**kwargs)`).
   - Возвращает отформатированную строку с временем выполнения.

3. **`log_time(method: callable, **kwargs)`**:
   - Функция принимает синхронный метод (`method`) и произвольные аргументы (`**kwargs`).
   - Измеряет время начала выполнения метода (`start = time()`).
   - Вызывает синхронный метод с переданными аргументами (`result = method(**kwargs)`).
   - Вычисляет время выполнения в секундах (`secs = f"{round(time() - start, 2)} secs"`).
   - Возвращает результат выполнения метода, объединенный со временем выполнения, или только время выполнения, если результат отсутствует.

Пример использования
-------------------------

```python
import asyncio
from time import sleep

from src.endpoints.gpt4free.etc.testing.log_time import log_time_async, log_time


async def my_async_method(param: str) -> str:
    """
    Асинхронный метод, который возвращает параметр с добавлением строки.
    Args:
        param: str
    Returns:
        str
    """
    await asyncio.sleep(1)  # Имитация асинхронной операции
    return f"Async result: {param}"


def my_sync_method(param: str) -> str:
    """
    Синхронный метод, который возвращает параметр с добавлением строки.
    Args:
        param: str
    Returns:
        str
    """
    sleep(1)  # Имитация синхронной операции
    return f"Sync result: {param}"


async def main():
    """
    Основная функция для демонстрации работы функций измерения времени.
    """
    async_result = await log_time_async(my_async_method, param="test_async")
    print(async_result)  # Вывод: Async result: test_async X.XX secs

    sync_result = log_time(my_sync_method, param="test_sync")
    print(sync_result)  # Вывод: Sync result: test_sync X.XX secs


if __name__ == "__main__":
    asyncio.run(main())
```