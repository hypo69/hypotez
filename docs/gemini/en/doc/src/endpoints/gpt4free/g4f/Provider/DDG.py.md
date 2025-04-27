# DuckDuckGo AI Chat Provider

## Overview

This module provides a class, `DDG`, for interacting with the DuckDuckGo AI Chat service. It allows developers to use the service as a backend for AI-powered conversations, leveraging the capabilities of various language models.

## Details

The `DDG` class implements a provider for the DuckDuckGo AI Chat service, using the `AsyncGeneratorProvider` and `ProviderModelMixin` abstract classes.  It offers support for streaming responses, system messages, and message history. The class utilizes a `Conversation` object to manage the context of the conversation, including VQD tokens, cookies, and the user's message history.

The module also includes several utility functions for:

* Parsing DOM fingerprints
* Parsing server hashes
* Building x-vqd-hash-1 headers
* Validating model names
* Handling rate limiting

## Classes

### `class DuckDuckGoSearchException`

**Description**: Base exception class for errors related to DuckDuckGo search.

### `class Conversation`

**Description**: Represents a conversation with the DuckDuckGo AI Chat service.

**Inherits**: `JsonConversation`

**Attributes**:

* `vqd` (str, optional): The VQD token for the conversation. Defaults to `None`.
* `vqd_hash_1` (str, optional): The x-vqd-hash-1 header value. Defaults to `None`.
* `message_history` (list): A list of messages in the conversation, in the format specified by `Messages`.
* `cookies` (dict): A dictionary containing the cookies for the conversation.
* `fe_version` (str, optional): The FE version of the DuckDuckGo chat service. Defaults to `None`.

**Methods**:

* `__init__(self, model: str)`: Initializes a new `Conversation` object with the specified language model.

### `class DDG`

**Description**: Provider class for the DuckDuckGo AI Chat service.

**Inherits**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Attributes**:

* `label` (str): Label for the provider, "DuckDuckGo AI Chat".
* `url` (str): Base URL for the DuckDuckGo AI Chat service.
* `api_endpoint` (str): API endpoint for sending chat requests.
* `status_url` (str): API endpoint for fetching VQD tokens.
* `working` (bool): Indicates whether the provider is currently working.
* `supports_stream` (bool): Indicates whether the provider supports streaming responses.
* `supports_system_message` (bool): Indicates whether the provider supports system messages.
* `supports_message_history` (bool): Indicates whether the provider supports message history.
* `default_model` (str): Default language model used by the provider.
* `models` (list): List of supported language models.
* `model_aliases` (dict): Mapping of aliases to supported models.
* `last_request_time` (float): Timestamp of the last request made to the API.
* `max_retries` (int): Maximum number of retries for failed requests.
* `base_delay` (float): Base delay time in seconds for retrying failed requests.
* `_chat_xfe` (str): Class variable storing the x-fe-version for all instances.

**Methods**:

* `sha256_base64(text: str) -> str`: Returns the base64 encoding of the SHA256 digest of the given text.

* `parse_dom_fingerprint(js_text: str) -> str`: Parses the DOM fingerprint from the JavaScript code.

* `parse_server_hashes(js_text: str) -> list`: Parses the server hashes from the JavaScript code.

* `build_x_vqd_hash_1(vqd_hash_1: str, headers: dict) -> str`: Builds the x-vqd-hash-1 header value based on the provided VQD hash and headers.

* `validate_model(model: str) -> str`: Validates the given model name and returns the correct model name.

* `sleep(multiplier=1.0)`: Implements rate limiting between API requests.

* `get_default_cookies(session: ClientSession) -> dict`: Obtains default cookies for API requests.

* `fetch_fe_version(session: ClientSession) -> str`: Fetches the `fe-version` from the DuckDuckGo AI Chat page.

* `fetch_vqd_and_hash(session: ClientSession, retry_count: int = 0) -> tuple[str, str]`: Fetches the VQD token and hash for the chat session with retries.

* `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 60, cookies: Cookies = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`: Creates an asynchronous generator for interacting with the DuckDuckGo AI Chat API.

