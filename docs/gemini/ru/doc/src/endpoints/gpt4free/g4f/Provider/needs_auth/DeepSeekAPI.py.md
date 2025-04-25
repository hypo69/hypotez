# DeepSeekAPI - провайдер для GPT4Free

## Обзор

Этот файл содержит класс `DeepSeekAPI`, который представляет собой провайдера для GPT4Free, использующего API DeepSeek. 
Провайдер предоставляет доступ к различным моделям DeepSeek, включая `deepseek-v3` и `deepseek-r1`, для выполнения 
задач обработки текста и генерации. 

## Подробности

`DeepSeekAPI` реализует асинхронную авторизацию и поддерживает как обычный, так и web-поиск. 
Провайдер использует модуль `dsk.api` для взаимодействия с API DeepSeek.

## Классы

### `class DeepSeekAPI`

**Описание**: Класс `DeepSeekAPI` является провайдером для GPT4Free, использующим API DeepSeek. 
**Наследует**: `AsyncAuthedProvider`, `ProviderModelMixin`
**Атрибуты**:
- `url (str)`: URL-адрес API DeepSeek.
- `working (bool)`: Флаг, указывающий на работоспособность провайдера.
- `needs_auth (bool)`: Флаг, указывающий на необходимость авторизации.
- `use_nodriver (bool)`: Флаг, указывающий на необходимость использования `nodriver`.
- `_access_token (str)`: Токен доступа для API DeepSeek.
- `default_model (str)`: Имя модели по умолчанию.
- `models (list)`: Список доступных моделей.

**Методы**:

- `on_auth_async(proxy: str = None, **kwargs) -> AsyncIterator`: Асинхронная авторизация. 
  - Получает токен доступа для API DeepSeek.
  - Возвращает `AuthResult`, содержащий токен доступа и другую информацию об авторизации.
- `create_authed(model: str, messages: Messages, auth_result: AuthResult, conversation: JsonConversation = None, web_search: bool = False, **kwargs) -> AsyncResult`: 
  - Создает асинхронную сессию чата с API DeepSeek.
  - Использует токен доступа для авторизации.
  - Возвращает `AsyncResult`, содержащий результаты запроса к модели.

**Внутренние функции**:

- `callback(page)`: Внутренняя функция, которая ожидает, пока токен доступа будет доступен в localStorage браузера.

**Как работает**:

- При создании экземпляра класса `DeepSeekAPI` устанавливается флаг `working` в зависимости от доступности модуля `dsk.api`.
- `on_auth_async` инициализирует браузер с помощью `get_nodriver` и запускает процесс авторизации. 
- В процессе авторизации `callback` ожидает появления токена доступа в localStorage браузера и сохраняет его в `_access_token`.
- `create_authed` создает новую сессию чата с использованием `dsk.api` и токена доступа.
- После этого происходит асинхронная отправка сообщений в сессию чата с использованием `api.chat_completion`.
- Функция `api.chat_completion` поддерживает асинхронное получение ответа,  обрабатывает состояния "thinking" и "text" и возвращает результаты в виде `AsyncResult`.


**Примеры**:

```python
# Пример использования DeepSeekAPI
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepSeekAPI import DeepSeekAPI

# Инициализация провайдера
deepseek_provider = DeepSeekAPI(model="deepseek-v3")

# Авторизация
async def auth_and_chat(provider):
    auth_result = await provider.on_auth_async()
    # Выполняем запрос к модели
    conversation = await provider.create_authed(model="deepseek-v3", messages=["Hello world!"], auth_result=auth_result)
    async for result in conversation:
        if isinstance(result, Reasoning):
            print(result.status)
        elif isinstance(result, str):
            print(result)
        elif isinstance(result, FinishReason):
            print(f"Finish reason: {result.reason}")

asyncio.run(auth_and_chat(deepseek_provider))
```
```python
# Пример использования DeepSeekAPI с web-поиском
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepSeekAPI import DeepSeekAPI

# Инициализация провайдера
deepseek_provider = DeepSeekAPI(model="deepseek-v3")

# Авторизация
async def auth_and_chat(provider):
    auth_result = await provider.on_auth_async()
    # Выполняем запрос к модели с web-поиском
    conversation = await provider.create_authed(model="deepseek-v3", messages=["What is the capital of France?"], auth_result=auth_result, web_search=True)
    async for result in conversation:
        if isinstance(result, Reasoning):
            print(result.status)
        elif isinstance(result, str):
            print(result)
        elif isinstance(result, FinishReason):
            print(f"Finish reason: {result.reason}")

asyncio.run(auth_and_chat(deepseek_provider))

```

## Параметры класса

- `url (str)`: URL-адрес API DeepSeek.
- `working (bool)`: Флаг, указывающий на работоспособность провайдера.
- `needs_auth (bool)`: Флаг, указывающий на необходимость авторизации.
- `use_nodriver (bool)`: Флаг, указывающий на необходимость использования `nodriver`.
- `_access_token (str)`: Токен доступа для API DeepSeek.
- `default_model (str)`: Имя модели по умолчанию.
- `models (list)`: Список доступных моделей.


## Примеры

```python
# Пример использования DeepSeekAPI
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepSeekAPI import DeepSeekAPI

# Инициализация провайдера
deepseek_provider = DeepSeekAPI(model="deepseek-v3")

# Авторизация
async def auth_and_chat(provider):
    auth_result = await provider.on_auth_async()
    # Выполняем запрос к модели
    conversation = await provider.create_authed(model="deepseek-v3", messages=["Hello world!"], auth_result=auth_result)
    async for result in conversation:
        if isinstance(result, Reasoning):
            print(result.status)
        elif isinstance(result, str):
            print(result)
        elif isinstance(result, FinishReason):
            print(f"Finish reason: {result.reason}")

asyncio.run(auth_and_chat(deepseek_provider))
```
```python
# Пример использования DeepSeekAPI с web-поиском
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepSeekAPI import DeepSeekAPI

# Инициализация провайдера
deepseek_provider = DeepSeekAPI(model="deepseek-v3")

# Авторизация
async def auth_and_chat(provider):
    auth_result = await provider.on_auth_async()
    # Выполняем запрос к модели с web-поиском
    conversation = await provider.create_authed(model="deepseek-v3", messages=["What is the capital of France?"], auth_result=auth_result, web_search=True)
    async for result in conversation:
        if isinstance(result, Reasoning):
            print(result.status)
        elif isinstance(result, str):
            print(result)
        elif isinstance(result, FinishReason):
            print(f"Finish reason: {result.reason}")

asyncio.run(auth_and_chat(deepseek_provider))

```
```python
# Пример использования DeepSeekAPI с моделью deepseek-r1
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepSeekAPI import DeepSeekAPI

# Инициализация провайдера
deepseek_provider = DeepSeekAPI(model="deepseek-r1")

# Авторизация
async def auth_and_chat(provider):
    auth_result = await provider.on_auth_async()
    # Выполняем запрос к модели
    conversation = await provider.create_authed(model="deepseek-r1", messages=["Write me a short story about a cat."], auth_result=auth_result)
    async for result in conversation:
        if isinstance(result, Reasoning):
            print(result.status)
        elif isinstance(result, str):
            print(result)
        elif isinstance(result, FinishReason):
            print(f"Finish reason: {result.reason}")

asyncio.run(auth_and_chat(deepseek_provider))