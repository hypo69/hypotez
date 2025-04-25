# Microsoft_Phi_4

## Обзор

Этот модуль предоставляет реализацию класса `Microsoft_Phi_4`, который представляет собой провайдера для работы с моделью `Microsoft Phi-4` через Hugging Face Spaces.

## Детали

### Класс `Microsoft_Phi_4`

```python
class Microsoft_Phi_4(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Класс провайдера для работы с моделью `Microsoft Phi-4` через Hugging Face Spaces.

    Inherits:
        AsyncGeneratorProvider: базовый класс асинхронных генераторов для провайдеров моделей.
        ProviderModelMixin: предоставляет методы для управления именами моделей и версиями.

    Attributes:
        label (str): метка провайдера ("Microsoft Phi-4").
        space (str): имя пространства Hugging Face Spaces ("microsoft/phi-4-multimodal").
        url (str): URL-адрес пространства Hugging Face Spaces.
        api_url (str): URL-адрес API-интерфейса.
        referer (str): URL-адрес для ссылки в запросах.
        working (bool): флаг, указывающий на работоспособность провайдера (True).
        supports_stream (bool): флаг, указывающий на поддержку потоковой передачи ответов (True).
        supports_system_message (bool): флаг, указывающий на поддержку системных сообщений (True).
        supports_message_history (bool): флаг, указывающий на поддержку истории сообщений (True).
        default_model (str): имя модели по умолчанию ("phi-4-multimodal").
        default_vision_model (str): имя модели по умолчанию для задач обработки изображений ("phi-4-multimodal").
        model_aliases (dict): словарь псевдонимов моделей.
        vision_models (list): список доступных моделей для задач обработки изображений.
        models (list): список доступных моделей.

    Methods:
        run(method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None):
            Отправляет запрос к API-интерфейсу модели для выполнения заданного метода (predict, post, get).
        create_async_generator(model: str, messages: Messages, media: MediaListType = None, prompt: str = None, proxy: str = None, cookies: Cookies = None, api_key: str = None, zerogpu_uuid: str = "[object Object]", return_conversation: bool = False, conversation: JsonConversation = None, **kwargs) -> AsyncResult:
            Создает асинхронный генератор для выполнения запросов к модели.
    """
    
    @classmethod
    def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None):
        """
        Отправляет запрос к API-интерфейсу модели для выполнения заданного метода (predict, post, get).

        Args:
            method (str): имя метода ("predict", "post", "get").
            session (StreamSession): объект сессии для выполнения запроса.
            prompt (str): текст запроса.
            conversation (JsonConversation): объект, содержащий информацию о сессии.
            media (list, optional): список медиафайлов для обработки. По умолчанию `None`.

        Returns:
            StreamResponse: объект ответа от API-интерфейса.

        Raises:
            ResponseError: если в ответе от API-интерфейса обнаружена ошибка.
        """

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
        """
        Создает асинхронный генератор для выполнения запросов к модели.

        Args:
            model (str): имя модели.
            messages (Messages): объект, содержащий историю сообщений.
            media (MediaListType, optional): список медиафайлов для обработки. По умолчанию `None`.
            prompt (str, optional): текст запроса. По умолчанию `None`.
            proxy (str, optional): адрес прокси-сервера. По умолчанию `None`.
            cookies (Cookies, optional): словарь cookie. По умолчанию `None`.
            api_key (str, optional): API-ключ. По умолчанию `None`.
            zerogpu_uuid (str, optional): UUID пользователя. По умолчанию `"[object Object]"`.
            return_conversation (bool, optional): флаг, указывающий на необходимость возврата объекта разговора. По умолчанию `False`.
            conversation (JsonConversation, optional): объект разговора. По умолчанию `None`.
            **kwargs: дополнительные аргументы.

        Returns:
            AsyncResult: асинхронный генератор, который возвращает ответы от модели.

        Raises:
            ResponseError: если в ответе от API-интерфейса обнаружена ошибка.
        """
```
### Методы класса
#### `run`
    ```python
    @classmethod
    def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None):
        """
        Отправляет запрос к API-интерфейсу модели для выполнения заданного метода (predict, post, get).

        Args:
            method (str): имя метода ("predict", "post", "get").
            session (StreamSession): объект сессии для выполнения запроса.
            prompt (str): текст запроса.
            conversation (JsonConversation): объект, содержащий информацию о сессии.
            media (list, optional): список медиафайлов для обработки. По умолчанию `None`.

        Returns:
            StreamResponse: объект ответа от API-интерфейса.

        Raises:
            ResponseError: если в ответе от API-интерфейса обнаружена ошибка.
        """
    ```
