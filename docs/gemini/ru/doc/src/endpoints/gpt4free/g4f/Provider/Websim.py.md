# Модуль Websim для g4f

## Обзор

Модуль `Websim` предоставляет асинхронный класс `Websim`, предназначенный для взаимодействия с API Websim AI. Он поддерживает как генерацию текста, так и генерацию изображений. Модуль использует `aiohttp` для выполнения асинхронных HTTP-запросов и реализует логику повторных попыток для обработки ошибок, связанных с ограничением скорости.

## Подробнее

Модуль определяет константы, такие как базовый URL, URL для входа (который не используется), конечные точки API для чата и генерации изображений. Он также определяет, что для работы не требуется аутентификация и не используется драйвер. В модуле реализована поддержка системных сообщений и истории сообщений.

## Классы

### `Websim`

**Описание**:
Класс `Websim` предоставляет методы для взаимодействия с Websim AI API. Он поддерживает как текстовые запросы (чат), так и запросы на генерацию изображений.

**Наследует**:

- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Добавляет поддержку выбора моделей.

**Атрибуты**:

- `url` (str): Базовый URL Websim AI.
- `login_url` (str | None): URL для входа (в данном случае `None`, так как аутентификация не требуется).
- `chat_api_endpoint` (str): URL для запросов к API чата.
- `image_api_endpoint` (str): URL для запросов к API генерации изображений.
- `working` (bool): Указывает, работает ли провайдер.
- `needs_auth` (bool): Указывает, требуется ли аутентификация.
- `use_nodriver` (bool): Указывает, используется ли драйвер.
- `supports_stream` (bool): Указывает, поддерживает ли потоковую передачу.
- `supports_system_message` (bool): Указывает, поддерживает ли системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию (`gemini-1.5-pro`).
- `default_image_model` (str): Модель для генерации изображений по умолчанию (`flux`).
- `image_models` (list[str]): Список поддерживаемых моделей для генерации изображений.
- `models` (list[str]): Список поддерживаемых моделей для чата и генерации изображений.

#### `generate_project_id`

```python
    @staticmethod
    def generate_project_id(for_image=False):
        """
        Generate a project ID in the appropriate format
        
        For chat: format like \'ke3_xh5gai3gjkmruomu\'
        For image: format like \'kx0m131_rzz66qb2xoy7\'
        """
```

**Назначение**:
Генерирует идентификатор проекта в нужном формате.

**Параметры**:
- `for_image` (bool): Указывает, генерируется ли идентификатор для запроса изображения.

**Возвращает**:
- `str`: Сгенерированный идентификатор проекта.

**Как работает функция**:
Функция генерирует идентификатор проекта на основе случайных символов. Если `for_image` имеет значение `True`, идентификатор генерируется в формате, подходящем для запросов изображений, в противном случае - в формате для запросов чата.

**Примеры**:

```python
project_id_chat = Websim.generate_project_id(for_image=False)
print(project_id_chat)  # Например: 'abc_123def456ghi789'

project_id_image = Websim.generate_project_id(for_image=True)
print(project_id_image) # Например: '123abcd_efg456789012'
```

#### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        prompt: str = None,
        proxy: str = None,
        aspect_ratio: str = "1:1",
        project_id: str = None,
        **kwargs
    ) -> AsyncResult:
```

**Назначение**:
Создает асинхронный генератор для выполнения запросов к API Websim AI.

**Параметры**:
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `prompt` (str, optional): Дополнительный промпт. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `aspect_ratio` (str, optional): Соотношение сторон изображения. По умолчанию `"1:1"`.
- `project_id` (str, optional): Идентификатор проекта. Если не указан, генерируется автоматически.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий результаты запроса.

**Как работает функция**:
Функция определяет, является ли запрос запросом изображения, и генерирует идентификатор проекта, если он не предоставлен. Затем она устанавливает заголовки для запроса и вызывает соответствующий обработчик (`_handle_image_request` или `_handle_chat_request`) в зависимости от типа запроса.

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello, Websim!"}]
async for result in Websim.create_async_generator(model='gemini-1.5-pro', messages=messages):
    print(result)

messages = [{"role": "user", "content": "A cat"}]
async for result in Websim.create_async_generator(model='flux', messages=messages, prompt="A cat", aspect_ratio="16:9"):
    print(result)
```

#### `_handle_image_request`

```python
    @classmethod
    async def _handle_image_request(
        cls,
        project_id: str,
        messages: Messages,
        prompt: str,
        aspect_ratio: str,
        headers: dict,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
```

**Назначение**:
Обрабатывает запрос на генерацию изображения.

**Параметры**:
- `project_id` (str): Идентификатор проекта.
- `messages` (Messages): Список сообщений.
- `prompt` (str): Промпт для генерации изображения.
- `aspect_ratio` (str): Соотношение сторон изображения.
- `headers` (dict): Заголовки запроса.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий URL изображения.

**Как работает функция**:
Функция формирует промпт для запроса изображения, используя функцию `format_image_prompt`, и отправляет POST-запрос к API генерации изображений. Она извлекает URL изображения из ответа и возвращает его в виде объекта `ImageResponse`.

**Примеры**:

```python
messages = [{"role": "user", "content": "A cat"}]
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'text/plain;charset=UTF-8',
    'origin': 'https://websim.ai',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'websim-flags;': ''
}
async for result in Websim._handle_image_request(
    project_id='test_image_project',
    messages=messages,
    prompt="A cat",
    aspect_ratio="1:1",
    headers=headers
):
    print(result)
```

#### `_handle_chat_request`

```python
    @classmethod
    async def _handle_chat_request(
        cls,
        project_id: str,
        messages: Messages,
        headers: dict,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
```

**Назначение**:
Обрабатывает запрос к API чата.

**Параметры**:
- `project_id` (str): Идентификатор проекта.
- `messages` (Messages): Список сообщений.
- `headers` (dict): Заголовки запроса.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответ чата.

**Как работает функция**:
Функция отправляет POST-запрос к API чата и возвращает ответ. Она включает логику повторных попыток для обработки ошибок, связанных с ограничением скорости (HTTP 429). Если ответ получен успешно, функция извлекает содержимое сообщения из JSON-ответа и возвращает его.

**Внутренние функции**:
В данной функции отсутствуют внутренние функции.

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello, Websim!"}]
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'text/plain;charset=UTF-8',
    'origin': 'https://websim.ai',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'websim-flags;': ''
}
async for result in Websim._handle_chat_request(
    project_id='test_chat_project',
    messages=messages,
    headers=headers
):
    print(result)
```