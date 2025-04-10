### **Анализ кода модуля `MetaAI.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование асинхронных операций для неблокирующего выполнения.
    - Наличие обработки исключений.
    - Реализация методов для обновления cookies и access token.
- **Минусы**:
    - Отсутствие аннотаций типов для переменных класса и параметров методов.
    - Смешанный стиль кавычек (использование как одинарных, так и двойных кавычек).
    - Не все методы имеют docstring.
    - Не используется `logger` для логирования ошибок.
    - Не используется `j_loads` для чтения JSON.

**Рекомендации по улучшению:**

1.  **Добавить docstring**: Добавить подробные docstring для всех классов и методов, включая описание параметров, возвращаемых значений и возможных исключений.
2.  **Использовать логирование**: Заменить `print` на `logger.error` для логирования ошибок с указанием `exc_info=True`.
3.  **Аннотации типов**: Добавить аннотации типов для всех переменных и параметров функций.
4.  **Унифицировать кавычки**: Использовать только одинарные кавычки для строк.
5.  **Использовать `j_loads`**: Использовать `j_loads` для чтения JSON-данных.
6.  **Обработка ошибок**: Добавить более детальную обработку ошибок и логирование.

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
from src.logger import logger  # Import logger

class Sources():
    """
    Класс для хранения и форматирования списка источников.

    Args:
        link_list (List[Dict[str, str]]): Список словарей, содержащих информацию об источниках.
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
        Форматирует список источников в виде строки.

        Returns:
            str: Отформатированная строка со списком источников.
        """
        return '\n\n' + ('\n'.join([f'[{link["title"]}]({link["link"]})' for link in self.list]))

class AbraGeoBlockedError(Exception):
    """
    Исключение, выбрасываемое при блокировке Abra по географическому признаку.
    """
    pass

