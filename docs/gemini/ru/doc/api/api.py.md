## Анализ кода модуля `src/endpoints/prestashop/api/api.py`

### Обзор

Этот модуль предназначен для взаимодействия с PrestaShop webservice API, используя JSON и XML для форматирования сообщений.

### Подробней

Модуль `src/endpoints/prestashop/api/api.py` предоставляет класс `PrestaShop` для взаимодействия с API PrestaShop. Он включает в себя методы для выполнения CRUD операций (создание, чтение, обновление, удаление), поиска ресурсов и загрузки изображений, а также содержит обработку ошибок для ответов от API.

### Классы

#### `Config`

**Описание**: Класс конфигурации для настроек PrestaShop API.

**Атрибуты**:

-   `language` (str): Код языка.
-   `ps_version` (str): Версия PrestaShop.
-   `MODE` (str): Определяет конечную точку API ('dev', 'dev8', 'prod').
-   `POST_FORMAT` (str): Формат отправляемых данных (по умолчанию 'JSON').
-   `API_DOMAIN` (str): Домен API.
-   `API_KEY` (str): Ключ API.

**Как работает класс**:

Класс `Config` используется для хранения настроек API PrestaShop. Он пытается загрузить значения для `API_DOMAIN` и `API_KEY` из переменных окружения. Если переменные окружения не установлены, используются значения из файла конфигурации `gs.credentials.presta.client`.

#### `PrestaShop`

**Описание**: Класс для взаимодействия с PrestaShop webservice API, использующий JSON и XML для форматирования сообщений.

**Наследует**:

-   Отсутствует.

**Атрибуты**:

-   `client` (Session): Объект `requests.Session` для выполнения HTTP-запросов.
-   `debug` (bool): Флаг, указывающий, включен ли режим отладки.
-   `language` (Optional[int]): ID языка по умолчанию.
-   `data_format` (str): Формат данных по умолчанию ('JSON' или 'XML').
-   `ps_version` (str): Версия PrestaShop.
-   `api_domain` (str): Домен API.
-   `api_key` (str): Ключ API.

**Методы**:

-   `__init__(self, api_key: str, api_domain: str, data_format: str = Config.POST_FORMAT, default_lang: int = 1, debug: bool = False) -> None`: Инициализирует объект `PrestaShop`.
-   `ping(self) -> bool`: Проверяет работоспособность веб-сервиса.
-   `_check_response(self, status_code: int, response: requests.Response, method: Optional[str] = None, url: Optional[str] = None, headers: Optional[dict] = None, data: Optional[dict] = None) -> bool`: Проверяет код ответа и обрабатывает ошибки.
-   `_parse_response_error(self, response: requests.Response, method: Optional[str] = None, url: Optional[str] = None, headers: Optional[dict] = None, data: Optional[dict] = None) -> None`: Разбирает сообщение об ошибке из ответа API PrestaShop.
-   `_prepare_url(self, url: str, params: dict) -> str`: Подготавливает URL для запроса.
-   `_exec(self, resource: str, resource_id: Optional[int | str] = None, resource_ids: Optional[int | Tuple[int]] = None, method: str = 'GET', data: Optional[dict | str] = None, headers: Optional[dict] = None, search_filter: Optional[str | dict] = None, display: Optional[str | list] = 'full', schema: Optional[str] = None, sort: Optional[str] = None, limit: Optional[str] = None, language: Optional[int] = None, data_format: str = Config.POST_FORMAT, **kwards) -> Optional[dict]`: Выполняет HTTP-запрос к PrestaShop API.
-   `create(self, resource: str, data: dict, *args, **kwards) -> Optional[dict]`: Создает новый ресурс в PrestaShop API.
-   `read(self, resource: str, resource_id: int | str, **kwargs) -> Optional[dict]`: Читает ресурс из PrestaShop API.
-   `write(self, resource: str, resource_id:int|str, data: dict, **kwards) -> Optional[dict]`: Обновляет существующий ресурс в PrestaShop API.
-   `unlink(self, resource: str, resource_id: int | str) -> bool`: Удаляет ресурс из PrestaShop API.
-   `search(self, resource: str, filter: Optional[str | dict] = None, **kwargs) -> List[dict]`: Ищет ресурсы в PrestaShop API.
-   `create_binary(self, resource: str, file_path: str, file_name: str) -> dict`: Загружает бинарный файл в ресурс API PrestaShop.
-   `get_schema(self, resource: Optional[str] = None, resource_id: Optional[int] = None, schema: Optional[str] = 'blank', **kwards) -> dict | None`: Получает схему ресурса из PrestaShop API.
-   `get_data(self, resource: str, **kwargs) -> Optional[dict]`: Извлекает данные из ресурса PrestaShop API и сохраняет их.
-   `get_apis(self) -> Optional[dict]`: Получает список всех доступных API.

