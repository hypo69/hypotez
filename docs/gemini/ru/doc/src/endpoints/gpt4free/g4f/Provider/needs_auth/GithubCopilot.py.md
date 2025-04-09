# Модуль для работы с GitHub Copilot
## Обзор

Модуль предоставляет класс `GithubCopilot`, который позволяет взаимодействовать с сервисом GitHub Copilot для генерации текста. Он поддерживает потоковую передачу данных, требует аутентификации и может работать через прокси. Класс асинхронный, что позволяет эффективно использовать ресурсы при работе с сетью.

## Подробней

Этот модуль предназначен для интеграции с GitHub Copilot API. Он включает в себя функции для создания асинхронного генератора, необходимого для потоковой обработки ответов от API. Модуль поддерживает различные модели, такие как "gpt-4o", "o1-mini", "o1-preview", "claude-3.5-sonnet" и требует аутентификации через API ключ или cookies. Он также умеет управлять conversation_id для поддержания контекста диалога.

## Классы

### `Conversation`
Описание назначения класса:

Класс `Conversation` представляет собой контейнер для хранения идентификатора беседы (conversation_id) с GitHub Copilot.

**Наследует:**

Не наследует другие классы.

**Атрибуты:**

- `conversation_id` (str): Уникальный идентификатор беседы.

### `GithubCopilot`

**Описание**: Класс `GithubCopilot` предназначен для взаимодействия с API GitHub Copilot. Он обеспечивает асинхронную генерацию текста на основе предоставленных сообщений, поддерживает потоковую передачу данных и требует аутентификации.

**Принцип работы**:
Класс `GithubCopilot` инициализируется без параметров. Для работы с API требуется передать API-ключ или cookies, а также идентификатор беседы (conversation_id) для поддержания контекста.

**Атрибуты:**
- `label` (str): Метка провайдера, в данном случае "GitHub Copilot".
- `url` (str): URL GitHub Copilot.
- `working` (bool): Указывает, работает ли провайдер (в данном случае `True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (в данном случае `True`).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (в данном случае `True`).
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o`).
- `models` (List[str]): Список поддерживаемых моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с API GitHub Copilot.

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
    Создает асинхронный генератор для взаимодействия с API GitHub Copilot.

    Args:
        model (str): Модель для генерации текста.
        messages (Messages): Список сообщений для передачи в API.
        stream (bool, optional): Флаг, указывающий на использование потоковой передачи данных. По умолчанию `False`.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
        conversation_id (str, optional): Идентификатор беседы. По умолчанию `None`.
        conversation (Conversation, optional): Объект беседы. По умолчанию `None`.
        return_conversation (bool, optional): Флаг, указывающий на необходимость возврата объекта беседы. По умолчанию `False`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор для получения ответов от API.

    Raises:
        Exception: В случае ошибок при запросе токена или при создании/отправке сообщений.
    """
```

**Назначение**: Функция `create_async_generator` создает и возвращает асинхронный генератор, который обеспечивает взаимодействие с API GitHub Copilot. Она отвечает за аутентификацию, установку заголовков, формирование данных запроса и обработку потоковых ответов от API.

**Параметры**:
- `cls`: Ссылка на класс `GithubCopilot`.
- `model` (str): Модель для генерации текста.
- `messages` (Messages): Список сообщений для передачи в API.
- `stream` (bool, optional): Флаг, указывающий на использование потоковой передачи данных. По умолчанию `False`.
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `cookies` (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
- `conversation_id` (str, optional): Идентификатор беседы. По умолчанию `None`.
- `conversation` (Conversation, optional): Объект беседы. По умолчанию `None`.
- `return_conversation` (bool, optional): Флаг, указывающий на необходимость возврата объекта беседы. По умолчанию `False`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор для получения ответов от API.

**Вызывает исключения**:
- `Exception`: В случае ошибок при запросе токена или при создании/отправке сообщений.

**Внутренние функции**:
- Отсутствуют

**Как работает функция**:

1. **Инициализация**:
   - Устанавливает модель по умолчанию, если она не предоставлена.
   - Получает cookies, если они не предоставлены.

2. **Создание сессии**:
   - Создает асинхронную сессию `ClientSession` с использованием `aiohttp`.
   - Устанавливает заголовки User-Agent, Accept-Language, Referer, Content-Type и другие.

3. **Аутентификация**:
   - Если `api_key` не предоставлен, запрашивает токен аутентификации с `https://github.com/github-copilot/chat/token`.
   - Добавляет заголовок `Authorization` с полученным токеном.

4. **Управление conversation_id**:
   - Если `conversation_id` не предоставлен, создает новую беседу, запросив `thread_id` с `https://api.individual.githubcopilot.com/github/chat/threads`.

5. **Формирование данных запроса**:
   - Если `return_conversation` установлен в `True`, возвращает объект `Conversation` с `conversation_id`.
   - Форматирует сообщения с использованием `format_prompt` или `get_last_user_message`.
   - Формирует JSON-данные для отправки запроса, включая `content`, `intent`, `references`, `context`, `currentURL`, `streaming`, `confirmations`, `customInstructions`, `model` и `mode`.

6. **Отправка запроса и обработка ответа**:
   - Отправляет POST-запрос на `https://api.individual.githubcopilot.com/github/chat/threads/{conversation_id}/messages` с сформированными JSON-данными и заголовками.
   - Асинхронно читает ответ по строкам и извлекает данные из строк, начинающихся с `data: `.
   - Декодирует JSON-данные и возвращает содержимое (`body`), если тип данных (`type`) равен `content`.

```
Инициализация
    │
    ├── Проверка наличия model и установка default_model
    │
    ├── Получение cookies
    │
    └── Создание ClientSession
         │
         ├── Определение api_key
         │   │
         │   └── Запрос токена, если api_key не предоставлен
         │
         ├── Определение conversation_id
         │   │
         │   └── Создание новой беседы, если conversation_id не предоставлен
         │
         └── Формирование json_data
              │
              └── Отправка POST-запроса
                   │
                   └── Обработка потока ответов
```

**Примеры**:

```python
# Пример 1: Создание асинхронного генератора с использованием API-ключа
async for message in GithubCopilot.create_async_generator(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello, Copilot!"}],
    api_key="YOUR_API_KEY"
):
    print(message)

# Пример 2: Создание асинхронного генератора с использованием cookies и прокси
async for message in GithubCopilot.create_async_generator(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello, Copilot!"}],
    cookies={"cookie_name": "cookie_value"},
    proxy="http://your_proxy:8080"
):
    print(message)

# Пример 3: Создание асинхронного генератора с возвратом объекта беседы
async for item in GithubCopilot.create_async_generator(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello, Copilot!"}],
    return_conversation=True
):
    if isinstance(item, Conversation):
        conversation = item
        print(f"Conversation ID: {conversation.conversation_id}")
    else:
        print(item)