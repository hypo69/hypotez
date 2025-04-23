## \file hypotez/src/endpoints/gpt4free/g4f/Provider/DuckDuckGo.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль реализует асинхронного провайдера DuckDuckGo для использования в gpt4free.

Он включает поддержку различных моделей, таких как gpt-4o-mini, llama-3.3-70b, claude-3-haiku и mistralai/Mistral-Small-24B-Instruct-2501,
а также обеспечивает взаимодействие с API DuckDuckGo через библиотеку duckduckgo_search.
"""
from __future__ import annotations

import asyncio

try:
    from duckduckgo_search import DDGS
    from duckduckgo_search.exceptions import DuckDuckGoSearchException, RatelimitException, ConversationLimitException

    has_requirements = True
except ImportError:
    has_requirements = False
try:
    import nodriver

    has_nodriver = True
except ImportError:
    has_nodriver = False

from ..typing import AsyncResult, Messages
from ..requests import get_nodriver
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from .helper import get_last_user_message

class DuckDuckGo(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер DuckDuckGo для gpt4free.

    Этот класс обеспечивает интеграцию с DuckDuckGo для использования их моделей в gpt4free.
    Поддерживает стриминг, системные сообщения и историю сообщений.
    """
    label = "Duck.ai (duckduckgo_search)"
    url = "https://duckduckgo.com/aichat"
    api_base = "https://duckduckgo.com/duckchat/v1/"

    working = False
    supports_stream = True
    supports_system_message = True
    supports_message_history = True

    default_model = "gpt-4o-mini"
    models = [default_model, "meta-llama/Llama-3.3-70B-Instruct-Turbo", "claude-3-haiku-20240307", "o3-mini",
              "mistralai/Mistral-Small-24B-Instruct-2501"]

    ddgs: DDGS = None

    model_aliases = {
        "gpt-4": "gpt-4o-mini",
        "llama-3.3-70b": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "claude-3-haiku": "claude-3-haiku-20240307",
        "mixtral-small-24b": "mistralai/Mistral-Small-24B-Instruct-2501",
    }

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            proxy: str = None,
            timeout: int = 60,
            **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с DuckDuckGo.

        Args:
            model (str): Имя модели для использования.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию None.
            timeout (int, optional): Время ожидания запроса. По умолчанию 60.
            **kwargs: Дополнительные параметры.

        Yields:
            str: Части ответа от DuckDuckGo.

        Raises:
            ImportError: Если не установлена библиотека duckduckgo_search.

        """
        if not has_requirements:
            raise ImportError(
                "duckduckgo_search is not installed. Install it with `pip install duckduckgo-search`.")
        if cls.ddgs is None:
            cls.ddgs = DDGS(proxy=proxy, timeout=timeout)
            if has_nodriver:
                await cls.nodriver_auth(proxy=proxy)
        model = cls.get_model(model)
        for chunk in cls.ddgs.chat_yield(get_last_user_message(messages), model, timeout):
            yield chunk

    @classmethod
    async def nodriver_auth(cls, proxy: str = None):
        """
        Выполняет аутентификацию через nodriver для получения необходимых параметров для взаимодействия с DuckDuckGo.

        Args:
            proxy (str, optional): Прокси-сервер для использования. По умолчанию None.
        """
        browser, stop_browser = await get_nodriver(proxy=proxy)
        try:
            page = browser.main_tab

            def on_request(event: nodriver.cdp.network.RequestWillBeSent, page=None):
                """
                Обработчик событий запросов для извлечения параметров аутентификации.

                Args:
                    event (nodriver.cdp.network.RequestWillBeSent): Событие запроса.
                    page: Страница браузера.
                """
                if cls.api_base in event.request.url:
                    if "X-Vqd-4" in event.request.headers:
                        cls.ddgs._chat_vqd = event.request.headers["X-Vqd-4"]
                    if "X-Vqd-Hash-1" in event.request.headers:
                        cls.ddgs._chat_vqd_hash = event.request.headers["X-Vqd-Hash-1"]
                    if "F-Fe-Version" in event.request.headers:
                        cls.ddgs._chat_xfe = event.request.headers["F-Fe-Version"]

            await page.send(nodriver.cdp.network.enable())
            page.add_handler(nodriver.cdp.network.RequestWillBeSent, on_request)
            page = await browser.get(cls.url)
            while True:
                if cls.ddgs._chat_vqd:
                    break
                await asyncio.sleep(1)
            await page.close()
        finally:
            stop_browser()
```

### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет класс `DuckDuckGo`, который позволяет взаимодействовать с моделями DuckDuckGo в проектах, использующих библиотеку `gpt4free`. Он настраивает асинхронный генератор для обмена сообщениями с моделями DuckDuckGo, поддерживает выбор модели, прокси и таймауты. Также включает механизм аутентификации через `nodriver` для получения необходимых параметров для API DuckDuckGo.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек и модулей**:
   - Импортируются `asyncio`, `DDGS` (из `duckduckgo_search`), `AsyncResult` и `Messages` (из `..typing`), `get_nodriver` (из `..requests`), `AsyncGeneratorProvider` и `ProviderModelMixin` (из `.base_provider`), и `get_last_user_message` (из `.helper`).
   - Проверяется наличие установленных библиотек `duckduckgo_search` и `nodriver`.

2. **Определение класса `DuckDuckGo`**:
   - Класс наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`.
   - Устанавливаются атрибуты класса, такие как `label`, `url`, `api_base`, `working`, `supports_stream`, `supports_system_message`, `supports_message_history`, `default_model` и `models`.
   - Определяется словарь `model_aliases` для альтернативных названий моделей.

3. **Метод `create_async_generator`**:
   - Проверяется, установлена ли библиотека `duckduckgo_search`, и если нет, вызывается исключение `ImportError`.
   - Если `cls.ddgs` не инициализирован, он инициализируется с использованием `DDGS` с заданным прокси и таймаутом.
   - Если `has_nodriver` истинно, вызывается метод `cls.nodriver_auth` для аутентификации.
   - Извлекается модель с использованием `cls.get_model(model)`.
   - Используется `cls.ddgs.chat_yield` для получения асинхронного генератора чанков ответа от DuckDuckGo.

4. **Метод `nodriver_auth`**:
   - Получается браузер и функция остановки браузера с использованием `get_nodriver`.
   - Определяется функция `on_request`, которая проверяет запросы, содержащие `cls.api_base` и извлекает значения `X-Vqd-4`, `X-Vqd-Hash-1` и `F-Fe-Version` из заголовков запроса, сохраняя их в атрибуты `cls.ddgs._chat_vqd`, `cls.ddgs._chat_vqd_hash` и `cls.ddgs._chat_xfe` соответственно.
   - Включается перехват сетевых запросов на странице браузера.
   - Добавляется обработчик `on_request` для перехвата запросов.
   - Открывается URL `cls.url` в браузере.
   - Ожидается, пока не будет получено значение `cls.ddgs._chat_vqd`.
   - Закрывается страница и останавливается браузер.

Пример использования
-------------------------

```python
    from src.endpoints.gpt4free.g4f.Provider.DuckDuckGo import DuckDuckGo
    import asyncio

    async def main():
        messages = [
            {"role": "user", "content": "Hello, how are you?"}
        ]
        model = "gpt-4o-mini"
        async for chunk in DuckDuckGo.create_async_generator(model=model, messages=messages):
            print(chunk, end="")

    if __name__ == "__main__":
        asyncio.run(main())