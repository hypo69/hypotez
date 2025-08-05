# Модуль для мокирования провайдеров GPT4Free

## Обзор

Модуль предоставляет набор мокированных классов, которые используются для имитации поведения провайдеров GPT4Free. Мокированные классы предназначены для тестирования функций и модулей, взаимодействующих с GPT4Free API.

## Подробности

Мокированные классы наследуют от базовых классов провайдеров GPT4Free (`AbstractProvider`, `AsyncProvider`, `AsyncGeneratorProvider`) и переопределяют методы для имитации различных сценариев. 

## Классы

### `class ProviderMock(AbstractProvider)`

**Описание**: Мокированный класс, имитирующий базовый провайдер GPT4Free.

**Inherits**: `AbstractProvider`

**Attributes**:
- `working (bool)`: Флаг, указывающий на доступность провайдера.

**Methods**:
- `create_completion(model, messages, stream, **kwargs)`: Мокированный метод для имитации ответа провайдера. Возвращает постоянное значение "Mock".

### `class AsyncProviderMock(AsyncProvider)`

**Описание**: Мокированный класс, имитирующий асинхронный провайдер GPT4Free.

**Inherits**: `AsyncProvider`

**Attributes**:
- `working (bool)`: Флаг, указывающий на доступность провайдера.

**Methods**:
- `create_async(model, messages, **kwargs)`: Мокированный метод для имитации ответа асинхронного провайдера. Возвращает постоянное значение "Mock".

### `class AsyncGeneratorProviderMock(AsyncGeneratorProvider)`

**Описание**: Мокированный класс, имитирующий асинхронный провайдер GPT4Free, который возвращает генератор.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:
- `working (bool)`: Флаг, указывающий на доступность провайдера.

**Methods**:
- `create_async_generator(model, messages, stream, **kwargs)`: Мокированный метод для имитации ответа асинхронного провайдера, возвращающего генератор. Возвращает генератор, который выдает "Mock".

### `class ModelProviderMock(AbstractProvider)`

**Описание**: Мокированный класс, имитирующий провайдер GPT4Free, который возвращает модель в качестве ответа.

**Inherits**: `AbstractProvider`

**Attributes**:
- `working (bool)`: Флаг, указывающий на доступность провайдера.

**Methods**:
- `create_completion(model, messages, stream, **kwargs)`: Мокированный метод для имитации ответа провайдера. Возвращает модель в качестве ответа.

### `class YieldProviderMock(AsyncGeneratorProvider)`

**Описание**: Мокированный класс, имитирующий провайдер GPT4Free, который возвращает генератор, выдающий содержимое сообщений.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:
- `working (bool)`: Флаг, указывающий на доступность провайдера.

**Methods**:
- `create_async_generator(model, messages, stream, **kwargs)`: Мокированный метод для имитации ответа провайдера, возвращающего генератор. Возвращает генератор, который выдает содержимое сообщения из списка `messages`.

### `class YieldImageResponseProviderMock(AsyncGeneratorProvider)`

**Описание**: Мокированный класс, имитирующий провайдер GPT4Free, который возвращает генератор, выдающий объект `ImageResponse`.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:
- `working (bool)`: Флаг, указывающий на доступность провайдера.

**Methods**:
- `create_async_generator(model, messages, stream, prompt: str, **kwargs)`: Мокированный метод для имитации ответа провайдера, возвращающего генератор. Возвращает генератор, который выдает объект `ImageResponse`.

### `class MissingAuthProviderMock(AbstractProvider)`

**Описание**: Мокированный класс, имитирующий провайдер GPT4Free, который вызывает исключение `MissingAuthError`.

**Inherits**: `AbstractProvider`

**Attributes**:
- `working (bool)`: Флаг, указывающий на доступность провайдера.

**Methods**:
- `create_completion(model, messages, stream, **kwargs)`: Мокированный метод для имитации ответа провайдера. Вызывает исключение `MissingAuthError`.

### `class RaiseExceptionProviderMock(AbstractProvider)`

**Описание**: Мокированный класс, имитирующий провайдер GPT4Free, который вызывает исключение `RuntimeError`.

**Inherits**: `AbstractProvider`

**Attributes**:
- `working (bool)`: Флаг, указывающий на доступность провайдера.

**Methods**:
- `create_completion(model, messages, stream, **kwargs)`: Мокированный метод для имитации ответа провайдера. Вызывает исключение `RuntimeError`.

### `class AsyncRaiseExceptionProviderMock(AsyncGeneratorProvider)`

**Описание**: Мокированный класс, имитирующий асинхронный провайдер GPT4Free, который возвращает генератор, вызывающий исключение `RuntimeError`.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:
- `working (bool)`: Флаг, указывающий на доступность провайдера.

**Methods**:
- `create_async_generator(model, messages, stream, **kwargs)`: Мокированный метод для имитации ответа провайдера, возвращающего генератор. Возвращает генератор, который вызывает исключение `RuntimeError`.

### `class YieldNoneProviderMock(AsyncGeneratorProvider)`

**Описание**: Мокированный класс, имитирующий провайдер GPT4Free, который возвращает генератор, выдающий значение `None`.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:
- `working (bool)`: Флаг, указывающий на доступность провайдера.

**Methods**:
- `create_async_generator(model, messages, stream, **kwargs)`: Мокированный метод для имитации ответа провайдера, возвращающего генератор. Возвращает генератор, который выдает значение `None`.

## Примеры

### Тестирование с мокированным провайдером

```python
from hypotez.src.endpoints.gpt4free.etc.unittest.mocks import ProviderMock

# Использование мокированного провайдера
provider = ProviderMock()
result = provider.create_completion(model="test_model", messages=[], stream=False)

# Ожидаемый результат:
# result = "Mock"
```

### Тестирование с мокированным провайдером, вызывающим исключение

```python
from hypotez.src.endpoints.gpt4free.etc.unittest.mocks import MissingAuthProviderMock

# Использование мокированного провайдера
provider = MissingAuthProviderMock()

try:
    provider.create_completion(model="test_model", messages=[], stream=False)
except MissingAuthError as ex:
    # Обработка исключения MissingAuthError
    print(f"Ошибка аутентификации: {ex}")
```