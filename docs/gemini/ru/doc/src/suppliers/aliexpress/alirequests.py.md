# Модуль для выполнения запросов к AliExpress

## Обзор

Модуль `alirequests.py` предназначен для организации и выполнения HTTP-запросов к AliExpress. Он предоставляет класс `AliRequests`, который упрощает работу с куки, заголовками и сессиями при взаимодействии с API AliExpress.

## Подробнее

Этот модуль облегчает взаимодействие с AliExpress, автоматически управляя куки и заголовками, что позволяет избежать ручной обработки этих данных при каждом запросе. Он использует `requests` для выполнения HTTP-запросов и `fake_useragent` для генерации случайных User-Agent, что помогает имитировать поведение реального пользователя.

## Классы

### `AliRequests`

**Описание**: Класс для отправки запросов к AliExpress с использованием библиотеки `requests`.

**Атрибуты**:

- `cookies_jar` (RequestsCookieJar): Объект для хранения и управления куки.
- `session_id` (str): Идентификатор сессии.
- `headers` (dict): Заголовки HTTP-запроса, включая User-Agent.
- `session` (requests.Session): Объект сессии `requests` для выполнения запросов.

**Методы**:

- `__init__(self, webdriver_for_cookies: str = 'chrome')`: Инициализирует класс `AliRequests`, загружает куки из файла, если он существует, и обновляет сессионные куки.
- `_load_webdriver_cookies_file(self, webdriver_for_cookies: str = 'chrome') -> bool`: Загружает куки из файла, созданного веб-драйвером.
- `_refresh_session_cookies(self)`: Обновляет сессионные куки, выполняя GET-запрос к AliExpress.
- `_handle_session_id(self, response_cookies)`: Обрабатывает `JSESSIONID` из куки ответа.
- `make_get_request(self, url: str, cookies: List[dict] = None, headers: dict = None)`: Выполняет GET-запрос с заданными куки и заголовками.
- `short_affiliate_link(self, link_url: str)`: Генерирует короткую партнерскую ссылку.

### `__init__`

```python
def __init__(self, webdriver_for_cookies: str = 'chrome'):
    """Инициализирует класс AliRequests.

    Args:
        webdriver_for_cookies (str, optional): Имя веб-драйвера для загрузки куки. По умолчанию 'chrome'.
    """
    ...
```

**Назначение**: Инициализация экземпляра класса `AliRequests`. Устанавливает куки, заголовки и создает сессию.

**Параметры**:

- `webdriver_for_cookies` (str, optional): Имя веб-драйвера, используемого для загрузки файлов cookie. По умолчанию используется 'chrome'.

**Как работает функция**:

- Инициализирует `cookies_jar` как экземпляр `RequestsCookieJar` для хранения куки.
- Устанавливает `session_id` в `None`.
- Определяет `headers` для HTTP-запросов, используя случайный User-Agent.
- Создает сессию `requests.Session()` для выполнения HTTP-запросов.
- Вызывает `self._load_webdriver_cookies_file(webdriver_for_cookies)` для загрузки куки из файла, соответствующего указанному веб-драйверу.

**Примеры**:

```python
ali_requests = AliRequests(webdriver_for_cookies='firefox')
```

### `_load_webdriver_cookies_file`

```python
def _load_webdriver_cookies_file(self, webdriver_for_cookies: str = 'chrome') -> bool:
    """Загружает куки из файла веб-драйвера.

    Args:
        webdriver_for_cookies (str, optional): Имя веб-драйвера. По умолчанию 'chrome'.

    Returns:
        bool: True, если куки успешно загружены, иначе False.
    """
    ...
```

**Назначение**: Загружает куки из файла, созданного веб-драйвером.

**Параметры**:

- `webdriver_for_cookies` (str, optional): Имя веб-драйвера, куки которого нужно загрузить. По умолчанию 'chrome'.

**Возвращает**:

- `bool`: `True`, если куки успешно загружены, `False` в противном случае.

**Как работает функция**:

- Формирует путь к файлу cookie на основе `gs.dir_cookies`, `'aliexpress.com'`, `webdriver_for_cookies` и `'cookie'`.
- Пытается открыть файл cookie и загрузить куки из него.
- Для каждой куки устанавливает значения `name`, `value`, `domain`, `path`, `secure`, `HttpOnly`, `SameSite` и `expires`.
- Вызывает `self._refresh_session_cookies()` для обновления куки сессии.
- Логирует успех или ошибку загрузки куки.

