# Модуль для тестирования вызова API с использованием IopClient

## Обзор

Данный модуль содержит пример кода, демонстрирующий использование библиотеки IopClient для вызова API AliExpress. Он демонстрирует процесс создания запроса API, отправки запроса и получения ответа. 

## Детали

Модуль предоставляет демонстрационный код, показывающий, как использовать IopClient для взаимодействия с API AliExpress. 

## Функции

### `iop.IopClient`

**Описание**: Класс `iop.IopClient` используется для взаимодействия с API AliExpress. 

**Параметры**:

- `url` (str): Базовый URL API.
- `appkey` (str): Ключ приложения.
- `appSecret` (str): Секретный ключ приложения.

**Атрибуты**:

- `log_level`: Уровень логирования.

**Методы**:

- `execute(request, access_token)`: Отправляет запрос API и возвращает ответ.

**Примеры**:

```python
# Создание экземпляра IopClient
client = iop.IopClient('https://api-sg.aliexpress.com/sync', '345846782', 'e1b26aac391d1bc3987732af93')
client.log_level = iop.P_LOG_LEVEL_DEBUG

# Создание запроса API 
request = iop.IopRequest('aliexpress.affiliate.link.generate')

# Добавление параметров запроса
request.add_api_param('promotion_link_type', '0')
request.add_api_param('source_values', 'https://www.aliexpress.com/item/1005005058280371.html')
request.add_api_param('tracking_id', 'default')

# Отправка запроса и получение ответа
response = client.execute(request)

# Вывод ответа
print(response.body)
print(response.type)
print(response.code)
print(response.message)
print(response.request_id)
print(response.body)
```


### `iop.IopRequest`

**Описание**: Класс `iop.IopRequest` используется для создания запросов API.

**Параметры**:

- `method` (str): Метод API (например, `aliexpress.affiliate.link.generate`).

**Атрибуты**:

- `source_values`: Значение параметра `source_values`.
- `api_params`: Словарь параметров запроса.

**Методы**:

- `add_api_param(key, value)`: Добавляет параметр в запрос.
- `set_simplify()`: Устанавливает тип параметров в `simple` (Number, String).

**Примеры**:

```python
# Создание запроса API
request = iop.IopRequest('aliexpress.affiliate.link.generate')

# Добавление параметров запроса
request.add_api_param('promotion_link_type', '0')
request.add_api_param('source_values', 'https://www.aliexpress.com/item/1005005058280371.html')
request.add_api_param('tracking_id', 'default')
```

## Примеры

```python
# Создание экземпляра IopClient
client = iop.IopClient('https://api-sg.aliexpress.com/sync', '345846782', 'e1b26aac391d1bc3987732af93')

# Создание запроса API
request = iop.IopRequest('aliexpress.affiliate.link.generate')

# Добавление параметров запроса
request.add_api_param('promotion_link_type', '0')
request.add_api_param('source_values', 'https://www.aliexpress.com/item/1005005058280371.html')
request.add_api_param('tracking_id', 'default')

# Отправка запроса и получение ответа
response = client.execute(request)

# Вывод ответа
print(response.body)
print(response.type)
print(response.code)
print(response.message)
print(response.request_id)
```

## Примечания

- Модуль использует библиотеку IopClient для взаимодействия с API AliExpress.
- Код предоставляет примеры создания запроса, отправки запроса и получения ответа.
- Модуль может быть использован для тестирования вызова API с использованием IopClient.

## Параметры

- `appkey`: Ключ приложения, используемый для аутентификации.
- `appSecret`: Секретный ключ приложения, используемый для аутентификации.
- `access_token`: Токен доступа для авторизации.
- `source_values`: Значение параметра `source_values`, которое представляет URL товара на AliExpress.
- `promotion_link_type`: Тип промо-ссылки.
- `tracking_id`: ID отслеживания.

## Дополнительная информация

- Библиотека IopClient позволяет разработчикам легко взаимодействовать с API AliExpress.
- Модуль демонстрирует основные функции IopClient, такие как создание запроса, добавление параметров, отправка запроса и получение ответа.
- Модуль также предоставляет примеры использования IopClient для вызова различных методов API.

## Как работает код

1. Создание экземпляра IopClient.
2. Создание запроса API.
3. Добавление параметров к запросу.
4. Отправка запроса API.
5. Получение ответа.
6. Обработка ответа.

## Принцип работы IopClient

- Библиотека IopClient использует протокол HTTP для взаимодействия с API AliExpress.
- IopClient отправляет запросы API в формате JSON.
- IopClient получает ответы API в формате JSON.
- IopClient предоставляет функции для обработки ответов API.

## Документация по IopClient

- https://iop.aliexpress.com/

## Примеры вызова API

- Получение списка категорий: `aliexpress.category.tree.list`
- Получение информации о товаре: `aliexpress.solution.product.schema.get`
- Генерация партнерской ссылки: `aliexpress.affiliate.link.generate`

## Начало работы

1. Установите библиотеку IopClient: `pip install iop`
2. Зарегистрируйте приложение в системе AliExpress.
3. Получите ключ приложения и секретный ключ приложения.
4. Используйте предоставленный код для тестирования вызова API.