#### `create_async_generator`
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
        """
        Создает асинхронный генератор для выполнения запросов к модели.

        Args:
            model (str): имя модели.
            messages (Messages): объект, содержащий историю сообщений.
            media (MediaListType, optional): список медиафайлов для обработки. По умолчанию `None`.
            prompt (str, optional): текст запроса. По умолчанию `None`.
            proxy (str, optional): адрес прокси-сервера. По умолчанию `None`.
            cookies (Cookies, optional): словарь cookie. По умолчанию `None`.
            api_key (str, optional): API-ключ. По умолчанию `None`.
            zerogpu_uuid (str, optional): UUID пользователя. По умолчанию `"[object Object]"`.
            return_conversation (bool, optional): флаг, указывающий на необходимость возврата объекта разговора. По умолчанию `False`.
            conversation (JsonConversation, optional): объект разговора. По умолчанию `None`.
            **kwargs: дополнительные аргументы.

        Returns:
            AsyncResult: асинхронный генератор, который возвращает ответы от модели.

        Raises:
            ResponseError: если в ответе от API-интерфейса обнаружена ошибка.
        """
    ```


## Примеры использования

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Microsoft_Phi_4 import Microsoft_Phi_4
from hypotez.src.endpoints.gpt4free.g4f.helper import format_prompt
from hypotez.src.endpoints.gpt4free.g4f.Provider.response import JsonConversation
from hypotez.src.requests.aiohttp import StreamSession

# Создание объекта разговора
conversation = JsonConversation(session_hash="your_session_hash", zerogpu_token="your_api_key", zerogpu_uuid="your_uuid")

# Создание объекта сессии
session = StreamSession(proxy="your_proxy")

# Запрос к модели
async def run_model():
    provider = Microsoft_Phi_4
    prompt = "Привет, как дела?"

    # Выполнение запроса с использованием метода "predict"
    response = await provider.run(
        method="predict",
        session=session,
        prompt=prompt,
        conversation=conversation,
    )

    # Получение ответа
    response_text = response.text

    # Вывод ответа
    print(response_text)

# Запуск асинхронной функции
asyncio.run(run_model())
```

## Пример работы с медиафайлами:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Microsoft_Phi_4 import Microsoft_Phi_4
from hypotez.src.endpoints.gpt4free.g4f.helper import format_prompt
from hypotez.src.endpoints.gpt4free.g4f.Provider.response import JsonConversation
from hypotez.src.requests.aiohttp import StreamSession
from hypotez.src.image import to_bytes

# Создание объекта разговора
conversation = JsonConversation(session_hash="your_session_hash", zerogpu_token="your_api_key", zerogpu_uuid="your_uuid")

# Создание объекта сессии
session = StreamSession(proxy="your_proxy")

# Запрос к модели
async def run_model():
    provider = Microsoft_Phi_4
    prompt = "Опиши это изображение"
    image_path = "path/to/your/image.jpg"

    # Загрузка изображения
    image_bytes = to_bytes(image_path)

    # Выполнение запроса с использованием метода "predict"
    response = await provider.run(
        method="predict",
        session=session,
        prompt=prompt,
        conversation=conversation,
        media=[(image_bytes, "image.jpg")],
    )

    # Получение ответа
    response_text = response.text

    # Вывод ответа
    print(response_text)

# Запуск асинхронной функции
asyncio.run(run_model())
```


```python
                from __future__ import annotations
