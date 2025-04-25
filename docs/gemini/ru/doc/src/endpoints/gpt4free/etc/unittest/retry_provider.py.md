# Модуль retry_provider

## Обзор

Модуль `retry_provider` предоставляет класс `IterListProvider`, который используется для организации циклического перебора нескольких провайдеров (например, для доступа к различным API). 

## Подробнее

`IterListProvider` позволяет переключаться между различными провайдерами, если один из них не работает. Это полезно при использовании нескольких API, где могут быть перебои или ограничения. 

`IterListProvider` может перебирать провайдеры как в стандартном режиме, так и в режиме потоковой передачи (streaming).

## Классы

### `class IterListProvider`

**Описание**: Класс `IterListProvider` реализует итератор для перебора нескольких провайдеров.
**Наследует**:  `_BaseProvider`

**Атрибуты**:

- `providers` (list): Список провайдеров, которые будут перебираться.
- `skip_exceptions` (bool):  Если `True`, то провайдеры, которые вызывают исключения, будут пропускаться.

**Методы**:

- `__init__`: Инициализирует класс `IterListProvider`.
- `__iter__`: Возвращает итератор для перебора провайдеров.
- `__next__`:  Возвращает следующий провайдер из списка.
- `get_next_provider`: Получает следующий доступный провайдер, учитывая `skip_exceptions`.

**Принцип работы**: 

`IterListProvider` хранит список провайдеров и предоставляет доступ к ним по очереди. При вызове `__next__` он возвращает следующий провайдер из списка. Если `skip_exceptions` установлено в `True`, то провайдеры, которые вызывают исключения, пропускаются.


## Функции

### `test_skip_provider`

**Назначение**: Тестовая функция, проверяющая, что `IterListProvider` пропускает провайдеры, которые вызывают исключения, если `skip_exceptions` установлен в `True`.

**Параметры**:

- Нет параметров

**Возвращает**:

- Нет возвращаемого значения

**Вызывает исключения**:

- Нет исключений

**Как работает**:

Функция создает экземпляр `AsyncClient` с `IterListProvider`, содержащим два провайдера: `RaiseExceptionProviderMock` (который всегда вызывает исключение) и `YieldProviderMock` (который возвращает тестовое значение). 

Затем функция вызывает `client.chat.completions.create` и проверяет, что полученный ответ содержит значение, возвращаемое `YieldProviderMock`, а не исключение от `RaiseExceptionProviderMock`.

**Примеры**:

```python
# Создание экземпляра `AsyncClient` с `IterListProvider`,
# где `skip_exceptions` установлено в `True`
client = AsyncClient(provider=IterListProvider([RaiseExceptionProviderMock, YieldProviderMock], True))

# Вызов `client.chat.completions.create`
response = await client.chat.completions.create(DEFAULT_MESSAGES, "")

# Проверка, что ответ содержит значение от `YieldProviderMock`
self.assertEqual("Hello", response.choices[0].message.content)
```

### `test_only_one_result`

**Назначение**: Тестовая функция, проверяющая, что `IterListProvider` возвращает только один результат, даже если в списке провайдеров несколько одинаковых.

**Параметры**:

- Нет параметров

**Возвращает**:

- Нет возвращаемого значения

**Вызывает исключения**:

- Нет исключений

**Как работает**:

Функция создает экземпляр `AsyncClient` с `IterListProvider`, содержащим два одинаковых провайдера: `YieldProviderMock`. 

Затем функция вызывает `client.chat.completions.create` и проверяет, что полученный ответ содержит значение, возвращаемое `YieldProviderMock`, а не дублирующееся.

**Примеры**:

```python
# Создание экземпляра `AsyncClient` с `IterListProvider`,
# где список провайдеров содержит два одинаковых элемента
client = AsyncClient(provider=IterListProvider([YieldProviderMock, YieldProviderMock]))

# Вызов `client.chat.completions.create`
response = await client.chat.completions.create(DEFAULT_MESSAGES, "")

# Проверка, что ответ содержит только одно значение
self.assertEqual("Hello", response.choices[0].message.content)
```

### `test_stream_skip_provider`

**Назначение**: Тестовая функция, проверяющая, что `IterListProvider` в режиме потоковой передачи пропускает провайдеры, которые вызывают исключения, если `skip_exceptions` установлен в `True`.

**Параметры**:

- Нет параметров

**Возвращает**:

- Нет возвращаемого значения

**Вызывает исключения**:

- Нет исключений

**Как работает**:

Функция создает экземпляр `AsyncClient` с `IterListProvider`, содержащим два провайдера: `AsyncRaiseExceptionProviderMock` (который всегда вызывает исключение в режиме потоковой передачи) и `YieldProviderMock` (который возвращает тестовое значение). 

Затем функция вызывает `client.chat.completions.create` в режиме потоковой передачи (`stream=True`) и проверяет, что полученные чанки (части ответа) содержат значение, возвращаемое `YieldProviderMock`, а не исключение от `AsyncRaiseExceptionProviderMock`.

