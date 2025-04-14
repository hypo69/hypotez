# Модуль для взаимодействия с PrestaShop API

## Обзор

Этот модуль предоставляет класс `PrestaShop` для взаимодействия с PrestaShop webservice API, используя JSON и XML для форматирования сообщений. Он поддерживает CRUD операции, поиск и загрузку изображений, а также обрабатывает ошибки.

## Подробнее

Модуль предназначен для упрощения взаимодействия с PrestaShop API. Он включает в себя настройку соединения, выполнение запросов, обработку ответов и преобразование данных. Поддерживает как JSON, так и XML форматы данных.

## Классы

### `Config`

**Описание**: Класс конфигурации для PrestaShop API.
    
**Атрибуты**:
- `language` (str): Язык.
- `ps_version` (str): Версия PrestaShop. По умолчанию ''.
- `MODE` (str): Определяет конечную точку API (`dev`, `dev8`, `prod`). По умолчанию 'dev'.
- `POST_FORMAT` (str): Формат отправляемых данных (XML). По умолчанию 'XML'.
- `API_DOMAIN` (str): Домен API. По умолчанию ''.
- `API_KEY` (str): Ключ API. По умолчанию ''.

**Принцип работы**:

Класс `Config` предназначен для хранения и управления конфигурационными данными, необходимыми для взаимодействия с API PrestaShop. Он автоматически загружает переменные окружения, если `USE_ENV` установлен в `True`, или использует жестко заданные значения для различных режимов (`dev`, `dev8`, `prod`). Если режим не указан или указан неверно, устанавливается режим `dev`.

### `PrestaShop`

**Описание**: Класс для взаимодействия с PrestaShop webservice API.

**Атрибуты**:
- `client` (Session): HTTP клиентская сессия для выполнения запросов.
- `debug` (bool): Флаг для активации режима отладки. По умолчанию `False`.
- `language` (Optional[int]): ID языка по умолчанию. По умолчанию `None`.
- `data_format` (str): Формат данных по умолчанию ('JSON' или 'XML'). По умолчанию `'JSON'`.
- `ps_version` (str): Версия PrestaShop. По умолчанию ''.
- `api_domain` (str): Домен API.
- `api_key` (str): Ключ API.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `PrestaShop`.
- `ping`: Проверяет работоспособность веб-сервиса.
- `_check_response`: Проверяет статус ответа и обрабатывает ошибки.
- `_parse_response_error`: Обрабатывает ошибки, полученные от PrestaShop API.
- `_prepare_url`: Подготавливает URL для запроса.
- `_exec`: Выполняет HTTP запрос к PrestaShop API.
- `_parse_response`: Преобразует XML или JSON ответ от API в структуру dict.
- `create`: Создает новый ресурс через API PrestaShop.
- `read`: Читает ресурс из API PrestaShop.
- `write`: Обновляет существующий ресурс в API PrestaShop.
- `unlink`: Удаляет ресурс из API PrestaShop.
- `search`: Поиск ресурсов в API PrestaShop.
- `create_binary`: Загружает бинарный файл в ресурс API PrestaShop.
- `get_schema`: Получает схему заданного ресурса из API PrestaShop.
- `get_data`: Получает данные из API PrestaShop.
- `get_apis`: Получает список всех доступных API.
- `upload_image_async`: Асинхронно загружает изображение в PrestaShop API.
- `upload_image_from_url`: Загружает изображение в PrestaShop API.
- `get_product_images`: Получает изображения продукта.

## Методы класса

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
    """Инициализирует класс PrestaShop.

    Args:
        api_key (str): Ключ API, полученный из PrestaShop.
        api_domain (str): Домен магазина PrestaShop (например, https://myPrestaShop.com).
        data_format (str): Формат данных по умолчанию ('JSON' или 'XML'). По умолчанию 'JSON'.
        default_lang (int): ID языка по умолчанию. По умолчанию 1.
        debug (bool): Включает режим отладки. По умолчанию False.

    Raises:
        PrestaShopAuthenticationError: Если ключ API неверный или не существует.
        PrestaShopException: Для общих ошибок веб-сервисов PrestaShop.
    """
```

**Как работает функция**:

1. **Инициализация атрибутов**: Устанавливает значения атрибутов `api_domain`, `api_key`, `debug`, `language` и `data_format` на основе переданных аргументов.
2. **Аутентификация клиента**: Если HTTP-клиент `self.client` не имеет настроек аутентификации, устанавливает аутентификацию на основе API-ключа.
3. **Проверка соединения**: Выполняет HEAD-запрос к API-домену, чтобы проверить соединение. Если соединение не установлено, регистрирует ошибку.
4. **Получение версии PrestaShop**: Получает версию PrestaShop из заголовков ответа и сохраняет её в атрибуте `ps_version`.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
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
        bool: Результат проверки. Возвращает `True`, если веб-сервис работает, иначе `False`.
    """
```