## Functions

### `create_async_generator`

**Purpose**: Creates an asynchronous generator that handles communication with the DuckDuckGo AI Chat API.

**Parameters**:

* `model` (str): Language model to use for the conversation.
* `messages` (list): List of messages in the conversation, in the format specified by `Messages`.
* `proxy` (str, optional): Proxy server to use for requests. Defaults to `None`.
* `timeout` (int, optional): Timeout in seconds for API requests. Defaults to `60`.
* `cookies` (dict, optional): Cookies to use for the conversation. Defaults to `None`.
* `conversation` (Conversation, optional): An existing `Conversation` object to continue from. Defaults to `None`.
* `return_conversation` (bool, optional): Whether to return the updated `Conversation` object. Defaults to `False`.
* `**kwargs`: Additional keyword arguments to pass to the API request.

**Returns**:

* `AsyncResult`: An asynchronous generator that yields responses from the API.

**Raises Exceptions**:

* `RateLimitError`: If the API returns a 429 status code (rate limited).
* `ResponseStatusError`: If the API returns a non-200 status code.
* `TimeoutError`: If the request times out.
* `ConversationLimitError`: If the API reports an error related to conversation limit.
* `DuckDuckGoSearchException`: For other errors during the API request.

**How the Function Works**:

* The function first validates the provided model name and initializes a new `Conversation` object if needed.
* It then fetches the required VQD tokens and cookies and prepares the request data, including the conversation history.
* The function sends a POST request to the DuckDuckGo API endpoint.
* It handles streaming responses from the API and yields messages as they are received.
* The function also manages rate limiting, retries, and timeout handling.
* If `return_conversation` is True, the updated `Conversation` object is yielded after the API request completes.

**Examples**:

```python
from src.endpoints.gpt4free.g4f.Provider.DDG import DDG, Conversation
from src.endpoints.gpt4free.g4f.typing import Messages

# Creating a DDG provider instance
provider = DDG(model='gpt-4o-mini')

# Example 1: Simple conversation with default model
async def simple_conversation():
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]
    async for response in provider.create_async_generator(messages=messages):
        print(response)

# Example 2: Continuing a conversation using Conversation object
async def continue_conversation():
    conversation = Conversation(model='gpt-4o-mini')
    conversation.message_history = [
        {"role": "user", "content": "What is the meaning of life?"},
        {"role": "assistant", "content": "The meaning of life is a question that has been pondered by philosophers for centuries. There is no single answer that everyone agrees on. Some people believe that the meaning of life is to find happiness, while others believe that it is to make a difference in the world."},
    ]
    messages = [
        {"role": "user", "content": "What are your thoughts on that?"},
    ]
    async for response in provider.create_async_generator(messages=messages, conversation=conversation):
        print(response)

# Run the examples
asyncio.run(simple_conversation())
asyncio.run(continue_conversation())
```

## Inner Functions

* The `create_async_generator` function contains several inner functions that assist in managing the conversation flow and API interactions.  For example:
    * `parse_server_hashes`: Parses server hashes from JavaScript code.
    * `validate_model`: Validates the model name.
    * `sleep`: Implements rate limiting between requests.
    * `get_default_cookies`: Fetches default cookies needed for API requests.
    * `fetch_fe_version`: Fetches the FE version from the DuckDuckGo AI Chat page.
    * `fetch_vqd_and_hash`: Fetches VQD tokens for the chat session.

* The `create_async_generator` function is responsible for managing the asynchronous interaction with the DuckDuckGo AI Chat API, handling errors, and providing the necessary information to the user.

## Parameter Details

* `model` (str): The language model to use for the conversation, which must be one of the supported models.
* `messages` (list): A list of messages in the conversation, in the format specified by `Messages`.  Each message is represented as a dictionary with keys "role" and "content", where "role" indicates whether the message is from the user or the assistant, and "content" is the message text.
* `proxy` (str, optional): A proxy server to use for requests, if needed.
* `timeout` (int, optional): The timeout for API requests in seconds.
* `cookies` (dict, optional): Cookies to use for the conversation. If `None`, the function will fetch default cookies.
* `conversation` (Conversation, optional): An existing `Conversation` object to continue from, if available.  This allows for maintaining the conversation history.
* `return_conversation` (bool, optional): Whether to return the updated `Conversation` object after the API request completes.

