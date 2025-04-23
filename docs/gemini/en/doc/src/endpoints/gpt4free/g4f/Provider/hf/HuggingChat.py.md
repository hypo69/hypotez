# Module src.endpoints.gpt4free.g4f.Provider.hf.HuggingChat

## Overview

The module is designed to interact with the HuggingChat service to conduct conversations using different models, including those that support image processing. It supports authentication, conversation creation, sending messages, and receiving responses in streaming mode.

## More details

This module implements the `HuggingChat` class, which inherits from `AsyncAuthedProvider` and `ProviderModelMixin`. It provides functionality for authenticating with HuggingChat, creating conversations, sending text and image messages, and processing responses. The module uses asynchronous requests and streaming responses to efficiently handle long conversations. The module is configured to work through `curl_cffi`.

## Classes

### `Conversation`

**Description**:
Класс для представления истории разговора в формате JSON.

**Inherits**:
- `JsonConversation`: Наследует функциональность для управления разговорами в формате JSON.

**Attributes**:
- `models` (dict): Словарь для хранения информации о моделях, используемых в разговоре.

### `HuggingChat`

**Description**:
Класс для взаимодействия с сервисом HuggingChat.

**Inherits**:
- `AsyncAuthedProvider`: Наследует функциональность для асинхронной аутентификации.
- `ProviderModelMixin`: Наследует функциональность для работы с моделями провайдера.

