Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода представляет собой реализацию асинхронного генератора ответов от провайдера Vitalentum, использующего GPT-3.5 Turbo. Он отправляет историю сообщений пользователя в API Vitalentum и возвращает сгенерированный контент в виде асинхронного генератора.

Шаги выполнения
-------------------------
1. **Подготовка заголовков**: Создаются заголовки HTTP-запроса, включающие User-Agent, Accept, Origin, Referer и Sec-Fetch параметры.
2. **Формирование данных**: История сообщений форматируется в JSON, где роль "user" преобразуется в "human", а "assistant" в "bot".
3. **Отправка запроса**: Асинхронно отправляется POST-запрос к API Vitalentum с использованием `ClientSession` из библиотеки `aiohttp`.
4. **Обработка ответа**: Ответ обрабатывается построчно, декодируется и извлекается контент из JSON-ответа, который затем передается через `yield` как часть асинхронного генератора.

Пример использования
-------------------------

```python
import asyncio

from src.endpoints.gpt4free.g4f.Provider.deprecated import Vitalentum
from src.endpoints.gpt4free.g4f.typing import Message

async def main():
    messages: list[Message] = [
        {"role": "user", "content": "Привет!"},
        {"role": "assistant", "content": "Здравствуйте! Как я могу вам помочь?"},
        {"role": "user", "content": "Расскажи мне о GPT-3."},
    ]

    async for content in Vitalentum.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(content, end="")

if __name__ == "__main__":
    asyncio.run(main())