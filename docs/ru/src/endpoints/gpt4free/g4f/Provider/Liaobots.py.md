# Модуль `Liaobots`

## Обзор

Модуль `Liaobots` предоставляет асинхронный генератор для взаимодействия с различными моделями, предоставляемыми сервисом `liaobots.site`. Он поддерживает сохранение истории сообщений и использование системных сообщений. Модуль включает в себя поддержку моделей `Claude`, `DeepSeek`, `Gemini` и `GPT`, а также предоставляет возможность выбора модели и установки параметров подключения.

## Подробней

Модуль предназначен для интеграции с сервисом `liaobots.site` для получения ответов от различных AI-моделей. Он использует асинхронные запросы для взаимодействия с API сервиса и предоставляет удобный интерфейс для выбора модели, передачи сообщений и получения результатов в виде асинхронного генератора.

## Классы

### `Liaobots`

**Описание**: Класс `Liaobots` является поставщиком асинхронного генератора, который взаимодействует с API `liaobots.site`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса `liaobots.site`.
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии.
- `supports_message_history` (bool): Указывает на поддержку истории сообщений.
- `supports_system_message` (bool): Указывает на поддержку системных сообщений.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-2024-08-06`).
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.
- `_auth_code` (str): Код аутентификации для доступа к API.
- `_cookie_jar`: Объект для хранения cookie.

**Методы**:
- `is_supported(model: str) -> bool`: Проверяет, поддерживается ли указанная модель.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, connector: BaseConnector = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от API.
- `initialize_auth_code(session: ClientSession) -> None`: Инициализирует код аутентификации.
- `ensure_auth_code(session: ClientSession) -> None`: Обеспечивает инициализацию кода аутентификации, если он еще не установлен.

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

**Назначение**: Проверяет, поддерживается ли указанная модель провайдером `Liaobots`.

**Параметры**:
- `model` (str): Идентификатор модели, которую необходимо проверить.

**Возвращает**:
- `bool`: `True`, если модель поддерживается, иначе `False`.

**Как работает функция**:
1. Функция `is_supported` принимает на вход строковый идентификатор модели (`model`).
2. Проверяет, присутствует ли `model` в списке поддерживаемых моделей (`models`) или в словаре псевдонимов моделей (`model_aliases`) класса `Liaobots`.
3. Возвращает `True`, если модель найдена в одном из этих мест, и `False` в противном случае.

**ASCII flowchart**:

```
    Модель -> Проверка в списке models -> Проверка в словаре model_aliases -> Возврат True/False
```

**Примеры**:

```python
Liaobots.is_supported("gpt-4o-2024-08-06")  # Вернет True
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
        ...
```

**Назначение**: Создает асинхронный генератор для получения ответов от API `liaobots.site`.

**Параметры**:
- `model` (str): Идентификатор модели, которую необходимо использовать.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `connector` (BaseConnector, optional): Объект коннектора AIOHTTP. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры, такие как `system_message`.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий ответы от API.

**Как работает функция**:

1.  **Получение модели**: Функция `create_async_generator` принимает идентификатор модели (`model`), сообщения (`messages`), прокси (`proxy`) и коннектор (`connector`) в качестве аргументов. Сначала она получает фактическое имя модели, используя `cls.get_model(model)`.
2.  **Формирование заголовков**: Функция задает заголовки HTTP-запроса, включая `referer`, `origin` и `user-agent`.
3.  **Создание сессии**: Создается асинхронная сессия с использованием `aiohttp.ClientSession` с заданными заголовками, файлами cookie и коннектором. Коннектор создается с использованием функции `get_connector` из модуля `helper`.
4.  **Формирование данных**: Формируются данные для отправки в теле запроса. Данные включают `conversationId` (случайный UUID), `model` (информация о модели из словаря `models`), `messages` и `prompt` (системное сообщение).
5.  **Аутентификация (если необходимо)**: Если `cls._auth_code` не установлен, выполняется запрос к `https://liaobots.work/recaptcha/api/login` для получения кода аутентификации.
6.  **Отправка запроса и получение ответа**: Выполняется POST-запрос к `https://liaobots.work/api/chat` с данными и заголовком `x-auth-code`. Функция асинхронно итерируется по строкам в ответе, извлекая содержимое JSON из строк, начинающихся с `data: `.
7.  **Обработка ошибок**: Если происходит ошибка, функция пытается повторно аутентифицироваться с другим кодом аутентификации (`jGDRFOqHcZKAo`) и повторяет запрос.
8.  **Генерация результатов**: Функция возвращает асинхронный генератор, который выдает извлеченное содержимое из ответов API.

**ASCII flowchart**:

```
    Model, Messages, Proxy, Connector -> Получение имени модели -> Формирование заголовков ->
    Создание асинхронной сессии -> Формирование данных -> Проверка auth_code ->
    Аутентификация (если необходимо) -> POST запрос к API -> Обработка ответа ->
    Генерация результатов (content)
```

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for message in Liaobots.create_async_generator(model="gpt-4o-2024-08-06", messages=messages):
    print(message)
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

**Назначение**: Инициализирует код аутентификации, выполняя необходимые запросы для входа.

**Параметры**:
- `session` (ClientSession): Асинхронная сессия AIOHTTP.

**Возвращает**:
- `None`

**Как работает функция**:
1. Функция `initialize_auth_code` принимает асинхронную сессию (`session`) в качестве аргумента.
2. Выполняет POST-запрос к `https://liaobots.work/api/user` с кодом аутентификации `pTIQr4FTnVRfr`.
3. Проверяет статус ответа, используя `await raise_for_status(response)`.
4. Извлекает код аутентификации из JSON-ответа и сохраняет его в `cls._auth_code`.
5. Если код аутентификации пустой, вызывает исключение `RuntimeError`.
6. Сохраняет cookie из сессии в `cls._cookie_jar`.

**ASCII flowchart**:

```
    Session -> POST запрос к API -> Проверка статуса ответа -> Извлечение authCode ->
    Проверка на пустоту authCode -> Сохранение authCode и cookie_jar
```

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
        if not cls._auth_code:
            await cls.initialize_auth_code(session)
```

**Назначение**: Обеспечивает инициализацию кода аутентификации, выполняя инициализацию, если он еще не установлен.

**Параметры**:
- `session` (ClientSession): Асинхронная сессия AIOHTTP.

**Возвращает**:
- `None`

**Как работает функция**:
1. Функция `ensure_auth_code` принимает асинхронную сессию (`session`) в качестве аргумента.
2. Проверяет, установлен ли `cls._auth_code`.
3. Если `cls._auth_code` не установлен, вызывает функцию `cls.initialize_auth_code(session)` для его инициализации.

**ASCII flowchart**:

```
    Session -> Проверка auth_code -> Инициализация auth_code (если необходимо)
```

**Примеры**:

```python
async with ClientSession() as session:
    await Liaobots.ensure_auth_code(session)