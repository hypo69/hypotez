# Module for Mocking Providers in Tests

## Overview

This module defines several mock classes for simulating different provider behaviors during testing. These mocks are designed to emulate successful, asynchronous, and error-throwing providers, allowing for comprehensive testing of components that rely on provider interactions.

## More details

This module provides a set of mock classes that inherit from `AbstractProvider`, `AsyncProvider`, and `AsyncGeneratorProvider`. These mock classes are used in unit tests to simulate different scenarios when interacting with providers, such as successful responses, asynchronous operations, generator-based responses, missing authentication, and exceptions.

## Classes

### `ProviderMock`

**Description**: Mock provider class that synchronously yields a predefined string ("Mock").

**Inherits**:
- `AbstractProvider`: Базовый класс для всех провайдеров.

**Attributes**:
- `working` (bool): Indicates whether the provider is working (always `True` in this mock).

**Methods**:
- `create_completion(model, messages, stream, **kwargs)`: Mock method that yields the string "Mock".

### `AsyncProviderMock`

**Description**: Mock asynchronous provider class that returns a predefined string ("Mock") asynchronously.

**Inherits**:
- `AsyncProvider`: Базовый класс для асинхронных провайдеров.

**Attributes**:
- `working` (bool): Indicates whether the provider is working (always `True` in this mock).

**Methods**:
- `create_async(model, messages, **kwargs)`: Mock asynchronous method that returns the string "Mock".

### `AsyncGeneratorProviderMock`

**Description**: Mock asynchronous generator provider class that asynchronously yields a predefined string ("Mock").

**Inherits**:
- `AsyncGeneratorProvider`: Базовый класс для асинхронных провайдеров-генераторов.

**Attributes**:
- `working` (bool): Indicates whether the provider is working (always `True` in this mock).

**Methods**:
- `create_async_generator(model, messages, stream, **kwargs)`: Mock asynchronous generator method that yields the string "Mock".

### `ModelProviderMock`

**Description**: Mock provider class that yields the model name passed to it.

**Inherits**:
- `AbstractProvider`: Базовый класс для всех провайдеров.

**Attributes**:
- `working` (bool): Indicates whether the provider is working (always `True` in this mock).

**Methods**:
- `create_completion(model, messages, stream, **kwargs)`: Mock method that yields the model name.

### `YieldProviderMock`

**Description**: Mock asynchronous generator provider class that yields the content of each message in the input messages.

**Inherits**:
- `AsyncGeneratorProvider`: Базовый класс для асинхронных провайдеров-генераторов.

**Attributes**:
- `working` (bool): Indicates whether the provider is working (always `True` in this mock).

**Methods**:
- `create_async_generator(model, messages, stream, **kwargs)`: Mock asynchronous generator method that yields the content of each message.

### `YieldImageResponseProviderMock`

**Description**: Mock asynchronous generator provider class that yields an `ImageResponse` object.

**Inherits**:
- `AsyncGeneratorProvider`: Базовый класс для асинхронных провайдеров-генераторов.

**Attributes**:
- `working` (bool): Indicates whether the provider is working (always `True` in this mock).

**Methods**:
- `create_async_generator(model, messages, stream, prompt: str, **kwargs)`: Mock asynchronous generator method that yields an `ImageResponse` object.

### `MissingAuthProviderMock`

**Description**: Mock provider class that raises a `MissingAuthError`.

**Inherits**:
- `AbstractProvider`: Базовый класс для всех провайдеров.

**Attributes**:
- `working` (bool): Indicates whether the provider is working (always `True` in this mock).

**Methods**:
- `create_completion(model, messages, stream, **kwargs)`: Mock method that raises a `MissingAuthError`.

### `RaiseExceptionProviderMock`

**Description**: Mock provider class that raises a `RuntimeError`.

**Inherits**:
- `AbstractProvider`: Базовый класс для всех провайдеров.

**Attributes**:
- `working` (bool): Indicates whether the provider is working (always `True` in this mock).

**Methods**:
- `create_completion(model, messages, stream, **kwargs)`: Mock method that raises a `RuntimeError`.

### `AsyncRaiseExceptionProviderMock`

**Description**: Mock asynchronous generator provider class that raises a `RuntimeError`.

**Inherits**:
- `AsyncGeneratorProvider`: Базовый класс для асинхронных провайдеров-генераторов.

**Attributes**:
- `working` (bool): Indicates whether the provider is working (always `True` in this mock).

**Methods**:
- `create_async_generator(model, messages, stream, **kwargs)`: Mock asynchronous generator method that raises a `RuntimeError`.

### `YieldNoneProviderMock`

**Description**: Mock asynchronous generator provider class that yields `None`.

**Inherits**:
- `AsyncGeneratorProvider`: Базовый класс для асинхронных провайдеров-генераторов.

**Attributes**:
- `working` (bool): Indicates whether the provider is working (always `True` in this mock).

**Methods**:
- `create_async_generator(model, messages, stream, **kwargs)`: Mock asynchronous generator method that yields `None`.

