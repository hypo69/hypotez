# Модуль для асинхронного взаимодействия с API PrestaShop
==============================================================

Модуль предоставляет класс `PrestaShopAsync` для асинхронного взаимодействия с API PrestaShop,
включая операции CRUD, поиск и загрузку изображений.

## Обзор

Данный модуль предназначен для упрощения взаимодействия с PrestaShop API. Он предоставляет асинхронный клиент,
который позволяет выполнять запросы к API PrestaShop и обрабатывать ответы в форматах JSON и XML.
Модуль включает в себя обработку ошибок, преобразование данных и вспомогательные функции для работы с API.

## Подробней

Модуль `api_async.py` предоставляет асинхронный класс `PrestaShopAsync` для взаимодействия с API PrestaShop.
Он позволяет выполнять различные операции, такие как создание, чтение, обновление и удаление ресурсов,
а также поиск и загрузку изображений. Класс поддерживает форматы данных JSON и XML.

## Классы

### `Format`

**Описание**:
Перечисление, определяющее форматы данных для взаимодействия с API (JSON, XML).

**Принцип работы**:
`Format` представляет собой перечисление, определяющее доступные форматы данных для обмена с API PrestaShop.
В настоящее время предпочтительным форматом является JSON.

### `PrestaShopAsync`

**Описание**:
Асинхронный класс для взаимодействия с API PrestaShop.

**Принцип работы**:
Класс `PrestaShopAsync` предоставляет методы для асинхронного взаимодействия с API PrestaShop.
Он инициализируется с использованием домена API и ключа API, а также поддерживает отладку и выбор формата данных.
Класс предоставляет методы для выполнения запросов к API, обработки ответов и выполнения различных операций,
таких как создание, чтение, обновление и удаление ресурсов.

**Атрибуты**:
- `client` (ClientSession): Асинхронный клиент сессии для выполнения HTTP-запросов.
- `debug` (bool): Флаг, определяющий, включен ли режим отладки.
- `lang_index` (Optional[int]): Индекс языка по умолчанию.
- `data_format` (str): Формат данных по умолчанию ('JSON' или 'XML').
- `ps_version` (str): Версия PrestaShop.
- `API_DOMAIN` (str): Домен API PrestaShop.
- `API_KEY` (str): Ключ API PrestaShop.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `PrestaShopAsync`.
- `ping`: Проверяет доступность веб-сервиса.
- `_check_response`: Проверяет код состояния HTTP-ответа и обрабатывает ошибки.
- `_parse_response_error`: Разбирает ответ об ошибке от API PrestaShop.
- `_prepare`: Подготавливает URL для запроса.
- `_exec`: Выполняет HTTP-запрос к API PrestaShop.
- `_parse`: Разбирает XML или JSON-ответ от API.
- `create`: Создает новый ресурс в API PrestaShop.
- `read`: Читает ресурс из API PrestaShop.
- `write`: Обновляет существующий ресурс в API PrestaShop.
- `unlink`: Удаляет ресурс из API PrestaShop.
- `search`: Выполняет поиск ресурсов в API PrestaShop.
- `create_binary`: Загружает бинарный файл в API PrestaShop.
- `_save`: Сохраняет данные в файл.
- `get_data`: Получает данные из API PrestaShop и сохраняет их.
- `remove_file`: Удаляет файл из файловой системы.
- `get_apis`: Получает список всех доступных API.
- `get_languages_schema`: Получает схему для языков.
- `upload_image_async`: Загружает изображение в API PrestaShop асинхронно.
- `upload_image`: Загружает изображение в API PrestaShop.
- `get_product_images`: Получает изображения для продукта.

## Функции

### `__init__`

```python
def __init__(self, api_domain: str, api_key: str, data_format: str = 'JSON', debug: bool = True) -> None
```

**Назначение**:
Инициализация класса `PrestaShopAsync`.

**Параметры**:
- `api_domain` (str): Домен API PrestaShop.
- `api_key` (str): Ключ API PrestaShop.
- `data_format` (str, optional): Формат данных по умолчанию ('JSON' или 'XML'). По умолчанию 'JSON'.
- `debug` (bool, optional): Флаг, определяющий, включен ли режим отладки. По умолчанию `True`.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `PrestaShopAuthenticationError`: Если ключ API неверен или не существует.
- `PrestaShopException`: Для общих ошибок веб-сервисов PrestaShop.

