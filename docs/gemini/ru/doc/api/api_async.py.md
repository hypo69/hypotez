### Анализ кода модуля `src/endpoints/prestashop/api/api_async.py`

## Обзор

Этот модуль предоставляет асинхронный интерфейс для взаимодействия с PrestaShop webservice API, используя JSON и XML для форматирования сообщений.

## Подробней

Модуль `src/endpoints/prestashop/api/api_async.py` определяет асинхронный класс `PrestaShopAsync`, который позволяет взаимодействовать с API PrestaShop, используя асинхронные запросы. Он предоставляет методы для выполнения CRUD операций (создание, чтение, обновление, удаление), поиска ресурсов и загрузки изображений.

## Классы

### `Format`

**Описание**: Enum, определяющий типы данных для возврата (JSON, XML).

**Члены**:

-   `JSON`: Представляет формат JSON.
-   `XML`: Представляет формат XML.

### `PrestaShopAsync`

**Описание**: Асинхронный класс для взаимодействия с PrestaShop API.

**Атрибуты**:

-   `client` (ClientSession): Асинхронный HTTP клиент для выполнения запросов.
-   `debug` (bool): Флаг, указывающий, включен ли режим отладки.
-   `lang_index` (Optional[int]): Индекс языка.
-   `data_format` (str): Формат данных ('JSON' или 'XML').
-   `ps_version` (str): Версия PrestaShop.
-   `API_DOMAIN` (str): Домен API.
-   `API_KEY` (str): Ключ API.

**Методы**:

-   `__init__(self, api_domain: str, api_key: str, data_format: str = Config.POST_FORMAT, debug: bool = True) -> None`: Инициализирует объект `PrestaShopAsync`.
-   `ping(self) -> bool`: Проверяет работоспособность веб-сервиса асинхронно.
-   `_check_response(self, status_code: int, response: ClientResponse, method: Optional[str] = None, url: Optional[str] = None, headers: Optional[dict] = None, data: Optional[dict] = None) -> bool`: Проверяет код ответа и обрабатывает ошибки асинхронно.
-   `_parse_response_error(self, response: ClientResponse, method: Optional[str] = None, url: Optional[str] = None, headers: Optional[dict] = None, data: Optional[dict] = None)`: Разбирает сообщение об ошибке из ответа API PrestaShop асинхронно.
-   `_prepare(self, url: str, params: dict) -> str`: Подготавливает URL для запроса.
-   `_exec(self, resource: str, resource_id: Optional[Union[int, str]] = None, resource_ids: Optional[Union[int, Tuple[int]]] = None, method: str = 'GET', data: Optional[dict] = None, headers: Optional[dict] = None, search_filter: Optional[Union[str, dict]] = None, display: Optional[Union[str, list]] = 'full', schema: Optional[str] = None, sort: Optional[str] = None, limit: Optional[str] = None, language: Optional[int] = None, io_format: str = 'JSON') -> Optional[dict]`: Выполняет HTTP запрос к PrestaShop API асинхронно.
-   `create(self, resource: str, data: dict) -> Optional[dict]`: Создает новый ресурс в PrestaShop API асинхронно.
-   `read(self, resource: str, resource_id: Union[int, str], **kwargs) -> Optional[dict]`: Читает ресурс из PrestaShop API асинхронно.
-   `write(self, resource: str, data: dict) -> Optional[dict]`: Обновляет существующий ресурс в PrestaShop API асинхронно.
-   `unlink(self, resource: str, resource_id: Union[int, str]) -> bool`: Удаляет ресурс из PrestaShop API асинхронно.
-   `search(self, resource: str, filter: Optional[Union[str, dict]] = None, **kwargs) -> List[dict]`: Ищет ресурсы в PrestaShop API асинхронно.
-   `create_binary(self, resource: str, file_path: str, file_name: str) -> dict`: Загружает бинарный файл в ресурс API PrestaShop асинхронно.
-   `get_schema(self, resource: Optional[str] = None, resource_id: Optional[int] = None, schema: Optional[str] = 'blank', **kwards) -> dict | None`: Retrieve the schema of a given resource from PrestaShop API.
-   `get_data(self, resource: str, **kwargs) -> Optional[dict]`: Извлекает данные из ресурса PrestaShop API и сохраняет их асинхронно.
-   `get_apis(self) -> Optional[dict]`: Асинхронно получает список всех доступных API.
-   `upload_image_async(self, resource: str, resource_id: int, img_url: str, img_name: Optional[str] = None) -> Optional[dict]`: Uploads an image to PrestaShop API asynchronously.
-   `upload_image(self, resource: str, resource_id: int, img_url: str, img_name: Optional[str] = None) -> Optional[dict]`: Uploads an image to PrestaShop API asynchronously.
-    `get_product_images`

