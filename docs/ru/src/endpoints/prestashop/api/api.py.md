# Модуль для взаимодействия с PrestaShop API

## Обзор

Модуль `src.endpoints.prestashop.api` предоставляет класс `PrestaShop` для взаимодействия с PrestaShop webservice API, используя JSON и XML для форматирования сообщений. Он поддерживает CRUD операции, поиск и загрузку изображений, с обработкой ошибок для ответов.

## Подробней

Этот модуль предназначен для упрощения взаимодействия с PrestaShop API, предоставляя удобные методы для выполнения различных операций, таких как создание, чтение, обновление и удаление данных, а также для поиска и загрузки изображений. Модуль поддерживает форматы данных JSON и XML и включает обработку ошибок для обеспечения надежности работы.

## Классы

### `Config`

**Описание**: Класс конфигурации для API PrestaShop.

**Принцип работы**: Этот класс определяет параметры конфигурации, такие как язык, версия PrestaShop, режим работы (разработка, продакшн), формат POST-запросов, домен API и ключ API. Он использует переменные окружения, если `USE_ENV` установлен в `True`, или значения по умолчанию для различных режимов работы.

**Аттрибуты**:

-   `language` (str): Язык, используемый в конфигурации.
-   `ps_version` (str): Версия PrestaShop (по умолчанию '').
-   `MODE` (str): Определяет конечную точку API (`dev`, `dev8`, `prod`).
-   `POST_FORMAT` (str): Формат данных для POST-запросов (по умолчанию 'XML').
-   `API_DOMAIN` (str): Домен API PrestaShop.
-   `API_KEY` (str): Ключ API PrestaShop.

### `PrestaShop`

**Описание**: Класс для взаимодействия с PrestaShop webservice API.

**Принцип работы**: Этот класс предоставляет методы для взаимодействия с PrestaShop API, позволяя выполнять CRUD-операции, поиск и загрузку изображений. Он также обеспечивает обработку ошибок и методы для работы с данными API.

**Аттрибуты**:

-   `client` (Session): Сессия для выполнения HTTP-запросов.
-   `debug` (bool): Флаг для активации режима отладки (по умолчанию `False`).
-   `language` (Optional[int]): ID языка по умолчанию (по умолчанию `None`).
-   `data_format` (str): Формат данных по умолчанию (`JSON` или `XML`, по умолчанию `'JSON'`).
-   `ps_version` (str): Версия PrestaShop.
-   `api_domain` (str): Домен API PrestaShop.
-   `api_key` (str): Ключ API PrestaShop.

**Методы**:

-   `__init__`: Инициализирует класс `PrestaShop`.
-   `ping`: Проверяет работоспособность веб-сервиса.
-   `_check_response`: Проверяет код состояния ответа и обрабатывает ошибки.
-   `_parse_response_error`: Анализирует ответ об ошибке от API PrestaShop.
-   `_prepare_url`: Подготавливает URL для запроса.
-   `_exec`: Выполняет HTTP-запрос к API PrestaShop.
-   `_parse_response`: Преобразует XML или JSON ответ от API в структуру dict.
-   `create`: Создает новый ресурс в API PrestaShop.
-   `read`: Читает ресурс из API PrestaShop.
-   `write`: Обновляет существующий ресурс в API PrestaShop.
-   `unlink`: Удаляет ресурс из API PrestaShop.
-   `search`: Выполняет поиск ресурсов в API PrestaShop.
-   `create_binary`: Загружает бинарный файл в ресурс API PrestaShop.
-   `get_schema`: Получает схему ресурса из API PrestaShop.
-   `get_data`: Получает данные из ресурса API PrestaShop.
-   `get_apis`: Получает список всех доступных API.
-   `upload_image_async`: Асинхронно загружает изображение в API PrestaShop.
-   `upload_image_from_url`: Загружает изображение в API PrestaShop.
-   `get_product_images`: Получает изображения для продукта.

## Функции

### `main`

```python
def main() -> None:
    """Проверка сущностей Prestashop"""
```

**Назначение**: Функция `main` предназначена для проверки работы с сущностями PrestaShop.

**Параметры**:

