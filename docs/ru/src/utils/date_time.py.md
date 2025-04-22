# Модуль для работы с датой и временем
## Обзор
Модуль `src.utils.date_time` предоставляет класс `TimeoutCheck` с функциональностью для проверки, находится ли текущее время в заданном интервале, с возможностью установки таймаута. Он полезен для задач, которые должны выполняться только в определенное время.

## Подробней

Модуль содержит класс `TimeoutCheck`, который включает методы для проверки попадания текущего времени в заданный интервал, а также для ожидания ввода пользователя с таймаутом. Это может быть полезно для выполнения операций, которые должны происходить только в определенные периоды времени (например, ночное обслуживание).

## Классы

### `TimeoutCheck`

**Описание**: Класс `TimeoutCheck` предназначен для проверки, находится ли текущее время в заданном интервале, с возможностью установки таймаута.

**Атрибуты**:
- `result` (bool | None): Результат проверки интервала времени.
- `user_input` (str | None): Ввод пользователя.

**Методы**:
- `__init__()`: Конструктор класса.
- `interval(start: time, end: time) -> bool`: Проверяет, находится ли текущее время в заданном интервале.
- `interval_with_timeout(timeout: int, start: time, end: time) -> bool`: Проверяет, находится ли текущее время в заданном интервале с учетом таймаута.
- `get_input() -> None`: Запрашивает ввод от пользователя.
- `input_with_timeout(timeout: int) -> str | None`: Ожидает ввод от пользователя с таймаутом.

#### `__init__`

```python
def __init__(self):
    """
    Конструктор класса TimeoutCheck.

    Инициализирует атрибуты result и user_input значением None.
    """
    self.result = None
    self.user_input = None
```
**Принцип работы**:
- Инициализирует атрибут `result` значением `None`.
- Инициализирует атрибут `user_input` значением `None`.

#### `interval`

```python
def interval(self, start: time = time(23, 0), end: time = time(6, 0)) -> bool:
    """ Проверяет, находится ли текущее время в заданном интервале.
    
    Args:
        start (time): Начало интервала (по умолчанию 23:00).
        end (time): Конец интервала (по умолчанию 06:00).

    Returns:
        bool: True, если текущее время находится в интервале, False в противном случае.
    """
    current_time = datetime.now().time()

    if start < end:
        # Интервал в пределах одного дня (например, с 08:00 до 17:00)
        self.result = start <= current_time <= end
    else:
        # Интервал, охватывающий полночь (например, с 23:00 до 06:00)
        self.result = current_time >= start or current_time <= end
```

**Назначение**: Проверяет, находится ли текущее время в указанном интервале.

**Параметры**:
- `start` (time): Начало интервала. По умолчанию `23:00`.
- `end` (time): Конец интервала. По умолчанию `06:00`.

**Возвращает**:
- `bool`: `True`, если текущее время находится в интервале, и `False` в противном случае.

**Как работает функция**:
- Функция получает текущее время с использованием `datetime.now().time()`.
- Если время начала интервала меньше времени окончания, то проверяется, находится ли текущее время между этими значениями.
- В противном случае (если интервал проходит через полночь), проверяется, находится ли текущее время после времени начала или до времени окончания.

**Примеры**:

```python
from datetime import time
timeout_check = TimeoutCheck()
# Пример 1: Проверка, находится ли текущее время между 23:00 и 06:00
result = timeout_check.interval()
print(result)

# Пример 2: Проверка, находится ли текущее время между 08:00 и 17:00
result = timeout_check.interval(start=time(8, 0), end=time(17, 0))
print(result)
```

#### `interval_with_timeout`

```python
def interval_with_timeout(self, timeout: int = 5, start: time = time(23, 0), end: time = time(6, 0)) -> bool:
    """ Проверяет, находится ли текущее время в заданном интервале с таймаутом.

    Args:
        timeout (int): Время в секундах для ожидания проверки интервала.
        start (time): Начало интервала (по умолчанию 23:00).
        end (time): Конец интервала (по умолчанию 06:00).

    Returns:
        bool: True, если текущее время находится в интервале и ответ получен в течение таймаута, False, если нет или произошел таймаут.
    """
    thread = threading.Thread(target=self.interval, args=(start, end))
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print(f"Timeout occurred after {timeout} seconds, continuing execution.")
        thread.join()  # Ensures thread stops after timeout
        return False  # Timeout occurred, so returning False
    return self.result
```

