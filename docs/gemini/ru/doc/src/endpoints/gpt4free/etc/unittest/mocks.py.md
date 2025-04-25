# Модуль `mocks`

## Обзор

Модуль `mocks` содержит набор мокированных классов для тестирования различных API-провайдеров, используемых в проекте `hypotez`. Мокированные классы предназначены для имитации поведения реальных API-провайдеров, что позволяет проводить изолированное тестирование функций и классов, взаимодействующих с этими API. 

##  Мокированные классы 

### `class ProviderMock`

**Описание**: Мокированный класс для имитации базового API-провайдера.

**Наследует**:
    - `AbstractProvider`

**Атрибуты**:

    - `working` (bool): Флаг, указывающий, что мокированный провайдер работает.

**Методы**:

    - `create_completion(model, messages, stream, **kwargs)`: Мокированная функция, возвращающая генератор, который выдает "Mock".

### `class AsyncProviderMock`

**Описание**: Мокированный класс для имитации асинхронного API-провайдера.

**Наследует**:
    - `AsyncProvider`

**Атрибуты**:

    - `working` (bool): Флаг, указывающий, что мокированный провайдер работает.

**Методы**:

    - `create_async(model, messages, **kwargs)`: Мокированная асинхронная функция, возвращающая "Mock".

### `class AsyncGeneratorProviderMock`

**Описание**: Мокированный класс для имитации асинхронного API-провайдера, использующего генератор.

**Наследует**:
    - `AsyncGeneratorProvider`

**Атрибуты**:

    - `working` (bool): Флаг, указывающий, что мокированный провайдер работает.

**Методы**:

    - `create_async_generator(model, messages, stream, **kwargs)`: Мокированная асинхронная функция, возвращающая генератор, который выдает "Mock".

### `class ModelProviderMock`

**Описание**: Мокированный класс для имитации API-провайдера, возвращающего модель.

**Наследует**:
    - `AbstractProvider`

**Атрибуты**:

    - `working` (bool): Флаг, указывающий, что мокированный провайдер работает.

**Методы**:

    - `create_completion(model, messages, stream, **kwargs)`: Мокированная функция, возвращающая генератор, который выдает `model`.

### `class YieldProviderMock`

**Описание**: Мокированный класс для имитации API-провайдера, возвращающего генератор, который выдает контент из `messages`.

**Наследует**:
    - `AsyncGeneratorProvider`

**Атрибуты**:

    - `working` (bool): Флаг, указывающий, что мокированный провайдер работает.

**Методы**:

    - `create_async_generator(model, messages, stream, **kwargs)`: Мокированная асинхронная функция, возвращающая генератор, который выдает `message["content"]` для каждого сообщения в `messages`.

### `class YieldImageResponseProviderMock`

**Описание**: Мокированный класс для имитации API-провайдера, возвращающего `ImageResponse`.

**Наследует**:
    - `AsyncGeneratorProvider`

**Атрибуты**:

    - `working` (bool): Флаг, указывающий, что мокированный провайдер работает.

**Методы**:

    - `create_async_generator(model, messages, stream, prompt: str, **kwargs)`: Мокированная асинхронная функция, возвращающая генератор, который выдает `ImageResponse(prompt, "")`.

### `class MissingAuthProviderMock`

**Описание**: Мокированный класс для имитации API-провайдера, который не может быть инициализирован из-за отсутствия авторизации.

**Наследует**:
    - `AbstractProvider`

**Атрибуты**:

    - `working` (bool): Флаг, указывающий, что мокированный провайдер работает.

**Методы**:

    - `create_completion(model, messages, stream, **kwargs)`: Мокированная функция, которая поднимает `MissingAuthError`.

### `class RaiseExceptionProviderMock`

**Описание**: Мокированный класс для имитации API-провайдера, который вызывает исключение `RuntimeError`.

**Наследует**:
    - `AbstractProvider`

**Атрибуты**:

    - `working` (bool): Флаг, указывающий, что мокированный провайдер работает.

**Методы**:

    - `create_completion(model, messages, stream, **kwargs)`: Мокированная функция, которая поднимает `RuntimeError`.

### `class AsyncRaiseExceptionProviderMock`

**Описание**: Мокированный класс для имитации асинхронного API-провайдера, который вызывает исключение `RuntimeError`.

