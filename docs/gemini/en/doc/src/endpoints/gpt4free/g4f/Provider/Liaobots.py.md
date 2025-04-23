# Модуль: Liaobots

## Обзор

Модуль `Liaobots` предоставляет асинхронный интерфейс для взаимодействия с провайдером Liaobots, который поддерживает различные модели, включая `Claude`, `DeepSeek`, `Gemini` и `GPT`. Он включает в себя функциональность для работы с историей сообщений и системными сообщениями. Модуль использует `aiohttp` для выполнения асинхронных HTTP-запросов.

## Более подробно

Модуль предназначен для интеграции с платформой Liaobots, предоставляя доступ к различным моделям искусственного интеллекта. Он поддерживает настройку моделей, прокси и аутентификацию через специальные коды авторизации. Модуль также обрабатывает ошибки и повторные запросы для обеспечения стабильной работы.

## Классы

### `Liaobots`

**Описание**: Класс `Liaobots` предоставляет асинхронный генератор для взаимодействия с API Liaobots.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Добавляет функциональность для работы с моделями провайдера.

**Атрибуты**:
- `url` (str): URL-адрес Liaobots.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `default_model` (str): Модель, используемая по умолчанию ("gpt-4o-2024-08-06").
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей для упрощения использования.
- `_auth_code` (str): Код авторизации для доступа к API.
- `_cookie_jar`: Cookie Jar для хранения cookie сессии.

**Принцип работы**:
Класс использует `aiohttp.ClientSession` для отправки асинхронных запросов к API Liaobots. Он поддерживает различные модели и псевдонимы моделей, а также обрабатывает аутентификацию через коды авторизации. В случае ошибки выполняется повторная попытка с другим кодом авторизации.

**Методы**:

- `is_supported(model: str) -> bool`
- `create_async_generator(model: str, messages: Messages, proxy: str = None, connector: BaseConnector = None, **kwargs) -> AsyncResult`
- `initialize_auth_code(session: ClientSession) -> None`
- `ensure_auth_code(session: ClientSession) -> None`

## Методы класса

### `is_supported`

```python
    @classmethod
    def is_supported(cls, model: str) -> bool:
        """
        Проверяет, поддерживается ли указанная модель.

        Args:
            model (str): Имя модели для проверки.

        Returns:
            bool: `True`, если модель поддерживается, иначе `False`.
        """
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
        Создает асинхронный генератор для взаимодействия с API Liaobots.

        Args:
            model (str): Имя модели для использования.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): URL прокси-сервера. Defaults to None.
            connector (BaseConnector, optional): Пользовательский коннектор aiohttp. Defaults to None.
            **kwargs: Дополнительные параметры, такие как `system_message`.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий результаты из API.
        """
```

**Как работает функция**:
1. **Извлекает модель**: Сначала функция извлекает правильное имя модели, используя `cls.get_model(model)`, чтобы учесть псевдонимы моделей.
2. **Определяет заголовки**: Определяются необходимые HTTP-заголовки, включая `referer`, `origin` и `user-agent`.
3. **Создает сессию**: Функция создает асинхронную сессию `aiohttp.ClientSession` с заданными заголовками, файлом cookie и коннектором.
4. **Подготавливает данные**: Создается словарь `data`, содержащий `conversationId`, `model`, `messages`, `key` и `prompt` (системное сообщение).
5. **Аутентификация**: Если `cls._auth_code` не установлен, функция пытается получить его, отправив запрос к `https://liaobots.work/recaptcha/api/login`.
6. **Отправляет сообщения и получает ответы**: Функция отправляет POST-запрос к `https://liaobots.work/api/chat` с данными и заголовком `x-auth-code`. Затем она перебирает строки в ответе и извлекает содержимое JSON, возвращая его через генератор.
7. **Обработка ошибок**: Если происходит ошибка, функция повторяет попытку с другим кодом авторизации.

```python
async with session.post(
                    "https://liaobots.work/api/user",
                    json={"authcode": "jGDRFOqHcZKAo"},
                    verify_ssl=False
                ) as response:
                    await raise_for_status(response)
                    cls._auth_code = (await response.json(content_type=None))["authCode"]
                    if not cls._auth_code:
                        raise RuntimeError("Empty auth code")
                    cls._cookie_jar = session.cookie_jar
```

8. **Безопасность**: `verify_ssl=False` указывает на отключение проверки SSL-сертификата, что не рекомендуется в производственной среде.

**Примеры**:

```python
# Пример вызова функции create_async_generator
model = "gpt-4o-2024-08-06"
messages = [{"role": "user", "content": "Привет!"}]
async for message in Liaobots.create_async_generator(model=model, messages=messages):
    print(message)
```

### `initialize_auth_code`

```python
    @classmethod
    async def initialize_auth_code(cls, session: ClientSession) -> None:
        """
        Инициализирует код авторизации, выполняя необходимые запросы для входа в систему.

        Args:
            session (ClientSession): Асинхронная сессия для выполнения HTTP-запросов.
        """
```

**Как работает функция**:
1. Отправляет POST-запрос к `https://liaobots.work/api/user` с фиксированным кодом авторизации.
2. Извлекает код авторизации из ответа JSON.
3. Устанавливает `cls._auth_code` и `cls._cookie_jar`.

**Примеры**:

```python
# Пример вызова функции initialize_auth_code
async with ClientSession() as session:
    await Liaobots.initialize_auth_code(session)
```

### `ensure_auth_code`

```python
    @classmethod
    async def ensure_auth_code(cls, session: ClientSession) -> None:
        """
        Проверяет, инициализирован ли код авторизации, и выполняет инициализацию, если это необходимо.

        Args:
            session (ClientSession): Асинхронная сессия для выполнения HTTP-запросов.
        """
```

**Как работает функция**:
1. Проверяет, установлен ли `cls._auth_code`.
2. Если `cls._auth_code` не установлен, вызывает `cls.initialize_auth_code(session)` для его инициализации.

**Примеры**:

```python
# Пример вызова функции ensure_auth_code
async with ClientSession() as session:
    await Liaobots.ensure_auth_code(session)