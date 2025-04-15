# Модуль для работы с Liaobots API

## Обзор

Модуль `Liaobots.py` предоставляет класс `Liaobots`, который позволяет взаимодействовать с API сервиса Liaobots для получения ответов от различных моделей искусственного интеллекта, таких как Claude, Gemini и GPT. Он поддерживает потоковую передачу ответов и предоставляет методы для проверки поддерживаемых моделей и создания асинхронных генераторов для взаимодействия с API.

## Подробнее

Этот модуль предназначен для интеграции с сервисом Liaobots, который предоставляет доступ к различным моделям ИИ. Модуль содержит информацию о доступных моделях и их параметрах, таких как максимальная длина и лимит токенов. Он также обеспечивает механизмы для аутентификации и установления соединения с API Liaobots.

## Классы

### `Liaobots`

**Описание**: Класс `Liaobots` реализует взаимодействие с API Liaobots. Он наследует функциональность асинхронного генератора и предоставляет методы для работы с моделями.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса Liaobots.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `default_model` (str): Модель, используемая по умолчанию (в данном случае `"gpt-4o-2024-08-06"`).
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.
- `_auth_code` (str): Код аутентификации.
- `_cookie_jar` (aiohttp.CookieJar): Cookie Jar для хранения cookie сессии.

**Принцип работы**:
Класс `Liaobots` использует асинхронные запросы для взаимодействия с API Liaobots. Он поддерживает различные модели ИИ, такие как Claude, Gemini и GPT. Класс предоставляет методы для проверки поддерживаемых моделей, создания асинхронных генераторов для получения ответов от API и аутентификации.

## Методы класса

### `is_supported`

```python
    @classmethod
    def is_supported(cls, model: str) -> bool:
        """
        Check if the given model is supported.
        """
        return model in models or model in cls.model_aliases
```

**Назначение**: Проверяет, поддерживается ли указанная модель.

**Параметры**:
- `model` (str): Название модели для проверки.

**Возвращает**:
- `bool`: `True`, если модель поддерживается, `False` в противном случае.

**Как работает функция**:
Функция проверяет, есть ли указанная модель в списке поддерживаемых моделей или в словаре псевдонимов моделей.

**Примеры**:
```python
    >>> Liaobots.is_supported("gpt-4o-2024-08-06")
    True

    >>> Liaobots.is_supported("unsupported-model")
    False
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
        ...
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API Liaobots.

**Параметры**:
- `model` (str): Название модели для использования.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `connector` (BaseConnector, optional): Aiohttp коннектор. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, такие как `system_message`.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий ответы от API.

**Как работает функция**:

1.  **Получение модели**: Функция получает фактическое название модели, используя псевдонимы, если необходимо.
2.  **Формирование заголовков**: Заголовки HTTP-запроса формируются с указанием referrer, origin и user-agent.
3.  **Создание сессии**: Создается асинхронная сессия `aiohttp.ClientSession` с заданными заголовками, cookie jar и коннектором.
4.  **Формирование данных**: Данные для запроса формируются в виде словаря, включающего ID разговора, модель, сообщения, ключ API и системное сообщение.
5.  **Аутентификация**: Если отсутствует код аутентификации (`cls._auth_code`), выполняется запрос на получение этого кода. Для этого отправляется POST-запрос к `https://liaobots.work/recaptcha/api/login` с фиктивным токеном.
6.  **Отправка запроса и получение ответа**:
    *   Отправляется POST-запрос к `https://liaobots.work/api/user` для получения актуального кода аутентификации.
    *   Полученный код сохраняется в `cls._auth_code`, и обновляется cookie jar сессии.
    *   Далее отправляется POST-запрос к `https://liaobots.work/api/chat` с данными разговора и кодом аутентификации в заголовке `x-auth-code`.
    *   Функция асинхронно читает ответ от сервера построчно.
    *   Если строка начинается с `b"data: "`, она декодируется из JSON и извлекается содержимое сообщения (`content`).
    *   Извлеченное содержимое передается в генератор.
7.  **Обработка ошибок**: Если в процессе выполнения возникают исключения, код пытается повторно получить код аутентификации, используя хардкодный `authcode` "jGDRFOqHcZKAo", и повторяет шаги отправки запроса и получения ответа.

**Внутренние функции**: Отсутствуют

**Примеры**:
```python
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    async def generator_example():
        async for message in Liaobots.create_async_generator(model="gpt-4o-2024-08-06", messages=messages):
            print(message)
    asyncio.run(generator_example())
```

### `initialize_auth_code`

```python
    @classmethod
    async def initialize_auth_code(cls, session: ClientSession) -> None:
        """
        Initialize the auth code by making the necessary login requests.
        """
        async with session.post(
            "https://liaobots.work/api/user",
            json={"authcode": "pTIQr4FTnVRfr"},
            verify_ssl=False
        ) as response:
            await raise_for_status(response)
            cls._auth_code = (await response.json(content_type=None))["authCode"]
            if not cls._auth_code:
                raise RuntimeError("Empty auth code")
            cls._cookie_jar = session.cookie_jar
```

**Назначение**: Инициализирует код аутентификации, выполняя необходимые запросы для входа в систему.

**Параметры**:
- `session` (ClientSession): Асинхронная сессия для выполнения HTTP-запросов.

**Как работает функция**:

1.  Отправляет POST-запрос к `https://liaobots.work/api/user` с жестко заданным кодом аутентификации `"pTIQr4FTnVRfr"`.
2.  Получает ответ от сервера и извлекает код аутентификации из JSON-ответа.
3.  Сохраняет полученный код в `cls._auth_code` и обновляет cookie jar сессии.
4.  Если код аутентификации не получен, вызывает исключение `RuntimeError`.

**Внутренние функции**: Отсутствуют

**Примеры**:
```python
    async def initialize_auth_code_example():
        async with ClientSession() as session:
            await Liaobots.initialize_auth_code(session)
            print(Liaobots._auth_code)

    asyncio.run(initialize_auth_code_example())
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

**Назначение**: Убеждается, что код аутентификации инициализирован, и выполняет инициализацию, если это необходимо.

**Параметры**:
- `session` (ClientSession): Асинхронная сессия для выполнения HTTP-запросов.

**Как работает функция**:

1.  Проверяет, инициализирован ли код аутентификации (`cls._auth_code`).
2.  Если код не инициализирован, вызывает функцию `initialize_auth_code` для его инициализации.

**Внутренние функции**: Отсутствуют

**Примеры**:
```python
    async def ensure_auth_code_example():
        async with ClientSession() as session:
            await Liaobots.ensure_auth_code(session)
            print(Liaobots._auth_code)

    asyncio.run(ensure_auth_code_example())
```

## Параметры класса

- `url` (str): URL сервиса Liaobots.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `default_model` (str): Модель, используемая по умолчанию (в данном случае `"gpt-4o-2024-08-06"`).
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.
- `_auth_code` (str): Код аутентификации.
- `_cookie_jar` (aiohttp.CookieJar): Cookie Jar для хранения cookie сессии.