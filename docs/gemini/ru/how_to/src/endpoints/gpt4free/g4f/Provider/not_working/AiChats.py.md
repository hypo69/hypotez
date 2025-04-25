## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Этот блок кода реализует класс `AiChats`, который представляет собой асинхронный провайдер для взаимодействия с API сервиса `ai-chats.org`. Он позволяет отправлять запросы в чат-бот, генерировать изображения с помощью DALL-E и получать ответы. 

### Шаги выполнения
-------------------------
1. **Инициализация класса:**  Создается экземпляр класса `AiChats` с использованием `AiChats()`.
2. **Выбор модели:** 
    - Для чата используйте модель `gpt-4`.
    - Для генерации изображений используйте модель `dalle`. 
3. **Отправка запросов:** Вызывается асинхронная функция `create_async` или `create_async_generator`:
    - `create_async` отправляет запрос и возвращает ответ в виде строки (для чата) или ссылки на изображение (для DALL-E).
    - `create_async_generator` отправляет запрос и возвращает генератор ответов. Это позволяет получить несколько ответов, если чат-бот выдает их постепенно.
4. **Формирование запроса:** 
    - В `create_async` и `create_async_generator` передаются параметры:
        - `model`: имя модели (gpt-4 или dalle).
        - `messages`: список сообщений в истории диалога.
        - `proxy`: прокси-сервер (опционально).
5. **Обработка ответов:** 
    - Для чата ответы получаются в виде строк.
    - Для DALL-E ответы получаются в виде объекта `ImageResponse`, который содержит ссылку на изображение в формате base64.

### Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AiChats import AiChats
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
from hypotez.src.endpoints.gpt4free.g4f.providers.response import ImageResponse

async def main():
    # Создаем экземпляр класса AiChats
    ai_chats = AiChats()

    # Отправка запроса в чат
    messages: Messages = [
        {"role": "user", "content": "Привет, как дела?"},
        {"role": "assistant", "content": "Хорошо, а у тебя?"},
        {"role": "user", "content": "Тоже отлично! Расскажи анекдот."},
    ]
    response = await ai_chats.create_async(model="gpt-4", messages=messages)
    print(response)

    # Генерация изображения с помощью DALL-E
    response = await ai_chats.create_async(model="dalle", messages=[{"role": "user", "content": "Кошка на луне"}] )
    if isinstance(response, ImageResponse):
        print(response.images[0])
    else:
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```