### **Анализ кода модуля `Gemini.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/Provider/needs_auth/Gemini.py

Модуль предоставляет класс `Gemini`, который является асинхронным генератором для взаимодействия с моделью Google Gemini.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Асинхронная реализация для неблокирующих операций.
    - Использование `ProviderModelMixin` для управления моделями.
    - Реализация автоматического обновления cookies.
    - Поддержка загрузки изображений.
- **Минусы**:
    - Многочисленные вложенные блоки `try-except` могут усложнить отладку.
    - Использование `json.loads` внутри цикла `async for` может быть неэффективным.
    - Не все переменные аннотированы типами.
    - Magic values.
    - Большой объем кода в одном классе. Желательно разбить на несколько подклассов.
    - Не все функции и методы документированы в соответствии с требованиями.
    - Не используется `j_loads` для загрузки `json`.
    - Присутствуют устаревшие конструкции, например `from __future__ import annotations`.
    - Не везде используется `logger` для логирования ошибок и информации.
    - Не используются возможности `webdriver` из проекта `hypotez`.
    - Много повторений кода, особенно в блоках обработки ошибок.
    - Не соблюдены отступы в некоторых местах, что ухудшает читаемость.

**Рекомендации по улучшению:**

1. **Документация**:
   - Добавить docstring к каждой функции и методу, включая описание аргументов, возвращаемых значений и возможных исключений.
   - Перевести все docstring на русский язык.
2. **Обработка исключений**:
   - Унифицировать обработку исключений с использованием `logger.error` и передачей исключения `ex`.
   - Избегать слишком общих блоков `except Exception as e`, заменяя их на более конкретные исключения.
3. **Типизация**:
   - Добавить аннотации типов для всех переменных и параметров функций.
4. **Логирование**:
   - Использовать `logger` для записи информации о процессе работы, особенно при обновлении cookies и загрузке изображений.
5. **Рефакторинг**:
   - Разбить класс `Gemini` на несколько подклассов для улучшения читаемости и поддержки.
   - Вынести повторяющийся код в отдельные функции.
6. **Cookies**:
   - Использовать `j_loads` для загрузки cookies из файла.
7. **Удалить устаревшие конструкции**:
   - Убрать `from __future__ import annotations`.
8. **Использовать webdriver**:
   - Переписать функции `nodriver_login` с использованием `webdriver` из `hypotez`.
9. **Обработка JSON**:
   - Использовать более надежные способы обработки JSON, чтобы избежать `ValueError` при парсинге.
10. **Улучшение читаемости**:
    - Следовать стандартам PEP8 для форматирования кода, включая пробелы вокруг операторов и отступы.

**Оптимизированный код:**