#### `__init__`

**Назначение**: Инициализирует объект класса `PrestaShop`.

```python
def __init__(
        self,
        api_key: str,
        api_domain: str,
        data_format: str = Config.POST_FORMAT,
        default_lang: int = 1,
        debug: bool = False,
    ) -> None:
    """Initialize the PrestaShop class.

    Args:
        data_format (str): Default data format ('JSON' or 'XML'). Defaults to 'JSON'.
        default_lang (int): Default language ID. Defaults to 1.
        debug (bool): Activate debug mode. Defaults to True.
    """
    ...
```

**Параметры**:

-   `api_key` (str): Ключ API для доступа к PrestaShop.
-   `api_domain` (str): Домен API PrestaShop.
-   `data_format` (str, optional): Формат данных по умолчанию ('JSON' или 'XML'). Defaults to 'JSON'.
-   `default_lang` (int, optional): ID языка по умолчанию. Defaults to 1.
-   `debug` (bool, optional): Включает режим отладки. Defaults to True.

**Как работает функция**:

1.  Принимает параметры для подключения к API PrestaShop.
2.  Инициализирует атрибуты объекта `PrestaShop` значениями, полученными из аргументов.
3.  Устанавливает заголовок `Authorization` для аутентификации в API PrestaShop.
4.  Выполняет HEAD-запрос к API для проверки соединения и получения версии PrestaShop.
5.  Логирует информацию об ошибках, используя `logger.error`.

#### `ping`

**Назначение**: Проверяет работоспособность веб-сервиса.

```python
def ping(self) -> bool:
    """Test if the webservice is working perfectly.

    Returns:
        bool: Result of the ping test. Returns `True` if the webservice is working, otherwise `False`.
    """
    ...
```

**Возвращает**:

-   `bool`: `True`, если веб-сервис работает, `False` - в противном случае.

**Как работает функция**:

1.  Выполняет HEAD-запрос к API PrestaShop.
2.  Вызывает метод `_check_response` для проверки статуса ответа.

#### `_check_response`

**Назначение**: Проверяет код ответа и обрабатывает ошибки.

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
    ...
```

**Параметры**:

-   `status_code` (int): Код состояния HTTP-ответа.
-   `response` (requests.Response): Объект HTTP-ответа.
-   `method` (Optional[str]): HTTP метод, используемый для запроса.
-   `url` (Optional[str]): URL запроса.
-   `headers` (Optional[dict]): Заголовки, использованные в запросе.
-   `data` (Optional[dict]): Данные, отправленные в запросе.

**Возвращает**:

-   `bool`: `True`, если код ответа 200 или 201, иначе `False`.

**Как работает функция**:

1.  Проверяет, входит ли код состояния в список успешных кодов (200, 201).
2.  Если код ответа не является успешным, вызывает метод `_parse_response_error` для обработки ошибки.

#### `_parse_response_error`

**Назначение**: Разбирает сообщение об ошибке из ответа API PrestaShop.

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
    ...
```

**Параметры**:

-   `response` (requests.Response): Объект HTTP-ответа от сервера.

**Как работает функция**:

1.  Проверяет формат ответа (`Config.POST_FORMAT`).
2.  В зависимости от формата ответа (JSON или XML) извлекает код и сообщение об ошибке из ответа API.
3.  Логирует информацию об ошибке, используя `logger.error`.

#### `_prepare_url`

**Назначение**: Подготавливает URL для запроса.

```python
def _prepare_url(self, url: str, params: dict) -> str:
    """Prepare the URL for the request.

    Args:
        url (str): The base URL.
        params (dict): The parameters for the request.

    Returns:
        str: The prepared URL with parameters.
    """
    ...
```

**Параметры**:

