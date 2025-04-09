# Модуль для взаимодействия с AllenAI Playground
## Обзор

Модуль `AllenAI` предоставляет асинхронный генератор для взаимодействия с AllenAI Playground. Он позволяет использовать различные модели, такие как `tulu3-405b`, `OLMo-2-1124-13B-Instruct`, `tulu-3-1-8b`, `Llama-3-1-Tulu-3-70B` и `olmoe-0125`, для генерации текста на основе заданных сообщений. Модуль поддерживает стриминг ответов, использование прокси и настройку температуры и вероятности (`top_p`).
## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с AllenAI Playground для генерации текста. Он использует асинхронные запросы для взаимодействия с API AllenAI и предоставляет возможность стриминга ответов. Расположение файла в проекте указывает на его роль как одного из провайдеров для генерации текста.
## Классы
### `Conversation`
**Описание**:
Класс `Conversation` представляет собой структуру данных для хранения истории разговора с AI-моделью. Он наследуется от класса `JsonConversation` и содержит информацию о сообщениях, идентификаторе пользователя и модели, используемой в разговоре.

**Наследует**:
`JsonConversation`

**Аттрибуты**:
- `parent` (str, optional): Идентификатор родительского сообщения в контексте разговора. По умолчанию `None`.
- `x_anonymous_user_id` (str, optional): Анонимный идентификатор пользователя. Генерируется случайным образом, если не задан.
- `model` (str): Модель, используемая в разговоре.
- `messages` (List[dict]): Список сообщений в разговоре, где каждое сообщение представлено в виде словаря с ключами "role" и "content".

### `AllenAI`
**Описание**:
Класс `AllenAI` является асинхронным провайдером для взаимодействия с AllenAI Playground. Он предоставляет методы для создания асинхронного генератора, который отправляет запросы к API AllenAI и возвращает сгенерированный текст.

**Наследует**:
`AsyncGeneratorProvider`, `ProviderModelMixin`

**Аттрибуты**:
- `label` (str): Метка провайдера ("Ai2 Playground").
- `url` (str): URL AllenAI Playground ("https://playground.allenai.org").
- `login_url` (str): URL для логина (в данном случае `None`, так как аутентификация не требуется).
- `api_endpoint` (str): URL API AllenAI ("https://olmo-api.allen.ai/v4/message/stream").
- `working` (bool): Указывает, работает ли провайдер (в данном случае `True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (в данном случае `False`).
- `use_nodriver` (bool): Указывает, используется ли драйвер (в данном случае `False`).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер стриминг ответов (в данном случае `True`).
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения (в данном случае `False`).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (в данном случае `True`).
- `default_model` (str): Модель, используемая по умолчанию (`tulu3-405b`).
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с API AllenAI.
## Функции
### `create_async_generator`
```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        host: str = "inferd",
        private: bool = True,
        top_p: float = None,
        temperature: float = None,
        conversation: Conversation = None,
        return_conversation: bool = False,
        **kwargs
    ) -> AsyncResult:
        ...