```
- **Описание**: Данная строка импортирует функции из модуля `__future__`, что позволяет использовать функции из будущих версий Python.
- **Пример**:  `from __future__ import annotations` позволяет использовать синтаксис аннотаций типов, который доступен только в Python 3.7 и выше.


```python
import json
import uuid
```
- **Описание**: Импорт модулей `json` и `uuid` для работы с JSON-данными и генерации UUID.
- **Пример**:
    - `json` используется для сериализации и десериализации JSON-данных.
    - `uuid` используется для генерации уникальных идентификаторов.


```python
from ...typing import AsyncResult, Messages, Cookies, MediaListType
```
- **Описание**: Импорт типов данных `AsyncResult`, `Messages`, `Cookies`, `MediaListType` из модуля `typing` в текущем проекте.
- **Пример**:
    - `AsyncResult` используется для представления асинхронного результата.
    - `Messages` используется для представления истории сообщений.
    - `Cookies` используется для представления словаря cookie.
    - `MediaListType` используется для представления списка медиафайлов.


```python
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
```
- **Описание**: Импорт классов `AsyncGeneratorProvider` и `ProviderModelMixin` из модуля `base_provider` в родительском пакете.
- **Пример**:
    - `AsyncGeneratorProvider` - базовый класс для провайдеров моделей, которые поддерживают асинхронные генераторы.
    - `ProviderModelMixin` - базовый класс для провайдеров моделей, который предоставляет методы для управления именами моделей и версиями.


```python
from ..helper import format_prompt, format_image_prompt
```
- **Описание**: Импорт функций `format_prompt` и `format_image_prompt` из модуля `helper` в родительском пакете.
- **Пример**:
    - `format_prompt` - функция для форматирования текста запроса.
    - `format_image_prompt` - функция для форматирования текста запроса, который содержит информацию об изображении.


```python
from ...providers.response import JsonConversation
```
- **Описание**: Импорт класса `JsonConversation` из модуля `response` в пакете `providers`.
- **Пример**:
    - `JsonConversation` - класс для представления информации о сессии разговора в формате JSON.


```python
from ...requests.aiohttp import StreamSession, StreamResponse, FormData
```
- **Описание**: Импорт классов `StreamSession`, `StreamResponse`, `FormData` из модуля `aiohttp` в пакете `requests`.
- **Пример**:
    - `StreamSession` - класс для создания сессии HTTP-запросов, который поддерживает потоковую передачу данных.
    - `StreamResponse` - класс для представления ответа от HTTP-запроса, который поддерживает потоковую передачу данных.
    - `FormData` - класс для представления данных в формате multipart/form-data.


```python
from ...requests.raise_for_status import raise_for_status
```
- **Описание**: Импорт функции `raise_for_status` из модуля `raise_for_status` в пакете `requests`.
- **Пример**:
    - `raise_for_status` - функция для проверки статуса ответа от HTTP-запроса и поднятия исключения в случае ошибки.


```python
from ...image import to_bytes, is_accepted_format, is_data_an_audio
```
- **Описание**: Импорт функций `to_bytes`, `is_accepted_format`, `is_data_an_audio` из модуля `image`.
- **Пример**:
    - `to_bytes` - функция для преобразования данных в байтовый поток.
    - `is_accepted_format` - функция для проверки формата медиафайла.
    - `is_data_an_audio` - функция для проверки того, является ли медиафайл аудиофайлом.


```python
from ...errors import ResponseError
```
- **Описание**: Импорт класса `ResponseError` из модуля `errors`.
- **Пример**:
    - `ResponseError` - класс для представления ошибки, полученной от API-интерфейса.


```python
from ... import debug
```
- **Описание**: Импорт модуля `debug` для отладки.
- **Пример**:
    - `debug` - модуль для вывода отладочной информации.


```python
from .DeepseekAI_JanusPro7b import get_zerogpu_token
```
- **Описание**: Импорт функции `get_zerogpu_token` из модуля `DeepseekAI_JanusPro7b` в текущем пакете.
- **Пример**:
    - `get_zerogpu_token` - функция для получения токена ZeroGPU.


```python
from .raise_for_status import raise_for_status
```
- **Описание**: Импорт функции `raise_for_status` из модуля `raise_for_status` в текущем пакете.
- **Пример**:
    - `raise_for_status` - функция для проверки статуса ответа от HTTP-запроса и поднятия исключения в случае ошибки.


```python
class Microsoft_Phi_4(AsyncGeneratorProvider, ProviderModelMixin):
    label = "Microsoft Phi-4"
    space = "microsoft/phi-4-multimodal"
    url = f"https://huggingface.co/spaces/{space}"
    api_url = "https://microsoft-phi-4-multimodal.hf.space"
    referer = f"{api_url}?__theme=light"

    working = True
    supports_stream = True
    supports_system_message = True
    supports_message_history = True

    default_model = "phi-4-multimodal"
    default_vision_model = default_model
    model_aliases = {"phi-4": default_vision_model}
    vision_models = list(model_aliases.keys())
    models = vision_models

    @classmethod
    def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None):
            headers = {
                "content-type": "application/json",
                "x-zerogpu-token": conversation.zerogpu_token,
                "x-zerogpu-uuid": conversation.zerogpu_uuid,
                "referer": cls.referer,
            }
            if method == "predict":
                return session.post(f"{cls.api_url}/gradio_api/run/predict", **{
                    "headers": {k: v for k, v in headers.items() if v is not None},
                    "json": {
                        "data":[\n
                            [],\n
                            {\n
                                "text": prompt,\n
                                "files": media,\n
                            },\n
                            None\n
                        ],\n
                        "event_data": None,\n
                        "fn_index": 10,\n
                        "trigger_id": 8,\n
                        "session_hash": conversation.session_hash\n
                    },\n
                })\n
            if method == "post":
                return session.post(f"{cls.api_url}/gradio_api/queue/join?__theme=light", **{
                    "headers": {k: v for k, v in headers.items() if v is not None},
                    "json": {
                        "data": [[\n
                                {\n
                                "role": "user",\n
                                "content": prompt,\n
                                }\n
                            ]] + [[\n
                                {\n
                                    "role": "user",\n
                                    "content": {"file": image}\n
                                } for image in media\n
                            ]],\n
                        "event_data": None,\n
                        "fn_index": 11,\n
                        "trigger_id": 8,\n
                        "session_hash": conversation.session_hash\n
                    },\n
                })\n
            return session.get(f"{cls.api_url}/gradio_api/queue/data?session_hash={conversation.session_hash}", **{
                "headers": {
                    "accept": "text/event-stream",
                    "content-type": "application/json",
                    "referer": cls.referer,
                }\n
            })\n
