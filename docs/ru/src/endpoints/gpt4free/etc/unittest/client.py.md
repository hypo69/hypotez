# Модуль для юнит-тестов клиентской части g4f

## Обзор

Модуль содержит набор юнит-тестов для проверки корректной работы клиентской части библиотеки `g4f` (gpt4free). Он тестирует асинхронные и синхронные вызовы, передачу моделей, ограничение количества токенов, потоковую передачу данных, остановку генерации и обработку ошибок.

## Подробнее

Этот модуль использует библиотеку `unittest` для создания тестовых случаев. Он включает в себя моки провайдеров для изоляции тестов от реальных API. Тесты охватывают различные аспекты взаимодействия с клиентской частью библиотеки, такие как создание запросов, обработка ответов и управление параметрами генерации.

## Классы

### `AsyncTestPassModel`

**Описание**: Класс, содержащий асинхронные тесты для проверки функциональности клиентской части библиотеки `g4f`.

**Наследует**:
- `unittest.IsolatedAsyncioTestCase`

**Методы**:
- `test_response()`: Проверяет корректность ответа от мок-провайдера.
- `test_pass_model()`: Проверяет передачу модели через клиент.
- `test_max_tokens()`: Проверяет ограничение количества токенов в ответе.
- `test_max_stream()`: Проверяет потоковую передачу данных.
- `test_stop()`: Проверяет остановку генерации по заданному стоп-слову.

### `TestPassModel`

**Описание**: Класс, содержащий синхронные тесты для проверки функциональности клиентской части библиотеки `g4f`.

**Наследует**:
- `unittest.TestCase`

**Методы**:
- `test_response()`: Проверяет корректность ответа от мок-провайдера.
- `test_pass_model()`: Проверяет передачу модели через клиент.
- `test_max_tokens()`: Проверяет ограничение количества токенов в ответе.
- `test_max_stream()`: Проверяет потоковую передачу данных.
- `test_stop()`: Проверяет остановку генерации по заданному стоп-слову.
- `test_model_not_found()`: Проверяет возникновение исключения `ModelNotFoundError` при отсутствии модели.
- `test_best_provider()`: Проверяет выбор лучшего провайдера для заданной модели.
- `test_default_model()`: Проверяет использование модели по умолчанию.
- `test_provider_as_model()`: Проверяет использование провайдера в качестве модели.
- `test_get_model()`: Проверяет получение модели.

## Функции

### `AsyncTestPassModel.test_response`

```python
    async def test_response(self):
        """
        Проверяет корректность ответа от мок-провайдера.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если полученный ответ не является экземпляром класса `ChatCompletion` или содержимое ответа не соответствует ожидаемому значению "Mock".
        """
```

**Как работает функция**:
1. Создается экземпляр `AsyncClient` с использованием мок-провайдера `AsyncGeneratorProviderMock`.
2. Вызывается метод `client.chat.completions.create` с параметрами по умолчанию.
3. Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
4. Проверяется, что содержимое ответа соответствует ожидаемому значению "Mock".

**Примеры**:
```python
# Пример использования в тестовом классе
class AsyncTestPassModel(unittest.IsolatedAsyncioTestCase):
    async def test_response(self):
        client = AsyncClient(provider=AsyncGeneratorProviderMock)
        response = await client.chat.completions.create(DEFAULT_MESSAGES, "")
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("Mock", response.choices[0].message.content)
```

### `AsyncTestPassModel.test_pass_model`

```python
    async def test_pass_model(self):
        """
        Проверяет передачу модели через клиент.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если полученный ответ не является экземпляром класса `ChatCompletion` или содержимое ответа не соответствует ожидаемому значению "Hello".
        """
```

**Как работает функция**:
1. Создается экземпляр `AsyncClient` с использованием мок-провайдера `ModelProviderMock`.
2. Вызывается метод `client.chat.completions.create` с параметрами по умолчанию.
3. Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
4. Проверяется, что содержимое ответа соответствует ожидаемому значению "Hello".

**Примеры**:
```python
# Пример использования в тестовом классе
class AsyncTestPassModel(unittest.IsolatedAsyncioTestCase):
    async def test_pass_model(self):
        client = AsyncClient(provider=ModelProviderMock)
        response = await client.chat.completions.create(DEFAULT_MESSAGES, "Hello")
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("Hello", response.choices[0].message.content)
```

### `AsyncTestPassModel.test_max_tokens`

```python
    async def test_max_tokens(self):
        """
        Проверяет ограничение количества токенов в ответе.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если полученный ответ не является экземпляром класса `ChatCompletion` или содержимое ответа не соответствует ожидаемому значению.
        """
```

