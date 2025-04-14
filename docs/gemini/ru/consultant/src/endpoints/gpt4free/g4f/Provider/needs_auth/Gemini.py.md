### **Анализ кода модуля `Gemini.py`**

**Расположение файла в проекте:** `hypotez/src/endpoints/gpt4free/g4f/Provider/needs_auth/Gemini.py`

**Описание:** Модуль предоставляет класс `Gemini`, который является асинхронным генератором для взаимодействия с моделью Google Gemini. Он поддерживает аутентификацию, обновление cookies и загрузку изображений.

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Асинхронная реализация для неблокирующего взаимодействия.
    - Поддержка cookies и их автоматическое обновление.
    - Обработка загрузки изображений.
    - Использование `nodriver` для автоматической аутентификации.
- **Минусы**:
    - Некоторые части кода сложны для понимания из-за большого количества вложенных структур данных и обработки строк.
    - Не все функции имеют подробные docstring.
    - Отсутствуют логирования во многих местах.
    - Не везде используются аннотации типов.

**Рекомендации по улучшению:**

1.  **Документация**:
    *   Добавить подробные docstring для всех функций и методов, включая описание параметров, возвращаемых значений и возможных исключений.
    *   Улучшить комментарии для сложных участков кода, чтобы сделать их более понятными.
2.  **Логирование**:
    *   Добавить логирование с использованием `logger` из `src.logger` для отслеживания ошибок и важных событий.
3.  **Обработка исключений**:
    *   Убедиться, что все исключения обрабатываются с использованием `logger.error` для логирования ошибок.
4.  **Типизация**:
    *   Добавить аннотации типов для всех переменных и параметров функций, где это необходимо.
5.  **Рефакторинг**:
    *   Разбить некоторые функции на более мелкие, чтобы улучшить читаемость и упростить отладку.
    *   Упростить обработку строк и JSON-данных, чтобы уменьшить сложность кода.

**Оптимизированный код:**

