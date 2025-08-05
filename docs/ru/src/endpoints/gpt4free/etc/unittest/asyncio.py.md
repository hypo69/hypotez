# Модуль тестирования асинхронности для gpt4free
## Обзор
Модуль содержит набор тестов для проверки асинхронной функциональности библиотеки `gpt4free`, включая `ChatCompletion` с использованием моковых провайдеров. Он проверяет правильность обработки исключений, асинхронное создание и генерацию чатов.

## Подробней
Данный модуль предназначен для тестирования асинхронных возможностей библиотеки `gpt4free`. Он использует `unittest` и `asyncio` для создания и запуска тестов. В частности, проверяется корректность работы `ChatCompletion.create_async` и `ChatCompletion.create` с моковыми асинхронными провайдерами. Также модуль проверяет обработку исключений, возникающих при использовании `asyncio` без установленного `nest_asyncio`.

## Классы
### `TestChatCompletion`
Класс содержит тесты для синхронного `ChatCompletion`.

**Наследует:**
- `unittest.TestCase`

**Атрибуты:**
- `DEFAULT_MESSAGES` (list): Список сообщений по умолчанию для использования в тестах.

**Методы:**
- `run_exception()`: Асинхронная функция, которая вызывает `ChatCompletion.create` с `AsyncProviderMock` для проверки исключений.
- `test_exception()`: Тест, проверяющий возникновение исключения `g4f.errors.NestAsyncioError` при запуске `run_exception()` без `nest_asyncio`.
- `test_create()`: Тест, проверяющий корректность создания чата с использованием `AsyncProviderMock`.
- `test_create_generator()`: Тест, проверяющий корректность создания чата с использованием `AsyncGeneratorProviderMock`.
- `test_await_callback()`: Тест, проверяющий асинхронный вызов `client.chat.completions.create` с `AsyncGeneratorProviderMock`.

### `TestChatCompletionAsync`
Класс содержит тесты для асинхронного `ChatCompletion`.

**Наследует:**
- `unittest.IsolatedAsyncioTestCase`

**Методы:**
- `test_base()`: Тест, проверяющий базовую асинхронную функциональность с использованием `ProviderMock`.
- `test_async()`: Тест, проверяющий асинхронную функциональность с использованием `AsyncProviderMock`.
- `test_create_generator()`: Тест, проверяющий асинхронное создание чата с использованием `AsyncGeneratorProviderMock`.

### `TestChatCompletionNestAsync`
Класс содержит тесты для `ChatCompletion` с использованием `nest_asyncio`.

**Наследует:**
- `unittest.IsolatedAsyncioTestCase`

**Методы:**
- `setUp()`: Метод, выполняемый перед каждым тестом, применяет `nest_asyncio`, если он установлен.
- `test_create()`: Тест, проверяющий создание чата с использованием `ProviderMock` и `nest_asyncio`.
- `_test_nested()`: Тест, проверяющий создание чата с использованием `AsyncProviderMock` и `nest_asyncio`.
- `_test_nested_generator()`: Тест, проверяющий создание чата с использованием `AsyncGeneratorProviderMock` и `nest_asyncio`.

## Переменные
- `DEFAULT_MESSAGES` (list): Список сообщений по умолчанию для использования в тестах.

## Функции

### `run_exception`

```python
async def run_exception() -> Any:
    """
    Асинхронно вызывает ChatCompletion.create с AsyncProviderMock для проверки обработки исключений.

    Args:
        None

    Returns:
        Any: Результат выполнения ChatCompletion.create.
    """
    return ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncProviderMock)

```

### `test_exception`

