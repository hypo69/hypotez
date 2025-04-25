## Как использовать `raise_for_status` и `raise_for_status_async` 
=========================================================================================

Описание
-------------------------
Функции `raise_for_status` и `raise_for_status_async` проверяют статус ответа HTTP-запроса и генерируют соответствующее исключение, если статус не равен 200 (OK). 

Шаги выполнения
-------------------------
1. **Проверяет статус ответа**: Функции `raise_for_status` и `raise_for_status_async` проверяют статус ответа HTTP-запроса.
2. **Анализирует содержимое ответа**: Если статус ответа не равен 200 (OK), функции извлекают содержимое ответа, анализируют его тип (JSON или HTML) и определяют тип ошибки.
3. **Генерирует исключение**: В зависимости от статуса ответа и типа ошибки, функции генерируют соответствующее исключение:
    - `ResponseStatusError` - общая ошибка ответа.
    - `RateLimitError` - ошибка лимита запросов.
    - `MissingAuthError` - ошибка авторизации.
    - `CloudflareError` - ошибка, связанная с Cloudflare.
4. **Возвращает None**: Если статус ответа равен 200 (OK), функции ничего не делают и возвращают `None`.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.requests.raise_for_status import raise_for_status, raise_for_status_async

async def send_request_async(url: str, headers: dict = None) -> str:
    """Отправляет асинхронный HTTP-запрос и обрабатывает ответ."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            await raise_for_status_async(response) # Проверяем статус ответа
            return await response.text()

def send_request(url: str, headers: dict = None) -> str:
    """Отправляет синхронный HTTP-запрос и обрабатывает ответ."""
    response = requests.get(url, headers=headers)
    raise_for_status(response) # Проверяем статус ответа
    return response.text

# Пример использования
async def main():
    response_text = await send_request_async('https://example.com')
    print(response_text)

if __name__ == '__main__':
    asyncio.run(main())

```

### Дополнительная информация:
- Функция `raise_for_status_async` предназначена для асинхронных HTTP-запросов, а `raise_for_status` для синхронных.
- Функции анализируют содержимое ответа на наличие признаков ошибок, связанных с Cloudflare и OpenAI.
- Вы можете использовать функции `raise_for_status` и `raise_for_status_async` для обработки ошибок HTTP-ответов в ваших приложениях.