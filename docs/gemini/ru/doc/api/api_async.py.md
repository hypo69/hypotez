### Анализ кода `hypotez/src/endpoints/prestashop/api/api_async.py.md`

## Обзор

Модуль предоставляет асинхронный интерфейс для взаимодействия с PrestaShop API.

## Подробнее

Этот модуль определяет класс `PrestaShopAsync`, который позволяет асинхронно взаимодействовать с PrestaShop WebService API, используя JSON и XML для форматирования сообщений. Он поддерживает CRUD-операции, поиск и загрузку изображений, а также предоставляет обработку ошибок для ответов и методы для обработки данных API.

## Классы

### `PrestaShopAsync`

```python
class PrestaShopAsync:
    """! Async Class for interacting with the PrestaShop API using JSON and XML.

    This class provides asynchronous methods to interact with the PrestaShop API,
    allowing for CRUD operations, searching, and uploading images. It also provides
    error handling for responses and methods to handle the API's data.

    Example usage:

    .. code-block:: python

        async def main():
            api = PrestaShopAsync(
                API_DOMAIN='https://your-prestashop-domain.com',
                API_KEY='your_api_key',
                default_lang=1,
                debug=True,
                data_format='JSON',
            )

            await api.ping()

            data = {
                'tax': {
                    'rate': 3.000,
                    'active': '1',
                    'name': {
                        'language': {
                            'attrs': {'id': '1'},
                            'value': '3% tax'
                        }
                    }
                }
            }

            # Create tax record
            rec = await api.create('taxes', data)

            # Update the same tax record
            update_data = {
                'tax': {
                    'id': str(rec['id']),
                    'rate': 3.000,
                    'active': '1',
                    'name': {
                        'language': {
                            'attrs': {'id': '1'},
                            'value': '3% tax'
                        }
                    }
                }
            }

            update_rec = await api.write('taxes', update_data)

            # Remove this tax
            await api.unlink('taxes', str(rec['id']))

            # Search the first 3 taxes with '5' in the name
            import pprint
            recs = await api.search('taxes', filter='[name]=%[5]%', limit='3')

            for rec in recs:
                pprint(rec)

            # Create binary (product image)
            await api.create_binary('images/products/22', 'img.jpeg', 'image')

        if __name__ == "__main__":
            asyncio.run(main())

    """
    ...
```

**Описание**:
Асинхронный класс для взаимодействия с PrestaShop API с использованием JSON и XML.

**Атрибуты**:

*   `client` (ClientSession): Экземпляр `aiohttp.ClientSession` для выполнения асинхронных HTTP-запросов.
*   `debug` (bool): Флаг, указывающий, включен ли режим отладки.
*   `language` (Optional[int]): ID языка по умолчанию.
*   `data_format` (str): Формат данных по умолчанию (`'JSON'` или `'XML'`).
*   `ps_version` (str): Версия PrestaShop.
*   `API_DOMAIN` (str): Домен API.
*   `API_KEY` (str): Ключ API.

**Методы**:

