# Модуль для работы с запросами к AliExpress

## Обзор

Модуль `alirequests.py` предназначен для упрощения выполнения HTTP-запросов к AliExpress с использованием библиотеки `requests`. Он включает в себя функциональность для управления cookie, обновления сессий и создания коротких партнерских ссылок. Модуль обеспечивает логирование ошибок и успешных операций через библиотеку `src.logger`.

## Подробней

Этот модуль предоставляет класс `AliRequests`, который облегчает взаимодействие с API AliExpress. Он автоматически загружает и обновляет cookies, что необходимо для авторизованных запросов. Класс также предоставляет методы для выполнения GET-запросов и создания коротких партнерских ссылок, что делает его полезным инструментом для парсинга и автоматизации задач, связанных с AliExpress.

## Классы

### `AliRequests`

**Описание**:
Класс `AliRequests` предназначен для работы с запросами к AliExpress с использованием библиотеки `requests`.

**Атрибуты**:
- `cookies_jar` (RequestsCookieJar): Объект для хранения и управления cookies.
- `session_id` (str): Идентификатор сессии.
- `headers` (dict): Заголовки HTTP-запроса, включая User-Agent.
- `session` (requests.Session): Объект сессии requests для выполнения запросов.

**Методы**:
- `__init__(webdriver_for_cookies: str = 'chrome')`: Инициализирует класс `AliRequests` и загружает cookies из файла.
- `_load_webdriver_cookies_file(webdriver_for_cookies: str = 'chrome') -> bool`: Загружает cookies из файла, созданного webdriver.
- `_refresh_session_cookies()`: Обновляет cookies сессии.
- `_handle_session_id(response_cookies)`: Обрабатывает JSESSIONID в cookies ответа.
- `make_get_request(url: str, cookies: List[dict] = None, headers: dict = None)`: Выполняет GET-запрос с заданными cookies и заголовками.
- `short_affiliate_link(link_url: str)`: Создает короткую партнерскую ссылку.

#### `__init__`

```python
def __init__(self, webdriver_for_cookies: str = 'chrome'):
    """Инициализирует класс AliRequests.

    Args:
        webdriver_for_cookies (str, optional): Имя веб-драйвера для загрузки cookies. По умолчанию 'chrome'.
    """
```

**Назначение**:
Инициализирует экземпляр класса `AliRequests`, устанавливает заголовки User-Agent, создает сессию `requests` и загружает cookies из файла, если он существует.

**Как работает функция**:
1. Инициализирует `cookies_jar` как экземпляр `RequestsCookieJar` для хранения cookies.
2. Устанавливает `session_id` в `None`.
3. Определяет `headers`, используя случайный `User-Agent` для имитации реального пользователя.
4. Создает экземпляр `requests.Session` для выполнения запросов.
5. Вызывает `_load_webdriver_cookies_file` для загрузки cookies из файла, специфичного для указанного веб-драйвера.

#### `_load_webdriver_cookies_file`

```python
def _load_webdriver_cookies_file(self, webdriver_for_cookies: str = 'chrome') -> bool:
    """Загружает cookies из файла, созданного webdriver.

    Args:
        webdriver_for_cookies (str, optional): Имя веб-драйвера. По умолчанию 'chrome'.

    Returns:
        bool: `True`, если cookies успешно загружены, `False` в противном случае.
    """
```

**Назначение**:
Загружает cookies из файла, который был сохранен веб-драйвером (например, Chrome).

**Как работает функция**:
1. Формирует путь к файлу cookie на основе переданного имени веб-драйвера и директории `gs.dir_cookies`.
2. Открывает файл cookie в бинарном режиме (`'rb'`).
3. Использует `pickle.load` для десериализации списка cookie.
4. Итерируется по списку cookie и добавляет их в `cookies_jar`. При этом учитываются параметры cookie, такие как домен, путь, secure, HttpOnly, SameSite и expirationDate.
5. Логирует успешную загрузку cookies.
6. В случае ошибки (например, файл не найден или ошибка десериализации) логирует ошибку и возвращает `False`.

**Примеры**:

```python
ali_requests = AliRequests(webdriver_for_cookies='chrome')
success = ali_requests._load_webdriver_cookies_file(webdriver_for_cookies='chrome')
if success:
    print("Cookies успешно загружены")
else:
    print("Не удалось загрузить cookies")
```

