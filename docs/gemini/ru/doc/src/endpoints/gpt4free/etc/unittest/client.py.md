# Модуль `client` - Тестирование клиента

## Обзор

Этот модуль содержит набор тестов для проверки функциональности клиента `g4f`. 
Он использует моки для имитации поведения различных провайдеров AI-моделей и проверки работы 
методов `Client` и `AsyncClient` при взаимодействии с ними.

## Подробнее

В модуле реализованы тесты для следующих функциональных блоков:

- Создание и проверка `ChatCompletion` при использовании моков в качестве провайдеров AI-моделей
- Работа с `max_tokens` и `stream` в методах `chat.completions.create`
- Обработка ситуации, когда модель не найдена (с использованием `ModelNotFoundError`)
- Получение модели и провайдера для различных сценариев (с использованием `get_model_and_provider`)

## Классы

### `AsyncTestPassModel`

**Описание**: Класс для тестирования асинхронных функций клиента с использованием моков.

**Наследует**: `unittest.IsolatedAsyncioTestCase`

**Методы**:

- `test_response()`: Проверяет правильную работу асинхронного клиента при получении ответа от модели.
- `test_pass_model()`: Проверяет передачу модели в клиент.
- `test_max_tokens()`: Проверяет правильную работу `max_tokens` в методе `chat.completions.create`.
- `test_max_stream()`: Проверяет правильную работу потоковой передачи (streaming) ответов.
- `test_stop()`: Проверяет работу параметра `stop` в методе `chat.completions.create`.

### `TestPassModel`

**Описание**: Класс для тестирования синхронных функций клиента с использованием моков.

**Наследует**: `unittest.TestCase`

**Методы**:

- `test_response()`: Проверяет правильную работу клиента при получении ответа от модели.
- `test_pass_model()`: Проверяет передачу модели в клиент.
- `test_max_tokens()`: Проверяет правильную работу `max_tokens` в методе `chat.completions.create`.
- `test_max_stream()`: Проверяет правильную работу потоковой передачи (streaming) ответов.
- `test_stop()`: Проверяет работу параметра `stop` в методе `chat.completions.create`.
- `test_model_not_found()`: Проверяет правильное возникновение ошибки `ModelNotFoundError`, когда модель не найдена.
- `test_best_provider()`: Проверяет получение модели и провайдера для модели, не являющейся стандартной.
- `test_default_model()`: Проверяет получение модели и провайдера для стандартной модели.
- `test_provider_as_model()`: Проверяет получение модели и провайдера, когда модель задана в виде имени провайдера.
- `test_get_model()`: Проверяет получение модели и провайдера по имени модели.


## Параметры

- `DEFAULT_MESSAGES`: Список сообщений по умолчанию, используемых в тестах.

## Примеры