```

**Назначение**:
Создает асинхронный генератор для взаимодействия с API AllenAI.

**Параметры**:
- `cls` (Type[AllenAI]): Класс `AllenAI`.
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `host` (str, optional): Хост для отправки запроса. По умолчанию `"inferd"`.
- `private` (bool, optional): Указывает, является ли запрос приватным. По умолчанию `True`.
- `top_p` (float, optional): Значение `top_p` для управления случайностью генерации. По умолчанию `None`.
- `temperature` (float, optional): Значение температуры для управления случайностью генерации. По умолчанию `None`.
- `conversation` (Conversation, optional): Объект `Conversation` для хранения истории разговора. По умолчанию `None`.
- `return_conversation` (bool, optional): Указывает, следует ли возвращать объект `Conversation` в результате. По умолчанию `False`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий текст от API AllenAI.

**Вызывает исключения**:
- `aiohttp.ClientResponseError`: В случае ошибки при выполнении HTTP-запроса.

**Как работает функция**:

1.  **Форматирование промпта**: Функция подготавливает текстовый запрос (prompt) на основе переданных сообщений. Если предоставлен объект `conversation`, используется последнее сообщение пользователя, иначе все сообщения форматируются в строку.
2.  **Инициализация/Обновление разговора**: Если объект `conversation` не предоставлен, создается новый.
3.  **Генерация разделителя**: Создается уникальный разделитель (boundary) для формирования multipart/form-data запроса.
4.  **Формирование заголовков**: Создаются заголовки запроса, включающие Content-Type с динамическим boundary, User-Agent, и X-Anonymous-User-ID.
5.  **Создание данных формы**: Формируется тело запроса в формате multipart/form-data, включая модель, хост, контент (prompt), флаг приватности и, при наличии, идентификатор родительского сообщения, температуру и top_p.
6.  **Отправка запроса**: Используется `aiohttp.ClientSession` для отправки POST-запроса к API AllenAI с сформированными данными и заголовками.
7.  **Обработка ответа**: Полученный ответ обрабатывается построчно, каждая строка парсится как JSON. Извлекается контент, сгенерированный ассистентом, и возвращается через генератор. Обновляется идентификатор родительского сообщения и добавляются сообщения в историю разговора.
8.  **Завершение**: При получении финального ответа или сигнала остановки, функция завершает работу, возвращая `FinishReason("stop")`. При необходимости возвращается объект `conversation` с историей разговора.

**ASCII flowchart**:

```
    [Начало]
     |
     v
    [Форматирование промпта]
     |
     v
    [Инициализация/Обновление разговора]
     |
     v
    [Генерация разделителя]
     |
     v
    [Формирование заголовков]
     |
     v
    [Создание данных формы]
     |
     v
    [Отправка POST-запроса]
     |
     v
    [Обработка ответа]
     |
     v
    [Извлечение и возврат контента]
     |
     v
    [Обновление истории разговора]
     |
     v
    [Завершение]
```

**Примеры**:

```python
    # Пример 1: Создание асинхронного генератора с минимальными параметрами
    async for message in AllenAI.create_async_generator(model="tulu3-405b", messages=[{"role": "user", "content": "Hello, world!"}]):
        print(message)

    # Пример 2: Создание асинхронного генератора с указанием прокси и температуры
    async for message in AllenAI.create_async_generator(model="OLMo-2-1124-13B-Instruct", messages=[{"role": "user", "content": "Tell me a story."}], proxy="http://proxy.example.com", temperature=0.7):
        print(message)

    # Пример 3: Создание асинхронного генератора с использованием объекта Conversation
    conversation = Conversation(model="tulu3-405b")
    async for message in AllenAI.create_async_generator(model="tulu3-405b", messages=[{"role": "user", "content": "How are you?"}], conversation=conversation, return_conversation=True):
        if isinstance(message, Conversation):
            print(f"Conversation history: {message.messages}")
        else:
            print(message)
```
```python
from __future__ import annotations
import json
from uuid import uuid4
from aiohttp import ClientSession
from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..requests.raise_for_status import raise_for_status
from ..providers.response import FinishReason, JsonConversation
from .helper import format_prompt, get_last_user_message


class Conversation(JsonConversation):
    parent: str = None
    x_anonymous_user_id: str = None

    def __init__(self, model: str):
        super().__init__()  # Ensure parent class is initialized
        self.model = model
        self.messages = []  # Instance-specific list
        if not self.x_anonymous_user_id:
            self.x_anonymous_user_id = str(uuid4())


