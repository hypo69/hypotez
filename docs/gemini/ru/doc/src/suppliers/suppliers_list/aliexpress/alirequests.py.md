# Модуль `alirequests.py`

## Обзор

Модуль `alirequests.py` предназначен для выполнения запросов к AliExpress с использованием библиотеки `requests`. Он включает в себя функциональность для управления куки, обработки сессий и создания партнерских ссылок. Модуль обеспечивает удобный интерфейс для взаимодействия с API AliExpress, обрабатывая ошибки и логируя действия.

## Подробней

Этот модуль предоставляет класс `AliRequests`, который инкапсулирует логику для работы с запросами к AliExpress. Он загружает куки из файла, поддерживает сессии, обрабатывает идентификаторы сессий и предоставляет методы для выполнения GET-запросов и получения коротких партнерских ссылок.

## Классы

### `AliRequests`

**Описание**: Класс `AliRequests` предназначен для обработки запросов к AliExpress с использованием библиотеки `requests`.

**Атрибуты**:
- `cookies_jar` (RequestsCookieJar): Объект для хранения и управления куки.
- `session_id` (str): Идентификатор текущей сессии.
- `headers` (dict): Заголовки HTTP-запросов, включая User-Agent.
- `session` (requests.Session): Объект сессии requests для выполнения запросов.

**Методы**:
- `__init__(webdriver_for_cookies: str = 'chrome')`: Инициализирует класс `AliRequests`, загружает куки из файла, создает сессию requests и устанавливает заголовки.
- `_load_webdriver_cookies_file(webdriver_for_cookies: str = 'chrome') -> bool`: Загружает куки из файла, созданного веб-драйвером.
- `_refresh_session_cookies()`: Обновляет куки сессии, выполняя GET-запрос к AliExpress.
- `_handle_session_id(response_cookies)`: Обрабатывает идентификатор сессии JSESSIONID, полученный в куках ответа.
- `make_get_request(url: str, cookies: List[dict] = None, headers: dict = None)`: Выполняет GET-запрос с заданными куки и заголовками.
- `short_affiliate_link(link_url: str)`: Генерирует короткую партнерскую ссылку для заданного URL.

### `__init__`

```python
def __init__(self, webdriver_for_cookies: str = 'chrome'):
    """ Initializes the AliRequests class.

    @param webdriver_for_cookies The name of the webdriver for loading cookies.
    """
    self.cookies_jar = RequestsCookieJar()
    self.session_id = None
    self.headers = {'User-Agent': UserAgent().random}
    self.session = requests.Session()

    self._load_webdriver_cookies_file(webdriver_for_cookies)
```

**Назначение**: Инициализирует экземпляр класса `AliRequests`.

**Параметры**:
- `webdriver_for_cookies` (str, optional): Имя веб-драйвера для загрузки куки. По умолчанию `'chrome'`.

**Как работает функция**:
- Инициализирует `cookies_jar` как экземпляр `RequestsCookieJar` для хранения куки.
- Устанавливает `session_id` в `None`.
- Устанавливает `headers` с рандомным `User-Agent`.
- Создает экземпляр `requests.Session` для `session`.
- Вызывает метод `_load_webdriver_cookies_file` для загрузки куки из файла.

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
    cookie_file_path = Path(gs.dir_cookies, 'aliexpress.com', webdriver_for_cookies, 'cookie')

    try:
        with open(cookie_file_path, 'rb') as file:
            cookies_list = pickle.load(file)
            for cookie in cookies_list:
                self.cookies_jar.set(
                    cookie['name'],
                    cookie['value'],
                    domain=cookie.get('domain', ''),
                    path=cookie.get('path', '/'),
                    secure=bool(cookie.get('secure', False)),
                    rest={'HttpOnly': cookie.get('HttpOnly', 'false'), 'SameSite': cookie.get('SameSite', 'unspecified')},
                    expires=cookie.get('expirationDate')
                )
            logger.success(f"Cookies loaded from {cookie_file_path}")
            self._refresh_session_cookies()  # Refresh session cookies after loading
            return True
    except (FileNotFoundError, ValueError) as ex:
        logger.error(f"Failed to load cookies from {cookie_file_path}", ex)
        return False
    except Exception as ex:
        logger.error("An error occurred while loading cookies", ex)
        return False
```

**Назначение**: Загружает куки из файла, созданного веб-драйвером.

**Параметры**:
- `webdriver_for_cookies` (str, optional): Имя веб-драйвера. По умолчанию `'chrome'`.

**Возвращает**:
- `bool`: `True`, если куки успешно загружены, `False` в противном случае.

**Как работает функция**:
- Формирует путь к файлу с куками на основе переданного имени веб-драйвера.
- Открывает файл с куками, загружает их с помощью `pickle.load`.
- Итерируется по списку куки и устанавливает их в `cookies_jar`.
- Логирует успешную загрузку куки или ошибки, если они возникают.
- Вызывает метод `_refresh_session_cookies` для обновления куки сессии.

**Примеры**:
```python
ali_requests = AliRequests()
success = ali_requests._load_webdriver_cookies_file(webdriver_for_cookies='firefox')
if success:
    print("Куки успешно загружены")
else:
    print("Не удалось загрузить куки")