#### `__init__`

**Назначение**: Инициализирует объект `PrestaShopAsync`.

```python
def __init__(self,
                api_domain:str,
                api_key:str,
                data_format: str = 'JSON',
                debug: bool = True) -> None:
    """Initialize the PrestaShopAsync class.

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
-   `data_format` (str, optional): Формат данных по умолчанию ('JSON' или 'XML'). По умолчанию 'JSON'.
-   `debug` (bool, optional): Включает режим отладки. По умолчанию `True`.

**Как работает функция**:

1.  Принимает параметры для подключения к API PrestaShop.
2.  Инициализирует атрибуты объекта `PrestaShopAsync` значениями, полученными из аргументов.
3.  Создает асинхронный HTTP-клиент `aiohttp.ClientSession` с базовой аутентификацией, используя переданные учетные данные.

#### `ping`

**Назначение**: Проверяет работоспособность веб-сервиса асинхронно.

```python
async def ping(self) -> bool:
    """! Test if the webservice is working perfectly asynchronously.

    Returns:
        bool: Result of the ping test. Returns `True` if the webservice is working, otherwise `False`.
    """
    ...
```

**Возвращает**:

-   `bool`: `True`, если веб-сервис работает, `False` - в противном случае.

**Как работает функция**:

1.  Выполняет HEAD-запрос к API PrestaShop с использованием асинхронного HTTP-клиента.
2.  Вызывает метод `_check_response` для проверки статуса ответа.

#### `_check_response`

**Назначение**: Проверяет код ответа и обрабатывает ошибки асинхронно.

```python
def _check_response(self, status_code: int, response, method: Optional[str] = None, url: Optional[str] = None,
                        headers: Optional[dict] = None, data: Optional[dict] = None) -> bool:
    """! Check the response status code and handle errors asynchronously.

    Args:
        status_code (int): HTTP response status code.
        response (aiohttp.ClientResponse): HTTP response object.
        method (str, optional): HTTP method used for the request.
        url (str, optional): The URL of the request.
        headers (dict, optional): The headers used in the request.
        data (dict, optional): The data sent in the request.

    Returns:
        bool: `True` if the status code is 200 or 201, otherwise `False`.
    """
    ...
```

**Параметры**:

-   `status_code` (int): Код состояния HTTP-ответа.
-   `response` (aiohttp.ClientResponse): Объект HTTP-ответа.
-   `method` (str, optional): HTTP метод, используемый для запроса.
-   `url` (str, optional): URL запроса.
-   `headers` (dict, optional): Заголовки запроса.
-   `data` (dict, optional): Данные запроса.

**Возвращает**:

-   `bool`: `True`, если код ответа 200 или 201, иначе `False`.

**Как работает функция**:

1.  Проверяет, входит ли код состояния в список успешных кодов (200, 201).
2.  Если код ответа не является успешным, вызывает метод `_parse_response_error` для обработки ошибки.

#### `_parse_response_error`

**Назначение**: Разбирает сообщение об ошибке из ответа API PrestaShop асинхронно.

```python
def _parse_response_error(self, response, method: Optional[str] = None, url: Optional[str] = None,
                              headers: Optional[dict] = None, data: Optional[dict] = None):
    """! Parse the error response from PrestaShop API asynchronously.

    Args:
        response (aiohttp.ClientResponse): HTTP response object from the server.
        method (str, optional): HTTP method used for the request.
        url (str, optional): The URL of the request.
        headers (dict, optional): The headers used in the request.
        data (dict, optional): The data sent in the request.
    """
    ...
