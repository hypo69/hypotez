# Модуль `Liaobots`

## Обзор

Модуль `Liaobots` предоставляет асинхронный интерфейс для взаимодействия с моделями, предоставляемыми сервисом [liaobots.site](https://liaobots.site). Он поддерживает ведение истории сообщений и системные сообщения. Модуль использует `aiohttp` для выполнения асинхронных HTTP-запросов и включает поддержку прокси-серверов.

## Подробнее

Модуль содержит класс `Liaobots`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он позволяет генерировать текст асинхронно, используя различные модели, предоставляемые Liaobots. Модуль также содержит информацию о поддерживаемых моделях, их максимальной длине и лимите токенов.

## Классы

### `Liaobots`

**Описание**: Класс `Liaobots` предоставляет асинхронный интерфейс для взаимодействия с моделями Liaobots.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию контента.
- `ProviderModelMixin`: Предоставляет вспомогательные методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса Liaobots (`https://liaobots.site`).
- `working` (bool): Флаг, указывающий, работает ли провайдер (всегда `True`).
- `supports_message_history` (bool): Флаг, указывающий, поддерживается ли история сообщений (всегда `True`).
- `supports_system_message` (bool): Флаг, указывающий, поддерживаются ли системные сообщения (всегда `True`).
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-2024-08-06`).
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей для удобства использования.
- `_auth_code` (str): Код аутентификации для доступа к API.
- `_cookie_jar`: Контейнер для хранения cookie-файлов сессии.

**Принцип работы**:

Класс `Liaobots` использует асинхронные HTTP-запросы для взаимодействия с API Liaobots. Он поддерживает различные модели и предоставляет методы для создания асинхронных генераторов текста. Для аутентификации используется код авторизации, который автоматически обновляется при необходимости.

## Методы класса

### `is_supported`

```python
    @classmethod
    def is_supported(cls, model: str) -> bool:
        """
        Check if the given model is supported.
        """
```

**Назначение**: Проверяет, поддерживается ли указанная модель.

**Параметры**:
- `model` (str): Имя модели для проверки.

**Возвращает**:
- `bool`: `True`, если модель поддерживается, иначе `False`.

**Как работает функция**:
Функция проверяет, есть ли модель в списке поддерживаемых моделей (`models`) или в словаре псевдонимов моделей (`model_aliases`).

**Примеры**:
```python
Liaobots.is_supported("gpt-4o-2024-08-06")  # Возвращает True
Liaobots.is_supported("nonexistent-model")  # Возвращает False
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
        Создает асинхронный генератор для получения ответов от API Liaobots.
        """
```

**Назначение**: Создает асинхронный генератор для получения ответов от API Liaobots.

**Параметры**:
- `model` (str): Имя модели для использования.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `connector` (BaseConnector, optional): Aiohttp коннектор. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, такие как `system_message`.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий текст от API.

**Как работает функция**:

1.  Извлекает модель, используя `cls.get_model(model)`.
2.  Формирует заголовки запроса.
3.  Создает асинхронную сессию `aiohttp` с заданными заголовками, cookie и коннектором.
4.  Формирует данные для отправки в API, включая `conversationId`, `model`, `messages`, `key` и `prompt` (системное сообщение).
5.  Если `_auth_code` не установлен, выполняет запрос для его получения.
6.  Отправляет запрос к API `https://liaobots.work/api/chat` с данными и заголовком `x-auth-code`.
7.  Получает ответ от API и возвращает асинхронный генератор, который извлекает содержимое из каждой строки ответа.
8.  Обрабатывает исключения, повторно запрашивая `_auth_code` в случае ошибки.

**Внутренние функции**:

Внутри функции используется асинхронный генератор, который обрабатывает строки ответа от API и извлекает содержимое.

**Примеры**:
```python
messages = [{"role": "user", "content": "Hello, world!"}]
async for message in Liaobots.create_async_generator(model="gpt-4o", messages=messages):
    print(message)
```

### `initialize_auth_code`

```python
    @classmethod
    async def initialize_auth_code(cls, session: ClientSession) -> None:
        """
        Initialize the auth code by making the necessary login requests.
        """
```

**Назначение**: Инициализирует код аутентификации, выполняя необходимые запросы для входа.

**Параметры**:
- `session` (ClientSession): Асинхронная сессия `aiohttp`.

**Возвращает**:
- `None`

**Как работает функция**:

1.  Отправляет POST-запрос к `https://liaobots.work/api/user` с фиктивным `authcode`.
2.  Обрабатывает ответ, извлекая код аутентификации из JSON-ответа.
3.  Устанавливает `_auth_code` и сохраняет cookie в `_cookie_jar`.

**Примеры**:
```python
async with ClientSession() as session:
    await Liaobots.initialize_auth_code(session)
```

### `ensure_auth_code`

```python
    @classmethod
    async def ensure_auth_code(cls, session: ClientSession) -> None:
        """
        Ensure the auth code is initialized, and if not, perform the initialization.
        """
```

**Назначение**: Проверяет, инициализирован ли код аутентификации, и если нет, выполняет инициализацию.

**Параметры**:
- `session` (ClientSession): Асинхронная сессия `aiohttp`.

**Возвращает**:
- `None`

**Как работает функция**:

1.  Проверяет, установлен ли `_auth_code`.
2.  Если `_auth_code` не установлен, вызывает `cls.initialize_auth_code(session)` для его инициализации.

**Примеры**:
```python
async with ClientSession() as session:
    await Liaobots.ensure_auth_code(session)
```