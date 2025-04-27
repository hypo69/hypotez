# Модуль для работы с API AliExpress

## Обзор

Модуль `alirequests` предоставляет класс `AliRequests`, который позволяет выполнять запросы к API AliExpress с использованием библиотеки `requests`. Класс `AliRequests` позволяет управлять сессионными куками, обновлять их при необходимости и получать короткие партнерские ссылки. 

## Подробности

Этот модуль используется для работы с API AliExpress в рамках проекта `hypotez`. Он обеспечивает взаимодействие с AliExpress, позволяя извлекать информацию о товарах, обновлять сессионные куки и получать короткие партнерские ссылки.

## Классы

### `AliRequests`

**Описание**: Класс `AliRequests` предназначен для выполнения запросов к API AliExpress с использованием библиотеки `requests`. Он обеспечивает управление сессионными куками, обновление их при необходимости и получение коротких партнерских ссылок.

**Атрибуты**:

- `cookies_jar` (RequestsCookieJar): Объект `RequestsCookieJar` для хранения куков.
- `session_id` (str): ID сессии, полученный из куков.
- `headers` (dict): Заголовки запросов, включающие `User-Agent`.
- `session` (requests.Session): Объект `requests.Session` для выполнения запросов.

**Методы**:

#### `__init__`

**Описание**: Инициализирует объект `AliRequests`.

**Параметры**:

- `webdriver_for_cookies` (str, optional): Имя веб-драйвера, используемого для загрузки куков. По умолчанию - "chrome".

**Возвращает**: None

**Пример**:

```python
>>> alirequests = AliRequests(webdriver_for_cookies='firefox') # Инициализация с использованием Firefox для загрузки куков
```

#### `_load_webdriver_cookies_file`

**Описание**: Загружает куки из файла веб-драйвера.

**Параметры**:

- `webdriver_for_cookies` (str, optional): Имя веб-драйвера. По умолчанию - "chrome".

**Возвращает**:

- `bool`: `True`, если куки загружены успешно, `False` в противном случае.

**Пример**:

```python
>>> alirequests._load_webdriver_cookies_file(webdriver_for_cookies='firefox') # Загрузка куков из файла Firefox
```

#### `_refresh_session_cookies`

**Описание**: Обновляет сессионные куки.

**Параметры**: None

**Возвращает**: None

**Пример**:

```python
>>> alirequests._refresh_session_cookies() # Обновление куков
```

#### `_handle_session_id`

**Описание**: Обрабатывает `JSESSIONID` из куков ответа.

**Параметры**:

- `response_cookies` (List[dict]): Куки ответа.

**Возвращает**: None

**Пример**:

```python
>>> alirequests._handle_session_id(response_cookies) # Обработка JSESSIONID
```

#### `make_get_request`

**Описание**: Выполняет GET-запрос с куками.

**Параметры**:

- `url` (str): URL для GET-запроса.
- `cookies` (List[dict], optional): Список куков для использования в запросе. По умолчанию - `None`.
- `headers` (dict, optional): Дополнительные заголовки для включения в запрос. По умолчанию - `None`.

**Возвращает**:

- `requests.Response`: Объект `requests.Response` в случае успеха, `False` в противном случае.

**Пример**:

```python
>>> response = alirequests.make_get_request('https://www.aliexpress.com') # Выполнение GET-запроса к AliExpress
```

#### `short_affiliate_link`

**Описание**: Получает короткую партнерскую ссылку.

**Параметры**:

- `link_url` (str): URL, который нужно сократить.

**Возвращает**:

- `requests.Response`: Объект `requests.Response` в случае успеха, `False` в противном случае.

**Пример**:

```python
>>> response = alirequests.short_affiliate_link('https://www.aliexpress.com/item/10000000000000.html') # Получение короткой ссылки
```

## Примеры использования

```python
from src.suppliers.suppliers_list.aliexpress.alirequests import AliRequests

alirequests = AliRequests() # Инициализация объекта AliRequests

# Загрузка куков из файла Chrome
alirequests._load_webdriver_cookies_file(webdriver_for_cookies='chrome')

# Обновление сессионных куков
alirequests._refresh_session_cookies()

# Выполнение GET-запроса к AliExpress
response = alirequests.make_get_request('https://www.aliexpress.com')

# Получение короткой партнерской ссылки
response = alirequests.short_affiliate_link('https://www.aliexpress.com/item/10000000000000.html')
```

## Как работает модуль

Модуль `alirequests` работает с API AliExpress, используя следующие шаги:

1. **Инициализация**: Создается объект `AliRequests` с указанием веб-драйвера, используемого для загрузки куков. 
2. **Загрузка куков**: Куки загружаются из файла веб-драйвера.
3. **Обновление куков**: Сессионные куки обновляются, чтобы гарантировать их актуальность.
4. **Выполнение запросов**: Выполняются GET-запросы к API AliExpress с использованием куков и заголовков запросов.
5. **Обработка ответа**: Ответы от API AliExpress обрабатываются, извлекаются нужные данные, а также обрабатывается `JSESSIONID`.
6. **Получение коротких ссылок**: Функция `short_affiliate_link` позволяет получить сокращенную партнерскую ссылку для заданного URL.

## Детализация параметров

### `webdriver_for_cookies`

- **Описание**: Имя веб-драйвера, используемого для загрузки куков.
- **Тип**: str
- **Значения**: 'chrome', 'firefox', 'playwright'
- **По умолчанию**: 'chrome'
- **Пример**: `alirequests = AliRequests(webdriver_for_cookies='firefox')`
- **Подробности**:  Этот параметр указывает, какой веб-драйвер использовать для загрузки куков. Файлы куков должны находиться в соответствующей папке `gs.dir_cookies` в проекте `hypotez`. 

### `link_url`

- **Описание**: URL, который нужно сократить.
- **Тип**: str
- **Пример**: `alirequests.short_affiliate_link('https://www.aliexpress.com/item/10000000000000.html')`
- **Подробности**: Этот параметр представляет собой URL, который будет обработан для получения короткой партнерской ссылки.

## Примеры

### Инициализация с использованием Chrome

```python
alirequests = AliRequests()
```

### Инициализация с использованием Firefox

```python
alirequests = AliRequests(webdriver_for_cookies='firefox')
```

### Загрузка куков из файла Firefox

```python
alirequests._load_webdriver_cookies_file(webdriver_for_cookies='firefox')
```

### Выполнение GET-запроса к AliExpress

```python
response = alirequests.make_get_request('https://www.aliexpress.com')
```

### Получение короткой партнерской ссылки

```python
response = alirequests.short_affiliate_link('https://www.aliexpress.com/item/10000000000000.html')
```

## Дополнительная информация

- **Логирование**: Модуль использует `logger` из модуля `src.logger.logger` для записи сообщений о работе и ошибках.
- **Обработка ошибок**: Модуль включает обработку исключений для различных ошибок, которые могут возникнуть при выполнении запросов к API AliExpress.
- **Совместимость**: Модуль `alirequests` работает с различными версиями библиотеки `requests`.