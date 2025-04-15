# Модуль `AI365VIP`

## Обзор

Модуль предоставляет класс `AI365VIP`, который является асинхронным генератором для взаимодействия с API AI365VIP. 
Он позволяет генерировать ответы от моделей, таких как `gpt-3.5-turbo` и `gpt-4o`.

## Подробнее

Этот модуль предназначен для интеграции с AI365VIP для получения ответов от различных моделей. 
Он использует `aiohttp` для выполнения асинхронных HTTP-запросов.

## Классы

### `AI365VIP`

**Описание**: Класс для взаимодействия с API AI365VIP.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса AI365VIP.
- `api_endpoint` (str): Endpoint API для чата.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь с псевдонимами моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API.

## Методы класса

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
    """Создает асинхронный генератор для получения ответов от API AI365VIP.

    Args:
        cls: Ссылка на класс.
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от API.

    Raises:
        Exception: Если возникает ошибка при выполнении запроса.

    Как работает функция:
    - Функция принимает модель, сообщения и прокси (опционально).
    - Формирует HTTP-заголовки для запроса.
    - Создает асинхронную сессию с использованием `aiohttp`.
    - Формирует данные запроса в формате JSON, включая модель, сообщения и параметры.
    - Отправляет POST-запрос к API.
    - Получает асинхронные чанки данных из ответа и декодирует их.
    - Возвращает асинхронный генератор, выдающий декодированные чанки.

    Примеры:
        >>> model = 'gpt-3.5-turbo'
        >>> messages = [{'role': 'user', 'content': 'Hello, how are you?'}]
        >>> generator = AI365VIP.create_async_generator(model=model, messages=messages)
        >>> async for chunk in generator:
        ...     print(chunk)
    """
    ...
```

## Параметры класса

- `url` (str): URL сервиса AI365VIP.
- `api_endpoint` (str): Endpoint API для чата.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь с псевдонимами моделей.

## Примеры

```python
model = 'gpt-3.5-turbo'
messages = [{'role': 'user', 'content': 'Hello, how are you?'}]
generator = AI365VIP.create_async_generator(model=model, messages=messages)
async for chunk in generator:
    print(chunk)