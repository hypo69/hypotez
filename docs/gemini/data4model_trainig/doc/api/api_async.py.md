# Модуль `api_async`

## Обзор

Модуль `api_async` предоставляет асинхронные инструменты для взаимодействия с API PrestaShop. Он включает в себя класс `PrestaShopAsync`, который позволяет выполнять CRUD операции, поиск и загрузку изображений, используя асинхронные вызовы.

## Подробней

Модуль предназначен для обеспечения асинхронного взаимодействия с PrestaShop API, что позволяет повысить производительность и эффективность при работе с большим объемом данных или при необходимости параллельного выполнения операций.

## Классы

### `Format`

**Описание**: Перечисление, определяющее формат данных (JSON или XML).

**Атрибуты**:

*   `JSON` = `'JSON'`
*   `XML` = `'XML'`

### `PrestaShopAsync`

**Описание**: Асинхронный класс для взаимодействия с PrestaShop API.

**Атрибуты**:

*   `client` (ClientSession): Асинхронный HTTP клиент для выполнения запросов.
*   `debug` (bool): Флаг отладки.
*   `lang_index` (Optional[int]): Индекс языка.
*   `data_format` (str): Формат данных (JSON или XML).
*   `ps_version` (str): Версия PrestaShop.
*   `API_DOMAIN` (str): Домен API PrestaShop.
*   `API_KEY` (str): Ключ API PrestaShop.

**Методы**:

*   `__init__`: Инициализирует объект `PrestaShopAsync`.
*   `ping`: Асинхронно проверяет работоспособность API.
*   `_check_response`: Асинхронно проверяет статус ответа и обрабатывает ошибки.
*   `_parse_response_error`: Асинхронно разбирает сообщение об ошибке из ответа API.
*   `_prepare`: Подготавливает URL для запроса.
*   `_exec`: Асинхронно выполняет HTTP запрос к API PrestaShop.
*   `_parse`: Асинхронно разбирает XML или JSON ответ от API.
*   `create`: Асинхронно создает новый ресурс в PrestaShop API.
*   `read`: Асинхронно читает ресурс из PrestaShop API.
*   `write`: Асинхронно обновляет существующий ресурс в PrestaShop API.
*   `unlink`: Асинхронно удаляет ресурс из PrestaShop API.
*   `search`: Асинхронно выполняет поиск ресурсов в PrestaShop API.
*   `create_binary`: Асинхронно загружает бинарный файл в ресурс API PrestaShop.
*   `_save`: Сохраняет данные в файл.
*   `get_data`: Асинхронно извлекает данные из ресурса API PrestaShop и сохраняет их.
*   `remove_file`: Удаляет файл из файловой системы.
*   `get_apis`: Асинхронно получает список всех доступных API.
*   `get_languages_schema`: Асинхронно получает схему для языков.
*   `upload_image_async`: Асинхронно загружает изображение в PrestaShop API.
*   `upload_image`: Асинхронно загружает изображение в PrestaShop API.
*   `get_product_images`: Асинхронно получает изображения для товара.

### `__init__`

```python
def __init__(self,
            api_domain:str,
            api_key:str,
            data_format: str = 'JSON',
            debug: bool = True) -> None:
    """! Initialize the PrestaShopAsync class.

    Args:
        data_format (str, optional): Default data format ('JSON' or 'XML'). Defaults to 'JSON'.
        default_lang (int, optional): Default language ID. Defaults to 1.
        debug (bool, optional): Activate debug mode. Defaults to True.

    Raises:
        PrestaShopAuthenticationError: When the API key is wrong or does not exist.
        PrestaShopException: For generic PrestaShop WebServices errors.
    """
    ...
```

**Назначение**: Инициализирует объект `PrestaShopAsync`.

**Параметры**:

*   `api_domain` (str): Домен API PrestaShop.
*   `api_key` (str): Ключ API PrestaShop.
*   `data_format` (str): Формат данных (JSON или XML). По умолчанию `'JSON'`.
*   `debug` (bool): Флаг отладки. По умолчанию `True`.

**Как работает функция**:

1.  Устанавливает значения атрибутов `API_DOMAIN`, `API_KEY`, `debug` и `data_format`.
2.  Создает асинхронный HTTP клиент `ClientSession` с аутентификацией и таймаутом.

### `ping`

```python
async def ping(self) -> bool:
    """! Test if the webservice is working perfectly asynchronously.

    Returns:
        bool: Result of the ping test. Returns `True` if the webservice is working, otherwise `False`.
    """
    ...
```

**Назначение**: Асинхронно проверяет работоспособность API PrestaShop.

**Возвращает**:

*   `bool`: `True`, если API работает, иначе `False`.

**Как работает функция**:

1.  Выполняет HEAD запрос к API с использованием асинхронного HTTP клиента.
2.  Проверяет статус ответа с помощью метода `_check_response`.

### `_check_response`

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

**Назначение**: Асинхронно проверяет статус ответа и обрабатывает ошибки.

**Параметры**:

*   `status_code` (int): HTTP статус код ответа.
*   `response` (aiohttp.ClientResponse): Объект HTTP ответа.
*   `method` (str, optional): HTTP метод, использованный для запроса.
*   `url` (str, optional): URL запроса.
*   `headers` (dict, optional): Заголовки, использованные в запросе.
*   `data` (dict, optional): Данные, отправленные в запросе.

**Возвращает**:

*   `bool`: `True`, если статус код 200 или 201, иначе `False`.

**Как работает функция**:

1.  Проверяет, является ли статус код 200 или 201.
2.  Если статус код не является 200 или 201, вызывает метод `_parse_response_error` для обработки ошибки.

### `_parse_response_error`

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

**Назначение**: Асинхронно разбирает сообщение об ошибке из ответа API PrestaShop.

**Параметры**:

*   `response` (aiohttp.ClientResponse): Объект HTTP ответа от сервера.
*   `method` (str, optional): HTTP метод, использованный для запроса.
*   `url` (str, optional): URL запроса.
*   `headers` (dict, optional): Заголовки, использованные в запросе.
*   `data` (dict, optional): Данные, отправленные в запросе.

**Как работает функция**:

1.  Проверяет формат ответа (JSON или XML).
2.  В зависимости от формата разбирает ответ и извлекает код и сообщение об ошибке.
3.  Логирует сообщение об ошибке.

### `_prepare`

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

**Назначение**: Подготавливает URL для запроса.

**Параметры**:

*   `url` (str): Базовый URL.
*   `params` (dict): Параметры для запроса.

**Возвращает**:

*   `str`: Подготовленный URL с параметрами.

**Как работает функция**:

1.  Использует класс `PreparedRequest` из библиотеки `requests` для подготовки URL с параметрами.

### `_exec`

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

**Назначение**: Асинхронно выполняет HTTP запрос к API PrestaShop.

**Параметры**:

*   `resource` (str): Ресурс API (например, `'products'`, `'categories'`).
*   `resource_id` (Union[int, str], optional): ID ресурса.
*   `resource_ids` (Union[int, Tuple[int]], optional): ID ресурсов.
*   `method` (str, optional): HTTP метод (`'GET'`, `'POST'`, `'PUT'`, `'DELETE'`).
*   `data` (Optional[dict]): Данные для отправки в запросе.
*   `headers` (Optional[dict]): Заголовки запроса.
*   `search_filter` (Optional[Union[str, dict]]): Фильтр для поиска.
*   `display` (Optional[Union[str, list]]): Что отображать в ответе.
*   `schema` (Optional[str]): Схема ресурса.
*   `sort` (Optional[str]): Параметр сортировки для запроса.
*   `limit` (Optional[str]): Лимит результатов для запроса.
*   `language` (Optional[int]): ID языка для запроса.
*   `io_format` (str): Формат ввода/вывода данных (`'JSON'` или `'XML'`).

**Возвращает**:

*   `Optional[dict]`: Разобранные данные из ответа API или `False` в случае ошибки.

**Как работает функция**:

1.  Подготавливает URL для запроса с использованием метода `_prepare`.
2.  Преобразует данные в XML, если `io_format` равен `'XML'`.
3.  Выполняет асинхронный HTTP-запрос с использованием библиотеки `aiohttp`.
4.  Проверяет статус ответа с помощью метода `_check_response`.
5.  Разбирает ответ с помощью метода `_parse`.

### `_parse`

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

**Назначение**: Асинхронно разбирает XML или JSON ответ от API.

**Параметры**:

*   `text` (str): Текст ответа.

**Возвращает**:

*   `dict | ElementTree.Element | bool`: Разобранные данные или `False` в случае неудачи.

**Как работает функция**:

1.  Определяет формат данных.
2.  Если формат данных JSON, загружает текст как JSON с помощью `j_loads`.
3.  Если формат данных XML, разбирает текст как XML с помощью `ElementTree.fromstring`.
4.  В случае ошибки разбора логирует ошибку и возвращает `False`.

### `create`

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

**Назначение**: Асинхронно создает новый ресурс в API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'products'`).
*   `data` (dict): Данные для нового ресурса.

**Возвращает**:

*   `Optional[dict]`: Ответ от API.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `method='POST'`, `data` и `io_format=self.data_format`.

### `read`

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

**Назначение**: Асинхронно читает ресурс из API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'products'`).
*   `resource_id` (Union[int, str]): ID ресурса.
*   `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:

*   `Optional[dict]`: Ответ от API.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `resource_id`, `method='GET'` и `io_format= self.data_format`.

### `write`

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

**Назначение**: Асинхронно обновляет существующий ресурс в API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'products'`).
*   `data` (dict): Данные для обновления ресурса.

**Возвращает**:

*   `Optional[dict]`: Ответ от API.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `resource_id=data.get('id')`, `method='PUT'`, `data` и `io_format=self.data_format`.

### `unlink`

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

