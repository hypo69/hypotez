# Модуль тестирования асинхронности для gpt4free

## Обзор

Этот модуль содержит набор модульных тестов для проверки асинхронной функциональности библиотеки `gpt4free`. Он включает тесты для `ChatCompletion.create_async` и `ChatCompletion.create`, а также тесты для обработки исключений и использования генераторов. Модуль использует `unittest` и `asyncio` для проведения тестов и моки для имитации поставщиков (providers) AI моделей.

## Подробнее

Модуль проверяет корректность работы асинхронных вызовов `ChatCompletion.create_async` с различными типами поставщиков (mocks), включая асинхронные и генераторные. Также проверяется обработка исключений, возникающих при неправильной настройке асинхронной среды (отсутствие `nest_asyncio`).

## Классы

### `TestChatCompletion`

**Описание**: Класс, содержащий тесты для синхронной версии `ChatCompletion.create`.

**Наследует**: `unittest.TestCase`

**Методы**:

- `run_exception()`: Запускает `ChatCompletion.create` в асинхронном контексте для проверки обработки исключения `NestAsyncioError`.
- `test_exception()`: Проверяет, что при отсутствии `nest_asyncio` выбрасывается исключение `g4f.errors.NestAsyncioError`.
- `test_create()`: Проверяет успешное создание ответа с использованием `AsyncProviderMock`.
- `test_create_generator()`: Проверяет успешное создание ответа с использованием `AsyncGeneratorProviderMock`.
- `test_await_callback()`: Проверяет успешное создание ответа с использованием `AsyncGeneratorProviderMock` через клиент.

### `TestChatCompletionAsync`

**Описание**: Класс, содержащий асинхронные тесты для `ChatCompletion.create_async`.

**Наследует**: `unittest.IsolatedAsyncioTestCase`

**Методы**:

- `test_base()`: Проверяет базовый асинхронный вызов `ChatCompletion.create_async` с использованием `ProviderMock`.
- `test_async()`: Проверяет асинхронный вызов `ChatCompletion.create_async` с использованием `AsyncProviderMock`.
- `test_create_generator()`: Проверяет асинхронный вызов `ChatCompletion.create_async` с использованием `AsyncGeneratorProviderMock`.

### `TestChatCompletionNestAsync`

**Описание**: Класс, содержащий асинхронные тесты для `ChatCompletion.create_async` с применением `nest_asyncio`.

**Наследует**: `unittest.IsolatedAsyncioTestCase`

**Методы**:

- `setUp()`: Устанавливает `nest_asyncio`, если он установлен, иначе пропускает тесты.
- `test_create()`: Проверяет асинхронный вызов `ChatCompletion.create_async` с использованием `ProviderMock`.
- `_test_nested()`: Проверяет вызов `ChatCompletion.create` (синхронный) в асинхронном контексте с использованием `AsyncProviderMock`.
- `_test_nested_generator()`: Проверяет вызов `ChatCompletion.create` (синхронный) в асинхронном контексте с использованием `AsyncGeneratorProviderMock`.

## Функции

### `run_exception`

```python
async def run_exception(self):
    """
    Запускает `ChatCompletion.create` в асинхронном контексте для проверки обработки исключения `NestAsyncioError`.

    Args:
        self: Экземпляр класса `TestChatCompletion`.

    Returns:
        Результат вызова `ChatCompletion.create`.

    Как работает функция:
     1. Вызывает асинхронно функцию `ChatCompletion.create` c параметрами `g4f.models.default`, `DEFAULT_MESSAGES` и `AsyncProviderMock`.
     2. Возвращает результат вызова `ChatCompletion.create`.
    """
    return ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncProviderMock)
```

### `test_exception`

```python
def test_exception(self):
    """
    Проверяет, что при отсутствии `nest_asyncio` выбрасывается исключение `g4f.errors.NestAsyncioError`.

    Args:
        self: Экземпляр класса `TestChatCompletion`.

    Raises:
        g4f.errors.NestAsyncioError: Если `nest_asyncio` не установлен.

    Как работает функция:

     1. Проверяет, установлен ли `nest_asyncio`. Если установлен, тест пропускается.
     2. В противном случае, вызывает `asyncio.run` для `self.run_exception()` и проверяет, что выбрасывается исключение `g4f.errors.NestAsyncioError`.
    """
    if has_nest_asyncio:
        self.skipTest('has nest_asyncio')
    self.assertRaises(g4f.errors.NestAsyncioError, asyncio.run, self.run_exception())
```

### `test_create`

```python
def test_create(self):
    """
    Проверяет успешное создание ответа с использованием `AsyncProviderMock`.

    Args:
        self: Экземпляр класса `TestChatCompletion`.

    Как работает функция:
     1. Вызывает `ChatCompletion.create` с параметрами `g4f.models.default`, `DEFAULT_MESSAGES` и `AsyncProviderMock`.
     2. Проверяет, что результат равен "Mock".
    """
    result = ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncProviderMock)
    self.assertEqual("Mock", result)
```

### `test_create_generator`