```

**Параметры**:

-   `response` (aiohttp.ClientResponse): Объект HTTP-ответа.
-   `method` (str, optional): HTTP метод, использованный для запроса.
-   `url` (str, optional): URL запроса.
-   `headers` (dict, optional): Заголовки запроса.
-   `data` (dict, optional): Данные запроса.

**Как работает функция**:

1.  Проверяет формат ответа (`self.data_format`).
2.  В зависимости от формата ответа (JSON или XML) извлекает код и сообщение об ошибке из ответа API.
3.  Логирует информацию об ошибке, используя `logger.critical`.

#### `_prepare`

**Назначение**: Подготавливает URL для запроса.

```python
def _prepare(self, url: str, params: dict) -> str:
    """! Prepare the URL for the request.

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

**Назначение**: Выполняет HTTP-запрос к PrestaShop API асинхронно.

```python
async def _exec(self,
              resource: str,
              resource_id: Optional[Union[int, str]] = None,
              resource_ids: Optional[Union[int, Tuple[int]]] = None,
              method: str = 'GET',
              data: Optional[dict] = None,
              headers: Optional[dict] = None,
              search_filter: Optional[Union[str, dict]] = None,
              display: Optional[Union[str, list]] = 'full',
              schema: Optional[str] = None,
              sort: Optional[str] = None,
              limit: Optional[str] = None,
              language: Optional[int] = None,
              io_format: str = 'JSON') -> Optional[dict]:
    """! Execute an HTTP request to the PrestaShop API asynchronously.

    Args:
        resource (str): The API resource (e.g., 'products', 'categories').
        resource_id (int | str, optional): The ID of the resource.
        resource_ids (int | tuple, optional): The IDs of multiple resources.
        method (str, optional): The HTTP method (GET, POST, PUT, DELETE).
        data (dict, optional): The data to be sent with the request.
        headers (dict, optional): Additional headers for the request.
        search_filter (str | dict, optional): Filter for the request.
        display (str | list, optional): Fields to display in the response.
        schema (str, optional): The schema of the data.
        sort (str, optional): Sorting parameter for the request.
        limit (str, optional): Limit of results for the request.
        language (int, optional): The language ID for the request.
        io_format (str, optional): The data format ('JSON' or 'XML').

    Returns:
        dict | None: The response from the API or `False` on failure.
    """
    ...
```

**Параметры**:

-   `resource` (str): API ресурс (например, 'products').
-   `resource_id` (Optional[int | str]): ID ресурса.
-    `resource_ids` (Optional[int | Tuple[int]]): ID ресурсов
-   `method` (str): HTTP метод ('GET', 'POST', 'PUT', 'DELETE'). По умолчанию 'GET'.
-   `data` (Optional[dict]): Данные для отправки (словарь или строка).
-   `headers` (Optional[dict]): Пользовательские заголовки запроса.
-   `search_filter` (Optional[str | dict]): Фильтр для поиска.
-   `display` (Optional[str | list]): Что отображать в ответе (например, 'full').
-   `schema` (Optional[str]): Используемая схема данных.
-   `sort` (Optional[str]): Порядок сортировки.
-   `limit` (Optional[str]): Лимит на количество возвращаемых записей.
    `language` (Optional[int]): The language ID for the request.
-   `io_format` (str, optional): Формат данных ('JSON' или 'XML').

**Возвращает**:

-   `dict | None`: Ответ от API в виде словаря или `False` в случае ошибки.

**Как работает функция**:

1.  Включает режим отладки, если `self.debug` равно `True`.
2.  Формирует URL для запроса, используя `_prepare`.
3.  Устанавливает заголовки запроса в зависимости от формата данных (`data_format`).
4.  Выполняет асинхронный HTTP-запрос с использованием `self.client.request`.
5.  Проверяет код ответа с помощью `self._check_response`.
6.  В случае успеха вызывает `self._parse_response` для разбора ответа.

### `_parse`

**Назначение**: Разбирает XML или JSON ответ от API в структуру словаря.

```python
def _parse(self, text: str) -> dict | ElementTree.Element | bool:
    """! Parse XML or JSON response from the API asynchronously.

    Args:
        text (str): Response text.

    Returns:
        dict | ElementTree.Element | bool: Parsed data or `False` on failure.
    """
    ...
```

**Параметры**:

-   `text` (str): Текст ответа.

**Возвращает**:

-   `dict | ElementTree.Element | bool`: Разобранные данные или `False` в случае ошибки.

**Как работает функция**:

1.  Пытается разобрать ответ как JSON, используя `j_loads(text)`.
2.  Если разбор JSON успешен, возвращает данные, извлекая корень `PrestaShop`.
3.  Если разбор JSON не удался, разбирает XML response
4.  В случае ошибки логирует информацию об ошибке и возвращает пустой словарь.

### `create`

**Назначение**: Создает новый ресурс в PrestaShop API асинхронно.

```python
async def create(self, resource: str, data: dict) -> Optional[dict]:
    """! Create a new resource in PrestaShop API asynchronously.

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

**Возвращает**:

-   `dict`: Ответ от API.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса и метода `POST`.

### `read`

**Назначение**: Читает ресурс из PrestaShop API асинхронно.

