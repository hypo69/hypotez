# Модуль тестирования image_client.py

## Обзор

Этот модуль содержит набор модульных тестов для проверки функциональности асинхронного клиента, генерирующего изображения с использованием различных провайдеров. В частности, он тестирует логику переключения между провайдерами при возникновении ошибок или получении неполных ответов. Модуль использует `unittest` и `asyncio` для организации и выполнения тестов.

## Подробнее

Этот модуль тестирует переключение между провайдерами изображений при использовании `AsyncClient` с `IterListProvider`. Он проверяет, что клиент корректно переходит к следующему провайдеру, если текущий провайдер возвращает ошибку, `None` или не предоставляет достаточно информации. Также проверяется, что при наличии нескольких рабочих провайдеров возвращается результат только от одного из них.

## Классы

### `TestIterListProvider`

**Описание**: Класс, содержащий асинхронные модульные тесты для проверки функциональности `IterListProvider`.

**Наследует**:
- `unittest.IsolatedAsyncioTestCase`: Предоставляет базовый класс для написания асинхронных тестов, обеспечивая изоляцию между тестами.

**Атрибуты**:
- `DEFAULT_MESSAGES (List[dict])`: Список сообщений по умолчанию, используемых в тестах.

**Методы**:
- `test_skip_provider()`: Тестирует пропуск провайдера, если он вызывает исключение.
- `test_only_one_result()`: Тестирует получение только одного результата, даже если несколько провайдеров возвращают данные.
- `test_skip_none()`: Тестирует пропуск провайдера, если он возвращает `None`.
- `test_raise_exception()`: Тестирует обработку исключений, возникающих при работе провайдера.

## Функции

### `test_skip_provider`

```python
async def test_skip_provider(self):
    """Тестирует пропуск провайдера, если он вызывает исключение.

    Args:
        self: Экземпляр класса `TestIterListProvider`.

    Returns:
        None

    Raises:
        AssertionError: Если утверждения в тесте не выполняются.
    """
```

**Назначение**: Проверяет, что `AsyncClient` корректно пропускает провайдера `MissingAuthProviderMock` и использует `YieldImageResponseProviderMock`, когда первый вызывает исключение.

**Как работает функция**:
1. Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит `MissingAuthProviderMock` и `YieldImageResponseProviderMock`.
2. Вызывается метод `images.generate` для генерации изображения.
3. Проверяется, что возвращенный объект является экземпляром `ImagesResponse`.
4. Проверяется, что URL в ответе соответствует ожидаемому значению ("Hello"), что указывает на успешное использование `YieldImageResponseProviderMock`.

**Примеры**:
```python
import unittest
import asyncio
from g4f.client import AsyncClient, ImagesResponse
from g4f.providers.retry_provider import IterListProvider
from .mocks import MissingAuthProviderMock, YieldImageResponseProviderMock

class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
    async def test_skip_provider(self):
        client = AsyncClient(image_provider=IterListProvider([MissingAuthProviderMock, YieldImageResponseProviderMock], False))
        response = await client.images.generate("Hello", "", response_format="orginal")
        self.assertIsInstance(response, ImagesResponse)
        self.assertEqual("Hello", response.data[0].url)
```

### `test_only_one_result`

```python
async def test_only_one_result(self):
    """Тестирует получение только одного результата, даже если несколько провайдеров возвращают данные.

    Args:
        self: Экземпляр класса `TestIterListProvider`.

    Returns:
        None

    Raises:
        AssertionError: Если утверждения в тесте не выполняются.
    """
```

**Назначение**: Проверяет, что `AsyncClient` возвращает только один результат, даже если несколько провайдеров в `IterListProvider` возвращают валидные ответы.

