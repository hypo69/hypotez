## \file hypotez/src/endpoints/gpt4free/etc/unittest/retry_provider.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль содержит модульные тесты для проверки функциональности IterListProvider.
==============================================================================

Этот модуль тестирует поведение IterListProvider при различных сценариях,
включая пропуск провайдеров, возвращающих исключения или None,
а также обработку потоковых ответов.

"""

## Оглавление
- [Обзор](#обзор)
- [Более подробно](#более-подробно)
- [Классы](#классы)
    - [TestIterListProvider](#testiterlistprovider)
        - [test_skip_provider](#test_skip_provider)
        - [test_only_one_result](#test_only_one_result)
        - [test_stream_skip_provider](#test_stream_skip_provider)
        - [test_stream_only_one_result](#test_stream_only_one_result)
        - [test_skip_none](#test_skip_none)
        - [test_stream_skip_none](#test_stream_skip_none)

## Обзор

Модуль предоставляет набор модульных тестов для проверки логики повторных попыток
с различными провайдерами, включая моки, которые возвращают исключения, значения None или корректные результаты.

## Более подробно

Этот код используется для тестирования механизма повторных попыток при работе с несколькими провайдерами.
Он проверяет, что IterListProvider правильно обрабатывает ситуации, когда один или несколько провайдеров
возвращают ошибку или None, и переключается на следующего провайдера в списке.

## Классы

### `TestIterListProvider`

**Описание**:
Класс, содержащий асинхронные тесты для проверки IterListProvider.

**Наследует**:
`unittest.IsolatedAsyncioTestCase` - базовый класс для написания асинхронных тестов.

**Атрибуты**:
- `DEFAULT_MESSAGES (List[Dict[str, str]])`: Список сообщений по умолчанию для использования в тестах.

**Принцип работы**:
Класс определяет несколько асинхронных тестов, которые создают экземпляры AsyncClient с IterListProvider,
настроенным с различными мок-провайдерами. Каждый тест проверяет определенный сценарий,
например, пропуск провайдера, возвращающего исключение, или обработку потоковых ответов.

**Методы**:
- `test_skip_provider`: Проверяет, что IterListProvider пропускает провайдера, возвращающего исключение, и использует следующего провайдера.
- `test_only_one_result`: Проверяет, что IterListProvider использует только одного провайдера, даже если их несколько.
- `test_stream_skip_provider`: Проверяет, что IterListProvider пропускает провайдера, возвращающего исключение при потоковой передаче, и использует следующего провайдера.
- `test_stream_only_one_result`: Проверяет, что IterListProvider корректно обрабатывает потоковые ответы только от одного провайдера.
- `test_skip_none`: Проверяет, что IterListProvider пропускает провайдера, возвращающего None, и использует следующего провайдера.
- `test_stream_skip_none`: Проверяет, что IterListProvider пропускает провайдера, возвращающего None при потоковой передаче, и использует следующего провайдера.

#### `test_skip_provider`

```python
async def test_skip_provider(self):
    """
    Проверяет, что IterListProvider пропускает провайдера, возвращающего исключение, и использует следующего провайдера.

    Args:
        self (TestIterListProvider): Экземпляр класса TestIterListProvider.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.
    """
```

**Как работает**:

- Создается экземпляр `AsyncClient` с `IterListProvider`, который настроен на использование `RaiseExceptionProviderMock` (который вызывает исключение) и `YieldProviderMock` (который возвращает строку "Hello").
- Вызывается метод `client.chat.completions.create` для получения ответа.
- Проверяется, что ответ является экземпляром `ChatCompletion` и что содержимое сообщения равно "Hello", что указывает на то, что был использован `YieldProviderMock`.

**Пример**:

```python
client = AsyncClient(provider=IterListProvider([RaiseExceptionProviderMock, YieldProviderMock], False))
response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
self.assertIsInstance(response, ChatCompletion)
self.assertEqual("Hello", response.choices[0].message.content)
```

#### `test_only_one_result`

```python
async def test_only_one_result(self):
    """
    Проверяет, что IterListProvider использует только одного провайдера, даже если их несколько.

    Args:
        self (TestIterListProvider): Экземпляр класса TestIterListProvider.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.
    """
```

**Как работает**:

- Создается экземпляр `AsyncClient` с `IterListProvider`, который настроен на использование двух экземпляров `YieldProviderMock` (оба возвращают строку "Hello").
- Вызывается метод `client.chat.completions.create` для получения ответа.
- Проверяется, что ответ является экземпляром `ChatCompletion` и что содержимое сообщения равно "Hello", что указывает на то, что был использован `YieldProviderMock`.

**Пример**:

```python
client = AsyncClient(provider=IterListProvider([YieldProviderMock, YieldProviderMock]))
response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
self.assertIsInstance(response, ChatCompletion)
self.assertEqual("Hello", response.choices[0].message.content)
```

#### `test_stream_skip_provider`

```python
async def test_stream_skip_provider(self):
    """
    Проверяет, что IterListProvider пропускает провайдера, возвращающего исключение при потоковой передаче, и использует следующего провайдера.

    Args:
        self (TestIterListProvider): Экземпляр класса TestIterListProvider.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.
    """
```

**Как работает**:

- Создается экземпляр `AsyncClient` с `IterListProvider`, который настроен на использование `AsyncRaiseExceptionProviderMock` (который вызывает исключение асинхронно) и `YieldProviderMock` (который возвращает строку "Hello").
- Создается список сообщений для потоковой передачи.
- Вызывается метод `client.chat.completions.create` для получения потокового ответа.
- Асинхронно перебираются чанки ответа и проверяется, что каждый чанк является экземпляром `ChatCompletionChunk` и что содержимое дельты не равно `None`, а также является строкой.

**Пример**:

```python
client = AsyncClient(provider=IterListProvider([AsyncRaiseExceptionProviderMock, YieldProviderMock], False))
messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
response = client.chat.completions.create(messages, "Hello", stream=True)
async for chunk in response:
    chunk: ChatCompletionChunk = chunk
    self.assertIsInstance(chunk, ChatCompletionChunk)
    if chunk.choices[0].delta.content is not None:
        self.assertIsInstance(chunk.choices[0].delta.content, str)
```

#### `test_stream_only_one_result`

```python
async def test_stream_only_one_result(self):
    """
    Проверяет, что IterListProvider корректно обрабатывает потоковые ответы только от одного провайдера.

    Args:
        self (TestIterListProvider): Экземпляр класса TestIterListProvider.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.
    """
```

**Как работает**:

- Создается экземпляр `AsyncClient` с `IterListProvider`, который настроен на использование двух экземпляров `YieldProviderMock` (оба возвращают строку "You ").
- Создается список сообщений для потоковой передачи.
- Вызывается метод `client.chat.completions.create` для получения потокового ответа с ограничением `max_tokens=2`.
- Асинхронно перебираются чанки ответа и добавляются в список `response_list`.
- Проверяется, что длина списка `response_list` равна 3 (ожидаемое количество чанков).
- Проверяется, что содержимое дельты каждого чанка (если оно не `None`) равно "You ".

**Пример**:

```python
client = AsyncClient(provider=IterListProvider([YieldProviderMock, YieldProviderMock], False))
messages = [{'role': 'user', 'content': chunk} for chunk in ["You ", "You "]]
response = client.chat.completions.create(messages, "Hello", stream=True, max_tokens=2)
response_list = []
async for chunk in response:
    response_list.append(chunk)
self.assertEqual(len(response_list), 3)
for chunk in response_list:
    if chunk.choices[0].delta.content is not None:
        self.assertEqual(chunk.choices[0].delta.content, "You ")
```

#### `test_skip_none`

```python
async def test_skip_none(self):
    """
    Проверяет, что IterListProvider пропускает провайдера, возвращающего None, и использует следующего провайдера.

    Args:
        self (TestIterListProvider): Экземпляр класса TestIterListProvider.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.
    """
```

**Как работает**:

- Создается экземпляр `AsyncClient` с `IterListProvider`, который настроен на использование `YieldNoneProviderMock` (который возвращает `None`) и `YieldProviderMock` (который возвращает строку "Hello").
- Вызывается метод `client.chat.completions.create` для получения ответа.
- Проверяется, что ответ является экземпляром `ChatCompletion` и что содержимое сообщения равно "Hello", что указывает на то, что был использован `YieldProviderMock`.

**Пример**:

```python
client = AsyncClient(provider=IterListProvider([YieldNoneProviderMock, YieldProviderMock], False))
response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
self.assertIsInstance(response, ChatCompletion)
self.assertEqual("Hello", response.choices[0].message.content)
```

#### `test_stream_skip_none`

```python
async def test_stream_skip_none(self):
    """
    Проверяет, что IterListProvider пропускает провайдера, возвращающего None при потоковой передаче, и использует следующего провайдера.

    Args:
        self (TestIterListProvider): Экземпляр класса TestIterListProvider.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.
    """
```

**Как работает**:

- Создается экземпляр `AsyncClient` с `IterListProvider`, который настроен на использование `YieldNoneProviderMock` (который возвращает `None`) и `YieldProviderMock` (который возвращает строку "Hello").
- Вызывается метод `client.chat.completions.create` для получения потокового ответа.
- Асинхронно перебираются чанки ответа и добавляются в список `response_list`.
- Проверяется, что длина списка `response_list` равна 2 (ожидаемое количество чанков).
- Проверяется, что содержимое дельты каждого чанка (если оно не `None`) равно "Hello".

**Пример**:

```python
client = AsyncClient(provider=IterListProvider([YieldNoneProviderMock, YieldProviderMock], False))
response = client.chat.completions.create(DEFAULT_MESSAGES, "", stream=True)
response_list = [chunk async for chunk in response]
self.assertEqual(len(response_list), 2)
for chunk in response_list:
    if chunk.choices[0].delta.content is not None:
        self.assertEqual(chunk.choices[0].delta.content, "Hello")