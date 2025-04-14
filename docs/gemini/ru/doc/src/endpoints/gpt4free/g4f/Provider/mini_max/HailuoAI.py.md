# Модуль `HailuoAI`

## Обзор

Модуль `HailuoAI` предоставляет асинхронный интерфейс для взаимодействия с сервисом Hailuo AI. Он реализует функциональность авторизации, создания бесед и обмена сообщениями с использованием асинхронных запросов. Модуль поддерживает потоковую передачу данных и предназначен для использования в проекте `hypotez`.

## Подробней

Модуль предназначен для интеграции с сервисом Hailuo AI через асинхронные запросы. Он обеспечивает авторизацию пользователя, создание и поддержание контекста беседы, а также потоковую передачу сообщений. В коде используется `aiohttp` для выполнения асинхронных HTTP-запросов и `FormData` для отправки данных формы. Для криптографических операций и формирования заголовков используется модуль `mini_max.crypt`.

## Классы

### `Conversation`

Описание: Класс представляет собой структуру для хранения информации о текущей беседе с Hailuo AI, включая токен авторизации, ID чата и ID персонажа.
**Атрибуты**:
- `token` (str): Токен авторизации для доступа к Hailuo AI.
- `chatID` (str): Идентификатор текущего чата.
- `characterID` (str, optional): Идентификатор персонажа, используемого в чате. По умолчанию равен 1.

### `HailuoAI`

Описание: Класс `HailuoAI` реализует асинхронный интерфейс для взаимодействия с сервисом Hailuo AI. Он предоставляет методы для авторизации, создания и ведения бесед, а также для обмена сообщениями.

**Наследует**:
- `AsyncAuthedProvider`: Предоставляет базовый функционал для асинхронной авторизации.
- `ProviderModelMixin`: Добавляет поддержку выбора модели.

**Атрибуты**:
- `label` (str): Метка, идентифицирующая провайдера ("Hailuo AI").
- `url` (str): URL сервиса Hailuo AI ("https://www.hailuo.ai").
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `use_nodriver` (bool): Флаг, указывающий на использование без драйвера (True).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи (True).
- `default_model` (str): Модель, используемая по умолчанию ("MiniMax").

**Методы**:
- `on_auth_async`: Асинхронный метод для выполнения авторизации.
- `create_authed`: Асинхронный метод для создания аутентифицированного запроса.

## Методы класса `HailuoAI`

### `on_auth_async`

```python
@classmethod
async def on_auth_async(cls, proxy: str = None, **kwargs) -> AsyncIterator:
    """
    Асинхронно выполняет процесс авторизации для Hailuo AI.

    Args:
        proxy (str, optional): URL прокси-сервера для использования при подключении. По умолчанию `None`.
        **kwargs: Дополнительные аргументы, которые могут быть переданы.

    Yields:
        RequestLogin: Если `login_url` найден, возвращает объект `RequestLogin` с URL для входа.
        AuthResult: Результат авторизации, содержащий необходимые параметры для дальнейшей работы.

    Raises:
        Exception: Если происходит ошибка во время авторизации.

    Как работает функция:
    - Проверяет наличие переменной окружения `G4F_LOGIN_URL`. Если она установлена, возвращает `RequestLogin` с URL для входа.
    - Получает параметры авторизации с использованием `get_args_from_nodriver` и `get_browser_callback`.
    - Возвращает `AuthResult` с результатами авторизации.

    Примеры:
        Пример 1: Успешная авторизация без прокси.
        >>> async for result in HailuoAI.on_auth_async():
        ...     print(result)

        Пример 2: Авторизация с использованием прокси.
        >>> async for result in HailuoAI.on_auth_async(proxy='http://proxy.example.com'):
        ...     print(result)
    """
    ...
```

### `create_authed`

```python
@classmethod
async def create_authed(
    cls,
    model: str,
    messages: Messages,
    auth_result: AuthResult,
    return_conversation: bool = False,
    conversation: Conversation = None,
    **kwargs
) -> AsyncResult:
    """
    Асинхронно создает аутентифицированный запрос к Hailuo AI.

    Args:
        model (str): Используемая модель.
        messages (Messages): Список сообщений для отправки.
        auth_result (AuthResult): Результат авторизации, содержащий необходимые параметры.
        return_conversation (bool, optional): Флаг, указывающий, нужно ли возвращать информацию о беседе. По умолчанию `False`.
        conversation (Conversation, optional): Объект `Conversation`, содержащий информацию о текущей беседе. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Yields:
        TitleGeneration: Если в ответе содержится заголовок чата, возвращает объект `TitleGeneration`.
        Conversation: Если `return_conversation` установлен в `True` и в ответе содержится ID чата, возвращает объект `Conversation`.
        str: Части контента сообщения, полученные в результате запроса.

    Raises:
        Exception: Если происходит ошибка во время создания запроса или обработки ответа.

    Как работает функция:
    - Извлекает параметры авторизации из `auth_result`.
    - Создает или обновляет данные формы (`form_data`) в зависимости от наличия существующей беседы (`conversation`).
    - Формирует заголовки запроса, включая токен авторизации и заголовок `yy`.
    - Отправляет POST-запрос к Hailuo AI с использованием `aiohttp.ClientSession`.
    - Обрабатывает потоковый ответ, извлекая события (`event`) и данные (`data`).
    - Возвращает заголовок чата, информацию о беседе и контент сообщения по частям.

    Примеры:
        Пример 1: Создание запроса без существующей беседы.
        >>> auth_result = AuthResult(token='example_token', path_and_query='/api/chat', timestamp='1234567890')
        >>> messages = [{'role': 'user', 'content': 'Hello'}]
        >>> async for result in HailuoAI.create_authed(model='MiniMax', messages=messages, auth_result=auth_result):
        ...     print(result)

        Пример 2: Создание запроса с существующей беседой.
        >>> auth_result = AuthResult(token='example_token', path_and_query='/api/chat', timestamp='1234567890')
        >>> messages = [{'role': 'user', 'content': 'How are you?'}]
        >>> conversation = Conversation(token='example_token', chatID='123')
        >>> async for result in HailuoAI.create_authed(model='MiniMax', messages=messages, auth_result=auth_result, conversation=conversation):
        ...     print(result)
    """
    ...