# Модуль HuggingChat

## Обзор

Модуль `HuggingChat` предоставляет реализацию асинхронного провайдера, который взаимодействует с API чата Hugging Face. Он позволяет использовать различные модели Hugging Face для генерации текста, обработки изображений и других задач.

## Подробнее

Модуль `HuggingChat` реализует асинхронный провайдер, наследуя от `AsyncAuthedProvider` и `ProviderModelMixin`. Он работает с API чата Hugging Face, используя HTTP запросы для отправки запросов и получения ответов.

## Классы

### `class HuggingChat`

**Описание**: Асинхронный провайдер для взаимодействия с API чата Hugging Face.

**Наследует**: `AsyncAuthedProvider`, `ProviderModelMixin`

**Атрибуты**:

- `domain`: Домен API чата Hugging Face (huggingface.co).
- `origin`: Базовый URL API чата Hugging Face.
- `url`: URL API чата Hugging Face.
- `working`: Флаг, указывающий, работает ли провайдер.
- `use_nodriver`: Флаг, указывающий, использует ли провайдер WebDriver.
- `supports_stream`: Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных.
- `needs_auth`: Флаг, указывающий, требуется ли авторизация для использования провайдера.
- `default_model`: Модель по умолчанию для текстового общения.
- `default_vision_model`: Модель по умолчанию для обработки изображений.
- `model_aliases`: Словарь, содержащий псевдонимы для моделей.
- `image_models`: Список моделей, которые поддерживают обработку изображений.
- `text_models`: Список моделей, которые поддерживают обработку текста.

**Методы**:

- `get_models()`: Получает список доступных моделей.
- `on_auth_async(cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator`: Выполняет асинхронную авторизацию.
- `create_authed(model: str, messages: Messages, auth_result: AuthResult, prompt: str = None, media: MediaListType = None, return_conversation: bool = False, conversation: Conversation = None, web_search: bool = False, **kwargs) -> AsyncResult`: Создает асинхронную сессию с авторизацией.
- `create_conversation(session: Session, model: str):`: Создает новую беседу с указанной моделью.
- `fetch_message_id(session: Session, conversation_id: str):`: Получает идентификатор последнего сообщения в беседе.


## Функции

### `Conversation`

**Описание**: Класс, который хранит информацию о беседе.

**Атрибуты**:

- `models`: Словарь, содержащий информацию о моделях, используемых в беседе.

**Методы**:

- `__init__(self, models: dict)`: Инициализирует экземпляр класса `Conversation`.


## Параметры

- `model`: (str) Идентификатор модели Hugging Face.
- `messages`: (Messages) Список сообщений, которые были отправлены в беседу.
- `auth_result`: (AuthResult) Результат авторизации.
- `prompt`: (str) Текстовый запрос для модели.
- `media`: (MediaListType) Список медиафайлов, которые были отправлены в беседу.
- `return_conversation`: (bool) Флаг, указывающий, нужно ли возвращать объект `Conversation`.
- `conversation`: (Conversation) Объект `Conversation`, содержащий информацию о беседе.
- `web_search`: (bool) Флаг, указывающий, нужно ли использовать веб-поиск.

## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf.HuggingChat import HuggingChat
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf.models import default_model

# Создание экземпляра провайдера HuggingChat
hugging_chat = HuggingChat()

# Получение списка доступных моделей
models = hugging_chat.get_models()
print(f"Available models: {models}")

# Создание новой беседы с моделью по умолчанию
conversation = hugging_chat.create_conversation(model=default_model)

# Отправка сообщения в беседу
response = hugging_chat.send_message(conversation, "Hello, world!")

# Получение ответа от модели
print(f"Response: {response}")
```
```markdown