# Модуль mocks.py
## Обзор

Модуль содержит моки (заглушки) для различных провайдеров g4f (GPT4Free). Эти моки используются для целей юнит-тестирования, позволяя имитировать поведение различных провайдеров без необходимости реального подключения к ним.

## Подробней

Модуль предоставляет набор классов, каждый из которых имитирует определенный аспект поведения провайдера, например, успешное выполнение запроса, генерацию асинхронного ответа, генерацию изображений, отсутствие аутентификации или возникновение исключения. Это позволяет изолированно тестировать компоненты, использующие g4f, и убедиться, что они корректно обрабатывают различные сценарии.

## Классы

### `ProviderMock`

**Описание**: Мок для абстрактного провайдера.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `working` (bool): Всегда `True`, указывает на то, что провайдер работает.

**Методы**:
- `create_completion`: Имитирует создание завершения текста.

#### `create_completion`

```python
    @classmethod
    def create_completion(
        cls, model, messages, stream, **kwargs
    ):
        """
        Имитирует создание завершения текста.

        Args:
            cls: Ссылка на класс.
            model: Модель для использования.
            messages: Список сообщений для завершения.
            stream: Флаг стриминга.
            **kwargs: Дополнительные аргументы.

        Returns:
            Generator[str, None, None]: Генератор, возвращающий строку "Mock".
        """
        ...
```

### `AsyncProviderMock`

**Описание**: Мок для асинхронного провайдера.

**Наследует**: `AsyncProvider`

**Атрибуты**:
- `working` (bool): Всегда `True`, указывает на то, что провайдер работает.

**Методы**:
- `create_async`: Имитирует создание асинхронного ответа.

#### `create_async`

```python
    @classmethod
    async def create_async(
        cls, model, messages, **kwargs
    ):
        """
        Имитирует создание асинхронного ответа.

        Args:
            cls: Ссылка на класс.
            model: Модель для использования.
            messages: Список сообщений для завершения.
            **kwargs: Дополнительные аргументы.

        Returns:
            str: Строка "Mock".
        """
        ...
```

### `AsyncGeneratorProviderMock`

**Описание**: Мок для асинхронного провайдера-генератора.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `working` (bool): Всегда `True`, указывает на то, что провайдер работает.

**Методы**:
- `create_async_generator`: Имитирует создание асинхронного генератора.

#### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls, model, messages, stream, **kwargs
    ):
        """
        Имитирует создание асинхронного генератора.

        Args:
            cls: Ссылка на класс.
            model: Модель для использования.
            messages: Список сообщений для завершения.
            stream: Флаг стриминга.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncGenerator[str, None]: Асинхронный генератор, возвращающий строку "Mock".
        """
        ...
```

### `ModelProviderMock`

**Описание**: Мок для провайдера, возвращающего имя модели.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `working` (bool): Всегда `True`, указывает на то, что провайдер работает.

**Методы**:
- `create_completion`: Имитирует создание завершения текста, возвращая имя модели.

#### `create_completion`

```python
    @classmethod
    def create_completion(
        cls, model, messages, stream, **kwargs
    ):
        """
        Имитирует создание завершения текста, возвращая имя модели.

        Args:
            cls: Ссылка на класс.
            model: Модель для использования.
            messages: Список сообщений для завершения.
            stream: Флаг стриминга.
            **kwargs: Дополнительные аргументы.

        Returns:
            Generator[str, None, None]: Генератор, возвращающий имя модели.
        """
        ...
```

### `YieldProviderMock`

**Описание**: Мок для асинхронного провайдера-генератора, возвращающего содержимое сообщений.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `working` (bool): Всегда `True`, указывает на то, что провайдер работает.

**Методы**:
- `create_async_generator`: Имитирует создание асинхронного генератора, возвращая содержимое каждого сообщения.

#### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls, model, messages, stream, **kwargs
    ):
        """
        Имитирует создание асинхронного генератора, возвращая содержимое сообщений.

        Args:
            cls: Ссылка на класс.
            model: Модель для использования.
            messages: Список сообщений для завершения.
            stream: Флаг стриминга.
            **kwargs: Дополнительные аргументы.

        Yields:
            str: Содержимое каждого сообщения.
        """
        ...
```