```
- **Описание**: Класс `Microsoft_Phi_4` - провайдер для работы с моделью Microsoft Phi-4 через Hugging Face Spaces. Наследуется от классов `AsyncGeneratorProvider` и `ProviderModelMixin`.

    - **Атрибуты**:
        - `label`: метка провайдера ("Microsoft Phi-4").
        - `space`: имя пространства Hugging Face Spaces ("microsoft/phi-4-multimodal").
        - `url`: URL-адрес пространства Hugging Face Spaces.
        - `api_url`: URL-адрес API-интерфейса.
        - `referer`: URL-адрес для ссылки в запросах.
        - `working`: флаг, указывающий на работоспособность провайдера (True).
        - `supports_stream`: флаг, указывающий на поддержку потоковой передачи ответов (True).
        - `supports_system_message`: флаг, указывающий на поддержку системных сообщений (True).
        - `supports_message_history`: флаг, указывающий на поддержку истории сообщений (True).
        - `default_model`: имя модели по умолчанию ("phi-4-multimodal").
        - `default_vision_model`: имя модели по умолчанию для задач обработки изображений ("phi-4-multimodal").
        - `model_aliases`: словарь псевдонимов моделей.
        - `vision_models`: список доступных моделей для задач обработки изображений.
        - `models`: список доступных моделей.

    - **Методы**:
        - `run`: отправляет запрос к API-интерфейсу модели для выполнения заданного метода (predict, post, get).
        - `create_async_generator`: создает асинхронный генератор для выполнения запросов к модели.


```python
    @classmethod
    def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None):
            headers = {
                "content-type": "application/json",
                "x-zerogpu-token": conversation.zerogpu_token,
                "x-zerogpu-uuid": conversation.zerogpu_uuid,
                "referer": cls.referer,
            }
            if method == "predict":
                return session.post(f"{cls.api_url}/gradio_api/run/predict", **{
                    "headers": {k: v for k, v in headers.items() if v is not None},
                    "json": {
                        "data":[\n
                            [],\n
                            {\n
                                "text": prompt,\n
                                "files": media,\n
                            },\n
                            None\n
                        ],\n
                        "event_data": None,\n
                        "fn_index": 10,\n
                        "trigger_id": 8,\n
                        "session_hash": conversation.session_hash\n
                    },\n
                })\n
            if method == "post":
                return session.post(f"{cls.api_url}/gradio_api/queue/join?__theme=light", **{
                    "headers": {k: v for k, v in headers.items() if v is not None},
                    "json": {
                        "data": [[\n
                                {\n
                                "role": "user",\n
                                "content": prompt,\n
                                }\n
                            ]] + [[\n
                                {\n
                                    "role": "user",\n
                                    "content": {"file": image}\n
                                } for image in media\n
                            ]],\n
                        "event_data": None,\n
                        "fn_index": 11,\n
                        "trigger_id": 8,\n
                        "session_hash": conversation.session_hash\n
                    },\n
                })\n
            return session.get(f"{cls.api_url}/gradio_api/queue/data?session_hash={conversation.session_hash}", **{
                "headers": {
                    "accept": "text/event-stream",
                    "content-type": "application/json",
                    "referer": cls.referer,
                }\n
            })\n
