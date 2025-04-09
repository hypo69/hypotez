# Модуль для экспериментов с IOP API AliExpress

## Обзор

Данный модуль предназначен для тестирования взаимодействия с IOP (Iopen Platform) API AliExpress. Он содержит примеры запросов к API для получения информации о продуктах и генерации партнерских ссылок.

## Подробнее

Модуль `test_iop_get.py` используется для экспериментов с API AliExpress через IOP. Он включает в себя настройку клиента IOP, создание запросов к API и обработку ответов. Код демонстрирует, как отправлять запросы для генерации партнерских ссылок и как интерпретировать полученные ответы.

## Функции

### `iop.IopClient`

```python
client = iop.IopClient(url: str, appkey: str, appSecret: str)
```

**Назначение**: Инициализация клиента IOP для взаимодействия с API AliExpress.

**Параметры**:

-   `url` (str): URL-адрес шлюза API.
-   `appkey` (str): Ключ приложения, предоставленный AliExpress.
-   `appSecret` (str): Секретный ключ приложения.

**Как работает функция**:

1.  Создается экземпляр класса `IopClient` с переданными параметрами.
2.  Устанавливается уровень логирования клиента IOP в `iop.P_LOG_LEVEL_DEBUG`.

**Примеры**:

```python
client = iop.IopClient('https://api-sg.aliexpress.com/sync', '345846782', 'e1b26aac391d1bc3987732af93eb26aabc391d187732af93')
client.log_level = iop.P_LOG_LEVEL_DEBUG
```

### `iop.IopRequest`

```python
request = iop.IopRequest(method: str)
```

**Назначение**: Создание запроса к API AliExpress.

**Параметры**:

-   `method` (str): Метод API, который будет вызван.

**Как работает функция**:

1.  Создается экземпляр класса `IopRequest` с указанным методом API.
2.  Добавляются параметры запроса, такие как `promotion_link_type`, `source_values` и `tracking_id`.

**Примеры**:

```python
request = iop.IopRequest('aliexpress.affiliate.link.generate')
request.add_api_param('promotion_link_type', '0')
request.add_api_param('source_values', 'https://www.aliexpress.com/item/1005005058280371.html')
request.add_api_param('tracking_id', 'default')
```

### `client.execute`

```python
response = client.execute(request: iop.IopRequest)
```

**Назначение**: Выполнение запроса к API AliExpress.

**Параметры**:

-   `request` (iop.IopRequest): Запрос, который необходимо выполнить.

**Возвращает**:

-   `response`: Объект ответа от API.

**Как работает функция**:

1.  Клиент IOP выполняет запрос к API с использованием переданного объекта `IopRequest`.
2.  Полученный ответ сохраняется в переменной `response`.
3.  Выводятся различные атрибуты ответа, такие как тело ответа (`response.body`), тип ответа (`response.type`), код ответа (`response.code`), сообщение об ошибке (`response.message`) и идентификатор запроса (`response.request_id`).

**Примеры**:

```python
response = client.execute(request)

print(response.body)
print(response.type)
print(response.code)
print(response.message)
print(response.request_id)
print(response.body)