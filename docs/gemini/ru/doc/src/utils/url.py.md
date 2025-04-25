# Модуль для работы с URL 

## Обзор

Модуль `src.utils.string.url`  предоставляет набор функций для работы с URL, включая извлечение параметров запроса, проверку на валидность и сокращение URL. 

## Подробнее

Модуль используется для обработки URL-строк и выполнения следующих операций:

- **Извлечение параметров запроса**: 
    - Функция `extract_url_params(url: str) -> dict | None` извлекает параметры из строки URL, возвращая словарь с параметрами и их значениями. 
- **Проверка валидности URL**: 
    - Функция `is_url(text: str) -> bool`  проверяет, является ли переданный текст валидным URL, используя библиотеку `validators`.
- **Сокращение URL**: 
    - Функция `url_shortener(long_url: str) -> str | None` сокращает длинный URL с использованием сервиса TinyURL.

## Классы

### `None`

**Описание**: В модуле нет собственных классов, но используются стандартные Python-классы, например `requests.Response`.

## Функции

### `extract_url_params`

**Назначение**: Извлекает параметры из строки URL.

**Параметры**:

- `url` (str): Строка URL для парсинга.

**Возвращает**:

- `dict | None`: Словарь параметров запроса и их значений или `None`, если URL не содержит параметров.

**Как работает**:

- Парсит URL-строку с помощью `urlparse` из `urllib.parse`.
- Извлекает параметры запроса из раздела `query` URL с помощью `parse_qs`.
- Преобразует значения параметров из списков в строки, если параметр имеет одно значение.

**Примеры**:

```python
>>> extract_url_params('https://www.example.com?param1=value1&param2=value2')
{'param1': 'value1', 'param2': 'value2'}

>>> extract_url_params('https://www.example.com')
None 
```

### `is_url`

**Назначение**: Проверяет, является ли переданный текст валидным URL.

**Параметры**:

- `text` (str): Строка для проверки.

**Возвращает**:

- `bool`: `True` если строка является валидным URL, иначе `False`.

**Как работает**:

- Использует библиотеку `validators` для проверки валидности URL.

**Примеры**:

```python
>>> is_url('https://www.example.com')
True

>>> is_url('example.com')
False

>>> is_url('http://www.example.com/path/to/file.txt')
True
```

### `url_shortener`

**Назначение**: Сокращает длинный URL с использованием сервиса TinyURL.

**Параметры**:

- `long_url` (str): Длинный URL для сокращения.

**Возвращает**:

- `str | None`: Сокращённый URL или `None`, если произошла ошибка.

**Как работает**:

- Формирует URL запроса к API TinyURL.
- Выполняет HTTP-запрос к API TinyURL с помощью `requests.get`.
- Возвращает сокращенный URL из ответа API или `None` в случае ошибки.

**Примеры**:

```python
>>> url_shortener('https://www.example.com/very/long/url/with/many/parts')
'http://tinyurl.com/your-short-url'

>>> url_shortener('invalid_url')
None