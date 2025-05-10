# Модуль для взаимодействия с PrestaShop API

## Обзор

Модуль `api.py` предоставляет класс `PrestaShop` для взаимодействия с PrestaShop webservice API. Он использует JSON и XML для обмена данными. Модуль поддерживает CRUD-операции, поиск и загрузку изображений, а также включает обработку ошибок.

## Подробнее

Этот модуль предназначен для упрощения взаимодействия с PrestaShop API. Он предоставляет удобные методы для выполнения различных операций, таких как создание, чтение, обновление и удаление ресурсов, а также для поиска и загрузки изображений.

## Классы

### `Config`

**Описание**: Класс конфигурации для API PrestaShop.

**Атрибуты**:

-   `language` (str): Язык.
-   `ps_version` (str): Версия PrestaShop.
-   `MODE` (str): Режим работы (`dev`, `dev8`, `prod`), определяет конечную точку API.
-   `POST_FORMAT` (str): Формат отправляемых данных (`JSON` или `XML`).
-   `API_DOMAIN` (str): Домен API PrestaShop.
-   `API_KEY` (str): Ключ API PrestaShop.

**Принцип работы**:

Класс `Config` используется для хранения параметров конфигурации, необходимых для взаимодействия с PrestaShop API. Он определяет режимы работы (разработка, тестирование, продакшн), формат данных и учетные данные для доступа к API.

### `PrestaShop`

**Описание**: Класс для взаимодействия с PrestaShop API.

**Атрибуты**:

-   `client` (Session): HTTP-клиент для выполнения запросов.
-   `debug` (bool): Флаг отладки.
-   `language` (Optional[int]): ID языка.
-   `data_format` (str): Формат данных (`JSON` или `XML`).
-   `ps_version` (str): Версия PrestaShop.
-   `api_domain` (str): Домен API.
-   `api_key` (str): Ключ API.

**Методы**:

-   `__init__`: Инициализирует класс `PrestaShop`.
-   `ping`: Проверяет работоспособность API.
-   `_check_response`: Проверяет статус ответа и обрабатывает ошибки.
-   `_parse_response_error`: Обрабатывает ошибки в ответе от PrestaShop API.
-   `_prepare_url`: Подготавливает URL для запроса.
-   `_exec`: Выполняет HTTP-запрос к PrestaShop API.
-   `_parse_response`: Преобразует XML или JSON ответ от API в структуру dict.
-   `create`: Создает новый ресурс в PrestaShop API.
-   `read`: Читает ресурс из PrestaShop API.
-   `write`: Обновляет существующий ресурс в PrestaShop API.
-   `unlink`: Удаляет ресурс из PrestaShop API.
-   `search`: Ищет ресурсы в PrestaShop API.
-   `create_binary`: Загружает бинарный файл в ресурс PrestaShop API.
-   `get_schema`: Получает схему ресурса из PrestaShop API.
-   `get_data`: Извлекает данные из ресурса PrestaShop API и сохраняет их.
-   `get_apis`: Получает список всех доступных API.
-   `upload_image_async`: Асинхронно загружает изображение в PrestaShop API.
-   `upload_image_from_url`: Загружает изображение в PrestaShop API.
-   `get_product_images`: Получает изображения для товара.

## Методы класса

### `__init__`

```python
def __init__(
    self,
    api_key: str,
    api_domain: str,
    data_format: str = Config.POST_FORMAT,
    default_lang: int = 1,
    debug: bool = False,
) -> None:
    """Инициализирует класс PrestaShop.

    Args:
        api_key (str): Ключ API, сгенерированный в PrestaShop.
        api_domain (str): Домен магазина PrestaShop (например, https://myPrestaShop.com).
        data_format (str): Формат данных по умолчанию ('JSON' или 'XML'). По умолчанию 'JSON'.
        default_lang (int): ID языка по умолчанию. По умолчанию 1.
        debug (bool): Активировать режим отладки. По умолчанию False.

    Raises:
        PrestaShopAuthenticationError: Если ключ API неверен или не существует.
        PrestaShopException: Для общих ошибок PrestaShop WebServices.
    """
```

