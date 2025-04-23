### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Функция `raise_for_status` проверяет статус ответа от сервера и вызывает исключение, если статус указывает на ошибку. 
Она обрабатывает различные типы ответов (async/sync, aiohttp/requests) и специфические ошибки, такие как Cloudflare, OpenAI Bot Detection, Rate Limit и другие.

Шаги выполнения
-------------------------
1. **Проверка типа ответа**:
   - Функция проверяет, является ли `response` асинхронным (aiohttp) или синхронным (requests) ответом. Если `response` имеет атрибут `status`, то вызывается асинхронная версия `raise_for_status_async`.

2. **Асинхронная обработка `raise_for_status_async`**:
   - Если ответ успешен (`response.ok`), функция возвращается без ошибок.
   - Функция пытается получить сообщение об ошибке из тела ответа. Если `content-type` - `application/json`, то сообщение извлекается из JSON. Если `content-type` - `text/html` или ответ начинается с `<!DOCTYPE`, то сообщение берется как текст ответа.
   - Если статус ответа равен 401, вызывается исключение `MissingAuthError`.
   - Если статус ответа равен 403 и обнаружен Cloudflare, вызывается исключение `CloudflareError`.
   - Если статус ответа равен 403 и обнаружен OpenAI Bot, вызывается исключение `ResponseStatusError`.
   - Если статус ответа равен 502, вызывается исключение `ResponseStatusError` с сообщением "Bad Gateway".
   - Если статус ответа равен 504, вызывается исключение `RateLimitError` с сообщением "Gateway Timeout".
   - В противном случае вызывается исключение `ResponseStatusError` с кодом статуса и сообщением об ошибке.

3. **Синхронная обработка**:
   - Если ответ успешен (`response.ok`), функция возвращается без ошибок.
   - Функция проверяет, является ли ответ HTML-страницей.
   - Функция пытается получить сообщение об ошибке из тела ответа.
   - Если статус ответа равен 401, вызывается исключение `MissingAuthError`.
   - Если статус ответа равен 403 и обнаружен Cloudflare, вызывается исключение `CloudflareError`.
   - Если статус ответа равен 403 и обнаружен OpenAI Bot, вызывается исключение `ResponseStatusError`.
   - Если статус ответа равен 502, вызывается исключение `ResponseStatusError` с сообщением "Bad Gateway".
   - Если статус ответа равен 504, вызывается исключение `RateLimitError` с сообщением "Gateway Timeout".
   - В противном случае вызывается исключение `ResponseStatusError` с кодом статуса и сообщением об ошибке.

Пример использования
-------------------------

```python
from aiohttp import ClientSession
import asyncio

async def make_request(url: str):
    """
    Функция выполняет асинхронный HTTP-запрос и обрабатывает ответ.

    Args:
        url (str): URL для запроса.

    Returns:
        None

    Raises:
        ResponseStatusError: Если статус ответа не равен 200.
    """
    async with ClientSession() as session:
        async with session.get(url) as response:
            try:
                await raise_for_status_async(response)
                print(f"Request to {url} was successful!")
            except ResponseStatusError as e:
                print(f"Request to {url} failed: {e}")

async def main():
    """
    Основная асинхронная функция для демонстрации работы `make_request`.
    """
    await make_request("https://example.com")
    await make_request("https://example.com/nonexistent")  # Вызовет исключение

if __name__ == "__main__":
    asyncio.run(main())