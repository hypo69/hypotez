# Module src.endpoints.gpt4free.g4f.Provider.deprecated.Cromicle

## Обзор

Модуль `Cromicle` предоставляет класс `Cromicle`, который является асинхронным генераторным провайдером для взаимодействия с сервисом cromicle.top.
Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и предоставляет функциональность для генерации текста на основе модели GPT-3.5 Turbo.
Модуль включает функции для создания заголовков и полезной нагрузки запроса.

## Подробнее

Этот модуль предназначен для интеграции с другими частями проекта `hypotez`, где требуется взаимодействие с API cromicle.top для генерации текста. Он обеспечивает асинхронный интерфейс, что позволяет эффективно обрабатывать запросы без блокировки основного потока выполнения.

## Классы

### `Cromicle`

**Описание**:
Класс `Cromicle` является асинхронным генераторным провайдером для взаимодействия с API cromicle.top.

**Наследует**:
`AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL-адрес сервиса cromicle.top.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий, поддерживает ли провайдер модель GPT-3.5 Turbo.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API cromicle.top.

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для получения ответов от API cromicle.top.

    Args:
        cls (type[Cromicle]): Класс `Cromicle`.
        model (str): Имя модели для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий текст ответа.

    Принцип работы:
        1. Создает HTTP-сессию с заголовками, созданными функцией `_create_header`.
        2. Выполняет POST-запрос к API cromicle.top с использованием `aiohttp`.
        3. Отправляет данные в формате JSON, созданные функцией `_create_payload`.
        4. Получает ответ в виде потока данных.
        5. Декодирует поток данных и выдает его частями через генератор.

    Примеры:
        Пример использования функции с указанием модели и сообщений:

        >>> model = "gpt-3.5-turbo"
        >>> messages = [{"role": "user", "content": "Hello, world!"}]
        >>> async def example():
        ...     async for message in Cromicle.create_async_generator(model=model, messages=messages):
        ...         print(message)
        >>> import asyncio
        >>> asyncio.run(example())
    """
```

## Функции

### `_create_header`

```python
def _create_header() -> Dict[str, str]:
    """Создает словарь с заголовками для HTTP-запроса.

    Returns:
        Dict[str, str]: Словарь с заголовками.

    Принцип работы:
        Функция создает словарь, содержащий заголовки 'accept' и 'content-type', необходимые для выполнения HTTP-запроса.

    Примеры:
        >>> _create_header()
        {'accept': '*/*', 'content-type': 'application/json'}
    """
```

### `_create_payload`

```python
def _create_payload(message: str) -> Dict[str, str]:
    """Создает словарь с полезной нагрузкой для HTTP-запроса.

    Args:
        message (str): Сообщение для отправки.

    Returns:
        Dict[str, str]: Словарь с полезной нагрузкой.

    Принцип работы:
        Функция создает словарь, содержащий сообщение, токен и хеш сообщения.
        Хеш вычисляется с использованием SHA256.

    Примеры:
        >>> _create_payload("Hello")
        {'message': 'Hello', 'token': 'abc', 'hash': '68d54a9d2ee960b66161c964a9314f15a5974adef27bb149e48106589a4dd294'}
    """