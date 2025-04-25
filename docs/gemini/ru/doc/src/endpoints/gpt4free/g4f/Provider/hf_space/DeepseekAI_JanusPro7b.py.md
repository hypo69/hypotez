# Модуль DeepseekAI_JanusPro7b 

## Обзор

Этот модуль предоставляет класс `DeepseekAI_JanusPro7b` для взаимодействия с моделью Janus-Pro-7B от DeepseekAI, размещенной на Hugging Face Spaces. 

Класс реализует интерфейс `AsyncGeneratorProvider`, предоставляя асинхронный генератор для получения ответов от модели, и наследует от `ProviderModelMixin` для управления моделями. 

## Подробнее

`DeepseekAI_JanusPro7b` использует API Hugging Face Spaces для отправки запросов к модели Janus-Pro-7B и обработки ответов. 

Он поддерживает следующие функции:

* **Асинхронный генератор:**  Класс `DeepseekAI_JanusPro7b` предоставляет асинхронный генератор для получения ответов от модели, позволяя обрабатывать поток ответов по мере их поступления.
* **Потоковая обработка:**  Класс `DeepseekAI_JanusPro7b` поддерживает потоковую обработку ответов, позволяя получать и обрабатывать данные модели частями.
* **Обработка системных сообщений:** Класс поддерживает использование системных сообщений, которые могут быть использованы для настройки поведения модели. 
* **История сообщений:** Класс поддерживает историю сообщений, чтобы модель могла получить контекст предыдущих взаимодействий.
* **Обработка изображений:**  Класс поддерживает отправку изображений в качестве входных данных для модели Janus-Pro-7B. 

## Классы

### `class DeepseekAI_JanusPro7b`

**Описание**: Класс для взаимодействия с моделью DeepseekAI Janus-Pro-7B. 

**Наследует**:

* `AsyncGeneratorProvider`: Предоставляет асинхронный генератор для получения ответов от модели.
* `ProviderModelMixin`:  Обеспечивает управление моделями, позволяя использовать различные модели для разных задач.

**Атрибуты**:

* `label (str)`: Название модели.
* `space (str)`:  Имя пространства на Hugging Face Spaces, где размещена модель.
* `url (str)`: URL пространства на Hugging Face Spaces.
* `api_url (str)`: URL API для взаимодействия с моделью.
* `referer (str)`:  Заголовок Referer для запросов к модели.
* `working (bool)`: Флаг, указывающий, работает ли модель.
* `supports_stream (bool)`: Флаг, указывающий, поддерживает ли модель потоковую обработку.
* `supports_system_message (bool)`: Флаг, указывающий, поддерживает ли модель системные сообщения.
* `supports_message_history (bool)`: Флаг, указывающий, поддерживает ли модель историю сообщений.
* `default_model (str)`: Название модели по умолчанию.
* `default_image_model (str)`:  Название модели для обработки изображений по умолчанию.
* `default_vision_model (str)`:  Название модели для обработки визуальной информации по умолчанию.
* `image_models (list)`: Список поддерживаемых моделей для обработки изображений.
* `vision_models (list)`:  Список поддерживаемых моделей для обработки визуальной информации.
* `models (list)`:  Объединенный список поддерживаемых моделей.

**Методы**:

* `run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, image: dict = None, seed: int = 0)`: Отправляет запрос к модели, используя указанный метод (POST или GET).
* `create_async_generator(cls, model: str, messages: Messages, media: MediaListType = None, prompt: str = None, proxy: str = None, cookies: Cookies = None, api_key: str = None, zerogpu_uuid: str = "[object Object]", return_conversation: bool = False, conversation: JsonConversation = None, seed: int = None, **kwargs)`:  Создает асинхронный генератор для взаимодействия с моделью.

### `async def get_zerogpu_token(space: str, session: StreamSession, conversation: JsonConversation, cookies: Cookies = None)`:

**Описание**: Получает токен Zerogpu для доступа к модели.

**Параметры**:

* `space (str)`:  Имя пространства на Hugging Face Spaces.
* `session (StreamSession)`:  Сессия для отправки запросов.
* `conversation (JsonConversation)`:  Объект, содержащий информацию о текущем разговоре.
* `cookies (Cookies, optional)`:  Словарь с cookies.

**Возвращает**:
* `zerogpu_uuid (str)`:  Идентификатор сессии.
* `zerogpu_token (str)`:  Токен для аутентификации.

**Пример**:

```python
# Получение токена Zerogpu
zerogpu_uuid, zerogpu_token = await get_zerogpu_token(space="deepseek-ai/Janus-Pro-7B", session=session, conversation=conversation)
```

## Внутренние функции

### `async def raise_for_status(response: StreamResponse)`:

**Описание**:  Проверяет статус ответа от API модели и выдает исключение `ResponseError` в случае ошибки.

**Параметры**:

* `response (StreamResponse)`:  Ответ от API модели.

### `async def get_cookies(domain: str, raise_requirements_error: bool = False)`:

**Описание**:  Получает cookies для доступа к Hugging Face Spaces.

**Параметры**:

* `domain (str)`:  Домен Hugging Face Spaces.
* `raise_requirements_error (bool, optional)`:  Флаг, указывающий, следует ли выдать исключение в случае отсутствия cookie.

**Возвращает**:
* `cookies (dict)`:  Словарь с cookies.

## Параметры класса

* `label (str)`:  Наименование модели.
* `space (str)`:  Имя пространства на Hugging Face Spaces, где размещена модель.
* `url (str)`:  URL пространства на Hugging Face Spaces.
* `api_url (str)`:  URL API для взаимодействия с моделью.
* `referer (str)`:  Заголовок Referer для запросов к модели.
* `working (bool)`: Флаг, указывающий, работает ли модель.
* `supports_stream (bool)`: Флаг, указывающий, поддерживает ли модель потоковую обработку.
* `supports_system_message (bool)`: Флаг, указывающий, поддерживает ли модель системные сообщения.
* `supports_message_history (bool)`: Флаг, указывающий, поддерживает ли модель историю сообщений.
* `default_model (str)`: Название модели по умолчанию.
* `default_image_model (str)`: Название модели для обработки изображений по умолчанию.
* `default_vision_model (str)`:  Название модели для обработки визуальной информации по умолчанию.
* `image_models (list)`:  Список поддерживаемых моделей для обработки изображений.
* `vision_models (list)`:  Список поддерживаемых моделей для обработки визуальной информации.
* `models (list)`:  Объединенный список поддерживаемых моделей.


## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.DeepseekAI_JanusPro7b import DeepseekAI_JanusPro7b
from hypotez.src.endpoints.gpt4free.g4f.Provider.helper import format_prompt
from hypotez.src.endpoints.gpt4free.g4f.Provider.response import JsonConversation
from hypotez.src.endpoints.gpt4free.g4f.Provider.requests.aiohttp import StreamSession

# Создание инстанса класса DeepseekAI_JanusPro7b
provider = DeepseekAI_JanusPro7b()

# Подготовка данных для запроса
messages = [{"role": "user", "content": "Привет! Как дела?"}]
prompt = format_prompt(messages)
conversation = JsonConversation(session_hash="1234567890abcdef") 

# Создание асинхронного генератора
async_generator = provider.create_async_generator(
    model="janus-pro-7b",
    messages=messages,
    conversation=conversation,
    seed=12345
)

# Обработка ответов от модели
async for response in async_generator:
    print(response)
```
```markdown