**Назначение**: Инициализация экземпляра класса `PrestaShop` с заданными параметрами подключения к API.

**Параметры**:

-   `api_key` (str): Ключ API для аутентификации в PrestaShop.
-   `api_domain` (str): Доменное имя магазина PrestaShop.
-   `data_format` (str): Формат данных для обмена с API (JSON или XML). По умолчанию используется значение из `Config.POST_FORMAT`.
-   `default_lang` (int): Идентификатор языка по умолчанию.
-   `debug` (bool): Флаг, определяющий, включен ли режим отладки.

**Как работает функция**:

1.  Устанавливает значения атрибутов экземпляра класса на основе переданных аргументов.
2.  Формирует URL API, добавляя `/api/` к домену.
3.  Устанавливает аутентификацию для HTTP-клиента, используя предоставленный API-ключ.
4.  Выполняет HEAD-запрос к API для проверки соединения и получения версии PrestaShop.
5.  Логирует ошибку, если соединение не установлено.

**Примеры**:

```python
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
    """Проверяет, работает ли веб-сервис.

    Returns:
        bool: Результат проверки связи. Возвращает `True`, если веб-сервис работает, иначе `False`.
    """
```

**Назначение**: Проверка доступности API PrestaShop.

**Возвращает**:

-   `bool`: `True`, если API доступен, `False` в противном случае.

**Как работает функция**:

1.  Выполняет HEAD-запрос к API.
2.  Вызывает метод `_check_response` для проверки статуса ответа.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
is_available = api.ping()
print(f"API доступен: {is_available}")
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
    """Проверяет код состояния ответа и обрабатывает ошибки.

    Args:
        status_code (int): Код состояния HTTP-ответа.
        response (requests.Response): Объект HTTP-ответа.
        method (Optional[str]): HTTP-метод, используемый для запроса.
        url (Optional[str]): URL-адрес запроса.
        headers (Optional[dict]): Заголовки, используемые в запросе.
        data (Optional[dict]): Данные, отправленные в запросе.

    Returns:
        bool: `True`, если код состояния равен 200 или 201, иначе `False`.
    """
```

**Назначение**: Проверка статуса HTTP-ответа и обработка ошибок.

**Параметры**:

-   `status_code` (int): HTTP код ответа.
-   `response` (requests.Response): Объект ответа `requests`.
-   `method` (Optional[str]) = None: HTTP метод запроса.
-   `url` (Optional[str]) = None: URL запроса.
-   `headers` (Optional[dict]) = None: Заголовки запроса.
-   `data` (Optional[dict]) = None: Данные запроса.

**Возвращает**:

-   `bool`: `True`, если статус код 200 или 201, иначе `False`.

**Как работает функция**:

1.  Проверяет, является ли код статуса 200 или 201.
2.  Если код статуса не 200 и не 201, вызывает метод `_parse_response_error` для обработки ошибки.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)

response = api.client.request(method='GET', url=api.api_domain)
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
    """Обрабатывает ответ об ошибке от PrestaShop API.

    Args:
        response (requests.Response): Объект HTTP-ответа от сервера.
    """
```

**Назначение**: Обработка ошибок, полученных в ответе от API PrestaShop.

**Параметры**:

-   `response` (requests.Response): Объект HTTP-ответа, содержащий информацию об ошибке.
-   `method` (Optional[str]) = None: HTTP метод запроса.
-   `url` (Optional[str]) = None: URL запроса.
-   `headers` (Optional[dict]) = None: Заголовки запроса.
-   `data` (Optional[dict]) = None: Данные запроса.

**Как работает функция**:

1.  Определяет формат данных (`JSON` или `XML`).
2.  В зависимости от формата данных, извлекает код и сообщение об ошибке из ответа.
3.  Логирует информацию об ошибке с использованием `logger.error`.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
response = requests.Response()
response.status_code = 400
response._content = b'{"errors": [{"code": 100, "message": "Bad Request"}]}'