**Как работает функция**:
1. Создается экземпляр `AsyncClient` с использованием мок-провайдера `YieldProviderMock`.
2. Формируется список сообщений, каждое из которых содержит отдельное слово.
3. Вызывается метод `client.chat.completions.create` с ограничением `max_tokens=1`.
4. Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
5. Проверяется, что содержимое ответа соответствует ожидаемому значению "How ".
6. Вызывается метод `client.chat.completions.create` с ограничением `max_tokens=2`.
7. Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
8. Проверяется, что содержимое ответа соответствует ожидаемому значению "How are ".

**Примеры**:
```python
# Пример использования в тестовом классе
class AsyncTestPassModel(unittest.IsolatedAsyncioTestCase):
    async def test_max_tokens(self):
        client = AsyncClient(provider=YieldProviderMock)
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        response = await client.chat.completions.create(messages, "Hello", max_tokens=1)
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("How ", response.choices[0].message.content)
        response = await client.chat.completions.create(messages, "Hello", max_tokens=2)
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("How are ", response.choices[0].message.content)
```

### `AsyncTestPassModel.test_max_stream`

```python
    async def test_max_stream(self):
        """
        Проверяет потоковую передачу данных.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если полученный чанк не является экземпляром класса `ChatCompletionChunk` или содержимое ответа не соответствует ожидаемому значению.
        """
```

**Как работает функция**:
1. Создается экземпляр `AsyncClient` с использованием мок-провайдера `YieldProviderMock`.
2. Формируется список сообщений, каждое из которых содержит отдельное слово.
3. Вызывается метод `client.chat.completions.create` в режиме потоковой передачи (`stream=True`).
4. Итерируется по чанкам ответа и проверяется, что каждый чанк является экземпляром класса `ChatCompletionChunk`.
5. Проверяется, что содержимое каждого чанка является строкой.
6. Вызывается метод `client.chat.completions.create` в режиме потоковой передачи с ограничением `max_tokens=2`.
7. Собирается список чанков ответа.
8. Проверяется, что количество чанков равно 3.
9. Проверяется, что содержимое каждого чанка соответствует ожидаемому значению "You ".

**Примеры**:
```python
# Пример использования в тестовом классе
class AsyncTestPassModel(unittest.IsolatedAsyncioTestCase):
    async def test_max_stream(self):
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
```

### `AsyncTestPassModel.test_stop`

```python
    async def test_stop(self):
        """
        Проверяет остановку генерации по заданному стоп-слову.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если полученный ответ не является экземпляром класса `ChatCompletion` или содержимое ответа не соответствует ожидаемому значению "How are you?".
        """
```

**Как работает функция**:
1. Создается экземпляр `AsyncClient` с использованием мок-провайдера `YieldProviderMock`.
2. Формируется список сообщений, каждое из которых содержит отдельное слово.
3. Вызывается метод `client.chat.completions.create` с параметром `stop=["and"]`.
4. Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
5. Проверяется, что содержимое ответа соответствует ожидаемому значению "How are you?".

**Примеры**:
```python
# Пример использования в тестовом классе
class AsyncTestPassModel(unittest.IsolatedAsyncioTestCase):
    async def test_stop(self):
        client = AsyncClient(provider=YieldProviderMock)
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        response = await client.chat.completions.create(messages, "Hello", stop=["and"])
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("How are you?", response.choices[0].message.content)
```

### `TestPassModel.test_response`

```python
    def test_response(self):
        """
        Проверяет корректность ответа от мок-провайдера.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если полученный ответ не является экземпляром класса `ChatCompletion` или содержимое ответа не соответствует ожидаемому значению "Mock".
        """
```

**Как работает функция**:
1. Создается экземпляр `Client` с использованием мок-провайдера `AsyncGeneratorProviderMock`.
2. Вызывается метод `client.chat.completions.create` с параметрами по умолчанию.
3. Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
4. Проверяется, что содержимое ответа соответствует ожидаемому значению "Mock".

**Примеры**:
```python
# Пример использования в тестовом классе
class TestPassModel(unittest.TestCase):
    def test_response(self):
        client = Client(provider=AsyncGeneratorProviderMock)
        response = client.chat.completions.create(DEFAULT_MESSAGES, "")
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("Mock", response.choices[0].message.content)
```

### `TestPassModel.test_pass_model`

```python
    def test_pass_model(self):
        """
        Проверяет передачу модели через клиент.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если полученный ответ не является экземпляром класса `ChatCompletion` или содержимое ответа не соответствует ожидаемому значению "Hello".
        """
```