*   `__init__(self, api_domain: str, api_key: str, data_format: str = 'JSON', debug: bool = True) -> None`: Инициализирует объект `PrestaShopAsync`.
*   `ping(self) -> bool`: Асинхронно проверяет работоспособность веб-сервиса.
*   `_check_response(self, status_code: int, response, method: Optional[str] = None, url: Optional[str] = None, headers: Optional[dict] = None, data: Optional[dict] = None) -> bool`: Асинхронно проверяет код состояния HTTP-ответа и обрабатывает ошибки.
*   `_parse_response_error(self, response, method: Optional[str] = None, url: Optional[str] = None, headers: Optional[dict] = None, data: Optional[dict] = None)`: Асинхронно разбирает ответ об ошибке от API PrestaShop.
*   `_prepare(self, url: str, params: dict) -> str`: Подготавливает URL для запроса.
*   `_exec(self, resource: str, resource_id: Optional[Union[int, str]] = None, resource_ids: Optional[Union[int, Tuple[int]]] = None, method: str = 'GET', data: Optional[dict | str] = None, headers: Optional[dict] = None, search_filter: Optional[Union[str, dict]] = None, display: Optional[Union[str, list]] = 'full', schema: Optional[str] = None, sort: Optional[str] = None, limit: Optional[str] = None, language: Optional[int] = None, io_format: str = 'JSON') -> Optional[dict]`: Асинхронно выполняет HTTP-запрос к API PrestaShop.
*   `_parse(self, text: str) -> dict | ElementTree.Element | bool`: Асинхронно разбирает XML или JSON ответ от API в структуру dict.
*   `create(self, resource: str, data: dict) -> Optional[dict]`: Асинхронно создает новый ресурс в API PrestaShop.
*   `read(self, resource: str, resource_id: Union[int, str], **kwargs) -> Optional[dict]`: Асинхронно читает ресурс из API PrestaShop.
*   `write(self, resource: str, data: dict) -> Optional[dict]`: Асинхронно обновляет существующий ресурс в API PrestaShop.
*   `unlink(self, resource: str, resource_id: Union[int, str]) -> bool`: Асинхронно удаляет ресурс из API PrestaShop.
*   `search(self, resource: str, filter: Optional[Union[str, dict]] = None, **kwargs) -> List[dict]`: Асинхронно ищет ресурсы в API PrestaShop.
*   `create_binary(self, resource: str, file_path: str, file_name: str) -> dict`: Асинхронно загружает бинарный файл в ресурс API PrestaShop.
*   `get_schema(self, resource: Optional[str] = None, resource_id: Optional[int] = None, schema: Optional[str] = 'blank', **kwards) -> dict | None`: AsRetrieve the schema of a given resource from PrestaShop API asynchronously.
*    `get_languages_schema(self) -> Optional[dict]`: Gets the schema for languages asynchronously.

## Методы класса

### `__init__`

```python
def __init__(
    self,
    api_domain: str,
    api_key: str,
    data_format: str = 'JSON',
    debug: bool = True
) -> None:
    """Initialize the PrestaShopAsync class.

    Args:
        data_format (str): Default data format ('JSON' or 'XML'). Defaults to 'JSON'.
        default_lang (int): Default language ID. Defaults to 1.
        debug (bool): Activate debug mode. Defaults to True.
    """
    ...
```

**Назначение**:
Инициализирует класс `PrestaShopAsync`.

**Параметры**:

*   `api_domain` (str): Домен API.
*   `api_key` (str): Ключ API.
*   `data_format` (str, optional): Формат данных по умолчанию (`'JSON'` или `'XML'`). По умолчанию `'JSON'`.
*   `debug` (bool, optional): Активировать режим отладки. По умолчанию `True`.

**Как работает функция**:

1.  Устанавливает значения атрибутов `API_DOMAIN`, `API_KEY`, `debug`, и `data_format`.
2.  Создает экземпляр `aiohttp.ClientSession` для выполнения асинхронных запросов с базовой аутентификацией.

### `ping`

```python
async def ping(self) -> bool:
    """! Test if the webservice is working perfectly asynchronously.

    Returns:
        bool: Result of the ping test. Returns `True` if the webservice is working, otherwise `False`.
    """
    ...
```

**Назначение**:
Асинхронно проверяет работоспособность веб-сервиса.

**Возвращает**:

*   `bool`: Результат проверки связи. Возвращает `True`, если веб-сервис работает, иначе `False`.

**Как работает функция**:

1.  Выполняет HEAD-запрос к API, используя `self.client.request`.
2.  Вызывает функцию `_check_response` для проверки статус кода ответа и обработки ошибок.
3.  Возвращает результат проверки.

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

**Назначение**:
Асинхронно проверяет код состояния HTTP-ответа и обрабатывает ошибки.

**Параметры**:

