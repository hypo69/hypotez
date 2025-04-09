# Модуль `GithubCopilot`

## Обзор

Модуль предназначен для взаимодействия с GitHub Copilot в режиме асинхронного генератора. Он предоставляет возможность создавать и поддерживать диалоги с использованием различных моделей, включая `gpt-4o`, `o1-mini`, `o1-preview` и `claude-3.5-sonnet`. Модуль требует аутентификации и поддерживает потоковую передачу данных.

## Подробней

Модуль предназначен для интеграции с GitHub Copilot и обеспечивает асинхронное взаимодействие с API. Он позволяет отправлять сообщения и получать ответы в потоковом режиме, что особенно полезно для длительных диалогов. Класс `GithubCopilot` реализует логику подключения, аутентификации и обмена сообщениями с сервером GitHub Copilot.

## Классы

### `Conversation`

**Описание**: Класс представляет собой структуру данных для хранения информации о текущем диалоге (conversation) с GitHub Copilot.

**Атрибуты**:
- `conversation_id` (str): Уникальный идентификатор диалога.

**Методы**:
- `__init__(self, conversation_id: str)`: Инициализирует объект `Conversation` с заданным `conversation_id`.

### `GithubCopilot`

**Описание**: Класс `GithubCopilot` реализует асинхронного провайдера для взаимодействия с GitHub Copilot. Он обеспечивает создание диалогов, отправку сообщений и получение ответов.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Добавляет поддержку выбора модели.

**Атрибуты**:
- `label` (str): Метка провайдера ("GitHub Copilot").
- `url` (str): URL GitHub Copilot ("https://github.com/copilot").
- `working` (bool): Указывает, что провайдер работает (True).
- `needs_auth` (bool): Указывает, что требуется аутентификация (True).
- `supports_stream` (bool): Указывает, что поддерживается потоковая передача (True).
- `default_model` (str): Модель по умолчанию ("gpt-4o").
- `models` (list[str]): Список поддерживаемых моделей (["gpt-4o", "o1-mini", "o1-preview", "claude-3.5-sonnet"]).

## Функции

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
    """
    Создает асинхронный генератор для взаимодействия с GitHub Copilot.

    Args:
        cls (GithubCopilot): Класс GithubCopilot.
        model (str): Используемая модель.
        messages (Messages): Список сообщений для отправки.
        stream (bool, optional): Флаг потоковой передачи. По умолчанию False.
        api_key (str, optional): API ключ для аутентификации. По умолчанию None.
        proxy (str, optional): Прокси сервер. По умолчанию None.
        cookies (Cookies, optional): Cookies для аутентификации. По умолчанию None.
        conversation_id (str, optional): Идентификатор существующего диалога. По умолчанию None.
        conversation (Conversation, optional): Объект Conversation. По умолчанию None.
        return_conversation (bool, optional): Флаг возврата объекта Conversation. По умолчанию False.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор для получения ответов от GitHub Copilot.
    
    Raises:
        Exception: Если происходит ошибка при получении токена или создании диалога.
    """
```

**Назначение**: Функция создает асинхронный генератор для взаимодействия с GitHub Copilot. Она отвечает за установку соединения, аутентификацию и обмен сообщениями с сервером GitHub Copilot.

**Параметры**:
- `cls` (GithubCopilot): Класс `GithubCopilot`.
- `model` (str): Используемая модель.
- `messages` (Messages): Список сообщений для отправки.
- `stream` (bool, optional): Флаг потоковой передачи. По умолчанию `False`.
- `api_key` (str, optional): API ключ для аутентификации. По умолчанию `None`.
- `proxy` (str, optional): Прокси сервер. По умолчанию `None`.
- `cookies` (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
- `conversation_id` (str, optional): Идентификатор существующего диалога. По умолчанию `None`.
- `conversation` (Conversation, optional): Объект `Conversation`. По умолчанию `None`.
- `return_conversation` (bool, optional): Флаг возврата объекта `Conversation`. По умолчанию `False`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор для получения ответов от GitHub Copilot.

**Вызывает исключения**:
- `Exception`: Если происходит ошибка при получении токена или создании диалога.

**Как работает функция**:

1. **Инициализация**: Функция начинается с установки значений по умолчанию для параметров `model` и `cookies`, если они не были предоставлены.
2. **Создание сессии**: Создается асинхронная сессия `ClientSession` с использованием `aiohttp`, которая будет использоваться для отправки запросов к API GitHub Copilot. Устанавливаются необходимые заголовки, такие как `User-Agent`, `Referer` и `Content-Type`.
3. **Аутентификация**: Если `api_key` не предоставлен, функция пытается получить его, отправляя POST-запрос на `https://github.com/github-copilot/chat/token`. Полученный токен используется для формирования заголовка `Authorization`.
4. **Создание диалога**: Если `conversation_id` не предоставлен, функция создает новый диалог, отправляя POST-запрос на `https://api.individual.githubcopilot.com/github/chat/threads`. Полученный `thread_id` используется в качестве `conversation_id`.
5. **Отправка сообщений и получение ответов**: Функция формирует JSON-данные для отправки сообщения, включая контент сообщения, параметры контекста и информацию о модели. Затем она отправляет POST-запрос на `https://api.individual.githubcopilot.com/github/chat/threads/{conversation_id}/messages` и получает ответы в потоковом режиме.
6. **Генерация ответов**: Функция итерирует по строкам ответа и извлекает полезные данные (тело ответа) из JSON-объектов, которые начинаются с `data: `. Полученные данные передаются в генератор для последующей обработки.

**Внутренние функции**: Отсутствуют

**ASCII flowchart**:

```
A: Инициализация параметров
↓
B: Создание асинхронной сессии
↓
C: Аутентификация (получение API ключа, если необходимо)
↓
D: Создание диалога (получение conversation_id, если необходимо)
↓
E: Формирование JSON-данных для отправки сообщения
↓
F: Отправка POST-запроса и получение ответов в потоковом режиме
↓
G: Извлечение полезных данных из JSON-ответов и передача в генератор
```

**Примеры**:

```python
# Пример использования с указанием модели и сообщениями
messages = [{"role": "user", "content": "Hello, Copilot!"}]
async for response in GithubCopilot.create_async_generator(model="gpt-4o", messages=messages):
    print(response)
```

```python
# Пример использования с указанием API ключа и прокси
messages = [{"role": "user", "content": "Tell me a joke."}]
async for response in GithubCopilot.create_async_generator(model="o1-mini", messages=messages, api_key="YOUR_API_KEY", proxy="http://your_proxy:8080"):
    print(response)
```

```python
# Пример использования с существующим conversation_id
messages = [{"role": "user", "content": "Continue the conversation."}]
async for response in GithubCopilot.create_async_generator(model="o1-preview", messages=messages, conversation_id="YOUR_CONVERSATION_ID"):
    print(response)