**Как работает функция**:
1. Создается экземпляр `AsyncClient` с `IterListProvider`, содержащим два экземпляра `YieldImageResponseProviderMock`.
2. Вызывается метод `images.generate` для генерации изображения.
3. Проверяется, что возвращенный объект является экземпляром `ImagesResponse`.
4. Проверяется, что URL в ответе соответствует ожидаемому значению ("Hello"), что указывает на успешное использование одного из `YieldImageResponseProviderMock`.

**Примеры**:
```python
import unittest
import asyncio
from g4f.client import AsyncClient, ImagesResponse
from g4f.providers.retry_provider import IterListProvider
from .mocks import YieldImageResponseProviderMock

class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
    async def test_only_one_result(self):
        client = AsyncClient(image_provider=IterListProvider([YieldImageResponseProviderMock, YieldImageResponseProviderMock], False))
        response = await client.images.generate("Hello", "", response_format="orginal")
        self.assertIsInstance(response, ImagesResponse)
        self.assertEqual("Hello", response.data[0].url)
```

### `test_skip_none`

```python
async def test_skip_none(self):
    """Тестирует пропуск провайдера, если он возвращает `None`.

    Args:
        self: Экземпляр класса `TestIterListProvider`.

    Returns:
        None

    Raises:
        AssertionError: Если утверждения в тесте не выполняются.
    """
```

**Назначение**: Проверяет, что `AsyncClient` пропускает провайдера `YieldNoneProviderMock`, если он возвращает `None`, и использует следующий провайдер `YieldImageResponseProviderMock`.

**Как работает функция**:
1. Создается экземпляр `AsyncClient` с `IterListProvider`, содержащим `YieldNoneProviderMock` и `YieldImageResponseProviderMock`.
2. Вызывается метод `images.generate` для генерации изображения.
3. Проверяется, что возвращенный объект является экземпляром `ImagesResponse`.
4. Проверяется, что URL в ответе соответствует ожидаемому значению ("Hello"), что указывает на успешное использование `YieldImageResponseProviderMock`.

**Примеры**:
```python
import unittest
import asyncio
from g4f.client import AsyncClient, ImagesResponse
from g4f.providers.retry_provider import IterListProvider
from .mocks import YieldNoneProviderMock, YieldImageResponseProviderMock

class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
    async def test_skip_none(self):
        client = AsyncClient(image_provider=IterListProvider([YieldNoneProviderMock, YieldImageResponseProviderMock], False))
        response = await client.images.generate("Hello", "", response_format="orginal")
        self.assertIsInstance(response, ImagesResponse)
        self.assertEqual("Hello", response.data[0].url)
```

### `test_raise_exception`

```python
def test_raise_exception(self):
    """Тестирует обработку исключений, возникающих при работе провайдера.

    Args:
        self: Экземпляр класса `TestIterListProvider`.

    Returns:
        None

    Raises:
        RuntimeError: Если исключение не возникает при генерации изображения.
    """
```

**Назначение**: Проверяет, что при возникновении исключения в одном из провайдеров (`AsyncRaiseExceptionProviderMock`), исключение правильно обрабатывается и поднимается.

**Как работает функция**:
1. Определяется асинхронная функция `run_exception`, которая создает экземпляр `AsyncClient` с `IterListProvider`, содержащим `YieldNoneProviderMock` и `AsyncRaiseExceptionProviderMock`.
2. В `run_exception` вызывается метод `images.generate`, который должен вызвать исключение.
3. Используется `self.assertRaises` для проверки, что вызов `asyncio.run(run_exception())` поднимает исключение `RuntimeError`.

**Примеры**:
```python
import unittest
import asyncio
from g4f.client import AsyncClient
from g4f.providers.retry_provider import IterListProvider
from .mocks import YieldNoneProviderMock, AsyncRaiseExceptionProviderMock

class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
    def test_raise_exception(self):
        async def run_exception():
            client = AsyncClient(image_provider=IterListProvider([YieldNoneProviderMock, AsyncRaiseExceptionProviderMock], False))
            await client.images.generate("Hello", "")
        self.assertRaises(RuntimeError, asyncio.run, run_exception())
```