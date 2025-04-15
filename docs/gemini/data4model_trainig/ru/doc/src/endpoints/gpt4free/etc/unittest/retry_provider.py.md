# Модуль `retry_provider.py` для модульного тестирования

## Обзор

Модуль содержит набор модульных тестов для проверки функциональности `IterListProvider`, который обеспечивает механизм повторных попыток с различными провайдерами в случае сбоя. Он использует `unittest` для определения тестовых случаев и `g4f.client` для эмуляции асинхронных вызовов к провайдерам.

## Подробней

Этот модуль тестирует различные сценарии, включая пропуск провайдеров, возвращающих исключения или `None`, а также проверяет потоковую передачу данных. Он гарантирует, что `IterListProvider` корректно обрабатывает различные ситуации и возвращает ожидаемые результаты.
В модуле используются моки (mocks), для эмуляции ответов от разных провайдеров.

## Классы

### `TestIterListProvider`

**Описание**: Класс `TestIterListProvider` содержит набор асинхронных тестов для проверки `IterListProvider`.

**Наследует**: `unittest.IsolatedAsyncioTestCase`

**Атрибуты**:
- `DEFAULT_MESSAGES` (List[dict]): Стандартный набор сообщений для использования в тестовых запросах.

**Методы**:
- `test_skip_provider()`: Проверяет, что провайдер пропускается, если он вызывает исключение.
- `test_only_one_result()`: Проверяет, что возвращается только один результат, даже если несколько провайдеров возвращают успешный ответ.
- `test_stream_skip_provider()`: Проверяет потоковую передачу данных с пропуском провайдера, вызывающего исключение.
- `test_stream_only_one_result()`: Проверяет потоковую передачу данных и убеждается, что возвращается только один результат.
- `test_skip_none()`: Проверяет, что провайдер пропускается, если он возвращает `None`.
- `test_stream_skip_none()`: Проверяет потоковую передачу данных с пропуском провайдера, возвращающего `None`.

## Методы класса

### `test_skip_provider`

```python
async def test_skip_provider(self):
    """
    Проверяет, что провайдер пропускается, если он вызывает исключение.

    Args:
        self (TestIterListProvider): Экземпляр тестового класса.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.

    Как работает функция:
    1. Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит `RaiseExceptionProviderMock` и `YieldProviderMock`.
    2. Вызывается метод `chat.completions.create` с стандартными сообщениями.
    3. Проверяется, что возвращенный объект является экземпляром `ChatCompletion`.
    4. Проверяется, что содержимое сообщения в ответе равно "Hello", что указывает на использование `YieldProviderMock` после пропуска `RaiseExceptionProviderMock`.
    """
```

### `test_only_one_result`

```python
async def test_only_one_result(self):
    """
    Проверяет, что возвращается только один результат, даже если несколько провайдеров возвращают успешный ответ.

    Args:
        self (TestIterListProvider): Экземпляр тестового класса.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.

    Как работает функция:
    1. Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит два экземпляра `YieldProviderMock`.
    2. Вызывается метод `chat.completions.create` с стандартными сообщениями.
    3. Проверяется, что возвращенный объект является экземпляром `ChatCompletion`.
    4. Проверяется, что содержимое сообщения в ответе равно "Hello", что указывает на успешное выполнение одного из провайдеров.
    """
```

### `test_stream_skip_provider`

```python
async def test_stream_skip_provider(self):
    """
    Проверяет потоковую передачу данных с пропуском провайдера, вызывающего исключение.

    Args:
        self (TestIterListProvider): Экземпляр тестового класса.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.

    Как работает функция:
    1. Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит `AsyncRaiseExceptionProviderMock` и `YieldProviderMock`.
    2. Формируются сообщения для потоковой передачи.
    3. Вызывается метод `chat.completions.create` с потоковой передачей.
    4. Асинхронно перебираются чанки ответа.
    5. Проверяется, что каждый чанк является экземпляром `ChatCompletionChunk` и содержит строковое содержимое.
    """
```

### `test_stream_only_one_result`

```python
async def test_stream_only_one_result(self):
    """
    Проверяет потоковую передачу данных и убеждается, что возвращается только один результат.

    Args:
        self (TestIterListProvider): Экземпляр тестового класса.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.

    Как работает функция:
    1. Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит два экземпляра `YieldProviderMock`.
    2. Формируются сообщения для потоковой передачи.
    3. Вызывается метод `chat.completions.create` с потоковой передачей и ограничением на 2 токена.
    4. Асинхронно перебираются чанки ответа и добавляются в список.
    5. Проверяется, что количество чанков равно 3.
    6. Проверяется, что содержимое каждого чанка равно "You ".
    """
```

### `test_skip_none`

```python
async def test_skip_none(self):
    """
    Проверяет, что провайдер пропускается, если он возвращает `None`.

    Args:
        self (TestIterListProvider): Экземпляр тестового класса.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.

    Как работает функция:
    1. Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит `YieldNoneProviderMock` и `YieldProviderMock`.
    2. Вызывается метод `chat.completions.create` с стандартными сообщениями.
    3. Проверяется, что возвращенный объект является экземпляром `ChatCompletion`.
    4. Проверяется, что содержимое сообщения в ответе равно "Hello", что указывает на использование `YieldProviderMock` после пропуска `YieldNoneProviderMock`.
    """
```

### `test_stream_skip_none`

```python
async def test_stream_skip_none(self):
    """
    Проверяет потоковую передачу данных с пропуском провайдера, возвращающего `None`.

    Args:
        self (TestIterListProvider): Экземпляр тестового класса.

    Returns:
        None

    Raises:
        AssertionError: Если результат не соответствует ожидаемому.

    Как работает функция:
    1. Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит `YieldNoneProviderMock` и `YieldProviderMock`.
    2. Вызывается метод `chat.completions.create` с потоковой передачей.
    3. Асинхронно перебираются чанки ответа и добавляются в список.
    4. Проверяется, что количество чанков равно 2.
    5. Проверяется, что содержимое каждого чанка равно "Hello".
    """
```

## Параметры класса

- `DEFAULT_MESSAGES`: Список, содержащий словарь с ключами 'role' и 'content'. Используется как стандартное сообщение для тестов.

## Примеры

**Пример 1: Пропуск провайдера, вызывающего исключение**

```python
client = AsyncClient(provider=IterListProvider([RaiseExceptionProviderMock, YieldProviderMock], False))
response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
assert isinstance(response, ChatCompletion)
assert response.choices[0].message.content == "Hello"
```

**Пример 2: Потоковая передача с пропуском `None`**

```python
client = AsyncClient(provider=IterListProvider([YieldNoneProviderMock, YieldProviderMock], False))
response = client.chat.completions.create(DEFAULT_MESSAGES, "", stream=True)
response_list = [chunk async for chunk in response]
assert len(response_list) == 2
for chunk in response_list:
    if chunk.choices[0].delta.content is not None:
        assert chunk.choices[0].delta.content == "Hello"
```