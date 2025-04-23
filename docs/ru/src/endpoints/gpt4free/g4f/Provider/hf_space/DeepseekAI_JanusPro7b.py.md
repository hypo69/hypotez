# Модуль DeepseekAI_JanusPro7b

## Обзор

Модуль `DeepseekAI_JanusPro7b` предоставляет асинхронный интерфейс для взаимодействия с моделью `Janus-Pro-7B` от Deepseek AI, размещенной на платформе Hugging Face Spaces. Он поддерживает как текстовые запросы, так и запросы, включающие изображения. Модуль использует асинхронные генераторы для обработки потоковых ответов от модели.

## Подробней

Модуль предназначен для интеграции с другими частями проекта `hypotez`, требующими взаимодействия с большими языковыми моделями (LLM) и моделями генерации изображений. Он предоставляет удобный способ отправки запросов к модели `Janus-Pro-7B` и получения результатов в асинхронном режиме.

## Классы

### `DeepseekAI_JanusPro7b`

**Описание**: Класс `DeepseekAI_JanusPro7b` является провайдером для модели `Janus-Pro-7B` от Deepseek AI. Он наследует функциональность от `AsyncGeneratorProvider` и `ProviderModelMixin`, предоставляя методы для отправки запросов к модели и обработки ответов.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями провайдеров.

**Атрибуты**:
- `label` (str): Метка провайдера (="DeepseekAI Janus-Pro-7B").
- `space` (str): Имя пространства на Hugging Face (="deepseek-ai/Janus-Pro-7B").
- `url` (str): URL страницы пространства на Hugging Face.
- `api_url` (str): Базовый URL для API.
- `referer` (str): Referer заголовок для HTTP-запросов.
- `working` (bool): Флаг, указывающий, что провайдер работает (True).
- `supports_stream` (bool): Флаг, указывающий, что провайдер поддерживает потоковую передачу (True).
- `supports_system_message` (bool): Флаг, указывающий, что провайдер поддерживает системные сообщения (True).
- `supports_message_history` (bool): Флаг, указывающий, что провайдер поддерживает историю сообщений (True).
- `default_model` (str): Модель, используемая по умолчанию для текстовых запросов (="janus-pro-7b").
- `default_image_model` (str): Модель, используемая по умолчанию для запросов изображений (="janus-pro-7b-image").
- `default_vision_model` (str): Модель, используемая по умолчанию для vision запросов (=default_model).
- `image_models` (List[str]): Список моделей, поддерживающих запросы изображений.
- `vision_models` (List[str]): Список моделей, поддерживающих vision запросы.
- `models` (List[str]): Список всех поддерживаемых моделей.

**Принцип работы**:

Класс использует HTTP-запросы к API Hugging Face Spaces для взаимодействия с моделью `Janus-Pro-7B`. Он поддерживает как текстовые, так и графические запросы, а также потоковую передачу ответов. Для аутентификации используются токены `zerogpu_token` и `zerogpu_uuid`, которые получаются динамически.

**Методы**:
- `run(method, session, prompt, conversation, image, seed)`: Выполняет HTTP-запрос к API.
- `create_async_generator(model, messages, media, prompt, proxy, cookies, api_key, zerogpu_uuid, return_conversation, conversation, seed, **kwargs)`: Создает асинхронный генератор для получения ответов от модели.

## Методы класса

### `run`

```python
    @classmethod
    def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, image: dict = None, seed: int = 0):
        """Выполняет HTTP-запрос к API Hugging Face Spaces.

        Args:
            method (str): HTTP-метод ("post", "image" или "get").
            session (StreamSession): Асинхровая HTTP-сессия.
            prompt (str): Текст запроса.
            conversation (JsonConversation): Объект, содержащий информацию о текущем диалоге.
            image (dict, optional): Данные изображения для запроса. По умолчанию `None`.
            seed (int): Зерно для генерации случайных чисел.

        Returns:
            StreamResponse: Объект ответа от HTTP-запроса.
        """
        ...
```

