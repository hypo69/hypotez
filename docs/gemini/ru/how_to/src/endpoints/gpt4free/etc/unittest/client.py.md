Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код содержит набор модульных тестов для проверки функциональности асинхронного и синхронного клиентов, используемых для взаимодействия с различными поставщиками моделей, такими как GPT-4. Тесты охватывают различные аспекты, такие как получение ответов, передача моделей, обработка максимального количества токенов, потоковая передача и остановка генерации.

Шаги выполнения
-------------------------
1. **Инициализация клиента**: Создаются экземпляры `AsyncClient` и `Client` с использованием различных мок-провайдеров (`AsyncGeneratorProviderMock`, `ModelProviderMock`, `YieldProviderMock`).
2. **Тестирование ответов**: Проверяется, что клиент возвращает ожидаемые ответы (`ChatCompletion`) при использовании мок-провайдеров.
3. **Тестирование передачи моделей**: Убеждаемся, что клиент правильно передает информацию о модели и получает ответы на основе этой информации.
4. **Тестирование максимального количества токенов**: Проверяется, что клиент корректно обрабатывает ограничение на максимальное количество токенов в запросах.
5. **Тестирование потоковой передачи**: Убеждаемся, что клиент поддерживает потоковую передачу ответов и корректно обрабатывает чанки данных.
6. **Тестирование остановки генерации**: Проверяется, что клиент может остановить генерацию текста на основе заданных стоп-слов.
7. **Тестирование обработки ошибок**: Проверяется, что выбрасывается исключение `ModelNotFoundError`, когда запрошенная модель не найдена.
8. **Тестирование выбора провайдера**: Убеждаемся, что функция `get_model_and_provider` правильно выбирает модель и провайдера на основе входных параметров.

Пример использования
-------------------------