**Как работает функция**:
1. Функция инициализирует класс `PrestaShopAsync`, присваивая значения атрибутам `API_DOMAIN`, `API_KEY`, `debug` и `data_format` на основе переданных аргументов.
2. Создается асинхронный клиент сессии `ClientSession` с использованием ключа API для аутентификации. Устанавливается таймаут для запросов.

```
A: Инициализация класса PrestaShopAsync
│
B: Создание асинхронного клиента сессии
│
C: Присвоение значений атрибутам
```

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

**Назначение**:
Проверка работоспособности веб-сервиса асинхронно.

**Параметры**:
- `self`

**Возвращает**:
- `bool`: `True`, если веб-сервис работает, иначе `False`.

**Как работает функция**:
1. Функция отправляет HEAD-запрос к API_DOMAIN.
2. Проверяется статус ответа с помощью `_check_response`.

```
A: Отправка HEAD-запроса к API_DOMAIN
│
B: Проверка статуса ответа с помощью _check_response
```

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

**Назначение**:
Проверка кода состояния HTTP-ответа и обработка ошибок асинхронно.

**Параметры**:
- `status_code` (int): Код состояния HTTP-ответа.
- `response` (aiohttp.ClientResponse): Объект HTTP-ответа.
- `method` (str, optional): HTTP-метод, использованный для запроса.
- `url` (str, optional): URL запроса.
- `headers` (dict, optional): Заголовки запроса.
- `data` (dict, optional): Данные, отправленные в запросе.

**Возвращает**:
- `bool`: `True`, если код состояния 200 или 201, иначе `False`.

**Как работает функция**:
1. Функция проверяет, находится ли код состояния HTTP-ответа в диапазоне 200-201.
2. Если код состояния не находится в указанном диапазоне, вызывается функция `_parse_response_error` для обработки ошибки.

```
A: Проверка кода состояния HTTP-ответа
│
B: Вызов _parse_response_error, если код состояния не 200 или 201
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    async with api.client.get('https://your-prestashop-domain.com/api/products') as response:
        result = api._check_response(response.status, response)
        print(f"Check response result: {result}")
```

### `_parse_response_error`

```python
def _parse_response_error(self, response, method: Optional[str] = None, url: Optional[str] = None,
                              headers: Optional[dict] = None, data: Optional[dict] = None)
```

**Назначение**:
Разбор ответа об ошибке от API PrestaShop асинхронно.

**Параметры**:
- `response` (aiohttp.ClientResponse): Объект HTTP-ответа от сервера.
- `method` (str, optional): HTTP-метод, использованный для запроса.
- `url` (str, optional): URL запроса.
- `headers` (dict, optional): Заголовки запроса.
- `data` (dict, optional): Данные, отправленные в запросе.

**Как работает функция**:
1. Функция проверяет формат данных (`data_format`).
2. Если формат данных JSON, извлекается код состояния и текст ответа, затем регистрируется критическая ошибка с использованием `logger.critical`.
3. Если формат данных XML, ответ разбирается с использованием `_parse`, и извлекаются код и сообщение об ошибке. Затем регистрируется ошибка с использованием `logger.error`.

```
A: Проверка формата данных
│
├───> B1: Если JSON, извлечение кода состояния и текста ответа, логирование критической ошибки
│
└───> B2: Если XML, разбор ответа, извлечение кода и сообщения об ошибке, логирование ошибки
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    async with api.client.get('https://your-prestashop-domain.com/api/nonexistent') as response:
        api._parse_response_error(response)
```

### `_prepare`

```python
def _prepare(self, url: str, params: dict) -> str
```

**Назначение**:
Подготовка URL для запроса.

**Параметры**:
- `url` (str): Базовый URL.
- `params` (dict): Параметры для запроса.

**Возвращает**:
- `str`: Подготовленный URL с параметрами.

**Как работает функция**:
1. Функция создает объект `PreparedRequest`.
2. Подготавливает URL с использованием базового URL и параметров.

```
A: Создание объекта PreparedRequest
│
B: Подготовка URL с использованием базового URL и параметров
```

**Примеры**:

