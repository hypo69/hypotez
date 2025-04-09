# Модуль для тестирования провайдера повторных попыток
=========================================================

Модуль содержит набор тестов для проверки функциональности `IterListProvider`, который позволяет последовательно использовать несколько провайдеров, пока один из них не вернет успешный результат.

## Обзор

Данный модуль содержит тесты для проверки логики переключения между провайдерами в `IterListProvider` в различных сценариях, включая случаи, когда провайдеры возвращают исключения или `None`. Он также проверяет корректность работы с потоковой передачей данных (streaming).

## Подробней

Этот файл находится в директории `hypotez/src/endpoints/gpt4free/etc/unittest` и содержит модульные тесты, использующие `unittest`. Он проверяет, как `IterListProvider` обрабатывает различные ситуации при работе с несколькими провайдерами, включая случаи, когда провайдеры выбрасывают исключения, возвращают `None` или успешно возвращают данные. Тесты охватывают как синхронные, так и асинхронные вызовы, а также потоковую передачу данных.

## Классы

### `TestIterListProvider`

**Описание**: Класс, содержащий набор асинхронных тестов для проверки работы `IterListProvider`.

**Наследует**:

- `unittest.IsolatedAsyncioTestCase`: Класс, предоставляющий структуру для написания асинхронных тестов.

**Методы**:

- `test_skip_provider`: Проверяет, что `IterListProvider` пропускает провайдера, выбрасывающего исключение, и использует следующего провайдера в списке.
- `test_only_one_result`: Проверяет, что `IterListProvider` использует только одного провайдера из списка, если он успешно возвращает результат.
- `test_stream_skip_provider`: Проверяет, что `IterListProvider` пропускает провайдера, выбрасывающего исключение при потоковой передаче данных, и использует следующего провайдера.
- `test_stream_only_one_result`: Проверяет, что при потоковой передаче данных используется только один провайдер из списка, если он успешно возвращает результат.
- `test_skip_none`: Проверяет, что `IterListProvider` пропускает провайдера, возвращающего `None`, и использует следующего провайдера в списке.
- `test_stream_skip_none`: Проверяет, что `IterListProvider` пропускает провайдера, возвращающего `None` при потоковой передаче данных, и использует следующего провайдера.

## Функции

### `test_skip_provider`

```python
async def test_skip_provider(self):
    """Проверяет, что IterListProvider пропускает провайдера, выбрасывающего исключение, и использует следующего провайдера в списке.

    Args:
        self (TestIterListProvider): Экземпляр класса TestIterListProvider.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.
    """
    ...
```

**Назначение**: Проверяет, что `IterListProvider` корректно обрабатывает ситуацию, когда один из провайдеров выбрасывает исключение. В этом случае, `IterListProvider` должен пропустить этого провайдера и попытаться использовать следующего провайдера в списке.

**Как работает функция**:

1.  **Инициализация клиента**: Создается экземпляр `AsyncClient` с `IterListProvider`, который настроен на использование `RaiseExceptionProviderMock` (который выбрасывает исключение) и `YieldProviderMock` (который возвращает успешный результат). Параметр `False` указывает, что исключения должны быть проигнорированы.
2.  **Вызов API**: Вызывается метод `client.chat.completions.create` с предопределенными сообщениями (`DEFAULT_MESSAGES`) и пустой строкой.
3.  **Проверка результата**: Проверяется, что возвращенный результат является экземпляром `ChatCompletion` и что содержимое сообщения соответствует ожидаемому значению "Hello", которое возвращает `YieldProviderMock`.

**ASCII Flowchart**:

```
A[Инициализация AsyncClient с IterListProvider([RaiseExceptionProviderMock, YieldProviderMock])]
|
B[Вызов client.chat.completions.create(DEFAULT_MESSAGES, "")]
|
C[Проверка, что полученный ответ - экземпляр ChatCompletion]
|
D[Проверка, что response.choices[0].message.content == "Hello"]
```