```python
def test_create_generator(self):
    """
    Проверяет успешное создание ответа с использованием `AsyncGeneratorProviderMock`.

    Args:
        self: Экземпляр класса `TestChatCompletion`.

    Как работает функция:
     1. Вызывает `ChatCompletion.create` с параметрами `g4f.models.default`, `DEFAULT_MESSAGES` и `AsyncGeneratorProviderMock`.
     2. Проверяет, что результат равен "Mock".
    """
    result = ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncGeneratorProviderMock)
    self.assertEqual("Mock", result)
```

### `test_await_callback`

```python
def test_await_callback(self):
    """
    Проверяет успешное создание ответа с использованием `AsyncGeneratorProviderMock` через клиент.

    Args:
        self: Экземпляр класса `TestChatCompletion`.

    Как работает функция:
     1. Создает экземпляр класса `Client` с параметром `provider=AsyncGeneratorProviderMock`.
     2. Вызывает `client.chat.completions.create` с параметрами `DEFAULT_MESSAGES`, `""`, `max_tokens=0`.
     3. Проверяет, что содержимое первого выбора в ответе равно "Mock".
    """
    client = Client(provider=AsyncGeneratorProviderMock)
    response = client.chat.completions.create(DEFAULT_MESSAGES, "", max_tokens=0)
    self.assertEqual("Mock", response.choices[0].message.content)
```

### `test_base`

```python
async def test_base(self):
    """
    Проверяет базовый асинхронный вызов `ChatCompletion.create_async` с использованием `ProviderMock`.

    Args:
        self: Экземпляр класса `TestChatCompletionAsync`.

    Как работает функция:
     1. Вызывает `ChatCompletion.create_async` с параметрами `g4f.models.default`, `DEFAULT_MESSAGES` и `ProviderMock`.
     2. Проверяет, что результат равен "Mock".
    """
    result = await ChatCompletion.create_async(g4f.models.default, DEFAULT_MESSAGES, ProviderMock)
    self.assertEqual("Mock",result)
```

### `test_async`

```python
async def test_async(self):
    """
    Проверяет асинхронный вызов `ChatCompletion.create_async` с использованием `AsyncProviderMock`.

    Args:
        self: Экземпляр класса `TestChatCompletionAsync`.

    Как работает функция:
     1. Вызывает `ChatCompletion.create_async` с параметрами `g4f.models.default`, `DEFAULT_MESSAGES` и `AsyncProviderMock`.
     2. Проверяет, что результат равен "Mock".
    """
    result = await ChatCompletion.create_async(g4f.models.default, DEFAULT_MESSAGES, AsyncProviderMock)
    self.assertEqual("Mock",result)
```

### `test_create_generator`

```python
async def test_create_generator(self):
    """
    Проверяет асинхронный вызов `ChatCompletion.create_async` с использованием `AsyncGeneratorProviderMock`.

    Args:
        self: Экземпляр класса `TestChatCompletionAsync`.

    Как работает функция:
     1. Вызывает `ChatCompletion.create_async` с параметрами `g4f.models.default`, `DEFAULT_MESSAGES` и `AsyncGeneratorProviderMock`.
     2. Проверяет, что результат равен "Mock".
    """
    result = await ChatCompletion.create_async(g4f.models.default, DEFAULT_MESSAGES, AsyncGeneratorProviderMock)
    self.assertEqual("Mock",result)
```

### `setUp`

```python
def setUp(self) -> None:
    """
    Устанавливает `nest_asyncio`, если он установлен, иначе пропускает тесты.

    Args:
        self: Экземпляр класса `TestChatCompletionNestAsync`.

    Как работает функция:
     1. Проверяет, установлен ли `nest_asyncio`. Если не установлен, тест пропускается.
     2. Если `nest_asyncio` установлен, применяется `nest_asyncio.apply()`.
    """
    if not has_nest_asyncio:
        self.skipTest('"nest_asyncio" not installed')
    nest_asyncio.apply()
```

### `test_create`

```python
async def test_create(self):
    """
    Проверяет асинхронный вызов `ChatCompletion.create_async` с использованием `ProviderMock`.

    Args:
        self: Экземпляр класса `TestChatCompletionNestAsync`.

    Как работает функция:
     1. Вызывает `ChatCompletion.create_async` с параметрами `g4f.models.default`, `DEFAULT_MESSAGES` и `ProviderMock`.
     2. Проверяет, что результат равен "Mock".
    """
    result = await ChatCompletion.create_async(g4f.models.default, DEFAULT_MESSAGES, ProviderMock)
    self.assertEqual("Mock",result)
```

### `_test_nested`

```python
async def _test_nested(self):
    """
    Проверяет вызов `ChatCompletion.create` (синхронный) в асинхронном контексте с использованием `AsyncProviderMock`.

    Args:
        self: Экземпляр класса `TestChatCompletionNestAsync`.

    Как работает функция:
     1. Вызывает `ChatCompletion.create` с параметрами `g4f.models.default`, `DEFAULT_MESSAGES` и `AsyncProviderMock`.
     2. Проверяет, что результат равен "Mock".
    """
    result = ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncProviderMock)
    self.assertEqual("Mock",result)
```

