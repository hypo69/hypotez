# DuckDuckGo Provider

## Overview

This module provides the `DuckDuckGo` class, which implements an asynchronous generator provider for the `hypotez` project, utilizing the `duckduckgo_search` library to interact with DuckDuckGo's AI chat API.

## Details

This module enables users to interact with DuckDuckGo's AI chat API through the `DuckDuckGo` class, which provides functionality for sending messages, receiving responses, and handling potential errors. It leverages the `duckduckgo_search` library for API communication and the `nodriver` library for authenticating with the API.

## Classes

### `class DuckDuckGo`

**Description:** This class implements an asynchronous generator provider for interacting with DuckDuckGo's AI chat API.

**Inherits:** `AsyncGeneratorProvider`, `ProviderModelMixin`

**Attributes:**

- `label (str)`: A label for the provider, set to "Duck.ai (duckduckgo_search)".
- `url (str)`: The base URL for the DuckDuckGo AI chat API.
- `api_base (str)`: The base URL for the DuckDuckGo chat API endpoint.
- `working (bool)`: Indicates whether the provider is currently active, set to `False`.
- `supports_stream (bool)`: Indicates whether the provider supports streaming responses, set to `True`.
- `supports_system_message (bool)`: Indicates whether the provider supports system messages, set to `True`.
- `supports_message_history (bool)`: Indicates whether the provider supports message history, set to `True`.
- `default_model (str)`: The default model for the provider, set to "gpt-4o-mini".
- `models (list)`: A list of available models for the provider.
- `ddgs (DDGS)`: An instance of the `DDGS` class from the `duckduckgo_search` library, used for API interactions.
- `model_aliases (dict)`: A dictionary mapping common model names to their corresponding actual model names.

**Methods:**

#### `create_async_generator`

**Purpose:** Creates an asynchronous generator for interacting with DuckDuckGo's AI chat API.

**Parameters:**

- `model (str)`: The name of the model to use for the conversation.
- `messages (Messages)`: A list of messages for the conversation.
- `proxy (str)`: A proxy server to use for the API requests. Defaults to `None`.
- `timeout (int)`: The timeout value in seconds for the API requests. Defaults to 60.
- `**kwargs`: Additional keyword arguments.

**Returns:**

- `AsyncResult`: An asynchronous generator that yields responses from the AI chat API.

**Raises Exceptions:**

- `ImportError`: If the `duckduckgo_search` library is not installed.

**How the Function Works:**

This method initializes the `DDGS` instance if it's not already created, sets up the model, and then yields responses from the AI chat API using the `ddgs.chat_yield` method.

#### `nodriver_auth`

**Purpose:** Authenticates with DuckDuckGo's AI chat API using the `nodriver` library.

**Parameters:**

- `proxy (str)`: A proxy server to use for the API requests. Defaults to `None`.

**Returns:**

- `None`: This method doesn't return a value.

**How the Function Works:**

This method initiates a browser instance using `nodriver`, navigates to the DuckDuckGo AI chat URL, intercepts API requests to retrieve authentication tokens, and finally closes the browser.

## Example File

```python
## \file hypotez/src/endpoints/gpt4free/g4f/Provider/DuckDuckGo.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для взаимодействия с API DuckDuckGo через duckduckgo_search
==================================================================

Модуль реализует класс `DuckDuckGo`, который обеспечивает взаимодействие с
API DuckDuckGo через библиотеку `duckduckgo_search`. Класс позволяет
отправлять сообщения, получать ответы и обрабатывать потенциальные ошибки.

## Details

Модуль предоставляет функциональность для работы с API чата DuckDuckGo.
Он использует библиотеку `duckduckgo_search` для взаимодействия с API и
библиотеку `nodriver` для аутентификации с API.

## Classes

### `class DuckDuckGo`

**Описание:** Класс реализует асинхронный генератор-поставщик для
взаимодействия с API чата DuckDuckGo.

**Наследует:** `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты:**

- `label (str)`: Метка для поставщика, установленная в "Duck.ai
(duckduckgo_search)".
- `url (str)`: Базовый URL для API чата DuckDuckGo.
- `api_base (str)`: Базовый URL для конечной точки API чата DuckDuckGo.
- `working (bool)`: Указывает, активен ли поставщик в данный момент,
установлено в `False`.
- `supports_stream (bool)`: Указывает, поддерживает ли поставщик потоковую
передачу ответов, установлено в `True`.
- `supports_system_message (bool)`: Указывает, поддерживает ли поставщик
системные сообщения, установлено в `True`.
- `supports_message_history (bool)`: Указывает, поддерживает ли поставщик
историю сообщений, установлено в `True`.
- `default_model (str)`: Модель по умолчанию для поставщика,
установлено в "gpt-4o-mini".
- `models (list)`: Список доступных моделей для поставщика.
- `ddgs (DDGS)`: Экземпляр класса `DDGS` из библиотеки
`duckduckgo_search`, используемый для взаимодействия с API.
- `model_aliases (dict)`: Словарь, сопоставляющий общие имена моделей с
их соответствующими фактическими именами моделей.