**Как работает функция**:

1. **Выполнение HEAD-запроса**: Выполняет HEAD-запрос к API-домену.
2. **Проверка ответа**: Вызывает метод `_check_response` для проверки статуса ответа.
3. **Возврат результата**: Возвращает `True`, если статус ответа 200 или 201, иначе `False`.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
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

**Как работает функция**:

1. **Проверка кода состояния**: Проверяет, находится ли `status_code` в диапазоне успешных кодов (200, 201).
2. **Обработка ошибок**: Если код состояния не является успешным, вызывает метод `_parse_response_error` для обработки ошибки.
3. **Возврат результата**: Возвращает `True`, если статус ответа 200 или 201, иначе `False`.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
import requests
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
response = requests.get('https://your-prestashop-domain.com/api/')
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
    """Разбирает ответ об ошибке от PrestaShop API.

    Args:
        response (requests.Response): Объект HTTP-ответа от сервера.
    """
```

**Как работает функция**:

1. **Определение формата данных**: Проверяет, какой формат данных используется (`JSON` или `XML`).
2. **Обработка JSON**: Если формат данных `JSON`, проверяет код состояния ответа и, если он не равен 200 или 201, выводит информацию об ошибке в лог.
3. **Обработка XML**: Если формат данных `XML`, вызывает метод `_parse_response` для преобразования XML-ответа в словарь, извлекает код и сообщение об ошибке и выводит их в лог.
4. **Возврат результата**: Возвращает объект ответа `response` (в случае JSON) или код и сообщение об ошибке (в случае XML).

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
import requests
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
response = requests.get('https://your-prestashop-domain.com/api/nonexistent_resource')
api._parse_response_error(response)
```

### `_prepare_url`

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

**Как работает функция**:

1. **Создание объекта PreparedRequest**: Создает экземпляр класса `PreparedRequest` из библиотеки `requests`.
2. **Подготовка URL**: Вызывает метод `prepare_url` объекта `PreparedRequest` для добавления параметров к базовому URL.
3. **Возврат URL**: Возвращает подготовленный URL.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
url = 'https://your-prestashop-domain.com/api/products'
params = {'display': 'full', 'limit': '10'}
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
    """Выполняет HTTP-запрос к PrestaShop API.

    Args:
        resource (str): API ресурс (например, 'products').
        resource_id (Optional[int | str]): ID ресурса.
        resource_ids (Optional[int | Tuple[int]]): ID ресурсов.
        method (str): HTTP-метод ('GET', 'POST', 'PUT', 'DELETE'). По умолчанию 'GET'.
        data (Optional[dict | str]): Данные для запроса.
        headers (Optional[dict]): Заголовки запроса.
        search_filter (Optional[str | dict]): Фильтр для поиска.
        display (Optional[str | list]): Поля для отображения. По умолчанию 'full'.
        schema (Optional[str]): Схема данных.
        sort (Optional[str]): Параметр сортировки.
        limit (Optional[str]): Лимит количества возвращаемых записей.
        language (Optional[int]): ID языка.
        data_format (str): Формат данных ('JSON' или 'XML'). По умолчанию 'JSON'.

    Returns:
        Optional[dict]: Ответ от API.
    """
```

**Как работает функция**:

1. **Настройка отладки**: Устанавливает уровень отладки HTTP-соединения.
2. **Подготовка URL**: Формирует URL на основе переданных параметров ресурса и ID, используя метод `_prepare_url`.
3. **Настройка заголовков**: Устанавливает заголовки запроса в зависимости от формата данных (`JSON` или `XML`).
4. **Выполнение запроса**: Выполняет HTTP-запрос с использованием библиотеки `requests` и переданных параметров.
5. **Проверка ответа**: Проверяет статус ответа с помощью метода `_check_response`.
6. **Обработка ответа**: Преобразует ответ в словарь с помощью метода `_parse_response`.
7. **Обработка ошибок**: В случае ошибки логирует её и возвращает `False`.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
products = api._exec(resource='products', method='GET', limit='5')
print(products)
```

### `_parse_response`

```python
def _parse_response(self, response: Response, data_format: Optional[str] = 'JSON') -> dict | None:
    """Преобразует XML или JSON ответ от API в структуру dict.

    Args:
        response (Response): Объект ответа.
        data_format (Optional[str]): Формат данных ('JSON' или 'XML'). По умолчанию 'JSON'.

    Returns:
        dict: Разобранные данные или `False` в случае ошибки.
    """
```

**Как работает функция**:

1. **Определение формата данных**: Определяет, в каком формате получен ответ (`JSON` или `XML`).
2. **Преобразование JSON**: Если формат `JSON`, использует метод `response.json()` для преобразования JSON-ответа в словарь.
3. **Преобразование XML**: Если формат `XML`, использует функцию `xml2dict` для преобразования XML-ответа в словарь.
4. **Извлечение данных**: Извлекает данные из словаря, возвращая значение ключа `prestashop`, если он существует, иначе возвращает весь словарь.
5. **Обработка ошибок**: В случае ошибки логирует её и возвращает пустой словарь.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
import requests
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
response = requests.get('https://your-prestashop-domain.com/api/products?output_format=JSON')
data = api._parse_response(response)
print(data)
```

### `create`

```python
def create(self, resource: str, data: dict, *args, **kwards) -> Optional[dict]:
    """Создает новый ресурс через PrestaShop API.

    Args:
        resource (str): API ресурс (например, 'products').
        data (dict): Данные для нового ресурса.

    Returns:
        dict: Ответ от API.
    """
```

**Как работает функция**:

Вызывает метод `_exec` с указанием ресурса, метода `POST` и передачей данных для создания нового ресурса.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
data = {
    'product': {
        'name': [{'language': {'id': '1', 'value': 'Новый продукт'}}],
        'active': '1'
    }
}
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

**Как работает функция**:

Вызывает метод `_exec` с указанием ресурса, ID ресурса и метода `GET` для чтения ресурса.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
product = api.read(resource='products', resource_id=1)
print(product)
```

### `write`

```python
def write(self, resource: str, data: dict) -> Optional[dict]:
    """Обновляет существующий ресурс в PrestaShop API.

    Args:
        resource (str): API ресурс (например, 'products').
        data (dict): Данные для ресурса.

    Returns:
        dict: Ответ от API.
    """
```

**Как работает функция**:

Вызывает метод `_exec` с указанием ресурса, ID ресурса (полученного из данных), метода `PUT` и передачей данных для обновления ресурса.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
data = {
    'id': 1,
    'product': {
        'name': [{'language': {'id': '1', 'value': 'Обновленный продукт'}}],
        'active': '1'
    }
}
response = api.write(resource='products', data=data)
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
        bool: `True`, если успешно, `False` иначе.
    """
```

**Как работает функция**:

Вызывает метод `_exec` с указанием ресурса, ID ресурса и метода `DELETE` для удаления ресурса.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
is_deleted = api.unlink(resource='products', resource_id=1)
print(f"Удалено: {is_deleted}")
```

### `search`

```python
def search(self, resource: str, filter: Optional[str | dict] = None, **kwargs) -> List[dict]:
    """Поиск ресурсов в PrestaShop API.

    Args:
        resource (str): API ресурс (например, 'products').
        filter (Optional[str  |  dict]): Фильтр для поиска.

    Returns:
        List[dict]: Список ресурсов, соответствующих критериям поиска.
    """
```

**Как работает функция**:

Вызывает метод `_exec` с указанием ресурса, фильтра поиска и метода `GET` для поиска ресурсов.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
products = api.search(resource='products', filter='[name]=%Новый%')
print(products)
```

### `create_binary`

```python
def create_binary(self, resource: str, file_path: str, file_name: str) -> dict:
    """Загружает бинарный файл в ресурс API PrestaShop."""
```

**Как работает функция**:

1. **Открытие файла**: Открывает файл по указанному пути (`file_path`) в бинарном режиме для чтения.
2. **Подготовка данных**: Формирует словарь `files` с данными файла, включая имя файла и MIME-тип.
3. **Выполнение POST-запроса**: Выполняет POST-запрос к API с использованием библиотеки `requests` для загрузки файла.
4. **Обработка ответа**: Проверяет статус ответа и возвращает результат.
5. **Обработка ошибок**: В случае ошибки логирует её и возвращает словарь с информацией об ошибке.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
file_path = 'path/to/image.jpg'
file_name = 'image.jpg'
response = api.create_binary(resource='images/products/1', file_path=file_path, file_name=file_name)
print(response)
```

### `get_schema`

```python
def get_schema(
    self, resource: Optional[str] = None, resource_id: Optional[int] = None, schema: Optional[str] = 'blank', **kwards
) -> dict | None:
    """Получает схему заданного ресурса из API PrestaShop.

    Args:
        resource (str): Название ресурса (например, 'products', 'customers').
                        Если не указан, возвращается список всех схем сущностей, доступных для API-ключа.
        resource_id (Optinal[str]): ID ресурса.
        schema (Optional[str]): Тип схемы:
            - 'blank': Возвращает пустую схему ресурса.
            - 'synopsis': Возвращает упрощенную схему.
            - 'full': Возвращает полную схему ресурса.

    Returns:
        dict | None: Схема запрошенного ресурса или `None` в случае ошибки.
    """
```

**Как работает функция**:

Вызывает метод `_exec` с указанием ресурса, ID ресурса, типа схемы и метода `GET` для получения схемы ресурса.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
schema = api.get_schema(resource='products', schema='blank')
print(schema)
```

### `get_data`

```python
def get_data(self, resource: str, **kwargs) -> Optional[dict]:
    """Извлекает данные из API PrestaShop и сохраняет их.

    Args:
        resource (str): API ресурс (например, 'products').
        **kwargs: Дополнительные аргументы для API запроса.

    Returns:
        dict | None: Данные из API или `False` в случае ошибки.
    """
```

**Как работает функция**:

Вызывает метод `_exec` с указанием ресурса и метода `GET` для получения данных из API.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
data = api.get_data(resource='products', limit='5')
print(data)
```

### `get_apis`

```python
def get_apis(self) -> Optional[dict]:
    """Получает список всех доступных API.

    Returns:
        dict: Список доступных API.
    """
```

**Как работает функция**:

Вызывает метод `_exec` с указанием ресурса `'apis'` и методом `GET` для получения списка доступных API.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
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
        img_url (str): URL изображения.
        img_name (Optional[str]): Имя файла изображения, по умолчанию None.

    Returns:
        dict | None: Ответ от API или `False` в случае ошибки.
    """
