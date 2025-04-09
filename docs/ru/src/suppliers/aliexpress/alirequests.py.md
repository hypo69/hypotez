# Модуль для выполнения запросов к AliExpress

## Обзор

Модуль `alirequests.py` предназначен для обработки HTTP-запросов к AliExpress с использованием библиотеки `requests`. Он включает в себя функциональность для управления cookie, пользовательскими агентами и сессиями. Основной класс `AliRequests` предоставляет методы для загрузки cookie из файлов, обновления сессионных cookie и выполнения GET-запросов.

## Подробней

Этот модуль играет важную роль в проекте `hypotez`, обеспечивая взаимодействие с AliExpress API. Он позволяет автоматически управлять сессиями и cookie, что необходимо для обхода ограничений и обеспечения стабильной работы парсера. Модуль использует файлы cookie для аутентификации и сохранения состояния сессии между запросами.

## Классы

### `AliRequests`

**Описание**: Класс `AliRequests` предназначен для обработки запросов к AliExpress с использованием библиотеки `requests`.

**Принцип работы**:
1.  **Инициализация**: При инициализации класса загружаются cookie из файла, генерируется случайный User-Agent и создается сессия `requests.Session()`.
2.  **Загрузка Cookie**: Cookie загружаются из файла, расположенного в директории `gs.dir_cookies` (например, `aliexpress.com/chrome/cookie`). Cookie используются для аутентификации и сохранения состояния сессии.
3.  **Управление сессией**: Класс обеспечивает обновление сессионных cookie и обработку `JSESSIONID` для поддержания активной сессии.
4.  **Выполнение запросов**: Предоставляет метод `make_get_request` для выполнения GET-запросов с заданными параметрами (URL, cookie, заголовки).
5.  **Сокращение ссылок**: Включает метод `short_affiliate_link` для получения коротких партнерских ссылок.

**Аттрибуты**:

*   `cookies_jar` (RequestsCookieJar): Объект для хранения cookie.
*   `session_id` (str): Идентификатор сессии.
*   `headers` (dict): Заголовки для HTTP-запросов, включая User-Agent.
*   `session` (requests.Session): Объект сессии requests.

**Методы**:

*   `__init__(webdriver_for_cookies: str = 'chrome')`: Инициализирует класс `AliRequests`.
*   `_load_webdriver_cookies_file(webdriver_for_cookies: str = 'chrome') -> bool`: Загружает cookie из файла веб-драйвера.
*   `_refresh_session_cookies()`: Обновляет сессионные cookie.
*   `_handle_session_id(response_cookies)`: Обрабатывает `JSESSIONID` в cookie ответа.
*   `make_get_request(url: str, cookies: List[dict] = None, headers: dict = None)`: Выполняет GET-запрос с заданными cookie и заголовками.
*   `short_affiliate_link(link_url: str)`: Получает короткую партнерскую ссылку.

## Функции

### `_load_webdriver_cookies_file`

```python
def _load_webdriver_cookies_file(self, webdriver_for_cookies: str = 'chrome') -> bool:
    """ Загружает cookies из файла веб-драйвера.

    Args:
        webdriver_for_cookies (str, optional): Имя веб-драйвера. По умолчанию 'chrome'.

    Returns:
        bool: `True`, если cookie успешно загружены, иначе `False`.
    
    Raises:
        FileNotFoundError: Если файл с cookie не найден.
        ValueError: Если файл с cookie содержит некорректные данные.
        Exception: При возникновении любой другой ошибки.
    
    """
    ...
```

**Назначение**: Загрузка cookie из файла, созданного веб-драйвером (например, Chrome или Firefox).

**Параметры**:

*   `webdriver_for_cookies` (str): Имя веб-драйвера, для которого загружаются cookie (по умолчанию `'chrome'`).

**Возвращает**:

*   `bool`: `True`, если cookie успешно загружены, `False` в противном случае.

**Вызывает исключения**:

*   `FileNotFoundError`: Если файл с cookie не найден.
*   `ValueError`: Если файл с cookie содержит некорректные данные.
*   `Exception`: При возникновении любой другой ошибки.

**Как работает функция**:

1.  **Определение пути к файлу**: Формируется путь к файлу cookie на основе переданного имени веб-драйвера и директории хранения cookie (`gs.dir_cookies`).
2.  **Чтение файла**: Файл открывается в бинарном режиме (`'rb'`) и считывается содержимое с помощью `pickle.load()`.
3.  **Обработка cookie**: Загруженные cookie итерируются, и каждый cookie добавляется в `self.cookies_jar` с соответствующими атрибутами (имя, значение, домен, путь, параметры безопасности и срок действия).
4.  **Обновление сессионных cookie**: После загрузки cookie вызывается метод `self._refresh_session_cookies()` для обновления cookie в сессии.
5.  **Обработка исключений**: В случае возникновения исключений (`FileNotFoundError`, `ValueError`, `Exception`) в процессе чтения или обработки файла, в лог записывается сообщение об ошибке, и функция возвращает `False`.