### `_test_nested_generator`

```python
async def _test_nested_generator(self):
    """
    Проверяет вызов `ChatCompletion.create` (синхронный) в асинхронном контексте с использованием `AsyncGeneratorProviderMock`.

    Args:
        self: Экземпляр класса `TestChatCompletionNestAsync`.

    Как работает функция:
     1. Вызывает `ChatCompletion.create` с параметрами `g4f.models.default`, `DEFAULT_MESSAGES` и `AsyncGeneratorProviderMock`.
     2. Проверяет, что результат равен "Mock".
    """
    result = ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncGeneratorProviderMock)
    self.assertEqual("Mock",result)
```

## Переменные

- `DEFAULT_MESSAGES`: Список, содержащий сообщение по умолчанию для использования в тестах.

## Зависимости

- `asyncio`: Для асинхронного выполнения тестов.
- `unittest`: Для организации и запуска тестов.
- `g4f`: Основная библиотека, для которой пишутся тесты.
- `nest_asyncio`: Для поддержки вложенных циклов событий (event loops) asyncio.
- `.mocks`: Локальный модуль, содержащий моки для поставщиков (providers).

## Как работает модуль:

1. **Импорт необходимых библиотек**:
   - Импортируются `asyncio`, `unittest`, `g4f`, `nest_asyncio` (если доступен) и моки поставщиков.
     ```python
     import asyncio
     import unittest
     import g4f
     from g4f import ChatCompletion
     from g4f.client import Client
     from .mocks import ProviderMock, AsyncProviderMock, AsyncGeneratorProviderMock
     ```

2. **Определение константы `DEFAULT_MESSAGES`**:
   - Определяется список сообщений по умолчанию, который будет использоваться в тестах.
     ```python
     DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]
     ```

3. **Определение тестовых классов**:
   - Определяются три тестовых класса: `TestChatCompletion`, `TestChatCompletionAsync` и `TestChatCompletionNestAsync`.
     - `TestChatCompletion`: Содержит тесты для синхронной версии `ChatCompletion.create`.
     - `TestChatCompletionAsync`: Содержит асинхронные тесты для `ChatCompletion.create_async`.
     - `TestChatCompletionNestAsync`: Содержит асинхронные тесты для `ChatCompletion.create_async` с применением `nest_asyncio`.

4. **Тестирование обработки исключений**:
   - В классе `TestChatCompletion` проверяется, что при отсутствии `nest_asyncio` выбрасывается исключение `g4f.errors.NestAsyncioError`.
     ```python
     def test_exception(self):
         if has_nest_asyncio:
             self.skipTest('has nest_asyncio')
         self.assertRaises(g4f.errors.NestAsyncioError, asyncio.run, self.run_exception())
     ```

5. **Тестирование асинхронных вызовов**:
   - В классах `TestChatCompletionAsync` и `TestChatCompletionNestAsync` проверяются асинхронные вызовы `ChatCompletion.create_async` с различными типами поставщиков (mocks).
     ```python
     async def test_async(self):
         result = await ChatCompletion.create_async(g4f.models.default, DEFAULT_MESSAGES, AsyncProviderMock)
         self.assertEqual("Mock",result)
     ```

6. **Запуск тестов**:
   - В блоке `if __name__ == '__main__':` запускаются все тесты с помощью `unittest.main()`.
     ```python
     if __name__ == '__main__':
         unittest.main()
     ```

## ASCII Flowchart:

```
Test Execution Flow
├── TestChatCompletion
│   ├── run_exception (Async call to ChatCompletion.create)
│   ├── test_exception (Check NestAsyncioError)
│   ├── test_create (ChatCompletion.create with AsyncProviderMock)
│   └── test_create_generator (ChatCompletion.create with AsyncGeneratorProviderMock)
│
├── TestChatCompletionAsync
│   ├── test_base (ChatCompletion.create_async with ProviderMock)
│   ├── test_async (ChatCompletion.create_async with AsyncProviderMock)
│   └── test_create_generator (ChatCompletion.create_async with AsyncGeneratorProviderMock)
│
└── TestChatCompletionNestAsync
    ├── setUp (Apply nest_asyncio if available)
    ├── test_create (ChatCompletion.create_async with ProviderMock)
    ├── _test_nested (ChatCompletion.create with AsyncProviderMock)
    └── _test_nested_generator (ChatCompletion.create with AsyncGeneratorProviderMock)
```

## Примеры:

### Пример запуска тестов

```python
if __name__ == '__main__':
    unittest.main()
```

### Пример использования `AsyncProviderMock`

```python
async def test_async(self):
    result = await ChatCompletion.create_async(g4f.models.default, DEFAULT_MESSAGES, AsyncProviderMock)
    self.assertEqual("Mock",result)
```

### Пример обработки исключения `NestAsyncioError`

```python
def test_exception(self):
    if has_nest_asyncio:
        self.skipTest('has nest_asyncio')
    self.assertRaises(g4f.errors.NestAsyncioError, asyncio.run, self.run_exception())