-   Отсутствуют.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Определяет данные для создания налога (`tax`).
2.  Создает экземпляр класса `PrestaShop` с использованием параметров конфигурации из класса `Config`.
3.  Вызывает метод `create` для создания налога (`taxes`) в PrestaShop.
4.  Вызывает метод `write` для записи налога (`taxes`) в PrestaShop.

**ASCII flowchart**:

```
A [Определение данных налога]
    ↓
B [Создание экземпляра PrestaShop]
    ↓
C [Вызов api.create('taxes', data)]
    ↓
D [Вызов api.write('taxes', data)]
```

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop, Config

# Пример вызова функции main
# (Необходимо настроить Config.API_DOMAIN и Config.API_KEY перед вызовом)
# main()
```

### `__init__`

```python
def __init__(
    self,
    api_key: str,
    api_domain: str,
    data_format: str = 'JSON',
    default_lang: int = 1,
    debug: bool = False,
) -> None:
    """Initialize the PrestaShop class.

    Args:
        data_format (str): Default data format ('JSON' or 'XML'). Defaults to 'JSON'.
        default_lang (int): Default language ID. Defaults to 1.
        debug (bool): Activate debug mode. Defaults to True.
    """
```

**Назначение**: Инициализирует класс `PrestaShop`.

**Параметры**:

-   `api_key` (str): Ключ API, сгенерированный в PrestaShop.
-   `api_domain` (str): Домен магазина PrestaShop (например, `https://myPrestaShop.com`).
-   `data_format` (str): Формат данных по умолчанию (`'JSON'` или `'XML'`). По умолчанию `'JSON'`.
-   `default_lang` (int): ID языка по умолчанию. По умолчанию `1`.
-   `debug` (bool): Активирует режим отладки. По умолчанию `False`.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Устанавливает значения атрибутов экземпляра класса `api_domain`, `api_key`, `debug`, `language` и `data_format` на основе переданных аргументов.
2.  Проверяет, установлена ли аутентификация в сессии клиента, и устанавливает ее, если нет.
3.  Выполняет `HEAD` запрос к API домену для проверки соединения.
4.  Получает версию PrestaShop из заголовков ответа.

**ASCII flowchart**:

```
A [Инициализация атрибутов класса]
    ↓
B [Установка аутентификации клиента, если необходимо]
    ↓
C [Выполнение HEAD запроса для проверки соединения]
    ↓
D [Получение версии PrestaShop из заголовков]
```

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop

# Пример инициализации класса PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
```

### `ping`

```python
def ping(self) -> bool:
    """Test if the webservice is working perfectly.

    Returns:
        bool: Result of the ping test. Returns `True` if the webservice is working, otherwise `False`.
    """
```

**Назначение**: Проверяет, работает ли веб-сервис.

**Параметры**:

-   Отсутствуют.

**Возвращает**:

-   `bool`: Результат проверки связи. Возвращает `True`, если веб-сервис работает, в противном случае `False`.

**Как работает функция**:

1.  Выполняет `HEAD` запрос к API домену.
2.  Вызывает метод `_check_response` для проверки статуса ответа.
3.  Возвращает результат проверки.

**ASCII flowchart**:

```
A [Выполнение HEAD запроса к API домену]
    ↓
B [Вызов _check_response для проверки статуса ответа]
    ↓
C [Возврат результата проверки]
```

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop

# Пример проверки работоспособности веб-сервиса
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
is_working = api.ping()
print(f"Веб-сервис работает: {is_working}")
```

### `_check_response`

```python
def _check_response(
    self,
    status_code: int,
    response: requests.Response,
    method: Optional[str] = None,
    url: Optional[str] = None,
    headers: Optional[dict] = None,
    data: Optional[dict] = None,
) -> bool:
    """Check the response status code and handle errors.

    Args:
        status_code (int): HTTP response status code.
        response (requests.Response): HTTP response object.
        method (Optional[str]): HTTP method used for the request.
        url (Optional[str]): The URL of the request.
        headers (Optional[dict]): The headers used in the request.
        data (Optional[dict]): The data sent in the request.

    Returns:
        bool: `True` if the status code is 200 or 201, otherwise `False`.
    """
```

**Назначение**: Проверяет код состояния ответа и обрабатывает ошибки.

**Параметры**:

-   `status_code` (int): Код состояния HTTP ответа.
-   `response` (requests.Response): Объект HTTP ответа.
-   `method` (Optional[str]): HTTP метод, использованный для запроса.
-   `url` (Optional[str]): URL запроса.
-   `headers` (Optional[dict]): Заголовки, использованные в запросе.
-   `data` (Optional[dict]): Данные, отправленные в запросе.

**Возвращает**:

-   `bool`: `True`, если код состояния 200 или 201, иначе `False`.

**Как работает функция**:

1.  Проверяет, является ли код состояния 200 или 201.
2.  Если код состояния не 200 и не 201, вызывает метод `_parse_response_error` для обработки ошибки.
3.  Возвращает `True`, если код состояния 200 или 201, иначе `False`.

**ASCII flowchart**:

```
A [Проверка status_code на 200 или 201]
    ↓
B [Если status_code не 200 и не 201, вызов _parse_response_error]
    ↓
C [Возврат True, если status_code 200 или 201, иначе False]
```

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
import requests

# Пример проверки ответа
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
response = requests.Response()
response.status_code = 200
is_valid = api._check_response(response.status_code, response)
print(f"Ответ валиден: {is_valid}")
```

### `_parse_response_error`

```python
def _parse_response_error(
    self,
    response: requests.Response,
    method: Optional[str] = None,
    url: Optional[str] = None,
    headers: Optional[dict] = None,
    data: Optional[dict] = None,
) -> None:
    """Parse the error response from PrestaShop API.

    Args:
        response (requests.Response): HTTP response object from the server.
    """
```

**Назначение**: Анализирует ответ об ошибке от API PrestaShop.

**Параметры**:

-   `response` (requests.Response): Объект HTTP ответа от сервера.
-   `method` (Optional[str]): HTTP метод, использованный для запроса.
-   `url` (Optional[str]): URL запроса.
-   `headers` (Optional[dict]): Заголовки, использованные в запросе.
-   `data` (Optional[dict]): Данные, отправленные в запросе.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Проверяет формат данных (`self.data_format`).
2.  Если формат данных `JSON`, то проверяет код состояния ответа. Если код состояния не 200 и не 201, то логирует сообщение об ошибке, содержащее код состояния, URL, заголовки и текст ответа.
3.  Если формат данных не `JSON` (предполагается, что `XML`), то вызывает метод `_parse_response` для анализа XML ответа. Затем извлекает код и сообщение об ошибке из XML структуры и логирует их.

**ASCII flowchart**:

```
A [Проверка self.data_format]
    ↓
B [Если self.data_format == 'JSON']
    ↓
C [Проверка status_code на 200 или 201]
    ↓
D [Если status_code не 200 и не 201, логирование ошибки JSON]
    ↓
E [Если self.data_format != 'JSON']
    ↓
F [Вызов _parse_response для анализа XML]
    ↓
G [Извлечение и логирование кода и сообщения об ошибке XML]
```

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
import requests

# Пример обработки ошибки JSON
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
response = requests.Response()
response.status_code = 400
response.url = 'https://your-prestashop-domain.com/api/products'
response.headers = {'Content-Type': 'application/json'}
response.text = '{"errors": [{"code": 100, "message": "Invalid parameter"}]}'

api._parse_response_error(response)

# Пример обработки ошибки XML
api.data_format = 'XML'
response.headers = {'Content-Type': 'application/xml'}
response.text = '<prestashop><errors><error><code>100</code><message>Invalid parameter</message></error></errors></prestashop>'

api._parse_response_error(response)
```

### `_prepare_url`

```python
def _prepare_url(self, url: str, params: dict) -> str:
    """Prepare the URL for the request.

    Args:
        url (str): The base URL.
        params (dict): The parameters for the request.

    Returns:
        str: The prepared URL with parameters.
    """
```

**Назначение**: Подготавливает URL для запроса.

**Параметры**:

-   `url` (str): Базовый URL.
-   `params` (dict): Параметры для запроса.

**Возвращает**:

-   `str`: Подготовленный URL с параметрами.

**Как работает функция**:

1.  Создает объект `PreparedRequest`.
2.  Подготавливает URL с параметрами, используя метод `prepare_url` объекта `PreparedRequest`.
3.  Возвращает подготовленный URL.

