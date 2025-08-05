# Модуль с моками провайдеров для тестирования g4f
## Обзор

Модуль содержит классы, представляющие собой моки различных провайдеров для использования в юнит-тестах библиотеки `g4f`. Эти моки позволяют имитировать поведение реальных провайдеров, не требуя подключения к внешним сервисам, что упрощает и ускоряет тестирование.

## Подробней

Этот модуль предоставляет набор мок-классов, каждый из которых имитирует определенный аспект работы провайдеров в библиотеке `g4f`. Они используются для изоляции тестируемого кода от реальных API и для проверки корректности обработки различных сценариев, таких как успешное завершение, асинхронные операции, генерация данных и возникновение ошибок.

## Классы

### `ProviderMock`

**Описание**: Мок-класс, имитирующий базового провайдера.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии (`True`).

**Методы**:
- `create_completion`: Генерирует строку "Mock".

### `AsyncProviderMock`

**Описание**: Мок-класс, имитирующий асинхронного провайдера.

**Наследует**: `AsyncProvider`

**Атрибуты**:
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии (`True`).

**Методы**:
- `create_async`: Асинхронно возвращает строку "Mock".

### `AsyncGeneratorProviderMock`

**Описание**: Мок-класс, имитирующий асинхронного провайдера-генератора.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии (`True`).

**Методы**:
- `create_async_generator`: Асинхронно генерирует строку "Mock".

### `ModelProviderMock`

**Описание**: Мок-класс, который возвращает название модели.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии (`True`).

**Методы**:
- `create_completion`: Генерирует название модели, переданной в качестве аргумента.

### `YieldProviderMock`

**Описание**: Мок-класс, который генерирует содержимое сообщений.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии (`True`).

**Методы**:
- `create_async_generator`: Асинхронно генерирует содержимое каждого сообщения из списка сообщений.

### `YieldImageResponseProviderMock`

**Описание**: Мок-класс, который генерирует объект `ImageResponse`.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии (`True`).

**Методы**:
- `create_async_generator`: Асинхронно генерирует объект `ImageResponse` с переданными параметрами `prompt` и пустой строкой.

### `MissingAuthProviderMock`

**Описание**: Мок-класс, имитирующий провайдера, требующего аутентификацию и выбрасывающего исключение `MissingAuthError`.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии (`True`).

**Методы**:
- `create_completion`: Вызывает исключение `MissingAuthError`.

### `RaiseExceptionProviderMock`

**Описание**: Мок-класс, имитирующий провайдера, который выбрасывает исключение `RuntimeError`.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии (`True`).

**Методы**:
- `create_completion`: Вызывает исключение `RuntimeError`.

### `AsyncRaiseExceptionProviderMock`

**Описание**: Мок-класс, имитирующий асинхронного провайдера, который выбрасывает исключение `RuntimeError`.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии (`True`).

**Методы**:
- `create_async_generator`: Асинхронно вызывает исключение `RuntimeError`.

### `YieldNoneProviderMock`

**Описание**: Мок-класс, имитирующий провайдера, который генерирует `None`.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии (`True`).

**Методы**:
- `create_async_generator`: Асинхронно генерирует значение `None`.

## Методы класса

### `ProviderMock`

#### `create_completion`

```python
@classmethod
def create_completion(
    cls, model, messages, stream, **kwargs
):
    """
    Генерирует строку "Mock".

    Args:
        cls: Ссылка на класс.
        model: Модель для генерации (не используется).
        messages: Список сообщений (не используется).
        stream: Флаг потоковой передачи (не используется).
        **kwargs: Дополнительные аргументы (не используются).

    Returns:
        str: Строка "Mock".
    """
```

### `AsyncProviderMock`

#### `create_async`

```python
@classmethod
async def create_async(
    cls, model, messages, **kwargs
):
    """
    Асинхронно возвращает строку "Mock".

    Args:
        cls: Ссылка на класс.
        model: Модель для генерации (не используется).
        messages: Список сообщений (не используется).
        **kwargs: Дополнительные аргументы (не используются).

    Returns:
        str: Строка "Mock".
    """
```

