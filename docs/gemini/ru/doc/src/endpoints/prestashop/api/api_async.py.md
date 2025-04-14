# Модуль для асинхронного взаимодействия с API PrestaShop
============================================================

Модуль содержит класс `PrestaShopAsync`, который предоставляет асинхронные методы для взаимодействия с API PrestaShop, включая операции CRUD, поиск и загрузку изображений.

## Обзор

Модуль предназначен для асинхронного взаимодействия с API PrestaShop. Он поддерживает форматы данных JSON и XML, предоставляет методы для выполнения основных операций, таких как создание, чтение, обновление и удаление ресурсов, а также для поиска и загрузки изображений. Класс `PrestaShopAsync` упрощает взаимодействие с API PrestaShop, обрабатывая ошибки и предоставляя удобный интерфейс для выполнения запросов.

## Подробнее

Этот модуль предоставляет асинхронный класс `PrestaShopAsync` для взаимодействия с API PrestaShop. Он включает в себя функции для выполнения HTTP-запросов, обработки ответов, аутентификации и преобразования данных между форматами JSON и XML. Модуль также содержит обработку ошибок и ведение журнала для отслеживания проблем и ошибок. Он разработан для упрощения взаимодействия с API PrestaShop и предоставления удобного интерфейса для разработчиков.

## Классы

### `Format`

**Описание**: Перечисление, определяющее формат данных для взаимодействия с API (JSON или XML).

**Наследует**: `Enum`

**Атрибуты**:
- `JSON`: Представляет формат JSON.
- `XML`: Представляет формат XML.

**Принцип работы**:
Перечисление `Format` используется для указания формата данных, который будет использоваться при взаимодействии с API PrestaShop. В данном случае предпочтение отдается формату JSON.

### `PrestaShopAsync`

**Описание**: Асинхронный класс для взаимодействия с API PrestaShop, поддерживающий форматы JSON и XML.

**Атрибуты**:
- `client` (ClientSession): Асинхронная HTTP-сессия для выполнения запросов.
- `debug` (bool): Флаг, указывающий, включен ли режим отладки.
- `lang_index` (Optional[int]): Индекс языка по умолчанию.
- `data_format` (str): Формат данных по умолчанию ('JSON' или 'XML').
- `ps_version` (str): Версия PrestaShop.
- `API_DOMAIN` (str): Домен API PrestaShop.
- `API_KEY` (str): Ключ API для аутентификации.

**Параметры**:
- `api_domain` (str): Домен API PrestaShop.
- `api_key` (str): Ключ API для аутентификации.
- `data_format` (str, optional): Формат данных по умолчанию ('JSON' или 'XML'). По умолчанию 'JSON'.
- `debug` (bool, optional): Флаг, указывающий, включен ли режим отладки. По умолчанию `True`.

**Принцип работы**:
Класс `PrestaShopAsync` предоставляет асинхронные методы для взаимодействия с API PrestaShop. Он инициализируется с доменом API и ключом API, создает асинхронную HTTP-сессию и предоставляет методы для выполнения различных операций, таких как создание, чтение, обновление и удаление ресурсов. Класс также обрабатывает ошибки и форматирует данные для отправки и получения из API.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `PrestaShopAsync`.
- `ping`: Проверяет, работает ли веб-сервис асинхронно.
- `_check_response`: Проверяет код состояния ответа и обрабатывает ошибки асинхронно.
- `_parse_response_error`: Разбирает ответ об ошибке от API PrestaShop асинхронно.
- `_prepare`: Подготавливает URL для запроса.
- `_exec`: Выполняет HTTP-запрос к API PrestaShop асинхронно.
- `_parse`: Разбирает XML или JSON ответ от API асинхронно.
- `create`: Создает новый ресурс в API PrestaShop асинхронно.
- `read`: Читает ресурс из API PrestaShop асинхронно.
- `write`: Обновляет существующий ресурс в API PrestaShop асинхронно.
- `unlink`: Удаляет ресурс из API PrestaShop асинхронно.
- `search`: Ищет ресурсы в API PrestaShop асинхронно.
- `create_binary`: Загружает бинарный файл в ресурс API PrestaShop асинхронно.
- `_save`: Сохраняет данные в файл.
- `get_data`: Получает данные из ресурса API PrestaShop и сохраняет их асинхронно.
- `remove_file`: Удаляет файл из файловой системы.
- `get_apis`: Получает список всех доступных API асинхронно.
- `get_languages_schema`: Получает схему для языков асинхронно.
- `upload_image_async`: Загружает изображение в API PrestaShop асинхронно.
- `upload_image`: Загружает изображение в API PrestaShop асинхронно.
- `get_product_images`: Получает изображения для продукта асинхронно.

