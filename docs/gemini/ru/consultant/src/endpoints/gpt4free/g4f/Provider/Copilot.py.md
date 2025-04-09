### **Анализ кода модуля `Copilot.py`**

#### **Качество кода:**
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код содержит асинхронные функции, что позволяет эффективно обрабатывать запросы.
    - Используется `curl_cffi` для выполнения HTTP-запросов, что может повысить производительность.
    - Присутствует обработка исключений для различных ситуаций, таких как отсутствие необходимых библиотек или неверные учетные данные.
- **Минусы**:
    -  Не все переменные аннотированы типами.
    -  В коде docstring на английском. Не переведено на русский.
    -  Присутствуют закомментированные участки кода, которые следует удалить или объяснить их назначение.
    -  Смешанный стиль кавычек (используются как одинарные, так и двойные).
    -  Отсутствует единообразие в форматировании кода (пробелы вокруг операторов, отступы).
    -  Не все функции и классы имеют подробные docstring, описывающие их назначение, аргументы и возвращаемые значения.
    -  Используется `MissingRequirementsError` вместо `ModuleNotFoundError`.

#### **Рекомендации по улучшению:**
1.  **Документирование кода**:
    - Добавить docstring для всех функций, методов и классов, используя формат, указанный в инструкции. Описать назначение, аргументы, возвращаемые значения и возможные исключения.
    - Перевести docstring на русский язык.
2.  **Логирование**:
    - Использовать модуль `logger` для записи информации об ошибках и других важных событиях.
    - Добавить логирование в блоки `try...except`, чтобы упростить отладку.
3.  **Обработка исключений**:
    - Использовать конкретные типы исключений вместо общих `Exception`.
    - Добавить обработку исключений для всех потенциально опасных операций, таких как чтение файлов и сетевые запросы.
    -  Использовать `ex` вместо `e` в блоках обработки исключений.
    - заменить `MissingRequirementsError` на `ModuleNotFoundError`.
4.  **Форматирование кода**:
    - Привести код в соответствие со стандартами PEP8.
    - Использовать одинарные кавычки для строк.
    - Добавить пробелы вокруг операторов присваивания и других операторов.
5.  **Удаление неиспользуемого кода**:
    - Удалить закомментированные участки кода, которые не используются.
6.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных и параметров функций.
7.  **Рефакторинг**:
    - Заменить использование `json.load` на `j_loads` или `j_loads_ns`.
    - Убедиться, что все импорты необходимы и используются.
8.  **Вебдрайвер**:
    -  Если в коде используется вебдрайвер, используй  `driver.execute_locator(l:dict)` для взаимодействия с веб-элементами.