## Example File

```python
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с API DuckDuckGo AI Chat
===============================================================
Модуль предоставляет класс `DDG`, который позволяет взаимодействовать с 
DuckDuckGo AI Chat в качестве бэкенда для AI-разговоров, используя различные 
языковые модели. 

## Подробности

Класс `DDG` реализует провайдера для DuckDuckGo AI Chat, используя абстрактные классы
`AsyncGeneratorProvider` и `ProviderModelMixin`. Он предлагает поддержку 
потоковых ответов, системных сообщений и истории сообщений. Класс использует 
объект `Conversation` для управления контекстом разговора, включая токены VQD, 
куки и историю сообщений пользователя. 

Модуль также включает несколько вспомогательных функций для:

* Парсинга отпечатков DOM
* Парсинга хэшей сервера
* Построения заголовков x-vqd-hash-1
* Проверки имен моделей
* Обработки ограничения скорости 

## Классы

### `class DuckDuckGoSearchException`

**Описание**: Базовый класс исключения для ошибок, связанных с поиском DuckDuckGo.

### `class Conversation`

**Описание**: Представляет собой разговор с сервисом DuckDuckGo AI Chat.

**Наследуется от**: `JsonConversation`

**Атрибуты**:

* `vqd` (str, optional): Токен VQD для разговора. По умолчанию `None`.
* `vqd_hash_1` (str, optional): Значение заголовка x-vqd-hash-1. По умолчанию `None`.
* `message_history` (list): Список сообщений в разговоре в формате, указанном `Messages`.
* `cookies` (dict): Словарь, содержащий куки для разговора.
* `fe_version` (str, optional): Версия FE сервиса DuckDuckGo chat. По умолчанию `None`.

**Методы**:

* `__init__(self, model: str)`: Инициализирует новый объект `Conversation` с указанной языковой моделью.

### `class DDG`

**Описание**: Класс-провайдер для сервиса DuckDuckGo AI Chat.

**Наследуется от**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:

* `label` (str): Метка для провайдера, "DuckDuckGo AI Chat".
* `url` (str): Базовый URL для сервиса DuckDuckGo AI Chat.
* `api_endpoint` (str): Конечная точка API для отправки запросов на чат.
* `status_url` (str): Конечная точка API для получения токенов VQD.
* `working` (bool): Указывает, работает ли провайдер в настоящее время.
* `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковые ответы.
* `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
* `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
* `default_model` (str): Языковая модель по умолчанию, используемая провайдером.
* `models` (list): Список поддерживаемых языковых моделей.
* `model_aliases` (dict): Сопоставление псевдонимов с поддерживаемыми моделями.
* `last_request_time` (float): Время последнего запроса к API.
* `max_retries` (int): Максимальное количество попыток повторной отправки для неудачных запросов.
* `base_delay` (float): Базовая задержка в секундах для повторной отправки неудачных запросов.
* `_chat_xfe` (str): Переменная класса, хранящая версию x-fe-version для всех экземпляров.

**Методы**:

* `sha256_base64(text: str) -> str`: Возвращает кодировку base64 дайджеста SHA256 для заданного текста.

* `parse_dom_fingerprint(js_text: str) -> str`: Разбирает отпечаток DOM из кода JavaScript.

* `parse_server_hashes(js_text: str) -> list`: Разбирает хэши сервера из кода JavaScript.

* `build_x_vqd_hash_1(vqd_hash_1: str, headers: dict) -> str`: Построение значения заголовка x-vqd-hash-1 на основе предоставленного хэша VQD и заголовков.

* `validate_model(model: str) -> str`: Проверяет имя модели и возвращает правильное имя модели.

