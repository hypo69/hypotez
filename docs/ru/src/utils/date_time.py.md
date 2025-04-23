# Модуль для работы с датой и временем

## Обзор

Модуль `src.utils.date_time` предоставляет инструменты для проверки, находится ли текущее время в заданном интервале, с возможностью установки таймаута. Он содержит класс `TimeoutCheck` с методами для определения попадания текущего времени в указанный временной промежуток, что полезно для выполнения операций, которые должны происходить только в определенные периоды времени (например, ночное обслуживание). Модуль также предоставляет функциональность ожидания ввода пользователя с таймаутом.

## Подробней

Этот модуль предназначен для определения, находится ли текущее время в заданном интервале. Он может быть использован для планирования задач, которые должны выполняться только в определенное время суток. Класс `TimeoutCheck` предоставляет методы для проверки интервала времени с учетом таймаута, а также для ожидания ввода пользователя с таймаутом.

## Классы

### `TimeoutCheck`

**Описание**: Класс для проверки, находится ли текущее время в заданном интервале, с возможностью установки таймаута.

**Атрибуты**:
- `result` (bool | None): Результат проверки интервала времени.
- `user_input` (str | None): Ввод пользователя.

**Методы**:
- `interval(start: time, end: time) -> bool`: Проверяет, находится ли текущее время в заданном интервале.
- `interval_with_timeout(timeout: int, start: time, end: time) -> bool`: Проверяет, находится ли текущее время в заданном интервале с таймаутом.
- `get_input() -> None`: Запрашивает ввод от пользователя.
- `input_with_timeout(timeout: int) -> str | None`: Ожидает ввод с таймаутом.

**Принцип работы**:
Класс `TimeoutCheck` предоставляет методы для проверки, находится ли текущее время в заданном интервале. Метод `interval` проверяет, находится ли текущее время в заданном интервале без таймаута. Метод `interval_with_timeout` проверяет, находится ли текущее время в заданном интервале с таймаутом. Если таймаут истекает, метод возвращает `False`. Методы `get_input` и `input_with_timeout` используются для получения ввода от пользователя с таймаутом.

## Методы класса

### `interval`

```python
def interval(self, start: time = time(23, 0), end: time = time(6, 0)) -> bool:
    """ Проверяет, находится ли текущее время в заданном интервале.

    Args:
        start (time): Начало интервала (по умолчанию 23:00).
        end (time): Конец интервала (по умолчанию 06:00).

    Returns:
        bool: True, если текущее время находится в интервале, False в противном случае.
    """
```

**Назначение**: Проверяет, находится ли текущее время в заданном интервале.

**Параметры**:
- `start` (time): Начало интервала. По умолчанию `23:00`.
- `end` (time): Конец интервала. По умолчанию `06:00`.

**Возвращает**:
- `bool`: `True`, если текущее время находится в интервале, `False` в противном случае.

**Как работает функция**:
Функция `interval` получает текущее время и сравнивает его с заданным интервалом, определенным параметрами `start` и `end`. Если `start` меньше `end`, интервал считается находящимся в пределах одного дня (например, с 08:00 до 17:00). Если `start` больше `end`, интервал считается пересекающим полночь (например, с 23:00 до 06:00). Результат сравнения сохраняется в атрибуте `self.result`.

```python
from datetime import datetime, time

current_time = datetime.now().time()

if start < end:
    # Интервал в пределах одного дня (например, с 08:00 до 17:00)
    self.result = start <= current_time <= end
else:
    # Интервал, охватывающий полночь (например, с 23:00 до 06:00)
    self.result = current_time >= start or current_time <= end
```

**Примеры**:

```python
from datetime import time
from src.utils.date_time import TimeoutCheck

timeout_check = TimeoutCheck()

# Проверка, находится ли текущее время между 23:00 и 06:00
result = timeout_check.interval(start=time(23, 0), end=time(6, 0))
print(result)

# Проверка, находится ли текущее время между 08:00 и 17:00
result = timeout_check.interval(start=time(8, 0), end=time(17, 0))
print(result)
```

