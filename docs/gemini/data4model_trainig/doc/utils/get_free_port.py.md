### Анализ кода модуля `hypotez/src/utils/get_free_port.py`

## Обзор

Этот модуль предоставляет функцию для поиска свободного порта в системе. Функция может искать порт в заданном диапазоне или найти первый доступный порт, если диапазон не указан.

## Подробнее

Модуль содержит функцию `get_free_port`, которая позволяет найти свободный порт для использования в сетевых приложениях. Функция использует сокеты для проверки доступности портов и может работать как с одним диапазоном портов, так и со списком диапазонов.

## Функции

### `get_free_port`

```python
def get_free_port(host: str, port_range: Optional[str | List[str]] = None) -> int:
    """
    Finds and returns a free port within the specified range, or the first available port if no range is given.

    Args:
        host (str): The host address to check for available ports.
        port_range (Optional[str | List[str]], optional): A port range specified as a string "min-max" or a list of strings.
               E.g.: "3000-3999", ["3000-3999", "8000-8010"], None. Defaults to `None`.

    Returns:
        int: An available port number.

    Raises:
        ValueError: If no free port can be found within the specified range, or if the port range is invalid.
    """
    ...
```

**Назначение**:
Находит и возвращает свободный порт в указанном диапазоне или первый доступный порт, если диапазон не задан.

**Параметры**:
- `host` (str): IP-адрес хоста для проверки доступных портов.
- `port_range` (Optional[str | List[str]], optional): Диапазон портов, заданный строкой "min-max" или списком строк. Например: "3000-3999", ["3000-3999", "8000-8010"], None. По умолчанию `None`.

**Возвращает**:
- `int`: Доступный номер порта.

**Вызывает исключения**:
- `ValueError`: Если не удается найти свободный порт в указанном диапазоне или если диапазон портов недействителен.

**Как работает функция**:

1. Определяет две внутренние функции: `_is_port_in_use` и `_parse_port_range`.
2.  `_is_port_in_use`: Проверяет, используется ли указанный порт на заданном хосте.
3.  `_parse_port_range`: Преобразует строку диапазона портов "min-max" в кортеж (min_port, max_port).
4. Если `port_range` указан:
    - Если `port_range` - строка:
        - Преобразует строку диапазона в кортеж (min_port, max_port) с помощью `_parse_port_range`.
        - Перебирает порты в указанном диапазоне и возвращает первый свободный порт.
    - Если `port_range` - список:
        - Перебирает элементы списка, преобразует каждый элемент в кортеж (min_port, max_port) и пытается найти свободный порт.
        - Если не удается найти свободный порт ни в одном из диапазонов, вызывает исключение ValueError.
    - Если `port_range` имеет неверный тип, вызывает исключение `ValueError`.
5. Если `port_range` не указан:
    - Начинает поиск с порта 1024 и перебирает порты, пока не найдет свободный.
    - Если не удается найти свободный порт до 65535, вызывает исключение `ValueError`.

**Примеры**:

```python
host = 'localhost'
port = get_free_port(host)
print(f'Free port: {port}')

port = get_free_port(host, '3000-3005')
print(f'Free port in range: {port}')

port = get_free_port(host, ['3000-3005', '8000-8010'])
print(f'Free port in multiple ranges: {port}')
```

## Внутренние функции

### `_is_port_in_use`

```python
def _is_port_in_use(host: str, port: int) -> bool:
    """
    Checks if a given port is in use on the specified host.

    Args:
        host (str): The host address.
        port (int): The port number to check.

    Returns:
        bool: True if the port is in use, False otherwise.
    """
    ...
```

**Назначение**:
Проверяет, используется ли указанный порт на заданном хосте.

**Параметры**:
- `host` (str): IP-адрес хоста.
- `port` (int): Номер порта для проверки.

**Возвращает**:
- `bool`: True, если порт используется, False в противном случае.

**Как работает функция**:
1. Создает сокет TCP.
2. Пытается привязать сокет к указанному хосту и порту.
3. Если привязка успешна, значит порт свободен, и функция возвращает `False`.
4. Если при привязке возникает исключение `OSError`, значит порт используется, и функция возвращает `True`.

### `_parse_port_range`

```python
def _parse_port_range(port_range_str: str) -> Tuple[int, int]:
    """
    Parses port range string "min-max" into a tuple (min_port, max_port).

    Args:
        port_range_str (str): The port range string.

    Returns:
        Tuple[int, int]: A tuple containing minimum and maximum port numbers.

    Raises:
        ValueError: If the port range string format is invalid.
    """
    ...
```

**Назначение**:
Преобразует строку диапазона портов "min-max" в кортеж (min_port, max_port).

**Параметры**:
- `port_range_str` (str): Строка диапазона портов.

**Возвращает**:
- `Tuple[int, int]`: Кортеж, содержащий минимальный и максимальный номера портов.

**Вызывает исключения**:
- `ValueError`: Если формат строки диапазона портов недействителен.

**Как работает функция**:
1. Разделяет строку `port_range_str` по символу "-".
2. Проверяет, что получено ровно 2 части. Если нет, вызывает исключение `ValueError`.
3. Преобразует обе части в целые числа.
4. Проверяет, что минимальный порт меньше максимального. Если нет, вызывает исключение `ValueError`.
5. Возвращает кортеж, содержащий минимальный и максимальный номера портов.

## Переменные

Отсутствуют

## Запуск

Для использования данного модуля необходимо импортировать функцию `get_free_port` из модуля `src.utils.get_free_port`.

```python
from src.utils.get_free_port import get_free_port

host = 'localhost'
port = get_free_port(host)
print(f'Free port: {port}')

port = get_free_port(host, '3000-3005')
print(f'Free port in range: {port}')