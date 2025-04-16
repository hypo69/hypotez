# Модуль `xml_json_convertor`

## Обзор

Модуль `xml_json_convertor` предоставляет утилиты для конвертации данных между форматами XML и JSON. Он включает функции для преобразования JSON-словарей в XML-строки и наоборот, а также содержит класс `Config` для хранения конфигурационных параметров.

## Подробней

Модуль предоставляет удобный интерфейс для работы с API PrestaShop, которые могут использовать разные форматы данных (XML и JSON). Он позволяет легко конвертировать данные из одного формата в другой, а также настраивать параметры подключения к API.

## Классы

### `Config`

**Описание**: Класс конфигурации для PrestaShop API.

**Атрибуты**:

-   `language` (str): Язык.
-   `ps_version` (str): Версия PrestaShop (по умолчанию `''`).
-   `MODE` (str): Режим работы (`'dev'`, `'dev8'`, `'prod'`). Определяет конечную точку API.
-   `POST_FORMAT` (str): Формат данных (`'JSON'` или `'XML'`).
-   `API_DOMAIN` (str): Домен API PrestaShop.
-   `API_KEY` (str): Ключ API PrestaShop.

**Принцип работы**:

Класс `Config` предназначен для хранения и предоставления доступа к настройкам, необходимым для взаимодействия с API PrestaShop. Он определяет значения `API_DOMAIN` и `API_KEY` в зависимости от режима работы, использования переменных окружения и значений, хранящихся в `gs.credentials`.

### `PrestaShop`

**Описание**: Класс для взаимодействия с PrestaShop webservice API, использующий JSON и XML для обмена сообщениями.

**Атрибуты**:

*   `client` (Session): HTTP клиент для выполнения запросов.
*   `debug` (bool): Флаг отладки.
*   `language` (Optional[int]): ID языка по умолчанию.
*   `data_format` (str): Формат данных (JSON или XML).
*   `ps_version` (str): Версия PrestaShop.
*   `api_domain` (str): Домен API PrestaShop.
*   `api_key` (str): Ключ API PrestaShop.

**Методы**:

*   `__init__`: Инициализирует объект `PrestaShop`.
*   `ping`: Проверяет работоспособность API.
*   `_check_response`: Проверяет статус ответа и обрабатывает ошибки.
*   `_parse_response_error`: Разбирает сообщение об ошибке из ответа API.
*   `_prepare_url`: Подготавливает URL для запроса.
*   `_exec`: Выполняет HTTP запрос к API PrestaShop.
*   `_parse_response`: Разбирает XML или JSON ответ от API в структуру dict.
*   `create`: Создает новый ресурс в PrestaShop API.
*   `read`: Читает ресурс из PrestaShop API.
*   `write`: Обновляет существующий ресурс в PrestaShop API.
*   `unlink`: Удаляет ресурс из PrestaShop API.
*   `search`: Выполняет поиск ресурсов в PrestaShop API.
*   `create_binary`: Загружает бинарный файл в ресурс API PrestaShop.
*   `get_schema`: Извлекает схему заданного ресурса из API PrestaShop.
*   `get_data`: Извлекает данные из ресурса API PrestaShop и сохраняет их.
*   `get_apis`: Получает список всех доступных API.
*   `upload_image_async`: Асинхронно загружает изображение в PrestaShop API.
*   `upload_image_from_url`: Загружает изображение в PrestaShop API.
*   `get_product_images`: Получает изображения для товара.

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
    """Initialize the PrestaShop class.

    Args:
        data_format (str): Default data format ('JSON' or 'XML'). Defaults to 'JSON'.
        default_lang (int): Default language ID. Defaults to 1.
        debug (bool): Activate debug mode. Defaults to True.
    """
    ...
```

**Назначение**: Инициализирует объект `PrestaShop`.

**Параметры**:

*   `api_key` (str): Ключ API PrestaShop.
*   `api_domain` (str): Домен API PrestaShop.
*   `data_format` (str): Формат данных (JSON или XML). По умолчанию `'JSON'`.
*   `default_lang` (int): ID языка по умолчанию. По умолчанию `1`.
*   `debug` (bool): Флаг отладки. По умолчанию `False`.

**Как работает функция**:

1.  Устанавливает значения атрибутов `api_domain`, `api_key`, `debug`, `language` и `data_format`.
2.  Устанавливает аутентификацию для HTTP клиента.
3.  Выполняет HEAD запрос к API для проверки соединения и получения версии PrestaShop.

### `ping`

```python
def ping(self) -> bool:
    """Test if the webservice is working perfectly.

    Returns:
        bool: Result of the ping test. Returns `True` if the webservice is working, otherwise `False`.
    """
    ...
