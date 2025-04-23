### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Функция `raise_for_status` проверяет статус HTTP-ответа и генерирует исключение `ResponseStatusError` в случае ошибки. Она анализирует содержимое ответа для получения более конкретного сообщения об ошибке, особенно если ответ в формате JSON или HTML.

Шаги выполнения
-------------------------
1. **Проверка статуса ответа**: Функция проверяет, является ли статус ответа `ok`. Если статус в диапазоне 200-299, функция завершается без ошибок.
2. **Обработка JSON-ответа**: Если `content-type` заголовка начинается с `application/json`, функция пытается извлечь сообщение об ошибке из JSON-содержимого.
   - Сначала она пытается получить поле `error`, затем `message` из JSON.
   - Если сообщение содержит HTML-теги (например, ссылку), они удаляются.
3. **Обработка не-JSON-ответа**: Если ответ не в формате JSON или произошла ошибка при парсинге JSON:
   - Функция получает текстовое содержимое ответа.
   - Определяется, является ли ответ HTML, проверяя заголовок `content-type` или начало текста на наличие `<!DOCTYPE`.
   - Сообщение устанавливается как `"HTML content"`, если это HTML, или как текст ответа в противном случае.
4. **Генерация исключения**: Если статус ответа не `ok`, функция генерирует исключение `ResponseStatusError` с сообщением, включающим статус ответа и детали ошибки.

Пример использования
-------------------------

```python
from __future__ import annotations

from typing import Union
from aiohttp import ClientResponse

from ...errors import ResponseStatusError
from ...requests import StreamResponse

async def raise_for_status(response: Union[StreamResponse, ClientResponse], message: str = None):
    """
    Проверяет статус HTTP-ответа и вызывает исключение в случае ошибки.

    Args:
        response (Union[StreamResponse, ClientResponse]): HTTP-ответ для проверки.
        message (str, optional): Дополнительное сообщение об ошибке. Defaults to None.

    Raises:
        ResponseStatusError: Если статус ответа не OK.
    """
    if response.ok:
        return
    content_type = response.headers.get("content-type", "")
    if content_type.startswith("application/json"):
        try:
            data = await response.json()
            message = data.get("error", data.get("message", message))
            if message:
                message = message.split(" <a ")[0]
        except Exception:
            pass
    if not message:
        text = await response.text()
        is_html = response.headers.get("content-type", "").startswith("text/html") or text.startswith("<!DOCTYPE")
        message = "HTML content" if is_html else text
    raise ResponseStatusError(f"Response {response.status}: {message}")

async def process_response(response: ClientResponse):
    """
    Обрабатывает HTTP-ответ, проверяя статус и выводя сообщение об ошибке при необходимости.

    Args:
        response (ClientResponse): HTTP-ответ для обработки.
    """
    try:
        await raise_for_status(response, "Ошибка при выполнении запроса")
        data = await response.json()
        print("Данные:", data)
    except ResponseStatusError as e:
        print(f"Произошла ошибка: {e}")

# Пример вызова (требуется реальный HTTP-клиент и сервер для полноценной демонстрации)
# import aiohttp
# async def main():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('https://example.com/api/nonexistent') as response:
#             await process_response(response)