```
- **Описание**: Класс-метод `run` отправляет запрос к API-интерфейсу модели для выполнения заданного метода (predict, post, get). 
    - **Параметры**:
        - `method`: имя метода ("predict", "post", "get").
        - `session`: объект сессии для выполнения запроса.
        - `prompt`: текст запроса.
        - `conversation`: объект, содержащий информацию о сессии.
        - `media`: список медиафайлов для обработки (опциональный).
    - **Возвращаемое значение**:
        - `StreamResponse`: объект ответа от API-интерфейса.
    - **Исключения**:
        - `ResponseError`: если в ответе от API-интерфейса обнаружена ошибка.


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
        prompt = format_prompt(messages) if prompt is None and conversation is None else prompt
        prompt = format_image_prompt(messages, prompt)

        session_hash = uuid.uuid4().hex if conversation is None else getattr(conversation, "session_hash", uuid.uuid4().hex)
        async with StreamSession(proxy=proxy, impersonate="chrome") as session:
            if api_key is None:
                zerogpu_uuid, api_key = await get_zerogpu_token(cls.space, session, conversation, cookies)
            if conversation is None or not hasattr(conversation, "session_hash"):
                conversation = JsonConversation(session_hash=session_hash, zerogpu_token=api_key, zerogpu_uuid=zerogpu_uuid)
            else:
                conversation.zerogpu_token = api_key
            if return_conversation:
                yield conversation

            if media is not None:
                data = FormData()
                mime_types = [None for i in range(len(media))]
                for i in range(len(media)):
                    mime_types[i] = is_data_an_audio(media[i][0], media[i][1])
                    media[i] = (to_bytes(media[i][0]), media[i][1])
                    mime_types[i] = is_accepted_format(media[i][0]) if mime_types[i] is None else mime_types[i]
                for image, image_name in media:
                    data.add_field(f"files", to_bytes(image), filename=image_name)
                async with session.post(f"{cls.api_url}/gradio_api/upload", params={"upload_id": session_hash}, data=data) as response:
                    await raise_for_status(response)
                    image_files = await response.json()
                media = [{\n
                    "path": image_file,\n
                    "url": f"{cls.api_url}/gradio_api/file={image_file}",\n
                    "orig_name": media[i][1],\n
                    "size": len(media[i][0]),\n
                    "mime_type": mime_types[i],\n
                    "meta": {\n
                        "_type": "gradio.FileData"\n
                    }\n
                } for i, image_file in enumerate(image_files)]
            \n            \n            async with cls.run("predict", session, prompt, conversation, media) as response:
                await raise_for_status(response)

            async with cls.run("post", session, prompt, conversation, media) as response:
                await raise_for_status(response)

            async with cls.run("get", session, prompt, conversation) as response:
                response: StreamResponse = response
                async for line in response.iter_lines():
                    if line.startswith(b\'data: \'):
                        try:
                            json_data = json.loads(line[6:])
                            if json_data.get(\'msg\') == \'process_completed\':
                                if \'output\' in json_data and \'error\' in json_data[\'output\']:\n                                    raise ResponseError(json_data[\'output\'][\'error\'])\n                                if \'output\' in json_data and \'data\' in json_data[\'output\']:\n                                    yield json_data[\'output\'][\'data\'][0][-1]["content"]\n                                break

                        except json.JSONDecodeError:\n                            debug.log("Could not parse JSON:", line.decode(errors="replace"))
```
- **Описание**: Класс-метод `create_async_generator` создает асинхронный генератор для выполнения запросов к модели.
    - **Параметры**:
        - `model`: имя модели.
        - `messages`: объект, содержащий историю сообщений.
        - `media`: список медиафайлов для обработки (опциональный).
        - `prompt`: текст запроса (опциональный).
        - `proxy`: адрес прокси-сервера (опциональный).
        - `cookies`: словарь cookie (опциональный).
        - `api_key`: API-ключ (опциональный).
        - `zerogpu_uuid`: UUID пользователя (опциональный).
        - `return_conversation`: флаг, указывающий на необходимость возврата объекта разговора (опциональный).
        - `conversation`: объект разговора (опциональный).
        - `**kwargs`: дополнительные аргументы.
    - **Возвращаемое значение**:
        - `AsyncResult`: асинхронный генератор, который возвращает ответы от модели.
    - **Исключения**:
        - `ResponseError`: если в ответе от API-интерфейса обнаружена ошибка.