* `sleep(multiplier=1.0)`: Реализует ограничение скорости между API-запросами.

* `get_default_cookies(session: ClientSession) -> dict`: Получение куков по умолчанию для API-запросов.

* `fetch_fe_version(session: ClientSession) -> str`: Извлечение версии `fe-version` со страницы DuckDuckGo AI Chat.

* `fetch_vqd_and_hash(session: ClientSession, retry_count: int = 0) -> tuple[str, str]`: Извлечение токена VQD и хэша для сеанса чата с попытками повторной отправки.

* `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 60, cookies: Cookies = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`: Создание асинхронного генератора для взаимодействия с API DuckDuckGo AI Chat.

## Функции

### `create_async_generator`

**Цель**: Создание асинхронного генератора, который обрабатывает коммуникацию с API DuckDuckGo AI Chat.

**Параметры**:

* `model` (str): Языковая модель для использования в разговоре.
* `messages` (list): Список сообщений в разговоре в формате, указанном `Messages`.
* `proxy` (str, optional): Прокси-сервер для использования для запросов. По умолчанию `None`.
* `timeout` (int, optional): Время ожидания в секундах для API-запросов. По умолчанию `60`.
* `cookies` (dict, optional): Куки для использования для разговора. По умолчанию `None`.
* `conversation` (Conversation, optional): Существующий объект `Conversation` для продолжения разговора. По умолчанию `None`.
* `return_conversation` (bool, optional): Возвращать ли обновленный объект `Conversation`. По умолчанию `False`.
* `**kwargs`: Дополнительные именованные аргументы для передачи в API-запрос.

**Возвращает**:

* `AsyncResult`: Асинхронный генератор, который выдает ответы от API.

**Возникающие исключения**:

* `RateLimitError`: Если API возвращает код состояния 429 (ограничение скорости).
* `ResponseStatusError`: Если API возвращает код состояния, отличный от 200.
* `TimeoutError`: Если запрос истекает по времени.
* `ConversationLimitError`: Если API сообщает об ошибке, связанной с ограничением разговора.
* `DuckDuckGoSearchException`: Для других ошибок во время API-запроса.

**Как работает функция**:

* Сначала функция проверяет имя предоставленной модели и, если необходимо, инициализирует новый объект `Conversation`.
* Затем она извлекает необходимые токены VQD и куки и подготавливает данные запроса, включая историю разговора.
* Функция отправляет POST-запрос к конечной точке API DuckDuckGo.
* Она обрабатывает потоковые ответы от API и выдает сообщения по мере их получения.
* Функция также управляет ограничением скорости, попытками повторной отправки и обработкой таймаутов.
* Если `return_conversation` равно True, обновленный объект `Conversation` выводится после завершения API-запроса.

**Примеры**:

```python
from src.endpoints.gpt4free.g4f.Provider.DDG import DDG, Conversation
from src.endpoints.gpt4free.g4f.typing import Messages

# Создание экземпляра провайдера DDG
provider = DDG(model='gpt-4o-mini')

# Пример 1: Простой разговор с моделью по умолчанию
async def simple_conversation():
    messages = [
        {"role": "user", "content": "Привет, как дела?"},
    ]
    async for response in provider.create_async_generator(messages=messages):
        print(response)

# Пример 2: Продолжение разговора с использованием объекта Conversation
async def continue_conversation():
    conversation = Conversation(model='gpt-4o-mini')
    conversation.message_history = [
        {"role": "user", "content": "В чем смысл жизни?"},
        {"role": "assistant", "content": "Смысл жизни - это вопрос, который философы задавали веками. Нет единого ответа, который бы все приняли. Некоторые люди считают, что смысл жизни - найти счастье, а другие считают, что смысл - это изменить мир."},
    ]
    messages = [
        {"role": "user", "content": "Что ты думаешь об этом?"},
    ]
    async for response in provider.create_async_generator(messages=messages, conversation=conversation):
        print(response)

# Запуск примеров
asyncio.run(simple_conversation())
asyncio.run(continue_conversation())
```

## Внутренние функции

