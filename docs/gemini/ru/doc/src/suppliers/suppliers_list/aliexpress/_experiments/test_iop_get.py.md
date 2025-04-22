# Модуль для тестирования API IOP AliExpress

## Обзор

Модуль `test_iop_get.py` предназначен для тестирования взаимодействия с API AliExpress через протокол IOP. Он содержит примеры запросов к API для генерации партнерских ссылок и вывода информации об ответе.

## Подробней

Этот модуль демонстрирует, как использовать клиент IOP для выполнения запросов к API AliExpress. Он инициализирует клиент IOP с параметрами доступа, создает запрос API для генерации партнерской ссылки, выполняет запрос и выводит информацию об ответе, включая тело ответа, тип, код, сообщение об ошибке и уникальный идентификатор запроса.

## Функции

### `None`

В данном коде функции отсутствуют.

## Параметры

- `client`: Объект класса `iop.IopClient`, используемый для взаимодействия с API AliExpress.
    - `url` (str): URL API AliExpress.
    - `appkey` (str): Ключ приложения для доступа к API.
    - `appSecret` (str): Секрет приложения для доступа к API.
- `request`: Объект класса `iop.IopRequest`, представляющий запрос к API.
    - `method` (str): Метод API для вызова (например, `'aliexpress.affiliate.link.generate'`).
- `response`: Объект, содержащий ответ от API.
    - `.body` (str): Тело ответа.
    - `.type` (str): Тип ответа.
    - `.code` (int): Код ответа (0 означает отсутствие ошибки).
    - `.message` (str): Сообщение об ошибке.
    - `.request_id` (str): Уникальный идентификатор запроса.

## Примеры

### Пример запроса на генерацию партнерской ссылки:

```python
import iop

# Инициализация клиента IOP
client = iop.IopClient('https://api-sg.aliexpress.com/sync', '345846782', 'e1b26aac391d1bc3987732af93eb26aabc391d187732af93')
client.log_level = iop.P_LOG_LEVEL_DEBUG

# Создание запроса на генерацию партнерской ссылки
request = iop.IopRequest('aliexpress.affiliate.link.generate')
request.add_api_param('promotion_link_type', '0')
request.add_api_param('source_values', 'https://www.aliexpress.com/item/1005005058280371.html')
request.add_api_param('tracking_id', 'default')

# Выполнение запроса
response = client.execute(request)

# Вывод информации об ответе
print(response.body)
print(response.type)
print(response.code)
print(response.message)
print(response.request_id)
print(response.body)