# Модуль для тестирования `retry_provider`

## Обзор

Модуль содержит юнит-тесты для проверки функциональности класса `IterListProvider`, который предназначен для повторных попыток использования различных провайдеров при взаимодействии с g4f (gpt4free). Он проверяет корректность работы провайдера при возникновении исключений, возврате `None` и при потоковой передаче данных.

## Подробней

Данный код является частью набора тестов для библиотеки `g4f`, в частности, для модуля `retry_provider`. Он проверяет, как `IterListProvider` обрабатывает различные сценарии, такие как пропуск провайдеров, возвращающих исключения или `None`, а также корректность работы в режиме потоковой передачи данных. Тесты используют моки провайдеров, чтобы имитировать различные ситуации и убедиться, что `IterListProvider` ведет себя ожидаемым образом.

## Классы

### `TestIterListProvider`

**Описание**: Класс, содержащий асинхронные юнит-тесты для проверки функциональности `IterListProvider`.

**Наследует**:

- `unittest.IsolatedAsyncioTestCase`: Класс для написания асинхронных юнит-тестов.

**Атрибуты**:

- `DEFAULT_MESSAGES` (list): Список сообщений по умолчанию, используемых в тестах.

**Методы**:

- `test_skip_provider()`: Тест проверяет, что `IterListProvider` пропускает провайдера, выбрасывающего исключение, и использует следующего провайдера в списке.
- `test_only_one_result()`: Тест проверяет, что `IterListProvider` использует только один результат от первого успешного провайдера.
- `test_stream_skip_provider()`: Тест проверяет, что `IterListProvider` пропускает провайдера, выбрасывающего исключение, при потоковой передаче данных и использует следующего провайдера.
- `test_stream_only_one_result()`: Тест проверяет, что при потоковой передаче данных используется только один результат от первого успешного провайдера.
- `test_skip_none()`: Тест проверяет, что `IterListProvider` пропускает провайдера, возвращающего `None`, и использует следующего провайдера в списке.
- `test_stream_skip_none()`: Тест проверяет, что `IterListProvider` пропускает провайдера, возвращающего `None`, при потоковой передаче данных и использует следующего провайдера.

## Функции

### `test_skip_provider`

```python
    async def test_skip_provider(self):
        """Тест проверяет, что `IterListProvider` пропускает провайдера, выбрасывающего исключение, и использует следующего провайдера в списке.

        Args:
            self (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

        Returns:
            None

        Raises:
            AssertionError: Если результат не соответствует ожидаемому.
        """
```

**Назначение**: Проверяет, что `IterListProvider` пропускает провайдера, выбрасывающего исключение, и использует следующего провайдера в списке.

**Параметры**:

