# Модуль `requests.py`

## Обзор

Модуль `requests.py` предназначен для выполнения API-запросов к AliExpress и обработки ответов. Он включает в себя функцию `api_request`, которая отправляет запрос, обрабатывает возможные ошибки и возвращает результат.

## Подробней

Этот модуль является частью подсистемы, взаимодействующей с API AliExpress. Он обеспечивает стандартизированный способ отправки запросов и обработки ответов, что упрощает интеграцию с API и уменьшает дублирование кода. Модуль использует логирование для записи ошибок и предупреждений, что помогает в отладке и мониторинге работы системы.

## Функции

### `api_request`

```python
def api_request(request, response_name: str, attemps: int = 1):
    """Выполняет API-запрос и обрабатывает ответ.

    Args:
        request: Объект запроса, содержащий информацию для выполнения API-запроса.
        response_name (str): Имя поля в ответе, содержащего результат.
        attemps (int): Количество попыток выполнения запроса. По умолчанию 1.

    Returns:
        object: Результат API-запроса в виде объекта `SimpleNamespace` или `None` в случае ошибки.

    Raises:
        ApiRequestException: Если возникает ошибка при выполнении запроса.
        ApiRequestResponseException: Если код ответа не равен 200.
    """
    try:
        response = request.getResponse()
    except Exception as error:           
        if hasattr(error, 'message'):
            #raise ApiRequestException(error.message) from error
            #logger.critical(error.message,pprint(error))
        #raise ApiRequestException(error) from error
        #logger.critical(error.message,pprint(error))
            ...    
            return 

    try:
        response = response[response_name]['resp_result']
        response = json.dumps(response)
        response = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
    except Exception as error:
        #raise ApiRequestResponseException(error) from error
        logger.critical(error.message, pprint(error), exc_info=False)
        return 
    try:
        if response.resp_code == 200:
            return response.result
        else:
            #raise ApiRequestResponseException(f'Response code {response.resp_code} - {response.resp_msg}')
            logger.warning(f'Response code {response.resp_code} - {response.resp_msg}',exc_info=False)
            return 
    except Exception as ex:
        logger.error(None, ex, exc_info=False)
        return 

```

#### Как работает функция `api_request`

1.  **Выполнение запроса**:
    *   Функция пытается выполнить API-запрос с помощью метода `getResponse()` объекта `request`.

2.  **Обработка исключений при выполнении запроса**:

    *   Если во время выполнения запроса возникает исключение, функция проверяет, содержит ли исключение атрибут `message`.

    *   В случае наличия сообщения об ошибке, функция логирует критическую ошибку, используя `logger.critical`, и возвращает `None`.

3.  **Обработка ответа**:

    *   После успешного выполнения запроса функция извлекает данные из ответа, используя `response_name` и ключ `resp_result`.

    *   Полученные данные преобразуются в JSON-строку, а затем обратно в объект `SimpleNamespace` для удобного доступа к атрибутам.

4.  **Обработка исключений при обработке ответа**:

    *   Если во время обработки ответа возникает исключение, функция логирует критическую ошибку с помощью `logger.critical` и возвращает `None`.

5.  **Проверка кода ответа**:

    *   Функция проверяет, равен ли код ответа `resp_code` значению 200.
    *   Если код ответа равен 200, функция возвращает результат `response.result`.
    *   Если код ответа не равен 200, функция логирует предупреждение, используя `logger.warning`, и возвращает `None`.

6.  **Обработка общих исключений**:

    *   Если на каком-либо этапе выполнения функции возникает необработанное исключение, функция логирует ошибку, используя `logger.error`, и возвращает `None`.

#### Параметры функции `api_request`

*   `request`: Объект запроса, который должен иметь метод `getResponse()` для выполнения API-запроса.
*   `response_name` (str): Имя поля в ответе, которое содержит полезные данные.
*   `attemps` (int, optional): Количество попыток выполнения запроса. По умолчанию равно 1.

#### Возвращаемое значение функции `api_request`

*   `object`: Если запрос выполнен успешно и код ответа равен 200, функция возвращает объект `response.result`.
*   `None`: Функция возвращает `None` в случае возникновения ошибки на любом этапе выполнения.

#### Примеры вызова функции `api_request`

```python
from types import SimpleNamespace
# Пример объекта request (предположим, что у него есть метод getResponse)
class MockRequest:
    def getResponse(self):
        # Имитация успешного ответа
        return {
            "items_search": {
                "resp_result": {
                    "resp_code": 200,
                    "result": {"item_list": [{"title": "test item"}]}
                }
            }
        }

# Пример использования функции api_request
request_object = MockRequest()
response = api_request(request_object, "items_search")
if response:
    print(response.item_list[0].title)  # Вывод: test item
else:
    print("Request failed")
```

```python
from types import SimpleNamespace
# Пример объекта request (предположим, что у него есть метод getResponse)
class MockRequest:
    def getResponse(self):
        # Имитация ответа с ошибкой
        return {
            "items_search": {
                "resp_result": {
                    "resp_code": 400,
                    "resp_msg": "Bad Request"
                }
            }
        }

# Пример использования функции api_request
request_object = MockRequest()
response = api_request(request_object, "items_search")
if response:
    print(response)
else:
    print("Request failed")  # Вывод: Request failed