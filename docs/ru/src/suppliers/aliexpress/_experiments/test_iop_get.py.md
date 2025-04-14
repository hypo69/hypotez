# Модуль для тестирования получения данных через IOP из AliExpress

## Обзор

Модуль `test_iop_get.py` предназначен для тестирования взаимодействия с API AliExpress через IOP (IopClient). Он демонстрирует, как отправлять запросы к API AliExpress и обрабатывать полученные ответы. В данном модуле создается клиент IOP, настраивается запрос и выводятся различные параметры ответа, такие как тело ответа, тип, код, сообщение и уникальный идентификатор запроса.

## Подробней

Этот модуль содержит примеры использования `IopClient` для выполнения запросов к API AliExpress. Он настраивает клиент с использованием URL, ключа приложения и секрета приложения, а также устанавливает уровень логирования. Затем создается запрос API для генерации партнерской ссылки и добавляются параметры, такие как тип партнерской ссылки, исходные значения и идентификатор отслеживания. После выполнения запроса модуль выводит различные атрибуты ответа, включая тело ответа, тип, код, сообщение и идентификатор запроса.

## Функции

### `IopClient`

`IopClient` - это класс для взаимодействия с API AliExpress через IOP.

**Параметры:**

-   `url` (str): URL для подключения к API.
-   `appkey` (str): Ключ приложения.
-   `appSecret` (str): Секрет приложения.

**Принцип работы:**

Класс `IopClient` инициализируется с URL-ом API, ключом приложения и секретом приложения, необходимыми для аутентификации и взаимодействия с API AliExpress. После инициализации можно выполнять запросы к API с использованием метода `execute`.

**Методы:**

-   `execute(request)`: выполняет API-запрос и возвращает ответ.

### `IopRequest`

`IopRequest` - это класс для создания API-запросов к AliExpress.

**Параметры:**

-   `method` (str): Метод API, который необходимо вызвать.

**Принцип работы:**

Класс `IopRequest` представляет собой запрос к API AliExpress. Он инициализируется с указанием метода API, и затем к нему можно добавлять параметры с помощью метода `add_api_param`.

**Методы:**

-   `add_api_param(param_name, param_value)`: добавляет параметр к API-запросу.

## Пример использования

```python
import iop

# Создание клиента IOP с параметрами подключения к API AliExpress
client = iop.IopClient('https://api-sg.aliexpress.com/sync', '345846782', 'e1b26aac391d1bc3987732af93eb26aabc391d187732af93')
client.log_level = iop.P_LOG_LEVEL_DEBUG

# Создание запроса для генерации партнерской ссылки
request = iop.IopRequest('aliexpress.affiliate.link.generate')
request.add_api_param('promotion_link_type', '0')
request.add_api_param('source_values', 'https://www.aliexpress.com/item/1005005058280371.html')
request.add_api_param('tracking_id', 'default')

# Выполнение запроса и получение ответа
response = client.execute(request)

# Вывод информации об ответе
print(response.body)
print(response.type)
print(response.code)
print(response.message)
print(response.request_id)
print(response.body)
```