**Как работает функция**:
1. Создается экземпляр `Client` с использованием мок-провайдера `ModelProviderMock`.
2. Вызывается метод `client.chat.completions.create` с параметрами по умолчанию.
3. Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
4. Проверяется, что содержимое ответа соответствует ожидаемому значению "Hello".

**Примеры**:
```python
# Пример использования в тестовом классе
class TestPassModel(unittest.TestCase):
    def test_pass_model(self):
        client = Client(provider=ModelProviderMock)
        response = client.chat.completions.create(DEFAULT_MESSAGES, "Hello")
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("Hello", response.choices[0].message.content)
```

### `TestPassModel.test_max_tokens`

```python
    def test_max_tokens(self):
        """
        Проверяет ограничение количества токенов в ответе.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если полученный ответ не является экземпляром класса `ChatCompletion` или содержимое ответа не соответствует ожидаемому значению.
        """
```

**Как работает функция**:
1. Создается экземпляр `Client` с использованием мок-провайдера `YieldProviderMock`.
2. Формируется список сообщений, каждое из которых содержит отдельное слово.
3. Вызывается метод `client.chat.completions.create` с ограничением `max_tokens=1`.
4. Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
5. Проверяется, что содержимое ответа соответствует ожидаемому значению "How ".
6. Вызывается метод `client.chat.completions.create` с ограничением `max_tokens=2`.
7. Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
8. Проверяется, что содержимое ответа соответствует ожидаемому значению "How are ".

**Примеры**:
```python
# Пример использования в тестовом классе
class TestPassModel(unittest.TestCase):
    def test_max_tokens(self):
        client = Client(provider=YieldProviderMock)
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        response = client.chat.completions.create(messages, "Hello", max_tokens=1)
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("How ", response.choices[0].message.content)
        response = client.chat.completions.create(messages, "Hello", max_tokens=2)
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("How are ", response.choices[0].message.content)
```

### `TestPassModel.test_max_stream`

```python
    def test_max_stream(self):
        """
        Проверяет потоковую передачу данных.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если полученный чанк не является экземпляром класса `ChatCompletionChunk` или содержимое ответа не соответствует ожидаемому значению.
        """
```

**Как работает функция**:
1. Создается экземпляр `Client` с использованием мок-провайдера `YieldProviderMock`.
2. Формируется список сообщений, каждое из которых содержит отдельное слово.
3. Вызывается метод `client.chat.completions.create` в режиме потоковой передачи (`stream=True`).
4. Итерируется по чанкам ответа и проверяется, что каждый чанк является экземпляром класса `ChatCompletionChunk`.
5. Проверяется, что содержимое каждого чанка является строкой.
6. Вызывается метод `client.chat.completions.create` в режиме потоковой передачи с ограничением `max_tokens=2`.
7. Собирается список чанков ответа.
8. Проверяется, что количество чанков равно 3.
9. Проверяется, что содержимое каждого чанка соответствует ожидаемому значению "You ".

**Примеры**:
```python
# Пример использования в тестовом классе
class TestPassModel(unittest.TestCase):
    def test_max_stream(self):
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
```

### `TestPassModel.test_stop`

```python
    def test_stop(self):
        """
        Проверяет остановку генерации по заданному стоп-слову.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если полученный ответ не является экземпляром класса `ChatCompletion` или содержимое ответа не соответствует ожидаемому значению "How are you?".
        """
```

**Как работает функция**:
1. Создается экземпляр `Client` с использованием мок-провайдера `YieldProviderMock`.
2. Формируется список сообщений, каждое из которых содержит отдельное слово.
3. Вызывается метод `client.chat.completions.create` с параметром `stop=["and"]`.
4. Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
5. Проверяется, что содержимое ответа соответствует ожидаемому значению "How are you?".

**Примеры**:
```python
# Пример использования в тестовом классе
class TestPassModel(unittest.TestCase):
    def test_stop(self):
        client = Client(provider=YieldProviderMock)
        messages = [{'role': 'user', 'content': chunk} for chunk in ["How ", "are ", "you", "?"]]
        response = client.chat.completions.create(messages, "Hello", stop=["and"])
        self.assertIsInstance(response, ChatCompletion)
        self.assertEqual("How are you?", response.choices[0].message.content)
```

### `TestPassModel.test_model_not_found`

```python
    def test_model_not_found(self):
        """
        Проверяет возникновение исключения `ModelNotFoundError` при отсутствии модели.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если не возникает исключение `ModelNotFoundError`.
        """
```