```
    Определение пути к файлу cookie
    │
    ├── Открытие файла cookie в бинарном режиме ('rb')
    │   │
    │   ├── Успешно: Загрузка содержимого файла с помощью pickle.load()
    │   │   │
    │   │   ├── Итерация по загруженным cookie
    │   │   │   │
    │   │   │   ├── Добавление каждого cookie в self.cookies_jar с атрибутами
    │   │   │   │   │
    │   │   │   │   └── Вызов self._refresh_session_cookies() для обновления cookie в сессии
    │   │   │   │
    │   │   │   └── Запись в лог об успешной загрузке cookie
    │   │   │
    │   │   └── Ошибка: Запись в лог об ошибке и возврат False
    │   │
    │   └── Ошибка: Запись в лог об ошибке и возврат False
    │
    └── Файл не найден: Запись в лог об ошибке и возврат False
```

**Примеры**:

```python
# Пример успешной загрузки cookie
ali_requests = AliRequests()
result = ali_requests._load_webdriver_cookies_file('chrome')
print(result)  # Вывод: True

# Пример неудачной загрузки cookie из-за отсутствия файла
ali_requests = AliRequests()
result = ali_requests._load_webdriver_cookies_file('nonexistent_driver')
print(result)  # Вывод: False
```

### `_refresh_session_cookies`

```python
def _refresh_session_cookies(self):
    """ Обновляет сессионные cookie.
    
    Args:
        Отсутствуют

    Returns:
        Отсутствует
    
    Raises:
        requests.RequestException: При ошибке выполнения запроса.
        Exception: При возникновении любой другой ошибки.
   
    """
    ...
```

**Назначение**: Обновление сессионных cookie путем выполнения GET-запроса к `https://portals.aliexpress.com`.

**Параметры**:

*   Отсутствуют

**Возвращает**:

*   Отсутствует

**Вызывает исключения**:

*   `requests.RequestException`: При ошибке выполнения запроса.
*   `Exception`: При возникновении любой другой ошибки.

**Как работает функция**:

1.  **Определение URL**: Устанавливается URL для обновления cookie (`https://portals.aliexpress.com`).
2.  **Выполнение GET-запроса**: Выполняется GET-запрос к указанному URL с использованием `self.session`. Если в `self.cookies_jar` есть cookie, они передаются в запросе.
3.  **Обработка ответа**: После получения ответа вызывается метод `self._handle_session_id()` для обработки `JSESSIONID` из cookie ответа.
4.  **Обработка исключений**: В случае возникновения исключений (`requests.RequestException`, `Exception`) в процессе выполнения запроса, в лог записывается сообщение об ошибке.

```
    Определение URL для обновления cookie
    │
    ├── Выполнение GET-запроса с использованием self.session
    │   │
    │   ├── Успешно: Вызов self._handle_session_id() для обработки JSESSIONID
    │   │
    │   └── Ошибка: Запись в лог об ошибке
    │
    └── Ошибка: Запись в лог об ошибке
```

**Примеры**:

```python
# Пример обновления сессионных cookie
ali_requests = AliRequests()
ali_requests._refresh_session_cookies()
```

### `_handle_session_id`

```python
def _handle_session_id(self, response_cookies):
    """ Обрабатывает JSESSIONID в cookie ответа.

    Args:
        response_cookies: (объект requests.cookies) - cookie, полученные в ответе на HTTP-запрос.

    Returns:
       Отсутствует
    
    Raises:
        Отсутствует
    
    """
    ...
```

**Назначение**: Обработка cookie `JSESSIONID` из ответа сервера.

**Параметры**:

*   `response_cookies` (объект `requests.cookies`): Cookie, полученные в ответе на HTTP-запрос.

**Возвращает**:

*   Отсутствует

**Вызывает исключения**:

*   Отсутствуют

**Как работает функция**:

1.  **Поиск JSESSIONID**: Функция итерируется по cookie в `response_cookies` для поиска cookie с именем `JSESSIONID`.
2.  **Проверка и обновление**: Если `JSESSIONID` найден, проверяется, отличается ли его значение от текущего значения `self.session_id`. Если значение отличается или `self.session_id` не установлен, `self.session_id` обновляется, и cookie добавляется в `self.cookies_jar`.
3.  **Предупреждение**: Если `JSESSIONID` не найден в cookie ответа, в лог записывается предупреждение.

```
    Итерация по cookie в response_cookies
    │
    ├── JSESSIONID найден
    │   │
    │   ├── Значение JSESSIONID отличается от self.session_id
    │   │   │
    │   │   ├── Обновление self.session_id и добавление cookie в self.cookies_jar
    │   │   │
    │   │   └── Значение JSESSIONID совпадает с self.session_id: выход
    │   │
    │   └── JSESSIONID не найден
    │       │
    │       └── Запись предупреждения в лог
    │
    └── Итерация завершена
```

