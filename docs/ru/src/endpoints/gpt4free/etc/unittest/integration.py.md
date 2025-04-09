# Модуль интеграционного тестирования провайдеров g4f
## Обзор

Модуль `integration.py` содержит интеграционные тесты для провайдеров `g4f`, таких как Copilot и DDG (DuckDuckGo). Он проверяет, что клиенты `g4f` правильно взаимодействуют с этими провайдерами, возвращая ожидаемые ответы в формате JSON.

## Подробнее

Этот модуль использует библиотеку `unittest` для определения тестовых случаев. Он проверяет, что при запросе к провайдерам возвращается ответ, содержащий JSON с ключом "success".
Тесты выполняются как синхронно, так и асинхронно, чтобы проверить оба варианта использования.
В данном модуле определены два класса: `TestProviderIntegration` и `TestChatCompletionAsync`.

## Классы

### `TestProviderIntegration`

**Описание**: Класс, содержащий интеграционные тесты для синхронных клиентов `g4f`.
**Наследует**: `unittest.TestCase`
**Методы**:

- `test_bing()`: Тест для провайдера Copilot.
- `test_openai()`: Тест для провайдера DDG.

### `TestChatCompletionAsync`

**Описание**: Класс, содержащий интеграционные тесты для асинхронных клиентов `g4f`.
**Наследует**: `unittest.IsolatedAsyncioTestCase`
**Методы**:

- `test_bing()`: Асинхронный тест для провайдера Copilot.
- `test_openai()`: Асинхронный тест для провайдера DDG.

## Функции

### `test_bing` (в классе `TestProviderIntegration`)

```python
def test_bing(self):
    """
    Тестирует интеграцию с провайдером Copilot для синхронного клиента.

    Args:
        self (TestProviderIntegration): Экземпляр класса TestProviderIntegration.

    Returns:
        None

    Raises:
        AssertionError: Если ответ не является экземпляром ChatCompletion или не содержит ключ "success" в JSON.
    """
```

**Назначение**: Тестирует интеграцию с провайдером Copilot для синхронного клиента.

**Как работает функция**:

1.  **Создание клиента**: Создается экземпляр класса `Client` с провайдером `Copilot`.
2.  **Выполнение запроса**: Выполняется запрос к `client.chat.completions.create` с предопределенными сообщениями, указанием формата ответа как JSON.
3.  **Проверка типа ответа**: Проверяется, что ответ является экземпляром класса `ChatCompletion`.
4.  **Проверка содержимого ответа**: Проверяется, что ответ содержит ключ "success" после загрузки JSON из содержимого ответа.

```
      Создание клиента
      │
      Выполнение запроса
      │
      Проверка типа ответа
      │
      Проверка содержимого ответа
```

**Примеры**:

```python
import unittest
from g4f.client import Client, ChatCompletion
from g4f.Provider import Copilot
import json

class TestProviderIntegration(unittest.TestCase):
    def test_bing(self):
        client = Client(provider=Copilot)
        response = client.chat.completions.create([{"role": "system", "content": 'Response in json, Example: {"success": false}'},
                                    {"role": "user", "content": "Say success true in json"}], "", response_format={"type": "json_object"})
        self.assertIsInstance(response, ChatCompletion)
        self.assertIn("success", json.loads(response.choices[0].message.content))
```

### `test_openai` (в классе `TestProviderIntegration`)

```python
def test_openai(self):
    """
    Тестирует интеграцию с провайдером DDG для синхронного клиента.

    Args:
        self (TestProviderIntegration): Экземпляр класса TestProviderIntegration.

    Returns:
        None

    Raises:
        AssertionError: Если ответ не является экземпляром ChatCompletion или не содержит ключ "success" в JSON.
    """
```

**Назначение**: Тестирует интеграцию с провайдером DDG (DuckDuckGo) для синхронного клиента.

**Как работает функция**:

1.  **Создание клиента**: Создается экземпляр класса `Client` с провайдером `DDG`.
2.  **Выполнение запроса**: Выполняется запрос к `client.chat.completions.create` с предопределенными сообщениями, указанием формата ответа как JSON.
3.  **Проверка типа ответа**: Проверяется, что ответ является экземпляром класса `ChatCompletion`.
4.  **Проверка содержимого ответа**: Проверяется, что ответ содержит ключ "success" после загрузки JSON из содержимого ответа.

```
      Создание клиента
      │
      Выполнение запроса
      │
      Проверка типа ответа
      │
      Проверка содержимого ответа
```

**Примеры**:

