# Модуль alirequests.py

## Обзор

Модуль `alirequests.py` предназначен для обработки запросов к AliExpress с использованием библиотеки `requests`. Он включает в себя функциональность для управления куками, создания GET-запросов и получения коротких партнерских ссылок. Модуль обеспечивает удобный интерфейс для взаимодействия с AliExpress, обрабатывая ошибки и логируя действия.

## Подробней

Этот модуль предоставляет класс `AliRequests`, который инкапсулирует логику работы с запросами к AliExpress. Он использует библиотеку `requests` для выполнения HTTP-запросов и управляет куками для поддержания сессии. Модуль также предоставляет методы для получения коротких партнерских ссылок. Расположение этого файла в проекте указывает на его роль в качестве поставщика данных для AliExpress.

## Классы

### `AliRequests`

**Описание**: Класс `AliRequests` предназначен для управления запросами к AliExpress.

**Атрибуты**:
- `cookies_jar` (RequestsCookieJar): Объект для хранения и управления куками.
- `session_id` (str | None): Идентификатор сессии.
- `headers` (dict): Заголовки HTTP-запросов, включая User-Agent.
- `session` (requests.Session): Объект сессии requests для выполнения запросов.

**Методы**:
- `__init__(webdriver_for_cookies: str = 'chrome')`: Инициализирует класс `AliRequests`.
- `_load_webdriver_cookies_file(webdriver_for_cookies: str = 'chrome') -> bool`: Загружает куки из файла, созданного веб-драйвером.
- `_refresh_session_cookies()`: Обновляет куки сессии.
- `_handle_session_id(response_cookies)`: Обрабатывает идентификатор сессии JSESSIONID из куки ответа.
- `make_get_request(url: str, cookies: List[dict] = None, headers: dict = None)`: Выполняет GET-запрос с заданными куками и заголовками.
- `short_affiliate_link(link_url: str)`: Получает короткую партнерскую ссылку.

**Принцип работы**:
Класс `AliRequests` инициализируется с указанием веб-драйвера для загрузки куки. Он загружает куки из файла, обновляет сессионные куки и предоставляет методы для выполнения GET-запросов и получения коротких партнерских ссылок. Куки используются для поддержания сессии и обеспечения доступа к защищенным ресурсам.

## Методы класса

### `__init__`

```python
def __init__(self, webdriver_for_cookies: str = 'chrome'):
    """ Initializes the AliRequests class.

    @param webdriver_for_cookies The name of the webdriver for loading cookies.
    """
    ...
```

**Назначение**: Инициализирует класс `AliRequests`, настраивает куки, заголовки и сессию.

**Параметры**:
- `webdriver_for_cookies` (str): Имя веб-драйвера для загрузки куки (по умолчанию 'chrome').

**Как работает функция**:
- Создает экземпляр `RequestsCookieJar` для хранения куки.
- Инициализирует `session_id` как `None`.
- Устанавливает случайный `User-Agent` в заголовках.
- Создает объект `requests.Session` для выполнения запросов.
- Вызывает `_load_webdriver_cookies_file` для загрузки куки из файла.

**Примеры**:
```python
ali_requests = AliRequests(webdriver_for_cookies='firefox')
```

### `_load_webdriver_cookies_file`

```python
def _load_webdriver_cookies_file(self, webdriver_for_cookies: str = 'chrome') -> bool:
    """ Loads cookies from a webdriver file.

    @param webdriver_for_cookies The name of the webdriver.
    @returns True if cookies loaded successfully, False otherwise.
    """
    ...
```

**Назначение**: Загружает куки из файла, созданного веб-драйвером.

**Параметры**:
- `webdriver_for_cookies` (str): Имя веб-драйвера (по умолчанию 'chrome').

**Возвращает**:
- `bool`: `True`, если куки успешно загружены, `False` в противном случае.

**Как работает функция**:
- Формирует путь к файлу с куками на основе имени веб-драйвера.
- Пытается открыть и прочитать файл с куками, используя `pickle`.
- Для каждой куки устанавливает значения домена, пути, безопасности и HTTPOnly.
- Логирует успешную загрузку куки или ошибки при загрузке.
- Обновляет куки сессии после загрузки.

**Вызывает исключения**:
- `FileNotFoundError`: Если файл с куками не найден.
- `ValueError`: Если файл с куками имеет неверный формат.
- `Exception`: При возникновении других ошибок при загрузке куки.

