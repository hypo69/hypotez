# Module src.endpoints.gpt4free.g4f.Provider.not_working.AiChats

## Обзор

Модуль `AiChats.py` предоставляет асинхронный интерфейс для взаимодействия с сервисом AiChats для генерации текста и изображений. Он поддерживает как текстовые запросы через модель `gpt-4`, так и запросы на генерацию изображений через модель `dalle`. Модуль использует `aiohttp` для выполнения асинхронных HTTP-запросов и возвращает результаты в виде асинхронного генератора.

## Более подробно

Модуль `AiChats` предназначен для интеграции с другими частями проекта `hypotez`, требующими взаимодействия с AI-сервисами. Он предоставляет удобный способ отправки запросов к AiChats и обработки ответов, включая обработку ошибок и форматирование данных. Модуль поддерживает использование прокси-серверов для обеспечения анонимности или обхода географических ограничений.

## Classes

### `AiChats`

**Описание**: Класс `AiChats` предоставляет функциональность для взаимодействия с сервисом AiChats. Он наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую структуру для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса AiChats (`https://ai-chats.org`).
- `api_endpoint` (str): URL API-endpoint для отправки запросов (`https://ai-chats.org/chat/send2/`).
- `working` (bool): Указывает, работает ли сервис (по умолчанию `False`).
- `supports_message_history` (bool): Указывает, поддерживает ли сервис историю сообщений (по умолчанию `True`).
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4`).
- `models` (list[str]): Список поддерживаемых моделей (`['gpt-4', 'dalle']`).

**Принцип работы**:
Класс использует `aiohttp` для отправки асинхронных запросов к API AiChats. Он поддерживает два типа запросов: текстовые (через модель `gpt-4`) и запросы на генерацию изображений (через модель `dalle`). Результаты возвращаются в виде асинхронного генератора, что позволяет обрабатывать большие объемы данных порционно.

## Class Methods

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
    """ Создает асинхронный генератор для взаимодействия с AiChats.

    Args:
        cls (AiChats): Класс AiChats.
        model (str): Модель для использования (`gpt-4` или `dalle`).
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий результаты от AiChats.

    Как работает функция:
    - Функция формирует заголовки HTTP-запроса, включая cookie и user-agent.
    - В зависимости от выбранной модели (`dalle` или `gpt-4`) формируется запрос.
    - Для модели `dalle` извлекается последний запрос пользователя.
    - Для модели `gpt-4` используется функция `format_prompt` для форматирования запроса.
    - Отправляет POST-запрос к API AiChats с использованием `aiohttp`.
    - Обрабатывает ответ от API:
        - Для модели `dalle` извлекает URL изображения из JSON-ответа и загружает изображение, кодирует его в base64 и возвращает `ImageResponse`.
        - Для модели `gpt-4` извлекает текстовые сообщения из потока данных и возвращает их.
    - Обрабатывает возможные исключения и возвращает сообщения об ошибках.
    """
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
    """ Создает асинхронный запрос к AiChats и возвращает результат.

    Args:
        cls (AiChats): Класс AiChats.
        model (str): Модель для использования (`gpt-4` или `dalle`).
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        str: Результат от AiChats (текст или URL изображения).

    Как работает функция:
    - Функция вызывает `create_async_generator` для получения асинхронного генератора.
    - Перебирает результаты, возвращаемые генератором.
    - Если результат является `ImageResponse`, возвращает URL первого изображения.
    - В противном случае возвращает результат как строку.
    """
```

## Примеры

### Пример использования `create_async_generator`

```python
# Пример вызова create_async_generator
async for response in AiChats.create_async_generator(model='gpt-4', messages=[{'role': 'user', 'content': 'Hello, how are you?'}], proxy=None):
    print(response)
```

### Пример использования `create_async`

```python
# Пример вызова create_async
result = await AiChats.create_async(model='dalle', messages=[{'role': 'user', 'content': 'Generate an image of a cat.'}], proxy=None)
print(result)
```