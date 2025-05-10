# Модуль для асинхронного взаимодействия с API PrestaShop
## Обзор

Модуль предоставляет асинхронный класс `PrestaShopAsync` для взаимодействия с API PrestaShop,
включая выполнение CRUD операций, поиска и загрузки изображений. Модуль поддерживает форматы данных JSON и XML,
а также предоставляет обработку ошибок и методы для управления данными API.

## Подробней

Этот модуль предназначен для асинхронного взаимодействия с API PrestaShop, обеспечивая возможность выполнения различных операций, таких как создание, чтение, обновление и удаление ресурсов, а также поиск и загрузку изображений. Он использует асинхронные запросы для повышения производительности и эффективности.

## Классы

### `Format`

**Описание**: Перечисление, определяющее форматы данных (JSON, XML) для взаимодействия с API.

**Параметры**:
- `JSON`: Представляет формат JSON.
- `XML`: Представляет формат XML.

### `PrestaShopAsync`

**Описание**: Асинхронный класс для взаимодействия с API PrestaShop.

**Атрибуты**:
- `client` (ClientSession): Асинхронный HTTP клиент для выполнения запросов.
- `debug` (bool): Флаг для включения режима отладки.
- `lang_index` (Optional[int]): Индекс языка по умолчанию.
- `data_format` (str): Формат данных по умолчанию ('JSON' или 'XML').
- `ps_version` (str): Версия PrestaShop.
- `API_DOMAIN` (str): Домен API PrestaShop.
- `API_KEY` (str): Ключ API PrestaShop.

**Методы**:
- `__init__`: Инициализирует класс `PrestaShopAsync`.
- `ping`: Проверяет работоспособность веб-сервиса асинхронно.
- `_check_response`: Проверяет статус ответа и обрабатывает ошибки асинхронно.
- `_parse_response_error`: Разбирает ошибки, полученные от API PrestaShop асинхронно.
- `_prepare`: Подготавливает URL для запроса.
- `_exec`: Выполняет HTTP-запрос к API PrestaShop асинхронно.
- `_parse`: Разбирает ответ API (XML или JSON) асинхронно.
- `create`: Создает новый ресурс в API PrestaShop асинхронно.
- `read`: Читает ресурс из API PrestaShop асинхронно.
- `write`: Обновляет существующий ресурс в API PrestaShop асинхронно.
- `unlink`: Удаляет ресурс из API PrestaShop асинхронно.
- `search`: Ищет ресурсы в API PrestaShop асинхронно.
- `create_binary`: Загружает бинарный файл в API PrestaShop асинхронно.
- `_save`: Сохраняет данные в файл.
- `get_data`: Получает данные из API PrestaShop и сохраняет их асинхронно.
- `remove_file`: Удаляет файл из файловой системы.
- `get_apis`: Получает список всех доступных API асинхронно.
- `get_languages_schema`: Получает схему для языков асинхронно.
- `upload_image_async`: Загружает изображение в API PrestaShop асинхронно.
- `upload_image`: Загружает изображение в API PrestaShop асинхронно.
- `get_product_images`: Получает изображения товара асинхронно.

## Методы класса

### `__init__`

```python
def __init__(self, api_domain: str, api_key: str, data_format: str = 'JSON', debug: bool = True) -> None
```

**Назначение**: Инициализирует класс `PrestaShopAsync`.

**Параметры**:
- `api_domain` (str): Домен API PrestaShop.
- `api_key` (str): Ключ API PrestaShop.
- `data_format` (str, optional): Формат данных по умолчанию ('JSON' или 'XML'). По умолчанию 'JSON'.
- `debug` (bool, optional): Флаг для включения режима отладки. По умолчанию `True`.

**Вызывает исключения**:
- `PrestaShopAuthenticationError`: Если ключ API неверен или не существует.
- `PrestaShopException`: Для общих ошибок веб-сервисов PrestaShop.

**Как работает функция**:
- Инициализирует атрибуты класса, такие как `API_DOMAIN`, `API_KEY`, `debug` и `data_format`.
- Создает асинхронный HTTP клиент `ClientSession` с использованием предоставленного API ключа для аутентификации. Устанавливает таймаут для запросов.

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
async def ping(self) -> bool
```

**Назначение**: Проверяет работоспособность веб-сервиса асинхронно.

**Возвращает**:
- `bool`: `True`, если веб-сервис работает, иначе `False`.

**Как работает функция**:
- Выполняет HTTP HEAD запрос к домену API.
- Проверяет статус ответа с помощью метода `_check_response`.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    result = await api.ping()
    print(f"Ping result: {result}")
```

