# Модуль `requests.py`

## Обзор

Модуль `requests.py` предназначен для обработки API-запросов к AliExpress. Он содержит функцию `api_request`, которая выполняет запрос, обрабатывает возможные ошибки и возвращает результат в формате, удобном для дальнейшего использования.

## Подробнее

Модуль обрабатывает ответы от API AliExpress, преобразует их в объекты `SimpleNamespace` для удобного доступа к данным и логирует ошибки.
Он используется для централизованного выполнения API-запросов и обработки ответов, что упрощает взаимодействие с API AliExpress в других частях проекта.

## Функции

### `api_request`

**Назначение**: Выполняет API-запрос, обрабатывает ответ и возвращает результат.

```python
def api_request(request, response_name, attemps:int = 1):
    """ Функция выполняет API-запрос и обрабатывает ответ.

    Args:
        request: Объект запроса, содержащий метод `getResponse` для выполнения запроса.
        response_name (str): Ключ в ответе, содержащий полезные данные.
        attemps (int): Количество попыток выполнения запроса. По умолчанию 1.

    Returns:
        SimpleNamespace | None: Результат запроса в виде объекта SimpleNamespace или None в случае ошибки.

    Raises:
        ApiRequestException: Если во время выполнения запроса возникает исключение.
        ApiRequestResponseException: Если код ответа не равен 200.

    Внутренние функции:
    - нет
    """
```

**Параметры**:
- `request`: Объект запроса с методом `getResponse`.
- `response_name` (str): Ключ, используемый для извлечения данных из ответа.
- `attemps` (int): Количество попыток выполнения запроса.

**Возвращает**:
- `SimpleNamespace | None`: Результат запроса в виде объекта `SimpleNamespace` или `None` в случае ошибки.

**Как работает функция**:

1. **Выполнение запроса**:
   - Функция пытается получить ответ от API с помощью метода `getResponse` объекта `request`.

2. **Обработка ошибок запроса**:
   - Если во время выполнения запроса возникает исключение, функция логирует сообщение об ошибке и возвращает `None`.

3. **Обработка ответа**:
   - Функция извлекает данные из ответа, используя ключ `response_name`, и преобразует JSON-ответ в объект `SimpleNamespace` для упрощения доступа к данным.

4. **Проверка кода ответа**:
   - Функция проверяет код ответа `resp_code`. Если код равен 200, возвращается результат. В противном случае логируется предупреждение и возвращается `None`.

5. **Обработка исключений**:
   - Если во время обработки ответа или проверки кода ответа возникают исключения, функция логирует ошибку и возвращает `None`.

**Примеры**:

```python
# Пример использования функции api_request
from types import SimpleNamespace

class MockRequest:
    def getResponse(self):
        return {
            "item_search_v2_by_image": {
                "resp_result": '{"resp_code": 200, "result": {"items": [{"title": "Example"}]}}'
            }
        }

request = MockRequest()
response = api_request(request, "item_search_v2_by_image")
if response:
    print(response.items[0].title)  # Вывод: Example
```
```python
# Пример обработки ошибки при выполнении запроса
class MockRequestWithError:
    def getResponse(self):
        raise Exception("Request failed")

request = MockRequestWithError()
response = api_request(request, "item_search_v2_by_image")
print(response)  # Вывод: None
```
```python
# Пример обработки ошибки в ответе
class MockRequestWithBadResponse:
    def getResponse(self):
        return {
            "item_search_v2_by_image": {
                "resp_result": '{"resp_code": 500, "resp_msg": "Server error"}'
            }
        }

request = MockRequestWithBadResponse()
response = api_request(request, "item_search_v2_by_image")
print(response)  # Вывод: None
```