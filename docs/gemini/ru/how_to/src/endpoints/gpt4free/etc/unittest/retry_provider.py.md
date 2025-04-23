### Как использовать этот блок кода

=========================================================================================

Описание
-------------------------

Этот блок кода содержит набор юнит-тестов для класса `IterListProvider`, который предназначен для перебора списка провайдеров при запросах к API. Тесты проверяют различные сценарии, такие как пропуск неработающих провайдеров, обработка нескольких результатов и потоковая передача данных.

Шаги выполнения
-------------------------

1.  **Инициализация:** Создается класс `TestIterListProvider`, который наследуется от `unittest.IsolatedAsyncioTestCase`.

2.  **Тест `test_skip_provider`:**
    *   Создается `AsyncClient` с `IterListProvider`, который содержит `RaiseExceptionProviderMock` (который вызывает исключение) и `YieldProviderMock` (который возвращает результат "Hello").
    *   Вызывается метод `chat.completions.create` для получения ответа.
    *   Проверяется, что ответ является экземпляром `ChatCompletion` и содержит ожидаемый контент "Hello".

3.  **Тест `test_only_one_result`:**
    *   Создается `AsyncClient` с `IterListProvider`, который содержит два экземпляра `YieldProviderMock`.
    *   Вызывается метод `chat.completions.create` для получения ответа.
    *   Проверяется, что ответ является экземпляром `ChatCompletion` и содержит ожидаемый контент "Hello".

4.  **Тест `test_stream_skip_provider`:**
    *   Создается `AsyncClient` с `IterListProvider`, который содержит `AsyncRaiseExceptionProviderMock` (который асинхронно вызывает исключение) и `YieldProviderMock` (который возвращает результат).
    *   Создаются сообщения для потоковой передачи.
    *   Вызывается метод `chat.completions.create` с параметром `stream=True` для получения потокового ответа.
    *   В цикле перебираются чанки ответа и проверяется, что каждый чанк является экземпляром `ChatCompletionChunk` и содержит ожидаемый контент (строку).

5.  **Тест `test_stream_only_one_result`:**
    *   Создается `AsyncClient` с `IterListProvider`, который содержит два экземпляра `YieldProviderMock`.
    *   Создаются сообщения для потоковой передачи.
    *   Вызывается метод `chat.completions.create` с параметром `stream=True` и `max_tokens=2` для получения потокового ответа.
    *   Собираются все чанки ответа в список.
    *   Проверяется, что количество чанков равно 3, и каждый чанк содержит ожидаемый контент "You ".

6.  **Тест `test_skip_none`:**
    *   Создается `AsyncClient` с `IterListProvider`, который содержит `YieldNoneProviderMock` (который возвращает `None`) и `YieldProviderMock` (который возвращает результат "Hello").
    *   Вызывается метод `chat.completions.create` для получения ответа.
    *   Проверяется, что ответ является экземпляром `ChatCompletion` и содержит ожидаемый контент "Hello".

7.  **Тест `test_stream_skip_none`:**
    *   Создается `AsyncClient` с `IterListProvider`, который содержит `YieldNoneProviderMock` (который возвращает `None`) и `YieldProviderMock` (который возвращает результат "Hello").
    *   Вызывается метод `chat.completions.create` с параметром `stream=True` для получения потокового ответа.
    *   Собираются все чанки ответа в список.
    *   Проверяется, что количество чанков равно 2, и каждый чанк содержит ожидаемый контент "Hello".

Пример использования
-------------------------

```python
import unittest

from g4f.client import AsyncClient, ChatCompletion, ChatCompletionChunk
from g4f.providers.retry_provider import IterListProvider
from .mocks import YieldProviderMock, RaiseExceptionProviderMock, AsyncRaiseExceptionProviderMock, YieldNoneProviderMock

DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]

class TestIterListProvider(unittest.IsolatedAsyncioTestCase):

    async def test_skip_provider(self):
        # Создание клиента с провайдером IterListProvider, который перебирает RaiseExceptionProviderMock и YieldProviderMock
        client = AsyncClient(provider=IterListProvider([RaiseExceptionProviderMock, YieldProviderMock], False))
        # Запрос к чат-комплишену
        response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
        # Проверка, что получен корректный ответ
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("Hello", response.choices[0].message.content)