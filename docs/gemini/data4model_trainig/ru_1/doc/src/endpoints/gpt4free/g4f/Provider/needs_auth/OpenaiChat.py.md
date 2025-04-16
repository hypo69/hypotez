# Модуль OpenaiChat

## Обзор

Модуль `OpenaiChat` предоставляет класс `OpenaiChat`, который используется для создания и управления диалогами с сервисом чата OpenAI.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с OpenAI ChatGPT. Он включает в себя функциональность для аутентификации, загрузки изображений, создания сообщений, итерации по ответам и синтеза речи. Модуль поддерживает работу через прокси, установку таймаутов для запросов и автоматическое продолжение диалогов.

## Классы

### `OpenaiChat`

**Описание**: Класс для создания и управления диалогами с сервисом чата OpenAI.

**Наследует**:
- `AsyncAuthedProvider`: Обеспечивает асинхронную аутентификацию.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("OpenAI ChatGPT").
- `url` (str): URL сервиса ("https://chatgpt.com").
- `working` (bool): Флаг, указывающий, что провайдер работает (True).
- `use_nodriver` (bool): Флаг, указывающий на использование nodriver (True).
- `supports_gpt_4` (bool): Флаг, указывающий на поддержку GPT-4 (True).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (True).
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (True).
- `default_model` (str): Модель, используемая по умолчанию (default_model).
- `default_image_model` (str): Модель для генерации изображений, используемая по умолчанию (default_image_model).
- `image_models` (list): Список моделей для генерации изображений (image_models).
- `vision_models` (list): Список моделей для анализа изображений (text_models).
- `models` (list): Список поддерживаемых моделей (models).
- `synthesize_content_type` (str): Тип контента для синтеза речи ("audio/aac").
- `request_config` (RequestConfig): Объект конфигурации запросов.
- `_api_key` (str): Ключ API для аутентификации.
- `_headers` (dict): Заголовки запросов.
- `_cookies` (Cookies): Куки для запросов.
- `_expires` (int): Время истечения срока действия ключа API.

**Методы**:
- `on_auth_async`: Асинхронный метод для аутентификации.
- `upload_images`: Асинхронный метод для загрузки изображений.
- `create_messages`: Метод для создания списка сообщений.
- `get_generated_image`: Асинхронный метод для получения сгенерированного изображения.
- `create_authed`: Асинхронный метод для создания аутентифицированного диалога.
- `iter_messages_line`: Асинхронный метод для итерации по строкам сообщений.
- `synthesize`: Асинхронный метод для синтеза речи.
- `login`: Асинхронный метод для аутентификации и получения необходимых данных.
- `nodriver_auth`: Асинхронный метод для аутентификации с использованием nodriver.
- `get_default_headers`: Статический метод для получения заголовков по умолчанию.
- `_create_request_args`: Метод для создания аргументов запроса.
- `_update_request_args`: Метод для обновления аргументов запроса.
- `_set_api_key`: Метод для установки ключа API.
- `_update_cookie_header`: Метод для обновления заголовка cookie.

### `Conversation`

**Описание**: Класс для инкапсуляции полей ответа.

**Наследует**:
- `JsonConversation`: Предоставляет функциональность для работы с JSON-ответами.

**Атрибуты**:
- `conversation_id` (str): ID разговора.
- `message_id` (str): ID сообщения.
- `finish_reason` (str): Причина завершения разговора.
- `is_recipient` (bool): Является ли получателем.
- `parent_message_id` (str): ID родительского сообщения.
- `user_id` (str): ID пользователя.
- `is_thinking` (bool): Флаг, указывающий, что бот "думает".

## Методы класса `OpenaiChat`

### `on_auth_async`

```python
    @classmethod
    async def on_auth_async(cls, proxy: str = None, **kwargs) -> AsyncIterator:
        """
        Асинхронный метод для аутентификации.

        Args:
            proxy (str, optional): Прокси для использования. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Yields:
            AsyncResult: Асинхронные результаты аутентификации.
        """
        ...
```
**Назначение**:
Асинхронный метод `on_auth_async` выполняет аутентификацию, необходимую для доступа к сервису OpenAI ChatGPT. Он является асинхронным генератором, который предоставляет результаты аутентификации в виде чанков.