**Примеры**:
```python
ali_requests = AliRequests()
success = ali_requests._load_webdriver_cookies_file(webdriver_for_cookies='chrome')
if success:
    print("Куки успешно загружены")
else:
    print("Не удалось загрузить куки")
```

### `_refresh_session_cookies`

```python
def _refresh_session_cookies(self):
    """ Refreshes session cookies."""
    ...
```

**Назначение**: Обновляет куки сессии, выполняя GET-запрос к порталу AliExpress.

**Как работает функция**:
- Определяет URL для обновления куки.
- Выполняет GET-запрос с текущими куками и заголовками.
- Обрабатывает полученные куки для обновления `session_id`.
- Логирует ошибки при выполнении запроса.

**Вызывает исключения**:
- `requests.RequestException`: Если происходит ошибка при выполнении запроса.
- `Exception`: При возникновении других ошибок при обновлении куки.

**Примеры**:
```python
ali_requests = AliRequests()
ali_requests._refresh_session_cookies()
```

### `_handle_session_id`

```python
def _handle_session_id(self, response_cookies):
    """ Handles the JSESSIONID in response cookies."""
    ...
```

**Назначение**: Обрабатывает идентификатор сессии `JSESSIONID` в куки ответа.

**Параметры**:
- `response_cookies`: Куки, полученные в ответе на HTTP-запрос.

**Как работает функция**:
- Проходит по куки ответа в поисках `JSESSIONID`.
- Если `JSESSIONID` найден и отличается от текущего `session_id`, обновляет `session_id` и куки в `cookies_jar`.
- Логирует предупреждение, если `JSESSIONID` не найден.

**Примеры**:
```python
ali_requests = AliRequests()
response = ali_requests.make_get_request('https://portals.aliexpress.com')
if response:
    ali_requests._handle_session_id(response.cookies)
```

### `make_get_request`

```python
def make_get_request(self, url: str, cookies: List[dict] = None, headers: dict = None):
    """ Makes a GET request with cookies.

    @param url The URL to make the GET request to.
    @param cookies List of cookies to use for the request.
    @param headers Optional headers to include in the request.

    @returns requests.Response object if successful, False otherwise.
    """
    ...
```

**Назначение**: Выполняет GET-запрос с заданными куками и заголовками.

**Параметры**:
- `url` (str): URL для выполнения GET-запроса.
- `cookies` (List[dict], optional): Список куки для использования в запросе (по умолчанию `None`).
- `headers` (dict, optional): Заголовки для включения в запрос (по умолчанию `None`).

**Возвращает**:
- `requests.Response`: Объект `requests.Response` в случае успеха, `False` в противном случае.

**Как работает функция**:
- Объединяет переданные заголовки с заголовками по умолчанию.
- Обновляет куки сессии из `cookies_jar`.
- Выполняет GET-запрос с заданным URL, заголовками и куками.
- Обрабатывает ответ, проверяя статус код и обновляя `session_id`.
- Логирует ошибки при выполнении запроса.

**Вызывает исключения**:
- `requests.RequestException`: Если происходит ошибка при выполнении запроса.
- `Exception`: При возникновении других ошибок при выполнении запроса.

**Примеры**:
```python
ali_requests = AliRequests()
response = ali_requests.make_get_request('https://portals.aliexpress.com')
if response:
    print("Запрос выполнен успешно")
else:
    print("Запрос не удался")
```

### `short_affiliate_link`

```python
def short_affiliate_link(self, link_url: str):
    """ Get a short affiliate link.

    @param link_url The URL to shorten.

    @returns requests.Response object if successful, False otherwise.
    """
    ...
```

**Назначение**: Получает короткую партнерскую ссылку для заданного URL.

**Параметры**:
- `link_url` (str): URL для сокращения.

**Возвращает**:
- `requests.Response`: Объект `requests.Response` в случае успеха, `False` в противном случае.

**Как работает функция**:
- Формирует URL для получения короткой партнерской ссылки на основе базового URL и переданного `link_url`.
- Вызывает `make_get_request` для выполнения GET-запроса и получения короткой ссылки.

**Примеры**:
```python
ali_requests = AliRequests()
response = ali_requests.short_affiliate_link('https://aliexpress.com/item/1234567890.html')
if response:
    print("Короткая ссылка получена")
else:
    print("Не удалось получить короткую ссылку")
```