**Как работает функция**:
1. Определяется внутренняя функция `run_exception`, которая создает экземпляр `Client` без указания провайдера и вызывает метод `client.chat.completions.create`.
2. Вызывается метод `self.assertRaises` для проверки того, что при вызове `run_exception` возникает исключение `ModelNotFoundError`.

**Внутренние функции**:
- `run_exception()`: Функция, которая пытается создать запрос без указания модели, чтобы вызвать исключение `ModelNotFoundError`.

**Примеры**:
```python
# Пример использования в тестовом классе
class TestPassModel(unittest.TestCase):
    def test_model_not_found(self):
        def run_exception():
            client = Client()
            client.chat.completions.create(DEFAULT_MESSAGES, "Hello")
        self.assertRaises(ModelNotFoundError, run_exception)
```

### `TestPassModel.test_best_provider`

```python
    def test_best_provider(self):
        """
        Проверяет выбор лучшего провайдера для заданной модели.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если у провайдера отсутствует атрибут `create_completion` или модель не соответствует ожидаемому значению.
        """
```

**Как работает функция**:
1. Определяется модель `not_default_model` как "gpt-4o".
2. Вызывается функция `get_model_and_provider` для получения модели и провайдера.
3. Проверяется, что у провайдера есть атрибут `create_completion`.
4. Проверяется, что модель соответствует ожидаемому значению "gpt-4o".

**Примеры**:
```python
# Пример использования в тестовом классе
class TestPassModel(unittest.TestCase):
    def test_best_provider(self):
        not_default_model = "gpt-4o"
        model, provider = get_model_and_provider(not_default_model, None, False)
        self.assertTrue(hasattr(provider, "create_completion"))
        self.assertEqual(model, not_default_model)
```

### `TestPassModel.test_default_model`

```python
    def test_default_model(self):
        """
        Проверяет использование модели по умолчанию.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если у провайдера отсутствует атрибут `create_completion` или модель не соответствует ожидаемому значению.
        """
```

**Как работает функция**:
1. Определяется модель `default_model` как "".
2. Вызывается функция `get_model_and_provider` для получения модели и провайдера.
3. Проверяется, что у провайдера есть атрибут `create_completion`.
4. Проверяется, что модель соответствует ожидаемому значению "".

**Примеры**:
```python
# Пример использования в тестовом классе
class TestPassModel(unittest.TestCase):
    def test_default_model(self):
        default_model = ""
        model, provider = get_model_and_provider(default_model, None, False)
        self.assertTrue(hasattr(provider, "create_completion"))
        self.assertEqual(model, default_model)
```

### `TestPassModel.test_provider_as_model`

```python
    def test_provider_as_model(self):
        """
        Проверяет использование провайдера в качестве модели.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если у провайдера отсутствует атрибут `create_completion` или модель не является строкой или модель не соответствует ожидаемому значению `Copilot.default_model`.
        """
```

**Как работает функция**:
1. Определяется модель `provider_as_model` как имя класса `Copilot`.
2. Вызывается функция `get_model_and_provider` для получения модели и провайдера.
3. Проверяется, что у провайдера есть атрибут `create_completion`.
4. Проверяется, что модель является строкой.
5. Проверяется, что модель соответствует значению `Copilot.default_model`.

**Примеры**:
```python
# Пример использования в тестовом классе
class TestPassModel(unittest.TestCase):
    def test_provider_as_model(self):
        provider_as_model = Copilot.__name__
        model, provider = get_model_and_provider(provider_as_model, None, False)
        self.assertTrue(hasattr(provider, "create_completion"))
        self.assertIsInstance(model, str)
        self.assertEqual(model, Copilot.default_model)
```

### `TestPassModel.test_get_model`

```python
    def test_get_model(self):
        """
        Проверяет получение модели.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если у провайдера отсутствует атрибут `create_completion` или модель не соответствует ожидаемому значению `gpt_4o.name`.
        """
```

**Как работает функция**:
1. Вызывается функция `get_model_and_provider` с именем модели `gpt_4o.name`.
2. Проверяется, что у провайдера есть атрибут `create_completion`.
3. Проверяется, что модель соответствует значению `gpt_4o.name`.

**Примеры**:
```python
# Пример использования в тестовом классе
class TestPassModel(unittest.TestCase):
    def test_get_model(self):
        model, provider = get_model_and_provider(gpt_4o.name, None, False)
        self.assertTrue(hasattr(provider, "create_completion"))
        self.assertEqual(model, gpt_4o.name)