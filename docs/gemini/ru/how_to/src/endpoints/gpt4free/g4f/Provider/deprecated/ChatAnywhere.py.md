## Как использовать класс `ChatAnywhere`
=========================================================================================

Описание
-------------------------
Класс `ChatAnywhere` предоставляет асинхронный генератор для общения с моделью GPT через API chatanywhere.cn. Он использует библиотеку `aiohttp` для отправки запросов и получения ответов от API.

Шаги выполнения
-------------------------
1. **Создание экземпляра класса**: Создайте объект `ChatAnywhere` с помощью метода `create_async_generator`.
2. **Передача параметров**: Передайте в метод следующие параметры:
    - `model`: Название модели, например, `gpt-3.5-turbo`.
    - `messages`: Список сообщений для отправки в чат.
    - `proxy`: (Необязательно) Прокси-сервер для использования.
    - `timeout`: (Необязательно) Таймаут для запросов.
    - `temperature`: (Необязательно) Температура модели, влияющая на креативность ответов.
3. **Получение асинхронного генератора**: Метод `create_async_generator` возвращает объект `AsyncResult`. Используйте его для итерации по ответам от модели.
4. **Обработка ответов**: Каждый итерационный шаг генератора `AsyncResult` возвращает строку, содержащую ответ от модели.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.ChatAnywhere import ChatAnywhere
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Привет, как дела?"},
]

async def main():
    """
    Пример использования ChatAnywhere
    """
    async with ChatAnywhere.create_async_generator(
        model="gpt-3.5-turbo", 
        messages=messages
    ) as response_generator:
        async for response in response_generator:
            print(f"Модель ответила: {response}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Важно**: Класс `ChatAnywhere` помечен как "deprecated" (устаревший), так как API chatanywhere.cn может быть нестабильным или недоступным.