**Примеры**:

```python
import unittest

from g4f.client import AsyncClient, ChatCompletion
from g4f.providers.retry_provider import IterListProvider
from .mocks import YieldProviderMock, RaiseExceptionProviderMock

DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]

class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
    async def test_skip_provider(self):
        client = AsyncClient(provider=IterListProvider([RaiseExceptionProviderMock, YieldProviderMock], False))
        response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("Hello", response.choices[0].message.content)
```

### `test_only_one_result`

```python
async def test_only_one_result(self):
    """Проверяет, что IterListProvider использует только одного провайдера из списка, если он успешно возвращает результат.

    Args:
        self (TestIterListProvider): Экземпляр класса TestIterListProvider.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.
    """
    ...
```

**Назначение**: Проверяет, что если первый провайдер в списке `IterListProvider` успешно возвращает результат, то остальные провайдеры не используются.

**Как работает функция**:

1.  **Инициализация клиента**: Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит два экземпляра `YieldProviderMock`.
2.  **Вызов API**: Вызывается метод `client.chat.completions.create` с предопределенными сообщениями (`DEFAULT_MESSAGES`) и пустой строкой.
3.  **Проверка результата**: Проверяется, что возвращенный результат является экземпляром `ChatCompletion` и что содержимое сообщения соответствует ожидаемому значению "Hello".

**ASCII Flowchart**:

```
A[Инициализация AsyncClient с IterListProvider([YieldProviderMock, YieldProviderMock])]
|
B[Вызов client.chat.completions.create(DEFAULT_MESSAGES, "")]
|
C[Проверка, что полученный ответ - экземпляр ChatCompletion]
|
D[Проверка, что response.choices[0].message.content == "Hello"]
```

**Примеры**:

```python
import unittest

from g4f.client import AsyncClient, ChatCompletion
from g4f.providers.retry_provider import IterListProvider
from .mocks import YieldProviderMock

DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]

class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
    async def test_only_one_result(self):
        client = AsyncClient(provider=IterListProvider([YieldProviderMock, YieldProviderMock]))
        response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("Hello", response.choices[0].message.content)
```

### `test_stream_skip_provider`

```python
async def test_stream_skip_provider(self):
    """Проверяет, что IterListProvider пропускает провайдера, выбрасывающего исключение при потоковой передаче данных, и использует следующего провайдера.

    Args:
        self (TestIterListProvider): Экземпляр класса TestIterListProvider.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.
    """
    ...
```

**Назначение**: Проверяет, что `IterListProvider` корректно обрабатывает ситуацию, когда один из провайдеров выбрасывает исключение при потоковой передаче данных.

**Как работает функция**:

1.  **Инициализация клиента**: Создается экземпляр `AsyncClient` с `IterListProvider`, который настроен на использование `AsyncRaiseExceptionProviderMock` (который выбрасывает исключение асинхронно) и `YieldProviderMock` (который возвращает успешный результат). Параметр `False` указывает, что исключения должны быть проигнорированы.
2.  **Подготовка сообщений**: Создается список сообщений для потоковой передачи, где каждое сообщение содержит часть фразы "How are you ?".
3.  **Вызов API**: Вызывается метод `client.chat.completions.create` с подготовленными сообщениями, строкой "Hello" и параметром `stream=True`.
4.  **Асинхронный перебор чанков**: Асинхронно перебираются чанки, возвращаемые генератором `response`.
5.  **Проверка результата**: Для каждого чанка проверяется, что он является экземпляром `ChatCompletionChunk` и что его содержимое (если оно не `None`) является строкой.

**ASCII Flowchart**:

```
A[Инициализация AsyncClient с IterListProvider([AsyncRaiseExceptionProviderMock, YieldProviderMock])]
|
B[Подготовка списка сообщений для стриминга]
|
C[Вызов client.chat.completions.create(messages, "Hello", stream=True)]
|
D[Асинхронный перебор чанков из response]
|
E[Проверка, что каждый chunk - экземпляр ChatCompletionChunk]
|
F[Проверка, что chunk.choices[0].delta.content (если не None) является строкой]
```

