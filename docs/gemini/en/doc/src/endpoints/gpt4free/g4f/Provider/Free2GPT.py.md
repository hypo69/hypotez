# Документация модуля Free2GPT

## Обзор

Модуль `Free2GPT.py` предоставляет асинхронный интерфейс для взаимодействия с сервисом Free2GPT, который использует модели Gemini для генерации текста. Он включает в себя функции для создания асинхронных генераторов, обработки сообщений и генерации подписей для запросов.

## Подробнее

Модуль предназначен для использования в асинхронных приложениях, где требуется взаимодействие с API Free2GPT. Он поддерживает указание прокси-сервера и использование истории сообщений.

## Классы

### `Free2GPT`

**Описание**: Класс, представляющий провайдера Free2GPT.

**Наследует**:
- `AsyncGeneratorProvider`: Предоставляет базовый класс для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями провайдера.

**Атрибуты**:
- `url` (str): URL-адрес сервиса Free2GPT (`https://chat10.free2gpt.xyz`).
- `working` (bool): Указывает, работает ли провайдер (`True`).
- `supports_message_history` (bool): Указывает, поддерживается ли история сообщений (`True`).
- `default_model` (str): Модель, используемая по умолчанию (`gemini-1.5-pro`).
- `models` (List[str]): Список поддерживаемых моделей (`[default_model, 'gemini-1.5-flash']`).

**Принцип работы**:
Класс использует асинхронные запросы для взаимодействия с API Free2GPT. Он генерирует подпись для каждого запроса, чтобы обеспечить его безопасность.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    connector: BaseConnector = None,
    **kwargs,
) -> AsyncResult:
    """Создает асинхронный генератор для взаимодействия с API Free2GPT.

    Args:
        cls: Класс, для которого создается генератор.
        model (str): Модель, которую следует использовать для генерации.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL-адрес прокси-сервера. По умолчанию `None`.
        connector (BaseConnector, optional): Aiohttp коннектор. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий чанки текста.

    Raises:
        RateLimitError: Если достигнут лимит запросов.
        Exception: При возникновении других ошибок при выполнении запроса.

    Как работает функция:
    - Формирует заголовки запроса, включая User-Agent, Accept и Content-Type.
    - Создает объект ClientSession для выполнения асинхронных запросов.
    - Генерирует timestamp и подпись для запроса.
    - Отправляет POST-запрос к API Free2GPT с использованием указанных данных.
    - Обрабатывает ответ, проверяя на наличие ошибок и лимитов запросов.
    - Возвращает асинхронный генератор, который выдает чанки текста из ответа.

    Пример:
        messages = [{"role": "user", "content": "Hello, Free2GPT!"}]
        async for chunk in Free2GPT.create_async_generator(model="gemini-1.5-pro", messages=messages):
            print(chunk, end="")
    """
```

## Функции

### `generate_signature`

```python
def generate_signature(time: int, text: str, secret: str = ""):
    """Генерирует подпись SHA256 для запроса.

    Args:
        time (int): Timestamp запроса.
        text (str): Текст сообщения.
        secret (str, optional): Секретный ключ. По умолчанию "".

    Returns:
        str: SHA256 хеш, представляющий подпись.

    Как работает функция:
    - Функция конкатенирует timestamp, текст сообщения и секретный ключ в одну строку.
    - Затем вычисляет SHA256 хеш от этой строки.
    - Возвращает полученный хеш в шестнадцатеричном формате.

    Пример:
        signature = generate_signature(1678886400, "Hello, World!", "secret")
        print(signature)
    """
```