```python
from __future__ import annotations

import os
import json
import random
import re
import base64
import asyncio
import time

from urllib.parse import quote_plus, unquote_plus
from pathlib import Path
from aiohttp import ClientSession, BaseConnector
from typing import Generator, Optional, List, AsyncIterator, Dict, Any, Tuple

from src.logger import logger  # Import logger
from ... import debug
from ...typing import Messages, Cookies, MediaListType, AsyncResult
from ...providers.response import JsonConversation, Reasoning, RequestLogin, ImageResponse, YouTube
from ...requests.raise_for_status import raise_for_status
from ...requests.aiohttp import get_connector
from ...requests import get_nodriver
from ...errors import MissingAuthError
from ...image import to_bytes
from ...cookies import get_cookies_dir
from ...tools.media import merge_media
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin

try:
    import nodriver
    has_nodriver = True
except ImportError:
    has_nodriver = False

REQUEST_HEADERS = {
    "authority": "gemini.google.com",
    "origin": "https://gemini.google.com",
    "referer": "https://gemini.google.com/",
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'x-same-domain': '1',
}
REQUEST_BL_PARAM = "boq_assistant-bard-web-server_20240519.16_p0"
REQUEST_URL = "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate"
UPLOAD_IMAGE_URL = "https://content-push.googleapis.com/upload/"
UPLOAD_IMAGE_HEADERS = {
    "authority": "content-push.googleapis.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.7",
    "authorization": "Basic c2F2ZXM6cyNMdGhlNmxzd2F2b0RsN3J1d1U=",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "origin": "https://gemini.google.com",
    "push-id": "feeds/mcudyrk2a4khkz",
    "referer": "https://gemini.google.com/",
    "x-goog-upload-command": "start",
    "x-goog-upload-header-content-length": "",
    "x-goog-upload-protocol": "resumable",
    "x-tenant-id": "bard-storage",
}
GOOGLE_COOKIE_DOMAIN = ".google.com"
ROTATE_COOKIES_URL = "https://accounts.google.com/RotateCookies"
GGOGLE_SID_COOKIE = "__Secure-1PSID"

models = {
    "gemini-2.0-flash": {"x-goog-ext-525001261-jspb": '[null,null,null,null,"f299729663a2343f"]'},
    "gemini-2.0-flash-exp": {"x-goog-ext-525001261-jspb": '[null,null,null,null,"f299729663a2343f"]'},
    "gemini-2.0-flash-thinking": {"x-goog-ext-525001261-jspb": '[null,null,null,null,"9c17b1863f581b8a"]'},
    "gemini-2.0-flash-thinking-with-apps": {"x-goog-ext-525001261-jspb": '[null,null,null,null,"f8f8f5ea629f5d37"]'},
    "gemini-2.0-exp-advanced": {"x-goog-ext-525001261-jspb": '[null,null,null,null,"b1e46a6037e6aa9f"]'},
    "gemini-1.5-flash": {"x-goog-ext-525001261-jspb": '[null,null,null,null,"418ab5ea040b5c43"]'},
    "gemini-1.5-pro": {"x-goog-ext-525001261-jspb": '[null,null,null,null,"9d60dfae93c9ff1f"]'},
    "gemini-1.5-pro-research": {"x-goog-ext-525001261-jspb": '[null,null,null,null,"e5a44cb1dae2b489"]'},
}


class Gemini(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Класс для взаимодействия с Google Gemini API.
    """
    label: str = "Google Gemini"
    url: str = "https://gemini.google.com"
    needs_auth: bool = True
    working: bool = True
    use_nodriver: bool = True
    default_model: str = ""
    default_image_model: str = default_model
    default_vision_model: str = default_model
    image_models: List[str] = [default_image_model]
    models: List[str] = [
        default_model, *models.keys()
    ]
    model_aliases: Dict[str, str] = {"gemini-2.0": ""}
    synthesize_content_type: str = "audio/vnd.wav"
    _cookies: Cookies = None
    _snlm0e: str = None
    _sid: str = None
    auto_refresh: bool = True
    refresh_interval: int = 540
    rotate_tasks: Dict[str, asyncio.Task] = {}

    @classmethod
    async def nodriver_login(cls, proxy: Optional[str] = None) -> AsyncIterator[str]:
        """
        Автоматически выполняет вход в Gemini с использованием nodriver.

        Args:
            proxy (Optional[str]): Прокси-сервер для использования.

        Yields:
            AsyncIterator[str]: Части ответа, содержащие информацию о процессе входа.

        Raises:
            ImportError: Если модуль nodriver не установлен.
            Exception: Если во время входа произошла ошибка.
        """
        if not has_nodriver:
            if debug.logging:
                print("Skip nodriver login in Gemini provider")
            return

        browser, stop_browser = await get_nodriver(proxy=proxy, user_data_dir="gemini")
        try:
            login_url = os.environ.get("G4F_LOGIN_URL")
            if login_url:
                yield RequestLogin(cls.label, login_url)
            page = await browser.get(f"{cls.url}/app")
            await page.select("div.ql-editor.textarea", 240)
            cookies: Dict[str, str] = {}
            for c in await page.send(nodriver.cdp.network.get_cookies([cls.url])):
                cookies[c.name] = c.value
            await page.close()
            cls._cookies = cookies
        except Exception as ex:
            logger.error('Error during nodriver login', ex, exc_info=True)  # Log the error
        finally:
            stop_browser()

    @classmethod
    async def start_auto_refresh(cls, proxy: str = None) -> None:
        """
        Запускает фоновую задачу для автоматического обновления cookies.
        """
        while True:
            try:
                new_1psidts = await rotate_1psidts(cls.url, cls._cookies, proxy)
            except Exception as ex:
                logger.error(f"Failed to refresh cookies: {ex}", exc_info=True)  # Log the error
                task = cls.rotate_tasks.get(cls._cookies[GGOGLE_SID_COOKIE])
                if task:
                    task.cancel()
                logger.error(
                    "Failed to refresh cookies. Background auto refresh task canceled."
                )

            debug.log(f"Gemini: Cookies refreshed. New __Secure-1PSIDTS: {new_1psidts}")
            if new_1psidts:
                cls._cookies["__Secure-1PSIDTS"] = new_1psidts
            await asyncio.sleep(cls.refresh_interval)

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: Optional[str] = None,
        cookies: Optional[Cookies] = None,
        connector: Optional[BaseConnector] = None,
        media: Optional[MediaListType] = None,
        return_conversation: bool = False,
        conversation: Optional[Conversation] = None,
        language: str = "en",
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с Gemini.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            proxy (Optional[str]): Прокси-сервер для использования.
            cookies (Optional[Cookies]): Cookies для аутентификации.
            connector (Optional[BaseConnector]): Коннектор для aiohttp.
            media (Optional[MediaListType]): Список медиафайлов для отправки.
            return_conversation (bool): Флаг, указывающий, нужно ли возвращать информацию о разговоре.
            conversation (Optional[Conversation]): Объект разговора.
            language (str): Язык ответа.

        Yields:
            AsyncIterator[str | Conversation | Reasoning | ImageResponse | YouTube]: Части ответа от Gemini.

        Raises:
            MissingAuthError: Если отсутствует cookie "__Secure-1PSID".
            RuntimeError: Если не удалось получить SNlM0e.
            Exception: Если во время создания генератора произошла ошибка.
        """
        cls._cookies = cookies or cls._cookies or get_cookies(GOOGLE_COOKIE_DOMAIN, False, True)
        if conversation is not None and getattr(conversation, "model", None) != model:
            conversation = None
        prompt = format_prompt(messages) if conversation is None else get_last_user_message(messages)
        base_connector = get_connector(connector, proxy)

        async with ClientSession(
            headers=REQUEST_HEADERS,
            connector=base_connector
        ) as session:
            if not cls._snlm0e:
                await cls.fetch_snlm0e(session, cls._cookies) if cls._cookies else None
            if not cls._snlm0e:
                try:
                    async for chunk in cls.nodriver_login(proxy):
                        yield chunk
                except Exception as ex:
                    raise MissingAuthError('Missing or invalid "__Secure-1PSID" cookie', ex)
            if not cls._snlm0e:
                if cls._cookies is None or "__Secure-1PSID" not in cls._cookies:
                    raise MissingAuthError('Missing "__Secure-1PSID" cookie')
                await cls.fetch_snlm0e(session, cls._cookies)
            if not cls._snlm0e:
                raise RuntimeError("Invalid cookies. SNlM0e not found")
            if GGOGLE_SID_COOKIE in cls._cookies:
                task = cls.rotate_tasks.get(cls._cookies[GGOGLE_SID_COOKIE])
                if not task:
                    cls.rotate_tasks[cls._cookies[GGOGLE_SID_COOKIE]] = asyncio.create_task(
                        cls.start_auto_refresh()
                    )

            uploads = await cls.upload_images(base_connector, merge_media(media, messages))
            async with ClientSession(
                cookies=cls._cookies,
                headers=REQUEST_HEADERS,
                connector=base_connector,
            ) as client:
                params = {
                    'bl': REQUEST_BL_PARAM,
                    'hl': language,
                    '_reqid': random.randint(1111, 9999),
                    'rt': 'c',
                    "f.sid": cls._sid,
                }
                data = {
                    'at': cls._snlm0e,
                    'f.req': json.dumps([None, json.dumps(cls.build_request(
                        prompt,
                        language=language,
                        conversation=conversation,
                        uploads=uploads
                    ))])
                }
                async with client.post(
                    REQUEST_URL,
                    data=data,
                    params=params,
                    headers=models[model] if model in models else None
                ) as response:
                    await raise_for_status(response)
                    image_prompt = response_part = None
                    last_content = ""
                    async for line in response.content:
                        try:
                            try:
                                line = json.loads(line)
                            except ValueError:
                                continue
                            if not isinstance(line, list):
                                continue
                            if len(line[0]) < 3 or not line[0][2]:
                                continue
                            response_part = json.loads(line[0][2])
                            if not response_part[4]:
                                continue
                            if return_conversation:
                                yield Conversation(response_part[1][0], response_part[1][1], response_part[4][0][0], model)
                            def read_recusive(data: list) -> Generator[Any, None, None]:
                                """
                                Рекурсивно читает данные из списка.

                                Args:
                                    data (list): Список для чтения.

                                Yields:
                                    Any: Элементы списка.
                                """
                                for item in data:
                                    if isinstance(item, list):
                                        yield from read_recusive(item)
                                    elif isinstance(item, str) and not item.startswith("rc_"):
                                        yield item
                            def find_str(data: list, skip: int = 0) -> Generator[str, None, None]:
                                """
                                Находит строки в данных, пропуская определенное количество элементов.

                                Args:
                                    data (list): Список для поиска.
                                    skip (int): Количество элементов для пропуска.

                                Yields:
                                    str: Найденные строки.
                                """
                                for item in read_recusive(data):
                                    if skip > 0:
                                        skip -= 1
                                        continue
                                    yield item
                            reasoning = "\\n\\n".join(find_str(response_part[4][0], 3))
                            reasoning = re.sub(r"<b>|</b>", "**", reasoning)
                            def replace_image(match: re.Match) -> str:
                                """
                                Заменяет URL изображения в тексте.

                                Args:
                                    match (re.Match): Объект соответствия регулярного выражения.

                                Returns:
                                    str: URL изображения в формате Markdown.
                                """
                                return f"![](https:{match.group(0)})"
                            reasoning = re.sub(r"//yt3.(?:ggpht.com|googleusercontent.com/ytc)/[\\w=-]+", replace_image, reasoning)
                            reasoning = re.sub(r"\\nyoutube\\n", "\\n\\n\\n", reasoning)
                            reasoning = re.sub(r"\\nyoutube_tool\\n", "\\n\\n", reasoning)
                            reasoning = re.sub(r"\\nYouTube\\n", "\\nYouTube ", reasoning)
                            reasoning = reasoning.replace('\\nhttps://www.gstatic.com/images/branding/productlogos/youtube/v9/192px.svg', '<i class="fa-brands fa-youtube"></i>')
                            content = response_part[4][0][1][0]
                            if reasoning:
                                yield Reasoning(reasoning, status="🤔")
                        except (ValueError, KeyError, TypeError, IndexError) as ex:
                            logger.error(f"{cls.__name__} {type(ex).__name__}: {ex}", exc_info=True)  # Log the error
                            continue
                        match = re.search(r'\\[Imagen of (.*?)\\]', content)
                        if match:
                            image_prompt = match.group(1)
                            content = content.replace(match.group(0), '')
                        pattern = r"http://googleusercontent.com/(?:image_generation|youtube|map)_content/\\d+"
                        content = re.sub(pattern, "", content)
                        content = content.replace("<!-- end list -->", "")
                        def replace_link(match: re.Match) -> str:
                            """
                            Заменяет URL ссылок в тексте.

                            Args:
                                match (re.Match): Объект соответствия регулярного выражения.

                            Returns:
                                str: URL ссылки в формате Markdown.
                            """
                            return f"(https://{quote_plus(unquote_plus(match.group(1)), '/?&=#')})"
                        content = re.sub(r"\\(https://www.google.com/(?:search\\?q=|url\\?sa=E&source=gmail&q=)https?://(.+?)\\)", replace_link, content)

                        if last_content and content.startswith(last_content):
                            yield content[len(last_content):]
                        else:
                            yield content
                        last_content = content
                        if image_prompt:
                            try:
                                images = [image[0][3][3] for image in response_part[4][0][12][7][0]]
                                image_prompt = image_prompt.replace("a fake image", "")
                                yield ImageResponse(images, image_prompt, {"cookies": cls._cookies})
                            except (TypeError, IndexError, KeyError) as ex:
                                logger.error(f"Error processing image response: {ex}", exc_info=True)  # Log the error
                                pass
                        youtube_ids = []
                        pattern = re.compile(r"http://www.youtube.com/watch\\?v=([\\w-]+)")
                        for match in pattern.finditer(content):
                            if match.group(1) not in youtube_ids:
                                youtube_ids.append(match.group(1))
                        if youtube_ids:
                            yield YouTube(youtube_ids)

    @classmethod
    async def synthesize(cls, params: dict, proxy: Optional[str] = None) -> AsyncIterator[bytes]:
        """
        Синтезирует речь на основе заданного текста.

        Args:
            params (dict): Параметры запроса, содержащие текст для синтеза.
            proxy (Optional[str]): Прокси-сервер для использования.

        Yields:
            AsyncIterator[bytes]: Аудиоданные в формате bytes.

        Raises:
            ValueError: Если отсутствует параметр "text".
            Exception: Если во время синтеза произошла ошибка.
        """
        if "text" not in params:
            raise ValueError("Missing parameter text")
        async with ClientSession(
            cookies=cls._cookies,
            headers=REQUEST_HEADERS,
            connector=get_connector(proxy=proxy),
        ) as session:
            if not cls._snlm0e:
                await cls.fetch_snlm0e(session, cls._cookies) if cls._cookies else None
            inner_data = json.dumps([None, params["text"], "en-US", None, 2])
            async with session.post(
                "https://gemini.google.com/_/BardChatUi/data/batchexecute",
                data={
                      "f.req": json.dumps([[["XqA3Ic", inner_data, None, "generic"]]]),
                      "at": cls._snlm0e,
                },
                params={
                    "rpcids": "XqA3Ic",
                    "source-path": "/app/2704fb4aafcca926",
                    "bl": "boq_assistant-bard-web-server_20241119.00_p1",
                    "f.sid": "" if cls._sid is None else cls._sid,
                    "hl": "de",
                    "_reqid": random.randint(1111, 9999),
                    "rt": "c"
                },
            ) as response:
                await raise_for_status(response)
                iter_base64_response = iter_filter_base64(response.content.iter_chunked(1024))
                async for chunk in iter_base64_decode(iter_base64_response):
                    yield chunk

    def build_request(
        prompt: str,
        language: str,
        conversation: Optional[Conversation] = None,
        uploads: Optional[List[Tuple[str, str]]] = None,
        tools: List[List[str]] = []
    ) -> list:
        """
        Создает запрос к Gemini API.

        Args:
            prompt (str): Текст запроса.
            language (str): Язык запроса.
            conversation (Optional[Conversation]): Объект разговора.
            uploads (Optional[List[Tuple[str, str]]]): Список загруженных изображений.
            tools (List[List[str]]): Список инструментов для использования.

        Returns:
            list: Сформированный запрос.
        """
        image_list = [[[image_url, 1], image_name] for image_url, image_name in uploads] if uploads else []
        return [
            [prompt, 0, None, image_list, None, None, 0],
            [language],
            [
                None if conversation is None else conversation.conversation_id,
                None if conversation is None else conversation.response_id,
                None if conversation is None else conversation.choice_id,
                None,
                None,
                []
            ],
            None,
            None,
            None,
            [1],
            0,
            [],
            tools,
            1,
            0,
        ]

    async def upload_images(connector: BaseConnector, media: MediaListType) -> List[List[str]]:
        """
        Загружает изображения на сервер Gemini.

        Args:
            connector (BaseConnector): Коннектор для aiohttp.
            media (MediaListType): Список медиафайлов для загрузки.

        Returns:
            List[List[str]]: Список URL загруженных изображений.

        Raises:
            Exception: Если во время загрузки изображения произошла ошибка.
        """
        async def upload_image(image: bytes, image_name: str = None) -> List[str]:
            """
            Загружает одно изображение на сервер.

            Args:
                image (bytes): Изображение в формате bytes.
                image_name (str): Имя изображения.

            Returns:
                List[str]: URL загруженного изображения и имя файла.
            """
            async with ClientSession(
                headers=UPLOAD_IMAGE_HEADERS,
                connector=connector
            ) as session:
                image = to_bytes(image)

                async with session.options(UPLOAD_IMAGE_URL) as response:
                    await raise_for_status(response)

                headers = {
                    "size": str(len(image)),
                    "x-goog-upload-command": "start"
                }
                data = f"File name: {image_name}" if image_name else None
                async with session.post(
                    UPLOAD_IMAGE_URL, headers=headers, data=data
                ) as response:
                    await raise_for_status(response)
                    upload_url = response.headers["X-Goog-Upload-Url"]

                async with session.options(upload_url, headers=headers) as response:
                    await raise_for_status(response)

                headers["x-goog-upload-command"] = "upload, finalize"
                headers["X-Goog-Upload-Offset"] = "0"
                async with session.post(
                    upload_url, headers=headers, data=image
                ) as response:
                    await raise_for_status(response)
                    return [await response.text(), image_name]
        return await asyncio.gather(*[upload_image(image, image_name) for image, image_name in media])

    @classmethod
    async def fetch_snlm0e(cls, session: ClientSession, cookies: Cookies) -> None:
        """
        Извлекает значение SNlM0e из ответа сервера.

        Args:
            session (ClientSession): Сессия aiohttp.
            cookies (Cookies): Cookies для запроса.

        Raises:
            Exception: Если не удалось получить SNlM0e.
        """
        async with session.get(cls.url, cookies=cookies) as response:
            await raise_for_status(response)
            response_text = await response.text()
        match = re.search(r'SNlM0e\\":\\"(.*?)\\"', response_text)
        if match:
            cls._snlm0e = match.group(1)
        sid_match = re.search(r'"FdrFJe":"([\d-]+)"', response_text)
        if sid_match:
            cls._sid = sid_match.group(1)

class Conversation(JsonConversation):
    """
    Класс для хранения информации о разговоре.
    """
    def __init__(self,
        conversation_id: str,
        response_id: str,
        choice_id: str,
        model: str
    ) -> None:
        """
        Инициализирует объект Conversation.

        Args:
            conversation_id (str): ID разговора.
            response_id (str): ID ответа.
            choice_id (str): ID выбора.
            model (str): Используемая модель.
        """
        self.conversation_id = conversation_id
        self.response_id = response_id
        self.choice_id = choice_id
        self.model = model

async def iter_filter_base64(chunks: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    """
    Фильтрует base64 данные из чанков.

    Args:
        chunks (AsyncIterator[bytes]): Асинхронный итератор байтовых чанков.

    Yields:
        AsyncIterator[bytes]: Отфильтрованные байтовые чанки.

    Raises:
        ValueError: Если ответ не содержит ожидаемые данные.
    """
    search_for = b'[["wrb.fr","XqA3Ic","[\\\\"\'
    end_with = b'\\\\\'
    is_started = False
    async for chunk in chunks:
        if is_started:
            if end_with in chunk:
                yield chunk.split(end_with, maxsplit=1).pop(0)
                break
            else:
                yield chunk
        elif search_for in chunk:
            is_started = True
            yield chunk.split(search_for, maxsplit=1).pop()
        else:
            raise ValueError(f"Response: {chunk}")

async def iter_base64_decode(chunks: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    """
    Декодирует base64 данные из чанков.

    Args:
        chunks (AsyncIterator[bytes]): Асинхронный итератор байтовых чанков.

    Yields:
        AsyncIterator[bytes]: Декодированные байтовые чанки.
    """
    buffer = b""
    rest = 0
    async for chunk in chunks:
        chunk = buffer + chunk
        rest = len(chunk) % 4
        buffer = chunk[-rest:]
        yield base64.b64decode(chunk[:-rest])
    if rest > 0:
        yield base64.b64decode(buffer+rest*b"=")

async def rotate_1psidts(url: str, cookies: dict, proxy: Optional[str] = None) -> str:
    """
    Обновляет cookie "__Secure-1PSIDTS".

    Args:
        url (str): URL для запроса.
        cookies (dict): Cookies для запроса.
        proxy (Optional[str]): Прокси-сервер для использования.

    Returns:
        str: Новое значение cookie "__Secure-1PSIDTS".

    Raises:
        MissingAuthError: Если cookies невалидны.
        Exception: Если во время обновления произошла ошибка.
    """
    path = Path(get_cookies_dir())
    path.mkdir(parents=True, exist_ok=True)
    filename = f"auth_Gemini.json"
    path = path / filename

    # Check if the cache file was modified in the last minute to avoid 429 Too Many Requests
    if not (path.is_file() and time.time() - os.path.getmtime(path) <= 60):
        async with ClientSession(proxy=proxy) as client:
            response = await client.post(
                url=ROTATE_COOKIES_URL,
                headers={
                    "Content-Type": "application/json",
                },
                cookies=cookies,
                data='[000,"-0000000000000000000"]',
            )
            if response.status == 401:
                raise MissingAuthError("Invalid cookies")
            response.raise_for_status()
            for key, c in response.cookies.items():
                cookies[key] = c.value
            new_1psidts = response.cookies.get("__Secure-1PSIDTS")
            path.write_text(json.dumps([
                {"name": k, "value": v, "domain": GOOGLE_COOKIE_DOMAIN} for k, v in cookies.items()
            ]))
            if new_1psidts:
                return new_1psidts