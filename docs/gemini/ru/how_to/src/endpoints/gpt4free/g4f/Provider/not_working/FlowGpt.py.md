## Как использовать FlowGpt
=========================================================================================

Описание
-------------------------
Данный код реализует класс `FlowGpt`, который является асинхронным генератором ответов от модели FlowGPT. Он позволяет взаимодействовать с разными моделями, в том числе GPT-3.5, GPT-4, Google Gemini и другими.

Шаги выполнения
-------------------------
1. **Инициализация**: Класс `FlowGpt` создается с использованием статического метода `create_async_generator()`.
2. **Параметры**: Метод принимает следующие параметры:
    - `model`:  Название модели, например "gpt-3.5-turbo", "gpt-4-turbo", "google-gemini".
    - `messages`: Список сообщений в формате `Messages` (см. документацию проекта).
    - `proxy`: Прокси-сервер для доступа к FlowGPT (опционально).
    - `temperature`: Параметр, влияющий на творческий потенциал модели (0.7 по умолчанию).
3. **Генерация ответов**: Метод возвращает асинхронный генератор `AsyncResult`, который по мере получения ответов от модели возвращает текст ответа.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.FlowGpt import FlowGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Привет! Как дела?"},
]

async def main():
    async for response in FlowGpt.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

```