## Методы класса

### `__init__`

```python
def __init__(self, api_domain: str, api_key: str, data_format: str = 'JSON', debug: bool = True) -> None:
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

**Назначение**: Инициализирует класс `PrestaShopAsync` с заданными параметрами.

**Параметры**:
- `api_domain` (str): Домен API PrestaShop.
- `api_key` (str): Ключ API для аутентификации.
- `data_format` (str, optional): Формат данных по умолчанию ('JSON' или 'XML'). По умолчанию 'JSON'.
- `debug` (bool, optional): Флаг, указывающий, включен ли режим отладки. По умолчанию `True`.

**Как работает функция**:
Функция инициализирует объект `PrestaShopAsync`, устанавливает домен API, ключ API, формат данных и режим отладки. Она также создает асинхронную HTTP-сессию с использованием `aiohttp.ClientSession` для выполнения запросов к API PrestaShop. В качестве аутентификации используется `aiohttp.BasicAuth` с API-ключом и пустым паролем.

**Примеры**:
```python
api = PrestaShopAsync(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key',
    data_format='JSON',
    debug=True
)
```

### `ping`

```python
async def ping(self) -> bool:
    """! Test if the webservice is working perfectly asynchronously.

    Returns:
        bool: Result of the ping test. Returns `True` if the webservice is working, otherwise `False`.
    """
    ...
```

**Назначение**: Проверяет, работает ли веб-сервис асинхронно.

**Возвращает**:
- `bool`: `True`, если веб-сервис работает, иначе `False`.

**Как работает функция**:
Функция отправляет HEAD-запрос к домену API и проверяет статус ответа. Если статус код 200 или 201, функция возвращает `True`, что указывает на то, что веб-сервис работает. В противном случае возвращается `False`.

**Примеры**:
```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key'
    )
    result = await api.ping()
    print(f"Ping result: {result}")

asyncio.run(main())
```

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

**Назначение**: Проверяет код состояния ответа и обрабатывает ошибки асинхронно.

**Параметры**:
- `status_code` (int): HTTP-код состояния ответа.
- `response` (aiohttp.ClientResponse): Объект HTTP-ответа.
- `method` (str, optional): HTTP-метод, используемый для запроса.
- `url` (str, optional): URL запроса.
- `headers` (dict, optional): Заголовки, используемые в запросе.
- `data` (dict, optional): Данные, отправленные в запросе.

**Возвращает**:
- `bool`: `True`, если код состояния равен 200 или 201, иначе `False`.

**Как работает функция**:
Функция проверяет, находится ли код состояния ответа в диапазоне успешных кодов (200 или 201). Если код состояния находится в этом диапазоне, функция возвращает `True`. В противном случае функция вызывает `_parse_response_error` для обработки ошибки и возвращает `False`.

**Примеры**:
```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key'
    )
    async with aiohttp.ClientSession() as session:
        async with session.get('https://your-prestashop-domain.com') as response:
            result = api._check_response(response.status, response)
            print(f"Response check result: {result}")

asyncio.run(main())
```

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

**Назначение**: Разбирает ответ об ошибке от API PrestaShop асинхронно.

**Параметры**:
- `response` (aiohttp.ClientResponse): Объект HTTP-ответа от сервера.
- `method` (str, optional): HTTP-метод, используемый для запроса.
- `url` (str, optional): URL запроса.
- `headers` (dict, optional): Заголовки, используемые в запросе.
- `data` (dict, optional): Данные, отправленные в запросе.

**Как работает функция**:
Функция разбирает ответ об ошибке от API PrestaShop в зависимости от формата данных. Если формат данных JSON, функция извлекает код состояния и текст ответа и записывает критическое сообщение в журнал. Если формат данных XML, функция разбирает XML-ответ, извлекает код и сообщение об ошибке и записывает сообщение об ошибке в журнал.

**Примеры**:
```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key'
    )
    async with aiohttp.ClientSession() as session:
        async with session.get('https://your-prestashop-domain.com/nonexistent') as response:
            api._parse_response_error(response)