* Функция `create_async_generator` содержит несколько внутренних функций, которые помогают управлять потоком разговора и взаимодействием с API. Например:
    * `parse_server_hashes`: Разбирает хэши сервера из кода JavaScript.
    * `validate_model`: Проверяет имя модели.
    * `sleep`: Реализует ограничение скорости между запросами.
    * `get_default_cookies`: Извлекает куки по умолчанию, необходимые для API-запросов.
    * `fetch_fe_version`: Извлекает версию FE со страницы DuckDuckGo AI Chat.
    * `fetch_vqd_and_hash`: Извлекает токены VQD для сеанса чата.

* Функция `create_async_generator` отвечает за управление асинхронным взаимодействием с API DuckDuckGo AI Chat, обработку ошибок и предоставление необходимой информации пользователю.

## Подробности о параметрах

* `model` (str): Языковая модель для использования в разговоре, которая должна быть одной из поддерживаемых моделей.
* `messages` (list): Список сообщений в разговоре в формате, указанном `Messages`.  Каждое сообщение представлено в виде словаря с ключами "role" и "content", где "role" указывает, является ли сообщение от пользователя или помощника, а "content" - это текст сообщения.
* `proxy` (str, optional): Прокси-сервер для использования для запросов, если необходимо.
* `timeout` (int, optional): Время ожидания для API-запросов в секундах.
* `cookies` (dict, optional): Куки для использования для разговора. Если `None`, функция извлечет куки по умолчанию.
* `conversation` (Conversation, optional): Существующий объект `Conversation` для продолжения разговора, если доступен.  Это позволяет поддерживать историю разговора.
* `return_conversation` (bool, optional): Возвращать ли обновленный объект `Conversation` после завершения API-запроса.

```python
## \file /hypotez/src/endpoints/gpt4free/g4f/Provider/DDG.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с API DuckDuckGo AI Chat
===============================================================
Модуль предоставляет класс `DDG`, который позволяет взаимодействовать с 
DuckDuckGo AI Chat в качестве бэкенда для AI-разговоров, используя различные 
языковые модели. 

## Подробности

Класс `DDG` реализует провайдера для DuckDuckGo AI Chat, используя абстрактные классы
`AsyncGeneratorProvider` и `ProviderModelMixin`. Он предлагает поддержку 
потоковых ответов, системных сообщений и истории сообщений. Класс использует 
объект `Conversation` для управления контекстом разговора, включая токены VQD, 
куки и историю сообщений пользователя. 

Модуль также включает несколько вспомогательных функций для:

* Парсинга отпечатков DOM
* Парсинга хэшей сервера
* Построения заголовков x-vqd-hash-1
* Проверки имен моделей
* Обработки ограничения скорости 

## Классы

### `class DuckDuckGoSearchException`

**Описание**: Базовый класс исключения для ошибок, связанных с поиском DuckDuckGo.

### `class Conversation`

**Описание**: Представляет собой разговор с сервисом DuckDuckGo AI Chat.

**Наследуется от**: `JsonConversation`

**Атрибуты**:

* `vqd` (str, optional): Токен VQD для разговора. По умолчанию `None`.
* `vqd_hash_1` (str, optional): Значение заголовка x-vqd-hash-1. По умолчанию `None`.
* `message_history` (list): Список сообщений в разговоре в формате, указанном `Messages`.
* `cookies` (dict): Словарь, содержащий куки для разговора.
* `fe_version` (str, optional): Версия FE сервиса DuckDuckGo chat. По умолчанию `None`.

**Методы**:

* `__init__(self, model: str)`: Инициализирует новый объект `Conversation` с указанной языковой моделью.

### `class DDG`

**Описание**: Класс-провайдер для сервиса DuckDuckGo AI Chat.

**Наследуется от**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:

* `label` (str): Метка для провайдера, "DuckDuckGo AI Chat".
* `url` (str): Базовый URL для сервиса DuckDuckGo AI Chat.
* `api_endpoint` (str): Конечная точка API для отправки запросов на чат.
* `status_url` (str): Конечная точка API для получения токенов VQD.
* `working` (bool): Указывает, работает ли провайдер в настоящее время.
* `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковые ответы.
* `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
* `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
* `default_model` (str): Языковая модель по умолчанию, используемая провайдером.
* `models` (list): Список поддерживаемых языковых моделей.
* `model_aliases` (dict): Сопоставление псевдонимов с поддерживаемыми моделями.
* `last_request_time` (float): Время последнего запроса к API.
* `max_retries` (int): Максимальное количество попыток повторной отправки для неудачных запросов.
* `base_delay` (float): Базовая задержка в секундах для повторной отправки неудачных запросов.
* `_chat_xfe` (str): Переменная класса, хранящая версию x-fe-version для всех экземпляров.