```python
"""
Модуль для работы с моделью Google Gemini
=========================================

Модуль содержит класс :class:`Gemini`, который используется для взаимодействия с моделью Google Gemini через асинхронный генератор.
Поддерживает автоматическое обновление cookies и загрузку изображений.

Пример использования
----------------------

>>> gemini = Gemini()
>>> async for chunk in gemini.create_async_generator(model="gemini-2.0-flash", messages=[{"role": "user", "content": "Hello"}]):
...     print(chunk, end="")
"""
from __future__ import annotations

import asyncio
import base64
import json
import os
import random
import re
import time
from pathlib import Path
from urllib.parse import quote_plus, unquote_plus

from aiohttp import ClientSession, BaseConnector

from src.logger import logger  # Используем logger из src.logger
from ... import debug
from ...typing import Messages, Cookies, MediaListType, AsyncResult, AsyncIterator
from ...providers.response import JsonConversation, Reasoning, RequestLogin, ImageResponse, YouTube
from ...requests.raise_for_status import raise_for_status
from ...requests.aiohttp import get_connector
from ...requests import get_nodriver
from ...errors import MissingAuthError
from ...image import to_bytes
from ...cookies import get_cookies_dir
from ...tools.media import merge_media
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..helper import format_prompt, get_cookies, get_last_user_message

REQUEST_HEADERS: dict[str, str] = {
    "authority": "gemini.google.com",
    "origin": "https://gemini.google.com",
    "referer": "https://gemini.google.com/",
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'x-same-domain': '1',
}
REQUEST_BL_PARAM: str = "boq_assistant-bard-web-server_20240519.16_p0"
REQUEST_URL: str = "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate"
UPLOAD_IMAGE_URL: str = "https://content-push.googleapis.com/upload/"
UPLOAD_IMAGE_HEADERS: dict[str, str] = {
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
GOOGLE_COOKIE_DOMAIN: str = ".google.com"
ROTATE_COOKIES_URL: str = "https://accounts.google.com/RotateCookies"
GGOGLE_SID_COOKIE: str = "__Secure-1PSID"

models: dict[str, dict[str, str]] = {
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
    Класс для взаимодействия с моделью Google Gemini.
    """
    label: str = "Google Gemini"
    url: str = "https://gemini.google.com"
    needs_auth: bool = True
    working: bool = True
    use_nodriver: bool = True

    default_model: str = ""
    default_image_model: str = default_model
    default_vision_model: str = default_model
    image_models: list[str] = [default_image_model]
    models: list[str] = [
        default_model, *models.keys()
    ]
    model_aliases: dict[str, str] = {"gemini-2.0": ""}

    synthesize_content_type: str = "audio/vnd.wav"

    _cookies: Cookies | None = None
    _snlm0e: str | None = None
    _sid: str | None = None

    auto_refresh: bool = True
    refresh_interval: int = 540
    rotate_tasks: dict[str, asyncio.Task] = {}

    @classmethod
    async def nodriver_login(cls, proxy: str | None = None) -> AsyncIterator[str] | None:
        """
        Автоматически проходит процесс логина с использованием nodriver для получения cookies.

        Args:
            proxy (str | None): Прокси для использования.

        Yields:
            AsyncIterator[str] | None: Часть страницы логина или None в случае ошибки.
        """
        if not hasattr(cls, 'has_nodriver'):
            try:
                import nodriver
                cls.has_nodriver = True
            except ImportError:
                cls.has_nodriver = False

        if not cls.has_nodriver:
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
            cookies = {}
            for c in await page.send(nodriver.cdp.network.get_cookies([cls.url])):
                cookies[c.name] = c.value
            await page.close()
            cls._cookies = cookies
        except Exception as ex:
            logger.error('Error while nodriver login', ex, exc_info=True)
        finally:
            stop_browser()

    @classmethod
    async def start_auto_refresh(cls, proxy: str | None = None) -> None:
        """
        Запускает фоновую задачу для автоматического обновления cookies.
        """
        while True:
            try:
                new_1psidts = await rotate_1psidts(cls.url, cls._cookies, proxy)
            except Exception as ex:
                logger.error(f"Failed to refresh cookies: {ex}", exc_info=True)
                task = cls.rotate_tasks.get(cls._cookies[GGOGLE_SID_COOKIE])
                if task:
                    task.cancel()
                logger.error(
                    "Failed to refresh cookies. Background auto refresh task canceled."
                )
                continue  # Добавлено для продолжения цикла

            debug.log(f"Gemini: Cookies refreshed. New __Secure-1PSIDTS: {new_1psidts}")
            if new_1psidts:
                cls._cookies["__Secure-1PSIDTS"] = new_1psidts
            await asyncio.sleep(cls.refresh_interval)

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str | None = None,
        cookies: Cookies | None = None,
        connector: BaseConnector | None = None,
        media: MediaListType | None = None,
        return_conversation: bool = False,
        conversation: "Conversation" | None = None,
        language: str = "en",
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения ответов от модели Gemini.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений для отправки.
            proxy (str | None): Прокси для использования.
            cookies (Cookies | None): Cookies для использования.
            connector (BaseConnector | None): Connector для использования.
            media (MediaListType | None): Медиафайлы для отправки.
            return_conversation (bool): Флаг для возврата объекта Conversation.
            conversation (Conversation | None): Объект Conversation для продолжения диалога.
            language (str): Язык ответа.
            **kwargs: Дополнительные аргументы.

        Yields:
            AsyncIterator[str]: Часть ответа от модели.
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
                            def read_recusive(data):
                                for item in data:
                                    if isinstance(item, list):
                                        yield from read_recusive(item)
                                    elif isinstance(item, str) and not item.startswith("rc_"):\
                                        yield item
                            def find_str(data, skip=0):
                                for item in read_recusive(data):
                                    if skip > 0:
                                        skip -= 1
                                        continue
                                    yield item
                            reasoning = "\\n\\n".join(find_str(response_part[4][0], 3))
                            reasoning = re.sub(r"<b>|</b>", "**", reasoning)
                            def replace_image(match):
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
                            logger.error(f"{cls.__name__} {type(ex).__name__}: {ex}", exc_info=True)
                            continue
                        match = re.search(r'\\[Imagen of (.*?)\\]', content)
                        if match:
                            image_prompt = match.group(1)
                            content = content.replace(match.group(0), '')
                        pattern = r"http://googleusercontent.com/(?:image_generation|youtube|map)_content/\\d+"
                        content = re.sub(pattern, "", content)
                        content = content.replace("<!-- end list -->", "")
                        def replace_link(match):
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
                                logger.error(f"{cls.__name__} {type(ex).__name__}: {ex}", exc_info=True)
                                pass
                        youtube_ids = []
                        pattern = re.compile(r"http://www.youtube.com/watch\\?v=([\\w-]+)")
                        for match in pattern.finditer(content):
                            if match.group(1) not in youtube_ids:
                                youtube_ids.append(match.group(1))
                        if youtube_ids:
                            yield YouTube(youtube_ids)

    @classmethod
    async def synthesize(cls, params: dict[str, str], proxy: str | None = None) -> AsyncIterator[bytes]:
        """
        Синтезирует речь из текста с использованием модели Gemini.

        Args:
            params (dict[str, str]): Параметры для синтеза речи, включая текст.
            proxy (str | None): Прокси для использования.

        Yields:
            AsyncIterator[bytes]: Аудиоданные в формате bytes.

        Raises:
            ValueError: Если отсутствует параметр "text".
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
        conversation: "Conversation" | None = None,
        uploads: list[list[str, str]] | None = None,
        tools: list[list[str]] = []
    ) -> list:
        """
        Создает запрос к модели Gemini.

        Args:
            prompt (str): Текст запроса.
            language (str): Язык запроса.
            conversation (Conversation | None): Объект Conversation для продолжения диалога.
            uploads (list[list[str, str]] | None): Список загруженных изображений.
            tools (list[list[str]]): Список инструментов для использования.

        Returns:
            list: Список параметров запроса.
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

    async def upload_images(connector: BaseConnector, media: MediaListType) -> list[list[str, str]]:
        """
        Загружает изображения на сервер Gemini.

        Args:
            connector (BaseConnector): Connector для использования.
            media (MediaListType): Список медиафайлов для загрузки.

        Returns:
            list[list[str, str]]: Список URL загруженных изображений и их имен.
        """
        async def upload_image(image: bytes, image_name: str | None = None) -> list[str, str]:
            """
            Загружает одно изображение на сервер Gemini.

            Args:
                image (bytes): Изображение в формате bytes.
                image_name (str | None): Имя изображения.

            Returns:
                list[str, str]: URL загруженного изображения и его имя.
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
        Получает значение SNlM0e из cookies.

        Args:
            session (ClientSession): Сессия для выполнения запроса.
            cookies (Cookies): Cookies для использования.
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
    Класс для представления истории диалога.
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
            conversation_id (str): ID диалога.
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
    """
    search_for = b'[["wrb.fr","XqA3Ic","[\\\\"\'
    end_with = b'\\\\'
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

async def rotate_1psidts(url: str, cookies: dict[str, str], proxy: str | None = None) -> str | None:
    """
    Обновляет cookie __Secure-1PSIDTS.

    Args:
        url (str): URL для запроса.
        cookies (dict[str, str]): Текущие cookies.
        proxy (str | None): Прокси для использования.

    Returns:
        str | None: Новое значение __Secure-1PSIDTS или None в случае ошибки.
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
            path.write_text(json.dumps([{\
                "name": k,\
                "value": v,\
                "domain": GOOGLE_COOKIE_DOMAIN,\
            } for k, v in cookies.items()]))
            if new_1psidts:
                return new_1psidts
    return None