asyncio.run(main())
```

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
- `url` (str): Базовый URL.
- `params` (dict): Параметры для запроса.

**Возвращает**:
- `str`: Подготовленный URL с параметрами.

**Как работает функция**:
Функция создает объект `PreparedRequest`, подготавливает URL с параметрами и возвращает подготовленный URL в виде строки.

**Примеры**:
```python
api = PrestaShopAsync(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key'
)
url = 'https://your-prestashop-domain.com/api/products'
params = {'display': 'full', 'limit': '1'}
prepared_url = api._prepare(url, params)
print(f"Prepared URL: {prepared_url}")
```

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

**Назначение**: Выполняет HTTP-запрос к API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API-ресурс (например, 'products', 'categories').
- `resource_id` (int | str, optional): ID ресурса.
- `resource_ids` (int | tuple, optional): ID нескольких ресурсов.
- `method` (str, optional): HTTP-метод (GET, POST, PUT, DELETE).
- `data` (dict, optional): Данные для отправки с запросом.
- `headers` (dict, optional): Дополнительные заголовки для запроса.
- `search_filter` (str | dict, optional): Фильтр для запроса.
- `display` (str | list, optional): Поля для отображения в ответе.
- `schema` (str, optional): Схема данных.
- `sort` (str, optional): Параметр сортировки для запроса.
- `limit` (str, optional): Лимит результатов для запроса.
- `language` (int, optional): ID языка для запроса.
- `io_format` (str, optional): Формат данных ('JSON' или 'XML').

**Возвращает**:
- `dict | None`: Ответ от API или `False` в случае неудачи.

**Как работает функция**:
Функция выполняет HTTP-запрос к API PrestaShop с использованием указанных параметров. Она подготавливает URL, добавляет параметры запроса, устанавливает заголовки и отправляет данные в нужном формате. Затем функция проверяет ответ и возвращает данные в формате JSON или XML.

**Примеры**:
```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key'
    )
    resource = 'products'
    data = {'product': {'name': 'Test Product'}}
    response = await api._exec(resource=resource, method='POST', data=data)
    print(f"API response: {response}")

asyncio.run(main())
```

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

**Назначение**: Разбирает XML или JSON ответ от API асинхронно.

**Параметры**:
- `text` (str): Текст ответа.

**Возвращает**:
- `dict | ElementTree.Element | bool`: Разобранные данные или `False` в случае неудачи.

**Как работает функция**:
Функция пытается разобрать текст ответа в зависимости от формата данных. Если формат данных JSON, функция использует `j_loads` для разбора текста в JSON и возвращает данные. Если формат данных XML, функция использует `ElementTree.fromstring` для разбора текста в XML и возвращает дерево элементов. В случае ошибки разбора функция записывает сообщение об ошибке в журнал и возвращает `False`.

**Примеры**:
```python
api = PrestaShopAsync(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key'
)
json_data = '{"PrestaShop":{"products":[{"id":1,"name":"Test Product"}]}}'
parsed_json = api._parse(json_data)
print(f"Parsed JSON: {parsed_json}")

xml_data = '<PrestaShop><products><product><id>1</id><name>Test Product</name></product></products></PrestaShop>'
parsed_xml = api._parse(xml_data)
print(f"Parsed XML: {parsed_xml}")
```

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

**Назначение**: Создает новый ресурс в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API-ресурс (например, 'products').
- `data` (dict): Данные для нового ресурса.

**Возвращает**:
- `dict`: Ответ от API.

**Как работает функция**:
Функция вызывает `_exec` с методом 'POST' для создания нового ресурса в API PrestaShop. Она передает ресурс и данные для создания ресурса.

**Примеры**:
```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key'
    )
    resource = 'products'
    data = {'product': {'name': 'Test Product'}}
    response = await api.create(resource, data)
    print(f"API response: {response}")

asyncio.run(main())
```

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

**Назначение**: Читает ресурс из API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API-ресурс (например, 'products').
- `resource_id` (int | str): ID ресурса.

**Возвращает**:
- `dict`: Ответ от API.

**Как работает функция**:
Функция вызывает `_exec` с методом 'GET' для чтения ресурса из API PrestaShop. Она передает ресурс и ID ресурса для чтения.

**Примеры**:
```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key'
    )
    resource = 'products'
    resource_id = 1
    response = await api.read(resource, resource_id)
    print(f"API response: {response}")

asyncio.run(main())
```

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

**Назначение**: Обновляет существующий ресурс в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API-ресурс (например, 'products').
- `data` (dict): Данные для ресурса.

**Возвращает**:
- `dict`: Ответ от API.

**Как работает функция**:
Функция вызывает `_exec` с методом 'PUT' для обновления существующего ресурса в API PrestaShop. Она передает ресурс и данные для обновления ресурса.

**Примеры**:
```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key'
    )
    resource = 'products'
    data = {'id': 1, 'product': {'name': 'Updated Test Product'}}
    response = await api.write(resource, data)
    print(f"API response: {response}")