- `self` (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

**Возвращает**:

- `None`

**Вызывает исключения**:

- `AssertionError`: Если результат не соответствует ожидаемому.

**Как работает функция**:

1.  Создается экземпляр `AsyncClient` с `IterListProvider`, которому передается список провайдеров, включающий `RaiseExceptionProviderMock` (который выбрасывает исключение) и `YieldProviderMock` (который возвращает результат "Hello").
2.  Вызывается метод `client.chat.completions.create` для получения ответа от провайдера.
3.  Проверяется, что полученный ответ является экземпляром `ChatCompletion` и что содержимое сообщения равно "Hello".

**ASCII flowchart**:

```
A: Создание AsyncClient с IterListProvider([RaiseExceptionProviderMock, YieldProviderMock])
|
B: Вызов client.chat.completions.create(DEFAULT_MESSAGES, "")
|
C: RaiseExceptionProviderMock выбрасывает исключение -> IterListProvider переходит к следующему провайдеру
|
D: YieldProviderMock возвращает ChatCompletion с сообщением "Hello"
|
E: Проверка, что ответ - ChatCompletion и содержимое сообщения == "Hello"
```

**Примеры**:

```python
# Пример использования в асинхронном тесте
async def test_skip_provider(self):
    client = AsyncClient(provider=IterListProvider([RaiseExceptionProviderMock, YieldProviderMock], False))
    response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
    self.assertIsInstance(response, ChatCompletion)
    self.assertEqual("Hello", response.choices[0].message.content)
```

### `test_only_one_result`

```python
    async def test_only_one_result(self):
        """Тест проверяет, что `IterListProvider` использует только один результат от первого успешного провайдера.

        Args:
            self (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

        Returns:
            None

        Raises:
            AssertionError: Если результат не соответствует ожидаемому.
        """
```

**Назначение**: Проверяет, что `IterListProvider` использует только один результат от первого успешного провайдера.

**Параметры**:

- `self` (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

**Возвращает**:

- `None`

**Вызывает исключения**:

- `AssertionError`: Если результат не соответствует ожидаемому.

**Как работает функция**:

1.  Создается экземпляр `AsyncClient` с `IterListProvider`, которому передается список, содержащий два экземпляра `YieldProviderMock`.
2.  Вызывается метод `client.chat.completions.create` для получения ответа от провайдера.
3.  Проверяется, что полученный ответ является экземпляром `ChatCompletion` и что содержимое сообщения равно "Hello".

**ASCII flowchart**:

```
A: Создание AsyncClient с IterListProvider([YieldProviderMock, YieldProviderMock])
|
B: Вызов client.chat.completions.create(DEFAULT_MESSAGES, "")
|
C: Первый YieldProviderMock возвращает ChatCompletion с сообщением "Hello"
|
D: IterListProvider прекращает итерацию после первого успешного результата
|
E: Проверка, что ответ - ChatCompletion и содержимое сообщения == "Hello"
```

**Примеры**:

```python
# Пример использования в асинхронном тесте
async def test_only_one_result(self):
    client = AsyncClient(provider=IterListProvider([YieldProviderMock, YieldProviderMock]))
    response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
    self.assertIsInstance(response, ChatCompletion)
    self.assertEqual("Hello", response.choices[0].message.content)
```

### `test_stream_skip_provider`

```python
    async def test_stream_skip_provider(self):
        """Тест проверяет, что `IterListProvider` пропускает провайдера, выбрасывающего исключение, при потоковой передаче данных и использует следующего провайдера.

        Args:
            self (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

        Returns:
            None

        Raises:
            AssertionError: Если результат не соответствует ожидаемому.
        """
```

**Назначение**: Проверяет, что `IterListProvider` пропускает провайдера, выбрасывающего исключение, при потоковой передаче данных и использует следующего провайдера.

**Параметры**:

- `self` (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

**Возвращает**:

- `None`

**Вызывает исключения**:

- `AssertionError`: Если результат не соответствует ожидаемому.

**Как работает функция**:

1.  Создается экземпляр `AsyncClient` с `IterListProvider`, которому передается список провайдеров, включающий `AsyncRaiseExceptionProviderMock` (который выбрасывает исключение асинхронно) и `YieldProviderMock` (который возвращает результат "Hello").
2.  Формируется список сообщений для отправки в потоковом режиме.
3.  Вызывается метод `client.chat.completions.create` с параметром `stream=True` для получения потока данных от провайдера.
4.  Асинхронно итерируемся по потоку данных и проверяется, что каждый чанк является экземпляром `ChatCompletionChunk`, и что содержимое сообщения не равно `None` и является строкой.

**ASCII flowchart**:

```
A: Создание AsyncClient с IterListProvider([AsyncRaiseExceptionProviderMock, YieldProviderMock])
|
B: Формирование списка сообщений для потоковой передачи
|
C: Вызов client.chat.completions.create(messages, "Hello", stream=True)
|
D: AsyncRaiseExceptionProviderMock выбрасывает исключение -> IterListProvider переходит к следующему провайдеру
|
E: YieldProviderMock возвращает поток ChatCompletionChunk с содержимым
|
F: Асинхронная итерация по потоку и проверка типов и содержимого чанков
```

**Примеры**:

```python
# Пример использования в асинхронном тесте для потоковой передачи данных
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
        """Тест проверяет, что при потоковой передаче данных используется только один результат от первого успешного провайдера.

        Args:
            self (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

        Returns:
            None

        Raises:
            AssertionError: Если результат не соответствует ожидаемому.
        """
```

**Назначение**: Проверяет, что при потоковой передаче данных используется только один результат от первого успешного провайдера.

**Параметры**:

- `self` (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

**Возвращает**:

- `None`

**Вызывает исключения**:

- `AssertionError`: Если результат не соответствует ожидаемому.

**Как работает функция**:

1.  Создается экземпляр `AsyncClient` с `IterListProvider`, которому передается список, содержащий два экземпляра `YieldProviderMock`.
2.  Формируется список сообщений для отправки в потоковом режиме.
3.  Вызывается метод `client.chat.completions.create` с параметром `stream=True` и `max_tokens=2` для получения потока данных от провайдера.
4.  Асинхронно итерируемся по потоку данных, собирая чанки в список `response_list`.
5.  Проверяется, что длина списка `response_list` равна 3.
6.  Проверяется, что содержимое каждого чанка, не равного `None`, равно "You ".

**ASCII flowchart**:

```
A: Создание AsyncClient с IterListProvider([YieldProviderMock, YieldProviderMock], False)
|
B: Формирование списка сообщений для потоковой передачи
|
C: Вызов client.chat.completions.create(messages, "Hello", stream=True, max_tokens=2)
|
D: Первый YieldProviderMock возвращает поток ChatCompletionChunk с содержимым "You "
|
E: Сбор чанков в список response_list
|
F: Проверка длины списка response_list == 3 и содержимого чанков
```

**Примеры**:

```python
# Пример использования в асинхронном тесте для потоковой передачи данных
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
        """Тест проверяет, что `IterListProvider` пропускает провайдера, возвращающего `None`, и использует следующего провайдера в списке.

        Args:
            self (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

        Returns:
            None

        Raises:
            AssertionError: Если результат не соответствует ожидаемому.
        """
```

**Назначение**: Проверяет, что `IterListProvider` пропускает провайдера, возвращающего `None`, и использует следующего провайдера в списке.

**Параметры**:

- `self` (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

**Возвращает**:

- `None`

**Вызывает исключения**:

- `AssertionError`: Если результат не соответствует ожидаемому.

**Как работает функция**:

1.  Создается экземпляр `AsyncClient` с `IterListProvider`, которому передается список провайдеров, включающий `YieldNoneProviderMock` (который возвращает `None`) и `YieldProviderMock` (который возвращает результат "Hello").
2.  Вызывается метод `client.chat.completions.create` для получения ответа от провайдера.
3.  Проверяется, что полученный ответ является экземпляром `ChatCompletion` и что содержимое сообщения равно "Hello".

**ASCII flowchart**:

```
A: Создание AsyncClient с IterListProvider([YieldNoneProviderMock, YieldProviderMock], False)
|
B: Вызов client.chat.completions.create(DEFAULT_MESSAGES, "")
|
C: YieldNoneProviderMock возвращает None -> IterListProvider переходит к следующему провайдеру
|
D: YieldProviderMock возвращает ChatCompletion с сообщением "Hello"
|
E: Проверка, что ответ - ChatCompletion и содержимое сообщения == "Hello"
```

**Примеры**:

```python
# Пример использования в асинхронном тесте
async def test_skip_none(self):
    client = AsyncClient(provider=IterListProvider([YieldNoneProviderMock, YieldProviderMock], False))
    response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
    self.assertIsInstance(response, ChatCompletion)
    self.assertEqual("Hello", response.choices[0].message.content)
```

### `test_stream_skip_none`

```python
    async def test_stream_skip_none(self):
        """Тест проверяет, что `IterListProvider` пропускает провайдера, возвращающего `None`, при потоковой передаче данных и использует следующего провайдера.

        Args:
            self (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

        Returns:
            None

        Raises:
            AssertionError: Если результат не соответствует ожидаемому.
        """
```

**Назначение**: Проверяет, что `IterListProvider` пропускает провайдера, возвращающего `None`, при потоковой передаче данных и использует следующего провайдера.

**Параметры**:

- `self` (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

**Возвращает**:

- `None`

**Вызывает исключения**:

- `AssertionError`: Если результат не соответствует ожидаемому.

**Как работает функция**:

1.  Создается экземпляр `AsyncClient` с `IterListProvider`, которому передается список провайдеров, включающий `YieldNoneProviderMock` (который возвращает `None`) и `YieldProviderMock` (который возвращает результат "Hello").
2.  Вызывается метод `client.chat.completions.create` с параметром `stream=True` для получения потока данных от провайдера.
3.  Асинхронно итерируемся по потоку данных, собирая чанки в список `response_list`.
4.  Проверяется, что длина списка `response_list` равна 2.
5.  Проверяется, что содержимое каждого чанка, не равного `None`, равно "Hello".

**ASCII flowchart**:

```
A: Создание AsyncClient с IterListProvider([YieldNoneProviderMock, YieldProviderMock], False)
|
B: Вызов client.chat.completions.create(DEFAULT_MESSAGES, "", stream=True)
|
C: YieldNoneProviderMock возвращает None -> IterListProvider переходит к следующему провайдеру
|
D: YieldProviderMock возвращает поток ChatCompletionChunk с содержимым "Hello"
|
E: Сбор чанков в список response_list
|
F: Проверка длины списка response_list == 2 и содержимого чанков
```

**Примеры**:

```python
# Пример использования в асинхронном тесте для потоковой передачи данных
async def test_stream_skip_none(self):
    client = AsyncClient(provider=IterListProvider([YieldNoneProviderMock, YieldProviderMock], False))
    response = client.chat.completions.create(DEFAULT_MESSAGES, "", stream=True)
    response_list = [chunk async for chunk in response]
    self.assertEqual(len(response_list), 2)
    for chunk in response_list:
        if chunk.choices[0].delta.content is not None:
            self.assertEqual(chunk.choices[0].delta.content, "Hello")
```