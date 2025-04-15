# Модуль для выбора случайного User-Agent

## Обзор

Модуль предназначен для предоставления случайного User-Agent из заданного списка. Это может быть полезно для имитации различных браузеров при выполнении запросов, например, при парсинге веб-страниц.

## Подробнее

Этот модуль содержит функцию `get_useragent`, которая возвращает случайно выбранный User-Agent из списка `_useragent_list`. Список содержит различные User-Agent, представляющие разные браузеры и операционные системы.  Модуль располагается в `hypotez/src/endpoints/bots/telegram/movie_bot-main/apps/useragent.py`, что говорит о его использовании в Telegram-боте для работы с фильмами, где требуется имитация пользовательского браузера для доступа к различным веб-ресурсам.

## Функции

### `get_useragent`

```python
def get_useragent() -> str:
    """
    Возвращает случайно выбранный User-Agent из списка.

    Returns:
        str: Случайно выбранный User-Agent.
    """
    ...
```

**Назначение**:
Функция выбирает случайный User-Agent из списка `_useragent_list` и возвращает его.

**Возвращает**:
- `str`: Случайно выбранный User-Agent.

**Как работает функция**:

1. Функция использует `random.choice()` для выбора случайного элемента из списка `_useragent_list`.
2. Возвращает выбранный элемент.

**Примеры**:

```python
import random

_useragent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
]

def get_useragent():
    return random.choice(_useragent_list)

user_agent = get_useragent()
print(user_agent)
# Пример вывода: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0

user_agent = get_useragent()
print(user_agent)
# Пример вывода: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36
```

## Переменные модуля

### `_useragent_list`

- **Описание**: Список, содержащий различные User-Agent.
```python
_useragent_list: list[str] = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
]
```
- **Назначение**: Хранит список строк, представляющих User-Agent различных браузеров. Этот список используется функцией `get_useragent` для случайного выбора User-Agent.