**Примеры**:

```python
# Создание экземпляра `AsyncClient` с `IterListProvider`,
# где `skip_exceptions` установлено в `True`
client = AsyncClient(provider=IterListProvider([AsyncRaiseExceptionProviderMock, YieldProviderMock], True))

# Вызов `client.chat.completions.create` в режиме потоковой передачи
response = client.chat.completions.create(messages, "Hello", stream=True)

# Проверка, что полученные чанки содержат значение от `YieldProviderMock`
async for chunk in response:
    chunk: ChatCompletionChunk = chunk
    if chunk.choices[0].delta.content is not None:
        self.assertIsInstance(chunk.choices[0].delta.content, str)
```

### `test_stream_only_one_result`

**Назначение**: Тестовая функция, проверяющая, что `IterListProvider` в режиме потоковой передачи возвращает только один результат, даже если в списке провайдеров несколько одинаковых.

**Параметры**:

- Нет параметров

**Возвращает**:

- Нет возвращаемого значения

**Вызывает исключения**:

- Нет исключений

**Как работает**:

Функция создает экземпляр `AsyncClient` с `IterListProvider`, содержащим два одинаковых провайдера: `YieldProviderMock`. 

Затем функция вызывает `client.chat.completions.create` в режиме потоковой передачи (`stream=True`) и проверяет, что полученные чанки содержат только одно значение, а не дублирующееся.

**Примеры**:

```python
# Создание экземпляра `AsyncClient` с `IterListProvider`,
# где список провайдеров содержит два одинаковых элемента
client = AsyncClient(provider=IterListProvider([YieldProviderMock, YieldProviderMock]))

# Вызов `client.chat.completions.create` в режиме потоковой передачи
response = client.chat.completions.create(messages, "Hello", stream=True)

# Проверка, что полученные чанки содержат только одно значение
response_list = []
async for chunk in response:
    response_list.append(chunk)
self.assertEqual(len(response_list), 3)
for chunk in response_list:
    if chunk.choices[0].delta.content is not None:
        self.assertEqual(chunk.choices[0].delta.content, "You ")
```

### `test_skip_none`

**Назначение**: Тестовая функция, проверяющая, что `IterListProvider` пропускает провайдеры, которые возвращают `None`, если `skip_exceptions` установлен в `True`.

**Параметры**:

- Нет параметров

**Возвращает**:

- Нет возвращаемого значения

**Вызывает исключения**:

- Нет исключений

**Как работает**:

Функция создает экземпляр `AsyncClient` с `IterListProvider`, содержащим два провайдера: `YieldNoneProviderMock` (который возвращает `None`) и `YieldProviderMock` (который возвращает тестовое значение). 

Затем функция вызывает `client.chat.completions.create` и проверяет, что полученный ответ содержит значение, возвращаемое `YieldProviderMock`, а не `None` от `YieldNoneProviderMock`.

**Примеры**:

```python
# Создание экземпляра `AsyncClient` с `IterListProvider`,
# где `skip_exceptions` установлено в `True`
client = AsyncClient(provider=IterListProvider([YieldNoneProviderMock, YieldProviderMock], True))

# Вызов `client.chat.completions.create`
response = await client.chat.completions.create(DEFAULT_MESSAGES, "")

# Проверка, что ответ содержит значение от `YieldProviderMock`
self.assertEqual("Hello", response.choices[0].message.content)
```

### `test_stream_skip_none`

**Назначение**: Тестовая функция, проверяющая, что `IterListProvider` в режиме потоковой передачи пропускает провайдеры, которые возвращают `None`, если `skip_exceptions` установлен в `True`.

**Параметры**:

- Нет параметров

**Возвращает**:

- Нет возвращаемого значения

**Вызывает исключения**:

- Нет исключений

**Как работает**:

Функция создает экземпляр `AsyncClient` с `IterListProvider`, содержащим два провайдера: `YieldNoneProviderMock` (который возвращает `None`) и `YieldProviderMock` (который возвращает тестовое значение). 

Затем функция вызывает `client.chat.completions.create` в режиме потоковой передачи (`stream=True`) и проверяет, что полученные чанки (части ответа) содержат значение, возвращаемое `YieldProviderMock`, а не `None` от `YieldNoneProviderMock`.

**Примеры**:

```python
# Создание экземпляра `AsyncClient` с `IterListProvider`,
# где `skip_exceptions` установлено в `True`
client = AsyncClient(provider=IterListProvider([YieldNoneProviderMock, YieldProviderMock], True))

# Вызов `client.chat.completions.create` в режиме потоковой передачи
response = client.chat.completions.create(DEFAULT_MESSAGES, "", stream=True)

# Проверка, что полученные чанки содержат значение от `YieldProviderMock`
response_list = [chunk async for chunk in response]
self.assertEqual(len(response_list), 2)
for chunk in response_list:
    if chunk.choices[0].delta.content is not None:
        self.assertEqual(chunk.choices[0].delta.content, "Hello")
```