## Как использовать TeachAnything
=========================================================================================

### Описание
-------------------------
Класс `TeachAnything` предоставляет асинхронный генератор, который взаимодействует с API TeachAnything для получения ответов от модели. 
Он реализует интерфейс `AsyncGeneratorProvider` и использует `aiohttp` для отправки запросов к API.

### Шаги выполнения
-------------------------
1. **Создание экземпляра класса:** Создается экземпляр класса `TeachAnything` с помощью метода `create_async_generator`.
2. **Настройка параметров:** В метод `create_async_generator` передаются следующие параметры:
    - `model`: Имя модели для использования (например, `gemini-1.5-pro`).
    - `messages`: Список сообщений для использования в качестве контекста для запроса.
    - `proxy`: (опционально) Прокси-сервер для использования при отправке запросов.
3. **Отправка запроса:** Метод `create_async_generator` формирует запрос к API TeachAnything с помощью `aiohttp` и отправляет его.
4. **Обработка ответа:** После получения ответа от API, метод `create_async_generator` преобразует поток байтов в текст, декодирует его с помощью `utf-8` и возвращает его в виде асинхронного генератора. 
5. **Обработка ошибок:** В случае ошибок, метод `create_async_generator` пытается обработать их, генерируя соответствующие исключения. 


### Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.TeachAnything import TeachAnything
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Привет, как дела?"},
    {"role": "assistant", "content": "Отлично, а у тебя как?"},
    {"role": "user", "content": "Тоже хорошо.  Расскажи мне анекдот."},
]

async def main():
    generator = await TeachAnything.create_async_generator(
        model="gemini-1.5-pro",
        messages=messages
    )
    async for chunk in generator:
        print(chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```