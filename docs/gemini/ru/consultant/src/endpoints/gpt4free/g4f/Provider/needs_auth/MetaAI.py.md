### **Анализ кода модуля `MetaAI.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование `AsyncGeneratorProvider` для асинхронной генерации данных.
    - Явное указание кодировки при работе с файлами.
    - Использование `aiohttp` для асинхронных запросов.
- **Минусы**:
    - Отсутствие аннотаций типов для переменных класса, что снижает читаемость и увеличивает вероятность ошибок.
    - Недостаточно подробные комментарии, особенно в сложных участках кода.
    - Смешанный стиль кавычек (используются как двойные, так и одинарные).
    - Не все методы и функции имеют docstring.
    - Отсутствие логирования ошибок и важных событий.
    - Не используется `j_loads` или `j_loads_ns` для чтения JSON.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**: Улучшить читаемость и надежность кода, добавив аннотации типов для всех переменных и возвращаемых значений функций.
2.  **Улучшить комментарии и docstring**: Добавить подробные docstring для всех классов, методов и функций. Описать назначение каждого блока кода. Перевести все комментарии и docstring на русский язык.
3.  **Использовать одинарные кавычки**: Привести все строки к использованию одинарных кавычек.
4.  **Добавить логирование**: Добавить логирование для отслеживания ошибок и важных событий в коде.
5.  **Использовать `j_loads` или `j_loads_ns`**: Заменить использование `json.loads` на `j_loads` или `j_loads_ns`.

**Оптимизированный код:**

