# Модуль для взаимодействия с PrestaShop API

## Обзор

Модуль предоставляет класс `PrestaShop` для взаимодействия с PrestaShop webservice API, используя JSON и XML для форматирования сообщений. Он поддерживает CRUD операции, поиск и загрузку изображений, с обработкой ошибок для ответов.

## Подробнее

Этот модуль предназначен для упрощения взаимодействия с API PrestaShop, предоставляя удобные методы для выполнения различных операций, таких как создание, чтение, обновление и удаление данных, а также для поиска и загрузки изображений. Он использует библиотеки `requests` для выполнения HTTP-запросов и поддерживает форматы данных JSON и XML. Модуль также включает обработку ошибок для обеспечения надежности и информативности при возникновении проблем.

## Содержание

- [Классы](#классы)
    - [Config](#config)
    - [PrestaShop](#prestashop)
- [Функции](#функции)
    - [main](#main)

## Классы

### `Config`

**Описание**: Класс конфигурации для API PrestaShop.

**Атрибуты**:

- `language` (str): Язык.
- `ps_version` (str): Версия PrestaShop (по умолчанию: '').
- `MODE` (str): Определяет конечную точку API (по умолчанию: 'dev'). Возможные значения: `dev`, `dev8`, `prod`.
- `POST_FORMAT` (str): Формат данных для POST-запросов (по умолчанию: 'JSON').
- `API_DOMAIN` (str): Домен API.
- `API_KEY` (str): Ключ API.

**Принцип работы**:

Класс `Config` используется для хранения и управления конфигурационными параметрами, необходимыми для взаимодействия с API PrestaShop. Он автоматически загружает значения из переменных окружения, если `USE_ENV` установлен в `True`. В противном случае используются значения, определенные в соответствии с параметром `MODE`.

### `PrestaShop`

**Описание**: Класс для взаимодействия с PrestaShop webservice API, использующий JSON и XML для обмена сообщениями.

**Атрибуты**:

- `client` (Session): HTTP-клиент для выполнения запросов.
- `debug` (bool): Флаг отладки. Если `True`, включает режим отладки HTTP-соединения.
- `language` (Optional[int]): ID языка по умолчанию.
- `data_format` (str): Формат данных по умолчанию ('JSON' или 'XML').
- `ps_version` (str): Версия PrestaShop.
- `api_domain` (str): Домен API PrestaShop.
- `api_key` (str): Ключ API PrestaShop.

**Методы**:

- [`__init__`](#init)
- [`ping`](#ping)
- [`_check_response`](#check_response)
- [`_parse_response_error`](#parse_response_error)
- [`_prepare_url`](#prepare_url)
- [`_exec`](#exec)
- [`_parse_response`](#parse_response)
- [`create`](#create)
- [`read`](#read)
- [`write`](#write)
- [`unlink`](#unlink)
- [`search`](#search)
- [`create_binary`](#create_binary)
- [`get_schema`](#get_schema)
- [`get_data`](#get_data)
- [`get_apis`](#get_apis)
- [`upload_image_async`](#upload_image_async)
- [`upload_image_from_url`](#upload_image_from_url)
- [`get_product_images`](#get_product_images)

#### `__init__`

```python
def __init__(
    self,
    api_key: str,
    api_domain: str,
    data_format: str = Config.POST_FORMAT,
    default_lang: int = 1,
    debug: bool = False,
) -> None:
    """Инициализация класса PrestaShop.

    Args:
        api_key (str): Ключ API, сгенерированный в PrestaShop.
        api_domain (str): Домен магазина PrestaShop (например, https://myPrestaShop.com).
        data_format (str): Формат данных по умолчанию ('JSON' или 'XML'). По умолчанию 'JSON'.
        default_lang (int): ID языка по умолчанию. По умолчанию 1.
        debug (bool): Активировать режим отладки. По умолчанию False.

    Raises:
        PrestaShopAuthenticationError: Если ключ API неверен или не существует.
        PrestaShopException: Для общих ошибок веб-сервисов PrestaShop.
    """
```

**Назначение**: Инициализирует экземпляр класса `PrestaShop` с заданными параметрами подключения к API PrestaShop.

**Параметры**:

- `api_key` (str): Ключ API PrestaShop.
- `api_domain` (str): Домен API PrestaShop.
- `data_format` (str, optional): Формат данных ('JSON' или 'XML'). По умолчанию 'JSON'.
- `default_lang` (int, optional): ID языка по умолчанию. По умолчанию 1.
- `debug` (bool, optional): Включает режим отладки. По умолчанию `False`.

**Как работает функция**:

1.  Инициализирует атрибуты экземпляра класса `PrestaShop` с переданными значениями.
2.  Устанавливает аутентификацию для HTTP-клиента, используя предоставленный ключ API.
3.  Выполняет HEAD-запрос к API для проверки соединения и получения версии PrestaShop.
4.  Логирует ошибку и прерывает выполнение, если не удается установить соединение.
5.  Сохраняет версию PrestaShop, полученную из заголовков ответа.

#### `ping`

```python
def ping(self) -> bool:
    """Проверяет, работает ли веб-сервис.

    Returns:
        bool: Результат проверки связи. Возвращает `True`, если веб-сервис работает, иначе `False`.
    """
```

**Назначение**: Проверяет доступность API PrestaShop, выполняя HEAD-запрос к домену API.

**Возвращает**:

- `bool`: `True`, если API доступен, `False` в противном случае.

**Как работает функция**:

1.  Выполняет HEAD-запрос к домену API.
2.  Вызывает метод `_check_response` для проверки статуса ответа.
3.  Возвращает результат проверки.

#### `_check_response`

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
        method (Optional[str]): HTTP-метод, использованный для запроса.
        url (Optional[str]): URL запроса.
        headers (Optional[dict]): Заголовки, использованные в запросе.
        data (Optional[dict]): Данные, отправленные в запросе.

    Returns:
        bool: `True`, если код состояния 200 или 201, иначе `False`.
    """
```

**Назначение**: Проверяет статус код HTTP-ответа и обрабатывает ошибки, если таковые имеются.

**Параметры**:

- `status_code` (int): HTTP код ответа.
- `response` (requests.Response): Объект HTTP-ответа.
- `method` (Optional[str]): HTTP-метод запроса (например, 'GET', 'POST').
- `url` (Optional[str]): URL, на который был отправлен запрос.
- `headers` (Optional[dict]): Заголовки запроса.
- `data` (Optional[dict]): Тело запроса (данные).

**Возвращает**:

- `bool`: `True`, если `status_code` равен 200 или 201, иначе `False`.

**Как работает функция**:

1.  Проверяет, входит ли `status_code` в список успешных (200, 201).
2.  Если код не успешный, вызывает `_parse_response_error` для обработки ошибки.
3.  Возвращает `True` или `False` в зависимости от успешности статуса.

#### `_parse_response_error`

```python
def _parse_response_error(
    self,
    response: requests.Response,
    method: Optional[str] = None,
    url: Optional[str] = None,
    headers: Optional[dict] = None,
    data: Optional[dict] = None,
) -> None:
    """Разбирает ответ об ошибке от API PrestaShop.

    Args:
        response (requests.Response): Объект HTTP-ответа от сервера.
    """
```

**Назначение**: Обрабатывает и логирует ошибки, полученные от API PrestaShop.

**Параметры**:

- `response` (requests.Response): Объект HTTP-ответа, содержащий информацию об ошибке.
- `method` (Optional[str]): HTTP-метод запроса (например, 'GET', 'POST').
- `url` (Optional[str]): URL, на который был отправлен запрос.
- `headers` (Optional[dict]): Заголовки запроса.
- `data` (Optional[dict]): Тело запроса (данные).

**Как работает функция**:

1.  В зависимости от формата данных (`Config.POST_FORMAT`):
    *   Если формат `JSON`, извлекает код состояния и JSON-содержимое ответа, логирует их как ошибку.
    *   Если формат `XML`, разбирает XML-ответ и извлекает код и сообщение об ошибке, затем логирует их.
2.  Использует `logger.error` для записи информации об ошибке.

#### `_prepare_url`

```python
def _prepare_url(self, url: str, params: dict) -> str:
    """Подготавливает URL для запроса.

    Args:
        url (str): Базовый URL.
        params (dict): Параметры для запроса.

    Returns:
        str: Подготовленный URL с параметрами.
    """
```

**Назначение**: Формирует URL с параметрами для выполнения запроса к API PrestaShop.

**Параметры**:

- `url` (str): Базовый URL API.
- `params` (dict): Словарь параметров запроса.

**Возвращает**:

- `str`: URL с добавленными параметрами.

**Как работает функция**:

1.  Использует `PreparedRequest` из библиотеки `requests` для подготовки URL.
2.  Добавляет параметры к базовому URL.
3.  Возвращает полный URL.

#### `_exec`

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
    """Выполняет HTTP-запрос к API PrestaShop."""
```

**Назначение**: Выполняет HTTP-запрос к API PrestaShop.

**Параметры**:

- `resource` (str): Ресурс API (например, 'products').
- `resource_id` (Optional[int  |  str]): ID ресурса.
- `resource_ids` (Optional[int  |  Tuple[int]]): ID ресурсов.
- `method` (str): HTTP-метод ('GET', 'POST', 'PUT', 'DELETE'). По умолчанию 'GET'.
- `data` (Optional[dict  |  str]): Данные для отправки.
- `headers` (Optional[dict]): Дополнительные заголовки.
- `search_filter` (Optional[str  |  dict]): Фильтр для поиска.
- `display` (Optional[str  |  list]): Что отображать. По умолчанию 'full'.
- `schema` (Optional[str]): Схема.
- `sort` (Optional[str]): Сортировка.
- `limit` (Optional[str]): Лимит.
- `language` (Optional[int]): Язык.
- `data_format` (str): Формат данных ('JSON' или 'XML'). По умолчанию 'JSON'.
- `**kwards`: Дополнительные параметры.

**Возвращает**:

- `Optional[dict]`: Ответ от API или `False` в случае ошибки.

**Как работает функция**:

1.  Устанавливает уровень отладки HTTP-соединения.
2.  Формирует URL запроса на основе переданных параметров.
3.  Определяет заголовки запроса в зависимости от формата данных (`data_format`).
4.  Выполняет HTTP-запрос с использованием библиотеки `requests`.
5.  Проверяет статус ответа с помощью `self._check_response`.
6.  В случае ошибки логирует информацию и возвращает `False`.
7.  Разбирает ответ с помощью `self._parse_response` и возвращает результат.
8.  Обрабатывает исключения и логирует ошибки.

#### `_parse_response`

```python
def _parse_response(self, response: Response) -> dict | None:
    """Разбирает XML или JSON ответ от API в структуру dict

    Args:
        text (str): Текст ответа.

    Returns:
        dict: Разобранные данные или `False` при неудаче.
    """
```

**Назначение**: Разбирает ответ от API PrestaShop в формате JSON или XML и преобразует его в структуру `dict`.

**Параметры**:

- `response` (Response): Объект ответа HTTP-запроса.

**Возвращает**:

- `dict  |  None`: Разобранные данные в виде словаря или `None` в случае ошибки.

**Как работает функция**:

1.  Пытается разобрать JSON-ответ с помощью `response.json()`.
2.  Если разбор успешен, возвращает словарь, полученный из JSON.
3.  Если происходит ошибка при разборе JSON, логирует ошибку и возвращает пустой словарь.

#### `create`

```python
def create(self, resource: str, data: dict, *args, **kwards) -> Optional[dict]:
    """Создает новый ресурс в API PrestaShop.

    Args:
        resource (str): API ресурс (например, 'products').
        data (dict): Данные для нового ресурса.

    Returns:
        dict: Ответ от API.
    """
```

**Назначение**: Создает новый ресурс в API PrestaShop.

**Параметры**:

-   `resource` (str): Тип ресурса, который нужно создать (например, `'products'`, `'categories'`).
-   `data` (dict): Данные ресурса для создания.

**Возвращает**:

-   `Optional[dict]`: Ответ от API в случае успеха или `None` в случае ошибки.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами:
    *   `resource`: Тип ресурса.
    *   `method`: `'POST'` (метод создания).
    *   `data`: Данные для создания ресурса.
2.  Возвращает результат выполнения метода `_exec`.

#### `read`

```python
def read(self, resource: str, resource_id: int | str, **kwargs) -> Optional[dict]:
    """Считывает ресурс из API PrestaShop.

    Args:
        resource (str): API ресурс (например, 'products').
        resource_id (int | str): ID ресурса.

    Returns:
        dict: Ответ от API.
    """
```

**Назначение**: Получает информацию о конкретном ресурсе из API PrestaShop.

**Параметры**:

-   `resource` (str): Тип ресурса, который нужно получить (например, `'products'`, `'categories'`).
-   `resource_id` (int | str): ID ресурса, который нужно получить.
-   `**kwargs`: Дополнительные параметры запроса.

**Возвращает**:

-   `Optional[dict]`: Ответ от API в случае успеха или `None` в случае ошибки.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами:
    *   `resource`: Тип ресурса.
    *   `resource_id`: ID ресурса.
    *   `method`: `'GET'` (метод чтения).
    *   `**kwargs`: Дополнительные параметры запроса.
2.  Возвращает результат выполнения метода `_exec`.

#### `write`

```python
def write(self, resource: str, resource_id:int|str, data: dict, **kwards) -> Optional[dict]:
    """Обновляет существующий ресурс в API PrestaShop.

    Args:
        resource (str): API ресурс (например, 'products').
        data (dict): Данные для ресурса.

    Returns:
        dict: Ответ от API.
    """
```

**Назначение**: Обновляет существующий ресурс в API PrestaShop.

**Параметры**:

-   `resource` (str): Тип ресурса, который нужно обновить (например, `'products'`, `'categories'`).
-   `resource_id` (int | str): ID ресурса, который нужно обновить.
-   `data` (dict): Данные для обновления ресурса.
-   `**kwargs`: Дополнительные параметры запроса.

**Возвращает**:

-   `Optional[dict]`: Ответ от API в случае успеха или `None` в случае ошибки.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами:
    *   `resource`: Тип ресурса.
    *   `resource_id`: ID ресурса.
    *   `method`: `'PUT'` (метод обновления).
    *   `data`: Данные для обновления ресурса.
    *   `**kwargs`: Дополнительные параметры запроса.
2.  Возвращает результат выполнения метода `_exec`.

#### `unlink`

```python
def unlink(self, resource: str, resource_id: int | str) -> bool:
    """Удаляет ресурс из API PrestaShop.

    Args:
        resource (str): API ресурс (например, 'products').
        resource_id (int | str): ID ресурса.

    Returns:
        bool: `True`, если успешно, `False` иначе.
    """
```

**Назначение**: Удаляет ресурс из API PrestaShop.

**Параметры**:

-   `resource` (str): Тип ресурса, который нужно удалить (например, `'products'`, `'categories'`).
-   `resource_id` (int | str): ID ресурса, который нужно удалить.

**Возвращает**:

-   `bool`: `True` в случае успешного удаления, `False` в случае ошибки.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами:
    *   `resource`: Тип ресурса.
    *   `resource_id`: ID ресурса.
    *   `method`: `'DELETE'` (метод удаления).
2.  Возвращает результат выполнения метода `_exec`.

#### `search`

```python
def search(self, resource: str, filter: Optional[str | dict] = None, **kwargs) -> List[dict]:
    """Ищет ресурсы в API PrestaShop.

    Args:
        resource (str): API ресурс (например, 'products').
        filter (Optional[str  |  dict]): Фильтр для поиска.

    Returns:
        List[dict]: Список ресурсов, соответствующих критериям поиска.
    """
```

**Назначение**: Выполняет поиск ресурсов в API PrestaShop с применением фильтра.

**Параметры**:

-   `resource` (str): Тип ресурса, в котором нужно выполнить поиск (например, `'products'`, `'categories'`).
-   `filter` (Optional[str  |  dict]): Фильтр поиска в виде строки или словаря.
-   `**kwargs`: Дополнительные параметры запроса.

**Возвращает**:

-   `List[dict]`: Список ресурсов, соответствующих критериям поиска.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами:
    *   `resource`: Тип ресурса.
    *   `search_filter`: Фильтр поиска.
    *   `method`: `'GET'` (метод чтения).
    *   `**kwargs`: Дополнительные параметры запроса.
2.  Возвращает результат выполнения метода `_exec`.

#### `create_binary`

```python
def create_binary(self, resource: str, file_path: str, file_name: str) -> dict:
    """Загружает двоичный файл в ресурс API PrestaShop."""
```

**Назначение**: Загружает бинарный файл (например, изображение) в указанный ресурс API PrestaShop.

**Параметры**:

-   `resource` (str): Путь к ресурсу API, куда нужно загрузить файл (например, `'images/products/22'`).
-   `file_path` (str): Путь к файлу на локальной файловой системе.
-   `file_name` (str): Имя файла, которое будет присвоено загружаемому файлу.

**Возвращает**:

-   `dict`: Ответ от API в случае успеха или словарь с информацией об ошибке в случае неудачи.

**Как работает функция**:

1.  Открывает файл, расположенный по пути `file_path`, в режиме чтения байтов (`'rb'`).
2.  Формирует словарь `files` для передачи в запросе, указывая имя файла (`file_name`), содержимое файла и MIME-тип (`'image/jpeg'`).
3.  Выполняет POST-запрос к API PrestaShop, передавая файл в параметре `files`.
4.  Проверяет статус ответа и вызывает исключение `HTTPError`, если произошла ошибка.
5.  Разбирает ответ от API с помощью метода `_parse_response`.
6.  В случае возникновения исключений `RequestException` или `Exception`, логирует ошибку и возвращает словарь с информацией об ошибке.

#### `get_schema`

```python
def get_schema(
    self, resource: Optional[str] = None, resource_id: Optional[int] = None, schema: Optional[str] = 'blank', **kwards
) -> dict | None:
    """Получает схему заданного ресурса из API PrestaShop.

    Args:
        resource (str): Название ресурса (например, 'products', 'customers').
            Если не указано - вернется список всех схем сущностей, доступных для API ключа.
        resource_id (Optinal[str]): ID ресурса.
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

**Назначение**: Получает схему указанного ресурса из API PrestaShop.

**Параметры**:

-   `resource` (str, optional): Имя ресурса (например, `'products'`, `'customers'`). Если не указано, возвращается список всех схем сущностей, доступных для API-ключа.
-   `resource_id` (int, optional): ID ресурса.
-   `schema` (str, optional): Тип схемы. Возможные значения:
    -   `'blank'` (по умолчанию): Возвращает пустую схему ресурса.
    -   `'synopsis'` или `'simplified'`: Возвращает упрощенную схему.
    -   `'full'` или отсутствует: Возвращает полную схему ресурса.
    -   `'form'`: Возвращает схему, оптимизированную для отображения в форме редактирования.
-   `**kwargs`: Дополнительные параметры запроса.

**Возвращает**:

-   `dict  |  None`: Схема запрошенного ресурса в виде словаря или `None` в случае ошибки.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами:
    *   `resource`: Имя ресурса.
    *   `resource_id`: ID ресурса.
    *   `schema`: Тип схемы.
    *   `method`: `'GET'` (метод чтения).
    *   `**kwargs`: Дополнительные параметры запроса.
2.  Возвращает результат выполнения метода `_exec`.

#### `get_data`

```python
def get_data(self, resource: str, **kwargs) -> Optional[dict]:
    """Получает данные из ресурса API PrestaShop и сохраняет их.

    Args:
        resource (str): API ресурс (например, 'products').
        **kwargs: Дополнительные аргументы для API запроса.

    Returns:
        dict | None: Данные из API или `False` в случае ошибки.
    """
```

**Назначение**: Получает данные из указанного ресурса API PrestaShop.

**Параметры**:

-   `resource` (str): Имя ресурса, данные которого необходимо получить (например, `'products'`, `'categories'`).
-   `**kwargs`: Дополнительные параметры запроса, которые будут переданы в метод `_exec`.

**Возвращает**:

-   `dict | None`: Данные, полученные из API, в виде словаря или `None` в случае ошибки.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами:
    *   `resource`: Имя ресурса.
    *   `method`: `'GET'` (метод чтения).
    *   `**kwargs`: Дополнительные параметры запроса.
2.  Возвращает результат выполнения метода `_exec`.

#### `get_apis`

```python
def get_apis(self) -> Optional[dict]:
    """Получает список всех доступных API.

    Returns:
        dict: Список доступных API.
    """
```

**Назначение**: Получает список всех доступных API из PrestaShop.

**Возвращает**:

-   `dict`: Список доступных API.

**Как работает функция**:

1.  Вызывает метод `_exec` с параметрами:
    *   `'apis'`: Указывает, что нужно получить список API.
    *   `method`: `'GET'` (метод чтения).
    *   `data_format`: Формат данных (`self.data_format`).
2.  Возвращает результат выполнения метода `_exec`.

#### `upload_image_async`

```python
def upload_image_async(
    self, resource: str, resource_id: int, img_url: str, img_name: Optional[str] = None
) -> Optional[dict]:
    """Асинхронно загружает изображение в API PrestaShop.

    Args:
        resource (str): API ресурс (например, 'images/products/22').
        resource_id (int): ID ресурса.
        img_url (str): URL изображения.
        img_name (Optional[str]): Имя файла изображения, по умолчанию None.

    Returns:
        dict | None: Ответ от API или `False` в случае ошибки.
    """
```

**Назначение**: Асинхронно загружает изображение по URL в API PrestaShop.

**Параметры**:

-   `resource` (str): Ресурс API, куда будет загружено изображение (например, `'images/products/22'`).
-   `resource_id` (int): ID ресурса, к которому привязывается изображение.
-   `img_url` (str): URL изображения, которое нужно загрузить.
-   `img_name` (Optional[str]): Имя файла изображения (без расширения). Если не указано, используется `None`.

**Возвращает**:

-   `dict | None`: Ответ от API в случае успеха или `None` в случае ошибки.

**Как работает функция**:

1.  Разделяет URL изображения на имя файла и расширение.
2.  Формирует имя файла изображения, используя `resource_id` и `img_name`.
3.  Сохраняет изображение с использованием `save_image_from_url` и получает путь к сохраненному файлу.
4.  Вызывает метод `create_binary` для загрузки изображения в API PrestaShop.
5.  Удаляет временный файл изображения с использованием `self.remove_file`.
6.  Возвращает ответ от API.

#### `upload_image_from_url`

```python
def upload_image_from_url(
    self, resource: str, resource_id: int, img_url: str, img_name: Optional[str] = None
) -> Optional[dict]:
    """Загружает изображение в API PrestaShop.

    Args:
        resource (str): API ресурс (например, 'images/products/22').
        resource_id (int): ID ресурса.
        img_url (str): URL изображения.
        img_name (Optional[str]): Имя файла изображения, по умолчанию None.

    Returns:
        dict | None: Ответ от API или `False` в случае ошибки.
    """
```

**Назначение**: Загружает изображение по URL в API PrestaShop.

**Параметры**:

-   `resource` (str): Ресурс API, куда будет загружено изображение (например, `'images/products/22'`).
-   `resource_id` (int): ID ресурса, к которому привязывается изображение.
-   `img_url` (str): URL изображения, которое нужно загрузить.
-   `img_name` (Optional[str]): Имя файла изображения (без расширения). Если не указано, используется `None`.

**Возвращает**:

-   `dict | None`: Ответ от API в случае успеха или `None` в случае ошибки.

**Как работает функция**:

1.  Разделяет URL изображения на имя файла и расширение.
2.  Формирует имя файла изображения, используя `resource_id` и `img_name`.
3.  Сохраняет изображение с использованием `save_image_from_url` и получает путь к сохраненному файлу.
4.  Вызывает метод `create_binary` для загрузки изображения в API PrestaShop.
5.  Удаляет временный файл изображения с использованием `self.remove_file`.
6.  Возвращает ответ от API.

#### `get_product_images`

```python
def get_product_images(self, product_id: int) -> Optional[dict]:
    """Получает изображения для продукта.

    Args:
        product_id (int): ID продукта.

    Returns:
        dict | None: Список изображений продукта или `False` в случае ошибки.
    """
```

**Назначение**: Получает список изображений, связанных с указанным продуктом в API PrestaShop.

**Параметры**:

-   `product_id` (int): ID продукта, для которого нужно получить изображения.

**Возвращает**:

-   `dict | None`: Список изображений продукта или `None` в случае ошибки.

**Как работает функция**:

1.  Формирует URL для запроса списка изображений продукта, используя `product_id`.
2.  Вызывает метод `_exec` с параметрами:
    *   `f'products/{product_id}/images'`: URL для запроса списка изображений продукта.
    *   `method`: `'GET'` (метод чтения).
    *   `data_format`: Формат данных (`self.data_format`).
3.  Возвращает результат выполнения метода `_exec`.

## Функции

### `main`

```python
def main() -> None:
    """Проверка сущностей Prestashop"""
```

**Назначение**: Функция для проверки сущностей Prestashop.

**Как работает функция**:

1.  Определяет данные для создания налога (`tax`).
2.  Создает экземпляр класса `PrestaShop` с параметрами подключения к API.
3.  Вызывает методы `create` и `write` для создания и записи данных о налоге.

```