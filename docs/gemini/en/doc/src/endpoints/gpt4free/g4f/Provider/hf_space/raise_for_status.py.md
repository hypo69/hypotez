# Модуль raise_for_status.py

## Обзор

Модуль содержит асинхронную функцию `raise_for_status`, предназначенную для проверки статуса HTTP-ответа и возбуждения исключения в случае ошибки. Она анализирует контент ответа для предоставления более информативного сообщения об ошибке.

## Подробнее

Этот модуль предоставляет функцию, которая проверяет, успешен ли HTTP-ответ. Если ответ не успешен, функция пытается извлечь сообщение об ошибке из тела ответа (если это JSON) или возвращает текстовое содержимое ответа. В конце возбуждается исключение `ResponseStatusError` с сообщением об ошибке.

## Функции

### `raise_for_status`

```python
async def raise_for_status(response: Union[StreamResponse, ClientResponse], message: str = None):
    """
    Проверяет статус HTTP-ответа и возбуждает исключение, если ответ содержит ошибку.

    Args:
        response (Union[StreamResponse, ClientResponse]): Объект HTTP-ответа, который необходимо проверить.
        message (str, optional): Дополнительное сообщение об ошибке. По умолчанию `None`.

    Raises:
        ResponseStatusError: Если HTTP-ответ не успешен.

    Пример:
        Примеры вызовов с полным диапазоном параметров, которые могут быть переданы в функцию.

    """
```

#### Параметры:

- `response` (Union[StreamResponse, ClientResponse]): Объект HTTP-ответа, который требуется проверить. Это может быть либо `StreamResponse`, либо `ClientResponse`.
- `message` (str, optional): Дополнительное сообщение об ошибке, которое можно передать. По умолчанию `None`.

#### Возвращает:

- Отсутствует. Функция ничего не возвращает при успешном выполнении.

#### Возбуждает:

- `ResponseStatusError`: Возбуждается, если `response.ok` имеет значение `False`.

#### Как работает функция:

1. **Проверка на успех**: Функция проверяет, успешен ли HTTP-ответ, анализируя атрибут `response.ok`. Если ответ успешен (код состояния в диапазоне 200-299), функция завершается без каких-либо действий.
2. **Анализ типа контента**: Если ответ не успешен, функция пытается получить тип контента из заголовков ответа. Если контент является JSON (`application/json`), функция пытается извлечь сообщение об ошибке из JSON-тела.
3. **Извлечение сообщения из JSON**: Если контент является JSON, функция пытается проанализировать JSON и извлечь сообщение об ошибке из полей `error` или `message` в JSON-данных.
4. **Получение текстового содержимого**: Если контент не является JSON или не удалось извлечь сообщение об ошибке из JSON, функция пытается получить текстовое содержимое ответа.
5. **Определение HTML-контента**: Если не удалось получить сообщение из JSON, функция проверяет, является ли контент HTML, анализируя заголовок `content-type` или начало текстового содержимого. Если контент является HTML, устанавливается сообщение `'HTML content'`.
6. **Возбуждение исключения**: В конце функция возбуждает исключение `ResponseStatusError` с сообщением, которое включает код состояния HTTP-ответа и сообщение об ошибке.

#### Примеры:

Примеры вызовов с полным диапазоном параметров, которые могут быть переданы в функцию.
```python
# Пример 1: Успешный ответ
response = MockResponse(status=200, ok=True)
await raise_for_status(response)  # Ничего не произойдет

# Пример 2: Ошибка с JSON-ответом
response = MockResponse(
    status=400,
    ok=False,
    headers={"content-type": "application/json"},
    json_data={"error": "Invalid request"}
)
try:
    await raise_for_status(response)
except ResponseStatusError as ex:
    print(ex)  # Выведет: Response 400: Invalid request

# Пример 3: Ошибка с HTML-ответом
response = MockResponse(
    status=500,
    ok=False,
    headers={"content-type": "text/html"},
    text="<!DOCTYPE html><html><body><h1>Error</h1></body></html>"
)
try:
    await raise_for_status(response)
except ResponseStatusError as ex:
    print(ex)  # Выведет: Response 500: HTML content

# Пример 4: Ошибка с текстовым ответом и дополнительным сообщением
response = MockResponse(
    status=404,
    ok=False,
    text="Not Found"
)
try:
    await raise_for_status(response, message="Custom message")
except ResponseStatusError as ex:
    print(ex)  # Выведет: Response 404: Custom message
```