**Методы**:

* `sha256_base64(text: str) -> str`: Возвращает кодировку base64 дайджеста SHA256 для заданного текста.

* `parse_dom_fingerprint(js_text: str) -> str`: Разбирает отпечаток DOM из кода JavaScript.

* `parse_server_hashes(js_text: str) -> list`: Разбирает хэши сервера из кода JavaScript.

* `build_x_vqd_hash_1(vqd_hash_1: str, headers: dict) -> str`: Построение значения заголовка x-vqd-hash-1 на основе предоставленного хэша VQD и заголовков.

* `validate_model(model: str) -> str`: Проверяет имя модели и возвращает правильное имя модели.

* `sleep(multiplier=1.0)`: Реализует ограничение скорости между API-запросами.

* `get_default_cookies(session: ClientSession) -> dict`: Получение куков по умолчанию для API-запросов.

* `fetch_fe_version(session: ClientSession) -> str`: Извлечение версии `fe-version` со страницы DuckDuckGo AI Chat.

* `fetch_vqd_and_hash(session: ClientSession, retry_count: int = 0) -> tuple[str, str]`: Извлечение токена VQD и хэша для сеанса чата с попытками повторной отправки.

* `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 60, cookies: Cookies = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`: Создание асинхронного генератора для взаимодействия с API DuckDuckGo AI Chat.

## Функции

### `create_async_generator`

**Цель**: Создание асинхронного генератора, который обрабатывает коммуникацию с API DuckDuckGo AI Chat.

**Параметры**:

* `model` (str): Языковая модель для использования в разговоре.
* `messages` (list): Список сообщений в разговоре в формате, указанном `Messages`.
* `proxy` (str, optional): Прокси-сервер для использования для запросов. По умолчанию `None`.
* `timeout` (int, optional): Время ожидания в секундах для API-запросов. По умолчанию `60`.
* `cookies` (dict, optional): Куки для использования для разговора. По умолчанию `None`.
* `conversation` (Conversation, optional): Существующий объект `Conversation` для продолжения разговора. По умолчанию `None`.
* `return_conversation` (bool, optional): Возвращать ли обновленный объект `Conversation`. По умолчанию `False`.
* `**kwargs`: Дополнительные именованные аргументы для передачи в API-запрос.

**Возвращает**:

* `AsyncResult`: Асинхронный генератор, который выдает ответы от API.

**Возникающие исключения**:

* `RateLimitError`: Если API возвращает код состояния 429 (ограничение скорости).
* `ResponseStatusError`: Если API возвращает код состояния, отличный от 200.
* `TimeoutError`: Если запрос истекает по времени.
* `ConversationLimitError`: Если API сообщает об ошибке, связанной с ограничением разговора.
* `DuckDuckGoSearchException`: Для других ошибок во время API-запроса.

**Как работает функция**:

* Сначала функция проверяет имя предоставленной модели и, если необходимо, инициализирует новый объект `Conversation`.
* Затем она извлекает необходимые токены VQD и куки и подготавливает данные запроса, включая историю разговора.
* Функция отправляет POST-запрос к конечной точке API DuckDuckGo.
* Она обрабатывает потоковые ответы от API и выдает сообщения по мере их получения.
* Функция также управляет ограничением скорости, попытками повторной отправки и обработкой таймаутов.
* Если `return_conversation` равно True, обновленный объект `Conversation` выводится после завершения API-запроса.