**Примеры**:

```python
import unittest

from g4f.client import AsyncClient, ChatCompletionChunk
from g4f.providers.retry_provider import IterListProvider
from .mocks import YieldProviderMock, AsyncRaiseExceptionProviderMock

DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]

class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
    async def test_stream_skip_provider(self):
        client = AsyncClient(provider=IterListProvider([AsyncRaiseExceptionProviderMock, YieldProviderMock], False))
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        response = client.chat.completions.create(messages, "Hello", stream=True)
        async for chunk in response:
            chunk: ChatCompletionChunk = chunk
            self.assertIsInstance(chunk, ChatCompletionChunk)
            if chunk.choices[0].delta.content is not None:
                self.assertIsInstance(chunk.choices[0].delta.content, str)
```

### `test_stream_only_one_result`

```python
async def test_stream_only_one_result(self):
    """Проверяет, что при потоковой передаче данных используется только один провайдер из списка, если он успешно возвращает результат.

    Args:
        self (TestIterListProvider): Экземпляр класса TestIterListProvider.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.
    """
    ...
```

**Назначение**: Проверяет, что если первый провайдер в списке `IterListProvider` успешно возвращает результат при потоковой передаче данных, то остальные провайдеры не используются.

**Как работает функция**:

1.  **Инициализация клиента**: Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит два экземпляра `YieldProviderMock`. Параметр `False` указывает, что исключения должны быть проигнорированы.
2.  **Подготовка сообщений**: Создается список сообщений для потоковой передачи, где каждое сообщение содержит строку "You ".
3.  **Вызов API**: Вызывается метод `client.chat.completions.create` с подготовленными сообщениями, строкой "Hello", параметром `stream=True` и `max_tokens=2`.
4.  **Асинхронный перебор чанков**: Асинхронно перебираются чанки, возвращаемые генератором `response`, и добавляются в список `response_list`.
5.  **Проверка количества чанков**: Проверяется, что количество чанков в списке `response_list` равно 3.
6.  **Проверка содержимого чанков**: Для каждого чанка проверяется, что его содержимое (если оно не `None`) равно "You ".

**ASCII Flowchart**:

```
A[Инициализация AsyncClient с IterListProvider([YieldProviderMock, YieldProviderMock])]
|
B[Подготовка списка сообщений для стриминга]
|
C[Вызов client.chat.completions.create(messages, "Hello", stream=True, max_tokens=2)]
|
D[Асинхронный перебор чанков из response и добавление в response_list]
|
E[Проверка, что len(response_list) == 3]
|
F[Проверка, что chunk.choices[0].delta.content (если не None) == "You "]
```

**Примеры**:

```python
import unittest

from g4f.client import AsyncClient, ChatCompletionChunk
from g4f.providers.retry_provider import IterListProvider
from .mocks import YieldProviderMock

DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]

class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
    async def test_stream_only_one_result(self):
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

### `test_skip_none`

```python
async def test_skip_none(self):
    """Проверяет, что IterListProvider пропускает провайдера, возвращающего None, и использует следующего провайдера в списке.

    Args:
        self (TestIterListProvider): Экземпляр класса TestIterListProvider.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.
    """
    ...