### `_check_response`

```python
def _check_response(self, status_code: int, response, method: Optional[str] = None, url: Optional[str] = None,
                        headers: Optional[dict] = None, data: Optional[dict] = None) -> bool
```

**Назначение**: Проверяет код статуса ответа и обрабатывает ошибки асинхронно.

**Параметры**:
- `status_code` (int): Код статуса HTTP-ответа.
- `response` (aiohttp.ClientResponse): Объект HTTP-ответа.
- `method` (str, optional): HTTP-метод, использованный для запроса.
- `url` (str, optional): URL запроса.
- `headers` (dict, optional): Заголовки, использованные в запросе.
- `data` (dict, optional): Данные, отправленные в запросе.

**Возвращает**:
- `bool`: `True`, если код статуса 200 или 201, иначе `False`.

**Как работает функция**:
- Проверяет, находится ли код статуса в диапазоне 200-201.
- Если код статуса не входит в указанный диапазон, вызывает метод `_parse_response_error` для обработки ошибки.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(api.API_DOMAIN) as response:
            result = api._check_response(response.status, response)
            print(f"Check response result: {result}")
```

### `_parse_response_error`

```python
def _parse_response_error(self, response, method: Optional[str] = None, url: Optional[str] = None,
                              headers: Optional[dict] = None, data: Optional[dict] = None)
```

**Назначение**: Разбирает ответ об ошибке от API PrestaShop асинхронно.

**Параметры**:
- `response` (aiohttp.ClientResponse): Объект HTTP-ответа от сервера.
- `method` (str, optional): HTTP-метод, использованный для запроса.
- `url` (str, optional): URL запроса.
- `headers` (dict, optional): Заголовки, использованные в запросе.
- `data` (dict, optional): Данные, отправленные в запросе.

**Как работает функция**:
- Проверяет формат данных (`data_format`).
- Если формат JSON, извлекает и логирует код статуса, URL, заголовки и текст ответа.
- Если формат XML, разбирает XML-ответ и извлекает код и сообщение об ошибке. Логирует сообщение об ошибке.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{api.API_DOMAIN}/nonexistent_resource') as response:
            api._parse_response_error(response)
```

### `_prepare`

```python
def _prepare(self, url: str, params: dict) -> str
```

**Назначение**: Подготавливает URL для запроса.

**Параметры**:
- `url` (str): Базовый URL.
- `params` (dict): Параметры для запроса.

**Возвращает**:
- `str`: Подготовленный URL с параметрами.

**Как работает функция**:
- Создает объект `PreparedRequest`.
- Подготавливает URL с использованием базового URL и параметров.

**Примеры**:

```python
api = PrestaShopAsync(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key',
    data_format='JSON',
    debug=True
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
              io_format: str = 'JSON') -> Optional[dict]
```

**Назначение**: Выполняет HTTP-запрос к API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'products', 'categories').
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
- Подготавливает URL с использованием метода `_prepare`.
- Преобразует данные в XML, если `data` предоставлены и `io_format` установлен как 'XML'.
- Выполняет асинхронный HTTP-запрос с использованием `ClientSession`.
- Проверяет статус ответа с помощью метода `_check_response`.
- Разбирает ответ (JSON или XML) с помощью метода `_parse`.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    resource = 'products'
    data = await api._exec(resource=resource, method='GET', limit='1')
    print(f"Data: {data}")
```

### `_parse`

```python
def _parse(self, text: str) -> dict | ElementTree.Element | bool
```

**Назначение**: Разбирает XML или JSON ответ от API асинхронно.

**Параметры**:
- `text` (str): Текст ответа.

**Возвращает**:
- `dict | ElementTree.Element | bool`: Разобранные данные или `False` в случае неудачи.

**Как работает функция**:
- Пытается разобрать текст ответа в зависимости от формата данных (`data_format`).
- Если формат JSON, использует `j_loads` для разбора JSON.
- Если формат XML, использует `ElementTree.fromstring` для разбора XML.
- Обрабатывает исключения, возникающие при разборе, и логирует ошибки.

**Примеры**:

```python
api = PrestaShopAsync(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key',
    data_format='JSON',
    debug=True
)
json_text = '{"PrestaShop":{"products":[]}}'
data = api._parse(json_text)
print(f"Parsed data: {data}")
```

### `create`

```python
async def create(self, resource: str, data: dict) -> Optional[dict]
```

**Назначение**: Создает новый ресурс в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'products').
- `data` (dict): Данные для нового ресурса.

**Возвращает**:
- `dict`: Ответ от API.

**Как работает функция**:
- Вызывает метод `_exec` с HTTP-методом 'POST' для создания нового ресурса.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    resource = 'products'
    data = {'product': {'name': 'Test Product'}}
    response = await api.create(resource, data)
    print(f"Response: {response}")
```