```

**Как работает функция**:

1. **Разделение URL**: Разделяет URL изображения на части, чтобы получить имя файла и расширение.
2. **Формирование имени файла**: Формирует имя файла на основе ID ресурса и имени изображения.
3. **Сохранение изображения**: Вызывает функцию `save_image_from_url` для сохранения изображения из URL во временный файл.
4. **Загрузка изображения**: Вызывает метод `create_binary` для загрузки изображения в API PrestaShop.
5. **Удаление временного файла**: Вызывает метод `remove_file` для удаления временного файла.
6. **Возврат результата**: Возвращает ответ от API.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
resource = 'images/products/1'
resource_id = 1
img_url = 'https://example.com/image.jpg'
response = api.upload_image_async(resource=resource, resource_id=resource_id, img_url=img_url)
print(response)
```

### `upload_image_from_url`

```python
def upload_image_from_url(
    self, resource: str, resource_id: int, img_url: str, img_name: Optional[str] = None
) -> Optional[dict]:
    """Загружает изображение в PrestaShop API.

    Args:
        resource (str): API ресурс (например, 'images/products/22').
        resource_id (int): ID ресурса.
        img_url (str): URL изображения.
        img_name (Optional[str]): Имя файла изображения, по умолчанию None.

    Returns:
        dict | None: Ответ от API или `False` в случае ошибки.
    """
```

**Как работает функция**:

1. **Разделение URL**: Разделяет URL изображения на части, чтобы получить имя файла и расширение.
2. **Формирование имени файла**: Формирует имя файла на основе ID ресурса и имени изображения.
3. **Сохранение изображения**: Вызывает функцию `save_image_from_url` для сохранения изображения из URL во временный файл.
4. **Загрузка изображения**: Вызывает метод `create_binary` для загрузки изображения в API PrestaShop.
5. **Удаление временного файла**: Вызывает метод `remove_file` для удаления временного файла.
6. **Возврат результата**: Возвращает ответ от API.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
resource = 'images/products/1'
resource_id = 1
img_url = 'https://example.com/image.jpg'
response = api.upload_image_from_url(resource=resource, resource_id=resource_id, img_url=img_url)
print(response)
```

### `get_product_images`

```python
def get_product_images(self, product_id: int) -> Optional[dict]:
    """Получает изображения продукта.

    Args:
        product_id (int): ID продукта.

    Returns:
        dict | None: Список изображений продукта или `False` в случае ошибки.
    """
```

**Как работает функция**:

Вызывает метод `_exec` с указанием ресурса `'products/{product_id}/images'` и методом `GET` для получения изображений продукта.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_key='your_api_key',
    api_domain='https://your-prestashop-domain.com'
)
product_id = 1
images = api.get_product_images(product_id=product_id)
print(images)
```

## Другие функции

### `main`

```python
def main() -> None:
    """Проверка сущностей Prestashop"""
```

**Как работает функция**:

1. **Определение данных**: Определяет данные для создания налога.
2. **Создание объекта PrestaShop**: Создает экземпляр класса `PrestaShop` с использованием параметров конфигурации.
3. **Создание налога**: Вызывает метод `create` для создания налога.
4. **Обновление налога**: Вызывает метод `write` для обновления налога.

**Примеры**:

```python
from src.endpoints.prestashop.api import PrestaShop
api = PrestaShop(
    api_domain = Config.API_DOMAIN,
    api_key = Config.API_KEY,
    default_lang = 1,
    debug = True,
    data_format = Config.POST_FORMAT,
)
api.create('taxes', data)
api.write('taxes', data)