```

### `_refresh_session_cookies`

```python
def _refresh_session_cookies(self):
    """ Refreshes session cookies."""
    url = 'https://portals.aliexpress.com'
    try:
        if self.cookies_jar:
            resp = self.session.get(url, headers=self.headers, cookies=self.cookies_jar)
        else:
            resp = self.session.get(url, headers=self.headers)

        self._handle_session_id(resp.cookies)
    except requests.RequestException as ex:
        logger.error(f"Failed to refresh session cookies from {url}", ex)
    except Exception as ex:
        logger.error("An error occurred while refreshing session cookies", ex)
```

**Назначение**: Обновляет куки сессии, выполняя GET-запрос к AliExpress.

**Как работает функция**:
- Определяет URL для обновления куки сессии (`https://portals.aliexpress.com`).
- Выполняет GET-запрос к указанному URL, используя `requests.session`.
- Если `cookies_jar` не пустой, передает куки в запросе.
- Вызывает метод `_handle_session_id` для обработки идентификатора сессии JSESSIONID из куки ответа.
- Логирует ошибки, если они возникают при выполнении запроса.

**Примеры**:
```python
ali_requests = AliRequests()
ali_requests._refresh_session_cookies()
```

### `_handle_session_id`

```python
def _handle_session_id(self, response_cookies):
    """ Handles the JSESSIONID in response cookies."""
    session_id_found = False
    for cookie in response_cookies:
        if cookie.name == 'JSESSIONID':
            if self.session_id == cookie.value:
                return
            self.session_id = cookie.value
            self.cookies_jar.set(
                cookie.name,
                cookie.value,
                domain=cookie.domain,
                path=cookie.path,
                secure=cookie.secure,
                rest={'HttpOnly': cookie._rest.get('HttpOnly', 'false'), 'SameSite': cookie._rest.get('SameSite', 'unspecified')},
                expires=cookie.expires
            )
            session_id_found = True
            break

    if not session_id_found:
        logger.warning("JSESSIONID not found in response cookies")
```

**Назначение**: Обрабатывает идентификатор сессии JSESSIONID, полученный в куках ответа.

**Параметры**:
- `response_cookies`: Куки, полученные в ответе на HTTP-запрос.

**Как работает функция**:
- Итерируется по кукам в `response_cookies`.
- Если находит куку с именем `JSESSIONID`, сравнивает ее значение с текущим `session_id`.
- Если значение изменилось, обновляет `session_id` и устанавливает куку в `cookies_jar`.
- Если `JSESSIONID` не найден, логирует предупреждение.

**Примеры**:
```python
ali_requests = AliRequests()
response = ali_requests.make_get_request('https://example.com')
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
    headers = headers or self.headers
    try:
        self.session.cookies.update(self.cookies_jar)
        resp = self.session.get(url, headers=headers)
        resp.raise_for_status()

        self._handle_session_id(resp.cookies)

        return resp
    except requests.RequestException as ex:
        logger.error(f"Request to {url} failed", ex)
        return False
    except Exception as ex:
        logger.error(f"An error occurred while making a GET request to {url}", ex)
        return False
```

**Назначение**: Выполняет GET-запрос с заданными куки и заголовками.

**Параметры**:
- `url` (str): URL для выполнения GET-запроса.
- `cookies` (List[dict], optional): Список куки для использования в запросе. По умолчанию `None`.
- `headers` (dict, optional): Заголовки для включения в запрос. По умолчанию `None`.

**Возвращает**:
- `requests.Response`: Объект `requests.Response` в случае успеха, `False` в противном случае.

**Как работает функция**:
- Объединяет переданные заголовки с заголовками экземпляра класса.
- Обновляет куки сессии с использованием `cookies_jar`.
- Выполняет GET-запрос к указанному URL с заданными заголовками.
- Вызывает `resp.raise_for_status()` для проверки статуса ответа.
- Вызывает метод `_handle_session_id` для обработки идентификатора сессии JSESSIONID из куки ответа.
- Логирует ошибки, если они возникают при выполнении запроса.

**Примеры**:
```python
ali_requests = AliRequests()
response = ali_requests.make_get_request('https://example.com')
if response:
    print(f"Статус код: {response.status_code}")
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
    base_url = 'https://portals.aliexpress.com/affiportals/web/link_generator.htm'
    track_id = 'default'
    url = f"{base_url}?trackId={track_id}&targetUrl={link_url}"
    return self.make_get_request(url)
```

**Назначение**: Генерирует короткую партнерскую ссылку для заданного URL.

**Параметры**:
- `link_url` (str): URL для которого нужно создать короткую партнерскую ссылку.

**Возвращает**:
- `requests.Response`: Объект `requests.Response` в случае успеха, `False` в противном случае.

**Как работает функция**:
- Формирует URL для запроса короткой партнерской ссылки на основе `base_url`, `track_id` и `link_url`.
- Вызывает метод `make_get_request` для выполнения GET-запроса к сформированному URL.

**Примеры**:
```python
ali_requests = AliRequests()
response = ali_requests.short_affiliate_link('https://example.com')
if response:
    print(f"Короткая партнерская ссылка: {response.url}")
else:
    print("Не удалось получить короткую партнерскую ссылку")