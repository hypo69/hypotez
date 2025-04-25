# Модуль `helper`

## Обзор

Модуль `helper` содержит набор вспомогательных функций для работы с API GPT-4Free, включая функции для создания запросов, обработки ответов и управления cookie.

## Подробнее

Данный модуль предоставляет набор инструментов для взаимодействия с API GPT-4Free, который использует бесплатный доступ к модели GPT-4. 

## Функции

### `get_cookies`

**Назначение**: Функция извлекает cookie-файлы, используемые для аутентификации с API GPT-4Free.

**Параметры**:

- `filename` (str): Имя файла cookie. По умолчанию `'cookies.json'`.

**Возвращает**:

- dict: Словарь с cookie-файлами или `None`, если файл не найден.

**Как работает функция**:

- Функция считывает данные из файла `cookies.json`, который содержит cookie-файлы, используемые для доступа к API GPT-4Free.

**Примеры**:

```python
>>> cookies = get_cookies()
>>> print(cookies)
{'sessionid': '...', 'csrftoken': '...'}
```

### `get_connector`

**Назначение**: Функция создает объект `aiohttp.ClientSession` с настройками, необходимыми для работы с API GPT-4Free.

**Параметры**:

- `cookie_jar` (aiohttp.CookieJar): Объект `aiohttp.CookieJar`, содержащий cookie-файлы.

**Возвращает**:

- aiohttp.ClientSession: Объект `aiohttp.ClientSession` с заданными настройками.

**Как работает функция**:

- Функция создает объект `aiohttp.ClientSession` с использованием  `cookie_jar` и  `get_connector` для управления соединением с API GPT-4Free.

**Примеры**:

```python
>>> from ..cookies import get_cookies
>>> connector = get_connector(get_cookies())
>>> print(connector)
<ClientSession ...>
```

### `get_data`

**Назначение**: Функция выполняет GET-запрос к API GPT-4Free.

**Параметры**:

- `url` (str): URL-адрес API-запроса.
- `connector` (aiohttp.ClientSession): Объект `aiohttp.ClientSession` для выполнения запроса.
- `data` (dict): Дополнительные данные для запроса.
- `headers` (dict): Дополнительные заголовки для запроса.

**Возвращает**:

- dict: Словарь с данными ответа.

**Как работает функция**:

- Функция отправляет GET-запрос к API GPT-4Free с использованием `connector` и дополнительных параметров `data` и `headers`.
- Функция обрабатывает ответ от API и возвращает его в виде словаря.

**Примеры**:

```python
>>> data = get_data('https://gpt4free.com/api/v1/chat', connector, headers={'Authorization': 'Bearer ...'})
>>> print(data)
{'status': 'ok', 'message': '...', 'data': {'...': ...}}
```

### `get_response`

**Назначение**: Функция обрабатывает ответ от API GPT-4Free и возвращает результат.

**Параметры**:

- `response` (dict): Данные ответа от API GPT-4Free.

**Возвращает**:

- str: Текстовый ответ от модели GPT-4Free.

**Как работает функция**:

- Функция извлекает текст ответа от модели из словаря `response`, полученного от API GPT-4Free.
- Функция проверяет наличие ошибки в ответе и выводит сообщение об ошибке, если оно имеется.

**Примеры**:

```python
>>> response = {'status': 'ok', 'message': '...', 'data': {'content': '...'}}
>>> text = get_response(response)
>>> print(text)
...
```

### `parse_response`

**Назначение**: Функция преобразует ответ от API GPT-4Free в формат, пригодный для использования.

**Параметры**:

- `response` (dict): Данные ответа от API GPT-4Free.

**Возвращает**:

- list: Список обработанных ответов от модели GPT-4Free.

**Как работает функция**:

- Функция проверяет наличие ошибки в ответе `response`.
- Функция извлекает список ответов от модели `response['data']['content']` и преобразует его в список.
- Функция возвращает обработанный список ответов.

**Примеры**:

```python
>>> response = {'status': 'ok', 'message': '...', 'data': {'content': '...'}}
>>> parsed_response = parse_response(response)
>>> print(parsed_response)
['...', '...', '...']
```

## Внутренние функции

### `_parse_response`

**Назначение**: Функция преобразует ответ от API GPT-4Free в формат, пригодный для использования.

**Параметры**:

- `response` (dict): Данные ответа от API GPT-4Free.

**Возвращает**:

- list: Список обработанных ответов от модели GPT-4Free.

**Как работает функция**:

- Функция проверяет наличие ошибки в ответе `response`.
- Функция извлекает список ответов от модели `response['data']['content']` и преобразует его в список.
- Функция возвращает обработанный список ответов.

**Примеры**:

```python
>>> response = {'status': 'ok', 'message': '...', 'data': {'content': '...'}}
>>> parsed_response = _parse_response(response)
>>> print(parsed_response)
['...', '...', '...']