api._parse_response_error(response)
```

### `_prepare_url`

```python
def _prepare_url(self, url: str, params: dict) -> str:
    """Подготавливает URL-адрес для запроса.

    Args:
        url (str): Базовый URL-адрес.
        params (dict): Параметры для запроса.

    Returns:
        str: Подготовленный URL-адрес с параметрами.
    """
```

**Назначение**: Формирование полного URL-адреса с учетом параметров запроса.

**Параметры**:

-   `url` (str): Базовый URL-адрес API.
-   `params` (dict): Словарь параметров запроса.

**Возвращает**:

-   `str`: Сформированный URL-адрес с параметрами.

**Как работает функция**:

1.  Использует `PreparedRequest` из библиотеки `requests` для подготовки URL.
2.  Вызывает метод `prepare_url` для добавления параметров к базовому URL.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
url = api._prepare_url(api.api_domain + 'products', {'limit': '3'})
print(url)
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
    data_format: str = Config.POST_FORMAT,
    **kwargs,
) -> Optional[dict]:
    """Выполняет HTTP-запрос к PrestaShop API."""
```

**Назначение**: Выполнение HTTP-запроса к API PrestaShop с заданными параметрами.

**Параметры**:

-   `resource` (str): Название ресурса API (например, 'products').
-   `resource_id` (Optional[int | str]) = None: ID ресурса.
-   `resource_ids` (Optional[int | Tuple[int]]) = None: ID ресурсов.
-   `method` (str) = 'GET': HTTP метод запроса (GET, POST, PUT, DELETE).
-   `data` (Optional[dict | str]) = None: Данные для отправки в запросе.
-   `headers` (Optional[dict]) = None: Дополнительные заголовки запроса.
-   `search_filter` (Optional[str | dict]) = None: Фильтр для поиска.
-   `display` (Optional[str | list]) = 'full': Отображаемые поля.
-   `schema` (Optional[str]) = None: Схема ресурса.
-   `sort` (Optional[str]) = None: Параметры сортировки.
-   `limit` (Optional[str]) = None: Лимит количества возвращаемых записей.
-   `language` (Optional[int]) = None: ID языка.
-   `data_format` (str) = Config.POST_FORMAT: Формат данных (JSON или XML).

**Возвращает**:

-   `Optional[dict]`: Распарсенные данные ответа API или `False` в случае ошибки.

**Как работает функция**:

1.  Включает режим отладки HTTP-соединения, если `self.debug` установлен в `True`.
2.  Формирует URL-адрес на основе переданных параметров.
3.  Определяет заголовки запроса в зависимости от формата данных (JSON или XML).
4.  Добавляет дополнительные заголовки, если они переданы.
5.  Выполняет HTTP-запрос с использованием библиотеки `requests`.
6.  Проверяет статус ответа с помощью метода `_check_response`.
7.  В случае ошибки логирует информацию об ошибке и возвращает `False`.
8.  В случае успешного выполнения преобразует ответ с помощью метода `_parse_response` и возвращает результат.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
products = api._exec(resource='products', method='GET', limit='5')
print(products)
```

### `_parse_response`

```python
def _parse_response(self, response: Response) -> dict | None:
    """Преобразует XML или JSON ответ от API в структуру dict.

    Args:
        text (str): Текст ответа.

    Returns:
        dict: Распарсенные данные или `False` в случае сбоя.
    """
```

**Назначение**: Преобразование ответа от API (в формате JSON или XML) в словарь Python.

**Параметры**:

-   `response` (Response): Объект ответа HTTP-запроса.

**Возвращает**:

-   `dict | None`: Словарь с данными, полученными из ответа API, или `None` в случае ошибки.

**Как работает функция**:

1.  Извлекает данные из ответа в формате JSON.
2.  Если в полученном словаре есть ключ 'prestashop', возвращает значение этого ключа.
3.  В противном случае возвращает исходный словарь.
4.  В случае возникновения исключения при парсинге ответа, логирует ошибку и возвращает пустой словарь.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)

response = requests.Response()
response.status_code = 200
response._content = b'{"prestashop": {"products": [{"id": 1, "name": "Product 1"}]}}'

data = api._parse_response(response)
print(data)
```

