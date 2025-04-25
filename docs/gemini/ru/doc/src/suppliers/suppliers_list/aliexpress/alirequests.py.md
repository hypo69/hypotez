# Модуль AliRequests

## Обзор

Модуль `alirequests.py` предоставляет класс `AliRequests`, который используется для работы с API AliExpress. 
Этот класс позволяет выполнять GET запросы к API AliExpress с использованием куки из файла веб-драйвера. 

## Подробнее

Класс `AliRequests` инициализируется с именем веб-драйвера, который используется для загрузки куки. 
По умолчанию используется `chrome`. 

Класс обеспечивает следующие функции:

- Загрузка куки из файла веб-драйвера.
- Обновление сессионных куки.
- Обработка `JSESSIONID` в ответе.
- Выполнение GET запросов с использованием куки.
- Сокращение аффилированных ссылок.

## Классы

### `class AliRequests`

**Описание**: 
Класс `AliRequests` используется для работы с API AliExpress. Он позволяет выполнять GET запросы к API AliExpress с использованием куки из файла веб-драйвера.

**Атрибуты**:

- `cookies_jar (RequestsCookieJar)`: Объект `RequestsCookieJar`, содержащий куки.
- `session_id (str)`: Сессионный ID.
- `headers (dict)`: Заголовки запросов.
- `session (requests.Session)`: Объект `requests.Session`, используемый для выполнения запросов.

**Методы**:

- `__init__(webdriver_for_cookies: str = 'chrome')`: Инициализирует класс `AliRequests`.

    **Параметры**:

    - `webdriver_for_cookies (str, optional)`: Имя веб-драйвера для загрузки куки. По умолчанию `chrome`.

- `_load_webdriver_cookies_file(webdriver_for_cookies: str = 'chrome') -> bool`: Загружает куки из файла веб-драйвера.

    **Параметры**:

    - `webdriver_for_cookies (str, optional)`: Имя веб-драйвера. По умолчанию `chrome`.

    **Возвращает**:
    - `bool`: `True`, если куки были загружены успешно, `False` в противном случае.

- `_refresh_session_cookies()`: Обновляет сессионные куки.

- `_handle_session_id(response_cookies)`: Обрабатывает `JSESSIONID` в ответе.

    **Параметры**:

    - `response_cookies`: Куки, полученные в ответе.

- `make_get_request(url: str, cookies: List[dict] = None, headers: dict = None)`: Выполняет GET запрос с использованием куки.

    **Параметры**:

    - `url (str)`: URL для запроса.
    - `cookies (List[dict], optional)`: Список куки для использования в запросе. По умолчанию `None`.
    - `headers (dict, optional)`: Дополнительные заголовки для использования в запросе. По умолчанию `None`.

    **Возвращает**:
    - `requests.Response`: Объект `requests.Response`, если запрос выполнен успешно, `False` в противном случае.

- `short_affiliate_link(link_url: str)`: Получает сокращенную аффилированную ссылку.

    **Параметры**:

    - `link_url (str)`: URL для сокращения.

    **Возвращает**:
    - `requests.Response`: Объект `requests.Response`, если запрос выполнен успешно, `False` в противном случае.

## Функции

## Примеры

### Пример создания и использования объекта `AliRequests`

```python
from src.suppliers.suppliers_list.aliexpress.alirequests import AliRequests

# Создание объекта AliRequests с использованием куки из Chrome
aliexpress_requests = AliRequests(webdriver_for_cookies='chrome')

# Выполнение GET запроса к API AliExpress
response = aliexpress_requests.make_get_request(
    url='https://api.aliexpress.com/product/v1/product/search/all',
    headers={'Accept': 'application/json'}
)

# Проверка результата запроса
if response:
    # Обработка результата запроса
    print(response.json())
else:
    print('Запрос не выполнен.')
```

## Внутренние функции

### `_load_webdriver_cookies_file`

**Описание**: 
Функция `_load_webdriver_cookies_file` загружает куки из файла веб-драйвера.

**Как работает функция**:
Функция считывает куки из файла `cookie`, который находится в директории `gs.dir_cookies/aliexpress.com/webdriver_for_cookies/`. 
Затем куки добавляются в объект `RequestsCookieJar` и обновляется объект `requests.Session`.

### `_refresh_session_cookies`

**Описание**: 
Функция `_refresh_session_cookies` обновляет сессионные куки.

**Как работает функция**:
Функция отправляет GET запрос на URL `https://portals.aliexpress.com` с использованием куки, загруженных из файла веб-драйвера. 
Затем она вызывается функция `_handle_session_id`, которая обрабатывает `JSESSIONID` в ответе.

### `_handle_session_id`

**Описание**: 
Функция `_handle_session_id` обрабатывает `JSESSIONID` в ответе.

**Как работает функция**:
Функция ищет куки `JSESSIONID` в ответе. Если куки найдены, она добавляет их в объект `RequestsCookieJar`. 
Если `JSESSIONID` не найден, выводится предупреждение в лог.

### `make_get_request`

**Описание**: 
Функция `make_get_request` выполняет GET запрос с использованием куки.

**Как работает функция**:
Функция отправляет GET запрос на указанный URL с использованием куки из объекта `RequestsCookieJar`. 
Затем она вызывается функция `_handle_session_id`, которая обрабатывает `JSESSIONID` в ответе.

### `short_affiliate_link`

**Описание**: 
Функция `short_affiliate_link` получает сокращенную аффилированную ссылку.

**Как работает функция**:
Функция отправляет GET запрос на URL `https://portals.aliexpress.com/affiportals/web/link_generator.htm` с параметрами `trackId` и `targetUrl`. 
Затем она возвращает объект `requests.Response`, который содержит сокращенную ссылку.