```

**Назначение**: Проверяет работоспособность API PrestaShop.

**Возвращает**:

*   `bool`: `True`, если API работает, иначе `False`.

**Как работает функция**:

1.  Выполняет HEAD запрос к API.
2.  Проверяет статус ответа с помощью метода `_check_response`.

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
    ...
```

**Назначение**: Проверяет статус ответа и обрабатывает ошибки.

**Параметры**:

*   `status_code` (int): HTTP статус код ответа.
*   `response` (requests.Response): Объект HTTP ответа.
*   `method` (Optional[str]): HTTP метод, использованный для запроса.
*   `url` (Optional[str]): URL запроса.
*   `headers` (Optional[dict]): Заголовки, использованные в запросе.
*   `data` (Optional[dict]): Данные, отправленные в запросе.

**Возвращает**:

*   `bool`: `True`, если статус код 200 или 201, иначе `False`.

**Как работает функция**:

1.  Проверяет, является ли статус код 200 или 201.
2.  Если статус код не является 200 или 201, вызывает метод `_parse_response_error` для обработки ошибки.

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
    ...
```

**Назначение**: Разбирает сообщение об ошибке из ответа API PrestaShop.

**Параметры**:

*   `response` (requests.Response): Объект HTTP ответа от сервера.

**Как работает функция**:

1.  Проверяет формат ответа (JSON или XML).
2.  В зависимости от формата разбирает ответ и извлекает код и сообщение об ошибке.
3.  Логирует сообщение об ошибке.

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

**Назначение**: Выполняет HTTP запрос к API PrestaShop.

**Параметры**:

*   `resource` (str): Ресурс API (например, `'products'`).
*   `resource_id` (Optional[int | str]): ID ресурса.
*   `resource_ids` (Optional[int | Tuple[int]]): ID ресурсов.
*   `method` (str): HTTP метод (`'GET'`, `'POST'`, `'PUT'`, `'DELETE'`).
*   `data` (Optional[dict | str]): Данные для отправки в запросе.
*   `headers` (Optional[dict]): Заголовки запроса.
*   `search_filter` (Optional[str | dict]): Фильтр для поиска.
*   `display` (Optional[str | list]): Что отображать в ответе.
*   `schema` (Optional[str]): Схема ресурса.
*   `sort` (Optional[str]): Поле для сортировки.
*   `limit` (Optional[str]): Лимит количества возвращаемых записей.
*   `language` (Optional[int]): ID языка.
*   `data_format` (str): Формат данных (`'JSON'` или `'XML'`).
*   `**kwards`: Дополнительные параметры.

**Возвращает**:

*   `Optional[dict]`: Разобранные данные из ответа API или `None` в случае ошибки.

**Как работает функция**:

1.  Подготавливает URL для запроса с помощью метода `_prepare_url`.
2.  Устанавливает заголовки запроса в зависимости от формата данных.
3.  Выполняет HTTP запрос с использованием библиотеки `requests`.
4.  Проверяет статус ответа с помощью метода `_check_response`.
5.  Разбирает ответ с помощью метода `_parse_response`.

### `_parse_response`

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

**Назначение**: Разбирает XML или JSON ответ от API в структуру dict.

**Параметры**:

*   `text` (str): Response text.

**Возвращает**:

*   `dict`: Разобранные данные или `False` в случае неудачи.

**Как работает функция**:

1.  Извлекает данные из ответа в формате JSON, если `self.data_format == 'JSON'`, иначе вызывает функцию `xml2dict` для преобразования XML в dict.
2.  В случае ошибки логирует ошибку и возвращает `{}`.

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
    ...
```

**Назначение**: Создает новый ресурс в PrestaShop API.

**Параметры**:

*   `resource` (str): Ресурс API (например, `'products'`).
*   `data` (dict): Данные для нового ресурса.
*   `*args`: Произвольные позиционные аргументы, передаваемые в функцию `_exec`.
*   `**kwards`: Произвольные именованные аргументы, передаваемые в функцию `_exec`.

**Возвращает**:

*   `Optional[dict]`: Ответ от API.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `method='POST'` и `data`.

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
    ...
```

**Назначение**: Читает ресурс из API PrestaShop.

**Параметры**:

*   `resource` (str): Ресурс API (например, `'products'`).
*   `resource_id` (int | str): ID ресурса.
*   `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:

*   `Optional[dict]`: Ответ от API.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `resource_id` и `method='GET'`.

### `write`

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

**Назначение**: Обновляет существующий ресурс в API PrestaShop.

**Параметры**:

*   `resource` (str): Ресурс API (например, `'products'`).
*   `resource_id` (int | str): ID ресурса.
*   `data` (dict): Данные для обновления ресурса.
*   `**kwards`: Дополнительные параметры для запроса.

**Возвращает**:

*   `Optional[dict]`: Ответ от API.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `resource_id`, `method='PUT'` и `data`.

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
    ...
```

**Назначение**: Удаляет ресурс из API PrestaShop.

**Параметры**:

*   `resource` (str): Ресурс API (например, `'products'`).
*   `resource_id` (int | str): ID ресурса.

**Возвращает**:

*   `bool`: `True`, если удаление успешно, иначе `False`.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `resource_id` и `method='DELETE'`.

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
    ...
```

**Назначение**: Поиск ресурсов в API PrestaShop.

**Параметры**:

*   `resource` (str): Ресурс API (например, `'products'`).
*   `filter` (Optional[str | dict]): Фильтр для поиска.
*   `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:

*   `List[dict]`: Список ресурсов, соответствующих критериям поиска.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `search_filter=filter` и `method='GET'`.

### `create_binary`

```python
def create_binary(self, resource: str, file_path: str, file_name: str) -> dict:
    """Upload a binary file to a PrestaShop API resource."""
    ...
```

**Назначение**: Загружает бинарный файл в ресурс API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'images/products/22'`).
*   `file_path` (str): Путь к файлу.
*   `file_name` (str): Имя файла.

**Возвращает**:

*   `dict`: Ответ от API.

**Как работает функция**:

1.  Открывает файл в бинарном режиме.
2.  Формирует словарь `files` для передачи в запросе.
3.  Выполняет POST запрос к API.
4.  Обрабатывает возможные исключения, связанные с запросом и файловой системой.

### `get_schema`

```python
def get_schema(
    self, resource: Optional[str] = None, resource_id: Optional[int] = None, schema: Optional[str] = 'blank', **kwards
) -> dict | None:
    """Retrieve the schema of a given resource from PrestaShop API.

    Args:
        resource (str): The name of the resource (e.g., 'products', 'customers').
            Если не указана - вернется список всех схем сущностей доступных для API ключа
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

**Назначение**: Извлекает схему заданного ресурса из API PrestaShop.

**Параметры**:

*   `resource` (Optional[str]): Имя ресурса (например, `'products'`, `'customers'`). Если не указано, возвращается список всех схем сущностей, доступных для ключа API.
*   `resource_id` (Optional[str]): ID ресурса.
*   `schema` (Optional[str]): Тип схемы (`'blank'`, `'synopsis'`, `'full'`).
*   `**kwards`: Дополнительные аргументы.

**Возвращает**:

*   `dict | None`: Схема запрошенного ресурса или `None` в случае ошибки.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `resource`, `resource_id`, `schema` и `method="GET"`.

### `get_data`

```python
def get_data(self, resource: str, **kwargs) -> Optional[dict]:
    """Fetch data from a PrestaShop API resource and save it.

    Args:
        resource (str): API resource (e.g., 'products').
        **kwargs: Additional arguments for the API request.

    Returns:
        dict | None: Data from the API or `False` on failure.
    """
    ...
```

**Назначение**: Извлекает данные из ресурса API PrestaShop и сохраняет их.

**Параметры**:

*   `resource` (str): API ресурс (например, `'products'`).
*   `**kwargs`: Дополнительные аргументы для запроса API.

**Возвращает**:

*   `dict | None`: Данные из API или `False` в случае неудачи.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметром `resource` и `method='GET'`.

### `get_apis`

```python
def get_apis(self) -> Optional[dict]:
    """Get a list of all available APIs.

    Returns:
        dict: List of available APIs.
    """
    ...