**Attributes**:
- `domain` (str): Доменное имя HuggingChat (`"huggingface.co"`).
- `origin` (str): Базовый URL HuggingChat (`"https://huggingface.co"`).
- `url` (str): URL для чата HuggingChat (`"https://huggingface.co/chat"`).
- `working` (bool): Указывает, работает ли провайдер (всегда `True`).
- `use_nodriver` (bool): Указывает, использовать ли бездрайверный режим (всегда `True`).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (всегда `True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (всегда `True`).
- `default_model` (str): Модель, используемая по умолчанию.
- `default_vision_model` (str): Модель для работы с изображениями, используемая по умолчанию.
- `model_aliases` (dict): Псевдонимы для моделей.
- `image_models` (list): Список моделей для обработки изображений.
- `text_models` (list): Список текстовых моделей.

**Working principle**:
Класс `HuggingChat` используется для взаимодействия с API HuggingChat. Он поддерживает аутентификацию, создание и ведение разговоров с использованием различных моделей. Аутентификация происходит через cookies или с использованием логина и пароля. Класс позволяет отправлять текстовые и графические запросы и получать ответы в режиме реального времени.
При создании разговора и последующих запросах используются уникальные идентификаторы разговоров и сообщений.

**Methods**:
- `get_models`: Возвращает список доступных моделей.
- `on_auth_async`: Асинхронно аутентифицирует пользователя.
- `create_authed`: Создает аутентифицированный запрос к HuggingChat.
- `create_conversation`: Создает новый разговор.
- `fetch_message_id`: Извлекает идентификатор последнего сообщения в разговоре.

## Class Methods

### `get_models`

```python
@classmethod
def get_models(cls):
    """ Возвращает список доступных моделей из HuggingChat.

    Извлекает список моделей из веб-страницы HuggingChat, используя регулярные выражения и JSON.
    Если происходит ошибка при чтении моделей, используется резервный список моделей.

    Returns:
        list: Список доступных моделей.

    Raises:
        Exception: Если возникает ошибка при чтении моделей.

    How the function works:
    - Функция пытается получить HTML-код страницы чата HuggingFace.
    - Извлекает JSON с моделями, используя регулярное выражение.
    - Очищает JSON от лишних данных и форматирует его.
    - Преобразует JSON в список идентификаторов моделей.
    - В случае неудачи записывает информацию об ошибке в лог и использует fallback-список моделей.

    """
```

### `on_auth_async`

```python
@classmethod
async def on_auth_async(cls, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator:
    """ Асинхронно аутентифицирует пользователя.

    Проверяет наличие cookies для HuggingChat и, если они отсутствуют, запрашивает логин.

    Args:
        cookies (Cookies, optional): Cookies для аутентификации. Defaults to `None`.
        proxy (str, optional): Прокси-сервер для использования. Defaults to `None`.

    Yields:
        AuthResult: Результат аутентификации, включающий cookies и заголовки.
        RequestLogin: Объект для запроса логина, если аутентификация не удалась.

    How the function works:
    - Проверяет наличие `hf-chat` cookie. Если cookie присутствует, возвращает результат аутентификации с этими cookie.
    - Если cookie отсутствует и требуется аутентификация, запрашивает логин.
    - В противном случае генерирует session ID и возвращает результат аутентификации.

    """
```

### `create_authed`

```python
@classmethod
async def create_authed(
    cls,
    model: str,
    messages: Messages,
    auth_result: AuthResult,
    prompt: str = None,
    media: MediaListType = None,
    return_conversation: bool = False,
    conversation: Conversation = None,
    web_search: bool = False,
    **kwargs
) -> AsyncResult:
    """ Создает аутентифицированный запрос к HuggingChat.

    Создает разговор или использует существующий, отправляет сообщение и обрабатывает ответ.

    Args:
        model (str): Модель для использования в разговоре.
        messages (Messages): Список сообщений в разговоре.
        auth_result (AuthResult): Результат аутентификации.
        prompt (str, optional): Дополнительный текст запроса. Defaults to `None`.
        media (MediaListType, optional): Список медиафайлов для отправки. Defaults to `None`.
        return_conversation (bool, optional): Указывает, возвращать ли объект разговора. Defaults to `False`.
        conversation (Conversation, optional): Объект разговора. Defaults to `None`.
        web_search (bool, optional): Указывает, использовать ли веб-поиск. Defaults to `False`.

    Yields:
        str | ImageResponse | Sources | TitleGeneration | Reasoning | FinishReason: Результаты разговора в виде текста, изображений, источников, заголовков, рассуждений и причины завершения.

    Raises:
        MissingRequirementsError: Если отсутствует библиотека `curl_cffi`.
        ResponseError: Если возникает ошибка при создании разговора.

    How the function works:
    - Проверяет наличие необходимых зависимостей (`curl_cffi`).
    - Определяет модель для использования.
    - Создает сессию с использованием данных аутентификации.
    - Создает или использует существующий разговор.
    - Форматирует входные данные и отправляет запрос к HuggingChat.
    - Обрабатывает потоковые ответы от HuggingChat и возвращает результаты.

    """
```

### `create_conversation`

```python
@classmethod
def create_conversation(cls, session: Session, model: str):
    """ Создает новый разговор.

    Создает новый разговор с указанной моделью и возвращает его идентификатор.

    Args:
        session (Session): Сессия для выполнения запросов.
        model (str): Модель для использования в разговоре.

    Returns:
        str: Идентификатор созданного разговора.

    Raises:
        MissingAuthError: Если отсутствует аутентификация.
        ResponseError: Если возникает ошибка при создании разговора.

    How the function works:
    - Отправляет POST-запрос на создание нового разговора с указанной моделью.
    - Обрабатывает возможные ошибки аутентификации и ошибки, связанные с моделью.
    - Возвращает идентификатор созданного разговора из JSON-ответа.

    """
```

### `fetch_message_id`

```python
@classmethod
def fetch_message_id(cls, session: Session, conversation_id: str):
    """ Извлекает идентификатор последнего сообщения в разговоре.

    Получает данные разговора и извлекает из них идентификатор последнего сообщения.

    Args:
        session (Session): Сессия для выполнения запросов.
        conversation_id (str): Идентификатор разговора.

    Returns:
        str: Идентификатор последнего сообщения.

    Raises:
        RuntimeError: Если не удалось распарсить данные ответа или извлечь идентификатор сообщения.

    How the function works:
    - Отправляет GET-запрос для получения данных разговора.
    - Разделяет ответ на строки и пытается распарсить каждую строку как JSON.
    - Извлекает идентификатор последнего сообщения из распарсенных данных.
    - Обрабатывает возможные ошибки при парсинге данных или извлечении идентификатора.

    """
```