**Примеры**:

```python
# Пример обработки JSESSIONID
import requests

ali_requests = AliRequests()
response = requests.get('https://portals.aliexpress.com')
ali_requests._handle_session_id(response.cookies)
```

### `make_get_request`

```python
def make_get_request(self, url: str, cookies: List[dict] = None, headers: dict = None):
    """ Выполняет GET-запрос с cookie.

    Args:
        url (str): URL для выполнения GET-запроса.
        cookies (List[dict], optional): Список cookie для использования в запросе. По умолчанию `None`.
        headers (dict, optional): Дополнительные заголовки для включения в запрос. По умолчанию `None`.

    Returns:
        requests.Response | bool: Объект `requests.Response` при успехе, `False` в противном случае.
    
    Raises:
        requests.RequestException: При ошибке выполнения запроса.
        Exception: При возникновении любой другой ошибки.
   
    """
    ...
```

**Назначение**: Выполнение GET-запроса с заданными параметрами (URL, cookie, заголовки).

**Параметры**:

*   `url` (str): URL для выполнения GET-запроса.
*   `cookies` (List[dict], optional): Список cookie для использования в запросе. По умолчанию `None`.
*   `headers` (dict, optional): Дополнительные заголовки для включения в запрос. По умолчанию `None`.

**Возвращает**:

*   `requests.Response`: Объект `requests.Response` при успехе, `False` в противном случае.

**Вызывает исключения**:

*   `requests.RequestException`: При ошибке выполнения запроса.
*   `Exception`: При возникновении любой другой ошибки.

**Как работает функция**:

1.  **Обновление cookie**: Cookie из `self.cookies_jar` добавляются в сессию.
2.  **Выполнение GET-запроса**: Выполняется GET-запрос к указанному URL с использованием `self.session` и переданных заголовков.
3.  **Обработка ответа**: Проверяется статус ответа (`resp.raise_for_status()`). В случае ошибки (например, 404, 500) вызывается исключение `requests.RequestException`. Также вызывается метод `self._handle_session_id()` для обработки `JSESSIONID` из cookie ответа.
4.  **Обработка исключений**: В случае возникновения исключений (`requests.RequestException`, `Exception`) в процессе выполнения запроса, в лог записывается сообщение об ошибке, и функция возвращает `False`.

```
    Обновление cookie в сессии
    │
    ├── Выполнение GET-запроса с использованием self.session
    │   │
    │   ├── Успешно: Проверка статуса ответа (resp.raise_for_status())
    │   │   │
    │   │   ├── Успешно: Вызов self._handle_session_id() для обработки JSESSIONID и возврат объекта Response
    │   │   │
    │   │   └── Ошибка: Запись в лог об ошибке и возврат False
    │   │
    │   └── Ошибка: Запись в лог об ошибке и возврат False
    │
    └── Ошибка: Запись в лог об ошибке и возврат False
```

**Примеры**:

```python
# Пример выполнения GET-запроса
ali_requests = AliRequests()
response = ali_requests.make_get_request('https://www.aliexpress.com/')
if response:
    print(f'Status code: {response.status_code}')
else:
    print('Request failed')
```

### `short_affiliate_link`

```python
def short_affiliate_link(self, link_url: str):
    """ Получает короткую партнерскую ссылку.

    Args:
        link_url (str): URL для сокращения.

    Returns:
        requests.Response | bool: Объект `requests.Response` при успехе, `False` в противном случае.
    
    Raises:
        Отсутствуют
   
    """
    ...
```

**Назначение**: Получение короткой партнерской ссылки через AliExpress API.

**Параметры**:

*   `link_url` (str): URL для сокращения.

**Возвращает**:

*   `requests.Response`: Объект `requests.Response` при успехе, `False` в противном случае.

**Вызывает исключения**:

*   Отсутствуют

**Как работает функция**:

1.  **Формирование URL**: Формируется URL для запроса короткой партнерской ссылки на основе переданного `link_url` и идентификатора трека (`track_id`).
2.  **Выполнение GET-запроса**: Вызывается метод `self.make_get_request()` для выполнения GET-запроса к сформированному URL. Результат этого запроса возвращается как результат работы функции.

```
    Формирование URL для запроса короткой партнерской ссылки
    │
    └── Вызов self.make_get_request() для выполнения GET-запроса
        │
        └── Возврат результата запроса
```

**Примеры**:

```python
# Пример получения короткой партнерской ссылки
ali_requests = AliRequests()
response = ali_requests.short_affiliate_link('https://www.aliexpress.com/item/1234567890.html')
if response:
    print(f'Status code: {response.status_code}')
else:
    print('Request failed')