-   `url` (str): Базовый URL.
-   `params` (dict): Параметры для запроса.

**Возвращает**:

-   `str`: Подготовленный URL с параметрами.

**Как работает функция**:

1.  Создает объект `PreparedRequest`.
2.  Подготавливает URL с параметрами, используя `req.prepare_url(url, params)`.
3.  Возвращает подготовленный URL.

#### `_exec`

**Назначение**: Выполняет HTTP-запрос к PrestaShop API.

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
        **kwards,
    ) -> Optional[dict]:
    """Execute an HTTP request to the PrestaShop API."""
    ...
```

**Параметры**:

-   `resource` (str): API ресурс (например, 'products').
-   `resource_id` (Optional[int | str]): ID ресурса.
     `resource_ids` (Optional[int | Tuple[int]]): ID ресурсов.
-   `method` (str): HTTP метод ('GET', 'POST', 'PUT', 'DELETE'). По умолчанию 'GET'.
-   `data` (Optional[dict | str]): Данные для отправки (словарь или строка).
-   `headers` (Optional[dict]): Пользовательские заголовки запроса.
-   `search_filter` (Optional[str | dict]): Фильтр для поиска.
-   `display` (Optional[str | list]): Что отображать в ответе (например, 'full').
-   `schema` (Optional[str]): Используемая схема данных.
-   `sort` (Optional[str]): Порядок сортировки.
-   `limit` (Optional[str]): Лимит на количество возвращаемых записей.
    `language` (Optional[int]): The language ID for the request.
-   `data_format` (str): Формат данных ('JSON' или 'XML'). По умолчанию `Config.POST_FORMAT`.
-*kwards: Произвольные именованные аргументы, передаваемые в функцию.

**Возвращает**:

-   `Optional[dict]`: Ответ от API в виде словаря или `False` в случае ошибки.

**Как работает функция**:

1.  Включает режим отладки, если `self.debug` равно `True`.
2.  Формирует URL для запроса, используя `_prepare_url`.
3.  Устанавливает заголовки запроса в зависимости от формата данных (`data_format`).
4.  Выполняет HTTP-запрос с использованием `self.client.request`.
5.  Проверяет код ответа с помощью `self._check_response`.
6.  В случае успеха вызывает `self._parse_response` для разбора ответа.

#### `_parse_response`

**Назначение**: Разбирает XML или JSON ответ от API в структуру словаря.

```python
def _parse_response(self, response: Response) -> dict | None:
    """Parse XML or JSON response from the API to dict structure

    Args:
        text (str): Response text.

    Returns:
        dict: Parsed data or `False` on failure.
    """
    ...
```

**Параметры**:

-   `response` (Response): Объект HTTP-ответа.

**Возвращает**:

-   `dict | None`: Разобранные данные или `False` в случае ошибки.

**Как работает функция**:

1.  Пытается разобрать ответ как JSON, используя `response.json()`.
2.  Если разбор JSON успешен, возвращает данные, извлекая корень `prestashop`.
3.  Если разбор JSON не удался, значит это XML, разбирает XML response
4.  В случае ошибки логирует информацию об ошибке и возвращает пустой словарь.

### `create`

**Назначение**: Создает новый ресурс в PrestaShop API.

```python
def create(self, resource: str, data: dict, *args, **kwards) -> Optional[dict]:
    """Create a new resource in PrestaShop API.

    Args:
        resource (str): API resource (e.g., 'products').
        data (dict): Data for the new resource.

    Returns:
        dict: Response from the API.
    """
    ...
```

**Параметры**:

-   `resource` (str): API ресурс (например, 'products').
-   `data` (dict): Данные для нового ресурса.
- `*args`: Произвольные позиционные аргументы, передаваемые в функцию.\
- `*kwargs`: Произвольные именованные аргументы, передаваемые в функцию.

**Возвращает**:

-   `dict`: Ответ от API.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса и метода `POST`.
2.   Возвращает от функцию `_exec`

### `read`

**Назначение**: Читает ресурс из PrestaShop API.

```python
def read(self, resource: str, resource_id: int | str, **kwargs) -> Optional[dict]:
    """Read a resource from the PrestaShop API.

    Args:
        resource (str): API resource (e.g., 'products').
        resource_id (int | str): Resource ID.

    Returns:
        dict: Response from the API.
    """
    ...