**Методы:**

#### `create_async_generator`

**Цель:** Создает асинхронный генератор для взаимодействия с API чата
DuckDuckGo.

**Параметры:**

- `model (str)`: Имя модели, которую нужно использовать для
разговора.
- `messages (Messages)`: Список сообщений для разговора.
- `proxy (str)`: Прокси-сервер, который нужно использовать для API-запросов.
По умолчанию `None`.
- `timeout (int)`: Значение тайм-аута в секундах для API-запросов. По
умолчанию 60.
- `**kwargs`: Дополнительные именованные аргументы.

**Возвращает:**

- `AsyncResult`: Асинхронный генератор, который выдает ответы от API
чата.

**Возможные исключения:**

- `ImportError`: Если библиотека `duckduckgo_search` не установлена.

**Принцип работы:**

Этот метод инициализирует экземпляр `DDGS`, если он еще не создан,
устанавливает модель, а затем выдает ответы от API чата с помощью метода
`ddgs.chat_yield`.

#### `nodriver_auth`

**Цель:** Аутентифицирует с API чата DuckDuckGo с помощью библиотеки
`nodriver`.

**Параметры:**

- `proxy (str)`: Прокси-сервер, который нужно использовать для
API-запросов. По умолчанию `None`.

**Возвращает:**

- `None`: Этот метод не возвращает значение.

**Принцип работы:**

Этот метод запускает экземпляр браузера с помощью `nodriver`, переходит
на URL-адрес чата DuckDuckGo AI, перехватывает API-запросы для получения
токенов аутентификации, а затем закрывает браузер.

## Example File

```python
## \file hypotez/src/endpoints/gpt4free/g4f/Provider/DuckDuckGo.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Module for interacting with the DuckDuckGo API via duckduckgo_search
==================================================================

The module implements the `DuckDuckGo` class, which provides interaction with
the DuckDuckGo API through the `duckduckgo_search` library. The class allows
you to send messages, receive responses, and handle potential errors.

## Details

The module provides functionality for working with the DuckDuckGo chat API.
It uses the `duckduckgo_search` library to interact with the API and
the `nodriver` library to authenticate with the API.

## Classes

### `class DuckDuckGo`

**Description:** The class implements an asynchronous generator provider for
interacting with the DuckDuckGo chat API.

**Inherits:** `AsyncGeneratorProvider`, `ProviderModelMixin`

**Attributes:**

- `label (str)`: A label for the provider, set to "Duck.ai
(duckduckgo_search)".
- `url (str)`: The base URL for the DuckDuckGo AI chat API.
- `api_base (str)`: The base URL for the DuckDuckGo chat API endpoint.
- `working (bool)`: Indicates whether the provider is currently active,
set to `False`.
- `supports_stream (bool)`: Indicates whether the provider supports streaming
responses, set to `True`.
- `supports_system_message (bool)`: Indicates whether the provider supports
system messages, set to `True`.
- `supports_message_history (bool)`: Indicates whether the provider supports
message history, set to `True`.
- `default_model (str)`: The default model for the provider,
set to "gpt-4o-mini".
- `models (list)`: A list of available models for the provider.
- `ddgs (DDGS)`: An instance of the `DDGS` class from the
`duckduckgo_search` library, used for API interactions.
- `model_aliases (dict)`: A dictionary mapping common model names to
their corresponding actual model names.

**Methods:**

#### `create_async_generator`

**Purpose:** Creates an asynchronous generator for interacting with the
DuckDuckGo chat API.

**Parameters:**

- `model (str)`: The name of the model to use for the conversation.
- `messages (Messages)`: A list of messages for the conversation.
- `proxy (str)`: A proxy server to use for the API requests. Defaults to
`None`.
- `timeout (int)`: The timeout value in seconds for the API requests. Defaults
to 60.
- `**kwargs`: Additional keyword arguments.

**Returns:**

- `AsyncResult`: An asynchronous generator that yields responses from the AI
chat API.

**Raises Exceptions:**

- `ImportError`: If the `duckduckgo_search` library is not installed.

**How the Function Works:**

This method initializes the `DDGS` instance if it's not already created,
sets up the model, and then yields responses from the AI chat API using the
`ddgs.chat_yield` method.

#### `nodriver_auth`

**Purpose:** Authenticates with the DuckDuckGo chat API using the `nodriver`
library.

**Parameters:**

- `proxy (str)`: A proxy server to use for the API requests. Defaults to
`None`.

**Returns:**

- `None`: This method doesn't return a value.

**How the Function Works:**

This method initiates a browser instance using `nodriver`, navigates to the
DuckDuckGo AI chat URL, intercepts API requests to retrieve authentication
tokens, and finally closes the browser.
```