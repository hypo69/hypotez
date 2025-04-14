# Модуль AiChats

## Обзор

Модуль `AiChats` предоставляет асинхронный интерфейс для взаимодействия с сервисом ai-chats.org. Он поддерживает как текстовые запросы через модель `gpt-4`, так и генерацию изображений с использованием модели `dalle`. Модуль использует `aiohttp` для асинхронных HTTP-запросов и предоставляет функциональность для форматирования запросов и обработки ответов, включая извлечение и кодирование изображений в формат base64.

## Подробней

Модуль предназначен для интеграции с другими частями проекта, где требуется взаимодействие с AI-моделями через API ai-chats.org. Он поддерживает проксирование запросов, что позволяет использовать его в различных сетевых конфигурациях. Важной особенностью является поддержка истории сообщений, что позволяет вести контекстные диалоги с моделью.

## Классы

### `AiChats`

**Описание**: Класс `AiChats` является асинхронным провайдером, предоставляющим методы для генерации текста и изображений с использованием API ai-chats.org.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию результатов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса ai-chats.org.
- `api_endpoint` (str): URL API для отправки запросов.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `supports_message_history` (bool): Поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4`).
- `models` (list): Список поддерживаемых моделей (`gpt-4`, `dalle`).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для обработки запросов к API.
- `create_async`: Отправляет запрос к API и возвращает результат.

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
    """Создает асинхронный генератор для взаимодействия с API ai-chats.org.

    Args:
        cls (AiChats): Ссылка на класс.
        model (str): Модель для использования (`gpt-4` или `dalle`).
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий результаты от API.

    Raises:
        Exception: Если происходит ошибка при отправке запроса или обработке ответа.

    Внутренние функции:
        Отсутствуют

    Как работает функция:
        1. Формирует заголовки запроса, включая cookies и user-agent.
        2. В зависимости от выбранной модели (`dalle` или `gpt-4`) формирует запрос.
        3. Отправляет запрос к API с использованием `aiohttp.ClientSession`.
        4. Обрабатывает ответ от API:
            - Для модели `dalle`: извлекает URL изображения из JSON-ответа, загружает изображение, кодирует его в base64 и возвращает в виде `ImageResponse`.
            - Для модели `gpt-4`: извлекает текстовые сообщения из потока данных и возвращает их.
        5. В случае ошибки возвращает сообщение об ошибке.

    Примеры:
        Пример использования с моделью `gpt-4`:
        ```python
        messages = [{"role": "user", "content": "Hello, how are you?"}]
        async for response in AiChats.create_async_generator(model='gpt-4', messages=messages):
            print(response)
        ```

        Пример использования с моделью `dalle`:
        ```python
        messages = [{"role": "user", "content": "Generate a picture of a cat."}]
        async for response in AiChats.create_async_generator(model='dalle', messages=messages):
            print(response)
        ```
    """
    ...
```

### `create_async`

```python
@classmethod
async def create_async(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    **kwargs
) -> str:
    """Отправляет запрос к API ai-chats.org и возвращает результат.

    Args:
        cls (AiChats): Ссылка на класс.
        model (str): Модель для использования (`gpt-4` или `dalle`).
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        str: Результат от API (текст или URL изображения).

    Raises:
        Отсутствуют

    Как работает функция:
        1. Вызывает `create_async_generator` для получения асинхронного генератора.
        2. Итерируется по генератору и возвращает первый результат.
        3. Если результат является экземпляром `ImageResponse`, возвращает URL изображения.
        4. В противном случае возвращает текстовый ответ.

    Примеры:
        Пример использования с моделью `gpt-4`:
        ```python
        messages = [{"role": "user", "content": "Hello, how are you?"}]
        response = await AiChats.create_async(model='gpt-4', messages=messages)
        print(response)
        ```

        Пример использования с моделью `dalle`:
        ```python
        messages = [{"role": "user", "content": "Generate a picture of a cat."}]
        response = await AiChats.create_async(model='dalle', messages=messages)
        print(response)
        ```
    """
    ...
```

## Параметры класса

- `url` (str): URL сервиса ai-chats.org. Используется для определения источника запросов.
- `api_endpoint` (str): URL API для отправки запросов.
- `working` (bool): Указывает, работает ли провайдер в данный момент. Может использоваться для мониторинга доступности сервиса.
- `supports_message_history` (bool): Поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4`).
- `models` (list): Список поддерживаемых моделей (`gpt-4`, `dalle`).

## Примеры

Пример использования класса `AiChats` для генерации текста:

```python
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for response in AiChats.create_async_generator(model='gpt-4', messages=messages):
    print(response)
```

Пример использования класса `AiChats` для генерации изображения:

```python
messages = [{"role": "user", "content": "Generate a picture of a cat."}]
async for response in AiChats.create_async_generator(model='dalle', messages=messages):
    print(response)