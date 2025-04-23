# Модуль `Websim`

## Обзор

Модуль `Websim` предоставляет асинхронтный интерфейс для взаимодействия с API Websim AI, позволяя генерировать текст и изображения. Он поддерживает как текстовые запросы, так и запросы на генерацию изображений, используя различные модели, предоставляемые Websim AI.

## Детали

Модуль предназначен для использования в асинхронных приложениях и предоставляет методы для генерации идентификаторов проектов, обработки запросов к API Websim AI и возврата результатов в виде асинхронного генератора.

## Классы

### `Websim`

**Описание**: Класс `Websim` является асинхронным провайдером и миксином моделей, предназначенным для взаимодействия с API Websim AI.

**Наследуется от**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию результатов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL Websim AI.
- `login_url` (None): URL для входа (не используется).
- `chat_api_endpoint` (str): URL API для генерации текста.
- `image_api_endpoint` (str): URL API для генерации изображений.
- `working` (bool): Указывает, что провайдер работает.
- `needs_auth` (bool): Указывает, требуется ли аутентификация (не требуется).
- `use_nodriver` (bool): Указывает, использовать ли драйвер (не используется).
- `supports_stream` (bool): Указывает, поддерживает ли потоковую передачу (не поддерживает).
- `supports_system_message` (bool): Указывает, поддерживает ли системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию для генерации текста (`gemini-1.5-pro`).
- `default_image_model` (str): Модель, используемая по умолчанию для генерации изображений (`flux`).
- `image_models` (list[str]): Список поддерживаемых моделей для генерации изображений.
- `models` (list[str]): Список всех поддерживаемых моделей (текстовых и графических).

**Принцип работы**:
Класс `Websim` использует API Websim AI для генерации текста и изображений. Он предоставляет методы для создания идентификаторов проектов, обработки запросов к API и возврата результатов в виде асинхронного генератора.

**Методы**:

- `generate_project_id(for_image: bool = False) -> str`
- `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, aspect_ratio: str = "1:1", project_id: str = None, **kwargs) -> AsyncResult`
- `_handle_image_request(project_id: str, messages: Messages, prompt: str, aspect_ratio: str, headers: dict, proxy: str = None, **kwargs) -> AsyncResult`
- `_handle_chat_request(project_id: str, messages: Messages, headers: dict, proxy: str = None, **kwargs) -> AsyncResult`

## Методы класса

### `generate_project_id`

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
Генерирует идентификатор проекта в соответствующем формате.

**Параметры**:
- `for_image` (bool, optional): Указывает, генерируется ли идентификатор для запроса изображения. По умолчанию `False`.

**Возвращает**:
- `str`: Сгенерированный идентификатор проекта.

**Как работает функция**:
- В зависимости от значения `for_image` генерирует идентификатор проекта в формате, требуемом для запросов чата или изображений.
- Для чата идентификатор имеет формат `xxx_xxxxxxxxxxxxxxx`, где `x` - случайный символ из букв нижнего регистра и цифр.
- Для изображений идентификатор имеет формат `xxxxxxx_xxxxxxxxxxxx`, где `x` - случайный символ из букв нижнего регистра и цифр.

**Примеры**:
```python
project_id_chat = Websim.generate_project_id()
project_id_image = Websim.generate_project_id(for_image=True)
print(f"Идентификатор проекта для чата: {project_id_chat}")
print(f"Идентификатор проекта для изображения: {project_id_image}")
```

### `create_async_generator`

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
        """
        """
```

**Назначение**:
Создает асинхронный генератор для обработки запросов к API Websim AI.

**Параметры**:
- `model` (str): Модель, используемая для генерации.
- `messages` (Messages): Список сообщений для запроса.
- `prompt` (str, optional): Дополнительный текст для запроса. По умолчанию `None`.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `aspect_ratio` (str, optional): Соотношение сторон изображения. По умолчанию `"1:1"`.
- `project_id` (str, optional): Идентификатор проекта. Если `None`, генерируется новый.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор результатов.

**Как работает функция**:
- Определяет, является ли запрос запросом изображения на основе модели.
- Генерирует идентификатор проекта, если он не предоставлен.
- Устанавливает заголовки для запроса.
- Вызывает `_handle_image_request` для запросов изображений или `_handle_chat_request` для текстовых запросов.
- Возвращает асинхронный генератор, предоставляющий результаты.

**Примеры**:
```python
messages = [{"role": "user", "content": "Generate a cat image"}]
async for result in Websim.create_async_generator(model='flux', messages=messages):
    print(result)
```

### `_handle_image_request`

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
        """
        """
```

**Назначение**:
Обрабатывает запросы на генерацию изображений.

**Параметры**:
- `project_id` (str): Идентификатор проекта.
- `messages` (Messages): Список сообщений для запроса.
- `prompt` (str): Текст для запроса.
- `aspect_ratio` (str): Соотношение сторон изображения.
- `headers` (dict): Заголовки для запроса.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор результатов.

**Как работает функция**:
- Форматирует запрос изображения с использованием `format_image_prompt`.
- Отправляет POST-запрос к `image_api_endpoint` с идентификатором проекта, текстом запроса и соотношением сторон.
- Извлекает URL изображения из ответа JSON и возвращает `ImageResponse`.

**Примеры**:
```python
messages = [{"role": "user", "content": "Generate a cat image"}]
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'text/plain;charset=UTF-8',
    'origin': 'https://websim.ai',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'websim-flags;': ''
}
async for result in Websim._handle_image_request(project_id='test_id', messages=messages, prompt='cat', aspect_ratio='1:1', headers=headers):
    print(result)
```

### `_handle_chat_request`

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
        """
        """
```

**Назначение**:
Обрабатывает запросы на генерацию текста.

**Параметры**:
- `project_id` (str): Идентификатор проекта.
- `messages` (Messages): Список сообщений для запроса.
- `headers` (dict): Заголовки для запроса.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор результатов.

**Как работает функция**:
- Отправляет POST-запрос к `chat_api_endpoint` с идентификатором проекта и списком сообщений.
- Обрабатывает ошибки статуса ответа, такие как `429` (превышение лимита запросов), и выполняет повторные попытки.
- Извлекает содержимое из ответа JSON и возвращает его.

**Примеры**:
```python
messages = [{"role": "user", "content": "Hello, how are you?"}]
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'text/plain;charset=UTF-8',
    'origin': 'https://websim.ai',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'websim-flags;': ''
}
async for result in Websim._handle_chat_request(project_id='test_id', messages=messages, headers=headers):
    print(result)