### `YieldImageResponseProviderMock`

**Описание**: Мок для асинхронного провайдера-генератора, возвращающего объект `ImageResponse`.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `working` (bool): Всегда `True`, указывает на то, что провайдер работает.

**Методы**:
- `create_async_generator`: Имитирует создание асинхронного генератора, возвращая объект `ImageResponse`.

#### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls, model, messages, stream, prompt: str, **kwargs
    ):
        """
        Имитирует создание асинхронного генератора, возвращающего объект `ImageResponse`.

        Args:
            cls: Ссылка на класс.
            model: Модель для использования.
            messages: Список сообщений для завершения.
            stream: Флаг стриминга.
            prompt (str): Запрос для генерации изображения.
            **kwargs: Дополнительные аргументы.

        Yields:
            ImageResponse: Объект `ImageResponse` с заданным запросом и пустой строкой.
        """
        ...
```

### `MissingAuthProviderMock`

**Описание**: Мок для провайдера, вызывающего исключение `MissingAuthError`.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `working` (bool): Всегда `True`, указывает на то, что провайдер работает.

**Методы**:
- `create_completion`: Имитирует создание завершения текста, вызывая исключение `MissingAuthError`.

#### `create_completion`

```python
    @classmethod
    def create_completion(
        cls, model, messages, stream, **kwargs
    ):
        """
        Имитирует создание завершения текста, вызывая исключение `MissingAuthError`.

        Args:
            cls: Ссылка на класс.
            model: Модель для использования.
            messages: Список сообщений для завершения.
            stream: Флаг стриминга.
            **kwargs: Дополнительные аргументы.

        Raises:
            MissingAuthError: Всегда вызывается.

        Yields:
            str: Никогда не возвращается, так как всегда вызывается исключение.
        """
        ...
```

### `RaiseExceptionProviderMock`

**Описание**: Мок для провайдера, вызывающего исключение `RuntimeError`.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `working` (bool): Всегда `True`, указывает на то, что провайдер работает.

**Методы**:
- `create_completion`: Имитирует создание завершения текста, вызывая исключение `RuntimeError`.

#### `create_completion`

```python
    @classmethod
    def create_completion(
        cls, model, messages, stream, **kwargs
    ):
        """
        Имитирует создание завершения текста, вызывая исключение `RuntimeError`.

        Args:
            cls: Ссылка на класс.
            model: Модель для использования.
            messages: Список сообщений для завершения.
            stream: Флаг стриминга.
            **kwargs: Дополнительные аргументы.

        Raises:
            RuntimeError: Всегда вызывается.

        Yields:
            str: Никогда не возвращается, так как всегда вызывается исключение.
        """
        ...
```

### `AsyncRaiseExceptionProviderMock`

**Описание**: Мок для асинхронного провайдера-генератора, вызывающего исключение `RuntimeError`.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `working` (bool): Всегда `True`, указывает на то, что провайдер работает.

**Методы**:
- `create_async_generator`: Имитирует создание асинхронного генератора, вызывая исключение `RuntimeError`.

#### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls, model, messages, stream, **kwargs
    ):
        """
        Имитирует создание асинхронного генератора, вызывая исключение `RuntimeError`.

        Args:
            cls: Ссылка на класс.
            model: Модель для использования.
            messages: Список сообщений для завершения.
            stream: Флаг стриминга.
            **kwargs: Дополнительные аргументы.

        Raises:
            RuntimeError: Всегда вызывается.

        Yields:
            str: Никогда не возвращается, так как всегда вызывается исключение.
        """
        ...
```

### `YieldNoneProviderMock`

**Описание**: Мок для асинхронного провайдера-генератора, возвращающего `None`.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `working` (bool): Всегда `True`, указывает на то, что провайдер работает.

**Методы**:
- `create_async_generator`: Имитирует создание асинхронного генератора, возвращая `None`.

#### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls, model, messages, stream, **kwargs
    ):
        """
        Имитирует создание асинхронного генератора, возвращая `None`.

        Args:
            cls: Ссылка на класс.
            model: Модель для использования.
            messages: Список сообщений для завершения.
            stream: Флаг стриминга.
            **kwargs: Дополнительные аргументы.

        Yields:
            None: Всегда возвращает `None`.
        """
        ...
```