*   `status_code` (int): HTTP-код состояния ответа.
*   `response` (aiohttp.ClientResponse): Объект HTTP-ответа от сервера.
*   `method` (str, optional): HTTP метод, использованный в запросе.
*   `url` (str, optional): URL запроса.
*   `headers` (dict, optional): Заголовки запроса.
*   `data` (dict, optional): Данные, отправленные в запросе.

**Возвращает**:

*   `bool`: `True`, если код состояния 200 или 201, иначе `False`.

**Как работает функция**:

1.  Проверяет код состояния HTTP-ответа. Если код равен 200 или 201, возвращает `True`.
2.  В противном случае вызывает функцию `_parse_response_error` для обработки ошибки и возвращает `False`.

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

**Назначение**:
Асинхронно разбирает ответ об ошибке от API PrestaShop.

**Параметры**:

*   `response` (aiohttp.ClientResponse): Объект HTTP-ответа от сервера.
*   `method` (str, optional): HTTP метод, использованный в запросе.
*   `url` (str, optional): URL запроса.
*   `headers` (dict, optional): Заголовки запроса.
*   `data` (dict, optional): Данные, отправленные в запросе.

**Как работает функция**:

1.  В зависимости от формата данных (`self.data_format`):

    *   Если формат JSON, пытается преобразовать текст ответа в JSON и извлечь информацию об ошибке из структуры JSON.
    *   Если формат XML, пытается распарсить XML-ответ и извлечь код и сообщение об ошибке.
2.  Логирует информацию об ошибке с использованием модуля `src.logger.logger`.

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

**Назначение**:
Подготавливает URL для запроса, добавляя параметры.

**Параметры**:

*   `url` (str): Базовый URL.
*   `params` (dict): Параметры для запроса.

**Возвращает**:

*   `str`: Подготовленный URL с параметрами.

**Как работает функция**:

1.  Создает объект `PreparedRequest` из библиотеки `requests`.
2.  Добавляет параметры к базовому URL.
3.  Возвращает полный URL с параметрами.

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

**Назначение**:
Асинхронно выполняет HTTP-запрос к API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'products'`, `'categories'`).
*   `resource_id` (int | str, optional): ID ресурса. По умолчанию `None`.
*   `resource_ids` (int | Tuple[int], optional): IDs ресурсов. По умолчанию `None`.
*   `method` (str, optional): HTTP-метод (`'GET'`, `'POST'`, `'PUT'`, `'DELETE'`). По умолчанию `'GET'`.
*   `data` (dict | str, optional): Данные для отправки в запросе. По умолчанию `None`.
*   `headers` (dict, optional): Заголовки запроса. По умолчанию `None`.
*   `search_filter` (str | dict, optional): Фильтр для поиска. По умолчанию `None`.
*   `display` (str | list, optional): Параметр `display` для запроса. По умолчанию `'full'`.
*   `schema` (str, optional): Схема для запроса. По умолчанию `None`.
*   `sort` (str, optional): Параметр сортировки для запроса. По умолчанию `None`.
*   `limit` (str, optional): Ограничение количества результатов в запросе. По умолчанию `None`.
*   `language` (int, optional): ID языка для запроса. По умолчанию `None`.
*   `io_format` (str, optional): Формат ввода-вывода данных (`'JSON'` или `'XML'`). По умолчанию `'JSON'`.

**Возвращает**:

*   `Optional[dict]`: Ответ от API или `False` в случае ошибки.

**Как работает функция**:

1.  Подготавливает URL для запроса, используя функцию `_prepare`.
2.  Формирует заголовки запроса в зависимости от формата данных (`data_format`).
3.  Выполняет асинхронный HTTP-запрос с использованием библиотеки `aiohttp`.
4.  Проверяет статус ответа с помощью функции `_check_response`.
5.  Разбирает ответ с помощью функции `_parse`.
6.  Логирует ошибки, если запрос не удался.

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

**Назначение**:
Асинхронно разбирает XML или JSON ответ от API в структуру dict.

**Параметры**:

*   `text` (str): Текст ответа.

**Возвращает**:

*   `dict | ElementTree.Element | bool`: Разобранные данные или `False` в случае ошибки.

**Как работает функция**:

1.  В зависимости от формата данных (`self.data_format`):

    *   Если формат JSON, пытается преобразовать текст ответа в JSON с помощью `j_loads`.
    *   Если формат XML, пытается распарсить текст ответа как XML с помощью `ElementTree.fromstring`.
2.  Обрабатывает исключения, если разбор не удался.

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

**Назначение**:
Асинхронно создает новый ресурс в API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'products'`).
*   `data` (dict): Данные для нового ресурса.