#### **Оптимизированный код:**
```python
"""
Модуль для взаимодействия с Microsoft Copilot
==============================================

Модуль содержит класс :class:`Copilot`, который используется для взаимодействия с Copilot API.
Он поддерживает создание завершений, стриминг, прокси и работу с медиа-файлами.

Пример использования
----------------------

>>> copilot = Copilot()
>>> messages = [{"role": "user", "content": "Hello, Copilot!"}]
>>> for response in copilot.create_completion(model="Copilot", messages=messages):
...     print(response)
"""

from __future__ import annotations

import os
import json
import asyncio
import base64
from urllib.parse import quote
from typing import Generator, Optional, List, Dict, Tuple, Any

try:
    from curl_cffi.requests import Session
    from curl_cffi import CurlWsFlag
    has_curl_cffi: bool = True
except ImportError:
    has_curl_cffi: bool = False
try:
    import nodriver
    has_nodriver: bool = True
except ImportError:
    has_nodriver: bool = False

from .base_provider import AbstractProvider, ProviderModelMixin
from .helper import format_prompt_max_length
from .openai.har_file import get_headers, get_har_files
from ..typing import CreateResult, Messages, MediaListType
from ..errors import NoValidHarFileError, MissingAuthError
from ..requests.raise_for_status import raise_for_status
from ..providers.response import (
    BaseConversation,
    JsonConversation,
    RequestLogin,
    ImageResponse,
    FinishReason,
    SuggestedFollowups,
)
from ..providers.asyncio import get_running_loop
from ..tools.media import merge_media
from ..requests import get_nodriver
from ..image import to_bytes, is_accepted_format
from .helper import get_last_user_message
from .. import debug
from src.logger import logger  # Добавлен импорт logger


class Conversation(JsonConversation):
    """
    Класс для представления идентификатора беседы.

    Attributes:
        conversation_id (str): Уникальный идентификатор беседы.
    """

    conversation_id: str

    def __init__(self, conversation_id: str):
        """
        Инициализирует экземпляр класса Conversation.

        Args:
            conversation_id (str): Уникальный идентификатор беседы.
        """
        self.conversation_id = conversation_id


class Copilot(AbstractProvider, ProviderModelMixin):
    """
    Провайдер для взаимодействия с Microsoft Copilot.

    Attributes:
        label (str): Метка провайдера.
        url (str): URL Copilot.
        working (bool): Флаг, указывающий, работает ли провайдер.
        supports_stream (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу.
        default_model (str): Модель по умолчанию.
        models (List[str]): Список поддерживаемых моделей.
        model_aliases (Dict[str, str]): Алиасы моделей.
        websocket_url (str): URL websocket для Copilot.
        conversation_url (str): URL для управления беседами.
        _access_token (Optional[str]): Токен доступа.
        _cookies (Optional[Dict[str, str]]): Cookies для аутентификации.
    """

    label: str = "Microsoft Copilot"
    url: str = "https://copilot.microsoft.com"

    working: bool = True
    supports_stream: bool = True

    default_model: str = "Copilot"
    models: List[str] = [default_model, "Think Deeper"]
    model_aliases: Dict[str, str] = {
        "gpt-4": default_model,
        "gpt-4o": default_model,
        "o1": "Think Deeper",
        "reasoning": "Think Deeper",
        "dall-e-3": default_model,
    }

    websocket_url: str = "wss://copilot.microsoft.com/c/api/chat?api-version=2"
    conversation_url: str = f"{url}/c/api/conversations"

    _access_token: Optional[str] = None
    _cookies: Optional[Dict[str, str]] = None

    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool = False,
        proxy: Optional[str] = None,
        timeout: int = 900,
        prompt: Optional[str] = None,
        media: Optional[MediaListType] = None,
        conversation: Optional[BaseConversation] = None,
        return_conversation: bool = False,
        api_key: Optional[str] = None,
        **kwargs,
    ) -> CreateResult:
        """
        Создает завершение для Copilot.

        Args:
            model (str): Используемая модель.
            messages (Messages): Список сообщений для отправки.
            stream (bool, optional): Флаг, указывающий, использовать ли потоковую передачу. По умолчанию False.
            proxy (Optional[str], optional): Адрес прокси-сервера. По умолчанию None.
            timeout (int, optional): Время ожидания запроса. По умолчанию 900.
            prompt (Optional[str], optional): Промпт для отправки. По умолчанию None.
            media (Optional[MediaListType], optional): Список медиа-файлов для отправки. По умолчанию None.
            conversation (Optional[BaseConversation], optional): Объект беседы. По умолчанию None.
            return_conversation (bool, optional): Флаг, указывающий, возвращать ли объект беседы. По умолчанию False.
            api_key (Optional[str], optional): Ключ API. По умолчанию None.
            **kwargs: Дополнительные аргументы.

        Yields:
            CreateResult: Результат завершения.

        Raises:
            ModuleNotFoundError: Если не установлены необходимые библиотеки.
            NoValidHarFileError: Если не найден действительный HAR-файл.
            MissingAuthError: Если отсутствует токен доступа.
            RuntimeError: Если произошла ошибка во время выполнения запроса.
        """
        if not has_curl_cffi:
            raise ModuleNotFoundError(
                'Установите или обновите пакет "curl_cffi" | pip install -U curl_cffi'
            )
        model = cls.get_model(model)
        websocket_url = cls.websocket_url
        headers: Optional[Dict[str, str]] = None
        if cls._access_token:
            if api_key is not None:
                cls._access_token = api_key
            if cls._access_token is None:
                try:
                    cls._access_token, cls._cookies = readHAR(cls.url)
                except NoValidHarFileError as h:
                    debug.log(f"Copilot: {h}")
                    if has_nodriver:
                        yield RequestLogin(
                            cls.label, os.environ.get("G4F_LOGIN_URL", "")
                        )
                        get_running_loop(check_nested=True)
                        cls._access_token, cls._cookies = asyncio.run(
                            get_access_token_and_cookies(cls.url, proxy)
                        )
                    else:
                        raise h
            websocket_url = f"{websocket_url}&accessToken={quote(cls._access_token)}"
            headers = {"authorization": f"Bearer {cls._access_token}"}

        with Session(
            timeout=timeout,
            proxy=proxy,
            impersonate="chrome",
            headers=headers,
            cookies=cls._cookies,
        ) as session:
            if cls._access_token is not None:
                cls._cookies = (
                    session.cookies.jar
                    if hasattr(session.cookies, "jar")
                    else session.cookies
                )
            response = session.get("https://copilot.microsoft.com/c/api/user")
            if response.status_code == 401:
                raise MissingAuthError("Status 401: Invalid access token")
            raise_for_status(response)
            user: Optional[str] = response.json().get("firstName")
            if user is None:
                cls._access_token = None
            debug.log(f"Copilot: User: {user or 'null'}")
            if conversation is None:
                response = session.post(cls.conversation_url)
                raise_for_status(response)
                conversation_id: str = response.json().get("id")
                conversation = Conversation(conversation_id)
                if return_conversation:
                    yield conversation
                if prompt is None:
                    prompt = format_prompt_max_length(messages, 10000)
                debug.log(f"Copilot: Created conversation: {conversation_id}")
            else:
                conversation_id = conversation.conversation_id
                if prompt is None:
                    prompt = get_last_user_message(messages)
                debug.log(f"Copilot: Use conversation: {conversation_id}")

            uploaded_images: List[Dict[str, str]] = []
            media, _ = [(None, None), *merge_media(media, messages)].pop()
            if media:
                if not isinstance(media, str):
                    data: bytes = to_bytes(media)
                    response = session.post(
                        "https://copilot.microsoft.com/c/api/attachments",
                        headers={"content-type": is_accepted_format(data)},
                        data=data,
                    )
                    raise_for_status(response)
                    media = response.json().get("url")
                uploaded_images.append({"type": "image", "url": media})

            wss = session.ws_connect(cls.websocket_url)
            wss.send(
                json.dumps(
                    {
                        "event": "setOptions",
                        "supportedCards": [
                            "weather",
                            "local",
                            "image",
                            "sports",
                            "video",
                            "ads",
                            "finance",
                        ],
                        "ads": {
                            "supportedTypes": [
                                "multimedia",
                                "product",
                                "tourActivity",
                                "propertyPromotion",
                                "text",
                            ]
                        },
                    }
                )
            )
            wss.send(
                json.dumps(
                    {
                        "event": "send",
                        "conversationId": conversation_id,
                        "content": [*uploaded_images, {"type": "text", "text": prompt}],
                        "mode": "reasoning" if "Think" in model else "chat",
                    }
                ).encode(),
                CurlWsFlag.TEXT,
            )

            is_started: bool = False
            msg: Optional[Dict[str, Any]] = None
            image_prompt: Optional[str] = None
            last_msg: Optional[Dict[str, Any]] = None
            try:
                while True:
                    try:
                        msg = wss.recv()[0]
                        msg = json.loads(msg)
                    except Exception as ex:  # Используем ex вместо e
                        logger.error(
                            "Ошибка при обработке сообщения websocket", ex, exc_info=True
                        )  # Логируем ошибку
                        break
                    last_msg = msg
                    if msg.get("event") == "appendText":
                        is_started = True
                        yield msg.get("text")
                    elif msg.get("event") == "generatingImage":
                        image_prompt = msg.get("prompt")
                    elif msg.get("event") == "imageGenerated":
                        yield ImageResponse(
                            msg.get("url"),
                            image_prompt,
                            {"preview": msg.get("thumbnailUrl")},
                        )
                    elif msg.get("event") == "done":
                        yield FinishReason("stop")
                        break
                    elif msg.get("event") == "suggestedFollowups":
                        yield SuggestedFollowups(msg.get("suggestions"))
                        break
                    elif msg.get("event") == "replaceText":
                        yield msg.get("text")
                    elif msg.get("event") == "error":
                        raise RuntimeError(f"Error: {msg}")
                    elif msg.get("event") not in [
                        "received",
                        "startMessage",
                        "citation",
                        "partCompleted",
                    ]:
                        debug.log(f"Copilot Message: {msg}")
                if not is_started:
                    raise RuntimeError(f"Invalid response: {last_msg}")
            finally:
                wss.close()


async def get_access_token_and_cookies(
    url: str, proxy: Optional[str] = None, target: str = "ChatAI"
) -> Tuple[Optional[str], Optional[Dict[str, str]]]:
    """
    Асинхронно получает токен доступа и cookies.

    Args:
        url (str): URL для получения токена и cookies.
        proxy (Optional[str], optional): Адрес прокси-сервера. По умолчанию None.
        target (str, optional): Цель для получения токена. По умолчанию "ChatAI".

    Returns:
        Tuple[Optional[str], Optional[Dict[str, str]]]: Токен доступа и cookies.
    """
    browser, stop_browser = await get_nodriver(proxy=proxy, user_data_dir="copilot")
    try:
        page = await browser.get(url)
        access_token: Optional[str] = None
        while access_token is None:
            access_token = await page.evaluate(
                """
                (() => {
                    for (var i = 0; i < localStorage.length; i++) {
                        try {
                            item = JSON.parse(localStorage.getItem(localStorage.key(i)));
                            if (item.credentialType == "AccessToken" 
                                && item.expiresOn > Math.floor(Date.now() / 1000)
                                && item.target.includes("target")) {
                                return item.secret;
                            }
                        } catch(e) {}
                    }
                })()
            """.replace(
                    '"target"', json.dumps(target)
                )
            )
            if access_token is None:
                await asyncio.sleep(1)
        cookies: Dict[str, str] = {}
        for c in await page.send(nodriver.cdp.network.get_cookies([url])):
            cookies[c.name] = c.value
        await page.close()
        return access_token, cookies
    finally:
        stop_browser()


def readHAR(url: str) -> Tuple[Optional[str], Optional[Dict[str, str]]]:
    """
    Считывает токен доступа и cookies из HAR-файлов.

    Args:
        url (str): URL для поиска в HAR-файлах.

    Returns:
        Tuple[Optional[str], Optional[Dict[str, str]]]: Токен доступа и cookies.

    Raises:
        NoValidHarFileError: Если не найден действительный HAR-файл.
    """
    api_key: Optional[str] = None
    cookies: Optional[Dict[str, str]] = None
    for path in get_har_files():
        with open(path, 'rb') as file:
            try:
                harFile: Dict[str, Any] = json.loads(file.read())
            except json.JSONDecodeError as ex:  # Используем ex вместо e
                logger.error(
                    "Ошибка при чтении HAR файла", ex, exc_info=True
                )  # Логируем ошибку
                continue
            for v in harFile['log']['entries']:
                if v['request']['url'].startswith(url):
                    v_headers: Dict[str, str] = get_headers(v)
                    if "authorization" in v_headers:
                        api_key = v_headers["authorization"].split(maxsplit=1).pop()
                    if v['request']['cookies']:
                        cookies = {
                            c['name']: c['value'] for c in v['request']['cookies']
                        }
    if api_key is None:
        raise NoValidHarFileError("No access token found in .har files")

    return api_key, cookies


def get_clarity() -> bytes:
    """
    Возвращает тело запроса для Clarity.

    Returns:
        bytes: Тело запроса.
    """
    # {"e":["0.7.58",5,7284,4779,"n59ae4ieqq","aln5en","1upufhz",1,0,0],"a":[[7323,12,65,217,324],[7344,12,65,214,329],[7385,12,65,211,334],[7407,12,65,210,337],[7428,12,65,209,338],[7461,12,65,209,339],[7497,12,65,209,339],[7531,12,65,208,340],[7545,12,65,208,342],[11654,13,65,208,342],[11728,14,65,208,342],[11728,9,65,208,342,17535,19455,0,0,0,"Annehmen",null,"52w7wqv1r.8ovjfyrpu",1],[7284,4,1,393,968,393,968,0,0,231,310,939,0],[12063,0,2,147,3,4,4,18,5,1,10,79,25,15],[12063,36,6,[11938,0]]]}
    body: bytes = base64.b64decode(
        "H4sIAAAAAAAAA23RwU7DMAwG4HfJ2aqS2E5ibjxH1cMOnQYqYZvUTQPx7vyJRGGAemj01XWcP+9udg+j80MetDhSyrEISc5GrqrtZnmaTydHbrdUnSsWYT2u+8Obo0Ce/IQvaDBmjkwhUlKKIRNHmQgosqEArWPRDQMx90rxeUMPzB1j+UJvwNIxhTvsPcXyX1T+rizE4juK3mEEhpAUg/JvzW1/+U/tB1LATmhqotoiweMea50PLy2vui4LOY3XfD1dwnkor5fn/e18XBFgm6fHjSzZmCyV7d3aRByAEYextaTHEH3i5pgKGVP/s+DScE5PuLKIpW6FnCi1gY3Rbpqmj0/DI/+L7QEAAA=="
    )
    return body