**Как работает функция**:
1. Вызывает метод `cls.login` для выполнения процесса входа в систему.
2. Передает прокси-сервер, если он указан.
3. Возвращает чанки результатов аутентификации.
4. После завершения процесса входа возвращает объект `AuthResult`, содержащий ключ API, куки, заголовки, время истечения срока действия, proof_token и turnstile_token.

**Примеры**:

```python
async for chunk in OpenaiChat.on_auth_async(proxy='some_proxy'):
    print(chunk)
```

### `upload_images`

```python
    @classmethod
    async def upload_images(
        cls,
        session: StreamSession,
        auth_result: AuthResult,
        media: MediaListType,
    ) -> ImageRequest:
        """
        Загружает изображение на сервис и получает URL для скачивания.

        Args:
            session (StreamSession): Объект StreamSession для выполнения запросов.
            auth_result (AuthResult): Результат аутентификации.
            media (MediaListType): Изображения для загрузки (PIL Image или bytes).

        Returns:
            ImageRequest: Объект ImageRequest, содержащий URL для скачивания, имя файла и другие данные.
        """
        ...
```

**Назначение**:
Асинхронный метод `upload_images` предназначен для загрузки изображений в сервис OpenAI и получения URL-адресов для скачивания этих изображений. Это необходимо для включения изображений в диалоги с чат-ботом.

**Как работает функция**:
1. Определяет внутреннюю асинхронную функцию `upload_image`, которая выполняет фактическую загрузку одного изображения.
2. Преобразует изображение в формат bytes и получает его расширение.
3. Создает JSON-данные, содержащие информацию об изображении (имя, размер, use_case).
4. Отправляет POST-запрос к сервису для создания файла и получает данные об изображении, включая URL для загрузки.
5. Отправляет PUT-запрос для загрузки байтов изображения по полученному URL.
6. Отправляет POST-запрос для получения URL-адреса скачивания загруженного изображения.
7. Возвращает объект `ImageRequest`, содержащий информацию об изображении.

**Примеры**:

```python
media = [(image_bytes, 'example.png')]
image_requests = await OpenaiChat.upload_images(session, auth_result, media)
```

### `create_messages`

```python
    @classmethod
    def create_messages(cls, messages: Messages, image_requests: ImageRequest = None, system_hints: list = None):
        """
        Создает список сообщений для пользовательского ввода.

        Args:
            messages (Messages): Список предыдущих сообщений.
            image_requests (ImageRequest, optional): Объект ответа изображения, если есть. По умолчанию `None`.
            system_hints (list, optional): Системные подсказки. По умолчанию `None`.

        Returns:
            list: Список сообщений с пользовательским вводом и изображением, если есть.
        """
        ...
```

**Назначение**:
Метод `create_messages` создает список сообщений, который будет отправлен в OpenAI. Он обрабатывает пользовательский ввод, а также добавляет информацию об изображениях, если они есть.

**Как работает функция**:
1. Преобразует входные сообщения в формат, ожидаемый OpenAI.
2. Если предоставлены `image_requests`, добавляет информацию об изображениях в последнее сообщение пользователя. Это включает в себя изменение типа контента на "multimodal_text" и добавление метаданных об изображениях.
3. Добавляет системные подсказки, если они предоставлены.

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello, bot!"}]
created_messages = OpenaiChat.create_messages(messages)
```

### `get_generated_image`

```python
    @classmethod
    async def get_generated_image(cls, session: StreamSession, auth_result: AuthResult, element: dict, prompt: str = None) -> ImageResponse:
        """
        Получает сгенерированное изображение.

        Args:
            session (StreamSession): Объект StreamSession для выполнения запросов.
            auth_result (AuthResult): Результат аутентификации.
            element (dict): Элемент, содержащий информацию об изображении.
            prompt (str, optional): Подсказка для генерации изображения. По умолчанию `None`.

        Returns:
            ImageResponse: Объект ImageResponse, содержащий URL для скачивания и подсказку.
        """
        ...