## Примеры использования

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Microsoft_Phi_4 import Microsoft_Phi_4
from hypotez.src.endpoints.gpt4free.g4f.helper import format_prompt
from hypotez.src.endpoints.gpt4free.g4f.Provider.response import JsonConversation
from hypotez.src.requests.aiohttp import StreamSession

# Создание объекта разговора
conversation = JsonConversation(session_hash="your_session_hash", zerogpu_token="your_api_key", zerogpu_uuid="your_uuid")

# Создание объекта сессии
session = StreamSession(proxy="your_proxy")

# Запрос к модели
async def run_model():
    provider = Microsoft_Phi_4
    prompt = "Привет, как дела?"

    # Выполнение запроса с использованием метода "predict"
    response = await provider.run(
        method="predict",
        session=session,
        prompt=prompt,
        conversation=conversation,
    )

    # Получение ответа
    response_text = response.text

    # Вывод ответа
    print(response_text)

# Запуск асинхронной функции
asyncio.run(run_model())
```

## Пример работы с медиафайлами:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Microsoft_Phi_4 import Microsoft_Phi_4
from hypotez.src.endpoints.gpt4free.g4f.helper import format_prompt
from hypotez.src.endpoints.gpt4free.g4f.Provider.response import JsonConversation
from hypotez.src.requests.aiohttp import StreamSession
from hypotez.src.image import to_bytes

# Создание объекта разговора
conversation = JsonConversation(session_hash="your_session_hash", zerogpu_token="your_api_key", zerogpu_uuid="your_uuid")

# Создание объекта сессии
session = StreamSession(proxy="your_proxy")

# Запрос к модели
async def run_model():
    provider = Microsoft_Phi_4
    prompt = "Опиши это изображение"
    image_path = "path/to/your/image.jpg"

    # Загрузка изображения
    image_bytes = to_bytes(image_path)

    # Выполнение запроса с использованием метода "predict"
    response = await provider.run(
        method="predict",
        session=session,
        prompt=prompt,
        conversation=conversation,
        media=[(image_bytes, "image.jpg")],
    )

    # Получение ответа
    response_text = response.text

    # Вывод ответа
    print(response_text)

# Запуск асинхронной функции
asyncio.run(run_model())