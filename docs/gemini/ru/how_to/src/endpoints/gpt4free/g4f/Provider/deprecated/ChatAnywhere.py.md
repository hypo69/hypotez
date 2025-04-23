### Как использовать блок кода ChatAnywhere
=========================================================================================

Описание
-------------------------
Этот код определяет класс `ChatAnywhere`, который является асинхронным провайдером для взаимодействия с API `chatanywhere.cn`. Он поддерживает модель `gpt-3.5-turbo` и сохранение истории сообщений. Класс предоставляет метод `create_async_generator`, который создает асинхронный генератор для отправки сообщений и получения ответов от API.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются `ClientSession` и `ClientTimeout` из библиотеки `aiohttp` для выполнения асинхронных HTTP-запросов.
   - Импортируются `AsyncResult` и `Messages` из модуля `typing` для аннотации типов.
   - Импортируется `AsyncGeneratorProvider` из `..base_provider` для наследования базового класса провайдера.

2. **Определение класса `ChatAnywhere`**:
   - Устанавливается URL `chatanywhere.cn` в качестве базового адреса API.
   - Указывается, что провайдер поддерживает модель `gpt-3.5-turbo` и сохранение истории сообщений.
   - Поле `working` указывает на работоспособность класса.

3. **Создание асинхронного генератора `create_async_generator`**:
   - Метод `create_async_generator` принимает следующие аргументы:
     - `model` (str): Модель для использования.
     - `messages` (Messages): Список сообщений для отправки.
     - `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
     - `timeout` (int, optional): Время ожидания ответа в секундах. По умолчанию `120`.
     - `temperature` (float, optional): Температура для генерации ответов. По умолчанию `0.5`.
     - `**kwargs`: Дополнительные параметры.
   - Формируются заголовки HTTP-запроса, включая `User-Agent`, `Accept`, `Content-Type` и другие.
   - Создается асинхронная сессия `ClientSession` с заданными заголовками и временем ожидания.
   - Формируются данные для отправки в теле запроса в формате JSON, включая список сообщений, идентификатор, заголовок, температуру и модель.
   - Выполняется POST-запрос к API `chatanywhere.cn` с использованием асинхронной сессии и прокси-сервера (если указан).
   - Обрабатывается ответ от API, и асинхронно итерируются чанки данных.
   - Каждый полученный чанк декодируется и передается в генератор.

Пример использования
-------------------------

```python
from typing import List, Dict, AsyncGenerator

from src.endpoints.gpt4free.g4f.Provider.deprecated.ChatAnywhere import ChatAnywhere

async def main():
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Hello, how are you?"}
    ]

    async def print_response(generator: AsyncGenerator[str, None]):
        async for chunk in generator:
            print(chunk, end="")

    try:
        generator = await ChatAnywhere.create_async_generator(
            model="gpt-3.5-turbo",
            messages=messages,
            timeout=120,
            temperature=0.5
        )
        await print_response(generator)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())