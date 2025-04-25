# Anthropic.py

## Обзор

Модуль предоставляет класс `Anthropic`, который реализует интерфейс для работы с API Anthropic, 
позволяя взаимодействовать с различными моделями Anthropic.

## Подробнее

Класс `Anthropic` наследует класс `OpenaiAPI` и предоставляет расширенные возможности 
для работы с моделями Anthropic. Он поддерживает:

- Авторизацию с помощью ключа API.
- Генерацию текста с использованием различных моделей.
- Поддержку потоковой передачи (streaming) ответов.
- Поддержку системных сообщений.
- Поддержку истории сообщений.
- Поддержку инструментов (tools).
- Обработку изображений.

## Классы

### `class Anthropic`

**Описание**: Класс `Anthropic` реализует интерфейс для работы с API Anthropic.

**Наследует**: `OpenaiAPI`

**Атрибуты**:

- `label (str)`: Название провайдера.
- `url (str)`: URL-адрес для доступа к веб-интерфейсу Anthropic API.
- `login_url (str)`: URL-адрес для доступа к странице авторизации Anthropic API.
- `working (bool)`: Флаг, указывающий на работоспособность провайдера.
- `api_base (str)`: Базовый URL-адрес для вызова API Anthropic.
- `needs_auth (bool)`: Флаг, указывающий на необходимость авторизации.
- `supports_stream (bool)`: Флаг, указывающий на поддержку потоковой передачи ответов.
- `supports_system_message (bool)`: Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history (bool)`: Флаг, указывающий на поддержку истории сообщений.
- `default_model (str)`: Название модели по умолчанию.
- `models (list[str])`: Список доступных моделей.
- `models_aliases (dict[str, str])`: Словарь псевдонимов для моделей.

**Методы**:

- `get_models(cls, api_key: str = None, **kwargs)`: Возвращает список доступных моделей.
- `create_async_generator(cls, model: str, messages: Messages, proxy: str = None, timeout: int = 120, media: MediaListType = None, api_key: str = None, temperature: float = None, max_tokens: int = 4096, top_k: int = None, top_p: float = None, stop: list[str] = None, stream: bool = False, headers: dict = None, impersonate: str = None, tools: Optional[list] = None, extra_data: dict = {}, **kwargs) -> AsyncResult`: Создает асинхронный генератор для генерации текста с использованием API Anthropic.
- `get_headers(cls, stream: bool, api_key: str = None, headers: dict = None) -> dict`: Возвращает заголовки для запроса к API Anthropic.

### Методы класса

#### `get_models`

**Назначение**: Возвращает список доступных моделей Anthropic.

**Параметры**:

- `api_key (str, optional)`: Ключ API для доступа к Anthropic API. По умолчанию `None`.

**Возвращает**:

- `list[str]`: Список доступных моделей Anthropic.

**Пример**:

```python
>>> Anthropic.get_models(api_key='your_api_key')
['claude-3-5-sonnet-latest', 'claude-3-5-sonnet-20241022', ...]
```

#### `create_async_generator`

**Назначение**: Создает асинхронный генератор для генерации текста с использованием API Anthropic.

**Параметры**:

- `model (str)`: Название модели Anthropic для использования.
- `messages (Messages)`: Список сообщений, которые будут использоваться для генерации текста.
- `proxy (str, optional)`: Прокси-сервер для использования. По умолчанию `None`.
- `timeout (int, optional)`: Максимальное время ожидания ответа. По умолчанию `120`.
- `media (MediaListType, optional)`: Список изображений, которые будут использоваться для генерации текста. По умолчанию `None`.
- `api_key (str, optional)`: Ключ API для доступа к Anthropic API. По умолчанию `None`.
- `temperature (float, optional)`: Параметр, контролирующий креативность модели. По умолчанию `None`.
- `max_tokens (int, optional)`: Максимальное количество токенов в ответе. По умолчанию `4096`.
- `top_k (int, optional)`: Параметр, контролирующий выбор токенов. По умолчанию `None`.
- `top_p (float, optional)`: Параметр, контролирующий выбор токенов. По умолчанию `None`.
- `stop (list[str], optional)`: Список токенов, которые должны остановить генерацию текста. По умолчанию `None`.
- `stream (bool, optional)`: Флаг, указывающий на использование потоковой передачи ответов. По умолчанию `False`.
- `headers (dict, optional)`: Дополнительные заголовки для запроса к API. По умолчанию `None`.
- `impersonate (str, optional)`: Имя пользователя, от которого будет выполняться запрос. По умолчанию `None`.
- `tools (Optional[list], optional)`: Список инструментов, которые будут использоваться для генерации текста. По умолчанию `None`.
- `extra_data (dict, optional)`: Дополнительные данные для запроса к API. По умолчанию `{}`.

**Возвращает**:

- `AsyncResult`: Асинхронный результат, представляющий собой генератор ответов от API Anthropic.

**Пример**:

```python
>>> async def generate_text():
...     messages = [
...         {"role": "user", "content": "Привет, как дела?"},
...     ]
...     async for response in Anthropic.create_async_generator(model='claude-3-5-sonnet-latest', messages=messages, api_key='your_api_key'):
...         print(response)
...
>>> asyncio.run(generate_text())
Хорошо, спасибо! А у вас?
```

#### `get_headers`

**Назначение**: Возвращает заголовки для запроса к API Anthropic.

**Параметры**:

- `stream (bool)`: Флаг, указывающий на использование потоковой передачи ответов.
- `api_key (str, optional)`: Ключ API для доступа к Anthropic API. По умолчанию `None`.
- `headers (dict, optional)`: Дополнительные заголовки для запроса к API. По умолчанию `None`.

**Возвращает**:

- `dict`: Словарь заголовков для запроса к API Anthropic.

**Пример**:

```python
>>> Anthropic.get_headers(stream=True, api_key='your_api_key')
{'Accept': 'text/event-stream', 'Content-Type': 'application/json', 'x-api-key': 'your_api_key', 'anthropic-version': '2023-06-01'}
```

## Параметры класса

- `api_key (str, optional)`: Ключ API для доступа к Anthropic API. По умолчанию `None`.

## Примеры

```python
# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)
```

```python
# Генерация текста с использованием модели claude-3-5-sonnet-latest
messages = [
    {"role": "user", "content": "Напиши мне стихотворение о любви."},
]
async for response in Anthropic.create_async_generator(model='claude-3-5-sonnet-latest', messages=messages, api_key='your_api_key'):
    print(response)