```

**Назначение**: Проверяет, что `IterListProvider` корректно обрабатывает ситуацию, когда один из провайдеров возвращает `None`. В этом случае, `IterListProvider` должен пропустить этого провайдера и попытаться использовать следующего провайдера в списке.

**Как работает функция**:

1.  **Инициализация клиента**: Создается экземпляр `AsyncClient` с `IterListProvider`, который настроен на использование `YieldNoneProviderMock` (который возвращает `None`) и `YieldProviderMock` (который возвращает успешный результат). Параметр `False` указывает, что `None` должен быть проигнорирован.
2.  **Вызов API**: Вызывается метод `client.chat.completions.create` с предопределенными сообщениями (`DEFAULT_MESSAGES`) и пустой строкой.
3.  **Проверка результата**: Проверяется, что возвращенный результат является экземпляром `ChatCompletion` и что содержимое сообщения соответствует ожидаемому значению "Hello", которое возвращает `YieldProviderMock`.

**ASCII Flowchart**:

```
A[Инициализация AsyncClient с IterListProvider([YieldNoneProviderMock, YieldProviderMock])]
|
B[Вызов client.chat.completions.create(DEFAULT_MESSAGES, "")]
|
C[Проверка, что полученный ответ - экземпляр ChatCompletion]
|
D[Проверка, что response.choices[0].message.content == "Hello"]
```

**Примеры**:

```python
import unittest

from g4f.client import AsyncClient, ChatCompletion
from g4f.providers.retry_provider import IterListProvider
from .mocks import YieldProviderMock, YieldNoneProviderMock

DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]

class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
    async def test_skip_none(self):
        client = AsyncClient(provider=IterListProvider([YieldNoneProviderMock, YieldProviderMock], False))
        response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("Hello", response.choices[0].message.content)
```

### `test_stream_skip_none`

```python
async def test_stream_skip_none(self):
    """Проверяет, что IterListProvider пропускает провайдера, возвращающего None при потоковой передаче данных, и использует следующего провайдера.

    Args:
        self (TestIterListProvider): Экземпляр класса TestIterListProvider.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.
    """
    ...
```

**Назначение**: Проверяет, что `IterListProvider` корректно обрабатывает ситуацию, когда один из провайдеров возвращает `None` при потоковой передаче данных.

**Как работает функция**:

1.  **Инициализация клиента**: Создается экземпляр `AsyncClient` с `IterListProvider`, который настроен на использование `YieldNoneProviderMock` (который возвращает `None`) и `YieldProviderMock` (который возвращает успешный результат). Параметр `False` указывает, что `None` должен быть проигнорирован.
2.  **Вызов API**: Вызывается метод `client.chat.completions.create` с предопределенными сообщениями (`DEFAULT_MESSAGES`), пустой строкой и параметром `stream=True`.
3.  **Асинхронный перебор чанков**: Асинхронно перебираются чанки, возвращаемые генератором `response`, и добавляются в список `response_list`.
4.  **Проверка количества чанков**: Проверяется, что количество чанков в списке `response_list` равно 2.
5.  **Проверка содержимого чанков**: Для каждого чанка проверяется, что его содержимое (если оно не `None`) равно "Hello".

**ASCII Flowchart**:

```
A[Инициализация AsyncClient с IterListProvider([YieldNoneProviderMock, YieldProviderMock])]
|
B[Вызов client.chat.completions.create(DEFAULT_MESSAGES, "", stream=True)]
|
C[Асинхронный перебор чанков из response и добавление в response_list]
|
D[Проверка, что len(response_list) == 2]
|
E[Проверка, что chunk.choices[0].delta.content (если не None) == "Hello"]
```

**Примеры**:

```python
import unittest

from g4f.client import AsyncClient, ChatCompletionChunk
from g4f.providers.retry_provider import IterListProvider
from .mocks import YieldProviderMock, YieldNoneProviderMock

DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]

class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
    async def test_stream_skip_none(self):
        client = AsyncClient(provider=IterListProvider([YieldNoneProviderMock, YieldProviderMock], False))
        response = client.chat.completions.create(DEFAULT_MESSAGES, "", stream=True)
        response_list = [chunk async for chunk in response]
        self.assertEqual(len(response_list), 2)
        for chunk in response_list:
            if chunk.choices[0].delta.content is not None:
                self.assertEqual(chunk.choices[0].delta.content, "Hello")