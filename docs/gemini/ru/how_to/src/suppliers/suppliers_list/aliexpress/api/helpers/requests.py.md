### **Инструкция по использованию блока кода `api_request`**

=========================================================================================

Описание
-------------------------
Функция `api_request` выполняет API-запрос, обрабатывает ответ и возвращает результат. Она принимает объект запроса, имя ожидаемого ответа и количество попыток выполнения запроса. В случае успеха возвращает результат из ответа, в противном случае логирует ошибки и возвращает `None`.

Шаги выполнения
-------------------------
1. **Выполнение запроса**:
   - Функция пытается выполнить API-запрос с помощью метода `getResponse()` объекта `request`.
   - Если во время выполнения запроса возникает исключение, функция логирует критическую ошибку и возвращает `None`.

2. **Обработка ответа**:
   - Извлекает данные из ответа, используя `response_name` и ключ `'resp_result'`.
   - Преобразует JSON-ответ в объект `SimpleNamespace` для удобного доступа к данным.

3. **Проверка кода ответа**:
   - Проверяет, равен ли код ответа `response.resp_code` значению `200`.
   - Если код ответа равен `200`, функция возвращает `response.result`.
   - Если код ответа не равен `200`, функция логирует предупреждение с кодом и сообщением ответа и возвращает `None`.

4. **Обработка исключений**:
   - Если во время обработки ответа или проверки кода ответа возникает исключение, функция логирует ошибку и возвращает `None`.

Пример использования
-------------------------

```python
from types import SimpleNamespace
import json
from src.logger.logger import logger
from src.utils.printer import pprint

def api_request(request, response_name, attemps:int = 1):
    """
    Выполняет API-запрос, обрабатывает ответ и возвращает результат.

    Args:
        request: Объект запроса с методом getResponse().
        response_name (str): Имя ожидаемого ответа.
        attemps (int): Количество попыток выполнения запроса.

    Returns:
        SimpleNamespace | None: Результат из ответа, если запрос успешен, иначе None.

    Raises:
        ApiRequestException: Если возникает ошибка при выполнении запроса.
        ApiRequestResponseException: Если возникает ошибка при обработке ответа.
    """
    try:
        response = request.getResponse()
    except Exception as error:
        logger.critical(f"Ошибка при выполнении запроса: {error}", exc_info=True)
        return None

    try:
        response = response[response_name]['resp_result']
        response = json.dumps(response)
        response = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
    except Exception as error:
        logger.critical(f"Ошибка при обработке ответа: {error}", exc_info=True)
        return None

    try:
        if response.resp_code == 200:
            return response.result
        else:
            logger.warning(f"Неудачный код ответа: {response.resp_code} - {response.resp_msg}")
            return None
    except Exception as ex:
        logger.error(f"Неизвестная ошибка: {ex}", exc_info=True)
        return None

# Пример использования
class MockRequest:
    def getResponse(self):
        # Эмулируем успешный ответ
        return {
            "test_response": {
                "resp_result": {
                    "resp_code": 200,
                    "result": {"data": "some data"}
                }
            }
        }

request_object = MockRequest()
result = api_request(request_object, "test_response")
if result:
    print(f"Результат: {result.data}")
else:
    print("Запрос не удался.")