**Назначение**: Проверяет, находится ли текущее время в заданном интервале, с учетом таймаута.

**Параметры**:
- `timeout` (int): Время ожидания проверки интервала в секундах. По умолчанию `5`.
- `start` (time): Начало интервала. По умолчанию `23:00`.
- `end` (time): Конец интервала. По умолчанию `06:00`.

**Возвращает**:
- `bool`: `True`, если текущее время находится в интервале и ответ получен в течение таймаута, `False`, если нет или произошел таймаут.

**Как работает функция**:
- Функция создает и запускает поток для выполнения проверки интервала с использованием метода `self.interval`.
- Поток ожидает завершения в течение заданного времени таймаута.
- Если поток все еще активен после таймаута, это означает, что таймаут произошел, и функция возвращает `False`.
- Если поток завершился вовремя, функция возвращает результат проверки интервала, сохраненный в `self.result`.

**Примеры**:

```python
from datetime import time
import threading
timeout_check = TimeoutCheck()

# Пример 1: Проверка интервала с таймаутом 3 секунды
result = timeout_check.interval_with_timeout(timeout=3)
print(result)

# Пример 2: Проверка интервала с таймаутом 5 секунд и указанными границами интервала
result = timeout_check.interval_with_timeout(timeout=5, start=time(8, 0), end=time(17, 0))
print(result)
```

#### `get_input`

```python
def get_input(self):
    """ Запрашиваем ввод от пользователя."""
    self.user_input = input("U:> ")
```

**Назначение**: Запрашивает ввод от пользователя.

**Как работает функция**:
- Функция использует `input()` для получения ввода от пользователя и сохраняет его в атрибуте `self.user_input`.

#### `input_with_timeout`

```python
def input_with_timeout(self, timeout: int = 5) -> str | None:
    """ Ожидаем ввод с тайм-аутом.

    Args:
        timeout (int): Время ожидания ввода в секундах.

    Returns:
        str | None: Введенные данные или None, если был тайм-аут.
    """
    # Запускаем поток для получения ввода от пользователя
    thread = threading.Thread(target=self.get_input)
    thread.start()

    # Ожидаем завершения потока или тайм-аут
    thread.join(timeout)

    if thread.is_alive():
        print(f"Timeout occurred after {timeout} seconds.")
        return  # Возвращаем None, если тайм-аут произошел

    return self.user_input
```

**Назначение**: Ожидает ввод от пользователя с таймаутом.

**Параметры**:
- `timeout` (int): Время ожидания ввода в секундах. По умолчанию `5`.

**Возвращает**:
- `str | None`: Введенные данные или `None`, если произошел таймаут.

**Как работает функция**:
- Функция создает и запускает поток для получения ввода от пользователя с использованием метода `self.get_input`.
- Поток ожидает завершения в течение заданного времени таймаута.
- Если поток все еще активен после таймаута, это означает, что таймаут произошел, и функция возвращает `None`.
- Если поток завершился вовремя, функция возвращает введенные пользователем данные, сохраненные в `self.user_input`.

**Примеры**:

```python
timeout_check = TimeoutCheck()

# Пример 1: Ожидание ввода с таймаутом 3 секунды
user_input = timeout_check.input_with_timeout(timeout=3)
if user_input:
    print(f"You entered: {user_input}")
else:
    print("Timeout occurred.")

# Пример 2: Ожидание ввода с таймаутом по умолчанию (5 секунд)
user_input = timeout_check.input_with_timeout()
if user_input:
    print(f"You entered: {user_input}")
else:
    print("Timeout occurred.")
```

## Пример использования
В блоке `if __name__ == '__main__'` показан пример использования класса `TimeoutCheck`.
```python
if __name__ == '__main__':
    # Example usage
    timeout_check = TimeoutCheck()
    
    # Check interval with a timeout of 5 seconds
    if timeout_check.interval_with_timeout(timeout=5):
        print("Current time is within the interval.")
    else:
        print("Current time is outside the interval or timeout occurred.")