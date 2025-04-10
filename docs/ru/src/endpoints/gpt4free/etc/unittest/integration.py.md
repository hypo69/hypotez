# Модуль интеграционного тестирования провайдеров gpt4free
## Обзор

Модуль `integration.py` выполняет интеграционные тесты для различных провайдеров, используемых в библиотеке `gpt4free`. Он проверяет правильность взаимодействия с провайдерами, такими как Copilot и DDG (DuckDuckGo), через асинхронные и синхронные клиенты. Цель - убедиться, что основные функции работают как ожидается, и ответы соответствуют заданным требованиям (например, возвращаются в формате JSON).
## Подробнее

В данном модуле определены классы `TestProviderIntegration` и `TestChatCompletionAsync`, которые содержат наборы тестов для проверки интеграции с различными провайдерами. Тесты используют библиотеку `unittest` для автоматизированного тестирования функциональности. Основная задача тестов - убедиться, что клиенты могут успешно взаимодействовать с провайдерами, отправлять запросы и получать ответы в ожидаемом формате (JSON).

## Классы

### `TestProviderIntegration`

**Описание**: Класс содержит интеграционные тесты для синхронных клиентов библиотеки `gpt4free`.

**Принцип работы**:

1.  Инициализируется клиент `Client` с указанным провайдером (например, `Copilot` или `DDG`).
2.  Отправляется запрос `chat.completions.create` с заданными сообщениями `DEFAULT_MESSAGES` и указанием формата ответа `response_format={"type": "json_object"}`.
3.  Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
4.  Проверяется, что ответ содержит ожидаемый ключ `"success"` в JSON.

**Методы**:

*   `test_bing`: Тест интеграции с провайдером `Copilot`.
*   `test_openai`: Тест интеграции с провайдером `DDG`.

### `TestChatCompletionAsync`

**Описание**: Класс содержит интеграционные тесты для асинхронных клиентов библиотеки `gpt4free`.

**Принцип работы**:

1.  Инициализируется асинхронный клиент `AsyncClient` с указанным провайдером (например, `Copilot` или `DDG`).
2.  Отправляется асинхронный запрос `chat.completions.create` с заданными сообщениями `DEFAULT_MESSAGES` и указанием формата ответа `response_format={"type": "json_object"}`.
3.  Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
4.  Проверяется, что ответ содержит ожидаемый ключ `"success"` в JSON.

**Методы**:

*   `test_bing`: Асинхронный тест интеграции с провайдером `Copilot`.
*   `test_openai`: Асинхронный тест интеграции с провайдером `DDG`.

## Функции

### `test_bing` (в классе `TestProviderIntegration`)

```python
def test_bing(self):
    """Тестирует интеграцию с провайдером Copilot (Bing).

    Создает синхронного клиента с провайдером Copilot, отправляет запрос на завершение чата,
    проверяет, что ответ является экземпляром ChatCompletion и содержит ключ "success" в JSON.
    """
    ...
```

**Назначение**: Тестирование интеграции с провайдером `Copilot` (Bing) через синхронный клиент.

**Параметры**:

*   `self` (TestProviderIntegration): Экземпляр класса `TestProviderIntegration`.

**Возвращает**: None

**Вызывает исключения**: Не вызывает.

**Как работает функция**:

1.  **Инициализация клиента**: Создается экземпляр класса `Client` с указанием провайдера `Copilot`.

2.  **Создание запроса**: Формируется запрос к API `chat.completions.create` с использованием `DEFAULT_MESSAGES` и указанием формата ответа в виде JSON (`response_format={"type": "json_object"}`).

3.  **Проверка типа ответа**: Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.

4.  **Проверка содержимого ответа**: Извлекается содержимое ответа в формате JSON и проверяется наличие ключа `"success"`.

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
    """Тестирует интеграцию с провайдером DDG (DuckDuckGo).

    Создает синхронного клиента с провайдером DDG, отправляет запрос на завершение чата,
    проверяет, что ответ является экземпляром ChatCompletion и содержит ключ "success" в JSON.
    """
    ...
