# src.endpoints.gpt4free.g4f.Provider.hf_space.raise_for_status

## Обзор

Модуль содержит асинхронную функцию `raise_for_status`, которая проверяет статус HTTP-ответа и вызывает исключение `ResponseStatusError`, если статус не является успешным (200-299). Функция анализирует тело ответа, чтобы предоставить более информативное сообщение об ошибке, в частности, обрабатывая JSON-ответы и HTML-контент.

## Подробней

Этот модуль предназначен для обработки HTTP-ответов и проверки их статуса. Он используется для того, чтобы убедиться, что HTTP-запросы выполняются успешно, и в случае ошибки предоставить детальную информацию об ошибке, основываясь на содержимом ответа.

## Функции

### `raise_for_status`

**Назначение**: Проверяет статус HTTP-ответа и вызывает исключение `ResponseStatusError`, если статус не является успешным.

**Параметры**:
- `response` (Union[StreamResponse, ClientResponse]): Объект ответа, который может быть как `StreamResponse` (из `g4f.requests`), так и `ClientResponse` (из `aiohttp`).
- `message` (str, optional): Дополнительное сообщение об ошибке, которое будет использовано, если не удастся извлечь сообщение из тела ответа. По умолчанию `None`.

**Возвращает**:
- `None`: Функция ничего не возвращает, если ответ успешен.

**Вызывает исключения**:
- `ResponseStatusError`: Если статус ответа не является успешным.

**Как работает функция**:
1. Функция проверяет, является ли статус ответа успешным, используя `response.ok`.
2. Если статус ответа успешен, функция завершается, ничего не возвращая.
3. Если статус ответа не успешен, функция пытается извлечь более подробную информацию об ошибке из тела ответа.
4. Сначала проверяется `content-type` заголовка ответа. Если заголовок указывает на `application/json`, функция пытается распарсить JSON из тела ответа и извлечь сообщение об ошибке из полей `error` или `message`.
5. Если не удалось извлечь сообщение об ошибке из JSON, функция пытается прочитать тело ответа как текст.
6. Если `content-type` заголовка ответа указывает на `text/html` или тело ответа начинается с `<!DOCTYPE`, функция определяет, что содержимое является HTML, и устанавливает сообщение об ошибке как "HTML content".
7. Если ни один из предыдущих способов не дал результата, в качестве сообщения об ошибке используется текст тела ответа.
8. В конце вызывается исключение `ResponseStatusError` с сформированным сообщением об ошибке, которое включает статус ответа и детали об ошибке.

**Примеры**:

```python
from aiohttp import ClientResponse
from unittest.mock import AsyncMock

# Пример успешного ответа
async def test_raise_for_status_success():
    response = AsyncMock(spec=ClientResponse)
    response.ok = True
    await raise_for_status(response)
    assert True  # Если дошли до сюда, значит, исключение не было вызвано

# Пример ответа с JSON-ошибкой
async def test_raise_for_status_json_error():
    response = AsyncMock(spec=ClientResponse)
    response.ok = False
    response.status = 400
    response.headers = {"content-type": "application/json"}
    response.json.return_value = {"error": "Invalid request"}
    try:
        await raise_for_status(response)
    except ResponseStatusError as ex:
        assert str(ex) == "Response 400: Invalid request"

# Пример ответа с HTML-содержимым
async def test_raise_for_status_html_content():
    response = AsyncMock(spec=ClientResponse)
    response.ok = False
    response.status = 500
    response.headers = {"content-type": "text/html"}
    response.text.return_value = "<!DOCTYPE html><html><body><h1>Error</h1></body></html>"
    try:
        await raise_for_status(response)
    except ResponseStatusError as ex:
        assert str(ex) == "Response 500: HTML content"