```python
api = PrestaShopAsync(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key',
    data_format='JSON',
    debug=True
)
url = api._prepare('https://your-prestashop-domain.com/api/products', {'limit': '3'})
print(url)
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

**Назначение**:
Выполнение HTTP-запроса к API PrestaShop асинхронно.

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
- `limit` (str, optional): Ограничение количества результатов для запроса.
- `language` (int, optional): ID языка для запроса.
- `io_format` (str, optional): Формат данных ('JSON' или 'XML').

**Возвращает**:
- `dict | None`: Ответ от API или `False` в случае неудачи.

**Как работает функция**:
1. Функция подготавливает URL с использованием `_prepare`.
2. Преобразует данные в XML, если `data` задано и `io_format` равно 'XML'.
3. Выполняет HTTP-запрос с использованием `aiohttp.ClientSession`.
4. Проверяет статус ответа с использованием `_check_response`.
5. Если запрос успешен, разбирает ответ и возвращает данные.

```
A: Подготовка URL с использованием _prepare
│
B: Преобразование данных в XML, если необходимо
│
C: Выполнение HTTP-запроса с использованием aiohttp.ClientSession
│
D: Проверка статуса ответа с использованием _check_response
│
E: Разбор ответа и возврат данных
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=False
    )
    products = await api._exec(resource='products', limit='3')
    print(products)
```

### `_parse`

```python
def _parse(self, text: str) -> dict | ElementTree.Element | bool
```

**Назначение**:
Разбор XML или JSON-ответа от API асинхронно.

**Параметры**:
- `text` (str): Текст ответа.

**Возвращает**:
- `dict | ElementTree.Element | bool`: Разобранные данные или `False` в случае неудачи.

**Как работает функция**:
1. Функция пытается разобрать текст ответа в зависимости от формата данных (`data_format`).
2. Если формат данных JSON, используется `j_loads` для разбора JSON.
3. Если формат данных XML, используется `ElementTree.fromstring` для разбора XML.
4. В случае ошибки разбора регистрируется ошибка с использованием `logger.error` и возвращается `False`.

```
A: Проверка формата данных
│
├───> B1: Если JSON, разбор JSON с использованием j_loads
│
└───> B2: Если XML, разбор XML с использованием ElementTree.fromstring
│
C: Обработка ошибок разбора, логирование ошибки и возврат False
```

**Примеры**:

```python
api = PrestaShopAsync(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key',
    data_format='JSON',
    debug=True
)
text = '{"PrestaShop":{"products":[]}}'
data = api._parse(text)
print(data)
```

### `create`

```python
async def create(self, resource: str, data: dict) -> Optional[dict]
```

**Назначение**:
Создание нового ресурса в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'products').
- `data` (dict): Данные для нового ресурса.

**Возвращает**:
- `dict`: Ответ от API.

**Как работает функция**:
1. Функция вызывает `_exec` с HTTP-методом 'POST' и переданными данными.

```
A: Вызов _exec с HTTP-методом 'POST' и переданными данными
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    data = {'product': {'name': 'Test Product'}}
    result = await api.create(resource='products', data=data)
    print(result)
```

### `read`

```python
async def read(self, resource: str, resource_id: Union[int, str], **kwargs) -> Optional[dict]
```

**Назначение**:
Чтение ресурса из API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'products').
- `resource_id` (int | str): ID ресурса.

**Возвращает**:
- `dict`: Ответ от API.

**Как работает функция**:
1. Функция вызывает `_exec` с HTTP-методом 'GET' и ID ресурса.

```
A: Вызов _exec с HTTP-методом 'GET' и ID ресурса
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    result = await api.read(resource='products', resource_id='1')
    print(result)
```

### `write`

```python
async def write(self, resource: str, data: dict) -> Optional[dict]
```

**Назначение**:
Обновление существующего ресурса в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'products').
- `data` (dict): Данные для ресурса.

**Возвращает**:
- `dict`: Ответ от API.

**Как работает функция**:
1. Функция вызывает `_exec` с HTTP-методом 'PUT', ID ресурса, полученным из `data.get('id')`, и переданными данными.

```
A: Вызов _exec с HTTP-методом 'PUT', ID ресурса и переданными данными
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    data = {'id': '1', 'product': {'name': 'Updated Product'}}
    result = await api.write(resource='products', data=data)
    print(result)