#### `_refresh_session_cookies`

```python
def _refresh_session_cookies(self):
    """Обновляет cookies сессии."""
```

**Назначение**:
Обновляет cookies сессии, выполняя GET-запрос к `https://portals.aliexpress.com`.

**Как работает функция**:
1. Определяет URL для обновления cookies.
2. Выполняет GET-запрос с использованием текущей сессии и заголовков. Если `cookies_jar` не пустой, добавляет cookies из него в запрос.
3. Вызывает `_handle_session_id` для обработки и обновления `JSESSIONID` из cookies ответа.
4. Логирует ошибки, если запрос не удался или произошла другая ошибка.

**Примеры**:

```python
ali_requests = AliRequests(webdriver_for_cookies='chrome')
ali_requests._refresh_session_cookies()
```

#### `_handle_session_id`

```python
def _handle_session_id(self, response_cookies):
    """Обрабатывает JSESSIONID в cookies ответа.

    Args:
        response_cookies: Cookies, полученные в ответе на HTTP-запрос.
    """
```

**Назначение**:
Обрабатывает `JSESSIONID` в cookies ответа, сравнивает с текущим `session_id` и обновляет, если необходимо.

**Как работает функция**:
1. Итерируется по cookies ответа.
2. Если находит cookie с именем `JSESSIONID`, сравнивает его значение с текущим `session_id`.
3. Если `session_id` изменился, обновляет `session_id` и добавляет cookie в `cookies_jar`.
4. Логирует предупреждение, если `JSESSIONID` не найден в cookies ответа.

**Примеры**:

```python
import requests
ali_requests = AliRequests(webdriver_for_cookies='chrome')
response = requests.get('https://portals.aliexpress.com')
ali_requests._handle_session_id(response.cookies)
```

#### `make_get_request`

```python
def make_get_request(self, url: str, cookies: List[dict] = None, headers: dict = None):
    """Выполняет GET-запрос с cookies.

    Args:
        url (str): URL для выполнения GET-запроса.
        cookies (List[dict], optional): Список cookies для использования в запросе. По умолчанию `None`.
        headers (dict, optional): Заголовки для включения в запрос. По умолчанию `None`.

    Returns:
        requests.Response: Объект `requests.Response` в случае успеха, `False` в противном случае.
    """
```

**Назначение**:
Выполняет GET-запрос к указанному URL с заданными cookies и заголовками.

**Как работает функция**:
1. Устанавливает заголовки запроса, используя переданные параметры или значения по умолчанию из `self.headers`.
2. Обновляет cookies сессии, добавляя cookies из `self.cookies_jar`.
3. Выполняет GET-запрос с использованием `self.session`.
4. Вызывает `resp.raise_for_status()` для проверки статуса ответа и возбуждения исключения в случае ошибки.
5. Вызывает `_handle_session_id` для обработки и обновления `JSESSIONID` из cookies ответа.
6. В случае успеха возвращает объект `requests.Response`.
7. В случае ошибки логирует ошибку и возвращает `False`.

**Примеры**:

```python
ali_requests = AliRequests(webdriver_for_cookies='chrome')
response = ali_requests.make_get_request(url='https://www.aliexpress.com')
if response:
    print("Запрос успешен")
else:
    print("Запрос не удался")
```

#### `short_affiliate_link`

```python
def short_affiliate_link(self, link_url: str):
    """Получает короткую партнерскую ссылку.

    Args:
        link_url (str): URL для сокращения.

    Returns:
        requests.Response: Объект `requests.Response` в случае успеха, `False` в противном случае.
    """
```

**Назначение**:
Создает короткую партнерскую ссылку на основе переданного URL.

**Как работает функция**:
1. Формирует URL для создания короткой ссылки, используя базовый URL `https://portals.aliexpress.com/affiportals/web/link_generator.htm`, trackId и переданный `link_url`.
2. Вызывает `self.make_get_request` для выполнения GET-запроса к сформированному URL.
3. Возвращает результат выполнения `self.make_get_request`.

**Примеры**:

```python
ali_requests = AliRequests(webdriver_for_cookies='chrome')
response = ali_requests.short_affiliate_link(link_url='https://www.aliexpress.com/item/1234567890.html')
if response:
    print("Запрос успешен")
else:
    print("Запрос не удался")