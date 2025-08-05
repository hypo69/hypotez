# hypotez/src/endpoints/gpt4free/etc/unittest/retry_provider.py

## Обзор

Модуль содержит тесты для `IterListProvider` - класса, отвечающего за перебор нескольких провайдеров в попытке получить успешный ответ. 

## Детали

Модуль тестирует различные сценарии использования класса `IterListProvider`, в том числе:

- Пропуск провайдеров, которые вызывают исключения.
- Возврат результата только от одного успешного провайдера.
- Стриминг ответов (по частям).
- Пропуск провайдеров, которые возвращают `None`.

## Классы

### `class TestIterListProvider`

**Описание**: Тестовый класс для `IterListProvider`.

**Inherits**: `unittest.IsolatedAsyncioTestCase` - класс для асинхронных тестов.

**Атрибуты**:

- `DEFAULT_MESSAGES` (list[dict]): Список сообщений по умолчанию для тестирования.

**Методы**:

- `test_skip_provider()`: Тестирует, что `IterListProvider` пропускает провайдеров, которые вызывают исключения, и возвращает результат от следующего успешного провайдера.
- `test_only_one_result()`: Тестирует, что `IterListProvider` возвращает результат только от одного успешного провайдера, даже если доступны несколько провайдеров.
- `test_stream_skip_provider()`: Тестирует, что `IterListProvider` пропускает провайдеров, которые вызывают исключения при стриминге ответов, и возвращает результат от следующего успешного провайдера.
- `test_stream_only_one_result()`: Тестирует, что `IterListProvider` возвращает результат только от одного успешного провайдера при стриминге ответов, даже если доступны несколько провайдеров.
- `test_skip_none()`: Тестирует, что `IterListProvider` пропускает провайдеров, которые возвращают `None`, и возвращает результат от следующего успешного провайдера.
- `test_stream_skip_none()`: Тестирует, что `IterListProvider` пропускает провайдеров, которые возвращают `None` при стриминге ответов, и возвращает результат от следующего успешного провайдера.

## Функции

### `test_skip_provider()`

**Purpose**: Проверяет, что `IterListProvider` пропускает провайдеров, которые вызывают исключения, и возвращает результат от следующего успешного провайдера.

**Parameters**: 
- None.

**Returns**: 
- None.

**Raises Exceptions**: 
- None.

**How the Function Works**: 
- Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит провайдер, который вызывается исключение, и провайдер, который возвращает успешный ответ.
- Вызывается метод `client.chat.completions.create` для получения ответа от API.
- Проверяется, что полученный ответ является экземпляром `ChatCompletion` и что его содержание соответствует ожидаемому значению.

**Examples**: 
- `client = AsyncClient(provider=IterListProvider([RaiseExceptionProviderMock, YieldProviderMock], False))` - создание экземпляра `AsyncClient` с `IterListProvider`, который содержит провайдер, который вызывается исключение, и провайдер, который возвращает успешный ответ.
- `response = await client.chat.completions.create(DEFAULT_MESSAGES, "")` - вызов метода `client.chat.completions.create` для получения ответа от API.
- `self.assertIsInstance(response, ChatCompletion)` - проверка, что полученный ответ является экземпляром `ChatCompletion`.
- `self.assertEqual("Hello", response.choices[0].message.content)` - проверка, что содержание ответа соответствует ожидаемому значению.

### `test_only_one_result()`

**Purpose**: Проверяет, что `IterListProvider` возвращает результат только от одного успешного провайдера, даже если доступны несколько провайдеров.

**Parameters**: 
- None.

**Returns**: 
- None.

**Raises Exceptions**: 
- None.

**How the Function Works**: 
- Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит два провайдера, которые возвращают успешные ответы.
- Вызывается метод `client.chat.completions.create` для получения ответа от API.
- Проверяется, что полученный ответ является экземпляром `ChatCompletion` и что его содержание соответствует ожидаемому значению.

**Examples**: 
- `client = AsyncClient(provider=IterListProvider([YieldProviderMock, YieldProviderMock]))` - создание экземпляра `AsyncClient` с `IterListProvider`, который содержит два провайдера, которые возвращают успешные ответы.
- `response = await client.chat.completions.create(DEFAULT_MESSAGES, "")` - вызов метода `client.chat.completions.create` для получения ответа от API.
- `self.assertIsInstance(response, ChatCompletion)` - проверка, что полученный ответ является экземпляром `ChatCompletion`.
- `self.assertEqual("Hello", response.choices[0].message.content)` - проверка, что содержание ответа соответствует ожидаемому значению.

### `test_stream_skip_provider()`

**Purpose**: Проверяет, что `IterListProvider` пропускает провайдеров, которые вызывают исключения при стриминге ответов, и возвращает результат от следующего успешного провайдера.

**Parameters**: 
- None.

**Returns**: 
- None.

**Raises Exceptions**: 
- None.

**How the Function Works**: 
- Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит провайдер, который вызывается исключение, и провайдер, который возвращает успешный ответ.
- Вызывается метод `client.chat.completions.create` с параметром `stream=True` для стриминга ответов.
- Проверяется, что каждый полученный чанк является экземпляром `ChatCompletionChunk` и что его содержание является строкой.

**Examples**: 
- `client = AsyncClient(provider=IterListProvider([AsyncRaiseExceptionProviderMock, YieldProviderMock], False))` - создание экземпляра `AsyncClient` с `IterListProvider`, который содержит провайдер, который вызывается исключение, и провайдер, который возвращает успешный ответ.
- `response = client.chat.completions.create(messages, "Hello", stream=True)` - вызов метода `client.chat.completions.create` с параметром `stream=True` для стриминга ответов.
- `async for chunk in response: ` - итерация по полученным чанкам.
- `chunk: ChatCompletionChunk = chunk` - тип чанка.
- `self.assertIsInstance(chunk, ChatCompletionChunk)` - проверка, что каждый полученный чанк является экземпляром `ChatCompletionChunk`.
- `self.assertIsInstance(chunk.choices[0].delta.content, str)` - проверка, что содержание чанка является строкой.