```python
import unittest
from g4f.client import Client, ChatCompletion
from g4f.Provider import DDG
import json

class TestProviderIntegration(unittest.TestCase):
    def test_openai(self):
        client = Client(provider=DDG)
        response = client.chat.completions.create([{"role": "system", "content": 'Response in json, Example: {"success": false}'},
                                    {"role": "user", "content": "Say success true in json"}], "", response_format={"type": "json_object"})
        self.assertIsInstance(response, ChatCompletion)
        self.assertIn("success", json.loads(response.choices[0].message.content))
```

### `test_bing` (в классе `TestChatCompletionAsync`)

```python
async def test_bing(self):
    """
    Асинхронно тестирует интеграцию с провайдером Copilot.

    Args:
        self (TestChatCompletionAsync): Экземпляр класса TestChatCompletionAsync.

    Returns:
        None

    Raises:
        AssertionError: Если ответ не является экземпляром ChatCompletion или не содержит ключ "success" в JSON.
    """
```

**Назначение**: Асинхронно тестирует интеграцию с провайдером Copilot.

**Как работает функция**:

1.  **Создание клиента**: Создается экземпляр класса `AsyncClient` с провайдером `Copilot`.
2.  **Выполнение запроса**: Выполняется асинхронный запрос к `client.chat.completions.create` с предопределенными сообщениями, указанием формата ответа как JSON.
3.  **Проверка типа ответа**: Проверяется, что ответ является экземпляром класса `ChatCompletion`.
4.  **Проверка содержимого ответа**: Проверяется, что ответ содержит ключ "success" после загрузки JSON из содержимого ответа.

```
      Создание клиента
      │
      Выполнение запроса
      │
      Проверка типа ответа
      │
      Проверка содержимого ответа
```

**Примеры**:

```python
import unittest
from g4f.client import AsyncClient, ChatCompletion
from g4f.Provider import Copilot
import json
import asyncio

class TestChatCompletionAsync(unittest.IsolatedAsyncioTestCase):
    async def test_bing(self):
        client = AsyncClient(provider=Copilot)
        response = await client.chat.completions.create([{"role": "system", "content": 'Response in json, Example: {"success": false}'},
                                    {"role": "user", "content": "Say success true in json"}], "", response_format={"type": "json_object"})
        self.assertIsInstance(response, ChatCompletion)
        self.assertIn("success", json.loads(response.choices[0].message.content))
```

### `test_openai` (в классе `TestChatCompletionAsync`)

```python
async def test_openai(self):
    """
    Асинхронно тестирует интеграцию с провайдером DDG.

    Args:
        self (TestChatCompletionAsync): Экземпляр класса TestChatCompletionAsync.

    Returns:
        None

    Raises:
        AssertionError: Если ответ не является экземпляром ChatCompletion или не содержит ключ "success" в JSON.
    """
```

**Назначение**: Асинхронно тестирует интеграцию с провайдером DDG (DuckDuckGo).

**Как работает функция**:

1.  **Создание клиента**: Создается экземпляр класса `AsyncClient` с провайдером `DDG`.
2.  **Выполнение запроса**: Выполняется асинхронный запрос к `client.chat.completions.create` с предопределенными сообщениями, указанием формата ответа как JSON.
3.  **Проверка типа ответа**: Проверяется, что ответ является экземпляром класса `ChatCompletion`.
4.  **Проверка содержимого ответа**: Проверяется, что ответ содержит ключ "success" после загрузки JSON из содержимого ответа.

```
      Создание клиента
      │
      Выполнение запроса
      │
      Проверка типа ответа
      │
      Проверка содержимого ответа
```

**Примеры**:

```python
import unittest
from g4f.client import AsyncClient, ChatCompletion
from g4f.Provider import DDG
import json
import asyncio

class TestChatCompletionAsync(unittest.IsolatedAsyncioTestCase):
    async def test_openai(self):
        client = AsyncClient(provider=DDG)
        response = await client.chat.completions.create([{"role": "system", "content": 'Response in json, Example: {"success": false}'},
                                    {"role": "user", "content": "Say success true in json"}], "", response_format={"type": "json_object"})
        self.assertIsInstance(response, ChatCompletion)
        self.assertIn("success", json.loads(response.choices[0].message.content))
```

###

### DEFAULT_MESSAGES

```python
DEFAULT_MESSAGES = [{"role": "system", "content": 'Response in json, Example: {"success": false}'},
                    {"role": "user", "content": "Say success true in json"}]
```

**Описание**: Список сообщений, используемый по умолчанию для запросов к провайдерам.
Первое сообщение задает системную роль, указывая, что ответ должен быть в формате JSON.
Второе сообщение содержит запрос пользователя с просьбой вернуть JSON с ключом "success" установленным в true.