class MetaAI(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер для взаимодействия с Meta AI.

    Args:
        proxy (str, optional): Прокси-сервер для использования. По умолчанию None.
        connector (BaseConnector, optional): Пользовательский коннектор aiohttp. По умолчанию None.
    """
    label: str = 'Meta AI'
    url: str = 'https://www.meta.ai'
    working: bool = True
    default_model: str = 'meta-ai'

    def __init__(self, proxy: str = None, connector: BaseConnector = None) -> None:
        """
        Инициализирует объект MetaAI.

        Args:
            proxy (str, optional): Прокси-сервер для использования. По умолчанию None.
            connector (BaseConnector, optional): Пользовательский коннектор aiohttp. По умолчанию None.
        """
        self.session: ClientSession = ClientSession(connector=get_connector(connector, proxy), headers=DEFAULT_HEADERS)
        self.cookies: Cookies = None
        self.access_token: str = None
        self.lsd: str = None
        self.dtsg: str = None

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с Meta AI.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию None.

        Yields:
            AsyncResult: Часть ответа от Meta AI.
        """
        async for chunk in cls(proxy).prompt(format_prompt(messages)):
            yield chunk

    async def update_access_token(self, birthday: str = '1999-01-01') -> None:
        """
        Обновляет access token для взаимодействия с Meta AI.

        Args:
            birthday (str, optional): Дата рождения пользователя. По умолчанию '1999-01-01'.

        Raises:
            ResponseError: Если не удалось получить access token.
        """
        url: str = 'https://www.meta.ai/api/graphql/'
        payload: Dict[str, str] = {
            'lsd': self.lsd,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'useAbraAcceptTOSForTempUserMutation',
            'variables': json.dumps({
                'dob': birthday,
                'icebreaker_type': 'TEXT',
                '__relay_internal__pv__WebPixelRatiorelayprovider': 1,
            }),
            'doc_id': '7604648749596940',
        }
        headers: Dict[str, str] = {
            'x-fb-friendly-name': 'useAbraAcceptTOSForTempUserMutation',
            'x-fb-lsd': self.lsd,
            'x-asbd-id': '129477',
            'alt-used': 'www.meta.ai',
            'sec-fetch-site': 'same-origin'
        }
        try:
            async with self.session.post(url, headers=headers, cookies=self.cookies, data=payload) as response:
                await raise_for_status(response, 'Fetch access_token failed')
                auth_json: dict = await response.json(content_type=None)
                self.access_token: str = auth_json['data']['xab_abra_accept_terms_of_service']['new_temp_user_auth']['access_token']
        except Exception as ex:
            logger.error('Error while fetching access token', ex, exc_info=True)
            raise

    async def prompt(self, message: str, cookies: Cookies = None) -> AsyncResult:
        """
        Отправляет запрос к Meta AI и возвращает ответ.

        Args:
            message (str): Сообщение для отправки.
            cookies (Cookies, optional): Cookies для использования. По умолчанию None.

        Yields:
            AsyncResult: Часть ответа от Meta AI.

        Raises:
            ResponseError: Если произошла ошибка при получении ответа.
            RuntimeError: Если в ответе есть ошибки.
        """
        if self.cookies is None:
            await self.update_cookies(cookies)
        if cookies is not None:
            self.access_token = None
        if self.access_token is None and cookies is None:
            await self.update_access_token()
        if self.access_token is None:
            url: str = 'https://www.meta.ai/api/graphql/'
            payload: Dict[str, str] = {'lsd': self.lsd, 'fb_dtsg': self.dtsg}
            headers: Dict[str, str] = {'x-fb-lsd': self.lsd}
        else:
            url: str = 'https://graph.meta.ai/graphql?locale=user'
            payload: Dict[str, str] = {'access_token': self.access_token}
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
        payload: Dict[str, str] = {
            **payload,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'useAbraSendMessageMutation',
            'variables': json.dumps({
                'message': {'sensitive_string_value': message},
                'externalConversationId': str(uuid.uuid4()),
                'offlineThreadingId': generate_offline_threading_id(),
                'suggestedPromptIndex': None,
                'flashVideoRecapInput': {'images': []},
                'flashPreviewInput': None,
                'promptPrefix': None,
                'entrypoint': 'ABRA__CHAT__TEXT',
                'icebreaker_type': 'TEXT',
                '__relay_internal__pv__AbraDebugDevOnlyrelayprovider': False,
                '__relay_internal__pv__WebPixelRatiorelayprovider': 1,
            }),
            'server_timestamps': 'true',
            'doc_id': '7783822248314888'
        }
        try:
            async with self.session.post(url, headers=headers, data=payload) as response:
                await raise_for_status(response, 'Fetch response failed')
                last_snippet_len: int = 0
                fetch_id: str = None
                async for line in response.content:
                    if b'<h1>Something Went Wrong</h1>' in line:
                        raise ResponseError('Response: Something Went Wrong')
                    try:
                        json_line: dict = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if json_line.get('errors'):
                        raise RuntimeError('\n'.join([error.get('message') for error in json_line.get('errors')]))
                    bot_response_message: dict = json_line.get('data', {}).get('node', {}).get('bot_response_message', {})
                    streaming_state: str = bot_response_message.get('streaming_state')
                    fetch_id: str = bot_response_message.get('fetch_id') or fetch_id
                    if streaming_state in ('STREAMING', 'OVERALL_DONE'):
                        imagine_card: dict = bot_response_message.get('imagine_card')
                        if imagine_card is not None:
                            imagine_session: dict = imagine_card.get('session')
                            if imagine_session is not None:
                                imagine_medias: list = imagine_session.get('media_sets', {}).pop().get('imagine_media')
                                if imagine_medias is not None:
                                    image_class = ImageResponse if streaming_state == 'OVERALL_DONE' else ImagePreview
                                    yield image_class([media['uri'] for media in imagine_medias], imagine_medias[0]['prompt'])
                        snippet: str =  bot_response_message['snippet']
                        new_snippet_len: int = len(snippet)
                        if new_snippet_len > last_snippet_len:
                            yield snippet[last_snippet_len:]
                            last_snippet_len: int = new_snippet_len
            #if last_streamed_response is None:
            #    if attempts > 3:
            #        raise Exception("MetaAI is having issues and was not able to respond (Server Error)")
            #    access_token = await self.get_access_token()
            #    return await self.prompt(message=message, attempts=attempts + 1)
            if fetch_id is not None:
                sources: Sources = await self.fetch_sources(fetch_id)
                if sources is not None:
                    yield sources
        except Exception as ex:
            logger.error('Error while fetching prompt', ex, exc_info=True)
            raise

    async def update_cookies(self, cookies: Cookies = None) -> None:
        """
        Обновляет cookies для взаимодействия с Meta AI.

        Args:
            cookies (Cookies, optional): Cookies для использования. По умолчанию None.

        Raises:
            AbraGeoBlockedError: Если Meta AI заблокирована в данной стране.
            ResponseError: Если не удалось получить cookies.
        """
        try:
            async with self.session.get('https://www.meta.ai/', cookies=cookies) as response:
                await raise_for_status(response, 'Fetch home failed')
                text: str = await response.text()
                if 'AbraGeoBlockedError' in text:
                    raise AbraGeoBlockedError('Meta AI isn\'t available yet in your country')
                if cookies is None:
                    cookies: Cookies = {
                        '_js_datr': self.extract_value(text, '_js_datr'),
                        'abra_csrf': self.extract_value(text, 'abra_csrf'),
                        'datr': self.extract_value(text, 'datr'),
                    }
                self.lsd: str = self.extract_value(text, start_str='\'LSD",[],{"token":"\', end_str=\'"}\'')
                self.dtsg: str = self.extract_value(text, start_str='\'DTSGInitialData",[],{"token":"\', end_str=\'"}\'')
                self.cookies: Cookies = cookies
        except Exception as ex:
            logger.error('Error while updating cookies', ex, exc_info=True)
            raise

    async def fetch_sources(self, fetch_id: str) -> Optional[Sources]:
        """
        Получает источники для данного fetch_id.

        Args:
            fetch_id (str): Идентификатор запроса.

        Returns:
            Optional[Sources]: Объект Sources с информацией об источниках, или None, если источники не найдены.

        Raises:
            ResponseError: Если произошла ошибка при получении источников.
            RuntimeError: Если произошла ошибка при обработке ответа.
        """
        if self.access_token is None:
            url: str = 'https://www.meta.ai/api/graphql/'
            payload: Dict[str, str] = {'lsd': self.lsd, 'fb_dtsg': self.dtsg}
            headers: Dict[str, str] = {'x-fb-lsd': self.lsd}
        else:
            url: str = 'https://graph.meta.ai/graphql?locale=user'
            payload: Dict[str, str] = {'access_token': self.access_token}
            headers: Dict[str, str] = {}
        payload: Dict[str, str] = {
            **payload,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'AbraSearchPluginDialogQuery',
            'variables': json.dumps({'abraMessageFetchID': fetch_id}),
            'server_timestamps': 'true',
            'doc_id': '6946734308765963',
        }
        headers: Dict[str, str] = {
            'authority': 'graph.meta.ai',
            'x-fb-friendly-name': 'AbraSearchPluginDialogQuery',
            **headers
        }
        try:
            async with self.session.post(url, headers=headers, cookies=self.cookies, data=payload) as response:
                await raise_for_status(response, 'Fetch sources failed')
                text: str = await response.text()
                if '<h1>Something Went Wrong</h1>' in text:
                    raise ResponseError('Response: Something Went Wrong')
                try:
                    response_json: dict = json.loads(text)
                    message: dict = response_json['data']['message']
                    if message is not None:
                        searchResults: dict = message['searchResults']
                        if searchResults is not None:
                            return Sources(searchResults['references'])
                except (KeyError, TypeError, json.JSONDecodeError) as ex:
                    raise RuntimeError(f'Response: {text}') from ex
        except Exception as ex:
            logger.error('Error while fetching sources', ex, exc_info=True)
            return None

    @staticmethod
    def extract_value(text: str, key: str = None, start_str: str = None, end_str: str = '\',\') -> str:
        """
        Извлекает значение из текста по заданным ключам.

        Args:
            text (str): Текст для извлечения значения.
            key (str, optional): Ключ для поиска значения. По умолчанию None.
            start_str (str, optional): Начальная строка для поиска значения. По умолчанию None.
            end_str (str, optional): Конечная строка для поиска значения. По умолчанию ',\'.

        Returns:
            str: Извлеченное значение.
        """
        if start_str is None:
            start_str: str = f'{key}":{{"value":"'
        start: int = text.find(start_str)
        if start >= 0:
            start+= len(start_str)
            end: int = text.find(end_str, start)
            if end >= 0:
                return text[start:end]
        return None

def generate_offline_threading_id() -> str:
    """
    Generates an offline threading ID.

    Returns:
        str: The generated offline threading ID.
    """
    # Generate a random 64-bit integer
    random_value: int = random.getrandbits(64)
    
    # Get the current timestamp in milliseconds
    timestamp: int = int(time.time() * 1000)
    
    # Combine timestamp and random value
    threading_id: int = (timestamp << 22) | (random_value & ((1 << 22) - 1))
    
    return str(threading_id)