```python
from __future__ import annotations

import unittest

from g4f.errors import ModelNotFoundError
from g4f.client import Client, AsyncClient, ChatCompletion, ChatCompletionChunk, get_model_and_provider
from g4f.Provider.Copilot import Copilot
from g4f.models import gpt_4o
from .mocks import AsyncGeneratorProviderMock, ModelProviderMock, YieldProviderMock

DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]

class AsyncTestPassModel(unittest.IsolatedAsyncioTestCase):

    async def test_response(self):
        """
        Проверяет правильную работу асинхронного клиента при получении ответа от модели.
        """
        client = AsyncClient(provider=AsyncGeneratorProviderMock)
        response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("Mock", response.choices[0].message.content)

    async def test_pass_model(self):
        """
        Проверяет передачу модели в клиент.
        """
        client = AsyncClient(provider=ModelProviderMock)
        response = await client.chat.completions.create(DEFAULT_MESSAGES, "Hello")
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("Hello", response.choices[0].message.content)

    async def test_max_tokens(self):
        """
        Проверяет правильную работу `max_tokens` в методе `chat.completions.create`.
        """
        client = AsyncClient(provider=YieldProviderMock)
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        response = await client.chat.completions.create(messages, "Hello", max_tokens=1)
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("How ", response.choices[0].message.content)
        response = await client.chat.completions.create(messages, "Hello", max_tokens=2)
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("How are ", response.choices[0].message.content)

    async def test_max_stream(self):
        """
        Проверяет правильную работу потоковой передачи (streaming) ответов.
        """
        client = AsyncClient(provider=YieldProviderMock)
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        response = client.chat.completions.create(messages, "Hello", stream=True)
        async for chunk in response:
            chunk: ChatCompletionChunk = chunk
            self.assertIsInstance(chunk, ChatCompletionChunk)
            if chunk.choices[0].delta.content is not None:
                self.assertIsInstance(chunk.choices[0].delta.content, str)
        messages = [{'role': 'user', 'content': chunk} for chunk in ["You ", "You ", "Other", "?"]]
        response = client.chat.completions.create(messages, "Hello", stream=True, max_tokens=2)
        response_list = []
        async for chunk in response:
            response_list.append(chunk)
        self.assertEqual(len(response_list), 3)
        for chunk in response_list:
            if chunk.choices[0].delta.content is not None:
                self.assertEqual(chunk.choices[0].delta.content, "You ")

    async def test_stop(self):
        """
        Проверяет работу параметра `stop` в методе `chat.completions.create`.
        """
        client = AsyncClient(provider=YieldProviderMock)
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        response = await client.chat.completions.create(messages, "Hello", stop=["and"])
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("How are you?", response.choices[0].message.content)

class TestPassModel(unittest.TestCase):

    def test_response(self):
        """
        Проверяет правильную работу клиента при получении ответа от модели.
        """
        client = Client(provider=AsyncGeneratorProviderMock)
        response = client.chat.completions.create(DEFAULT_MESSAGES, "")
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("Mock", response.choices[0].message.content)

    def test_pass_model(self):
        """
        Проверяет передачу модели в клиент.
        """
        client = Client(provider=ModelProviderMock)
        response = client.chat.completions.create(DEFAULT_MESSAGES, "Hello")
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("Hello", response.choices[0].message.content)

    def test_max_tokens(self):
        """
        Проверяет правильную работу `max_tokens` в методе `chat.completions.create`.
        """
        client = Client(provider=YieldProviderMock)
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        response = client.chat.completions.create(messages, "Hello", max_tokens=1)
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("How ", response.choices[0].message.content)
        response = client.chat.completions.create(messages, "Hello", max_tokens=2)
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("How are ", response.choices[0].message.content)

    def test_max_stream(self):
        """
        Проверяет правильную работу потоковой передачи (streaming) ответов.
        """
        client = Client(provider=YieldProviderMock)
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        response = client.chat.completions.create(messages, "Hello", stream=True)
        for chunk in response:
            self.assertIsInstance(chunk, ChatCompletionChunk)
            if chunk.choices[0].delta.content is not None:
                self.assertIsInstance(chunk.choices[0].delta.content, str)
        messages = [{'role': 'user', 'content': chunk} for chunk in ["You ", "You ", "Other", "?"]]
        response = client.chat.completions.create(messages, "Hello", stream=True, max_tokens=2)
        response_list = list(response)
        self.assertEqual(len(response_list), 3)
        for chunk in response_list:
            if chunk.choices[0].delta.content is not None:
                self.assertEqual(chunk.choices[0].delta.content, "You ")

    def test_stop(self):
        """
        Проверяет работу параметра `stop` в методе `chat.completions.create`.
        """
        client = Client(provider=YieldProviderMock)
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        response = client.chat.completions.create(messages, "Hello", stop=["and"])
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("How are you?", response.choices[0].message.content)

    def test_model_not_found(self):
        """
        Проверяет правильное возникновение ошибки `ModelNotFoundError`, когда модель не найдена.
        """
        def run_exception():
            client = Client()
            client.chat.completions.create(DEFAULT_MESSAGES, "Hello")
        self.assertRaises(ModelNotFoundError, run_exception)

    def test_best_provider(self):
        """
        Проверяет получение модели и провайдера для модели, не являющейся стандартной.
        """
        not_default_model = "gpt-4o"
        model, provider = get_model_and_provider(not_default_model, None, False)
        self.assertTrue(hasattr(provider, "create_completion"))
        self.assertEqual(model, not_default_model)

    def test_default_model(self):
        """
        Проверяет получение модели и провайдера для стандартной модели.
        """
        default_model = ""
        model, provider = get_model_and_provider(default_model, None, False)
        self.assertTrue(hasattr(provider, "create_completion"))
        self.assertEqual(model, default_model)

    def test_provider_as_model(self):
        """
        Проверяет получение модели и провайдера, когда модель задана в виде имени провайдера.
        """
        provider_as_model = Copilot.__name__
        model, provider = get_model_and_provider(provider_as_model, None, False)
        self.assertTrue(hasattr(provider, "create_completion"))
        self.assertIsInstance(model, str)
        self.assertEqual(model, Copilot.default_model)

    def test_get_model(self):
        """
        Проверяет получение модели и провайдера по имени модели.
        """
        model, provider = get_model_and_provider(gpt_4o.name, None, False)
        self.assertTrue(hasattr(provider, "create_completion"))
        self.assertEqual(model, gpt_4o.name)

if __name__ == '__main__':
    unittest.main()

```

## Внутренние функции

### `get_model_and_provider`

**Назначение**: Эта функция определяет модель и соответствующего провайдера 
на основе заданных параметров.

**Параметры**:

- `model`: Имя модели или провайдера.
- `config`: Конфигурационный файл (не используется).
- `get_from_default_provider`: Флаг, указывающий, нужно ли искать модель в стандартном провайдере.

**Возвращает**:

- `model`: Имя модели.
- `provider`:  Провайдер AI-модели.

**Как работает функция**:

- Если модель задана в виде имени провайдера, функция извлекает модель из атрибута `default_model` провайдера.
- Если модель не задана, используется значение по умолчанию ("").
- В противном случае функция проверяет наличие модели в стандартном провайдере и возвращает модель и соответствующий провайдер.

**Примеры**:

```python
from g4f.models import gpt_4o
from g4f.Provider.Copilot import Copilot

model, provider = get_model_and_provider(gpt_4o.name, None, False)
# model = "gpt-4o"
# provider = <Провайдер для модели gpt-4o>

model, provider = get_model_and_provider(Copilot.__name__, None, False)
# model = "gpt-4o"
# provider = <Провайдер для модели Copilot>

model, provider = get_model_and_provider("", None, False)
# model = ""
# provider = <Стандартный провайдер>
```

## Внутренние функции

### `test_model_not_found`

**Назначение**: Эта функция проверяет правильное возникновение ошибки `ModelNotFoundError`, 
когда модель не найдена.

**Как работает функция**:

- Создает экземпляр класса `Client` без указания модели.
- Вызывает метод `chat.completions.create`, который должен вызвать ошибку, 
поскольку модель не задана.
- Проверяет, что функция `assertRaises` была вызвана с ожидаемой ошибкой.

**Примеры**:

```python
from g4f.errors import ModelNotFoundError

def run_exception():
    client = Client()
    client.chat.completions.create(DEFAULT_MESSAGES, "Hello")
self.assertRaises(ModelNotFoundError, run_exception)