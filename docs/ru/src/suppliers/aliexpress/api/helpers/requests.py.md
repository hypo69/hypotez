# Модуль для выполнения API-запросов к AliExpress

## Обзор

Модуль `requests.py` содержит функции, необходимые для отправки и обработки API-запросов к AliExpress. Основная функция `api_request` выполняет запрос, обрабатывает возможные ошибки и возвращает результат.

## Подробнее

Этот модуль предназначен для упрощения взаимодействия с API AliExpress. Он предоставляет единую точку входа для выполнения запросов, автоматическую обработку ответов и логирование ошибок. Это помогает избежать дублирования кода и упрощает отладку.

## Функции

### `api_request`

```python
def api_request(request, response_name, attemps:int = 1) -> SimpleNamespace | None:
    """ Выполняет API-запрос, обрабатывает ответ и возвращает результат.

    Args:
        request: Объект запроса, содержащий детали запроса к API.
        response_name (str): Ключ, используемый для извлечения данных из ответа.
        attemps (int, optional): Количество попыток выполнения запроса. По умолчанию 1.

    Returns:
        SimpleNamespace | None: Результат запроса, представленный в виде объекта SimpleNamespace, или None в случае ошибки.

    Raises:
        ApiRequestException: Если при выполнении запроса возникает исключение.
        ApiRequestResponseException: Если ответ API содержит ошибку.

    **Внутренние функции**:
    В данной функции нет внутренних функций.

    **Как работает функция**:
     1. **Выполнение запроса**: Функция пытается выполнить запрос к API, используя метод `getResponse` объекта `request`.
     2. **Обработка исключений при запросе**: Если во время выполнения запроса возникает исключение, функция логирует критическую ошибку.
     3. **Обработка ответа**: Если запрос выполнен успешно, функция извлекает данные из ответа, используя предоставленное имя ответа (`response_name`).
     4. **Преобразование ответа**: Функция преобразует JSON-ответ в объект `SimpleNamespace` для удобного доступа к данным.
     5. **Обработка ошибок в ответе**: Если во время обработки ответа возникает исключение, функция логирует критическую ошибку.
     6. **Проверка кода ответа**: Функция проверяет код ответа (`resp_code`). Если код равен 200, возвращается результат.
     7. **Обработка предупреждений**: Если код ответа не равен 200, функция логирует предупреждение и возвращает `None`.
     8. **Обработка общих исключений**: Если возникает любое другое исключение, функция логирует ошибку и возвращает `None`.

    **ASCII flowchart**:

    ```
    Начало
    |
    -- Запрос к API --> Получение ответа
    |
    -- Обработка ответа --> Преобразование JSON в SimpleNamespace
    |
    -- Проверка кода ответа (200?)
    |
    Да -- Возврат результата
    |
    Нет -- Логирование предупреждения и возврат None
    |
    Конец
    ```

    **Примеры**:
    ```python
    # Пример вызова функции api_request с объектом запроса и именем ответа
    # (Предполагается, что request - это настроенный объект запроса)
    result = api_request(request, 'item_detail')
    if result:
        print(f'Результат запроса: {result}')
    else:
        print('Ошибка при выполнении запроса')
    ```
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