```python
def test_exception() -> None:
    """
    Проверяет возникновение исключения g4f.errors.NestAsyncioError при запуске run_exception() без nest_asyncio.
    
    Если установлен nest_asyncio, тест пропускается.

    Args:
        None

    Returns:
        None

    Raises:
        g4f.errors.NestAsyncioError: Если nest_asyncio не установлен и asyncio.run вызывается вложенно.
    """
    if has_nest_asyncio:
        self.skipTest('has nest_asyncio')
    self.assertRaises(g4f.errors.NestAsyncioError, asyncio.run, self.run_exception())
```

### `test_create`

```python
def test_create() -> None:
    """
    Проверяет корректность создания чата с использованием AsyncProviderMock.

    Args:
        None

    Returns:
        None
    """
    result = ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncProviderMock)
    self.assertEqual("Mock", result)
```

### `test_create_generator`

```python
def test_create_generator() -> None:
    """
    Проверяет корректность создания чата с использованием AsyncGeneratorProviderMock.

    Args:
        None

    Returns:
        None
    """
    result = ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncGeneratorProviderMock)
    self.assertEqual("Mock", result)
```

### `test_await_callback`

```python
def test_await_callback() -> None:
    """
    Проверяет асинхронный вызов client.chat.completions.create с AsyncGeneratorProviderMock.

    Args:
        None

    Returns:
        None
    """
    client = Client(provider=AsyncGeneratorProviderMock)
    response = client.chat.completions.create(DEFAULT_MESSAGES, "", max_tokens=0)
    self.assertEqual("Mock", response.choices[0].message.content)
```

### `test_base`

```python
async def test_base() -> None:
    """
    Проверяет базовую асинхронную функциональность с использованием ProviderMock.

    Args:
        None

    Returns:
        None
    """
    result = await ChatCompletion.create_async(g4f.models.default, DEFAULT_MESSAGES, ProviderMock)
    self.assertEqual("Mock",result)
```

### `test_async`

```python
async def test_async() -> None:
    """
    Проверяет асинхронную функциональность с использованием AsyncProviderMock.

    Args:
        None

    Returns:
        None
    """
    result = await ChatCompletion.create_async(g4f.models.default, DEFAULT_MESSAGES, AsyncProviderMock)
    self.assertEqual("Mock",result)
```

### `test_create_generator`

```python
async def test_create_generator() -> None:
    """
    Проверяет асинхронное создание чата с использованием AsyncGeneratorProviderMock.

    Args:
        None

    Returns:
        None
    """
    result = await ChatCompletion.create_async(g4f.models.default, DEFAULT_MESSAGES, AsyncGeneratorProviderMock)
    self.assertEqual("Mock",result)
```

### `setUp`

```python
def setUp(self) -> None:
    """
    Выполняется перед каждым тестом, применяет nest_asyncio, если он установлен.

    Args:
        None

    Returns:
        None
    """
    if not has_nest_asyncio:
        self.skipTest('"nest_asyncio" not installed')
    nest_asyncio.apply()
```

### `test_create`

```python
async def test_create() -> None:
    """
    Проверяет создание чата с использованием ProviderMock и nest_asyncio.

    Args:
        None

    Returns:
        None
    """
    result = await ChatCompletion.create_async(g4f.models.default, DEFAULT_MESSAGES, ProviderMock)
    self.assertEqual("Mock",result)
```

### `_test_nested`

```python
async def _test_nested() -> None:
    """
    Проверяет создание чата с использованием AsyncProviderMock и nest_asyncio.

    Args:
        None

    Returns:
        None
    """
    result = ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncProviderMock)
    self.assertEqual("Mock",result)
```

### `_test_nested_generator`

```python
async def _test_nested_generator() -> None:
    """
    Проверяет создание чата с использованием AsyncGeneratorProviderMock и nest_asyncio.

    Args:
        None

    Returns:
        None
    """
    result = ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncGeneratorProviderMock)
    self.assertEqual("Mock",result)
```

## Запуск тестов
В конце файла находится блок `if __name__ == '__main__':`, который запускает тесты при выполнении файла как скрипта.
```python
if __name__ == '__main__':
    unittest.main()