**Примеры**:

```python
from src.endpoints.gpt4free.g4f.Provider.DDG import DDG, Conversation
from src.endpoints.gpt4free.g4f.typing import Messages

# Создание экземпляра провайдера DDG
provider = DDG(model='gpt-4o-mini')

# Пример 1: Простой разговор с моделью по умолчанию
async def simple_conversation():
    messages = [
        {"role": "user", "content": "Привет, как дела?"},
    ]
    async for response in provider.create_async_generator(messages=messages):
        print(response)

# Пример 2: Продолжение разговора с использованием объекта Conversation
async def continue_conversation():
    conversation = Conversation(model='gpt-4o-mini')
    conversation.message_history = [
        {"role": "user", "content": "В чем смысл жизни?"},
        {"role": "assistant", "content": "Смысл жизни - это вопрос, который философы задавали веками. Нет единого ответа, который бы все приняли. Некоторые люди считают, что смысл жизни - найти счастье, а другие считают, что смысл - это изменить мир."},
    ]
    messages = [
        {"role": "user", "content": "Что ты думаешь об этом?"},
    ]
    async for response in provider.create_async_generator(messages=messages, conversation=conversation):
        print(response)

# Запуск примеров
asyncio.run(simple_conversation())
asyncio.run(continue_conversation())
```

## Внутренние функции

* Функция `create_async_generator` содержит несколько внутренних функций, которые помогают управлять потоком разговора и взаимодействием с API. Например:
    * `parse_server_hashes`: Разбирает хэши сервера из кода JavaScript.
    * `validate_model`: Проверяет имя модели.
    * `sleep`: Реализует ограничение скорости между запросами.
    * `get_default_cookies`: Извлекает куки по умолчанию, необходимые для API-запросов.
    * `fetch_fe_version`: Извлекает версию FE со страницы DuckDuckGo AI Chat.
    * `fetch_vqd_and_hash`: Извлекает токены VQD для сеанса чата.

* Функция `create_async_generator` отвечает за управление асинхронным взаимодействием с API DuckDuckGo AI Chat, обработку ошибок и предоставление необходимой информации пользователю.

## Подробности о параметрах

* `model` (str): Языковая модель для использования в разговоре, которая должна быть одной из поддерживаемых моделей.
* `messages` (list): Список сообщений в разговоре в формате, указанном `Messages`.  Каждое сообщение представлено в виде словаря с ключами "role" и "content", где "role" указывает, является ли сообщение от пользователя или помощника, а "content" - это текст сообщения.
* `proxy` (str, optional): Прокси-сервер для использования для запросов, если необходимо.
* `timeout` (int, optional): Время ожидания для API-запросов в секундах.
* `cookies` (dict, optional): Куки для использования для разговора. Если `None`, функция извлечет куки по умолчанию.
* `conversation` (Conversation, optional): Существующий объект `Conversation` для продолжения разговора, если доступен.  Это позволяет поддерживать историю разговора.
* `return_conversation` (bool, optional): Возвращать ли обновленный объект `Conversation` после завершения API-запроса.

```python
from typing import Generator, Optional, List
from pathlib import Path


def read_text_file(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[List[str]] = None,
    chunk_size: int = 8192,
) -> Generator[str, None, None] | str | None:
    """
    Считывает содержимое файла (или файлов из каталога) с использованием генератора для экономии памяти.

    Args:
        file_path (str | Path): Путь к файлу или каталогу.
        as_list (bool): Если `True`, возвращает генератор строк.
        extensions (Optional[List[str]]): Список расширений файлов для чтения из каталога.
        chunk_size (int): Размер чанков для чтения файла в байтах.

    Returns:
        Generator[str, None, None] | str | None: Генератор строк, объединенная строка или `None` в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при чтении файла.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> content = read_text_file(file_path)
        >>> if content:
        ...    print(f'File content: {content[:100]}...')
        File content: Example text...
    """
    ...
```