class AllenAI(AsyncGeneratorProvider, ProviderModelMixin):
    label = "Ai2 Playground"
    url = "https://playground.allenai.org"
    login_url = None
    api_endpoint = "https://olmo-api.allen.ai/v4/message/stream"
    
    working = True
    needs_auth = False
    use_nodriver = False
    supports_stream = True
    supports_system_message = False
    supports_message_history = True

    default_model = 'tulu3-405b'
    models = [
        default_model,
        'OLMo-2-1124-13B-Instruct',
        'tulu-3-1-8b',
        'Llama-3-1-Tulu-3-70B',
        'olmoe-0125'
    ]
    
    model_aliases = {
        "tulu-3-405b": default_model,
        "olmo-2-13b": "OLMo-2-1124-13B-Instruct",
        "tulu-3-1-8b": "tulu-3-1-8b",
        "tulu-3-70b": "Llama-3-1-Tulu-3-70B",
        "llama-3.1-405b": "tulu3-405b",
        "llama-3.1-8b": "tulu-3-1-8b",
        "llama-3.1-70b": "Llama-3-1-Tulu-3-70B",
    }

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        host: str = "inferd",
        private: bool = True,
        top_p: float = None,
        temperature: float = None,
        conversation: Conversation = None,
        return_conversation: bool = False,
        **kwargs
    ) -> AsyncResult:
        prompt = format_prompt(messages) if conversation is None else get_last_user_message(messages)
        # Initialize or update conversation
        if conversation is None:
            conversation = Conversation(model)
        
        # Generate new boundary for each request
        boundary = f"----WebKitFormBoundary{uuid4().hex}"
        
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": f"multipart/form-data; boundary={boundary}",
            "origin": cls.url,
            "referer": f"{cls.url}/",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "x-anonymous-user-id": conversation.x_anonymous_user_id,
        }
        
        # Build multipart form data
        form_data = [
            f'--{boundary}\\r\\n'\
            f'Content-Disposition: form-data; name="model"\\r\\n\\r\\n{cls.get_model(model)}\\r\\n',\
            
            f'--{boundary}\\r\\n'\
            f'Content-Disposition: form-data; name="host"\\r\\n\\r\\n{host}\\r\\n',\
            
            f'--{boundary}\\r\\n'\
            f'Content-Disposition: form-data; name="content"\\r\\n\\r\\n{prompt}\\r\\n',\
            
            f'--{boundary}\\r\\n'\
            f'Content-Disposition: form-data; name="private"\\r\\n\\r\\n{str(private).lower()}\\r\\n'\
        ]
        
        # Add parent if exists in conversation
        if conversation.parent:
            form_data.append(
                f'--{boundary}\\r\\n'\
                f'Content-Disposition: form-data; name="parent"\\r\\n\\r\\n{conversation.parent}\\r\\n'\
            )
        
        # Add optional parameters
        if temperature is not None:
            form_data.append(
                f'--{boundary}\\r\\n'\
                f'Content-Disposition: form-data; name="temperature"\\r\\n\\r\\n{temperature}\\r\\n'\
            )
        
        if top_p is not None:
            form_data.append(
                f'--{boundary}\\r\\n'\
                f'Content-Disposition: form-data; name="top_p"\\r\\n\\r\\n{top_p}\\r\\n'\
            )
        
        form_data.append(f'--{boundary}--\\r\\n')
        data = "".join(form_data).encode()

        async with ClientSession(headers=headers) as session:
            async with session.post(
                cls.api_endpoint,
                data=data,
                proxy=proxy,
            ) as response:
                await raise_for_status(response)
                current_parent = None
                
                async for chunk in response.content:
                    if not chunk:
                        continue
                    decoded = chunk.decode(errors="ignore")
                    for line in decoded.splitlines():
                        line = line.strip()
                        if not line:
                            continue
                        
                        try:
                            data = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        
                        if isinstance(data, dict):
                            # Update the parental ID
                            if data.get("children"):
                                for child in data["children"]:
                                    if child.get("role") == "assistant":
                                        current_parent = child.get("id")
                                        break
                            
                            # We process content only from the assistant
                            if "message" in data and data.get("content"):
                                content = data["content"]
                                # Skip empty content blocks
                                if content.strip():
                                    yield content
                            
                            # Processing the final response
                            if data.get("final") or data.get("finish_reason") == "stop":
                                if current_parent:
                                    conversation.parent = current_parent
                                
                                # Add a message to the story
                                conversation.messages.extend([
                                    {"role": "user", "content": prompt},
                                    {"role": "assistant", "content": content}
                                ])
                                
                                if return_conversation:
                                    yield conversation
                                
                                yield FinishReason("stop")
                                return