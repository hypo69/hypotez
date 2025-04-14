# Модуль для работы с Github Copilot
=====================================

Модуль предоставляет асинхронный класс `GithubCopilot` для взаимодействия с API Github Copilot.
Он поддерживает создание бесед, отправку сообщений и получение ответов в режиме реального времени.

## Обзор

Модуль предназначен для интеграции с Github Copilot в асинхронном режиме. Он включает в себя:
- Аутентификацию через API key или cookies.
- Поддержку потоковой передачи данных (streaming).
- Управление беседами (conversation management).
- Различные модели, такие как gpt-4o, o1-mini, o1-preview и claude-3.5-sonnet.

## Классы

### `Conversation`
Описание класса для представления беседы с Github Copilot.

**Наследует:**
- `BaseConversation`

**Атрибуты:**
- `conversation_id` (str): Уникальный идентификатор беседы.

**Методы:**
- `__init__(conversation_id: str)`: Конструктор класса.

### `GithubCopilot`
Описание класса для взаимодействия с API Github Copilot.

**Наследует:**
- `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты:**
- `label` (str): Метка провайдера ("GitHub Copilot").
- `url` (str): URL Github Copilot ("https://github.com/copilot").
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации (True).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи (True).
- `default_model` (str): Модель по умолчанию ("gpt-4o").
- `models` (list): Список поддерживаемых моделей.

## Методы класса

### `create_async_generator`
```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool = False,
    api_key: str = None,
    proxy: str = None,
    cookies: Cookies = None,
    conversation_id: str = None,
    conversation: Conversation = None,
    return_conversation: bool = False,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для взаимодействия с API Github Copilot.

    Args:
        cls (GithubCopilot): Ссылка на класс.
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки.
        stream (bool): Флаг, указывающий на использование потоковой передачи.
        api_key (str, optional): API ключ для аутентификации. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
        conversation_id (str, optional): Идентификатор беседы. По умолчанию `None`.
        conversation (Conversation, optional): Объект беседы. По умолчанию `None`.
        return_conversation (bool, optional): Флаг, указывающий на возврат объекта беседы. По умолчанию `False`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор для получения ответов от API.

    Raises:
        Exception: В случае ошибок при запросе токена или создании беседы.

    Example:
        >>> async for message in GithubCopilot.create_async_generator(model="gpt-4o", messages=[{"role": "user", "content": "Hello"}], api_key="YOUR_API_KEY"):
        ...     print(message)
    """
```
**Назначение**:
Создает асинхронный генератор для взаимодействия с API Github Copilot.

**Параметры**:
- `cls`: Ссылка на класс `GithubCopilot`.
- `model` (str): Название модели для использования.
- `messages` (Messages): Список сообщений для отправки.
- `stream` (bool): Флаг, указывающий на использование потоковой передачи. По умолчанию `False`.
- `api_key` (str, optional): API ключ для аутентификации. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `cookies` (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
- `conversation_id` (str, optional): Идентификатор беседы. По умолчанию `None`.
- `conversation` (Conversation, optional): Объект беседы. По умолчанию `None`.
- `return_conversation` (bool, optional): Флаг, указывающий на возврат объекта беседы. По умолчанию `False`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор для получения ответов от API.

**Как работает функция**:
1.  Определяет модель для использования, если она не указана, использует `default_model`.
2.  Получает cookies с github.com, если они не были переданы.
3.  Создает асинхронную сессию `aiohttp.ClientSession` с заданными параметрами.
4.  Если `api_key` не предоставлен, пытается получить его, запросив токен с `https://github.com/github-copilot/chat/token`.
5.  Устанавливает заголовки для аутентификации с использованием полученного `api_key`.
6.  Если `conversation_id` не предоставлен, создает новую беседу, запросив `thread_id` с `https://api.individual.githubcopilot.com/github/chat/threads`.
7.  Если `return_conversation` установлен в `True`, возвращает объект `Conversation` с полученным `conversation_id`.
8.  Форматирует сообщения для отправки в API.
9.  Формирует `json_data` с содержимым сообщения, моделью и другими параметрами.
10. Отправляет POST-запрос к API Github Copilot `https://api.individual.githubcopilot.com/github/chat/threads/{conversation_id}/messages` с данными в формате JSON.
11. Получает ответ от API в режиме потоковой передачи и извлекает данные из каждой строки, начинающейся с `data: `.
12. Преобразует полученные данные JSON и возвращает `body` из `content`, если `type` имеет значение `content`.

**Примеры**:

```python
# Пример использования create_async_generator с указанием api_key
async def example():
    api_key = "YOUR_API_KEY"
    messages = [{"role": "user", "content": "Напиши функцию на Python, которая вычисляет факториал числа."}]
    async for message in GithubCopilot.create_async_generator(model="gpt-4o", messages=messages, api_key=api_key):
        print(message)

# Пример использования create_async_generator с указанием proxy
async def example_with_proxy():
    proxy = "http://your_proxy:8080"
    messages = [{"role": "user", "content": "Как погода в Москве?"}]
    async for message in GithubCopilot.create_async_generator(model="gpt-4o", messages=messages, proxy=proxy):
        print(message)

# Пример использования create_async_generator с указанием conversation_id
async def example_with_conversation():
    conversation_id = "your_conversation_id"
    messages = [{"role": "user", "content": "Продолжи, пожалуйста."}]
    async for message in GithubCopilot.create_async_generator(model="gpt-4o", messages=messages, conversation_id=conversation_id):
        print(message)