### `create`

```python
def create(self, resource: str, data: dict, *args, **kwargs) -> Optional[dict]:
    """Создает новый ресурс в PrestaShop API.

    Args:
        resource (str): API ресурс (например, 'products').
        data (dict): Данные для нового ресурса.

    Returns:
        dict: Ответ от API.
    """
```

**Назначение**: Создание нового ресурса в API PrestaShop.

**Параметры**:

-   `resource` (str): Тип ресурса (например, 'products', 'categories').
-   `data` (dict): Данные для создания ресурса.
-   `*args`: Произвольные позиционные аргументы, передаваемые в `_exec`.
-   `**kwargs`: Произвольные именованные аргументы, передаваемые в `_exec`.

**Возвращает**:

-   `Optional[dict]`: Ответ от API в виде словаря или `None` в случае ошибки.

**Как работает функция**:

1.  Вызывает метод `_exec` с указанием ресурса, метода `POST` и переданных данных.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
data = {'product': {'name': 'New Product', 'price': 10.0}}
response = api.create(resource='products', data=data)
print(response)
```

### `read`

```python
def read(self, resource: str, resource_id: int | str, **kwargs) -> Optional[dict]:
    """Читает ресурс из PrestaShop API.

    Args:
        resource (str): API ресурс (например, 'products').
        resource_id (int | str): ID ресурса.

    Returns:
        dict: Ответ от API.
    """
```

**Назначение**: Получение информации о конкретном ресурсе из API PrestaShop.

**Параметры**:

-   `resource` (str): Тип ресурса (например, 'products').
-   `resource_id` (int | str): Идентификатор ресурса.
-   `**kwargs`: Дополнительные параметры, передаваемые в `_exec`.

**Возвращает**:

-   `Optional[dict]`: Ответ от API в виде словаря.

**Как работает функция**:

1.  Вызывает метод `_exec` с указанием ресурса, идентификатора ресурса и метода `GET`.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
product = api.read(resource='products', resource_id=1)
print(product)
```

### `write`

```python
def write(self, resource: str, resource_id:int|str, data: dict, **kwargs) -> Optional[dict]:
    """Обновляет существующий ресурс в PrestaShop API.

    Args:
        resource (str): API ресурс (например, 'products').
        data (dict): Данные для ресурса.

    Returns:
        dict: Ответ от API.
    """
```

**Назначение**: Обновление существующего ресурса в API PrestaShop.

**Параметры**:

-   `resource` (str): Тип ресурса (например, 'products').
-   `resource_id` (int | str): Идентификатор ресурса.
-   `data` (dict): Данные для обновления ресурса.
-   `**kwargs`: Дополнительные параметры, передаваемые в `_exec`.

**Возвращает**:

-   `Optional[dict]`: Ответ от API в виде словаря.

**Как работает функция**:

1.  Вызывает метод `_exec` с указанием ресурса, идентификатора ресурса, метода `PUT` и переданных данных.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
data = {'product': {'id': 1, 'name': 'Updated Product', 'price': 12.0}}
response = api.write(resource='products', resource_id=1, data=data)
print(response)
```

### `unlink`

```python
def unlink(self, resource: str, resource_id: int | str) -> bool:
    """Удаляет ресурс из PrestaShop API.

    Args:
        resource (str): API ресурс (например, 'products').
        resource_id (int | str): ID ресурса.

    Returns:
        bool: `True`, если успешно, `False` в противном случае.
    """