```

**Параметры**:

-   `resource` (str): API ресурс (например, 'products').
-   `resource_id` (int | str): ID ресурса.
-`**kwargs`: Произвольные именованные аргументы, передаваемые в функцию.

**Возвращает**:

-   `dict`: Ответ от API.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса, ID ресурса и метода `GET`.
2.  Возвращает от функцию `_exec`

### `write`

**Назначение**: Обновляет существующий ресурс в PrestaShop API.

```python
def write(self, resource: str, resource_id:int|str, data: dict, **kwards) -> Optional[dict]:
    """Update an existing resource in the PrestaShop API.

    Args:
        resource (str): API resource (e.g., 'products').
        data (dict): Data for the resource.

    Returns:
        dict: Response from the API.
    """
    ...
```

**Параметры**:

-   `resource` (str): API ресурс (например, 'products').
-   `resource_id` (int | str): ID ресурса.
-   `data` (dict): Данные для ресурса.
-`**kwargs`: Произвольные именованные аргументы, передаваемые в функцию.

**Возвращает**:

-   `dict`: Ответ от API.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса, ID ресурса и метода `PUT`.
2.  Возвращает от функцию `_exec`

### `unlink`

**Назначение**: Удаляет ресурс из PrestaShop API.

```python
def unlink(self, resource: str, resource_id: int | str) -> bool:
    """Delete a resource from the PrestaShop API.

    Args:
        resource (str): API resource (e.g., 'products').
        resource_id (int | str): Resource ID.

    Returns:
        bool: `True` if successful, `False` otherwise.
    """
    ...
```

**Параметры**:

-   `resource` (str): API ресурс (например, 'products').
-   `resource_id` (int | str): ID ресурса.

**Возвращает**:

-   `bool`: `True`, если удаление прошло успешно, `False` - в противном случае.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса, ID ресурса и метода `DELETE`.
2.  Возвращает от функцию `_exec`

### `search`

**Назначение**: Ищет ресурсы в PrestaShop API.

```python
def search(self, resource: str, filter: Optional[str | dict] = None, **kwargs) -> List[dict]:
    """Search for resources in the PrestaShop API.

    Args:
        resource (str): API resource (e.g., 'products').
        filter (Optional[str  |  dict]): Filter for the search.

    Returns:
        List[dict]: List of resources matching the search criteria.
    """
    ...
```

**Параметры**:

-   `resource` (str): API ресурс (например, 'products').
-   `filter` (Optional[str  |  dict]): Фильтр для поиска.
-   `**kwargs`: Произвольные именованные аргументы, передаваемые в функцию.

**Возвращает**:

-   `List[dict]`: Список ресурсов, соответствующих критериям поиска.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса, фильтра и метода `GET`.
2.  Возвращает от функцию `_exec`

### `create_binary`

**Назначение**: Загружает бинарный файл в ресурс API PrestaShop.

```python
def create_binary(self, resource: str, file_path: str, file_name: str) -> dict:
    """Upload a binary file to a PrestaShop API resource."""
    ...
```

**Параметры**:

-   `resource` (str): API ресурс (например, 'images/products/22').
-   `file_path` (str): Путь к файлу для загрузки.
-   `file_name` (str): Имя файла.

**Возвращает**:

-   `dict`: Ответ от API.

**Как работает функция**:

1.  Открывает указанный файл для чтения в бинарном режиме (`'rb'`).
2.  Формирует словарь `files` для передачи файла в запросе.
3.  Выполняет POST-запрос к API с использованием `self.client.post`.
4.  Проверяет код ответа HTTP и логирует информацию об успехе или ошибке.
5.  Возвращает ответ от API.

### `get_schema`

**Назначение**: Получает схему для ресурса из PrestaShop API.

```python
def get_schema(
        self, resource: Optional[str] = None, resource_id: Optional[int] = None, schema: Optional[str] = 'blank', **kwards
    ) -> dict | None:
    """Retrieve the schema of a given resource from PrestaShop API.

    Args:
        resource (str): The name of the resource (e.g., 'products', 'customers').
        resource_id (Optinal[str]):
        schema (Optional[str]): обычно подразумеваются следующие опции:
            - blank: (Самая распространенная опция, как и в вашем коде)
                Возвращает пустую схему ресурса. Это полезно для определения минимального набора полей,
                необходимых для создания нового объекта. То есть возвращает структуру XML или JSON с пустыми полями,
                которые можно заполнить данными.
            - synopsis (или simplified): В некоторых версиях и для некоторых ресурсов может существовать опция,
                возвращающая упрощенную схему. Она может содержать только основные поля ресурса и их типы.
                Это может быть удобнее, чем полная схема, если вам не нужны все детали.
            - full (или без указания schema): Часто, если параметр schema не указан,
                или если он указан как full, возвращается полная схема ресурса. Она включает все поля, их типы,
                возможные значения, описания и другие метаданные. Это самый подробный вид схемы.\n
        Returns:\n dict | None: The schema of the requested resource or `None` in case of an error.
        """