### `read`

```python
async def read(self, resource: str, resource_id: Union[int, str], **kwargs) -> Optional[dict]
```

**Назначение**: Читает ресурс из API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'products').
- `resource_id` (int | str): ID ресурса.

**Возвращает**:
- `dict`: Ответ от API.

**Как работает функция**:
- Вызывает метод `_exec` с HTTP-методом 'GET' для чтения ресурса.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    resource = 'products'
    resource_id = 1
    response = await api.read(resource, resource_id)
    print(f"Response: {response}")
```

### `write`

```python
async def write(self, resource: str, data: dict) -> Optional[dict]
```

**Назначение**: Обновляет существующий ресурс в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'products').
- `data` (dict): Данные для ресурса.

**Возвращает**:
- `dict`: Ответ от API.

**Как работает функция**:
- Вызывает метод `_exec` с HTTP-методом 'PUT' для обновления существующего ресурса.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    resource = 'products'
    data = {'id': 1, 'product': {'name': 'Updated Product'}}
    response = await api.write(resource, data)
    print(f"Response: {response}")
```

### `unlink`

```python
async def unlink(self, resource: str, resource_id: Union[int, str]) -> bool
```

**Назначение**: Удаляет ресурс из API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'products').
- `resource_id` (int | str): ID ресурса.

**Возвращает**:
- `bool`: `True`, если успешно, `False` иначе.

**Как работает функция**:
- Вызывает метод `_exec` с HTTP-методом 'DELETE' для удаления ресурса.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    resource = 'products'
    resource_id = 1
    response = await api.unlink(resource, resource_id)
    print(f"Response: {response}")
```

### `search`

```python
async def search(self, resource: str, filter: Optional[Union[str, dict]] = None, **kwargs) -> List[dict]
```

**Назначение**: Ищет ресурсы в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'products').
- `filter` (str | dict, optional): Фильтр для поиска.

**Возвращает**:
- `List[dict]`: Список ресурсов, соответствующих критериям поиска.

**Как работает функция**:
- Вызывает метод `_exec` с HTTP-методом 'GET' и параметром `search_filter` для поиска ресурсов.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    resource = 'products'
    filter = '[name]=%Test%'
    response = await api.search(resource, filter=filter)
    print(f"Response: {response}")
```

### `create_binary`

```python
async def create_binary(self, resource: str, file_path: str, file_name: str) -> dict
```

**Назначение**: Загружает бинарный файл в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'images/products/22').
- `file_path` (str): Путь к бинарному файлу.
- `file_name` (str): Имя файла.

**Возвращает**:
- `dict`: Ответ от API.

**Как работает функция**:
- Открывает файл в бинарном режиме.
- Устанавливает заголовок `'Content-Type'` как `'application/octet-stream'`.
- Выполняет асинхронный POST-запрос с использованием `ClientSession` для загрузки файла.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    resource = 'images/products/22'
    file_path = 'img.jpg'  # Replace with a valid image file
    file_name = 'img.jpg'
    response = await api.create_binary(resource, file_path, file_name)
    print(f"Response: {response}")
```

### `_save`

```python
def _save(self, file_name: str, data: dict)
```

**Назначение**: Сохраняет данные в файл.

**Параметры**:
- `file_name` (str): Имя файла.
- `data` (dict): Данные для сохранения.

**Как работает функция**:
- Использует функцию `save_text_file` для сохранения данных в файл в формате JSON.

**Примеры**:

```python
api = PrestaShopAsync(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key',
    data_format='JSON',
    debug=True
)
file_name = 'data.json'
data = {'key': 'value'}
api._save(file_name, data)
```

### `get_data`

```python
async def get_data(self, resource: str, **kwargs) -> Optional[dict]
```

**Назначение**: Получает данные из API PrestaShop и сохраняет их асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'products').
- `**kwargs`: Дополнительные аргументы для API запроса.

**Возвращает**:
- `dict | None`: Данные из API или `False` в случае неудачи.

**Как работает функция**:
- Вызывает метод `_exec` для получения данных из API.
- Сохраняет полученные данные в файл с использованием метода `_save`.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    resource = 'products'
    data = await api.get_data(resource, limit='1')
    print(f"Data: {data}")
```