```

**Назначение**: Удаление ресурса из API PrestaShop.

**Параметры**:

-   `resource` (str): Тип ресурса (например, 'products').
-   `resource_id` (int | str): Идентификатор ресурса.

**Возвращает**:

-   `bool`: `True`, если удаление прошло успешно, `False` в противном случае.

**Как работает функция**:

1.  Вызывает метод `_exec` с указанием ресурса, идентификатора ресурса и метода `DELETE`.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
result = api.unlink(resource='products', resource_id=1)
print(f"Удаление успешно: {result}")
```

### `search`

```python
def search(self, resource: str, filter: Optional[str | dict] = None, **kwargs) -> List[dict]:
    """Ищет ресурсы в PrestaShop API.

    Args:
        resource (str): API ресурс (например, 'products').
        filter (Optional[str  |  dict]): Фильтр для поиска.

    Returns:
        List[dict]: Список ресурсов, соответствующих критериям поиска.
    """
```

**Назначение**: Поиск ресурсов в API PrestaShop с использованием фильтра.

**Параметры**:

-   `resource` (str): Тип ресурса (например, 'products').
-   `filter` (Optional[str  |  dict]) = None: Фильтр для поиска ресурсов.
-   `**kwargs`: Дополнительные параметры, передаваемые в `_exec`.

**Возвращает**:

-   `List[dict]`: Список словарей, представляющих найденные ресурсы.

**Как работает функция**:

1.  Вызывает метод `_exec` с указанием ресурса, фильтра и метода `GET`.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
products = api.search(resource='products', filter='[name]=%Product%')
print(products)
```

### `create_binary`

```python
def create_binary(self, resource: str, file_path: str, file_name: str) -> dict:
    """Загружает бинарный файл в ресурс PrestaShop API."""
```

**Назначение**: Загрузка бинарного файла (например, изображения) в API PrestaShop.

**Параметры**:

-   `resource` (str): API ресурс, к которому загружается файл (например, 'images/products/22').
-   `file_path` (str): Путь к файлу.
-   `file_name` (str): Имя файла.

**Возвращает**:

-   `dict`: Ответ от API в виде словаря.

**Как работает функция**:

1.  Открывает файл по указанному пути в бинарном режиме.
2.  Формирует словарь `files` для передачи файла в запросе.
3.  Выполняет POST-запрос к API с использованием `requests.post`.
4.  Проверяет статус ответа и вызывает `raise_for_status()` для обработки HTTP-ошибок.
5.  Преобразует ответ в формат JSON и возвращает его.
6.  В случае возникновения исключений логирует ошибку и возвращает словарь с информацией об ошибке.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
file_path = 'path/to/image.jpg'
file_name = 'image.jpg'
response = api.create_binary(resource='images/products/22', file_path=file_path, file_name=file_name)
print(response)
```

### `get_schema`

```python
def get_schema(
    self, resource: Optional[str] = None, resource_id: Optional[int] = None, schema: Optional[str] = 'blank', **kwargs
) -> dict | None:
    """Получает схему данного ресурса из PrestaShop API.

    Args:
        resource (str): Название ресурса (например, 'products', 'customers').
            Если не указано - вернется список всех схем сущностей, доступных для API-ключа.
        resource_id (Optinal[str]):
        schema (Optional[str]): Обычно подразумеваются следующие опции:
            - blank: (Самая распространенная опция, как и в вашем коде)
                Возвращает пустую схему ресурса. Это полезно для определения минимального набора полей,
                необходимых для создания нового объекта. То есть возвращает структуру XML или JSON с пустыми полями,
                которые можно заполнить данными.
            - synopsis (или simplified): В некоторых версиях и для некоторых ресурсов может существовать опция,
                возвращающая упрощенную схему. Она может содержать только основные поля ресурса и их типы.
                Это может быть удобнее, чем полная схема, если вам не нужны все детали.
            - full (или без указания schema): Часто, если параметр schema не указан,
                или если он указан как full, возвращается полная схема ресурса. Она включает все поля, их типы,
                возможные значения, описания и другие метаданные. Это самый подробный вид схемы.
            - form (или что-то подобное): Реже, но может быть опция, возвращающая схему,
                оптимизированную для отображения в форме редактирования. Она может включать информацию о валидации
                полей, порядке отображения и т.п.

    Returns:
        dict  |  None: Схема запрошенного ресурса или `None` в случае ошибки.
    """
```