```python
async def read(self, resource: str, resource_id: Union[int, str], **kwargs) -> Optional[dict]:
    """! Read a resource from the PrestaShop API asynchronously.

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
-  `**kwargs`: Произвольные именованные аргументы, передаваемые в функцию.

**Возвращает**:

-   `dict`: Ответ от API.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса, ID ресурса и метода `GET`.

### `write`

**Назначение**: Обновляет существующий ресурс в PrestaShop API асинхронно.

```python
async def write(self, resource: str, data: dict) -> Optional[dict]:
    """! Update an existing resource in the PrestaShop API asynchronously.

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
-   `data` (dict): Данные для ресурса.

**Возвращает**:

-   `dict`: Ответ от API.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса, ID ресурса и метода `PUT`.

### `unlink`

**Назначение**: Удаляет ресурс из PrestaShop API асинхронно.

```python
async def unlink(self, resource: str, resource_id: Union[int, str]) -> bool:
    """! Delete a resource from the PrestaShop API asynchronously.

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

### `search`

**Назначение**: Ищет ресурсы в PrestaShop API асинхронно.

```python
async def search(self, resource: str, filter: Optional[Union[str, dict]] = None, **kwargs) -> List[dict]:
    """! Search for resources in the PrestaShop API asynchronously.

    Args:
        resource (str): API resource (e.g., 'products').
        filter (str | dict, optional): Filter for the search.

    Returns:
         List[dict]: List of resources matching the search criteria.
    """
    ...
```

**Параметры**:

-   `resource` (str): API ресурс (например, 'products').
-   `filter` (Optional[str  |  dict]): Фильтр для поиска.

**Возвращает**:

-   `List[dict]`: Список ресурсов, соответствующих критериям поиска.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса, фильтра и метода `GET`.

### `create_binary`

**Назначение**: Загружает бинарный файл в ресурс API PrestaShop асинхронно.

```python
async def create_binary(self, resource: str, file_path: str, file_name: str) -> dict:
    """! Upload a binary file to a PrestaShop API resource asynchronously.

    Args:
        resource (str): API resource (e.g., 'images/products/22').
        file_path (str): Path to the binary file.
        file_name (str): File name.

    Returns:
        dict: Response from the API.
    """
    ...
```

**Параметры**:

-   `resource` (str): API ресурс (например, 'images/products/22').
-   `file_path` (str): Путь к бинарному файлу.
-   `file_name` (str): Имя файла.

**Возвращает**:

-   `dict`: Ответ от API.

**Как работает функция**:

1.  Открывает указанный файл для чтения в бинарном режиме (`'rb'`).
2.  Формирует словарь `files` для передачи файла в запросе.
3.  Выполняет POST-запрос к API с использованием асинхронного HTTP-клиента.

### `get_schema`

