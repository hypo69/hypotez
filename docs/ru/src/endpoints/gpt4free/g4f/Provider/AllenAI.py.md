# Модуль `AllenAI.py`

## Обзор

Модуль предоставляет асинхронный интерфейс для взаимодействия с моделями AllenAI, такими как tulu3-405b и OLMo-2-1124-13B-Instruct. Он включает в себя класс `AllenAI`, который позволяет генерировать текст на основе предоставленных сообщений, используя API AllenAI. Модуль поддерживает потоковую передачу данных, что позволяет получать ответы от модели по частям, и предоставляет возможность сохранения истории разговоров.

## Подробнее

Модуль предназначен для интеграции с другими частями проекта `hypotez`, где требуется взаимодействие с AI-моделями AllenAI. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и `json` для обработки данных в формате JSON. Модуль также содержит классы `Conversation` для управления историей разговоров и вспомогательные функции для форматирования запросов.

## Классы

### `Conversation`

**Описание**: Класс для хранения истории разговоров с AI-моделью.

**Наследует**: `JsonConversation`

**Атрибуты**:

- `parent` (str): Идентификатор родительского сообщения в разговоре.
- `x_anonymous_user_id` (str): Уникальный идентификатор анонимного пользователя.
- `model` (str): Название используемой модели.
- `messages` (list): Список сообщений в разговоре.

**Методы**:

- `__init__(self, model: str)`: Инициализирует новый экземпляр класса `Conversation`.

### `AllenAI`

**Описание**: Класс, предоставляющий интерфейс для взаимодействия с AI-моделями AllenAI.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:

- `label` (str): Метка провайдера ("Ai2 Playground").
- `url` (str): URL основного сайта AllenAI.
- `login_url` (str): URL для входа в систему (в данном случае `None`, так как аутентификация не требуется).
- `api_endpoint` (str): URL API для отправки сообщений.
- `working` (bool): Флаг, указывающий, работает ли провайдер (в данном случае `True`).
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация (в данном случае `False`).
- `use_nodriver` (bool): Флаг, указывающий, используется ли драйвер (в данном случае `False`).
- `supports_stream` (bool): Флаг, указывающий, поддерживается ли потоковая передача данных (в данном случае `True`).
- `supports_system_message` (bool): Флаг, указывающий, поддерживаются ли системные сообщения (в данном случае `False`).
- `supports_message_history` (bool): Флаг, указывающий, поддерживается ли история сообщений (в данном случае `True`).
- `default_model` (str): Модель по умолчанию ('tulu3-405b').
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.

**Методы**:

- `create_async_generator(cls, model: str, messages: Messages, proxy: str = None, host: str = "inferd", private: bool = True, top_p: float = None, temperature: float = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`: Асинхронный генератор для создания запросов к API AllenAI и обработки ответов.

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
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API AllenAI.

**Параметры**:

- `cls` (AllenAI): Ссылка на класс `AllenAI`.
- `model` (str): Название используемой модели.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `host` (str, optional): Хост для запроса. По умолчанию "inferd".
- `private` (bool, optional): Флаг, указывающий, является ли разговор приватным. По умолчанию `True`.
- `top_p` (float, optional): Значение для параметра top_p. По умолчанию `None`.
- `temperature` (float, optional): Значение для параметра temperature. По умолчанию `None`.
- `conversation` (Conversation, optional): Объект разговора. По умолчанию `None`.
- `return_conversation` (bool, optional): Флаг, указывающий, нужно ли возвращать объект разговора. По умолчанию `False`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, возвращающий части ответа от API AllenAI.

**Вызывает исключения**:

- `aiohttp.ClientResponseError`: Если возникает ошибка при выполнении HTTP-запроса.
- `json.JSONDecodeError`: Если не удается декодировать JSON-ответ.

**Как работает функция**:

1.  **Формирование запроса**: Функция получает на вход параметры, необходимые для запроса к API AllenAI. Она формирует запрос, включая необходимые заголовки и данные формы. Если предоставлен объект `conversation`, используется последнее сообщение пользователя. В противном случае, формируется полный промпт из всех сообщений.

2.  **Создание объекта разговора**: Если объект `conversation` не предоставлен, создается новый экземпляр класса `Conversation`.

3.  **Выполнение HTTP-запроса**: Функция использует `aiohttp.ClientSession` для выполнения асинхронного POST-запроса к API AllenAI. Запрос отправляется с использованием потоковой передачи данных.

4.  **Обработка ответа**: Функция обрабатывает ответ от API AllenAI по частям. Каждая часть ответа декодируется и преобразуется в JSON. Извлекается содержимое сообщения от ассистента, и возвращается в виде отдельных частей через `yield`.

5.  **Завершение разговора**: Когда приходит финальное сообщение или указана причина остановки, функция обновляет информацию о разговоре, добавляет сообщения пользователя и ассистента в историю разговора и возвращает объект `conversation`, если это указано.

6. **Опциональные параметры**: Если `temperature` или `top_p` заданы, они добавляются в форму запроса.

```
Формирование запроса и инициализация -> HTTP POST запрос -> Обработка чанков ответа -> Извлечение содержимого -> Обновление истории разговора -> Завершение
```

**Примеры**:

```python
# Пример использования функции create_async_generator
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for chunk in AllenAI.create_async_generator(model="tulu3-405b", messages=messages):
    print(chunk)

# Пример использования с прокси
messages = [{"role": "user", "content": "Tell me a joke."}]
async for chunk in AllenAI.create_async_generator(model="tulu3-405b", messages=messages, proxy="http://your-proxy:8080"):
    print(chunk)

# Пример использования с conversation
conversation = Conversation(model="tulu3-405b")
messages = [{"role": "user", "content": "Continue the story."}]
async for chunk in AllenAI.create_async_generator(model="tulu3-405b", messages=messages, conversation=conversation, return_conversation=True):
    if isinstance(chunk, Conversation):
        print(f"Conversation object: {chunk}")
    else:
        print(chunk)