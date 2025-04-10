# Модуль для работы с User-Agent
=================================================

Модуль содержит функцию `get_useragent`, которая возвращает случайный User-Agent из списка `_useragent_list`.

## Обзор

Модуль предназначен для предоставления случайных User-Agent строк для использования в запросах к веб-сайтам. Это может быть полезно для имитации различных браузеров и операционных систем, например, при парсинге веб-страниц или тестировании веб-приложений.

## Подробнее

Этот модуль предоставляет простой способ получения случайного User-Agent из предопределенного списка.  Он используется в проекте `hypotez` для имитации различных браузеров при выполнении HTTP-запросов. Это позволяет избежать блокировок со стороны серверов, которые могут ограничивать доступ для автоматизированных запросов, и обеспечивает более реалистичное поведение бота.

## Функции

### `get_useragent`

```python
def get_useragent() -> str:
    """
    Возвращает случайный User-Agent из списка.

    Returns:
        str: Случайный User-Agent.
    """
    ...
```

**Назначение**: Возвращает случайно выбранный User-Agent из списка `_useragent_list`.

**Возвращает**:
- `str`: Случайный User-Agent.

**Как работает функция**:
- Функция использует `random.choice` для случайного выбора одного элемента из списка `_useragent_list`.

**Примеры**:

```python
import random

def get_useragent() -> str:
    """
    Возвращает случайный User-Agent из списка.

    Returns:
        str: Случайный User-Agent.
    """
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

## Переменные модуля

### `_useragent_list`

- **Описание**: Список строк, содержащих различные User-Agent.
- **Тип**: `List[str]`
- **Назначение**: Хранит набор User-Agent, из которых функция `get_useragent` выбирает случайный.
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