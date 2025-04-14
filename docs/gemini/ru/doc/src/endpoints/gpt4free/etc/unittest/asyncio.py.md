# Модуль для юнит-тестов асинхронных операций в gpt4free
========================================================

Модуль содержит набор тестов для проверки асинхронной функциональности `ChatCompletion` в библиотеке `gpt4free`. В частности, проверяется корректность обработки исключений, асинхронного создания чатов и работы с генераторами.

## Обзор

Этот модуль предназначен для тестирования асинхронных функций, связанных с `ChatCompletion` в библиотеке `gpt4free`. Он использует `unittest` и `asyncio` для проведения тестов, а также включает моки для имитации поведения провайдеров.

## Подробней

Модуль содержит три класса для тестирования: `TestChatCompletion`, `TestChatCompletionAsync` и `TestChatCompletionNestAsync`. Каждый класс тестирует различные аспекты асинхронной работы `ChatCompletion`, включая обработку исключений, асинхронное создание чатов и использование генераторов.

## Классы

### `TestChatCompletion`

**Описание**: Класс содержит тесты для синхронной работы `ChatCompletion` с использованием асинхронных моков.
**Наследует**: `unittest.TestCase`

**Методы**:
- `run_exception()`: Запускает `ChatCompletion.create` с асинхронным провайдером и возвращает результат.
- `test_exception()`: Проверяет, что при попытке синхронного запуска асинхронной функции без установленного `nest_asyncio` возникает исключение `g4f.errors.NestAsyncioError`.
- `test_create()`: Проверяет создание `ChatCompletion` с асинхронным провайдером.
- `test_create_generator()`: Проверяет создание `ChatCompletion` с асинхронным провайдером, возвращающим генератор.
- `test_await_callback()`: Тестирует асинхронный вызов `client.chat.completions.create`.

#### `run_exception`

```python
    async def run_exception(self):
        """ Запускает ChatCompletion.create с асинхронным провайдером и возвращает результат.
        Args:
            None

        Returns:
            ChatCompletion.create: Результат выполнения ChatCompletion.create.

        Raises:
            None
        """
        ...
```

#### `test_exception`

```python
    def test_exception(self):
        """ Проверяет, что при попытке синхронного запуска асинхронной функции без установленного nest_asyncio возникает исключение g4f.errors.NestAsyncioError.

        Args:
            None

        Returns:
            None

        Raises:
            g4f.errors.NestAsyncioError: Если nest_asyncio не установлен.
        """
        ...
```

#### `test_create`

```python
    def test_create(self):
        """ Проверяет создание ChatCompletion с асинхронным провайдером.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если результат не равен "Mock".
        """
        ...
```

#### `test_create_generator`

```python
    def test_create_generator(self):
        """ Проверяет создание ChatCompletion с асинхронным провайдером, возвращающим генератор.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если результат не равен "Mock".
        """
        ...
```

#### `test_await_callback`

```python
    def test_await_callback(self):
        """ Тестирует асинхронный вызов client.chat.completions.create.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если результат не равен "Mock".
        """
        ...
```

### `TestChatCompletionAsync`

**Описание**: Класс содержит тесты для проверки асинхронного создания чатов с использованием `ChatCompletion.create_async`.
**Наследует**: `unittest.IsolatedAsyncioTestCase`

**Методы**:
- `test_base()`: Проверяет асинхронное создание чата с синхронным провайдером.
- `test_async()`: Проверяет асинхронное создание чата с асинхронным провайдером.
- `test_create_generator()`: Проверяет асинхронное создание чата с асинхронным провайдером, возвращающим генератор.

#### `test_base`

```python
    async def test_base(self):
        """ Проверяет асинхронное создание чата с синхронным провайдером.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если результат не равен "Mock".
        """
        ...
```

#### `test_async`

```python
    async def test_async(self):
        """ Проверяет асинхронное создание чата с асинхронным провайдером.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если результат не равен "Mock".
        """
        ...
```

#### `test_create_generator`

```python
    async def test_create_generator(self):
        """ Проверяет асинхронное создание чата с асинхронным провайдером, возвращающим генератор.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если результат не равен "Mock".
        """
        ...
```

### `TestChatCompletionNestAsync`

**Описание**: Класс содержит тесты для проверки вложенных асинхронных вызовов с использованием `nest_asyncio`.
**Наследует**: `unittest.IsolatedAsyncioTestCase`

**Методы**:
- `setUp()`: Применяет `nest_asyncio`, если он установлен.
- `test_create()`: Проверяет асинхронное создание чата с синхронным провайдером.
- `_test_nested()`: Проверяет вложенный вызов `ChatCompletion.create` с асинхронным провайдером.
- `_test_nested_generator()`: Проверяет вложенный вызов `ChatCompletion.create` с асинхронным провайдером, возвращающим генератор.

#### `setUp`

```python
    def setUp(self) -> None:
        """ Применяет nest_asyncio, если он установлен.

        Args:
            None

        Returns:
            None

        Raises:
            unittest.SkipTest: Если nest_asyncio не установлен.
        """
        ...
```

#### `test_create`

```python
    async def test_create(self):
        """ Проверяет асинхронное создание чата с синхронным провайдером.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если результат не равен "Mock".
        """
        ...
```

#### `_test_nested`

```python
    async def _test_nested(self):
        """ Проверяет вложенный вызов ChatCompletion.create с асинхронным провайдером.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если результат не равен "Mock".
        """
        ...
```

#### `_test_nested_generator`

```python
    async def _test_nested_generator(self):
        """ Проверяет вложенный вызов ChatCompletion.create с асинхронным провайдером, возвращающим генератор.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: Если результат не равен "Mock".
        """
        ...
```

## Параметры классов

- `DEFAULT_MESSAGES`: Список сообщений по умолчанию для использования в тестах.

## Зависимости

- `asyncio`: Для асинхронного программирования.
- `unittest`: Для модульного тестирования.
- `g4f`: Библиотека для работы с GPT-4.
- `nest_asyncio`: Для поддержки вложенных асинхронных вызовов (опционально).
- `.mocks`: Модуль с моками провайдеров.

## Примеры

```python
import unittest
import asyncio

from .mocks import AsyncProviderMock
from g4f import ChatCompletion, models

DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]

class TestChatCompletionAsync(unittest.IsolatedAsyncioTestCase):

    async def test_async(self):
        result = await ChatCompletion.create_async(models.default, DEFAULT_MESSAGES, AsyncProviderMock)
        self.assertEqual("Mock", result)

if __name__ == '__main__':
    unittest.main()