**Примеры**:

```python
success = self._load_webdriver_cookies_file(webdriver_for_cookies='chrome')
if success:
    print("Cookies loaded successfully")
else:
    print("Failed to load cookies")
```

### `_refresh_session_cookies`

```python
def _refresh_session_cookies(self):
    """Обновляет куки сессии."""
    ...
```

**Назначение**: Обновляет куки текущей сессии, выполняя GET-запрос к `https://portals.aliexpress.com`.

**Как работает функция**:

- Выполняет GET-запрос к `https://portals.aliexpress.com` с использованием текущих куки и заголовков.
- Если `cookies_jar` не пустой, передает куки в запросе.
- Вызывает `self._handle_session_id(resp.cookies)` для обработки полученных куки, чтобы обновить `JSESSIONID`.
- Логирует ошибки, если запрос не удался.

**Примеры**:

```python
self._refresh_session_cookies()
```

### `_handle_session_id`

```python
def _handle_session_id(self, response_cookies):
    """Обрабатывает JSESSIONID в куки ответа."""
    ...
```

**Назначение**: Обрабатывает `JSESSIONID` в куки ответа, чтобы поддерживать сессию.

**Параметры**:

- `response_cookies` (requests.cookies.RequestsCookieJar): Куки, полученные в ответе на HTTP-запрос.

**Как работает функция**:

- Перебирает куки в `response_cookies`.
- Если находит куки с именем `JSESSIONID`:
    - Сравнивает значение найденной куки с текущим `self.session_id`. Если они одинаковы, функция завершается.
    - Если значения разные, обновляет `self.session_id` новым значением.
    - Обновляет `cookies_jar` с новой кукой `JSESSIONID`.
- Если `JSESSIONID` не найден, логирует предупреждение.

**Примеры**:

```python
self._handle_session_id(resp.cookies)
```

### `make_get_request`

```python
def make_get_request(self, url: str, cookies: List[dict] = None, headers: dict = None):
    """Выполняет GET-запрос с куки.

    Args:
        url (str): URL для выполнения GET-запроса.
        cookies (List[dict], optional): Список куки для использования в запросе. По умолчанию None.
        headers (dict, optional): Заголовки для включения в запрос. По умолчанию None.

    Returns:
        requests.Response: Объект requests.Response в случае успеха, False в противном случае.
    """
    ...
```

**Назначение**: Выполняет GET-запрос к указанному URL с заданными куки и заголовками.

**Параметры**:

- `url` (str): URL для выполнения GET-запроса.
- `cookies` (List[dict], optional): Список куки для использования в запросе. По умолчанию `None`.
- `headers` (dict, optional): Заголовки для включения в запрос. По умолчанию `None`.

**Возвращает**:

- `requests.Response`: Объект `requests.Response` в случае успеха, `False` в противном случае.

**Как работает функция**:

- Обновляет куки сессии из `self.cookies_jar`.
- Выполняет GET-запрос к указанному URL с заданными заголовками.
- Обрабатывает `JSESSIONID` из куки ответа.
- Возвращает объект `requests.Response` в случае успеха.
- Логирует ошибки, если запрос не удался.

**Примеры**:

```python
response = self.make_get_request(url='https://example.com', headers={'Custom-Header': 'value'})
if response:
    print("Request successful")
else:
    print("Request failed")
```

### `short_affiliate_link`

```python
def short_affiliate_link(self, link_url: str):
    """Получает короткую партнерскую ссылку.

    Args:
        link_url (str): URL для сокращения.

    Returns:
        requests.Response: Объект requests.Response в случае успеха, False в противном случае.
    """
    ...
```

**Назначение**: Генерирует короткую партнерскую ссылку на основе предоставленного URL.

**Параметры**:

- `link_url` (str): URL, который нужно сократить.

**Возвращает**:

- `requests.Response`: Объект `requests.Response` в случае успеха, `False` в противном случае.

**Как работает функция**:

- Формирует URL для запроса к сервису сокращения ссылок AliExpress.
- Вызывает `self.make_get_request(url)` для выполнения GET-запроса.
- Возвращает результат запроса.

**Примеры**:

```python
response = self.short_affiliate_link(link_url='https://aliexpress.com/item/1234567890.html')
if response:
    print("Short link generated")
else:
    print("Failed to generate short link")