# Модуль `DeepSeekAPI.py`

## Обзор

Модуль `DeepSeekAPI.py` предоставляет асинхронный интерфейс для взаимодействия с API DeepSeek. Он позволяет выполнять аутентификацию, создавать чат-сессии и получать ответы от модели DeepSeek. Модуль поддерживает модели `deepseek-v3` и `deepseek-r1`, а также предоставляет возможность использования веб-поиска.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с различными AI-моделями. Он использует асинхронный подход для обеспечения высокой производительности и эффективного использования ресурсов. Модуль требует наличия установленной библиотеки `dsk.api`.

## Классы

### `DeepSeekAPI`

**Описание**: Класс `DeepSeekAPI` предоставляет асинхронный интерфейс для взаимодействия с API DeepSeek.

**Наследует**:
- `AsyncAuthedProvider`: Обеспечивает асинхронную аутентификацию.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL для доступа к API DeepSeek.
- `working` (bool): Указывает, работает ли API DeepSeek (зависит от наличия `dsk.api`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация для доступа к API DeepSeek.
- `use_nodriver` (bool): Указывает, использовать ли `nodriver` для аутентификации.
- `_access_token` (str | None): Токен доступа для аутентификации.
- `default_model` (str): Модель, используемая по умолчанию (`deepseek-v3`).
- `models` (List[str]): Список поддерживаемых моделей (`["deepseek-v3", "deepseek-r1"]`).

**Методы**:
- `on_auth_async()`: Асинхронно выполняет аутентификацию пользователя.
- `create_authed()`: Создает аутентифицированный запрос к API DeepSeek.

### `on_auth_async`

```python
    @classmethod
    async def on_auth_async(cls, proxy: str = None, **kwargs) -> AsyncIterator:
        """ Асинхронно выполняет аутентификацию пользователя.

        Args:
            proxy (str, optional): Прокси-сервер для использования при аутентификации. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Yields:
            RequestLogin: Объект, содержащий URL для входа.
            AuthResult: Объект, содержащий результаты аутентификации.

        Пример:
            Асинхронный запуск аутентификации с использованием прокси:

            >>> async for result in DeepSeekAPI.on_auth_async(proxy='http://your_proxy:8080'):
            ...     print(result)
        """
```

**Назначение**: Асинхронно выполняет аутентификацию пользователя.

**Параметры**:
- `proxy` (str, optional): Прокси-сервер для использования при аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncIterator`: Асинхронный итератор, возвращающий объекты `RequestLogin` и `AuthResult`.

**Как работает функция**:

1. Проверяет, существует ли атрибут `browser` в классе. Если нет, создает экземпляры `browser` и `stop_browser` с использованием `get_nodriver()`.
2. Возвращает объект `RequestLogin` с URL для входа. URL берется из переменной окружения `G4F_LOGIN_URL` или используется пустая строка, если переменная не задана.
3. Определяет асинхронную функцию `callback`, которая ожидает установку токена пользователя (`userToken`) в `localStorage` и сохраняет его в `cls._access_token`.
4. Получает аргументы из `nodriver` с использованием `get_args_from_nodriver()`, передавая URL, прокси и функцию `callback`.
5. Возвращает объект `AuthResult` с токеном доступа и аргументами.

```
A: Проверка наличия browser
|
B: Создание browser, stop_browser (если нет)
|
C: Yield RequestLogin
|
D: Определение callback(page)
|
E: Получение аргументов из nodriver
|
F: Yield AuthResult
```

**Примеры**:

```python
async for result in DeepSeekAPI.on_auth_async(proxy='http://your_proxy:8080'):
    print(result)
```

### `create_authed`

```python
    @classmethod
    async def create_authed(
        cls,
        model: str,
        messages: Messages,
        auth_result: AuthResult,
        conversation: JsonConversation = None,
        web_search: bool = False,
        **kwargs
    ) -> AsyncResult:
        """ Создает аутентифицированный запрос к API DeepSeek.

        Args:
            model (str): Используемая модель.
            messages (Messages): Список сообщений для отправки.
            auth_result (AuthResult): Результаты аутентификации.
            conversation (JsonConversation, optional): Объект разговора. По умолчанию `None`.
            web_search (bool, optional): Указывает, следует ли использовать веб-поиск. По умолчанию `False`.
            **kwargs: Дополнительные аргументы.

        Yields:
            JsonConversation: Объект разговора.
            Reasoning: Объект, содержащий промежуточные результаты (статус "Is thinking...", "Thought for...").
            str: Текст ответа от API DeepSeek.
            FinishReason: Объект, содержащий причину завершения.
        """
```

**Назначение**: Создает аутентифицированный запрос к API DeepSeek.

**Параметры**:
- `model` (str): Используемая модель.
- `messages` (Messages): Список сообщений для отправки.
- `auth_result` (AuthResult): Результаты аутентификации.
- `conversation` (JsonConversation, optional): Объект разговора. По умолчанию `None`.
- `web_search` (bool, optional): Указывает, следует ли использовать веб-поиск. По умолчанию `False`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий объекты `JsonConversation`, `Reasoning`, текст ответа и `FinishReason`.

**Как работает функция**:

1. Инициализирует API DeepSeek с использованием токена аутентификации из `auth_result`.
2. Если объект разговора (`conversation`) равен `None`, создает новую чат-сессию с использованием `api.create_chat_session()` и создает объект `JsonConversation` с идентификатором чата.
3. Возвращает объект `conversation`.
4. Отправляет запрос на завершение чата с использованием `api.chat_completion()`, передавая идентификатор чата, последнее сообщение пользователя, флаг включения "thinking" (для модели `deepseek-r1`) и флаг включения веб-поиска.
5. Итерируется по чанкам ответа от API DeepSeek и возвращает объекты `Reasoning` (если включено "thinking"), текст ответа и `FinishReason`.

```
A: Инициализация API с auth_result
|
B: Проверка conversation
|
C: Создание conversation (если None)
|
D: Yield conversation
|
E: Запрос chat_completion
|
F: Итерация по чанкам ответа
|
G: Yield Reasoning (если thinking)
|
H: Yield текст ответа
|
I: Yield FinishReason
```

**Примеры**:

```python
async for chunk in DeepSeekAPI.create_authed(
    model="deepseek-v3",
    messages=[{"role": "user", "content": "Hello"}],
    auth_result=auth_result,
    web_search=True
):
    print(chunk)
```
```python
from __future__ import annotations

import os
import json
import time
from typing import AsyncIterator

import asyncio

from ..base_provider import AsyncAuthedProvider, ProviderModelMixin
from ...providers.helper import get_last_user_message
from ...requests import get_args_from_nodriver, get_nodriver
from ...providers.response import AuthResult, RequestLogin, Reasoning, JsonConversation, FinishReason
from ...typing import AsyncResult, Messages

try:
    from dsk.api import DeepSeekAPI as DskAPI

    has_dsk = True
except ImportError:
    has_dsk = False


class DeepSeekAPI(AsyncAuthedProvider, ProviderModelMixin):
    url = "https://chat.deepseek.com"
    working = has_dsk
    needs_auth = True
    use_nodriver = True
    _access_token = None

    default_model = "deepseek-v3"
    models = ["deepseek-v3", "deepseek-r1"]

    @classmethod
    async def on_auth_async(cls, proxy: str = None, **kwargs) -> AsyncIterator:
        """Асинхронно выполняет аутентификацию пользователя.

        Args:
            proxy (str, optional): Прокси-сервер для использования при аутентификации. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Yields:
            RequestLogin: Объект, содержащий URL для входа.
            AuthResult: Объект, содержащий результаты аутентификации.

        Пример:
            Асинхронный запуск аутентификации с использованием прокси:

            >>> async for result in DeepSeekAPI.on_auth_async(proxy='http://your_proxy:8080'):
            ...     print(result)
        """
        if not hasattr(cls, "browser"):
            cls.browser, cls.stop_browser = await get_nodriver()
        yield RequestLogin(cls.__name__, os.environ.get("G4F_LOGIN_URL") or "")

        async def callback(page):
            """Внутренняя функция, ожидающая установки токена пользователя в localStorage.

            Args:
                page: Объект страницы браузера.
            """
            while True:
                await asyncio.sleep(1)
                cls._access_token = json.loads(await page.evaluate("localStorage.getItem('userToken')") or "{}").get("value")
                if cls._access_token:
                    break

        args = await get_args_from_nodriver(cls.url, proxy, callback=callback, browser=cls.browser)
        yield AuthResult(
            api_key=cls._access_token,
            **args,
        )

    @classmethod
    async def create_authed(
        cls,
        model: str,
        messages: Messages,
        auth_result: AuthResult,
        conversation: JsonConversation = None,
        web_search: bool = False,
        **kwargs,
    ) -> AsyncResult:
        """Создает аутентифицированный запрос к API DeepSeek.

        Args:
            model (str): Используемая модель.
            messages (Messages): Список сообщений для отправки.
            auth_result (AuthResult): Результаты аутентификации.
            conversation (JsonConversation, optional): Объект разговора. По умолчанию `None`.
            web_search (bool, optional): Указывает, следует ли использовать веб-поиск. По умолчанию `False`.
            **kwargs: Дополнительные аргументы.

        Yields:
            JsonConversation: Объект разговора.
            Reasoning: Объект, содержащий промежуточные результаты (статус "Is thinking...", "Thought for...").
            str: Текст ответа от API DeepSeek.
            FinishReason: Объект, содержащий причину завершения.
        """
        # Initialize with your auth token
        api = DskAPI(auth_result.get_dict())

        # Create a new chat session
        if conversation is None:
            chat_id = api.create_chat_session()
            conversation = JsonConversation(chat_id=chat_id)
        yield conversation

        is_thinking = 0
        for chunk in api.chat_completion(
            conversation.chat_id,
            get_last_user_message(messages),
            thinking_enabled="deepseek-r1" in model,
            search_enabled=web_search,
        ):
            if chunk["type"] == "thinking":
                if not is_thinking:
                    yield Reasoning(status="Is thinking...")
                    is_thinking = time.time()
                yield Reasoning(chunk["content"])
            elif chunk["type"] == "text":
                if is_thinking:
                    yield Reasoning(status=f"Thought for {time.time() - is_thinking:.2f}s")
                    is_thinking = 0
                if chunk["content"]:
                    yield chunk["content"]
            if chunk["finish_reason"]:
                yield FinishReason(chunk["finish_reason"])