```

**Назначение**:
Асинхронный метод `get_generated_image` используется для получения сгенерированных изображений из OpenAI.

**Как работает функция**:
1. Извлекает подсказку и file_id из элемента.
2. Отправляет GET-запрос для скачивания изображения.
3. Возвращает объект `ImageResponse`, содержащий URL для скачивания и подсказку.

**Примеры**:

```python
image_response = await OpenaiChat.get_generated_image(session, auth_result, element)
```

### `create_authed`

```python
    @classmethod
    async def create_authed(
        cls,
        model: str,
        messages: Messages,
        auth_result: AuthResult,
        proxy: str = None,
        timeout: int = 180,
        auto_continue: bool = False,
        action: str = "next",
        conversation: Conversation = None,
        media: MediaListType = None,
        return_conversation: bool = False,
        web_search: bool = False,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для разговора.

        Args:
            model (str): Имя модели.
            messages (Messages): Список предыдущих сообщений.
            auth_result (AuthResult): Результат аутентификации.
            proxy (str, optional): Прокси для использования. По умолчанию `None`.
            timeout (int, optional): Таймаут для запросов. По умолчанию 180.
            auto_continue (bool, optional): Флаг для автоматического продолжения разговора. По умолчанию `False`.
            action (str, optional): Тип действия ('next', 'continue', 'variant'). По умолчанию "next".
            conversation (Conversation, optional): Объект Conversation. По умолчанию `None`.
            media (MediaListType, optional): Изображения для включения в разговор. По умолчанию `None`.
            return_conversation (bool, optional): Флаг для включения полей ответа в вывод. По умолчанию `False`.
            web_search (bool, optional): Флаг для включения веб-поиска. По умолчанию `False`.
            **kwargs: Дополнительные параметры.

        Yields:
            AsyncResult: Асинхронные результаты от генератора.
        """
        ...
```

**Назначение**:
Асинхронный метод `create_authed` создает асинхронный генератор для ведения диалога с OpenAI. Он обеспечивает аутентификацию, загрузку изображений, отправку сообщений и обработку ответов.

**Как работает функция**:
1. Инициализирует `StreamSession` для выполнения запросов.
2. Загружает изображения, если они предоставлены.
3. Определяет, нужно ли выполнять аутентификацию, и выполняет её, если необходимо.
4. Отправляет POST-запросы для получения ответов от OpenAI.
5. Итерирует по ответам и извлекает информацию о сообщениях, изображениях и других данных.
6. Возвращает асинхронные результаты в виде генератора.

**Примеры**:

```python
async for chunk in OpenaiChat.create_authed(model='gpt-4', messages=messages, auth_result=auth_result):
    print(chunk)
```

### `iter_messages_line`

```python
    @classmethod
    async def iter_messages_line(cls, session: StreamSession, auth_result: AuthResult, line: bytes, fields: Conversation, sources: Sources) -> AsyncIterator:
        """
        Итерирует по строкам сообщений.

        Args:
            session (StreamSession): Объект StreamSession для выполнения запросов.
            auth_result (AuthResult): Результат аутентификации.
            line (bytes): Строка сообщения.
            fields (Conversation): Объект Conversation для хранения информации о разговоре.
            sources (Sources): Объект Sources для хранения источников.

        Yields:
            str | ImageResponse: Части сообщения или объект ImageResponse.
        """
        ...
```

**Назначение**:
Асинхронный метод `iter_messages_line` обрабатывает каждую строку ответа от OpenAI и извлекает из неё полезную информацию, такую как текст, изображения и источники.

**Как работает функция**:
1. Проверяет, начинается ли строка с "data: ".
2. Загружает JSON из строки.
3. Извлекает различные типы данных из JSON, такие как текст, изображения, источники и метаданные.
4. Возвращает части сообщения или объекты `ImageResponse`.

**Примеры**:

```python
async for chunk in OpenaiChat.iter_messages_line(session, auth_result, line, conversation, sources):
    print(chunk)
```

### `synthesize`

```python
    @classmethod
    async def synthesize(cls, params: dict) -> AsyncIterator[bytes]:
        """
        Синтезирует речь.

        Args:
            params (dict): Параметры для синтеза речи.

        Yields:
            bytes: Части синтезированной речи.
        """
        ...
```

**Назначение**:
Асинхронный метод `synthesize` используется для синтеза речи на основе заданных параметров.

**Как работает функция**:
1. Выполняет вход в систему.
2. Отправляет GET-запрос для синтеза речи.
3. Итерирует по частям ответа и возвращает их.

**Примеры**:

```python
async for chunk in OpenaiChat.synthesize(params):
    print(chunk)
```

### `login`

```python
    @classmethod
    async def login(
        cls,
        proxy: str = None,
        api_key: str = None,
        proof_token: str = None,
        cookies: Cookies = None,
        headers: dict = None,
        **kwargs
    ) -> AsyncIterator:
        """
        Выполняет аутентификацию и получает необходимые данные.

        Args:
            proxy (str, optional): Прокси для использования. По умолчанию `None`.
            api_key (str, optional): Ключ API. По умолчанию `None`.
            proof_token (str, optional): Proof token. По умолчанию `None`.
            cookies (Cookies, optional): Куки. По умолчанию `None`.
            headers (dict, optional): Заголовки. По умолчанию `None`.

        Yields:
            RequestLogin: Объект RequestLogin, если требуется логин.
        """
        ...
```

**Назначение**:
Асинхронный метод `login` выполняет аутентификацию и подготавливает необходимые данные для дальнейшей работы с OpenAI.

**Как работает функция**:
1. Проверяет, истек ли срок действия текущего ключа API.
2. Если предоставлены новые куки, proof_token или ключ API, обновляет соответствующие атрибуты класса.
3. Пытается получить конфигурацию запроса из HAR-файла.
4. Если не удается получить конфигурацию из HAR-файла и включен `has_nodriver`, выполняет аутентификацию с использованием `nodriver`.

**Примеры**:

```python
async for chunk in OpenaiChat.login(api_key='your_api_key'):
    print(chunk)
```

### `nodriver_auth`

```python
    @classmethod
    async def nodriver_auth(cls, proxy: str = None):
        """
        Выполняет аутентификацию с использованием nodriver.

        Args:
            proxy (str, optional): Прокси для использования. По умолчанию `None`.
        """
        ...
```

**Назначение**:
Асинхронный метод `nodriver_auth` выполняет аутентификацию с использованием безголового браузера `nodriver`. Это альтернативный способ аутентификации, который может быть использован, если стандартные методы не работают.

**Как работает функция**:
1. Запускает безголовый браузер с использованием `get_nodriver`.
2. Перехватывает сетевые запросы для получения кук, заголовков и ключа API.
3. Выполняет действия на странице, такие как ввод текста и нажатие кнопки отправки.
4. Извлекает ключ API из ответа.
5. Обновляет атрибуты класса с полученными данными.
6. Останавливает браузер.

**Примеры**:

```python
await OpenaiChat.nodriver_auth(proxy='some_proxy')
```

### `get_default_headers`

```python
    @staticmethod
    def get_default_headers() -> Dict[str, str]:
        """
        Возвращает заголовки по умолчанию.

        Returns:
            Dict[str, str]: Словарь заголовков по умолчанию.
        """
        ...
```

**Назначение**:
Статический метод `get_default_headers` возвращает словарь с заголовками HTTP по умолчанию, используемыми для взаимодействия с API OpenAI.

**Как работает функция**:
Метод создает и возвращает словарь, содержащий общие заголовки, такие как `accept`, `accept-encoding`, `user-agent` и `content-type`.

**Примеры**:

```python
headers = OpenaiChat.get_default_headers()
print(headers)
```

### `_create_request_args`

```python
    @classmethod
    def _create_request_args(cls, cookies: Cookies = None, headers: dict = None, user_agent: str = None):
        """
        Создает аргументы запроса.

        Args:
            cookies (Cookies, optional): Куки. По умолчанию `None`.
            headers (dict, optional): Заголовки. По умолчанию `None`.
            user_agent (str, optional): User-agent. По умолчанию `None`.
        """
        ...
```

**Назначение**:
Метод `_create_request_args` создает и настраивает заголовки и куки для последующих запросов к API OpenAI.

**Как работает функция**:
Метод объединяет переданные заголовки с заголовками по умолчанию, устанавливает User-Agent, если он передан, и обновляет куки.

**Примеры**:

```python
OpenaiChat._create_request_args(cookies={'cookie1': 'value1'}, user_agent='CustomUserAgent')
```

### `_update_request_args`

```python
    @classmethod
    def _update_request_args(cls, auth_result: AuthResult, session: StreamSession):
        """
        Обновляет аргументы запроса.

        Args:
            auth_result (AuthResult): Результат аутентификации.
            session (StreamSession): Объект StreamSession для выполнения запросов.
        """
        ...
```

**Назначение**:
Метод `_update_request_args` обновляет куки в текущем сеансе на основе данных аутентификации.

**Как работает функция**:
Метод итерирует по кукам в `session.cookie_jar` и обновляет их в `auth_result.cookies`. Затем обновляет локальные куки (`cls._cookies`) и заголовок cookie.

**Примеры**:

```python
OpenaiChat._update_request_args(auth_result, session)
```

### `_set_api_key`

```python
    @classmethod
    def _set_api_key(cls, api_key: str):
        """
        Устанавливает ключ API.

        Args:
            api_key (str): Ключ API.

        Returns:
            bool: True, если ключ API установлен успешно, иначе False.
        """
        ...
```

**Назначение**:
Метод `_set_api_key` устанавливает ключ API и проверяет срок его действия.

**Как работает функция**:
Метод декодирует ключ API, извлекает время истечения срока действия, проверяет, не истек ли срок действия ключа, и устанавливает ключ API и заголовок авторизации.

**Примеры**:

```python
if OpenaiChat._set_api_key('valid_api_key'):
    print('API key установлен')
```

### `_update_cookie_header`

```python
    @classmethod
    def _update_cookie_header(cls):
        """
        Обновляет заголовок cookie.
        """
        ...
```

**Назначение**:
Метод `_update_cookie_header` обновляет заголовок cookie в заголовках запроса на основе текущих кук.

**Как работает функция**:
Метод форматирует куки и устанавливает заголовок cookie в `cls._headers`.

**Примеры**:

```python
OpenaiChat._update_cookie_header()
```

## Методы класса `Conversation`

### `__init__`

```python
    def __init__(self, conversation_id: str = None, message_id: str = None, user_id: str = None, finish_reason: str = None, parent_message_id: str = None, is_thinking: bool = False):
        self.conversation_id = conversation_id
        self.message_id = message_id
        self.finish_reason = finish_reason
        self.is_recipient = False
        self.parent_message_id = message_id if parent_message_id is None else parent_message_id
        self.user_id = user_id
        self.is_thinking = is_thinking
```

**Назначение**:
Метод `__init__` инициализирует объект класса `Conversation`.

**Параметры**:
- `conversation_id` (str, optional): ID разговора. По умолчанию `None`.
- `message_id` (str, optional): ID сообщения. По умолчанию `None`.
- `user_id` (str, optional): ID пользователя. По умолчанию `None`.
- `finish_reason` (str, optional): Причина завершения разговора. По умолчанию `None`.
- `parent_message_id` (str, optional): ID родительского сообщения. По умолчанию `None`.
- `is_thinking` (bool, optional): Флаг, указывающий, что бот "думает". По умолчанию `False`.

## Функции

### `get_cookies`

```python
def get_cookies(
    urls: Optional[Iterator[str]] = None
) -> Generator[Dict, Dict, Dict[str, str]]:
    """
    Получает куки для указанных URL.

    Args:
        urls (Optional[Iterator[str]], optional): Итератор URL. По умолчанию `None`.

    Yields:
        Generator[Dict, Dict, Dict[str, str]]: Генератор словарей с куками.
    """
    ...
```

**Назначение**:
Функция `get_cookies` используется для получения кук для указанных URL-адресов с использованием протокола Chrome DevTools Protocol (CDP).

**Как работает функция**:
1. Формирует словарь параметров для CDP команды `Network.getCookies`.
2. Отправляет команду `Network.getCookies` и получает JSON-ответ.
3. Извлекает куки из JSON-ответа и возвращает их в виде словаря.

**Примеры**:

```python
cookies = get_cookies(['https://chatgpt.com'])
print(cookies)