```python
from __future__ import annotations

import json
import uuid
import random
import time
from typing import Dict, List, Optional

from aiohttp import ClientSession, BaseConnector, ClientResponse

from ...typing import AsyncResult, Messages, Cookies
from ...requests import raise_for_status, DEFAULT_HEADERS
from ...providers.response import ImageResponse, ImagePreview
from ...errors import ResponseError
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..helper import format_prompt, get_connector, format_cookies
from src.logger import logger
from pathlib import Path


class Sources:
    """
    Класс для хранения и форматирования источников информации.

    Attributes:
        list (List[Dict[str, str]]): Список словарей, каждый из которых содержит информацию об источнике.
    """

    def __init__(self, link_list: List[Dict[str, str]]) -> None:
        """
        Инициализирует объект Sources.

        Args:
            link_list (List[Dict[str, str]]): Список словарей, содержащих информацию об источниках.
        """
        self.list: List[Dict[str, str]] = link_list

    def __str__(self) -> str:
        """
        Возвращает строковое представление списка источников в формате Markdown.

        Returns:
            str: Отформатированная строка со списком источников.
        """
        return "\n\n" + ("\n".join([f"[{link['title']}]({link['link']})" for link in self.list]))


class AbraGeoBlockedError(Exception):
    """
    Исключение, поднимаемое при географической блокировке доступа к Meta AI.
    """

    pass


class MetaAI(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер для взаимодействия с Meta AI.

    Attributes:
        label (str): Метка провайдера.
        url (str): URL Meta AI.
        working (bool): Статус работоспособности провайдера.
        default_model (str): Модель, используемая по умолчанию.
        session (ClientSession): Асинхронная сессия для выполнения HTTP-запросов.
        cookies (Cookies | None): Cookies для аутентификации.
        access_token (str | None): Токен доступа.
    """

    label: str = "Meta AI"
    url: str = "https://www.meta.ai"
    working: bool = True
    default_model: str = 'meta-ai'

    def __init__(self, proxy: str = None, connector: Optional[BaseConnector] = None) -> None:
        """
        Инициализирует объект MetaAI.

        Args:
            proxy (str, optional): Прокси-сервер для использования. По умолчанию None.
            connector (BaseConnector, optional): Пользовательский коннектор aiohttp. По умолчанию None.
        """
        self.session: ClientSession = ClientSession(connector=get_connector(connector, proxy), headers=DEFAULT_HEADERS)
        self.cookies: Cookies | None = None
        self.access_token: str | None = None

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения ответов от Meta AI.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию None.
            **kwargs: Дополнительные аргументы.

        Yields:
            AsyncResult: Части ответа от Meta AI.
        """
        async for chunk in cls(proxy).prompt(format_prompt(messages)):
            yield chunk

    async def update_access_token(self, birthday: str = "1999-01-01") -> None:
        """
        Обновляет токен доступа.

        Args:
            birthday (str, optional): Дата рождения пользователя. По умолчанию "1999-01-01".

        Raises:
            ResponseError: Если не удается получить токен доступа.
        """
        url: str = "https://www.meta.ai/api/graphql/"
        payload: Dict[str, str | dict] = {
            "lsd": self.lsd,
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "useAbraAcceptTOSForTempUserMutation",
            "variables": json.dumps({
                "dob": birthday,
                "icebreaker_type": "TEXT",
                "__relay_internal__pv__WebPixelRatiorelayprovider": 1,
            }),
            "doc_id": "7604648749596940",
        }
        headers: Dict[str, str] = {
            "x-fb-friendly-name": "useAbraAcceptTOSForTempUserMutation",
            "x-fb-lsd": self.lsd,
            "x-asbd-id": "129477",
            "alt-used": "www.meta.ai",
            "sec-fetch-site": "same-origin"
        }
        try:
            async with self.session.post(url, headers=headers, cookies=self.cookies, data=payload) as response:
                await raise_for_status(response, "Fetch access_token failed")
                auth_json: dict = await response.json(content_type=None)
                self.access_token = auth_json["data"]["xab_abra_accept_terms_of_service"]["new_temp_user_auth"]["access_token"]
        except Exception as ex:
            logger.error('Error while fetching access token', ex, exc_info=True)
            raise

    async def prompt(self, message: str, cookies: Cookies = None) -> AsyncResult:
        """
        Отправляет запрос в Meta AI и возвращает ответ.

        Args:
            message (str): Текст сообщения.
            cookies (Cookies, optional): Cookies для аутентификации. По умолчанию None.

        Yields:
            AsyncResult: Части ответа от Meta AI.

        Raises:
            ResponseError: При возникновении ошибки в ответе от Meta AI.
        """
        if self.cookies is None:
            await self.update_cookies(cookies)
        if cookies is not None:
            self.access_token = None
        if self.access_token is None and cookies is None:
            await self.update_access_token()
        if self.access_token is None:
            url: str = "https://www.meta.ai/api/graphql/"
            payload: Dict[str, str] = {"lsd": self.lsd, 'fb_dtsg': self.dtsg}
            headers: Dict[str, str] = {'x-fb-lsd': self.lsd}
        else:
            url: str = "https://graph.meta.ai/graphql?locale=user"
            payload: Dict[str, str] = {"access_token": self.access_token}
            headers: Dict[str, str] = {}
        headers: Dict[str, str] = {
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': format_cookies(self.cookies),
            'origin': 'https://www.meta.ai',
            'referer': 'https://www.meta.ai/',
            'x-asbd-id': '129477',
            'x-fb-friendly-name': 'useAbraSendMessageMutation',
            **headers
        }
        payload: Dict[str, str | dict] = {
            **payload,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'useAbraSendMessageMutation',
            "variables": json.dumps({
                "message": {"sensitive_string_value": message},
                "externalConversationId": str(uuid.uuid4()),
                "offlineThreadingId": generate_offline_threading_id(),
                "suggestedPromptIndex": None,
                "flashVideoRecapInput": {"images": []},
                "flashPreviewInput": None,
                "promptPrefix": None,
                "entrypoint": "ABRA__CHAT__TEXT",
                "icebreaker_type": "TEXT",
                "__relay_internal__pv__AbraDebugDevOnlyrelayprovider": False,
                "__relay_internal__pv__WebPixelRatiorelayprovider": 1,
            }),
            'server_timestamps': 'true',
            'doc_id': '7783822248314888'
        }
        try:
            async with self.session.post(url, headers=headers, data=payload) as response:
                await raise_for_status(response, "Fetch response failed")
                last_snippet_len: int = 0
                fetch_id: str | None = None
                async for line in response.content:
                    if b"<h1>Something Went Wrong</h1>" in line:
                        raise ResponseError("Response: Something Went Wrong")
                    try:
                        json_line: dict = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if json_line.get("errors"):
                        raise RuntimeError("\n".join([error.get("message") for error in json_line.get("errors")]))
                    bot_response_message: dict = json_line.get("data", {}).get("node", {}).get("bot_response_message", {})
                    streaming_state: str | None = bot_response_message.get("streaming_state")
                    fetch_id = bot_response_message.get("fetch_id") or fetch_id
                    if streaming_state in ("STREAMING", "OVERALL_DONE"):
                        imagine_card: dict | None = bot_response_message.get("imagine_card")
                        if imagine_card is not None:
                            imagine_session: dict | None = imagine_card.get("session")
                            if imagine_session is not None:
                                imagine_medias: list | None = imagine_session.get("media_sets", {}).pop().get("imagine_media")
                                if imagine_medias is not None:
                                    image_class: type = ImageResponse if streaming_state == "OVERALL_DONE" else ImagePreview
                                    yield image_class([media["uri"] for media in imagine_medias], imagine_medias[0]["prompt"])
                        snippet: str = bot_response_message["snippet"]
                        new_snippet_len: int = len(snippet)
                        if new_snippet_len > last_snippet_len:
                            yield snippet[last_snippet_len:]
                            last_snippet_len = new_snippet_len

                if fetch_id is not None:
                    sources: Sources | None = await self.fetch_sources(fetch_id)
                    if sources is not None:
                        yield sources
        except Exception as ex:
            logger.error('Error while fetching response', ex, exc_info=True)
            raise

    async def update_cookies(self, cookies: Cookies = None) -> None:
        """
        Обновляет cookies для сессии.

        Args:
            cookies (Cookies, optional): Cookies для обновления. По умолчанию None.

        Raises:
            AbraGeoBlockedError: Если Meta AI недоступен в данной стране.
            ResponseError: Если не удается получить cookies.
        """
        try:
            async with self.session.get("https://www.meta.ai/", cookies=cookies) as response:
                await raise_for_status(response, "Fetch home failed")
                text: str = await response.text()
                if "AbraGeoBlockedError" in text:
                    raise AbraGeoBlockedError("Meta AI isn't available yet in your country")
                if cookies is None:
                    cookies: Cookies = {
                        "_js_datr": self.extract_value(text, "_js_datr"),
                        "abra_csrf": self.extract_value(text, "abra_csrf"),
                        "datr": self.extract_value(text, "datr"),
                    }
                self.lsd: str = self.extract_value(text, start_str='"LSD",[],{"token":"', end_str='"}')
                self.dtsg: str = self.extract_value(text, start_str='"DTSGInitialData",[],{"token":"', end_str='"}')
                self.cookies: Cookies = cookies
        except Exception as ex:
            logger.error('Error while updating cookies', ex, exc_info=True)
            raise

    async def fetch_sources(self, fetch_id: str) -> Sources | None:
        """
        Извлекает источники информации по fetch_id.

        Args:
            fetch_id (str): Идентификатор запроса.

        Returns:
            Sources | None: Объект Sources с информацией об источниках или None, если источники не найдены.

        Raises:
            ResponseError: Если не удается получить источники.
            RuntimeError: Если произошла ошибка при обработке ответа.
        """
        if self.access_token is None:
            url: str = "https://www.meta.ai/api/graphql/"
            payload: Dict[str, str] = {"lsd": self.lsd, 'fb_dtsg': self.dtsg}
            headers: Dict[str, str] = {'x-fb-lsd': self.lsd}
        else:
            url: str = "https://graph.meta.ai/graphql?locale=user"
            payload: Dict[str, str] = {"access_token": self.access_token}
            headers: Dict[str, str] = {}
        payload: Dict[str, str | dict] = {
            **payload,
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "AbraSearchPluginDialogQuery",
            "variables": json.dumps({"abraMessageFetchID": fetch_id}),
            "server_timestamps": "true",
            "doc_id": "6946734308765963",
        }
        headers: Dict[str, str] = {
            "authority": "graph.meta.ai",
            "x-fb-friendly-name": "AbraSearchPluginDialogQuery",
            **headers
        }
        try:
            async with self.session.post(url, headers=headers, cookies=self.cookies, data=payload) as response:
                await raise_for_status(response, "Fetch sources failed")
                text: str = await response.text()
                if "<h1>Something Went Wrong</h1>" in text:
                    raise ResponseError("Response: Something Went Wrong")
                try:
                    response_json: dict = json.loads(text)
                    message: dict | None = response_json["data"]["message"]
                    if message is not None:
                        searchResults: dict | None = message["searchResults"]
                        if searchResults is not None:
                            return Sources(searchResults["references"])
                except (KeyError, TypeError, json.JSONDecodeError) as ex:
                    raise RuntimeError(f"Response: {text}") from ex
        except Exception as ex:
            logger.error('Error while fetching sources', ex, exc_info=True)
            return None

    @staticmethod
    def extract_value(text: str, key: str = None, start_str: str = None, end_str: str = '",') -> str:
        """
        Извлекает значение из текста на основе заданных разделителей.

        Args:
            text (str): Текст для извлечения значения.
            key (str, optional): Ключ для поиска начального разделителя. По умолчанию None.
            start_str (str, optional): Начальный разделитель. По умолчанию None.
            end_str (str, optional): Конечный разделитель. По умолчанию '",'.

        Returns:
            str: Извлеченное значение.
        """
        if start_str is None:
            start_str: str = f'{key}":{{"value":"'
        start: int = text.find(start_str)
        if start >= 0:
            start += len(start_str)
            end: int = text.find(end_str, start)
            if end >= 0:
                return text[start:end]
        return ""


def generate_offline_threading_id() -> str:
    """
    Генерирует идентификатор для оффлайн тредов.

    Returns:
        str: Сгенерированный идентификатор.
    """
    # Generate a random 64-bit integer
    random_value: int = random.getrandbits(64)

    # Get the current timestamp in milliseconds
    timestamp: int = int(time.time() * 1000)

    # Combine timestamp and random value
    threading_id: int = (timestamp << 22) | (random_value & ((1 << 22) - 1))

    return str(threading_id)