# Модуль `useragent`

## Обзор

Модуль `useragent` предназначен для случайного выбора user-agent из предопределенного списка. Это полезно для имитации запросов от различных браузеров и операционных систем, что может быть необходимо для обхода ограничений или маскировки активности бота.

## Более подробная информация

Этот модуль предоставляет простую функцию `get_useragent`, которая возвращает случайный user-agent из списка `_useragent_list`. User-agent используется для идентификации браузера и операционной системы, с которых делается запрос к веб-серверу. Модуль может использоваться для ротации user-agent в запросах, чтобы избежать блокировки или ограничения доступа к сайту.

## Функции

### `get_useragent`

```python
def get_useragent() -> str:
    """
    Функция возвращает случайно выбранный user-agent из списка.

    Returns:
        str: Случайно выбранный user-agent.

    Пример:
        >>> get_useragent()
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
    """
    ...
```

**Как работает функция**:

1. Функция `get_useragent` не принимает аргументов.
2. Внутри функции вызывается `random.choice(_useragent_list)`, что выбирает случайный элемент из списка `_useragent_list`.
3. Функция возвращает выбранный user-agent в виде строки.

**Примеры**:

```python
import random

def get_useragent():
    return random.choice(_useragent_list)

_useragent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
]

print(get_useragent())
```

## Переменные

### `_useragent_list`

- **Описание**: Список строк, содержащих различные user-agent.
- **Тип**: `List[str]`
- **Назначение**: Хранит набор user-agent, из которого функция `get_useragent` случайным образом выбирает один.
```python
_useragent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
]