## Class Methods

### `ProviderMock`

#### `create_completion`

```python
def create_completion(cls, model, messages, stream, **kwargs):
    """
    Mock метод, генерирующий строку "Mock".

    Args:
        cls: Класс.
        model: Модель.
        messages: Сообщения.
        stream: Параметр потока.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Строка "Mock".
    """
    yield "Mock"
```

**How the function works**:
- This method is a mock implementation of the `create_completion` method.
- It simply yields the string "Mock".

**Examples**:
```python
# Создание экземпляра класса ProviderMock
mock_provider = ProviderMock()

# Вызов метода create_completion
result = mock_provider.create_completion(model="test_model", messages=["test_message"], stream=False)

# Итерация по результату
for item in result:
    print(item)  # Вывод: Mock
```

### `AsyncProviderMock`

#### `create_async`

```python
async def create_async(cls, model, messages, **kwargs):
    """
    Асинхронный mock метод, возвращающий строку "Mock".

    Args:
        cls: Класс.
        model: Модель.
        messages: Сообщения.
        **kwargs: Дополнительные аргументы.

    Returns:
        str: Строка "Mock".
    """
    return "Mock"
```

**How the function works**:
- This method is a mock asynchronous implementation of the `create_async` method.
- It simply returns the string "Mock".

**Examples**:
```python
import asyncio
# Создание экземпляра класса AsyncProviderMock
mock_provider = AsyncProviderMock()

# Вызов асинхронного метода create_async
async def main():
    result = await mock_provider.create_async(model="test_model", messages=["test_message"])
    print(result)  # Вывод: Mock

asyncio.run(main())
```

### `AsyncGeneratorProviderMock`

#### `create_async_generator`

```python
async def create_async_generator(cls, model, messages, stream, **kwargs):
    """
    Асинхронный mock метод-генератор, генерирующий строку "Mock".

    Args:
        cls: Класс.
        model: Модель.
        messages: Сообщения.
        stream: Параметр потока.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Строка "Mock".
    """
    yield "Mock"
```

**How the function works**:
- This method is a mock asynchronous generator implementation of the `create_async_generator` method.
- It simply yields the string "Mock".

**Examples**:
```python
import asyncio

# Создание экземпляра класса AsyncGeneratorProviderMock
mock_provider = AsyncGeneratorProviderMock()

# Вызов асинхронного метода-генератора create_async_generator
async def main():
    async for item in mock_provider.create_async_generator(model="test_model", messages=["test_message"], stream=False):
        print(item)  # Вывод: Mock

asyncio.run(main())
```

### `ModelProviderMock`

#### `create_completion`

```python
def create_completion(cls, model, messages, stream, **kwargs):
    """
    Mock метод, генерирующий имя модели.

    Args:
        cls: Класс.
        model: Модель.
        messages: Сообщения.
        stream: Параметр потока.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Имя модели.
    """
    yield model
```

**How the function works**:
- This method is a mock implementation of the `create_completion` method.
- It yields the name of the model passed as an argument.

**Examples**:
```python
# Создание экземпляра класса ModelProviderMock
mock_provider = ModelProviderMock()

# Вызов метода create_completion
result = mock_provider.create_completion(model="test_model", messages=["test_message"], stream=False)

# Итерация по результату
for item in result:
    print(item)  # Вывод: test_model
```

### `YieldProviderMock`

#### `create_async_generator`

```python
async def create_async_generator(cls, model, messages, stream, **kwargs):
    """
    Асинхронный mock метод-генератор, генерирующий содержимое каждого сообщения.

    Args:
        cls: Класс.
        model: Модель.
        messages: Сообщения.
        stream: Параметр потока.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Содержимое каждого сообщения.
    """
    for message in messages:
        yield message["content"]
```

**How the function works**:
- This method is a mock asynchronous generator implementation of the `create_async_generator` method.
- It iterates through the messages and yields the content of each message.

**Examples**:
```python
import asyncio

# Создание экземпляра класса YieldProviderMock
mock_provider = YieldProviderMock()

# Вызов асинхронного метода-генератора create_async_generator
async def main():
    messages = [{"content": "message 1"}, {"content": "message 2"}]
    async for item in mock_provider.create_async_generator(model="test_model", messages=messages, stream=False):
        print(item)  # Вывод: message 1, message 2

asyncio.run(main())
```

### `YieldImageResponseProviderMock`

#### `create_async_generator`

```python
async def create_async_generator(cls, model, messages, stream, prompt: str, **kwargs):
    """
    Асинхронный mock метод-генератор, генерирующий объект ImageResponse.

    Args:
        cls: Класс.
        model: Модель.
        messages: Сообщения.
        stream: Параметр потока.
        prompt (str): Подсказка для генерации изображения.
        **kwargs: Дополнительные аргументы.

    Yields:
        ImageResponse: Объект ImageResponse с подсказкой и пустой строкой.
    """
    yield ImageResponse(prompt, "")
```