**Назначение**: Получает схему ресурса из PrestaShop API.

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
                возможные значения, описания и другие метаданные. Это самый подробный вид схемы.
            - form (или что-то подобное): Реже, но может быть опция, возвращающая схему,
                оптимизированную для отображения в форме редактирования. Она может включать информацию о валидации
                полей, порядке отображения и т.п.

    Returns:
        dict  |  None: The schema of the requested resource or `None` in case of an error.
    """
    ...
```

**Параметры**:

-   `resource` (str): Имя ресурса (например, 'products', 'customers'). Если не указан, возвращается список всех схем сущностей, доступных для API ключа.
-   `resource_id` (Optional[str]):
-   `schema` (Optional[str]): Тип схемы. Возможные значения:
    -   `'blank'`: Возвращает пустую схему ресурса.
    -   `'synopsis'`: Возвращает упрощенную схему.
    -   `None`: Возвращает полную схему ресурса.
- `**kwards`: Произвольные именованные аргументы, передаваемые в функцию.

**Возвращает**:

-   `dict  |  None`: The schema of the requested resource or `None` in case of an error.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса, ID ресурса (если указан) и типа схемы.

### `get_data`

**Назначение**: Извлекает данные из ресурса PrestaShop API и сохраняет их асинхронно.

```python
async def get_data(self, resource: str, **kwargs) -> Optional[dict]:
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
2.  Сохраняет полученные данные в файл с помощью функции `_save`.
     -   В коде закомментирован кусок кода (отсутсвует реализация тела функции)

### `upload_image_async`

**Назначение**: Загружает изображение в ресурс API PrestaShop асинхронно.

```python
async def upload_image_async(self, resource: str, resource_id: int, img_url: str,
                           img_name: Optional[str] = None) -> Optional[dict]:
    """! Upload an image to PrestaShop API asynchronously.

    Args:
        resource (str): API resource (e.g., 'images/products/22').
        resource_id (int): Resource ID.
        img_url (str): URL of the image.
        img_name (str, optional): Name of the image file, defaults to None.

    Returns:
        dict | None: Response from the API or `False` on failure.
    """
    ...
```

**Параметры**:

-   `resource` (str): API ресурс (например, 'images/products/22').
-   `resource_id` (int): ID ресурса.
-   `img_url` (str): URL изображения.
-   `img_name` (str, optional): Имя файла изображения, по умолчанию `None`.

**Возвращает**:

-   `dict | None`: Ответ от API или `False` в случае ошибки.

**Как работает функция**:

1.  Разбивает URL изображения на части, чтобы получить расширение файла.
2.  Формирует имя файла для сохранения изображения.
3.  Загружает изображение с использованием `save_image_from_url`.
4.  Вызывает метод create_binary для добавления изображения.

    Логически не имеет смысла, поскольку в теле функции вызывается save_image_from_url, но в коде она не реализована.
5.  Удаляет временный файл изображения.
6.  Логирует информацию об ошибках, используя `logger.error`.

В коде присутствует логика для асинхронной загрузки изображения, однако отсутствует функция save_image_from_url.

### `upload_image`

**Назначение**: Uploads an image to PrestaShop API asynchronously. (Копия `upload_image_async`)

```python
async def upload_image(self, resource: str, resource_id: int, img_url: str,
                     img_name: Optional[str] = None) -> Optional[dict]:
    """! Upload an image to PrestaShop API asynchronously.

    Args:
        resource (str): API resource (e.g., 'images/products/22').
        resource_id (int): Resource ID.
        img_url (str): URL of the image.
        img_name (str, optional): Name of the image file, defaults to None.

    Returns:
        dict | None: Response from the API or `False` on failure.
    """
    ...
```

**Параметры**:

-   `resource` (str): API ресурс (например, 'images/products/22').
-   `resource_id` (int): ID ресурса.
-   `img_url` (str): URL изображения.
-   `img_name` (str, optional): Имя файла изображения, по умолчанию `None`.

**Возвращает**:

-   `dict | None`: Ответ от API или `False` в случае ошибки.

**Как работает функция**:

1.  Разбивает URL изображения на части, чтобы получить расширение файла.
2.  Формирует имя файла для сохранения изображения.
3.  Загружает изображение с использованием `save_image_from_url`.

        Логически не имеет смысла, поскольку в теле функции вызывается save_image_from_url, но в коде она не реализована.
4.  Вызывает метод create_binary для добавления изображения.
5.  Удаляет временный файл изображения.
6.  Логирует информацию об ошибках, используя `logger.error`.

В коде присутствует логика для асинхронной загрузки изображения, однако отсутствует функция save_image_from_url.

### `get_product_images`

**Назначение**: Получает изображения для продукта асинхронно.

```python
async def get_product_images(self, product_id: int) -> Optional[dict]:
    """! Get images for a product asynchronously.

    Args:
        product_id (int): Product ID.

    Returns:
        dict | None: List of product images or `False` on failure.
    """
    ...
```

**Параметры**:

-   `product_id` (int): ID продукта.

**Возвращает**:

-   `dict | None`: Список изображений продукта или `False` в случае ошибки.

**Как работает функция**:

1.  Формирует URL для запроса списка изображений продукта.
2.  Вызывает функцию `_exec` для выполнения запроса к API PrestaShop.

## Переменные модуля

-   Отсутствуют.

## Пример использования

**Создание экземпляра PrestaShopAsync и получение данных:**

```python
import asyncio
from src.endpoints.prestashop.api import PrestaShopAsync

async def main():
    api = PrestaShopAsync(api_domain='your_api_domain', api_key='your_api_key')
    
    product_data = await api.get_data('products', display='full')
    
    if product_data:
        print(f"Данные о товарах получены: {product_data}")
    else:
        print("Не удалось получить данные о товарах.")

if __name__ == "__main__":
    asyncio.run(main())
```

## Взаимосвязь с другими частями проекта

-   Модуль зависит от модуля `src.endpoints.prestashop.api` для выполнения запросов к PrestaShop API.
-   Зависит от `src.logger.logger` для логирования ошибок и информации.
- Зависит от модуля `src.utils.jjson` для обработки данных в формате JSON.
-   Модуль может использоваться другими частями проекта `hypotez` для получения информации о товарах и категориях PrestaShop.