**Назначение**: Получение схемы ресурса из API PrestaShop.

**Параметры**:

-   `resource` (Optional[str]) = None: Имя ресурса (например, 'products', 'customers'). Если не указан, возвращается список всех доступных схем.
-   `resource_id` (Optional[int]) = None: ID ресурса.
-   `schema` (Optional[str]) = 'blank': Тип схемы. Возможные значения: 'blank', 'synopsis', 'full', 'form'.
-   `**kwargs`: Дополнительные параметры, передаваемые в `_exec`.

**Возвращает**:

-   `dict  |  None`: Схема запрошенного ресурса или `None` в случае ошибки.

**Как работает функция**:

1.  Вызывает метод `_exec` с указанием ресурса, ID ресурса, типа схемы и метода `GET`.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
schema = api.get_schema(resource='products', schema='blank')
print(schema)
```

### `get_data`

```python
def get_data(self, resource: str, **kwargs) -> Optional[dict]:
    """Извлекает данные из ресурса PrestaShop API и сохраняет их.

    Args:
        resource (str): API ресурс (например, 'products').
        **kwargs: Дополнительные аргументы для API-запроса.

    Returns:
        dict | None: Данные из API или `False` в случае ошибки.
    """
```

**Назначение**: Получение данных из API PrestaShop.

**Параметры**:

-   `resource` (str): Тип ресурса (например, 'products').
-   `**kwargs`: Дополнительные параметры, передаваемые в `_exec`.

**Возвращает**:

-   `Optional[dict]`: Данные, полученные из API, или `None` в случае ошибки.

**Как работает функция**:

1.  Вызывает метод `_exec` с указанием ресурса и метода `GET`.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
products = api.get_data(resource='products', limit='5')
print(products)
```

### `get_apis`

```python
def get_apis(self) -> Optional[dict]:
    """Получает список всех доступных API.

    Returns:
        dict: Список доступных API.
    """
```

**Назначение**: Получение списка доступных API из PrestaShop.

**Возвращает**:

-   `Optional[dict]`: Список доступных API в виде словаря.

**Как работает функция**:

1.  Вызывает метод `_exec` с указанием ресурса 'apis' и методом 'GET'.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)
apis = api.get_apis()
print(apis)
```

### `upload_image_async`

```python
def upload_image_async(
    self, resource: str, resource_id: int, img_url: str, img_name: Optional[str] = None
) -> Optional[dict]:
    """Асинхронно загружает изображение в PrestaShop API.

    Args:
        resource (str): API ресурс (например, 'images/products/22').
        resource_id (int): ID ресурса.
        img_url (str): URL-адрес изображения.
        img_name (Optional[str]): Имя файла изображения, по умолчанию None.

    Returns:
        dict | None: Ответ от API или `False` в случае ошибки.
    """
```

**Назначение**: Асинхронная загрузка изображения в API PrestaShop.

**Параметры**:

-   `resource` (str): API ресурс, куда загружается изображение (например, 'images/products/22').
-   `resource_id` (int): ID ресурса.
-   `img_url` (str): URL-адрес изображения.
-   `img_name` (Optional[str]) = None: Имя изображения.

**Возвращает**:

-   `Optional[dict]`: Ответ от API или `False` в случае ошибки.

**Как работает функция**:

1.  Разделяет URL-адрес изображения на имя файла и расширение.
2.  Формирует имя файла на основе ID ресурса и имени изображения.
3.  Сохраняет изображение с использованием функции `save_image_from_url`.
4.  Вызывает метод `create_binary` для загрузки изображения в API.
5.  Удаляет временный файл изображения.
6.  Возвращает ответ от API.

**Примеры**:

```python
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com',
    data_format='JSON',
    default_lang=1,
    debug=True
)