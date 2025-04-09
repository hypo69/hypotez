# Модуль `Grok.py`

## Обзор

Модуль предназначен для взаимодействия с Grok AI, предоставляя асинхронный интерфейс для работы с этой языковой моделью. Он включает поддержку аутентификации, создания бесед, отправки запросов и обработки ответов, включая текстовые и графические данные.

## Подробней

Этот модуль позволяет взаимодействовать с Grok AI, используя асинхронные запросы. Он поддерживает аутентификацию через cookie-файлы или URL для логина, создание новых бесед и отправку сообщений в существующих беседах. Модуль обрабатывает ответы от Grok AI, включая текстовые токены, изображения и заголовки, а также предоставляет информацию о процессе обдумывания (reasoning) модели.

## Классы

### `Conversation`

**Описание**: Класс представляет собой разговор (conversation) с Grok AI.

**Атрибуты**:

-   `conversation_id` (str): Уникальный идентификатор разговора.

### `Grok`

**Описание**: Класс предоставляет асинхронный интерфейс для взаимодействия с Grok AI.

**Наследует**:

-   `AsyncAuthedProvider`: Обеспечивает поддержку асинхронной аутентификации.
-   `ProviderModelMixin`: Предоставляет общие методы для работы с моделями провайдера.

**Атрибуты**:

-   `label` (str): Метка провайдера, `"Grok AI"`.
-   `url` (str): URL главной страницы Grok AI, `"https://grok.com"`.
-   `cookie_domain` (str): Домен для cookie-файлов, `".grok.com"`.
-   `assets_url` (str): URL для ресурсов Grok AI, `"https://assets.grok.com"`.
-   `conversation_url` (str): URL для управления беседами, `"https://grok.com/rest/app-chat/conversations"`.
-   `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации, `True`.
-   `working` (bool): Флаг, указывающий на работоспособность провайдера, `True`.
-   `default_model` (str): Модель, используемая по умолчанию, `"grok-3"`.
-   `models` (List[str]): Список поддерживаемых моделей, `["grok-3", "grok-3-thinking", "grok-2"]`.
-   `model_aliases` (Dict[str, str]): Псевдонимы моделей, `{"grok-3-r1": "grok-3-thinking"}`.

**Методы**:

-   `on_auth_async(cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator`: Асинхронный метод для аутентификации.
-   `_prepare_payload(model: str, message: str) -> Dict[str, Any]`: Асинхронный метод для подготовки payload запроса.
-   `create_authed(model: str, messages: Messages, auth_result: AuthResult, cookies: Cookies = None, return_conversation: bool = False, conversation: Conversation = None, **kwargs) -> AsyncResult`: Асинхронный метод для создания аутентифицированного запроса.

## Функции

### `on_auth_async`

```python
@classmethod
async def on_auth_async(cls, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator:
    """Асинхронно обрабатывает процесс аутентификации для Grok AI.

    Args:
        cookies (Cookies, optional): Cookie-файлы для аутентификации. Defaults to None.
        proxy (str, optional): Прокси-сервер для использования при аутентификации. Defaults to None.
        **kwargs: Дополнительные параметры.

    Yields:
        AuthResult: Результат аутентификации, содержащий cookie-файлы, информацию для имитации браузера и прокси.
        RequestLogin: Объект запроса на логин, если требуется URL для логина.

    Как работает функция:
    1. Проверяет наличие переданных cookie-файлов. Если они не предоставлены, пытается получить их из домена `.grok.com`.
    2. Если cookie-файлы найдены и содержат ключ "sso", возвращает результат аутентификации с этими cookie-файлами.
    3. Если cookie-файлы отсутствуют или не содержат "sso", запрашивает URL для логина из переменной окружения `G4F_LOGIN_URL` или использует пустую строку, создавая объект `RequestLogin`.
    4. После запроса URL для логина, пытается получить аргументы из безголового браузера, ожидая появления элемента `[href="/chat#private"]`.
    5. Возвращает результат аутентификации с аргументами, полученными из безголового браузера.

    A -- Проверка наличия cookies
    |   Yes
    B -- Проверка наличия "sso" в cookies
    |   Yes
    C -- Возврат AuthResult с cookies
    |   No
    D -- Запрос URL для логина
    |
    E -- Получение аргументов из безголового браузера
    |
    F -- Возврат AuthResult с аргументами

    Примеры:
        Пример 1: Использование с существующими cookies
        cookies = {"sso": "some_sso_token"}
        async for result in Grok.on_auth_async(cookies=cookies):
            print(result)

        Пример 2: Использование без cookies (требуется URL для логина)
        async for result in Grok.on_auth_async():
            print(result)
    """
    ...
```

### `_prepare_payload`

```python
    @classmethod
    async def _prepare_payload(cls, model: str, message: str) -> Dict[str, Any]:
        """Подготавливает payload для запроса к Grok AI.

        Args:
            model (str): Имя модели Grok AI.
            message (str): Сообщение для отправки.

        Returns:
            Dict[str, Any]: Словарь с данными payload.

        Как работает функция:
        1. Определяет, какую модель использовать: "grok-latest" для "grok-2" или "grok-3" для остальных.
        2. Создает словарь payload с различными параметрами, такими как `temporary`, `modelName`, `message`, `fileAttachments`, `imageAttachments` и другие.
        3. Устанавливает значения параметров, такие как `disableSearch`, `enableImageGeneration`, `returnImageBytes`, `returnRawGrokInXaiRequest`, `enableImageStreaming`, `imageGenerationCount`, `forceConcise`, `toolOverrides`, `enableSideBySide`, `isPreset`, `sendFinalMetadata`, `customInstructions`, `deepsearchPreset`, `isReasoning`.

        A -- Определение имени модели
        |
        B -- Создание payload
        |
        C -- Установка параметров
        |
        D -- Возврат payload

        Примеры:
            Пример 1: Подготовка payload для модели "grok-2"
            payload = await Grok._prepare_payload("grok-2", "Hello Grok!")
            print(payload)

            Пример 2: Подготовка payload для модели "grok-3"
            payload = await Grok._prepare_payload("grok-3", "Hello Grok!")
            print(payload)
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
        cookies: Cookies = None,
        return_conversation: bool = False,
        conversation: Conversation = None,
        **kwargs
    ) -> AsyncResult:
        """Создает аутентифицированный запрос к Grok AI и обрабатывает ответ.

        Args:
            model (str): Имя модели Grok AI.
            messages (Messages): Список сообщений для отправки.
            auth_result (AuthResult): Результат аутентификации.
            cookies (Cookies, optional): Cookie-файлы для запроса. Defaults to None.
            return_conversation (bool, optional): Флаг, указывающий, нужно ли возвращать объект Conversation. Defaults to False.
            conversation (Conversation, optional): Объект Conversation для продолжения беседы. Defaults to None.
            **kwargs: Дополнительные параметры.

        Yields:
            str: Текстовые токены из ответа Grok AI.
            ImagePreview: Превью изображений из ответа Grok AI.
            ImageResponse: Сгенерированные изображения из ответа Grok AI.
            TitleGeneration: Сгенерированный заголовок беседы из ответа Grok AI.
            Conversation: Объект Conversation, если `return_conversation` установлен в `True`.

        Как работает функция:
        1. Извлекает идентификатор беседы из объекта `conversation`, если он предоставлен.
        2. Форматирует сообщение из списка сообщений, используя `format_prompt` для новых бесед или `get_last_user_message` для продолжения существующих.
        3. Создает асинхронную сессию с использованием данных из `auth_result`.
        4. Подготавливает payload для запроса с использованием `_prepare_payload`.
        5. Определяет URL для запроса: создает новую беседу, если `conversation_id` отсутствует, или отправляет сообщение в существующую беседу.
        6. Отправляет POST-запрос к Grok AI с payload.
        7. Обрабатывает ответ построчно, извлекая текстовые токены, изображения и заголовок.
        8. Возвращает текстовые токены, превью изображений, сгенерированные изображения и сгенерированный заголовок.
        9. Если `return_conversation` установлен в `True` и `conversation_id` получен, возвращает объект `Conversation`.

        A -- Извлечение conversation_id
        |
        B -- Форматирование сообщения
        |
        C -- Создание асинхронной сессии
        |
        D -- Подготовка payload
        |
        E -- Определение URL запроса
        |
        F -- Отправка POST запроса
        |
        G -- Обработка ответа
        |
        H -- Возврат данных

        Примеры:
            Пример 1: Создание новой беседы
            auth_result = AuthResult(cookies={"sso": "some_sso_token"})
            messages = [{"role": "user", "content": "Hello Grok!"}]
            async for result in Grok.create_authed("grok-3", messages, auth_result):
                print(result)

            Пример 2: Продолжение существующей беседы
            auth_result = AuthResult(cookies={"sso": "some_sso_token"})
            messages = [{"role": "user", "content": "How are you?"}]
            conversation = Conversation(conversation_id="some_conversation_id")
            async for result in Grok.create_authed("grok-3", messages, auth_result, conversation=conversation):
                print(result)
        """
        ...