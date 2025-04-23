# Модуль Gemini

## Обзор

Модуль `Gemini` предоставляет асинхронный интерфейс для взаимодействия с моделями Google Gemini. Он включает в себя поддержку текстовых и визуальных запросов, а также механизм автоматического обновления файлов cookie для поддержания аутентификации.

## Более подробно

Этот модуль предназначен для работы с API Google Gemini. Он поддерживает отправку текстовых и визуальных запросов, а также автоматически обновляет файлы cookie для поддержания аутентификации. В модуле реализованы функции для загрузки изображений, обработки ответов и синтеза речи.

## Содержание

- [Классы](#классы)
    - [Gemini](#класс-gemini)
    - [Conversation](#класс-conversation)
- [Функции](#функции)
    - [iter_filter_base64](#функция-iter_filter_base64)
    - [iter_base64_decode](#функция-iter_base64_decode)
    - [rotate_1psidts](#функция-rotate_1psidts)

## Классы

### `Gemini`

**Описание**:
Класс `Gemini` предоставляет асинхронный генератор для взаимодействия с моделями Google Gemini.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера (Google Gemini).
- `url` (str): URL для доступа к Gemini.
- `needs_auth` (bool): Требуется ли аутентификация (True).
- `working` (bool): Указывает, работает ли провайдер (True).
- `use_nodriver` (bool): Использовать ли nodriver для аутентификации (True).
- `default_model` (str): Модель по умолчанию.
- `default_image_model` (str): Модель для обработки изображений по умолчанию.
- `default_vision_model` (str): Модель для обработки визуальных данных по умолчанию.
- `image_models` (list[str]): Список поддерживаемых моделей для обработки изображений.
- `models` (list[str]): Список поддерживаемых моделей.
- `model_aliases` (dict[str, str]): Псевдонимы моделей.
- `synthesize_content_type` (str): Тип контента для синтеза речи (audio/vnd.wav).
- `_cookies` (Cookies): Файлы cookie для аутентификации.
- `_snlm0e` (str): Токен аутентификации.
- `_sid` (str): SID токен.
- `auto_refresh` (bool): Автоматически обновлять cookie.
- `refresh_interval` (int): Интервал обновления cookie в секундах.
- `rotate_tasks` (dict): Задачи для ротации cookie.

**Принцип работы**:
Класс `Gemini` использует асинхронные запросы для взаимодействия с API Gemini. Он поддерживает как текстовые, так и визуальные запросы, а также автоматически обновляет файлы cookie для поддержания аутентификации. Для аутентификации может использоваться `nodriver`.

**Методы**:
- `nodriver_login(proxy: str = None) -> AsyncIterator[str]`: Асинхронный генератор для выполнения входа с использованием `nodriver`.
- `start_auto_refresh(proxy: str = None) -> None`: Запускает задачу для автоматического обновления cookie.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, cookies: Cookies = None, connector: BaseConnector = None, media: MediaListType = None, return_conversation: bool = False, conversation: Conversation = None, language: str = "en", **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от модели Gemini.
- `synthesize(params: dict, proxy: str = None) -> AsyncIterator[bytes]`: Синтезирует речь на основе переданного текста.
- `build_request(prompt: str, language: str, conversation: Conversation = None, uploads: list[list[str, str]] = None, tools: list[list[str]] = []) -> list`: Создает структуру запроса для отправки в Gemini.
- `upload_images(connector: BaseConnector, media: MediaListType) -> list`: Загружает изображения на сервер Gemini.
- `fetch_snlm0e(session: ClientSession, cookies: Cookies) -> None`: Извлекает токен `SNlM0e` из cookie.

#### `nodriver_login`

```python
@classmethod
async def nodriver_login(cls, proxy: str = None) -> AsyncIterator[str]:
    """
    Асинхронный генератор для выполнения входа с использованием `nodriver`.

    Args:
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

    Yields:
        AsyncIterator[str]: Частичные результаты входа.

    Raises:
        ImportError: Если модуль `nodriver` не установлен.
    """
    ...
```

#### `start_auto_refresh`

```python
@classmethod
async def start_auto_refresh(cls, proxy: str = None) -> None:
    """
    Запускает задачу для автоматического обновления cookie.

    Args:
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

    Raises:
        Exception: Если не удалось обновить cookie.
    """
    ...
```

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    cookies: Cookies = None,
    connector: BaseConnector = None,
    media: MediaListType = None,
    return_conversation: bool = False,
    conversation: Conversation = None,
    language: str = "en",
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от модели Gemini.

    Args:
        model (str): Имя модели для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        cookies (Cookies, optional): Файлы cookie для аутентификации. По умолчанию `None`.
        connector (BaseConnector, optional): HTTP коннектор для использования. По умолчанию `None`.
        media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
        return_conversation (bool, optional): Возвращать ли объект Conversation. По умолчанию `False`.
        conversation (Conversation, optional): Объект Conversation для продолжения беседы. По умолчанию `None`.
        language (str, optional): Язык ответа. По умолчанию "en".
        **kwargs: Дополнительные аргументы.

    Yields:
        AsyncResult: Асинхронный результат генерации.

    Raises:
        MissingAuthError: Если отсутствует или недействительный cookie "__Secure-1PSID".
        RuntimeError: Если не удалось получить токен SNlM0e.
    """
    ...
```

#### `synthesize`

```python
@classmethod
async def synthesize(cls, params: dict, proxy: str = None) -> AsyncIterator[bytes]:
    """
    Синтезирует речь на основе переданного текста.

    Args:
        params (dict): Параметры для синтеза речи, содержащие текст.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

    Yields:
        AsyncIterator[bytes]: Асинхронный генератор байтов аудиоданных.

    Raises:
        ValueError: Если отсутствует параметр "text".
    """
    ...
```

#### `build_request`

```python
def build_request(
    prompt: str,
    language: str,
    conversation: Conversation = None,
    uploads: list[list[str, str]] = None,
    tools: list[list[str]] = []
) -> list:
    """
    Создает структуру запроса для отправки в Gemini.

    Args:
        prompt (str): Текст запроса.
        language (str): Язык запроса.
        conversation (Conversation, optional): Объект Conversation для продолжения беседы. По умолчанию `None`.
        uploads (list[list[str, str]], optional): Список загруженных изображений. По умолчанию `None`.
        tools (list[list[str]], optional): Список инструментов. По умолчанию [].

    Returns:
        list: Структура запроса.
    """
    ...
```

#### `upload_images`

```python
async def upload_images(connector: BaseConnector, media: MediaListType) -> list:
    """
    Загружает изображения на сервер Gemini.

    Args:
        connector (BaseConnector): HTTP коннектор для использования.
        media (MediaListType): Список медиафайлов для загрузки.

    Returns:
        list: Список URL загруженных изображений.
    """
    ...
```

#### `fetch_snlm0e`

```python
@classmethod
async def fetch_snlm0e(cls, session: ClientSession, cookies: Cookies):
    """
    Извлекает токен `SNlM0e` из cookie.

    Args:
        session (ClientSession): Асинхронная HTTP сессия.
        cookies (Cookies): Файлы cookie для аутентификации.
    """
    ...
```

### `Conversation`

**Описание**:
Класс `Conversation` представляет собой JSON-объект, хранящий информацию о текущем диалоге с моделью Gemini.

**Наследует**:
- `JsonConversation`: Базовый класс для представления JSON-конвертации.

**Атрибуты**:
- `conversation_id` (str): ID текущего диалога.
- `response_id` (str): ID последнего ответа в диалоге.
- `choice_id` (str): ID выбора.
- `model` (str): Используемая модель.

**Принцип работы**:
Класс `Conversation` используется для хранения и передачи информации о контексте диалога между пользователем и моделью Gemini. Он содержит идентификаторы диалога, последнего ответа и выбора, а также имя используемой модели.

```python
class Conversation(JsonConversation):
    """
    Представляет собой JSON-объект, хранящий информацию о текущем диалоге с моделью Gemini.

    Args:
        conversation_id (str): ID текущего диалога.
        response_id (str): ID последнего ответа в диалоге.
        choice_id (str): ID выбора.
        model (str): Используемая модель.
    """
    def __init__(self,\
        conversation_id: str,\
        response_id: str,\
        choice_id: str,\
        model: str\
    ) -> None:\
        self.conversation_id = conversation_id\
        self.response_id = response_id\
        self.choice_id = choice_id\
        self.model = model
```

## Функции

### `iter_filter_base64`

```python
async def iter_filter_base64(chunks: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    """
    Фильтрует base64-данные из асинхронного итератора байтов.

    Args:
        chunks (AsyncIterator[bytes]): Асинхронный итератор байтов.

    Yields:
        AsyncIterator[bytes]: Отфильтрованные байты.

    Raises:
        ValueError: Если в ответе нет ожидаемой структуры.
    """
    ...
```

**Назначение**:
Функция `iter_filter_base64` предназначена для извлечения полезных данных в формате base64 из потока байтов, получаемого от сервера. Она ищет определенные маркеры начала и конца данных (`search_for` и `end_with`) и возвращает только содержимое между этими маркерами.

**Как работает**:
1. Функция принимает асинхронный итератор байтов (`chunks`) в качестве входных данных.
2. Определяет маркеры начала (`search_for`) и конца (`end_with`) полезных данных.
3. Итерируется по входному потоку байтов.
4. Если маркер начала найден, устанавливает флаг `is_started` в `True` и возвращает часть данных после маркера.
5. Если маркер конца найден, возвращает часть данных до маркера и завершает работу.
6. Если маркер начала не найден, вызывает исключение `ValueError`.

### `iter_base64_decode`

```python
async def iter_base64_decode(chunks: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    """
    Декодирует base64-данные из асинхронного итератора байтов.

    Args:
        chunks (AsyncIterator[bytes]): Асинхронный итератор байтов.

    Yields:
        AsyncIterator[bytes]: Декодированные байты.
    """
    ...
```

**Назначение**:
Функция `iter_base64_decode` предназначена для декодирования данных в формате base64 из асинхронного потока байтов. Она накапливает входные байты в буфере, пока не получит полный блок base64, а затем декодирует его.

**Как работает**:
1. Функция принимает асинхронный итератор байтов (`chunks`) в качестве входных данных.
2. Инициализирует пустой буфер (`buffer`) и переменную `rest` для хранения остатка байтов, не образующих полный блок base64.
3. Итерируется по входному потоку байтов.
4. Добавляет каждый полученный блок байтов в буфер.
5. Вычисляет остаток от деления длины буфера на 4 (размер блока base64).
6. Сохраняет остаток байтов в буфере для следующей итерации.
7. Декодирует часть буфера, не содержащую остаток, с помощью `base64.b64decode` и возвращает декодированные байты.
8. Если после завершения итерации в буфере остались байты, декодирует их, добавив необходимое количество символов `=`, чтобы образовать полный блок base64.

### `rotate_1psidts`

```python
async def rotate_1psidts(url, cookies: dict, proxy: str | None = None) -> str:
    """
    Обновляет cookie __Secure-1PSIDTS.

    Args:
        url (str): URL для запроса.
        cookies (dict): Cookie для аутентификации.
        proxy (str | None, optional): Прокси-сервер для использования. По умолчанию `None`.

    Returns:
        str: Новое значение cookie __Secure-1PSIDTS.

    Raises:
        MissingAuthError: Если cookie недействительны.
        HTTPError: Если возникает HTTP-ошибка.
    """
    ...
```

**Назначение**:
Функция `rotate_1psidts` предназначена для обновления cookie `__Secure-1PSIDTS`, который используется для аутентификации в сервисах Google. Она отправляет POST-запрос на специальный URL (`ROTATE_COOKIES_URL`) с текущими cookie и получает в ответ новые cookie, включая обновленный `__Secure-1PSIDTS`.

**Как работает**:
1. Функция принимает URL, словарь с cookie и опциональный прокси-сервер в качестве входных данных.
2. Формирует путь к файлу, в котором хранятся cookie.
3. Проверяет, не был ли файл cookie модифицирован в течение последней минуты, чтобы избежать отправки слишком большого количества запросов.
4. Отправляет POST-запрос на URL `ROTATE_COOKIES_URL` с текущими cookie.
5. Если сервер возвращает код состояния 401, вызывает исключение `MissingAuthError`, указывающее на недействительные cookie.
6. Обновляет входной словарь `cookies` новыми значениями, полученными из ответа сервера.
7. Извлекает новое значение cookie `__Secure-1PSIDTS` из ответа.
8. Записывает обновленные cookie в файл.
9. Возвращает новое значение cookie `__Secure-1PSIDTS`.