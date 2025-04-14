# Модуль для экспериментов с API AliExpress (iop_get.py)

## Обзор

Этот модуль предназначен для экспериментов с API AliExpress с использованием библиотеки `iop`. Он демонстрирует, как создавать запросы к API, устанавливать параметры и обрабатывать ответы.

## Подробней

Модуль содержит примеры запросов к API AliExpress для генерации партнерских ссылок. В коде демонстрируется создание клиента `IopClient`, формирование запроса `IopRequest` с необходимыми параметрами и выполнение запроса с последующей обработкой ответа.
Этот код может использоваться для тестирования интеграции с API AliExpress и проверки работоспособности различных методов API.

## Функции

### `IopClient`

```python
client = iop.IopClient('https://api-sg.aliexpress.com/sync', '345846782', 'e1b26aac391d1bc3987732af93eb26aabc391d187732af93')
```

- **Назначение**: Создание клиента для взаимодействия с API AliExpress.
- **Параметры**:
  - `url` (str): URL API.
  - `appkey` (str): Ключ приложения.
  - `appSecret` (str): Секрет приложения.
- **Как работает**:
  - Инициализирует клиент `IopClient` с предоставленными URL, ключом и секретом приложения.
  - Устанавливает уровень логирования клиента на `P_LOG_LEVEL_DEBUG`.
- **Примеры**:
  ```python
  client = iop.IopClient('https://api-sg.aliexpress.com/sync', '345846782', 'e1b26aac391d1bc3987732af93eb26aabc391d187732af93')
  client.log_level = iop.P_LOG_LEVEL_DEBUG
  ```

### `IopRequest`

```python
request = iop.IopRequest('aliexpress.affiliate.link.generate')
```

- **Назначение**: Создание запроса к API AliExpress.
- **Параметры**:
  - `method` (str): Метод API.
- **Как работает**:
  - Инициализирует запрос `IopRequest` с указанным методом API.
  - Добавляет параметры запроса, такие как `promotion_link_type`, `source_values` и `tracking_id`.
- **Примеры**:
  ```python
  request = iop.IopRequest('aliexpress.affiliate.link.generate')
  request.add_api_param('promotion_link_type', '0')
  request.add_api_param('source_values', 'https://www.aliexpress.com/item/1005005058280371.html')
  request.add_api_param('tracking_id', 'default')
  ```

### `client.execute`

```python
response = client.execute(request)
```

- **Назначение**: Выполнение запроса к API AliExpress.
- **Параметры**:
  - `request` (IopRequest): Запрос, который необходимо выполнить.
- **Как работает**:
  - Выполняет запрос с использованием клиента `IopClient`.
  - Возвращает объект ответа `IopResponse`, содержащий информацию о результате выполнения запроса.
- **Примеры**:
  ```python
  response = client.execute(request)
  ```

### Обработка ответа

```python
print(response.body)
print(response.type)
print(response.code)
print(response.message)
print(response.request_id)
print(response.body)
```

- **Назначение**: Вывод информации об ответе API.
- **Параметры**:
  - `response` (IopResponse): Объект ответа, полученный от API.
- **Как работает**:
  - Выводит различные атрибуты ответа, такие как тело ответа, тип, код, сообщение и идентификатор запроса.
- **Примеры**:
  ```python
  print(response.body)
  print(response.type)
  print(response.code)
  print(response.message)
  print(response.request_id)
  print(response.body)
  ```

## Переменные

- `client`: Объект `IopClient`, используемый для выполнения запросов к API AliExpress.
- `request`: Объект `IopRequest`, представляющий запрос к API.
- `response`: Объект `IopResponse`, содержащий ответ от API.

## Дополнительная информация

Код также содержит закомментированные примеры других запросов и параметров, которые можно использовать для экспериментов с API AliExpress.
Обратите внимание на закомментированные строки, которые демонстрируют различные способы использования API, такие как установка параметров, выбор метода запроса (GET или POST) и упрощение ответа.