```

### `unlink`

```python
async def unlink(self, resource: str, resource_id: Union[int, str]) -> bool
```

**Назначение**:
Удаление ресурса из API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'products').
- `resource_id` (int | str): ID ресурса.

**Возвращает**:
- `bool`: `True`, если успешно, `False` иначе.

**Как работает функция**:
1. Функция вызывает `_exec` с HTTP-методом 'DELETE' и ID ресурса.

```
A: Вызов _exec с HTTP-методом 'DELETE' и ID ресурса
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    result = await api.unlink(resource='products', resource_id='1')
    print(result)
```

### `search`

```python
async def search(self, resource: str, filter: Optional[Union[str, dict]] = None, **kwargs) -> List[dict]
```

**Назначение**:
Поиск ресурсов в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'products').
- `filter` (str | dict, optional): Фильтр для поиска.

**Возвращает**:
- `List[dict]`: Список ресурсов, соответствующих критериям поиска.

**Как работает функция**:
1. Функция вызывает `_exec` с HTTP-методом 'GET' и фильтром для поиска.

```
A: Вызов _exec с HTTP-методом 'GET' и фильтром для поиска
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    result = await api.search(resource='products', filter='[name]=%Test%')
    print(result)
```

### `create_binary`

```python
async def create_binary(self, resource: str, file_path: str, file_name: str) -> dict
```

**Назначение**:
Загрузка бинарного файла в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'images/products/22').
- `file_path` (str): Путь к бинарному файлу.
- `file_name` (str): Имя файла.

**Возвращает**:
- `dict`: Ответ от API.

**Как работает функция**:
1. Функция открывает файл по указанному пути в бинарном режиме.
2. Формирует заголовки запроса, указывая тип контента как 'application/octet-stream'.
3. Отправляет POST-запрос с содержимым файла в теле запроса.
4. Возвращает JSON-ответ от API.

```
A: Открытие файла по указанному пути в бинарном режиме
│
B: Формирование заголовков запроса
│
C: Отправка POST-запроса с содержимым файла в теле запроса
│
D: Возврат JSON-ответа от API
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    # Создайте файл example.txt
    with open('example.txt', 'w') as f:
        f.write('This is a test file.')
    result = await api.create_binary(resource='images/products/22', file_path='example.txt', file_name='example')
    print(result)
```

### `_save`

```python
def _save(self, file_name: str, data: dict)
```

**Назначение**:
Сохранение данных в файл.

**Параметры**:
- `file_name` (str): Имя файла.
- `data` (dict): Данные для сохранения.

**Как работает функция**:
1. Функция использует `save_text_file` для сохранения данных в формате JSON в файл.

```
A: Сохранение данных в формате JSON в файл с использованием save_text_file
```

**Примеры**:

```python
api = PrestaShopAsync(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key',
    data_format='JSON',
    debug=True
)
data = {'products': []}
api._save(file_name='products.json', data=data)
```

### `get_data`

```python
async def get_data(self, resource: str, **kwargs) -> Optional[dict]
```

**Назначение**:
Получение данных из API PrestaShop и сохранение их асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'products').
- `**kwargs`: Дополнительные аргументы для API-запроса.

**Возвращает**:
- `dict | None`: Данные из API или `False` в случае неудачи.

**Как работает функция**:
1. Функция вызывает `_exec` с HTTP-методом 'GET'.
2. Если данные получены, они сохраняются в файл с использованием `_save`.

```
A: Вызов _exec с HTTP-методом 'GET'
│
B: Сохранение данных в файл с использованием _save, если данные получены
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    result = await api.get_data(resource='products', limit='3')
    print(result)
```

### `remove_file`

```python
def remove_file(self, file_path: str)
```

**Назначение**:
Удаление файла из файловой системы.

**Параметры**:
- `file_path` (str): Путь к файлу.

**Как работает функция**:
1. Функция пытается удалить файл с использованием `os.remove`.
2. В случае ошибки регистрируется ошибка с использованием `logger.error`.

```
A: Попытка удаления файла с использованием os.remove
│
B: Обработка ошибок удаления, логирование ошибки
```

**Примеры**:

```python
api = PrestaShopAsync(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key',
    data_format='JSON',
    debug=True
)
# Создайте файл example.txt
with open('example.txt', 'w') as f:
    f.write('This is a test file.')