**How the function works**:
- This method is a mock asynchronous generator implementation of the `create_async_generator` method.
- It yields an `ImageResponse` object with the provided prompt and an empty string as the image data.

**Examples**:
```python
import asyncio
from g4f.providers.response import ImageResponse

# Создание экземпляра класса YieldImageResponseProviderMock
mock_provider = YieldImageResponseProviderMock()

# Вызов асинхронного метода-генератора create_async_generator
async def main():
    async for item in mock_provider.create_async_generator(model="test_model", messages=["test_message"], stream=False, prompt="test_prompt"):
        print(type(item))  # Вывод: <class 'g4f.providers.response.ImageResponse'>
        print(item.prompt)  # Вывод: test_prompt
        print(item.image)   # Вывод: 

asyncio.run(main())
```

### `MissingAuthProviderMock`

#### `create_completion`

```python
def create_completion(cls, model, messages, stream, **kwargs):
    """
    Mock метод, вызывающий исключение MissingAuthError.

    Args:
        cls: Класс.
        model: Модель.
        messages: Сообщения.
        stream: Параметр потока.
        **kwargs: Дополнительные аргументы.

    Raises:
        MissingAuthError: Всегда вызывается.
    """
    raise MissingAuthError(cls.__name__)
    yield cls.__name__
```

**How the function works**:
- This method is a mock implementation of the `create_completion` method.
- It always raises a `MissingAuthError` exception.

**Examples**:
```python
# Создание экземпляра класса MissingAuthProviderMock
mock_provider = MissingAuthProviderMock()

# Вызов метода create_completion
try:
    result = mock_provider.create_completion(model="test_model", messages=["test_message"], stream=False)
    for item in result:
        print(item)
except MissingAuthError as ex:
    print(f"Caught exception: {ex}")  # Вывод: Caught exception: MissingAuthProviderMock
```

### `RaiseExceptionProviderMock`

#### `create_completion`

```python
def create_completion(cls, model, messages, stream, **kwargs):
    """
    Mock метод, вызывающий исключение RuntimeError.

    Args:
        cls: Класс.
        model: Модель.
        messages: Сообщения.
        stream: Параметр потока.
        **kwargs: Дополнительные аргументы.

    Raises:
        RuntimeError: Всегда вызывается.
    """
    raise RuntimeError(cls.__name__)
    yield cls.__name__
```

**How the function works**:
- This method is a mock implementation of the `create_completion` method.
- It always raises a `RuntimeError` exception.

**Examples**:
```python
# Создание экземпляра класса RaiseExceptionProviderMock
mock_provider = RaiseExceptionProviderMock()

# Вызов метода create_completion
try:
    result = mock_provider.create_completion(model="test_model", messages=["test_message"], stream=False)
    for item in result:
        print(item)
except RuntimeError as ex:
    print(f"Caught exception: {ex}")  # Вывод: Caught exception: RaiseExceptionProviderMock
```

### `AsyncRaiseExceptionProviderMock`

#### `create_async_generator`

```python
async def create_async_generator(cls, model, messages, stream, **kwargs):
    """
    Асинхронный mock метод-генератор, вызывающий исключение RuntimeError.

    Args:
        cls: Класс.
        model: Модель.
        messages: Сообщения.
        stream: Параметр потока.
        **kwargs: Дополнительные аргументы.

    Raises:
        RuntimeError: Всегда вызывается.
    """
    raise RuntimeError(cls.__name__)
    yield cls.__name__
```

**How the function works**:
- This method is a mock asynchronous generator implementation of the `create_async_generator` method.
- It always raises a `RuntimeError` exception.

**Examples**:
```python
import asyncio

# Создание экземпляра класса AsyncRaiseExceptionProviderMock
mock_provider = AsyncRaiseExceptionProviderMock()

# Вызов асинхронного метода-генератора create_async_generator
async def main():
    try:
        async for item in mock_provider.create_async_generator(model="test_model", messages=["test_message"], stream=False):
            print(item)
    except RuntimeError as ex:
        print(f"Caught exception: {ex}")  # Вывод: Caught exception: AsyncRaiseExceptionProviderMock

asyncio.run(main())
```

### `YieldNoneProviderMock`

#### `create_async_generator`

```python
async def create_async_generator(cls, model, messages, stream, **kwargs):
    """
    Асинхронный mock метод-генератор, генерирующий None.

    Args:
        cls: Класс.
        model: Модель.
        messages: Сообщения.
        stream: Параметр потока.
        **kwargs: Дополнительные аргументы.

    Yields:
        None: Всегда генерируется.
    """
    yield None
```

**How the function works**:
- This method is a mock asynchronous generator implementation of the `create_async_generator` method.
- It always yields `None`.

**Examples**:
```python
import asyncio

# Создание экземпляра класса YieldNoneProviderMock
mock_provider = YieldNoneProviderMock()

# Вызов асинхронного метода-генератора create_async_generator
async def main():
    async for item in mock_provider.create_async_generator(model="test_model", messages=["test_message"], stream=False):
        print(item)  # Вывод: None

asyncio.run(main())
```