### `remove_file`

```python
def remove_file(self, file_path: str)
```

**Назначение**: Удаляет файл из файловой системы.

**Параметры**:
- `file_path` (str): Путь к файлу.

**Как работает функция**:
- Пытается удалить файл с использованием `os.remove`.
- Логирует ошибки, если удаление не удалось.

**Примеры**:

```python
api = PrestaShopAsync(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key',
    data_format='JSON',
    debug=True
)
file_path = 'data.json'
api.remove_file(file_path)
```

### `get_apis`

```python
async def get_apis(self) -> Optional[dict]
```

**Назначение**: Получает список всех доступных API асинхронно.

**Возвращает**:
- `dict`: Список доступных API.

**Как работает функция**:
- Вызывает метод `_exec` для получения списка API.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    apis = await api.get_apis()
    print(f"APIs: {apis}")
```

### `get_languages_schema`

```python
async def get_languages_schema(self) -> Optional[dict]
```

**Назначение**: Получает схему для языков асинхронно.

**Возвращает**:
- `dict`: Схема языка или `None` в случае неудачи.

**Как работает функция**:
- Вызывает метод `_exec` для получения схемы языков.
- Обрабатывает возможные исключения и логирует ошибки.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    schema = await api.get_languages_schema()
    print(f"Schema: {schema}")
```

### `upload_image_async`

```python
async def upload_image_async(self, resource: str, resource_id: int, img_url: str,
                           img_name: Optional[str] = None) -> Optional[dict]
```

**Назначение**: Загружает изображение в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'images/products/22').
- `resource_id` (int): ID ресурса.
- `img_url` (str): URL изображения.
- `img_name` (str, optional): Имя файла изображения, по умолчанию `None`.

**Возвращает**:
- `dict | None`: Ответ от API или `False` в случае неудачи.

**Как работает функция**:
- Получает расширение файла из URL изображения.
- Создает имя файла.
- Сохраняет изображение из URL во временный файл.
- Загружает изображение в API с использованием метода `create_binary`.
- Удаляет временный файл.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    resource = 'images/products/22'
    resource_id = 22
    img_url = 'https://example.com/image.jpg'  # Replace with a valid image URL
    img_name = 'test_image'
    response = await api.upload_image_async(resource, resource_id, img_url, img_name)
    print(f"Response: {response}")
```

### `upload_image`

```python
async def upload_image(self, resource: str, resource_id: int, img_url: str,
                     img_name: Optional[str] = None) -> Optional[dict]
```

**Назначение**: Загружает изображение в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'images/products/22').
- `resource_id` (int): ID ресурса.
- `img_url` (str): URL изображения.
- `img_name` (str, optional): Имя файла изображения, по умолчанию `None`.

**Возвращает**:
- `dict | None`: Ответ от API или `False` в случае неудачи.

**Как работает функция**:
- Получает расширение файла из URL изображения.
- Создает имя файла.
- Сохраняет изображение из URL во временный файл.
- Загружает изображение в API с использованием метода `create_binary`.
- Удаляет временный файл.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    resource = 'images/products/22'
    resource_id = 22
    img_url = 'https://example.com/image.jpg'  # Replace with a valid image URL
    img_name = 'test_image'
    response = await api.upload_image(resource, resource_id, img_url, img_name)
    print(f"Response: {response}")
```

### `get_product_images`

```python
async def get_product_images(self, product_id: int) -> Optional[dict]
```

**Назначение**: Получает изображения товара асинхронно.

**Параметры**:
- `product_id` (int): ID товара.

**Возвращает**:
- `dict | None`: Список изображений товара или `False` в случае неудачи.

**Как работает функция**:
- Вызывает метод `_exec` для получения списка изображений товара.

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    product_id = 22
    images = await api.get_product_images(product_id)
    print(f"Images: {images}")
```