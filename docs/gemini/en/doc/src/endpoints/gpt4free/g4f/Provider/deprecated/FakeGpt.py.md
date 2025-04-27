# Модуль FakeGpt
## Обзор
Модуль `FakeGpt` предоставляет класс `FakeGpt` для работы с фейковым API GPT, 
который имитирует поведение реального API OpenAI GPT.

## Details
Данный модуль используется для тестирования и отладки кода, 
взаимодействующего с API OpenAI GPT. Он предоставляет альтернативный 
API, который не отправляет запросы в реальный API GPT, 
а вместо этого генерирует случайные ответы. 

## Classes
### `class FakeGpt`
**Description**: Класс `FakeGpt` реализует интерфейс `AsyncGeneratorProvider` 
и предоставляет фейковый API, имитирующий поведение реального API OpenAI GPT.

**Inherits**: 
    - `AsyncGeneratorProvider`: Класс `FakeGpt` наследует от 
    `AsyncGeneratorProvider`, который обеспечивает базовый интерфейс 
    для асинхронных генераторов, предоставляющих ответы от GPT-моделей.

**Attributes**:
    - `url (str)`: URL-адрес фейкового API.
    - `supports_gpt_35_turbo (bool)`: Указывает, поддерживается ли модель GPT-3.5 Turbo.
    - `working (bool)`: Указывает, работает ли API.
    - `_access_token (str)`: Токен доступа, используемый для аутентификации в API.
    - `_cookie_jar`: Хранит cookie-файлы, используемые для сессии.

**Methods**:
    - `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`:
        - **Purpose**:  Асинхронный генератор для получения ответов от фейкового API.
        - **Parameters**:
            - `model (str)`: Название модели GPT.
            - `messages (Messages)`: Список сообщений в истории чата.
            - `proxy (str, optional)`: Прокси-сервер для использования с API. По умолчанию `None`.
        - **Returns**:
            - `AsyncResult`: Объект `AsyncResult` для асинхронного доступа к ответам.
        - **Raises Exceptions**:
            - `RuntimeError`: Если не получен допустимый ответ.
    - `inner_function()`: 
        - **Purpose**:  Внутренняя функция, которая имитирует отправку запроса в API.
        - **Parameters**: None
        - **Returns**: None
        - **Raises Exceptions**: None

## Functions
### `format_prompt(messages: Messages) -> str`:
    - **Purpose**: Форматирует текст запроса, объединяя сообщения из истории чата.
    - **Parameters**:
        - `messages (Messages)`: Список сообщений в истории чата.
    - **Returns**:
        - `str`: Текст запроса, готовый к отправке в API.

## Parameter Details
    - `messages (Messages)`: Список сообщений в истории чата. Каждый элемент списка 
     представляет собой словарь с ключами `id`, `author`, `content`, `metadata`, 
     который описывает конкретное сообщение. 

    - `proxy (str)`: Прокси-сервер, используемый для обхода блокировок или 
     для доступа к интернет-ресурсам из заблокированных сетей.