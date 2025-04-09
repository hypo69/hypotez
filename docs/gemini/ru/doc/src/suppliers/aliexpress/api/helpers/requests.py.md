# Модуль для выполнения API-запросов к AliExpress

## Обзор

Модуль `requests.py` предназначен для упрощения выполнения API-запросов к AliExpress. Он содержит функцию `api_request`, которая выполняет запрос, обрабатывает ответ и возвращает результат. Модуль также обрабатывает исключения, которые могут возникнуть во время выполнения запроса или обработки ответа, и логирует ошибки.

## Подробней

Модуль обеспечивает стандартизированный способ взаимодействия с API AliExpress, включая обработку ошибок и логирование. Это позволяет упростить код, необходимый для получения данных от AliExpress API, и повысить надежность приложения.

## Функции

### `api_request`

**Назначение**: Выполняет API-запрос, обрабатывает ответ и возвращает результат.

**Параметры**:

- `request` (объект запроса): Объект, представляющий API-запрос. Ожидается, что у объекта есть метод `getResponse()`.
- `response_name` (str): Имя ключа в ответе, содержащего полезные данные.
- `attemps` (int, optional): Количество попыток выполнения запроса. По умолчанию `1`.

**Возвращает**:

- Объект `SimpleNamespace` с результатом, если запрос выполнен успешно и код ответа `200`.
- `None`, если произошла ошибка во время выполнения запроса или обработки ответа.

**Вызывает исключения**:

- `ApiRequestException`: Если произошла ошибка во время выполнения запроса.
- `ApiRequestResponseException`: Если произошла ошибка при обработке ответа.

**Как работает функция**:

1.  Функция пытается выполнить запрос с помощью метода `getResponse()` объекта `request`.
2.  Если во время выполнения запроса возникает исключение, функция пытается получить сообщение об ошибке из исключения и логирует его с использованием `logger.critical`. Возвращает `None`.
3.  Если запрос выполнен успешно, функция пытается извлечь данные из ответа, используя имя ответа `response_name`. Затем функция преобразует JSON-ответ в объект `SimpleNamespace` для удобного доступа к данным.
4.  Если во время обработки ответа возникает исключение, функция логирует сообщение об ошибке с использованием `logger.critical` и возвращает `None`.
5.  Если ответ содержит код `200`, функция возвращает результат `response.result`.
6.  Если ответ содержит код, отличный от `200`, функция логирует предупреждение с кодом ответа и сообщением об ошибке с использованием `logger.warning` и возвращает `None`.
7.  Если в процессе обработки ответа возникает исключение, функция логирует ошибку с использованием `logger.error` и возвращает `None`.

**Примеры**:

```python
from types import SimpleNamespace
import json
from src.logger.logger import logger

class MockRequest:
    def getResponse(self):
        # Имитация успешного ответа
        response_data = {
            "item_list_search": {
                "resp_result": {
                    "resp_code": 200,
                    "result": {"items": [{"id": 1, "name": "Product 1"}]}
                }
            }
        }
        return response_data

class MockRequestError:
    def getResponse(self):
        # Имитация ошибки при выполнении запроса
        raise Exception("Ошибка запроса")

# Пример успешного запроса
request = MockRequest()
response_name = "item_list_search"
result = api_request(request, response_name)
if result:
    print(result.items[0].name)  # Вывод: Product 1

# Пример обработки ошибки запроса
request_error = MockRequestError()
result = api_request(request_error, response_name)
if result is None:
    print("Произошла ошибка при выполнении запроса")  # Вывод: Произошла ошибка при выполнении запроса

# Пример обработки ответа с кодом ошибки
class MockRequestErrorResponse:
    def getResponse(self):
        # Имитация ответа с кодом ошибки
        response_data = {
            "item_list_search": {
                "resp_result": {
                    "resp_code": 500,
                    "resp_msg": "Внутренняя ошибка сервера"
                }
            }
        }
        return response_data
        
request_error_response = MockRequestErrorResponse()
result = api_request(request_error_response, response_name)
if result is None:
    print("Получен ответ с кодом ошибки")  # Вывод: Получен ответ с кодом ошибки