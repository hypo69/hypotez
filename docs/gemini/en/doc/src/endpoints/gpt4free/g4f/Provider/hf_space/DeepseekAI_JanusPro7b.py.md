# Модуль DeepseekAI_JanusPro7b

## Обзор

Модуль `DeepseekAI_JanusPro7b` предназначен для взаимодействия с моделью Janus-Pro-7B от Deepseek AI, размещенной на платформе Hugging Face Spaces. Этот модуль предоставляет асинхронный генератор для обработки текстовых и графических запросов к модели, а также поддерживает потоковую передачу данных.

## Более подробно

Модуль использует асинхронные запросы для взаимодействия с API Hugging Face Spaces, обеспечивая эффективную обработку запросов. Он поддерживает как текстовые, так и графические запросы, а также позволяет передавать историю сообщений и использовать прокси-серверы.

## Классы

### `DeepseekAI_JanusPro7b`

**Описание**: Класс `DeepseekAI_JanusPro7b` является реализацией асинхронного генератора для взаимодействия с моделью Janus-Pro-7B.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("DeepseekAI Janus-Pro-7B").
- `space` (str): Имя пространства на Hugging Face ("deepseek-ai/Janus-Pro-7B").
- `url` (str): URL пространства на Hugging Face.
- `api_url` (str): Базовый URL API.
- `referer` (str): Referer для HTTP-запросов.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель по умолчанию ("janus-pro-7b").
- `default_image_model` (str): Модель для обработки изображений по умолчанию ("janus-pro-7b-image").
- `default_vision_model` (str): Модель для обработки визуальных данных по умолчанию.
- `image_models` (list[str]): Список моделей для обработки изображений.
- `vision_models` (list[str]): Список моделей для обработки визуальных данных.
- `models` (list[str]): Объединенный список моделей для визуальных данных и изображений.

**Принцип работы**:
Класс использует асинхронные запросы к API Hugging Face Spaces для отправки текстовых и графических запросов к модели Janus-Pro-7B. Он обрабатывает ответы API, извлекая текстовые и графические данные, и предоставляет их в виде асинхронного генератора.

**Методы**:
- `run`: Выполняет HTTP-запрос к API.
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с моделью.

## Методы класса

### `run`

```python
@classmethod
def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, image: dict = None, seed: int = 0):
    """
    Выполняет HTTP-запрос к API.

    Args:
        cls (DeepseekAI_JanusPro7b): Класс.
        method (str): HTTP-метод ("post" или "image").
        session (StreamSession): Асинхронная сессия для выполнения запросов.
        prompt (str): Текст запроса.
        conversation (JsonConversation): Объект, содержащий информацию о сессии.
        image (dict, optional): Данные изображения. По умолчанию `None`.
        seed (int, optional): Зерно для генерации случайных чисел. По умолчанию 0.

    Returns:
        StreamResponse: Объект ответа от API.
    """
```

**Как работает**:
Функция `run` выполняет HTTP-запрос к API Hugging Face Spaces в зависимости от указанного метода (`post` для текстовых запросов, `image` для графических). Она формирует заголовки запроса, включая токен и UUID, и отправляет запрос с соответствующими данными.

**Примеры**:
```python
# Пример вызова метода run
async with StreamSession() as session:
    response = await DeepseekAI_JanusPro7b.run(
        method="post",
        session=session,
        prompt="Hello, world!",
        conversation=JsonConversation(session_hash="123", zerogpu_token="token", zerogpu_uuid="uuid"),
        seed=12345
    )
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    media: MediaListType = None,
    prompt: str = None,
    proxy: str = None,
    cookies: Cookies = None,
    api_key: str = None,
    zerogpu_uuid: str = "[object Object]",
    return_conversation: bool = False,
    conversation: JsonConversation = None,
    seed: int = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с моделью.

    Args:
        cls (DeepseekAI_JanusPro7b): Класс.
        model (str): Имя модели.
        messages (Messages): Список сообщений для формирования запроса.
        media (MediaListType, optional): Список медиафайлов. По умолчанию `None`.
        prompt (str, optional): Текст запроса. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        cookies (Cookies, optional): Cookies для HTTP-запросов. По умолчанию `None`.
        api_key (str, optional): API-ключ. По умолчанию `None`.
        zerogpu_uuid (str, optional): UUID. По умолчанию "[object Object]".
        return_conversation (bool, optional): Флаг, указывающий, возвращать ли объект conversation. По умолчанию `False`.
        conversation (JsonConversation, optional): Объект, содержащий информацию о сессии. По умолчанию `None`.
        seed (int, optional): Зерно для генерации случайных чисел. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Yields:
        AsyncResult: Результаты работы генератора.
    """
```

**Как работает**:
Функция `create_async_generator` создает асинхронный генератор, который отправляет запросы к API Hugging Face Spaces и возвращает результаты. Она определяет метод запроса (`post` или `image`) в зависимости от типа запроса (текст или изображение), формирует запрос, получает токен и UUID, и отправляет запрос с использованием асинхронной сессии. Функция также обрабатывает медиафайлы, загружая их на сервер и передавая их в запросе.

**Примеры**:
```python
# Пример вызова метода create_async_generator
async def main():
    async for result in DeepseekAI_JanusPro7b.create_async_generator(
        model="janus-pro-7b",
        messages=[{"role": "user", "content": "Hello, world!"}]
    ):
        print(result)

# Запуск асинхронной функции
# asyncio.run(main())
```

## Внутренние функции

### `get_zerogpu_token`

```python
async def get_zerogpu_token(space: str, session: StreamSession, conversation: JsonConversation, cookies: Cookies = None):
    """
    Получает zerogpu_token и zerogpu_uuid.

    Args:
        space (str): Имя пространства на Hugging Face.
        session (StreamSession): Асинхронная сессия для выполнения запросов.
        conversation (JsonConversation): Объект, содержащий информацию о сессии.
        cookies (Cookies, optional): Cookies для HTTP-запросов. По умолчанию `None`.

    Returns:
        tuple[str, str]: zerogpu_uuid и zerogpu_token.
    """
```

**Как работает**:
Функция `get_zerogpu_token` извлекает `zerogpu_token` и `zerogpu_uuid` из API Hugging Face Spaces. Она выполняет GET-запросы к страницам Hugging Face Spaces и анализирует HTML-код для извлечения необходимых значений. Функция также использует cookies для аутентификации и получения токена.

**Примеры**:
```python
# Пример вызова функции get_zerogpu_token
async def main():
    async with StreamSession() as session:
        uuid, token = await get_zerogpu_token(
            space="deepseek-ai/Janus-Pro-7B",
            session=session,
            conversation=JsonConversation(session_hash="123")
        )
        print(f"UUID: {uuid}, Token: {token}")

# asyncio.run(main())
```