```

**Назначение**: Получает список всех доступных API.

**Возвращает**:

*   `dict`: Список доступных API.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `'apis'` и `method='GET'`.

### `upload_image_async`

```python
def upload_image_async(
    self, resource: str, resource_id: int, img_url: str, img_name: Optional[str] = None
) -> Optional[dict]:
    """Upload an image to PrestaShop API asynchronously.

    Args:
        resource (str): API resource (e.g., 'images/products/22').
        resource_id (int): Resource ID.
        img_url (str): URL of the image.
        img_name (Optional[str]): Name of the image file, defaults to None.

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
*   `img_name` (Optional[str]): Имя файла изображения, по умолчанию `None`.

**Возвращает**:

*   `dict | None`: Ответ от API или `False` в случае ошибки.

**Как работает функция**:

1.  Разделяет URL изображения на имя файла и расширение.
2.  Формирует имя файла для сохранения.
3.  Сохраняет изображение из URL во временный файл.
4.  Вызывает метод `create_binary` для загрузки изображения в API.
5.  Удаляет временный файл.

### `upload_image_from_url`

```python
def upload_image_from_url(
    self, resource: str, resource_id: int, img_url: str, img_name: Optional[str] = None
) -> Optional[dict]:
    """Upload an image to PrestaShop API.

    Args:
        resource (str): API resource (e.g., 'images/products/22').
        resource_id (int): Resource ID.
        img_url (str): URL of the image.
        img_name (Optional[str]): Name of the image file, defaults to None.

    Returns:
        dict | None: Response from the API or `False` on failure.
    """
    ...
```

**Назначение**: Загружает изображение в API PrestaShop.

**Параметры**:

*   `resource` (str): API ресурс (например, `'images/products/22'`).
*   `resource_id` (int): ID ресурса.
*   `img_url` (str): URL изображения.
*   `img_name` (Optional[str]): Имя файла изображения, по умолчанию `None`.

**Возвращает**:

*   `dict | None`: Ответ от API или `False` в случае ошибки.

**Как работает функция**:

1.  Разделяет URL изображения на имя файла и расширение.
2.  Формирует имя файла для сохранения.
3.  Сохраняет изображение из URL во временный файл.
4.  Вызывает метод `create_binary` для загрузки изображения в API.
5.  Удаляет временный файл.

### `get_product_images`

```python
def get_product_images(self, product_id: int) -> Optional[dict]:
    """Get images for a product.

    Args:
        product_id (int): Product ID.

    Returns:
        dict | None: List of product images or `False` on failure.
    """
    ...
```

**Назначение**: Получает изображения для товара.

**Параметры**:

*   `product_id` (int): ID товара.

**Возвращает**:

*   `dict | None`: Список изображений товара или `False` в случае неудачи.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами `f'products/{product_id}/images'` и `method='GET'`.

## Функции

### `main`

```python
def main() -> None:
    """Проверка сущностей Prestashop"""
    data: dict = {
        'tax': {
            'rate': 3.000,
            'active': '1',
            'name': {
                'language': {
                    'attrs': {'id': '1'},
                    'value': '3% tax',
                }
            },
        }
    }
    api: PrestaShop = PrestaShop(
        api_domain = Config.API_DOMAIN,
        api_key = Config.API_KEY,
        default_lang = 1,
        debug = True,
        data_format = Config.POST_FORMAT,
    )
    api.create('taxes', data)
    api.write('taxes', data)
```

**Назначение**: Проверяет сущности PrestaShop.

**Как работает функция**:

1.  Формирует словарь `data` с информацией о налоге.
2.  Создает экземпляр класса `PrestaShop`.
3.  Вызывает методы `create` и `write` для создания и обновления информации о налоге через API PrestaShop.

## Дополнительные замечания

Предоставленный код является примером реализации взаимодействия с PrestaShop API и может потребовать доработки в зависимости от конкретных задач и требований. Важно обращать внимание на обработку ошибок и исключений, а также на правильную настройку параметров подключения к API.