**ASCII flowchart**:

```
A [Создание объекта PreparedRequest]
    ↓
B [Подготовка URL с параметрами]
    ↓
C [Возврат подготовленного URL]
```

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop

# Пример подготовки URL
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
url = 'https://your-prestashop-domain.com/api/products'
params = {'limit': '10', 'display': 'full'}
prepared_url = api._prepare_url(url, params)
print(f"Подготовленный URL: {prepared_url}")
```

### `_exec`

```python
def _exec(
    self,
    resource: str,
    resource_id: Optional[int | str] = None,
    resource_ids: Optional[int | Tuple[int]] = None,
    method: str = 'GET',
    data: Optional[dict | str] = None,
    headers: Optional[dict] = None,
    search_filter: Optional[str | dict] = None,
    display: Optional[str | list] = 'full',
    schema: Optional[str] = None,
    sort: Optional[str] = None,
    limit: Optional[str] = None,
    language: Optional[int] = None,
    data_format: str = 'JSON',
) -> Optional[dict]:
    """Execute an HTTP request to the PrestaShop API."""
```

**Назначение**: Выполняет HTTP-запрос к API PrestaShop.

**Параметры**:

-   `resource` (str): API ресурс (например, `'products'`).
-   `resource_id` (Optional[int  |  str]): ID ресурса.
-   `resource_ids` (Optional[int  |  Tuple[int]]): ID ресурсов.
-   `method` (str): HTTP метод (`'GET'`, `'POST'`, `'PUT'`, `'DELETE'`). По умолчанию `'GET'`.
-   `data` (Optional[dict  |  str]): Данные для отправки.
-   `headers` (Optional[dict]): Заголовки запроса.
-   `search_filter` (Optional[str  |  dict]): Фильтр для поиска.
-   `display` (Optional[str  |  list]): Поля для отображения. По умолчанию `'full'`.
-   `schema` (Optional[str]): Схема ресурса.
-   `sort` (Optional[str]): Поле для сортировки.
-   `limit` (Optional[str]): Лимит количества записей.
-   `language` (Optional[int]): ID языка.
-   `data_format` (str): Формат данных (`'JSON'` или `'XML'`). По умолчанию `'JSON'`.

**Возвращает**:

-   `Optional[dict]`: Ответ от API или `False` в случае ошибки.

**Как работает функция**:

1.  Устанавливает уровень отладки HTTP соединения.
2.  Подготавливает URL для запроса с учетом `resource`, `resource_id` и параметров запроса (фильтр, отображение, схема, сортировка, лимит, язык и формат данных).
3.  Определяет заголовки запроса в зависимости от формата данных (`JSON` или `XML`).
4.  Обновляет заголовки запроса, если переданы дополнительные заголовки.
5.  Устанавливает формат данных (`self.data_format`).
6.  Выполняет HTTP-запрос с использованием метода `self.client.request`.
7.  Проверяет ответ с помощью метода `_check_response`. Если ответ содержит ошибку, логирует информацию об ошибке и возвращает `False`.
8.  Анализирует ответ с помощью метода `_parse_response` и возвращает результат.

**ASCII flowchart**:

```
A [Установка уровня отладки HTTP соединения]
    ↓
B [Подготовка URL]
    ↓
C [Определение заголовков запроса]
    ↓
D [Обновление заголовков запроса (если необходимо)]
    ↓
E [Установка формата данных]
    ↓
F [Выполнение HTTP-запроса]
    ↓
G [Проверка ответа с помощью _check_response]
    ↓
H [Если ошибка, логирование и возврат False]
    ↓
I [Анализ ответа с помощью _parse_response]
    ↓
J [Возврат результата]
```

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop

# Пример выполнения GET запроса
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
resource = 'products'
products = api._exec(resource=resource, method='GET', limit='5')
print(products)

# Пример выполнения POST запроса
data = {'product': {'name': 'New Product', 'price': 10.0}}
new_product = api._exec(resource=resource, method='POST', data=data)
print(new_product)
```

### `_parse_response`