### `AsyncGeneratorProviderMock`

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls, model, messages, stream, **kwargs
):
    """
    Асинхронно генерирует строку "Mock".

    Args:
        cls: Ссылка на класс.
        model: Модель для генерации (не используется).
        messages: Список сообщений (не используется).
        stream: Флаг потоковой передачи (не используется).
        **kwargs: Дополнительные аргументы (не используются).

    Yields:
        str: Строка "Mock".
    """
```

### `ModelProviderMock`

#### `create_completion`

```python
@classmethod
def create_completion(
    cls, model, messages, stream, **kwargs
):
    """
    Генерирует название модели, переданной в качестве аргумента.

    Args:
        cls: Ссылка на класс.
        model: Модель для генерации.
        messages: Список сообщений (не используется).
        stream: Флаг потоковой передачи (не используется).
        **kwargs: Дополнительные аргументы (не используются).

    Returns:
        str: Название модели.
    """
```

### `YieldProviderMock`

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls, model, messages, stream, **kwargs
):
    """
    Асинхронно генерирует содержимое каждого сообщения из списка сообщений.

    Args:
        cls: Ссылка на класс.
        model: Модель для генерации (не используется).
        messages: Список сообщений.
        stream: Флаг потоковой передачи (не используется).
        **kwargs: Дополнительные аргументы (не используются).

    Yields:
        str: Содержимое каждого сообщения.
    """
```

### `YieldImageResponseProviderMock`

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls, model, messages, stream, prompt: str, **kwargs
):
    """
    Асинхронно генерирует объект `ImageResponse` с переданными параметрами `prompt` и пустой строкой.

    Args:
        cls: Ссылка на класс.
        model: Модель для генерации (не используется).
        messages: Список сообщений (не используется).
        stream: Флаг потоковой передачи (не используется).
        prompt (str): Текст запроса для генерации изображения.
        **kwargs: Дополнительные аргументы (не используются).

    Yields:
        ImageResponse: Объект `ImageResponse`.
    """
```

### `MissingAuthProviderMock`

#### `create_completion`

```python
@classmethod
def create_completion(
    cls, model, messages, stream, **kwargs
):
    """
    Вызывает исключение `MissingAuthError`.

    Args:
        cls: Ссылка на класс.
        model: Модель для генерации (не используется).
        messages: Список сообщений (не используется).
        stream: Флаг потоковой передачи (не используется).
        **kwargs: Дополнительные аргументы (не используются).

    Raises:
        MissingAuthError: Всегда выбрасывается.
    """
```

### `RaiseExceptionProviderMock`

#### `create_completion`

```python
@classmethod
def create_completion(
    cls, model, messages, stream, **kwargs
):
    """
    Вызывает исключение `RuntimeError`.

    Args:
        cls: Ссылка на класс.
        model: Модель для генерации (не используется).
        messages: Список сообщений (не используется).
        stream: Флаг потоковой передачи (не используется).
        **kwargs: Дополнительные аргументы (не используются).

    Raises:
        RuntimeError: Всегда выбрасывается.
    """
```

### `AsyncRaiseExceptionProviderMock`

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls, model, messages, stream, **kwargs
):
    """
    Асинхронно вызывает исключение `RuntimeError`.

    Args:
        cls: Ссылка на класс.
        model: Модель для генерации (не используется).
        messages: Список сообщений (не используется).
        stream: Флаг потоковой передачи (не используется).
        **kwargs: Дополнительные аргументы (не используются).

    Raises:
        RuntimeError: Всегда выбрасывается.
    """
```

### `YieldNoneProviderMock`

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls, model, messages, stream, **kwargs
):
    """
    Асинхронно генерирует значение `None`.

    Args:
        cls: Ссылка на класс.
        model: Модель для генерации (не используется).
        messages: Список сообщений (не используется).
        stream: Флаг потоковой передачи (не используется).
        **kwargs: Дополнительные аргументы (не используются).

    Yields:
        None: Значение `None`.
    """