**Возвращает**:

*   `dict`: Ответ от API.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса, метода `POST` и данных для создания ресурса.

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

**Назначение**:
Асинхронно читает ресурс из API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'products'`).
*   `resource_id` (int | str): ID ресурса.

**Возвращает**:

*   `dict`: Ответ от API.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса, ID ресурса и метода `GET`.

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

**Назначение**:
Асинхронно обновляет существующий ресурс в API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'products'`).
*   `data` (dict): Данные для ресурса.

**Возвращает**:

*   `dict`: Ответ от API.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса, ID ресурса (полученного из данных) и метода `PUT`.

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

**Назначение**:
Асинхронно удаляет ресурс из API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'products'`).
*   `resource_id` (int | str): ID ресурса.

**Возвращает**:

*   `bool`: `True`, если удаление прошло успешно, `False` в противном случае.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса, ID ресурса и метода `DELETE`.

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

**Назначение**:
Асинхронно ищет ресурсы в API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'products'`).
*   `filter` (str | dict, optional): Фильтр для поиска.

**Возвращает**:

*   `List[dict]`: Список ресурсов, соответствующих критериям поиска.

**Как работает функция**:

1.  Вызывает функцию `_exec` с указанием ресурса, фильтра и метода `GET`.

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

**Назначение**:
Асинхронно загружает бинарный файл в ресурс API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'images/products/22'`).
*   `file_path` (str): Путь к бинарному файлу.
*   `file_name` (str): Имя файла.

**Возвращает**:

*   `dict`: Ответ от API.

**Как работает функция**:

1.  Открывает файл в бинарном режиме для чтения.
2.  Формирует заголовки запроса, указывая `Content-Type` как `application/octet-stream`.
3.  Выполняет POST-запрос к API, используя библиотеку `aiohttp`.
4.  Возвращает ответ в формате JSON.

### `get_schema`

*Данная функция отсутствует в коде*
### `get_languages_schema`

*Данная функция отсутствует в коде*

## Переменные

*   `client`: HTTP клиент для выполнения запросов.
*   `debug`: Флаг, для дебага.
*   `data_format`: Показывает формат данных для отправки `JSON` или `XML`

## Примеры использования

*Примеры отсутствуют*

## Зависимости

*   `typing.List, typing.Dict, typing.Optional, typing.Union`: Для аннотаций типов.
*   `src.logger.logger`: Для логирования.
*   `src.utils.jjson.j_loads, src.utils.jjson.j_dumps`: Для загрузки и сохранения JSON-данных.
*   `src.endpoints.prestashop.api.PrestaShop`: Для взаимодействия с API PrestaShop.
* `pathlib.Path` и `os` для работы с файловой системой
*   `aiohttp`: Для асинхронных HTTP-запросов.
*   `xml.etree.ElementTree`: Для обработки XML данных.
* `from src.endpoints.prestashop.utils import dict2xml, xml2dict`: Преобразование данных в XML

## Взаимосвязи с другими частями проекта

*   Модуль `api_async.py` предоставляет асинхронный интерфейс для взаимодействия с API PrestaShop и используется в других частях проекта `hypotez`, где требуется асинхронное выполнение запросов к PrestaShop.
*   Использует модуль `src.logger.logger` для логирования.
*   Использует `src.utils.jjson` для загрузки и сохранения данных в формате JSON.
*   Для выполнения преобразований используются `from src.endpoints.prestashop.utils import dict2xml, xml2dict`
*   Для создания асинхронных запросов используется `import aiohttp`