**Наследует**:
    - `AsyncGeneratorProvider`

**Атрибуты**:

    - `working` (bool): Флаг, указывающий, что мокированный провайдер работает.

**Методы**:

    - `create_async_generator(model, messages, stream, **kwargs)`: Мокированная асинхронная функция, которая поднимает `RuntimeError`.

### `class YieldNoneProviderMock`

**Описание**: Мокированный класс для имитации API-провайдера, который возвращает генератор, который выдает `None`.

**Наследует**:
    - `AsyncGeneratorProvider`

**Атрибуты**:

    - `working` (bool): Флаг, указывающий, что мокированный провайдер работает.

**Методы**:

    - `create_async_generator(model, messages, stream, **kwargs)`: Мокированная асинхронная функция, возвращающая генератор, который выдает `None`.

## Примеры

```python
# Пример использования ProviderMock
from hypotez.src.endpoints.gpt4free.etc.unittest.mocks import ProviderMock

provider = ProviderMock()
response = provider.create_completion(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world!"}], stream=False)
print(next(response)) # Выведет "Mock"

# Пример использования AsyncProviderMock
from hypotez.src.endpoints.gpt4free.etc.unittest.mocks import AsyncProviderMock

async def test_async_provider():
    provider = AsyncProviderMock()
    response = await provider.create_async(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world!"}])
    assert response == "Mock"

# Пример использования AsyncGeneratorProviderMock
from hypotez.src.endpoints.gpt4free.etc.unittest.mocks import AsyncGeneratorProviderMock

async def test_async_generator_provider():
    provider = AsyncGeneratorProviderMock()
    async for response in provider.create_async_generator(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world!"}], stream=False):
        assert response == "Mock"

# Пример использования ModelProviderMock
from hypotez.src.endpoints.gpt4free.etc.unittest.mocks import ModelProviderMock

provider = ModelProviderMock()
response = provider.create_completion(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world!"}], stream=False)
print(next(response)) # Выведет "gpt-3.5-turbo"

# Пример использования YieldProviderMock
from hypotez.src.endpoints.gpt4free.etc.unittest.mocks import YieldProviderMock

async def test_yield_provider():
    provider = YieldProviderMock()
    async for response in provider.create_async_generator(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world!"}], stream=False):
        assert response == "Hello world!"

# Пример использования YieldImageResponseProviderMock
from hypotez.src.endpoints.gpt4free.etc.unittest.mocks import YieldImageResponseProviderMock

async def test_yield_image_response_provider():
    provider = YieldImageResponseProviderMock()
    async for response in provider.create_async_generator(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world!"}], stream=False, prompt="image_prompt"):
        assert response.prompt == "image_prompt"
        assert response.content == ""

# Пример использования MissingAuthProviderMock
from hypotez.src.endpoints.gpt4free.etc.unittest.mocks import MissingAuthProviderMock
from hypotez.src.endpoints.gpt4free.errors import MissingAuthError

provider = MissingAuthProviderMock()
try:
    response = provider.create_completion(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world!"}], stream=False)
except MissingAuthError as ex:
    assert ex.message == "MissingAuthProviderMock"

# Пример использования RaiseExceptionProviderMock
from hypotez.src.endpoints.gpt4free.etc.unittest.mocks import RaiseExceptionProviderMock

provider = RaiseExceptionProviderMock()
try:
    response = provider.create_completion(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world!"}], stream=False)
except RuntimeError as ex:
    assert ex.args[0] == "RaiseExceptionProviderMock"

# Пример использования AsyncRaiseExceptionProviderMock
from hypotez.src.endpoints.gpt4free.etc.unittest.mocks import AsyncRaiseExceptionProviderMock

async def test_async_raise_exception_provider():
    provider = AsyncRaiseExceptionProviderMock()
    try:
        async for response in provider.create_async_generator(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world!"}], stream=False):
            pass
    except RuntimeError as ex:
        assert ex.args[0] == "AsyncRaiseExceptionProviderMock"

# Пример использования YieldNoneProviderMock
from hypotez.src.endpoints.gpt4free.etc.unittest.mocks import YieldNoneProviderMock

async def test_yield_none_provider():
    provider = YieldNoneProviderMock()
    async for response in provider.create_async_generator(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world!"}], stream=False):
        assert response is None