asyncio.run(main())
```

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

**Назначение**: Удаляет ресурс из API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API-ресурс (например, 'products').
- `resource_id` (int | str): ID ресурса.

**Возвращает**:
- `bool`: `True`, если удаление прошло успешно, `False` в противном случае.

**Как работает функция**:
Функция вызывает `_exec` с методом 'DELETE' для удаления ресурса из API PrestaShop. Она передает ресурс и ID ресурса для удаления.

**Примеры**:
```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key'
    )
    resource = 'products'
    resource_id = 1
    response = await api.unlink(resource, resource_id)
    print(f"API response: {response}")

asyncio.run(main())
```

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

**Назначение**: Ищет ресурсы в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API-ресурс (например, 'products').
- `filter` (str | dict, optional): Фильтр для поиска.

**Возвращает**:
- `List[dict]`: Список ресурсов, соответствующих критериям поиска.

**Как работает функция**:
Функция вызывает `_exec` с методом 'GET' и параметром `search_filter` для поиска ресурсов в API PrestaShop. Она передает ресурс и фильтр для поиска.

**Примеры**:
```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key'
    )
    resource = 'products'
    filter = '[name]=%Test%'
    response = await api.search(resource, filter=filter)
    print(f"API response: {response}")

asyncio.run(main())
```

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

**Назначение**: Загружает бинарный файл в ресурс API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API-ресурс (например, 'images/products/22').
- `file_path` (str): Путь к бинарному файлу.
- `file_name` (str): Имя файла.

**Возвращает**:
- `dict`: Ответ от API.

**Как работает функция**:
Функция открывает файл в бинарном режиме, устанавливает заголовок 'Content-Type' в 'application/octet-stream' и отправляет содержимое файла в API PrestaShop с использованием метода POST.

**Примеры**:
```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key'
    )
    resource = 'images/products/22'
    file_path = 'img.jpg'
    file_name = 'img.jpg'
    response = await api.create_binary(resource, file_path, file_name)
    print(f"API response: {response}")

asyncio.run(main())
```

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
- `file_name` (str): Имя файла.
- `data` (dict): Данные для сохранения.

**Как работает функция**:
Функция использует `save_text_file` для сохранения данных в файл в формате JSON с отступами и поддержкой Unicode.

**Примеры**:
```python
api = PrestaShopAsync(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key'
)
file_name = 'data.json'
data = {'key': 'value'}
api._save(file_name, data)
```

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

**Назначение**: Получает данные из ресурса API PrestaShop и сохраняет их асинхронно.

**Параметры**:
- `resource` (str): API-ресурс (например, 'products').
- `**kwargs`: Дополнительные аргументы для API-запроса.

**Возвращает**:
- `dict | None`: Данные из API или `False` в случае неудачи.

**Как работает функция**:
Функция вызывает `_exec` для получения данных из API, затем сохраняет данные в файл с использованием `_save`.

**Примеры**:
```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key'
    )
    resource = 'products'
    response = await api.get_data(resource)
    print(f"API response: {response}")

asyncio.run(main())
```

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
- `file_path` (str): Путь к файлу.

**Как работает функция**:
Функция пытается удалить файл из файловой системы с использованием `os.remove`. В случае ошибки функция записывает сообщение об ошибке в журнал.

**Примеры**:
```python
api = PrestaShopAsync(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key'
)
file_path = 'data.json'
api._save(file_path, {'key': 'value'})  # create temporary file
api.remove_file(file_path)
```

### `get_apis`

```python
async def get_apis(self) -> Optional[dict]:
    """! Get a list of all available APIs asynchronously.

    Returns:
         dict: List of available APIs.
    """
    ...
```

**Назначение**: Получает список всех доступных API асинхронно.

**Возвращает**:
- `dict`: Список доступных API.

**Как работает функция**:
Функция вызывает `_exec` с ресурсом 'apis' и методом 'GET' для получения списка доступных API.

**Примеры**:
```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key'
    )
    response = await api.get_apis()
    print(f"API response: {response}")

asyncio.run(main())
```

### `get_languages_schema`

```python
async def get_languages_schema(self) -> Optional[dict]:
    """! Get the schema for languages asynchronously.

    Returns:
        dict: Language schema or `None` on failure.
    """
    ...
```

**Назначение**: Получает схему для языков асинхронно.

**Возвращает**:
- `dict`: Схема языка или `None` в случае неудачи.

**Как работает функция**:
Функция вызывает `_exec` с ресурсом 'languages', параметром `display='full'` и методом 'GET' для получения схемы языков.

**Примеры**:
```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key'
    )
    response = await api.get_languages_schema()
    print(f"API response: {response}")

asyncio.run(main())
```

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

**Назначение**: Загружает изображение в API PrestaShop асинхронно.

**Парамет