api.remove_file(file_path='example.txt')
```

### `get_apis`

```python
async def get_apis(self) -> Optional[dict]
```

**Назначение**:
Получение списка всех доступных API асинхронно.

**Возвращает**:
- `dict`: Список доступных API.

**Как работает функция**:
1. Функция вызывает `_exec` с ресурсом 'apis' и HTTP-методом 'GET'.

```
A: Вызов _exec с ресурсом 'apis' и HTTP-методом 'GET'
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    result = await api.get_apis()
    print(result)
```

### `get_languages_schema`

```python
async def get_languages_schema(self) -> Optional[dict]
```

**Назначение**:
Получение схемы для языков асинхронно.

**Возвращает**:
- `dict`: Схема языков или `None` в случае неудачи.

**Как работает функция**:
1. Функция вызывает `_exec` с ресурсом 'languages', `display='full'` и `io_format='JSON'`.
2. В случае ошибки регистрируется ошибка с использованием `logger.error` и возвращается `None`.

```
A: Вызов _exec с ресурсом 'languages', display='full' и io_format='JSON'
│
B: Обработка ошибок, логирование ошибки и возврат None
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    result = await api.get_languages_schema()
    print(result)
```

### `upload_image_async`

```python
async def upload_image_async(self, resource: str, resource_id: int, img_url: str,
                           img_name: Optional[str] = None) -> Optional[dict]
```

**Назначение**:
Загрузка изображения в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'images/products/22').
- `resource_id` (int): ID ресурса.
- `img_url` (str): URL изображения.
- `img_name` (str, optional): Имя файла изображения, по умолчанию `None`.

**Возвращает**:
- `dict | None`: Ответ от API или `False` в случае неудачи.

**Как работает функция**:
1. Функция разделяет URL изображения на имя файла и расширение.
2. Формирует имя файла.
3. Сохраняет изображение из URL в файл с использованием `save_image_from_url`.
4. Загружает изображение в API PrestaShop с использованием `create_binary`.
5. Удаляет временный файл.

```
A: Разделение URL изображения на имя файла и расширение
│
B: Формирование имени файла
│
C: Сохранение изображения из URL в файл с использованием save_image_from_url
│
D: Загрузка изображения в API PrestaShop с использованием create_binary
│
E: Удаление временного файла
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    result = await api.upload_image_async(resource='images/products/22', resource_id=22, img_url='https://example.com/image.jpg', img_name='image')
    print(result)
```

### `upload_image`

```python
async def upload_image(self, resource: str, resource_id: int, img_url: str,
                     img_name: Optional[str] = None) -> Optional[dict]
```

**Назначение**:
Загрузка изображения в API PrestaShop асинхронно.

**Параметры**:
- `resource` (str): API ресурс (например, 'images/products/22').
- `resource_id` (int): ID ресурса.
- `img_url` (str): URL изображения.
- `img_name` (str, optional): Имя файла изображения, по умолчанию `None`.

**Возвращает**:
- `dict | None`: Ответ от API или `False` в случае неудачи.

**Как работает функция**:
Функция выполняет те же действия, что и `upload_image_async`.

```
A: Разделение URL изображения на имя файла и расширение
│
B: Формирование имени файла
│
C: Сохранение изображения из URL в файл с использованием save_image_from_url
│
D: Загрузка изображения в API PrestaShop с использованием create_binary
│
E: Удаление временного файла
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    result = await api.upload_image(resource='images/products/22', resource_id=22, img_url='https://example.com/image.jpg', img_name='image')
    print(result)
```

### `get_product_images`

```python
async def get_product_images(self, product_id: int) -> Optional[dict]
```

**Назначение**:
Получение изображений для продукта асинхронно.

**Параметры**:
- `product_id` (int): ID продукта.

**Возвращает**:
- `dict | None`: Список изображений продукта или `False` в случае неудачи.

**Как работает функция**:
1. Функция вызывает `_exec` с ресурсом 'products/{product_id}/images' и HTTP-методом 'GET'.

```
A: Вызов _exec с ресурсом 'products/{product_id}/images' и HTTP-методом 'GET'
```

**Примеры**:

```python
async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )
    result = await api.get_product_images(product_id=22)
    print(result)