```python
import unittest

from g4f.errors import ModelNotFoundError
from g4f.client import Client, AsyncClient, ChatCompletion, ChatCompletionChunk, get_model_and_provider
from g4f.Provider.Copilot import Copilot
from g4f.models import gpt_4o
from .mocks import AsyncGeneratorProviderMock, ModelProviderMock, YieldProviderMock

DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]

class AsyncTestPassModel(unittest.IsolatedAsyncioTestCase):

    async def test_response(self):
        # Создание асинхронного клиента с мок-провайдером
        client = AsyncClient(provider=AsyncGeneratorProviderMock)
        # Выполнение запроса к чат-комплишену
        response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
        # Проверка, что получен ответ типа ChatCompletion
        self.assertIsInstance(response, ChatCompletion)
        # Проверка содержимого ответа
        self.assertEqual("Mock", response.choices[0].message.content)

    async def test_pass_model(self):
        # Создание асинхронного клиента с мок-провайдером модели
        client = AsyncClient(provider=ModelProviderMock)
        # Выполнение запроса к чат-комплишену с передачей сообщения
        response = await client.chat.completions.create(DEFAULT_MESSAGES, "Hello")
        # Проверка, что получен ответ типа ChatCompletion
        self.assertIsInstance(response, ChatCompletion)
        # Проверка содержимого ответа
        self.assertEqual("Hello", response.choices[0].message.content)

    async def test_max_tokens(self):
        # Создание асинхронного клиента с мок-провайдером, генерирующим чанки
        client = AsyncClient(provider=YieldProviderMock)
        # Формирование списка сообщений из чанков
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        # Выполнение запроса с ограничением на максимальное количество токенов (1)
        response = await client.chat.completions.create(messages, "Hello", max_tokens=1)
        # Проверка, что получен ответ типа ChatCompletion
        self.assertIsInstance(response, ChatCompletion)
        # Проверка содержимого ответа
        self.assertEqual("How ", response.choices[0].message.content)
        # Выполнение запроса с ограничением на максимальное количество токенов (2)
        response = await client.chat.completions.create(messages, "Hello", max_tokens=2)
        # Проверка, что получен ответ типа ChatCompletion
        self.assertIsInstance(response, ChatCompletion)
        # Проверка содержимого ответа
        self.assertEqual("How are ", response.choices[0].message.content)

    async def test_max_stream(self):
        # Создание асинхронного клиента с мок-провайдером, генерирующим чанки
        client = AsyncClient(provider=YieldProviderMock)
        # Формирование списка сообщений из чанков
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        # Выполнение запроса в режиме потоковой передачи
        response = client.chat.completions.create(messages, "Hello", stream=True)
        # Итерация по чанкам ответа
        async for chunk in response:
            # Приведение типа чанка
            chunk: ChatCompletionChunk = chunk
            # Проверка, что чанк является экземпляром ChatCompletionChunk
            self.assertIsInstance(chunk, ChatCompletionChunk)
            # Проверка, что содержимое чанка является строкой, если оно не None
            if chunk.choices[0].delta.content is not None:
                self.assertIsInstance(chunk.choices[0].delta.content, str)
        # Формирование другого списка сообщений из чанков
        messages = [{'role': 'user', 'content': chunk} for chunk in ["You ", "You ", "Other", "?"]]
        # Выполнение запроса в режиме потоковой передачи с ограничением на максимальное количество токенов (2)
        response = client.chat.completions.create(messages, "Hello", stream=True, max_tokens=2)
        # Сбор чанков в список
        response_list = []
        async for chunk in response:
            response_list.append(chunk)
        # Проверка количества чанков
        self.assertEqual(len(response_list), 3)
        # Проверка содержимого каждого чанка
        for chunk in response_list:
            if chunk.choices[0].delta.content is not None:
                self.assertEqual(chunk.choices[0].delta.content, "You ")

    async def test_stop(self):
        # Создание асинхронного клиента с мок-провайдером, генерирующим чанки
        client = AsyncClient(provider=YieldProviderMock)
        # Формирование списка сообщений из чанков
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        # Выполнение запроса с указанием стоп-слов
        response = await client.chat.completions.create(messages, "Hello", stop=["and"])
        # Проверка, что получен ответ типа ChatCompletion
        self.assertIsInstance(response, ChatCompletion)
        # Проверка содержимого ответа
        self.assertEqual("How are you?", response.choices[0].message.content)

class TestPassModel(unittest.TestCase):

    def test_response(self):
        # Создание синхронного клиента с мок-провайдером
        client = Client(provider=AsyncGeneratorProviderMock)
        # Выполнение запроса к чат-комплишену
        response = client.chat.completions.create(DEFAULT_MESSAGES, "")
        # Проверка, что получен ответ типа ChatCompletion
        self.assertIsInstance(response, ChatCompletion)
        # Проверка содержимого ответа
        self.assertEqual("Mock", response.choices[0].message.content)

    def test_pass_model(self):
        # Создание синхронного клиента с мок-провайдером модели
        client = Client(provider=ModelProviderMock)
        # Выполнение запроса к чат-комплишену с передачей сообщения
        response = client.chat.completions.create(DEFAULT_MESSAGES, "Hello")
        # Проверка, что получен ответ типа ChatCompletion
        self.assertIsInstance(response, ChatCompletion)
        # Проверка содержимого ответа
        self.assertEqual("Hello", response.choices[0].message.content)

    def test_max_tokens(self):
        # Создание синхронного клиента с мок-провайдером, генерирующим чанки
        client = Client(provider=YieldProviderMock)
        # Формирование списка сообщений из чанков
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        # Выполнение запроса с ограничением на максимальное количество токенов (1)
        response = client.chat.completions.create(messages, "Hello", max_tokens=1)
        # Проверка, что получен ответ типа ChatCompletion
        self.assertIsInstance(response, ChatCompletion)
        # Проверка содержимого ответа
        self.assertEqual("How ", response.choices[0].message.content)
        # Выполнение запроса с ограничением на максимальное количество токенов (2)
        response = client.chat.completions.create(messages, "Hello", max_tokens=2)
        # Проверка, что получен ответ типа ChatCompletion
        self.assertIsInstance(response, ChatCompletion)
        # Проверка содержимого ответа
        self.assertEqual("How are ", response.choices[0].message.content)

    def test_max_stream(self):
        # Создание синхронного клиента с мок-провайдером, генерирующим чанки
        client = Client(provider=YieldProviderMock)
        # Формирование списка сообщений из чанков
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        # Выполнение запроса в режиме потоковой передачи
        response = client.chat.completions.create(messages, "Hello", stream=True)
        # Итерация по чанкам ответа
        for chunk in response:
            # Проверка, что чанк является экземпляром ChatCompletionChunk
            self.assertIsInstance(chunk, ChatCompletionChunk)
            # Проверка, что содержимое чанка является строкой, если оно не None
            if chunk.choices[0].delta.content is not None:
                self.assertIsInstance(chunk.choices[0].delta.content, str)
        # Формирование другого списка сообщений из чанков
        messages = [{'role': 'user', 'content': chunk} for chunk in ["You ", "You ", "Other", "?"]]
        # Выполнение запроса в режиме потоковой передачи с ограничением на максимальное количество токенов (2)
        response = client.chat.completions.create(messages, "Hello", stream=True, max_tokens=2)
        # Сбор чанков в список
        response_list = list(response)
        # Проверка количества чанков
        self.assertEqual(len(response_list), 3)
        # Проверка содержимого каждого чанка
        for chunk in response_list:
            if chunk.choices[0].delta.content is not None:
                self.assertEqual(chunk.choices[0].delta.content, "You ")

    def test_stop(self):
        # Создание синхронного клиента с мок-провайдером, генерирующим чанки
        client = Client(provider=YieldProviderMock)
        # Формирование списка сообщений из чанков
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        # Выполнение запроса с указанием стоп-слов
        response = client.chat.completions.create(messages, "Hello", stop=["and"])
        # Проверка, что получен ответ типа ChatCompletion
        self.assertIsInstance(response, ChatCompletion)
        # Проверка содержимого ответа
        self.assertEqual("How are you?", response.choices[0].message.content)

    def test_model_not_found(self):
        # Определение функции для вызова исключения
        def run_exception():
            # Создание клиента без указания провайдера
            client = Client()
            # Попытка выполнения запроса к чат-комплишену
            client.chat.completions.create(DEFAULT_MESSAGES, "Hello")
        # Проверка, что выбрасывается исключение ModelNotFoundError
        self.assertRaises(ModelNotFoundError, run_exception)

    def test_best_provider(self):
        # Определение модели, отличной от дефолтной
        not_default_model = "gpt-4o"
        # Получение модели и провайдера
        model, provider = get_model_and_provider(not_default_model, None, False)
        # Проверка наличия атрибута create_completion у провайдера
        self.assertTrue(hasattr(provider, "create_completion"))
        # Проверка, что модель соответствует запрошенной
        self.assertEqual(model, not_default_model)

    def test_default_model(self):
        # Определение дефолтной модели
        default_model = ""
        # Получение модели и провайдера
        model, provider = get_model_and_provider(default_model, None, False)
        # Проверка наличия атрибута create_completion у провайдера
        self.assertTrue(hasattr(provider, "create_completion"))
        # Проверка, что модель соответствует дефолтной
        self.assertEqual(model, default_model)

    def test_provider_as_model(self):
        # Определение провайдера в качестве модели
        provider_as_model = Copilot.__name__
        # Получение модели и провайдера
        model, provider = get_model_and_provider(provider_as_model, None, False)
        # Проверка наличия атрибута create_completion у провайдера
        self.assertTrue(hasattr(provider, "create_completion"))
        # Проверка, что модель является строкой
        self.assertIsInstance(model, str)
        # Проверка, что модель соответствует дефолтной модели Copilot
        self.assertEqual(model, Copilot.default_model)

    def test_get_model(self):
        # Получение модели и провайдера для gpt_4o
        model, provider = get_model_and_provider(gpt_4o.name, None, False)
        # Проверка наличия атрибута create_completion у провайдера
        self.assertTrue(hasattr(provider, "create_completion"))
        # Проверка, что модель соответствует gpt_4o
        self.assertEqual(model, gpt_4o.name)

if __name__ == '__main__':
    unittest.main()