```python
def _parse_response(self, response: Response, data_format: Optional[str] = 'JSON') -> dict | None:
    """Parse XML or JSON response from the API to dict structure

    Args:
        text (str): Response text.

    Returns:
        dict: Parsed data or `False` on failure.
    """
```

**Назначение**: Анализирует XML или JSON ответ от API и преобразует его в структуру `dict`.

**Параметры**:

-   `response` (Response): Объект ответа `Response`.
-   `data_format` (Optional[str]): Формат данных (`'JSON'` или `'XML'`). По умолчанию `'JSON'`.

**Возвращает**:

-   `dict | None`: Проанализированные данные или `{}` в случае ошибки.

**Как работает функция**:

1.  Проверяет формат данных (`self.data_format`).
2.  Если формат данных `'JSON'`, анализирует JSON ответ с помощью метода `response.json()`.
3.  Если формат данных не `'JSON'`, анализирует XML ответ с помощью функции `xml2dict`.
4.  Извлекает данные из структуры ответа (`data.get('prestashop', {})`) и возвращает их. Если ключ `'prestashop'` отсутствует, возвращает `data`.

**ASCII flowchart**:

```
A [Проверка self.data_format]
    ↓
B [Если self.data_format == 'JSON', анализ JSON ответа]
    ↓
C [Если self.data_format != 'JSON', анализ XML ответа]
    ↓
D [Извлечение данных из структуры ответа]
    ↓
E [Возврат данных]
```

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
import requests

# Пример анализа JSON ответа
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
response = requests.Response()
response.headers = {'Content-Type': 'application/json'}
response.text = '{"prestashop": {"products": [{"id": 1, "name": "Product 1"}]}}'
response.status_code = 200

data = api._parse_response(response)
print(data)

# Пример анализа XML ответа
api.data_format = 'XML'
response.headers = {'Content-Type': 'application/xml'}
response.text = '<prestashop><products><product><id>1</id><name>Product 1</name></product></products></prestashop>'
response.status_code = 200

data = api._parse_response(response)
print(data)
```

### `create`

```python
def create(self, resource: str, data: dict, *args, **kwards) -> Optional[dict]:
    """Create a new resource in PrestaShop API.

    Args:
        resource (str): API resource (e.g., 'products').
        data (dict): Data for the new resource.

    Returns:
        dict: Response from the API.
    """
```

**Назначение**: Создает новый ресурс в API PrestaShop.

**Параметры**:

-   `resource` (str): API ресурс (например, `'products'`).
-   `data` (dict): Данные для нового ресурса.
-   `*args`: Произвольные позиционные аргументы, которые будут переданы в метод `_exec`.
-   `**kwards`: Произвольные именованные аргументы, которые будут переданы в метод `_exec`.

**Возвращает**:

-   `dict`: Ответ от API.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `method='POST'` и `data`.
2.  Возвращает результат вызова метода `_exec`.

**ASCII flowchart**:

```
A [Вызов _exec с method='POST']
    ↓
B [Возврат результата]
```

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop

# Пример создания нового продукта
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
resource = 'products'
data = {'product': {'name': 'New Product', 'price': 10.0}}
new_product = api.create(resource=resource, data=data)
print(new_product)
```

### `read`

```python
def read(self, resource: str, resource_id: int | str, **kwargs) -> Optional[dict]:
    """Read a resource from the PrestaShop API.

    Args:
        resource (str): API resource (e.g., 'products').
        resource_id (int | str): Resource ID.

    Returns:
        dict: Response from the API.
    """
```

**Назначение**: Читает ресурс из API PrestaShop.

**Параметры**:

-   `resource` (str): API ресурс (например, `'products'`).
-   `resource_id` (int  |  str): ID ресурса.
-   `**kwargs`: Произвольные именованные аргументы, которые будут переданы в метод `_exec`.

**Возвращает**:

-   `dict`: Ответ от API.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `resource_id` и `method='GET'`.
2.  Возвращает результат вызова метода `_exec`.

**ASCII flowchart**:

```
A [Вызов _exec с method='GET']
    ↓
B [Возврат результата]
```

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop

# Пример чтения продукта
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
resource = 'products'
resource_id = 1
product = api.read(resource=resource, resource_id=resource_id)
print(product)
```

### `write`

```python
def write(self, resource: str, data: dict) -> Optional[dict]:
    """Update an existing resource in the PrestaShop API.

    Args:
        resource (str): API resource (e.g., 'products').
        data (dict): Data for the resource.

    Returns:
        dict: Response from the API.
    """
```

**Назначение**: Обновляет существующий ресурс в API PrestaShop.

**Параметры**:

-   `resource` (str): API ресурс (например, `'products'`).
-   `data` (dict): Данные для ресурса.

**Возвращает**:

-   `dict`: Ответ от API.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `resource_id` (извлекается из `data.get('id')`), `method='PUT'` и `data`.
2.  Возвращает результат вызова метода `_exec`.

**ASCII flowchart**:

```
A [Извлечение resource_id из data.get('id')]
    ↓
B [Вызов _exec с method='PUT']
    ↓
C [Возврат результата]
```

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop

# Пример обновления продукта
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
resource = 'products'
data = {'product': {'id': 1, 'name': 'Updated Product', 'price': 12.0}}
updated_product = api.write(resource=resource, data=data)
print(updated_product)
```

### `unlink`

```python
def unlink(self, resource: str, resource_id: int | str) -> bool:
    """Delete a resource from the PrestaShop API.

    Args:
        resource (str): API resource (e.g., 'products').
        resource_id (int | str): Resource ID.

    Returns:
        bool: `True` if successful, `False` otherwise.
    """
```

**Назначение**: Удаляет ресурс из API PrestaShop.

**Параметры**:

-   `resource` (str): API ресурс (например, `'products'`).
-   `resource_id` (int  |  str): ID ресурса.

**Возвращает**:

-   `bool`: `True`, если удаление успешно, `False` в противном случае.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `resource_id` и `method='DELETE'`.
2.  Возвращает результат вызова метода `_exec`.

**ASCII flowchart**:

```
A [Вызов _exec с method='DELETE']
    ↓
B [Возврат результата]
```

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop

# Пример удаления продукта
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
resource = 'products'
resource_id = 1
result = api.unlink(resource=resource, resource_id=resource_id)
print(f"Удаление успешно: {result}")
```

### `search`

```python
def search(self, resource: str, filter: Optional[str | dict] = None, **kwargs) -> List[dict]:
    """Search for resources in the PrestaShop API.

    Args:
        resource (str): API resource (e.g., 'products').
        filter (Optional[str  |  dict]): Filter for the search.

    Returns:
        List[dict]: List of resources matching the search criteria.
    """
```

**Назначение**: Выполняет поиск ресурсов в API PrestaShop.

**Параметры**:

-   `resource` (str): API ресурс (например, `'products'`).
-   `filter` (Optional[str  |  dict]): Фильтр для поиска.
-   `**kwargs`: Произвольные именованные аргументы, которые будут переданы в метод `_exec`.

**Возвращает**:

-   `List[dict]`: Список ресурсов, соответствующих критериям поиска.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `search_filter=filter` и `method='GET'`.
2.  Возвращает результат вызова метода `_exec`.

**ASCII flowchart**:

```
A [Вызов _exec с method='GET' и search_filter=filter]
    ↓
B [Возврат результата]
```

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop

# Пример поиска продуктов
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
resource = 'products'
filter = '[name]=%Product%'
products = api.search(resource=resource, filter=filter)
print(products)
```

### `create_binary`

```python
def create_binary(self, resource: str, file_path: str, file_name: str) -> dict:
    """Upload a binary file to a PrestaShop API resource."""
```

**Назначение**: Загружает бинарный файл в ресурс API PrestaShop.

**Параметры**:

-   `resource` (str): API ресурс (например, `'images/products/22'`).
-   `file_path` (str): Путь к файлу.
-   `file_name` (str): Имя файла.

**Возвращает**:

-   `dict`: Ответ от API.

**Как работает функция**:

1.  Открывает файл в режиме чтения байтов.
2.  Формирует словарь `files` для передачи файла в запросе.
3.  Выполняет POST-запрос к API с использованием `self.client.post`, передавая файл и аутентификацию.
4.  Проверяет HTTP-статус ответа на наличие ошибок.
5.  Анализирует ответ с помощью метода `_parse_response` и возвращает результат.