**Назначение**: Асинхронно удаляет ресурс из API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'products'`).
*   `resource_id` (Union[int, str]): ID ресурса.

**Возвращает**:

*   `bool`: `True`, если удаление успешно, иначе `False`.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `resource_id`, `method='DELETE'` и `io_format=self.data_format`.

### `search`

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

**Назначение**: Асинхронно выполняет поиск ресурсов в API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'products'`).
*   `filter` (Union[str, dict], optional): Фильтр для поиска.
*   `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:

*   `List[dict]`: Список ресурсов, соответствующих критериям поиска.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `search_filter=filter`, `method='GET'` и `io_format=self.data_format`.

### `create_binary`

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

**Назначение**: Асинхронно загружает бинарный файл в ресурс API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'images/products/22'`).
*   `file_path` (str): Путь к бинарному файлу.
*   `file_name` (str): Имя файла.

**Возвращает**:

*   `dict`: Ответ от API.

**Как работает функция**:

1.  Открывает файл в бинарном режиме.
2.  Устанавливает заголовок `Content-Type` как `application/octet-stream`.
3.  Выполняет POST запрос к API с использованием библиотеки `aiohttp`.

### `_save`

```python
def _save(self, file_name: str, data: dict):
    """! Save data to a file.

    Args:
        file_name (str): Name of the file.
        data (dict): Data to be saved.
    """
    ...
```

**Назначение**: Сохраняет данные в файл.

**Параметры**:

*   `file_name` (str): Имя файла.
*   `data` (dict): Данные для сохранения.

**Как работает функция**:

1.  Вызывает функцию `save_text_file` для сохранения данных в файл в формате JSON.

### `get_data`

```python
async def get_data(self, resource: str, **kwargs) -> Optional[dict]:
    """! Fetch data from a PrestaShop API resource and save it asynchronously.

    Args:
        resource (str): API resource (e.g., 'products').
        **kwargs: Additional arguments for the API request.

    Returns:
        dict | None: Data from the API or `False` on failure.
    """
    ...
```

**Назначение**: Асинхронно извлекает данные из ресурса API PrestaShop и сохраняет их.

**Параметры**:

*   `resource` (str): API ресурс (например, `'products'`).
*   `**kwargs`: Дополнительные аргументы для запроса API.

**Возвращает**:

*   `dict | None`: Данные из API или `False` в случае неудачи.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметром `resource` и `method='GET'`.
2.  Сохраняет полученные данные в файл с помощью метода `_save`.

### `remove_file`

```python
def remove_file(self, file_path: str):
    """! Remove a file from the filesystem.

    Args:
        file_path (str): Path to the file.
    """
    ...
```

**Назначение**: Удаляет файл из файловой системы.

**Параметры**:

*   `file_path` (str): Путь к файлу.

**Как работает функция**:

1.  Вызывает функцию `os.remove` для удаления файла.
2.  В случае ошибки логирует сообщение об ошибке.

### `get_apis`

```python
async def get_apis(self) -> Optional[dict]:
    """! Get a list of all available APIs asynchronously.

    Returns:
         dict: List of available APIs.
    """
    ...
```

**Назначение**: Асинхронно получает список всех доступных API.

**Возвращает**:

*   `dict`: Список доступных API.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметром `'apis'` и `method='GET'`.

### `get_languages_schema`

```python
async def get_languages_schema(self) -> Optional[dict]:
    """! Get the schema for languages asynchronously.

    Returns:
        dict: Language schema or `None` on failure.
    """
    ...
```

**Назначение**: Асинхронно получает схему для языков.

**Возвращает**:

*   `dict`: Схема языка или `None` в случае ошибки.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `'languages'`, `display='full'` и `io_format='JSON'`.

### `upload_image_async`

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

**Назначение**: Асинхронно загружает изображение в API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'images/products/22'`).
*   `resource_id` (int): ID ресурса.
*   `img_url` (str): URL изображения.
*   `img_name` (str, optional): Имя файла изображения, по умолчанию `None`.

**Возвращает**:

*   `dict | None`: Ответ от API или `False` в случае ошибки.

**Как работает функция**:

1.  Разделяет URL изображения на имя файла и расширение.
2.  Формирует имя файла для сохранения.
3.  Асинхронно сохраняет изображение из URL во временный файл.
4.  Вызывает метод `create_binary` для загрузки изображения в API.
5.  Удаляет временный файл.

### `upload_image`

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

**Назначение**: Асинхронно загружает изображение в API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'images/products/22'`).
*   `resource_id` (int): ID ресурса.
*   `img_url` (str): URL изображения.
*   `img_name` (str, optional): Имя файла изображения, по умолчанию `None`.

**Возвращает**:

*   `dict | None`: Ответ от API или `False` в случае ошибки.

**Как работает функция**:

1.  Разделяет URL изображения на имя файла и расширение.
2.  Формирует имя файла для сохранения.
3.  Асинхронно сохраняет изображение из URL во временный файл.
4.  Вызывает метод `create_binary` для загрузки изображения в API.
5.  Удаляет временный файл.

### `get_product_images`

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

**Назначение**: Асинхронно получает изображения для товара.

**Параметры**:

*   `product_id` (int): ID товара.

**Возвращает**:

*   `dict | None`: Список изображений товара или `False` в случае неудачи.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметром `f'products/{product_id}/images'` и `method='GET'`.