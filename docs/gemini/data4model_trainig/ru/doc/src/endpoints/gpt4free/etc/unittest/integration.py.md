# Модуль интеграционных тестов для gpt4free
## Обзор
Модуль содержит интеграционные тесты для проверки работы различных провайдеров в gpt4free, таких как Copilot и DDG. Тесты проверяют возможность получения ответа в формате JSON от этих провайдеров как в синхронном, так и в асинхронном режимах.

## Подробнее

Этот модуль является частью набора тестов для проекта `hypotez` и предназначен для проверки интеграции с внешними API, предоставляемыми gpt4free.
Он проверяет корректность взаимодействия с Copilot и DDG, удостоверяясь, что они возвращают ответы в ожидаемом формате (JSON).
Модуль содержит как синхронные, так и асинхронные тесты для всесторонней проверки.

## Классы

### `TestProviderIntegration`

**Описание**: Класс для интеграционных тестов провайдеров.

**Наследует**: `unittest.TestCase`

**Атрибуты**:
- Отсутствуют.

**Методы**:
- `test_bing()`: Тест для проверки интеграции с провайдером Copilot.
- `test_openai()`: Тест для проверки интеграции с провайдером DDG.

### `TestChatCompletionAsync`

**Описание**: Класс для асинхронных интеграционных тестов провайдеров.

**Наследует**: `unittest.IsolatedAsyncioTestCase`

**Атрибуты**:
- Отсутствуют.

**Методы**:
- `test_bing()`: Асинхронный тест для проверки интеграции с провайдером Copilot.
- `test_openai()`: Асинхронный тест для проверки интеграции с провайдером DDG.

## Методы класса `TestProviderIntegration`

### `test_bing`

```python
def test_bing(self):
    """
    Тестирует интеграцию с провайдером Copilot.

    Args:
        self (TestProviderIntegration): Экземпляр класса TestProviderIntegration.

    Returns:
        None

    Raises:
        AssertionError: Если ответ не является экземпляром ChatCompletion или не содержит "success" в JSON.

    Как работает функция:
    1. Создается экземпляр клиента Client с провайдером Copilot.
    2. Вызывается метод create для получения ответа от провайдера.
    3. Проверяется, что ответ является экземпляром ChatCompletion.
    4. Проверяется, что ответ содержит ключ "success" в JSON.
    """
    client = Client(provider=Copilot)
    response = client.chat.completions.create(DEFAULT_MESSAGES, "", response_format={"type": "json_object"})
    self.assertIsInstance(response, ChatCompletion)
    self.assertIn("success", json.loads(response.choices[0].message.content))
```

### `test_openai`

```python
def test_openai(self):
    """
    Тестирует интеграцию с провайдером DDG (DuckDuckGo).

    Args:
        self (TestProviderIntegration): Экземпляр класса TestProviderIntegration.

    Returns:
        None

    Raises:
        AssertionError: Если ответ не является экземпляром ChatCompletion или не содержит "success" в JSON.

    Как работает функция:
    1. Создается экземпляр клиента Client с провайдером DDG.
    2. Вызывается метод create для получения ответа от провайдера.
    3. Проверяется, что ответ является экземпляром ChatCompletion.
    4. Проверяется, что ответ содержит ключ "success" в JSON.
    """
    client = Client(provider=DDG)
    response = client.chat.completions.create(DEFAULT_MESSAGES, "", response_format={"type": "json_object"})
    self.assertIsInstance(response, ChatCompletion)
    self.assertIn("success", json.loads(response.choices[0].message.content))
```

## Методы класса `TestChatCompletionAsync`

### `test_bing`

```python
async def test_bing(self):
    """
    Асинхронно тестирует интеграцию с провайдером Copilot.

    Args:
        self (TestChatCompletionAsync): Экземпляр класса TestChatCompletionAsync.

    Returns:
        None

    Raises:
        AssertionError: Если ответ не является экземпляром ChatCompletion или не содержит "success" в JSON.

    Как работает функция:
    1. Создается экземпляр асинхронного клиента AsyncClient с провайдером Copilot.
    2. Вызывается метод create для получения ответа от провайдера.
    3. Проверяется, что ответ является экземпляром ChatCompletion.
    4. Проверяется, что ответ содержит ключ "success" в JSON.
    """
    client = AsyncClient(provider=Copilot)
    response = await client.chat.completions.create(DEFAULT_MESSAGES, "", response_format={"type": "json_object"})
    self.assertIsInstance(response, ChatCompletion)
    self.assertIn("success", json.loads(response.choices[0].message.content))
```

### `test_openai`

```python
async def test_openai(self):
    """
    Асинхронно тестирует интеграцию с провайдером DDG (DuckDuckGo).

    Args:
        self (TestChatCompletionAsync): Экземпляр класса TestChatCompletionAsync.

    Returns:
        None

    Raises:
        AssertionError: Если ответ не является экземпляром ChatCompletion или не содержит "success" в JSON.

    Как работает функция:
    1. Создается экземпляр асинхронного клиента AsyncClient с провайдером DDG.
    2. Вызывается метод create для получения ответа от провайдера.
    3. Проверяется, что ответ является экземпляром ChatCompletion.
    4. Проверяется, что ответ содержит ключ "success" в JSON.
    """
    client = AsyncClient(provider=DDG)
    response = await client.chat.completions.create(DEFAULT_MESSAGES, "", response_format={"type": "json_object"})
    self.assertIsInstance(response, ChatCompletion)
    self.assertIn("success", json.loads(response.choices[0].message.content))
```

## Переменные

- `DEFAULT_MESSAGES`: Список словарей, представляющих собой сообщения по умолчанию для тестов.
  Первый элемент задаёт системное сообщение, требующее ответа в формате JSON с полем "success".
  Второй элемент задаёт пользовательское сообщение, просящее вернуть `{"success": true}` в формате JSON.

```python
DEFAULT_MESSAGES = [{"role": "system", "content": 'Response in json, Example: {"success": false}'},
                    {"role": "user", "content": "Say success true in json"}]
```

## Примеры

Пример запуска тестов:

```python
if __name__ == '__main__':
    unittest.main()