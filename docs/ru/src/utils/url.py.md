# Модуль для работы с URL

## Обзор

Модуль `src.utils.string.url` предназначен для обработки URL-адресов. Он предоставляет функциональность для извлечения параметров запроса из URL, проверки валидности URL и сокращения длинных URL с использованием сервиса TinyURL.

## Подробнее

Модуль содержит функции для:

- Извлечения параметров из URL-строки.
- Проверки, является ли строка валидным URL.
- Сокращения длинных URL с использованием сервиса TinyURL.

## Функции

### `extract_url_params`

```python
def extract_url_params(url: str) -> dict | None:
    """ Извлекает параметры из строки URL.

    Args:
        url (str): Строка URL для парсинга.

    Returns:
        dict | None: Словарь параметров запроса и их значений или `None`, если URL не содержит параметров.
    """
```

**Назначение**: Извлечение параметров запроса из URL.

**Параметры**:
- `url` (str): URL-адрес, из которого требуется извлечь параметры.

**Возвращает**:
- `dict | None`: Словарь, содержащий параметры запроса и их значения. Если URL не содержит параметров, возвращает `None`. Если параметр имеет только одно значение, значением в словаре будет строка, иначе - список строк.

**Как работает функция**:
1. Использует `urlparse` для разбора URL.
2. Использует `parse_qs` для извлечения параметров запроса в виде словаря.
3. Преобразует значения параметров из списка в строку, если параметр имеет только одно значение.

**Примеры**:

```python
url_with_params = "https://example.com/path?param1=value1&param2=value2&param2=value3"
params = extract_url_params(url_with_params)
print(params)  # Вывод: {'param1': 'value1', 'param2': ['value2', 'value3']}

url_with_single_params = "https://example.com/path?param1=value1"
params = extract_url_params(url_with_single_params)
print(params)  # Вывод: {'param1': 'value1'}

url_without_params = "https://example.com/path"
params = extract_url_params(url_without_params)
print(params)  # Вывод: None
```

### `is_url`

```python
def is_url(text: str) -> bool:
    """ Проверяет, является ли переданный текст валидным URL с использованием библиотеки validators.

    Args:
        text (str): Строка для проверки.

    Returns:
        bool: `True` если строка является валидным URL, иначе `False`.
    """
```

**Назначение**: Проверка, является ли переданная строка валидным URL.

**Параметры**:
- `text` (str): Строка, которую необходимо проверить на соответствие формату URL.

**Возвращает**:
- `bool`: `True`, если строка является валидным URL, и `False` в противном случае.

**Как работает функция**:
1. Использует функцию `validators.url` для проверки валидности URL.

**Примеры**:

```python
valid_url = "https://example.com"
is_valid = is_url(valid_url)
print(is_valid)  # Вывод: True

invalid_url = "not a url"
is_valid = is_url(invalid_url)
print(is_valid)  # Вывод: False
```

### `url_shortener`

```python
def url_shortener(long_url: str) -> str | None:
    """ Сокращает длинный URL с использованием сервиса TinyURL.

    Args:
        long_url (str): Длинный URL для сокращения.

    Returns:
        str | None: Сокращённый URL или `None`, если произошла ошибка.
    """
```

**Назначение**: Сокращение длинного URL с использованием сервиса TinyURL.

**Параметры**:
- `long_url` (str): Длинный URL, который необходимо сократить.

**Возвращает**:
- `str | None`: Сокращенный URL в случае успешного сокращения или `None`, если произошла ошибка.

**Как работает функция**:
1. Формирует URL для запроса к API TinyURL.
2. Отправляет GET-запрос к API TinyURL.
3. Если запрос выполнен успешно (код состояния 200), возвращает сокращенный URL из ответа. В противном случае возвращает `None`.

**Примеры**:

```python
long_url = "https://www.example.com/very/long/path/to/resource"
short_url = url_shortener(long_url)
if short_url:
    print(f"Сокращенный URL: {short_url}")
else:
    print("Ошибка при сокращении URL.")