# Модуль `Microsoft_Phi_4`

## Обзор

Модуль `Microsoft_Phi_4` предназначен для взаимодействия с мультимодальной моделью Microsoft Phi-4 через Hugging Face Space. Он предоставляет асинхронный генератор для получения ответов от модели, поддерживает потоковую передачу данных и работу с изображениями.

## Подробней

Этот модуль позволяет отправлять текстовые запросы и изображения в модель Microsoft Phi-4 и получать ответы в потоковом режиме. Он использует API Hugging Face Spaces для взаимодействия с моделью и поддерживает как текстовые, так и мультимодальные запросы.

## Классы

### `Microsoft_Phi_4`

**Описание**: Класс `Microsoft_Phi_4` предоставляет методы для взаимодействия с мультимодальной моделью Microsoft Phi-4 через Hugging Face Space.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями провайдеров.

**Атрибуты**:
- `label` (str): Метка провайдера, `"Microsoft Phi-4"`.
- `space` (str): Hugging Face Space, `"microsoft/phi-4-multimodal"`.
- `url` (str): URL Hugging Face Space.
- `api_url` (str): URL API Hugging Face Space.
- `referer` (str): Referer для HTTP-запросов.
- `working` (bool): Флаг, указывающий на работоспособность провайдера, `True`.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных, `True`.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений, `True`.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений, `True`.
- `default_model` (str): Модель по умолчанию, `"phi-4-multimodal"`.
- `default_vision_model` (str): Модель для работы с изображениями по умолчанию, `"phi-4-multimodal"`.
- `model_aliases` (dict): Псевдонимы моделей, `{"phi-4": default_vision_model}`.
- `vision_models` (list): Список моделей для работы с изображениями.
- `models` (list): Список поддерживаемых моделей.

**Методы**:
- `run()`: Выполняет HTTP-запрос к API Hugging Face Space.
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от модели.

## Функции

### `run`

```python
    @classmethod
    def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None):
        ...
```

**Назначение**: Выполняет HTTP-запрос к API Hugging Face Space для взаимодействия с моделью Microsoft Phi-4.

**Параметры**:
- `cls` (Microsoft_Phi_4): Ссылка на класс `Microsoft_Phi_4`.
- `method` (str): HTTP-метод (`"predict"`, `"post"` или `"get"`).
- `session` (StreamSession): Асинхровая сессия для выполнения HTTP-запросов.
- `prompt` (str): Текстовый запрос.
- `conversation` (JsonConversation): Объект, содержащий информацию о текущем диалоге.
- `media` (list, optional): Список медиафайлов (изображений), которые нужно отправить. По умолчанию `None`.

**Возвращает**:
- `StreamResponse`: Асинхронный ответ от сервера.

**Как работает функция**:

1. **Определение заголовков**: Определяются заголовки запроса, включая `content-type`, `x-zerogpu-token`, `x-zerogpu-uuid` и `referer`.
2. **Выбор метода**: В зависимости от значения параметра `method` выбирается соответствующий HTTP-метод и формируется тело запроса.
3. **Выполнение запроса**: Выполняется HTTP-запрос с использованием переданной сессии и возвращается ответ.

```
     Определение заголовков
     ↓
     Выбор метода ("predict", "post", "get")
     ↓
     Формирование тела запроса
     ↓
     Выполнение HTTP-запроса
```

**Примеры**:
```python
# Пример вызова метода run
import asyncio
from aiohttp import ClientSession
from src.providers.response import JsonConversation

async def test_run():
    async with ClientSession() as session:
        conversation = JsonConversation(session_hash="test_session")
        response = await Microsoft_Phi_4.run("get", session, "test prompt", conversation)
        print(response)

if __name__ == "__main__":
    asyncio.run(test_run())
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
        **kwargs
    ) -> AsyncResult:
        ...
```

**Назначение**: Создает асинхронный генератор для получения ответов от модели Microsoft Phi-4.

**Параметры**:
- `cls` (Microsoft_Phi_4): Ссылка на класс `Microsoft_Phi_4`.
- `model` (str): Название модели.
- `messages` (Messages): Список сообщений для отправки в модель.
- `media` (MediaListType, optional): Список медиафайлов (изображений), которые нужно отправить. По умолчанию `None`.
- `prompt` (str, optional): Текстовый запрос. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `cookies` (Cookies, optional): Cookies для отправки с запросом. По умолчанию `None`.
- `api_key` (str, optional): API-ключ для доступа к модели. По умолчанию `None`.
- `zerogpu_uuid` (str, optional): UUID для zerogpu. По умолчанию `"[object Object]"`.
- `return_conversation` (bool, optional): Флаг, указывающий, нужно ли возвращать объект диалога. По умолчанию `False`.
- `conversation` (JsonConversation, optional): Объект, содержащий информацию о текущем диалоге. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от модели.

**Как работает функция**:

1. **Форматирование запроса**: Форматируется текстовый запрос и запрос изображения, если они предоставлены.
2. **Создание сессии**: Создается асинхровая сессия для выполнения HTTP-запросов.
3. **Получение токена**: Если API-ключ не предоставлен, он получается с использованием функции `get_zerogpu_token`.
4. **Создание объекта диалога**: Создается объект диалога `JsonConversation`, если он не был передан.
5. **Загрузка медиафайлов**: Если предоставлены медиафайлы, они загружаются на сервер.
6. **Выполнение запросов**: Выполняются HTTP-запросы к API Hugging Face Space для получения ответов от модели.
7. **Обработка ответов**: Ответы от модели обрабатываются и возвращаются через асинхронный генератор.

```
     Форматирование запроса
     ↓
     Создание асинхронной сессии
     ↓
     Получение токена (если отсутствует)
     ↓
     Создание объекта диалога
     ↓
     Загрузка медиафайлов (если предоставлены)
     ↓
     Выполнение HTTP-запросов ("predict", "post", "get")
     ↓
     Обработка ответов и возврат через генератор
```

**Примеры**:
```python
# Пример вызова метода create_async_generator
import asyncio
from typing import AsyncGenerator
from src.typing import Messages
from src.providers.response import JsonConversation

async def test_create_async_generator():
    messages: Messages = [{"role": "user", "content": "test message"}]
    async for response in Microsoft_Phi_4.create_async_generator(model="phi-4-multimodal", messages=messages):
        print(response)

if __name__ == "__main__":
    asyncio.run(test_create_async_generator())