### `test_stream_only_one_result()`

**Purpose**: Проверяет, что `IterListProvider` возвращает результат только от одного успешного провайдера при стриминге ответов, даже если доступны несколько провайдеров.

**Parameters**: 
- None.

**Returns**: 
- None.

**Raises Exceptions**: 
- None.

**How the Function Works**: 
- Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит два провайдера, которые возвращают успешные ответы.
- Вызывается метод `client.chat.completions.create` с параметром `stream=True` для стриминга ответов.
- Проверяется, что получено правильное количество чанков, и что содержание каждого чанка соответствует ожидаемому значению.

**Examples**: 
- `client = AsyncClient(provider=IterListProvider([YieldProviderMock, YieldProviderMock], False))` - создание экземпляра `AsyncClient` с `IterListProvider`, который содержит два провайдера, которые возвращают успешные ответы.
- `response = client.chat.completions.create(messages, "Hello", stream=True, max_tokens=2)` - вызов метода `client.chat.completions.create` с параметром `stream=True` для стриминга ответов.
- `response_list = [chunk async for chunk in response]` - сбор всех чанков в список.
- `self.assertEqual(len(response_list), 3)` - проверка, что получено правильное количество чанков.
- `for chunk in response_list: ... self.assertEqual(chunk.choices[0].delta.content, "You ")` - проверка, что содержание каждого чанка соответствует ожидаемому значению.

### `test_skip_none()`

**Purpose**: Проверяет, что `IterListProvider` пропускает провайдеров, которые возвращают `None`, и возвращает результат от следующего успешного провайдера.

**Parameters**: 
- None.

**Returns**: 
- None.

**Raises Exceptions**: 
- None.

**How the Function Works**: 
- Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит провайдер, который возвращает `None`, и провайдер, который возвращает успешный ответ.
- Вызывается метод `client.chat.completions.create` для получения ответа от API.
- Проверяется, что полученный ответ является экземпляром `ChatCompletion` и что его содержание соответствует ожидаемому значению.

**Examples**: 
- `client = AsyncClient(provider=IterListProvider([YieldNoneProviderMock, YieldProviderMock], False))` - создание экземпляра `AsyncClient` с `IterListProvider`, который содержит провайдер, который возвращает `None`, и провайдер, который возвращает успешный ответ.
- `response = await client.chat.completions.create(DEFAULT_MESSAGES, "")` - вызов метода `client.chat.completions.create` для получения ответа от API.
- `self.assertIsInstance(response, ChatCompletion)` - проверка, что полученный ответ является экземпляром `ChatCompletion`.
- `self.assertEqual("Hello", response.choices[0].message.content)` - проверка, что содержание ответа соответствует ожидаемому значению.

### `test_stream_skip_none()`

**Purpose**: Проверяет, что `IterListProvider` пропускает провайдеров, которые возвращают `None` при стриминге ответов, и возвращает результат от следующего успешного провайдера.

**Parameters**: 
- None.

**Returns**: 
- None.

**Raises Exceptions**: 
- None.

**How the Function Works**: 
- Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит провайдер, который возвращает `None`, и провайдер, который возвращает успешный ответ.
- Вызывается метод `client.chat.completions.create` с параметром `stream=True` для стриминга ответов.
- Проверяется, что получено правильное количество чанков, и что содержание каждого чанка соответствует ожидаемому значению.

**Examples**: 
- `client = AsyncClient(provider=IterListProvider([YieldNoneProviderMock, YieldProviderMock], False))` - создание экземпляра `AsyncClient` с `IterListProvider`, который содержит провайдер, который возвращает `None`, и провайдер, который возвращает успешный ответ.
- `response = client.chat.completions.create(DEFAULT_MESSAGES, "", stream=True)` - вызов метода `client.chat.completions.create` с параметром `stream=True` для стриминга ответов.
- `response_list = [chunk async for chunk in response]` - сбор всех чанков в список.
- `self.assertEqual(len(response_list), 2)` - проверка, что получено правильное количество чанков.
- `for chunk in response_list: ... self.assertEqual(chunk.choices[0].delta.content, "Hello")` - проверка, что содержание каждого чанка соответствует ожидаемому значению.

## Parameter Details

- `DEFAULT_MESSAGES` (list[dict]): Список сообщений по умолчанию для тестирования.
- `RaiseExceptionProviderMock`: Моковый провайдер, который вызывается исключение.
- `YieldProviderMock`: Моковый провайдер, который возвращает успешный ответ.
- `AsyncRaiseExceptionProviderMock`: Моковый провайдер, который вызывается исключение при стриминге ответов.
- `YieldNoneProviderMock`: Моковый провайдер, который возвращает `None`.

## Examples

```python
# Пример теста с `test_skip_provider()`:
client = AsyncClient(provider=IterListProvider([RaiseExceptionProviderMock, YieldProviderMock], False))
response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
self.assertIsInstance(response, ChatCompletion)
self.assertEqual("Hello", response.choices[0].message.content)

# Пример теста с `test_stream_only_one_result()`:
client = AsyncClient(provider=IterListProvider([YieldProviderMock, YieldProviderMock], False))
response = client.chat.completions.create(messages, "Hello", stream=True, max_tokens=2)
response_list = [chunk async for chunk in response]
self.assertEqual(len(response_list), 3)
for chunk in response_list:
    if chunk.choices[0].delta.content is not None:
        self.assertEqual(chunk.choices[0].delta.content, "You ")
```