**Назначение**: Метод `run` выполняет HTTP-запрос к API Hugging Face Spaces в зависимости от переданных параметров.

**Параметры**:
- `method` (str): HTTP-метод, который будет использоваться для запроса. Допустимые значения: "post", "image" или "get".
- `session` (StreamSession): Асинхровая HTTP-сессия, используемая для выполнения запроса.
- `prompt` (str): Текст запроса, который будет отправлен модели.
- `conversation` (JsonConversation): Объект, содержащий информацию о текущем диалоге, такую как `session_hash`, `zerogpu_token` и `zerogpu_uuid`.
- `image` (dict, optional): Данные изображения для запроса. Если передано, запрос будет выполнен как запрос изображения. По умолчанию `None`.
- `seed` (int): Зерно для генерации случайных чисел, используемое для воспроизводимости результатов.

**Как работает функция**:
- Формирует заголовки запроса, включая `content-type`, `x-zerogpu-token`, `x-zerogpu-uuid` и `referer`.
- В зависимости от значения параметра `method`, выполняет `POST` или `GET` запрос к соответствующему API endpoint.
- Для `POST` запросов отправляет JSON-данные, содержащие `prompt`, `seed` и другие параметры.
- Для `image` запросов отправляет JSON-данные, специфичные для генерации изображений.
- Возвращает объект `StreamResponse`, представляющий ответ от HTTP-запроса.

**Примеры**:

```python
# Пример вызова метода run для выполнения POST-запроса
response = DeepseekAI_JanusPro7b.run(
    method="post",
    session=session,
    prompt="Hello, world!",
    conversation=conversation,
    seed=12345
)

# Пример вызова метода run для выполнения запроса изображения
response = DeepseekAI_JanusPro7b.run(
    method="image",
    session=session,
    prompt="Generate a cat image",
    conversation=conversation,
    seed=54321
)

# Пример вызова метода run для выполнения GET-запроса
response = DeepseekAI_JanusPro7b.run(
    method="get",
    session=session,
    prompt="Hello, world!",
    conversation=conversation,
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
        """Создает асинхронный генератор для получения ответов от модели.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений для отправки.
            media (MediaListType, optional): Список медиа-файлов для отправки. По умолчанию `None`.
            prompt (str, optional): Текст запроса. По умолчанию `None`.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            cookies (Cookies, optional): HTTP-куки. По умолчанию `None`.
            api_key (str, optional): API-ключ. По умолчанию `None`.
            zerogpu_uuid (str, optional): UUID для ZeroGPU. По умолчанию "[object Object]".
            return_conversation (bool, optional): Флаг, указывающий, следует ли возвращать объект диалога. По умолчанию `False`.
            conversation (JsonConversation, optional): Объект диалога. По умолчанию `None`.
            seed (int, optional): Зерно для генерации случайных чисел. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от модели.
        """
        ...
```

**Назначение**: Метод `create_async_generator` создает и возвращает асинхронный генератор, который позволяет получать ответы от модели `Janus-Pro-7B` асинхронно.

**Параметры**:
- `model` (str): Имя модели, которую следует использовать.
- `messages` (Messages): Список сообщений, представляющих контекст диалога.
- `media` (MediaListType, optional): Список медиа-файлов (например, изображений) для отправки вместе с запросом. По умолчанию `None`.
- `prompt` (str, optional): Текст запроса. Если не указан, формируется на основе `messages`. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера для использования при выполнении запроса. По умолчанию `None`.
- `cookies` (Cookies, optional): HTTP-куки для отправки с запросом. По умолчанию `None`.
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.
- `zerogpu_uuid` (str, optional): UUID для ZeroGPU. По умолчанию "[object Object]".
- `return_conversation` (bool, optional): Флаг, указывающий, следует ли возвращать объект диалога вместе с ответом. По умолчанию `False`.
- `conversation` (JsonConversation, optional): Объект диалога, содержащий историю сообщений и другие параметры. По умолчанию `None`.
- `seed` (int, optional): Зерно для генерации случайных чисел, используемое для воспроизводимости результатов. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, которые могут быть переданы в функцию.

