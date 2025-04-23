### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код определяет асинхронного провайдера `Acytoo` для взаимодействия с API `chat.acytoo.com`. Он использует `aiohttp` для отправки запросов и получения потоковых ответов, которые затем передаются как асинхронный генератор. Провайдер поддерживает модели `gpt-3.5-turbo` и может работать с историей сообщений.

Шаги выполнения
-------------------------
1. **Инициализация**: Создается класс `Acytoo`, который наследуется от `AsyncGeneratorProvider`. Указывается URL (`https://chat.acytoo.com`) и поддерживаемые возможности.
2. **Создание асинхронного генератора**: Метод `create_async_generator` создает асинхронный генератор, который отправляет POST-запрос к API и возвращает поток данных.
3. **Создание сессии**: Используется `aiohttp.ClientSession` для управления HTTP-соединением. Заголовки и payload создаются с помощью функций `_create_header` и `_create_payload`.
4. **Отправка запроса**: POST-запрос отправляется на URL `/api/completions` с использованием `session.post`. При этом используется прокси, если он указан.
5. **Обработка ответа**: Полученный ответ обрабатывается потоково через `response.content.iter_any()`. Каждый чанк данных декодируется и передается через `yield`, что делает функцию асинхронным генератором.
6. **Создание заголовков**: Функция `_create_header` создает заголовок для запроса, указывая `accept` и `content-type`.
7. **Создание payload**: Функция `_create_payload` создает JSON payload с параметрами, такими как модель, сообщения и температура.

Пример использования
-------------------------

```python
from aiohttp import ClientSession

from ...typing import AsyncResult, Messages
from ..base_provider import AsyncGeneratorProvider


class Acytoo(AsyncGeneratorProvider):
    url = 'https://chat.acytoo.com'
    working = False
    supports_message_history = True
    supports_gpt_35_turbo = True

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        async with ClientSession(
            headers=_create_header()
        ) as session:
            async with session.post(
                f'{cls.url}/api/completions',
                proxy=proxy,
                json=_create_payload(messages, **kwargs)
            ) as response:
                response.raise_for_status()
                async for stream in response.content.iter_any():
                    if stream:
                        yield stream.decode()


def _create_header():
    return {
        'accept': '*/*',
        'content-type': 'application/json',
    }


def _create_payload(messages: Messages, temperature: float = 0.5, **kwargs):
    return {
        'key': '',
        'model': 'gpt-3.5-turbo',
        'messages': messages,
        'temperature': temperature,
        'password': ''
    }

# Пример использования:
async def main():
    messages = [{"role": "user", "content": "Hello, Acytoo!"}]
    async for message in Acytoo.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(message, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())