### `interval_with_timeout`

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
```

**Назначение**: Проверяет, находится ли текущее время в заданном интервале с таймаутом.

**Параметры**:
- `timeout` (int): Время в секундах для ожидания проверки интервала.
- `start` (time): Начало интервала. По умолчанию `23:00`.
- `end` (time): Конец интервала. По умолчанию `06:00`.

**Возвращает**:
- `bool`: `True`, если текущее время находится в интервале и ответ получен в течение таймаута, `False`, если нет или произошел таймаут.

**Как работает функция**:
Функция `interval_with_timeout` запускает проверку интервала времени в отдельном потоке. Она ожидает завершения потока в течение заданного времени ожидания (`timeout`). Если поток завершается до истечения таймаута, функция возвращает результат проверки интервала. Если таймаут истекает, функция возвращает `False`.

```python
thread = threading.Thread(target=self.interval, args=(start, end))
thread.start()
thread.join(timeout)

if thread.is_alive():
    print(f"Timeout occurred after {timeout} seconds, continuing execution.")
    thread.join()  # Ensures thread stops after timeout
    return False  # Timeout occurred, so returning False
return self.result
```

**Примеры**:

```python
from datetime import time
from src.utils.date_time import TimeoutCheck

timeout_check = TimeoutCheck()

# Проверка, находится ли текущее время между 23:00 и 06:00 с таймаутом 5 секунд
result = timeout_check.interval_with_timeout(timeout=5, start=time(23, 0), end=time(6, 0))
print(result)

# Проверка, находится ли текущее время между 08:00 и 17:00 с таймаутом 10 секунд
result = timeout_check.interval_with_timeout(timeout=10, start=time(8, 0), end=time(17, 0))
print(result)
```

### `get_input`

```python
def get_input(self):
    """ Запрашивает ввод от пользователя."""
    self.user_input = input("U:> ")
```

**Назначение**: Запрашивает ввод от пользователя.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
Функция `get_input` запрашивает ввод от пользователя через консоль и сохраняет его в атрибуте `self.user_input`.

**Примеры**:

```python
from src.utils.date_time import TimeoutCheck

timeout_check = TimeoutCheck()

# Запрос ввода от пользователя
timeout_check.get_input()
print(timeout_check.user_input)
```

### `input_with_timeout`

```python
def input_with_timeout(self, timeout: int = 5) -> str | None:
    """ Ожидает ввод с таймаутом.

    Args:
        timeout (int): Время ожидания ввода в секундах.

    Returns:
        str | None: Введенные данные или None, если был тайм-аут.
    """
```

**Назначение**: Ожидает ввод от пользователя с таймаутом.

**Параметры**:
- `timeout` (int): Время ожидания ввода в секундах.

**Возвращает**:
- `str | None`: Введенные данные или `None`, если произошел таймаут.

**Как работает функция**:
Функция `input_with_timeout` запускает ввод от пользователя в отдельном потоке и ожидает завершения потока в течение заданного времени ожидания (`timeout`). Если поток завершается до истечения таймаута, функция возвращает введенные данные. Если таймаут истекает, функция возвращает `None`.

```python
thread = threading.Thread(target=self.get_input)
thread.start()

# Ожидаем завершения потока или тайм-аут
thread.join(timeout)

if thread.is_alive():
    print(f"Timeout occurred after {timeout} seconds.")
    return  # Возвращаем None, если тайм-аут произошел

return self.user_input
```

**Примеры**:

```python
from src.utils.date_time import TimeoutCheck

timeout_check = TimeoutCheck()

# Ожидание ввода от пользователя с таймаутом 5 секунд
user_input = timeout_check.input_with_timeout(timeout=5)
print(user_input)

# Ожидание ввода от пользователя с таймаутом 10 секунд
user_input = timeout_check.input_with_timeout(timeout=10)
print(user_input)