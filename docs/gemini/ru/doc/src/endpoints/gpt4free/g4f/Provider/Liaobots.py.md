# Модуль для работы с провайдером Liaobots
================================================

Модуль содержит класс :class:`Liaobots`, который используется для взаимодействия с Liaobots API для получения ответов от различных AI-моделей.
Модуль определяет модели и предоставляет асинхронный генератор для взаимодействия с API.

## Оглавление
- [Обзор](#обзор)
- [Подробнее](#подробнее)
- [Классы](#классы)
    - [Liaobots](#liaobots)
- [Функции](#функции)
    - [is_supported](#is_supported)
    - [create_async_generator](#create_async_generator)
    - [initialize_auth_code](#initialize_auth_code)
    - [ensure_auth_code](#ensure_auth_code)

## Обзор

Модуль предназначен для асинхронного взаимодействия с API Liaobots, предоставляющего доступ к различным моделям, таким как Claude, Gemini и GPT.
Он включает в себя поддержку истории сообщений и системных сообщений.

## Подробнее

Модуль определяет класс `Liaobots`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`.
Он содержит информацию о поддерживаемых моделях, их максимальной длине и контексте.
Модуль использует асинхронные запросы для взаимодействия с API Liaobots и предоставляет методы для создания асинхронного генератора, инициализации и обеспечения наличия кода аутентификации.

## Классы

### `Liaobots`

**Описание**: Класс для взаимодействия с API Liaobots.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL API Liaobots.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.
- `_auth_code` (str): Код аутентификации.
- `_cookie_jar` (aiohttp.CookieJar): Cookie Jar для хранения cookie сессии.

**Методы**:
- `is_supported(model: str) -> bool`: Проверяет, поддерживается ли данная модель.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, connector: BaseConnector = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от API.
- `initialize_auth_code(session: ClientSession) -> None`: Инициализирует код аутентификации.
- `ensure_auth_code(session: ClientSession) -> None`: Проверяет и инициализирует код аутентификации, если он не инициализирован.

## Функции

### `is_supported`

```python
@classmethod
def is_supported(cls, model: str) -> bool:
    """
    Check if the given model is supported.
    """
    return model in models or model in cls.model_aliases
```

**Назначение**: Проверяет, поддерживается ли указанная модель провайдером.

**Параметры**:
- `model` (str): Имя модели для проверки.

**Возвращает**:
- `bool`: `True`, если модель поддерживается, `False` в противном случае.

**Как работает функция**:
1. Функция проверяет, содержится ли имя модели в списке поддерживаемых моделей (`models`) или в словаре псевдонимов моделей (`cls.model_aliases`).
2. Если модель найдена хотя бы в одном из этих мест, функция возвращает `True`, иначе возвращает `False`.

```
Проверка наличия модели в списках
    A: model in models or model in cls.model_aliases
    |
    B: Возвращает True, если модель найдена, иначе False
```

**Примеры**:
```python
# Пример 1: Проверка поддерживаемой модели
Liaobots.is_supported("gpt-4o-2024-08-06")  # Вернет True

# Пример 2: Проверка модели с псевдонимом
Liaobots.is_supported("gpt-4o")  # Вернет True, так как "gpt-4o" является псевдонимом для "gpt-4o-2024-08-06"

# Пример 3: Проверка неподдерживаемой модели
Liaobots.is_supported("unsupported-model")  # Вернет False
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    connector: BaseConnector = None,
    **kwargs
) -> AsyncResult:
    """
    Creates an asynchronous generator for interacting with the API.
    """
    ...
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API Liaobots и получения ответов.

**Параметры**:
- `model` (str): Имя модели для использования.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `connector` (BaseConnector, optional): Aiohttp коннектор. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, такие как `system_message`.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий содержимое ответов от API.

**Вызывает исключения**:
- `RuntimeError`: Если не удается получить код аутентификации.

**Как работает функция**:

1. **Выбор модели**: Функция `get_model` используется для получения фактического имени модели из псевдонима, если указано псевдоним.
2. **Подготовка заголовков**: Создаются заголовки HTTP-запроса, включая `referer`, `origin` и `user-agent`.
3. **Создание сессии**: Создается асинхронная сессия `ClientSession` с заданными заголовками, cookie jar и коннектором.
4. **Подготовка данных**: Создается словарь `data` с информацией о запросе, включая `conversationId`, `model`, `messages`, `key` и `prompt` (системное сообщение).
5. **Получение кода аутентификации**:
   - Если `cls._auth_code` пуст, выполняется запрос к `https://liaobots.work/recaptcha/api/login` для получения кода аутентификации.
   - Затем выполняется запрос к `https://liaobots.work/api/user` с текущим `authcode` для обновления кода аутентификации.
   - Если код аутентификации не получен, вызывается `RuntimeError`.
6. **Отправка запроса и получение ответа**:
   - Выполняется POST-запрос к `https://liaobots.work/api/chat` с данными запроса и заголовком `x-auth-code`.
   - Асинхронно обрабатывается ответ, и из каждой строки, начинающейся с `data: `, извлекается содержимое (`content`) и возвращается через `yield`.
7. **Обработка исключений**:
   - Если происходит исключение, повторяется попытка получения кода аутентификации и отправки запроса с фиксированным `authcode`.
   - Это позволяет обработать временные проблемы с аутентификацией.

```
Получение ответа от API Liaobots
    A: Получение имени модели
    |
    B: Создание заголовков HTTP-запроса
    |
    C: Создание асинхронной сессии
    |
    D: Подготовка данных для запроса
    |
    E: Проверка и получение кода аутентификации
    |
    F: Отправка POST-запроса к API
    |
    G: Асинхронное получение и обработка ответа
    |
    H: Обработка исключений и повторная попытка
```

**Примеры**:

```python
# Пример 1: Создание асинхронного генератора с минимальными параметрами
messages = [{"role": "user", "content": "Hello, how are you?"}]
async_generator = Liaobots.create_async_generator(model="gpt-4o-2024-08-06", messages=messages)

# Пример 2: Создание асинхронного генератора с прокси и системным сообщением
messages = [{"role": "user", "content": "Translate 'hello' to French."}]
async_generator = Liaobots.create_async_generator(
    model="gpt-4o-2024-08-06",
    messages=messages,
    proxy="http://your-proxy:8080",
    system_message="You are a translation assistant."
)

# Пример 3: Использование асинхронного генератора для получения ответа
async def get_response():
    messages = [{"role": "user", "content": "Tell me a joke."}]
    async for response_chunk in Liaobots.create_async_generator(model="gpt-4o-2024-08-06", messages=messages):
        print(response_chunk, end="")

import asyncio
asyncio.run(get_response())
```

### `initialize_auth_code`

```python
@classmethod
async def initialize_auth_code(cls, session: ClientSession) -> None:
    """
    Initialize the auth code by making the necessary login requests.
    """
    ...
```

**Назначение**: Инициализирует код аутентификации, выполняя необходимые запросы для входа в систему.

**Параметры**:
- `session` (ClientSession): Асинхронная сессия для выполнения запросов.

**Как работает функция**:

1. **Выполнение POST-запроса**:
   - Выполняется POST-запрос к `https://liaobots.work/api/user` с фиксированным `authcode` "pTIQr4FTnVRfr".
2. **Обработка ответа**:
   - Извлекается `authCode` из JSON-ответа.
   - Если `authCode` пуст, вызывается `RuntimeError`.
3. **Сохранение кода и cookie**:
   - Сохраненный `authCode` присваивается `cls._auth_code`.
   - Cookie Jar из сессии сохраняется в `cls._cookie_jar`.

```
Инициализация кода аутентификации
    A: Выполнение POST-запроса к API
    |
    B: Извлечение authCode из JSON-ответа
    |
    C: Проверка наличия authCode
    |
    D: Сохранение authCode и cookie
```

**Примеры**:

```python
# Пример 1: Инициализация кода аутентификации с использованием асинхронной сессии
import aiohttp
import asyncio

async def initialize():
    async with aiohttp.ClientSession() as session:
        await Liaobots.initialize_auth_code(session)
        print(f"Auth code initialized: {Liaobots._auth_code}")

asyncio.run(initialize())
```

### `ensure_auth_code`

```python
@classmethod
async def ensure_auth_code(cls, session: ClientSession) -> None:
    """
    Ensure the auth code is initialized, and if not, perform the initialization.
    """
    if not cls._auth_code:
        await cls.initialize_auth_code(session)
```

**Назначение**: Проверяет, инициализирован ли код аутентификации, и выполняет инициализацию, если это необходимо.

**Параметры**:
- `session` (ClientSession): Асинхронная сессия для выполнения запросов.

**Как работает функция**:

1. **Проверка кода аутентификации**:
   - Проверяется, является ли `cls._auth_code` пустым.
2. **Инициализация, если необходимо**:
   - Если `cls._auth_code` пуст, вызывается `cls.initialize_auth_code(session)` для инициализации кода аутентификации.

```
Проверка и инициализация кода аутентификации
    A: Проверка наличия кода аутентификации
    |
    B: Вызов initialize_auth_code, если код отсутствует
```

**Примеры**:

```python
# Пример 1: Обеспечение инициализации кода аутентификации перед использованием API
import aiohttp
import asyncio

async def ensure_and_use():
    async with aiohttp.ClientSession() as session:
        await Liaobots.ensure_auth_code(session)
        print(f"Auth code ensured: {Liaobots._auth_code}")

asyncio.run(ensure_and_use())