```

**Параметры**:

-   `resource` (str): Название ресурса (например, 'products', 'customers'). Если не указан, возвращается список всех схем сущностей, доступных для API ключа.
-   `resource_id` (Optional[str]):
-   `schema` (Optional[str]): Тип схемы. Возможные значения:
    -   `'blank'`: Возвращает пустую схему ресурса.
    -   `'synopsis'`: Возвращает упрощенную схему.
    -   `None`: Возвращает полную схему ресурса.

**Возвращает**:

-   `dict  |  None`: The schema of the requested resource or `None` in case of an error.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса, ID ресурса (если указан) и типа схемы.
    2. Возвращает результат от функции `_exec`

### `get_data`

**Назначение**: Извлекает данные из ресурса PrestaShop API и сохраняет их асинхронно.

```python
def get_data(self, resource: str, **kwargs) -> Optional[dict]:
    """Fetch data from a PrestaShop API resource and save it asynchronously.

    Args:
        resource (str): API resource (e.g., 'products').
        **kwargs: Additional arguments for the API request.

    Returns:
        dict | None: Data from the API or `False` on failure.
    """
    ...
```

**Параметры**:

-   `resource` (str): API ресурс (например, 'products').
-   `**kwargs`: Дополнительные аргументы для API-запроса.

**Возвращает**:

-   `dict | None`: Данные из API или `False` в случае ошибки.

**Как работает функция**:

1.  Вызывает функцию `_exec` для выполнения запроса к API PrestaShop и получения данных.
2. Вызывает функцию `_save` для сохранения ответа в файле
3.   Возвращает от функцию `_exec`

### `get_apis`

**Назначение**: Получает список всех доступных API.

```python
def get_apis(self) -> Optional[dict]:
    """Get a list of all available APIs.

    Returns:
        dict: List of available APIs.
    """
    ...
```

**Возвращает**:

-   `dict`: Список доступных API.

**Как работает функция**:

1.  Вызывает функцию `_exec` для выполнения запроса к API PrestaShop и получения списка доступных API.
2.  Возвращает от функцию `_exec`

## Переменные модуля

-   `Config`: Внутренний класс для хранения конфигурационных параметров, таких как домен API и ключ API.
    -   `language` (str): Код языка.
    -   `ps_version` (str): Версия PrestaShop.
    -   `MODE` (str): Определяет конечную точку API ('dev', 'dev8', 'prod').
    -   `POST_FORMAT` (str): Определяет формат данных для POST-запросов (JSON или XML).
    -   `API_DOMAIN` (str): Домен API PrestaShop.
    -   `API_KEY` (str): Ключ API PrestaShop.

## Пример использования

**Чтение данных о товаре:**

```python
from src.endpoints.prestashop.api import PrestaShop

# Инициализация класса PrestaShop
api = PrestaShop(api_key='YOUR_API_KEY', api_domain='https://your-prestashop-domain.com')

# Получение данных о товаре с ID 1
product_data = api.read('products', 1)
print(product_data)
```

## Взаимосвязь с другими частями проекта

-   Модуль `src/endpoints/prestashop/api/api.py` предоставляет базовый класс `PrestaShop`, который используется другими модулями для взаимодействия с API PrestaShop.
-   Он использует модуль `src.logger.exceptions` для определения пользовательских исключений и модуль `src.logger.logger` для логирования.
-   Также модуль использует `src.utils.jjson` и `src.utils.convertors.dict` для работы с JSON и XML, соответственно.