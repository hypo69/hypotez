### Анализ кода модуля `hypotez/src/utils/url.py`

## Обзор

Модуль предназначен для работы с URL-адресами, включая извлечение параметров запроса, проверку на валидность URL и сокращение ссылок.

## Подробнее

Модуль содержит функции, упрощающие обработку URL-адресов, такие как извлечение параметров, проверку валидности URL и сокращение длинных ссылок с использованием сервиса TinyURL.

## Функции

### `extract_url_params`

```python
def extract_url_params(url: str) -> dict | None:
    """Извлекает параметры из строки URL.

    Args:
        url (str): Строка URL для парсинга.

    Returns:
        dict | None: Словарь параметров запроса и их значений или `None`, если URL не содержит параметров.
    """
    ...
```

**Назначение**:
Извлекает параметры из строки URL.

**Параметры**:
- `url` (str): Строка URL для парсинга.

**Возвращает**:
- `dict | None`: Словарь параметров запроса и их значений или `None`, если URL не содержит параметров.

**Как работает функция**:
1.  Использует `urlparse` для разбора URL.
2.  Использует `parse_qs` для извлечения параметров запроса.
3.  Преобразует значения параметров из списка в строку, если параметр имеет одно значение.
4.  Возвращает словарь параметров.

**Примеры**:

```python
url = "https://example.com/path?param1=value1&param2=value2"
params = extract_url_params(url)
print(params)  # Вывод: {'param1': 'value1', 'param2': 'value2'}
```

### `is_url`

```python
def is_url(text: str) -> bool:
    """Проверяет, является ли переданный текст валидным URL с использованием библиотеки validators.

    Args:
        text (str): Строка для проверки.

    Returns:
        bool: `True` если строка является валидным URL, иначе `False`.
    """
    ...
```

**Назначение**:
Проверяет, является ли переданный текст валидным URL с использованием библиотеки `validators`.

**Параметры**:
- `text` (str): Строка для проверки.

**Возвращает**:
- `bool`: `True`, если строка является валидным URL, иначе `False`.

**Как работает функция**:
1. Использует `validators.url(text)` для проверки, является ли строка валидным URL.
2. Возвращает результат проверки.

**Примеры**:

```python
text = "https://example.com"
is_valid = is_url(text)
print(is_valid)  # Вывод: True

text = "not a url"
is_valid = is_url(text)
print(is_valid)  # Вывод: False
```

### `url_shortener`

```python
def url_shortener(long_url: str) -> str | None:
    """Сокращает длинный URL с использованием сервиса TinyURL.

    Args:
        long_url (str): Длинный URL для сокращения.

    Returns:
        str | None: Сокращённый URL или `None`, если произошла ошибка.
    """
    ...
```

**Назначение**:
Сокращает длинный URL с использованием сервиса TinyURL.

**Параметры**:
- `long_url` (str): Длинный URL для сокращения.

**Возвращает**:
- `str | None`: Сокращенный URL или `None`, если произошла ошибка.

**Как работает функция**:
1. Формирует URL для запроса к сервису TinyURL.
2. Отправляет GET-запрос к сервису.
3. Если запрос успешен, возвращает сокращенный URL из ответа.
4. Если произошла ошибка, возвращает `None`.

**Примеры**:

```python
long_url = "https://example.com/very/long/path/to/resource"
short_url = url_shortener(long_url)
if short_url:
    print(f"Сокращенный URL: {short_url}")
else:
    print("Ошибка при сокращении URL.")
```

## Переменные

Отсутствуют

## Запуск

Для использования этого модуля необходимо установить библиотеку `requests` и `validators`.

```bash
pip install requests validators
```

```python
from src.utils.url import extract_url_params, is_url, url_shortener

url = "https://example.com/path?param1=value1&param2=value2"
params = extract_url_params(url)
print(params)

text = "https://example.com"
is_valid = is_url(text)
print(is_valid)

long_url = "https://example.com/very/long/path/to/resource"
short_url = url_shortener(long_url)
if short_url:
    print(f"Сокращенный URL: {short_url}")