**Как работает функция**:
- Определяет метод запроса (`"post"` или `"image"`) в зависимости от того, является ли запрос текстовым или включает изображения.
- Форматирует `prompt` на основе `messages`, если `prompt` не предоставлен явно.
- Генерирует случайное зерно (`seed`), если оно не указано.
- Создает или использует существующий объект `JsonConversation` для хранения информации о диалоге.
- Если `return_conversation` установлен в `True`, возвращает объект `conversation` в качестве первого элемента генератора.
- Выполняет загрузку медиа-файлов, если они предоставлены, и подготавливает их для отправки с запросом.
- Вызывает метод `run` для отправки запроса к API и получения ответа.
- Обрабатывает потоковый ответ от API, извлекая данные и возвращая их в виде объектов `Reasoning` и `ImageResponse`.

**Внутренние функции**:

Внутри `create_async_generator` вызывается асинхронная функция `get_zerogpu_token`, которая получает токены аутентификации (`zerogpu_uuid` и `api_key`).

**Примеры**:

```python
# Пример создания асинхронного генератора для текстового запроса
async_generator = DeepseekAI_JanusPro7b.create_async_generator(
    model="janus-pro-7b",
    messages=[{"role": "user", "content": "Hello, world!"}]
)

# Пример создания асинхронного генератора для запроса изображения
async_generator = DeepseekAI_JanusPro7b.create_async_generator(
    model="janus-pro-7b-image",
    messages=[{"role": "user", "content": "Generate a cat image"}]
)

# Пример использования асинхронного генератора
async for response in async_generator:
    if isinstance(response, Reasoning):
        print(f"Reasoning: {response.status}")
    elif isinstance(response, ImageResponse):
        print(f"Image URL: {response.images[0]}")
    else:
        print(f"Response: {response}")
```

## Функции

### `get_zerogpu_token`

```python
async def get_zerogpu_token(space: str, session: StreamSession, conversation: JsonConversation, cookies: Cookies = None):
    """Получает токены аутентификации (zerogpu_uuid и zerogpu_token) для Hugging Face Spaces.

    Args:
        space (str): Имя пространства на Hugging Face.
        session (StreamSession): Асинхровая HTTP-сессия.
        conversation (JsonConversation): Объект диалога.
        cookies (Cookies, optional): HTTP-куки. По умолчанию `None`.

    Returns:
        Tuple[str, str]: Кортеж, содержащий zerogpu_uuid и zerogpu_token.
    """
    ...
```

**Назначение**: Функция `get_zerogpu_token` получает токены аутентификации (`zerogpu_uuid` и `zerogpu_token`) для Hugging Face Spaces.

**Параметры**:
- `space` (str): Имя пространства на Hugging Face.
- `session` (StreamSession): Асинхровая HTTP-сессия.
- `conversation` (JsonConversation): Объект диалога.
- `cookies` (Cookies, optional): HTTP-куки. По умолчанию `None`.

**Как работает функция**:
- Получает `zerogpu_uuid` из объекта `conversation`, если он существует.
- Получает `zerogpu_token`, выполняя `GET` запросы к Hugging Face Spaces и API.
- Использует регулярные выражения для извлечения токенов из HTML-ответа.
- Обновляет `zerogpu_token`, выполняя `GET` запросы к API с использованием куки.
- Возвращает кортеж, содержащий `zerogpu_uuid` и `zerogpu_token`.

**Примеры**:

```python
# Пример вызова функции get_zerogpu_token
zerogpu_uuid, zerogpu_token = await get_zerogpu_token(
    space="deepseek-ai/Janus-Pro-7B",
    session=session,
    conversation=conversation
)

print(f"zerogpu_uuid: {zerogpu_uuid}")
print(f"zerogpu_token: {zerogpu_token}")