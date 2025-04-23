# Модуль для тестирования IOP-клиента AliExpress

## Обзор

Модуль `test_iop_get.py` предназначен для тестирования взаимодействия с API AliExpress через IOP (IopClient). В данном файле выполняются запросы к API для генерации партнерских ссылок и вывода информации об ответе, включая тело ответа, тип, код, сообщение об ошибке и уникальный идентификатор запроса.

## Подробнее

Этот модуль содержит примеры использования библиотеки `iop` для выполнения API-запросов к AliExpress. Он демонстрирует, как создать клиента IOP, сформировать запрос и обработать ответ. В частности, здесь показано, как генерировать партнерские ссылки на товары AliExpress и анализировать полученные данные.

## Функции

В данном файле не определены отдельные функции, однако он содержит примеры кода, демонстрирующие работу с IOP-клиентом.

## Пример использования

```python
import iop

# Создание IOP-клиента для взаимодействия с API AliExpress
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
print(response.body)  # Тело ответа
print(response.type)  # Тип ответа
print(response.code)  # Код ответа
print(response.message)  # Сообщение об ошибке
print(response.request_id)  # Уникальный идентификатор запроса
print(response.body)  # Полное тело ответа
```

## Переменные

- `client`: Инстанс класса `IopClient`, используемый для взаимодействия с API AliExpress.
- `request`: Инстанс класса `IopRequest`, представляющий запрос к API AliExpress.
- `response`: Результат выполнения запроса, содержащий информацию об ответе от API.

```python
import iop

# Создание IOP-клиента для взаимодействия с API AliExpress
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
print(response.body)  # Тело ответа
print(response.type)  # Тип ответа
print(response.code)  # Код ответа
print(response.message)  # Сообщение об ошибке
print(response.request_id)  # Уникальный идентификатор запроса
print(response.body)  # Полное тело ответа
```

### `iop.IopClient`

   **Описание**: Класс для взаимодействия с API AliExpress через IOP.

   **Параметры**:
   - `url` (str): URL API.
   - `appkey` (str): Ключ приложения.
   - `appSecret` (str): Секрет приложения.

   **Принцип работы**:

    - `IopClient` инициализируется с URL, ключом приложения и секретом.
    - `log_level` устанавливается для отладки.
    - Создается `IopRequest` с указанием метода API (`aliexpress.affiliate.link.generate`).
    - Добавляются параметры запроса, такие как `promotion_link_type`, `source_values` и `tracking_id`.
    - Выполняется запрос с помощью `client.execute(request)`.
    - Выводятся различные атрибуты ответа, такие как тело, тип, код, сообщение и ID запроса.

### `iop.IopRequest`

   **Описание**: Класс для формирования запросов к API AliExpress.

   **Параметры**:
   - `method` (str): Метод API, который будет вызван.

   **Принцип работы**:

    - `IopRequest` инициализируется с указанием метода API.
    - Параметры добавляются с помощью `add_api_param`.
    - Запрос передается в `client.execute` для выполнения.