```

**Назначение**: Тестирование интеграции с провайдером `DDG` (DuckDuckGo) через синхронный клиент.

**Параметры**:

*   `self` (TestProviderIntegration): Экземпляр класса `TestProviderIntegration`.

**Возвращает**: None

**Вызывает исключения**: Не вызывает.

**Как работает функция**:

1.  **Инициализация клиента**: Создается экземпляр класса `Client` с указанием провайдера `DDG`.

2.  **Создание запроса**: Формируется запрос к API `chat.completions.create` с использованием `DEFAULT_MESSAGES` и указанием формата ответа в виде JSON (`response_format={"type": "json_object"}`).

3.  **Проверка типа ответа**: Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.

4.  **Проверка содержимого ответа**: Извлекается содержимое ответа в формате JSON и проверяется наличие ключа `"success"`.

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
    """Тестирует асинхронную интеграцию с провайдером Copilot (Bing).

    Создает асинхронного клиента с провайдером Copilot, отправляет асинхронный запрос на завершение чата,
    проверяет, что ответ является экземпляром ChatCompletion и содержит ключ "success" в JSON.
    """
    ...
```

**Назначение**: Асинхронное тестирование интеграции с провайдером `Copilot` (Bing).

**Параметры**:

*   `self` (TestChatCompletionAsync): Экземпляр класса `TestChatCompletionAsync`.

**Возвращает**: None

**Вызывает исключения**: Не вызывает.

**Как работает функция**:

1.  **Инициализация асинхронного клиента**: Создается экземпляр класса `AsyncClient` с указанием провайдера `Copilot`.

2.  **Создание асинхронного запроса**: Формируется асинхронный запрос к API `chat.completions.create` с использованием `DEFAULT_MESSAGES` и указанием формата ответа в виде JSON (`response_format={"type": "json_object"}`).

3.  **Проверка типа ответа**: Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.

4.  **Проверка содержимого ответа**: Извлекается содержимое ответа в формате JSON и проверяется наличие ключа `"success"`.

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
    """Тестирует асинхронную интеграцию с провайдером DDG (DuckDuckGo).

    Создает асинхронного клиента с провайдером DDG, отправляет асинхронный запрос на завершение чата,
    проверяет, что ответ является экземпляром ChatCompletion и содержит ключ "success" в JSON.
    """
    ...
```

**Назначение**: Асинхронное тестирование интеграции с провайдером `DDG` (DuckDuckGo).

**Параметры**:

*   `self` (TestChatCompletionAsync): Экземпляр класса `TestChatCompletionAsync`.

**Возвращает**: None

**Вызывает исключения**: Не вызывает.

**Как работает функция**:

1.  **Инициализация асинхронного клиента**: Создается экземпляр класса `AsyncClient` с указанием провайдера `DDG`.

2.  **Создание асинхронного запроса**: Формируется асинхронный запрос к API `chat.completions.create` с использованием `DEFAULT_MESSAGES` и указанием формата ответа в виде JSON (`response_format={"type": "json_object"}`).

3.  **Проверка типа ответа**: Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.

4.  **Проверка содержимого ответа**: Извлекается содержимое ответа в формате JSON и проверяется наличие ключа `"success"`.

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

### `DEFAULT_MESSAGES`

```python
DEFAULT_MESSAGES = [{"role": "system", "content": 'Response in json, Example: {"success": false}'},
                    {"role": "user", "content": "Say success true in json"}]
```

**Описание**: Список сообщений, используемых по умолчанию для запросов к провайдерам.

**Назначение**: Определяет структуру запроса, отправляемого в тестах. Содержит системное сообщение, указывающее на ожидаемый формат ответа (JSON с ключом "success"), и пользовательское сообщение с запросом вернуть JSON с `success: true`.

**Тип**: `List[Dict[str, str]]`

## Запуск тестов

```python
if __name__ == '__main__':
    unittest.main()
```

**Описание**: Запускает тесты, если скрипт вызывается напрямую.

**Назначение**: Обеспечивает возможность запуска тестов из командной строки с помощью `python integration.py`.