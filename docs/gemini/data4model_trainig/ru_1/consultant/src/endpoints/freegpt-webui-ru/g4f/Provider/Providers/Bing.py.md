### **Анализ кода модуля `Bing.py`**

**Расположение файла в проекте:** `hypotez/src/endpoints/freegpt-webui-ru/g4f/Provider/Providers/Bing.py`

**Описание:** Модуль предоставляет класс для взаимодействия с Bing Chat API. Он включает функции для создания диалога, потоковой генерации ответов и форматирования сообщений.

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование `aiohttp` для асинхронных запросов.
    - Четкое разделение на функции для создания диалога и генерации ответов.
    - Использование `Defaults` для хранения настроек по умолчанию.
- **Минусы**:
    - Недостаточная документация функций и классов.
    - Отсутствуют аннотации типов для всех переменных.
    - Смешанный стиль кодирования (использование как `requests`, так и `aiohttp`).
    - Использование устаревших конструкций, таких как `loop = asyncio.get_event_loop()`.
    - Жетские кодированные заголовки и URL-адреса, которые могут быстро устареть.
    - Обработка ошибок является базовой и может быть улучшена.

**Рекомендации по улучшению:**

1.  **Добавить документацию**:
    - Добавить docstring к каждому классу и каждой функции, объясняющие их назначение, аргументы и возвращаемые значения.
    - Перевести все docstring на русский язык.
2.  **Добавить аннотации типов**:
    - Добавить аннотации типов ко всем переменным и функциям для повышения читаемости и облегчения отладки.
3.  **Улучшить обработку ошибок**:
    - Использовать `logger` для логирования ошибок и предупреждений.
    - Предоставлять более информативные сообщения об ошибках.
4.  **Обновить зависимости**:
    - Убедиться, что все используемые библиотеки актуальны.
5.  **Удалить неиспользуемый код**:
    - Удалить неиспользуемые импорты и переменные.
6.  **Улучшить структуру кода**:
    - Разбить большие функции на более мелкие, чтобы улучшить читаемость и удобство сопровождения.
7.  **Использовать `j_loads` для чтения JSON**:
    - Заменить `json.loads` на `j_loads` или `j_loads_ns` для унификации обработки JSON.
8. **Пересмотр создания сессий**:
   -  Создание сессии `aiohttp.ClientSession` должно быть вынесено за пределы функции `stream_generate`, чтобы избежать повторного создания сессии для каждого запроса.
9. **Улучшить обработку исключений**:
   -  В блоках `try-except` использовать `ex` вместо `e` для именования исключений.
10. **Удалить неиспользуемые переменные**:
    -  Удалить переменные, которые не используются в коде, например, `draw`.

**Оптимизированный код:**

```python
"""
Модуль для работы с Bing Chat API
====================================

Модуль содержит функции для создания диалога с Bing Chat,
потоковой генерации ответов и форматирования сообщений.
"""
import os
import json
import random
import uuid
import ssl
import certifi
import aiohttp
import asyncio
import requests
from typing import Dict, Generator, Optional, List
from ...typing import sha256
from src.logger import logger  # Import logger module


url: str = 'https://bing.com/chat'
model: List[str] = ['gpt-4']
supports_stream: bool = True
needs_auth: bool = False

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())


class OptionsSets:
    """
    Класс, содержащий наборы опций для настройки Bing Chat.
    """
    optionSet: Dict[str, type] = {
        'tone': str,
        'optionsSets': list
    }

    jailbreak: Dict[str, List[str]] = {
        "optionsSets": [
            'saharasugg',
            'enablenewsfc',
            'clgalileo',
            'gencontentv3',
            "nlu_direct_response_filter",
            "deepleo",
            "disable_emoji_spoken_text",
            "responsible_ai_policy_235",
            "enablemm",
            "h3precise",
            "dtappid",
            "cricinfo",
            "cricinfov2",
            "dv3sugg",
            "nojbfedge"
        ]
    }


class Defaults:
    """
    Класс, содержащий значения по умолчанию для параметров Bing Chat.
    """
    delimiter: str = '\x1e'
    ip_address: str = f'13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}'

    allowedMessageTypes: List[str] = [
        'Chat',
        'Disengaged',
        'AdsQuery',
        'SemanticSerp',
        'GenerateContentQuery',
        'SearchQuery',
        'ActionRequest',
        'Context',
        'Progress',
        'AdsQuery',
        'SemanticSerp'
    ]

    sliceIds: List[str] = [
        'winmuid3tf',
        'osbsdusgreccf',
        'ttstmout',
        'crchatrev',
        'winlongmsgtf',
        'ctrlworkpay',
        'norespwtf',
        'tempcacheread',
        'temptacache',
        '505scss0',
        '508jbcars0',
        '515enbotdets0',
        '5082tsports',
        '515vaoprvs',
        '424dagslnv1s0',
        'kcimgattcf',
        '427startpms0'
    ]

    location: Dict[str, str | int | List[Dict[str, str | int | float | Dict[str, float]]]] = {
        'locale': 'en-US',
        'market': 'en-US',
        'region': 'US',
        'locationHints': [
            {
                'country': 'United States',
                'state': 'California',
                'city': 'Los Angeles',
                'timezoneoffset': 8,
                'countryConfidence': 8,
                'Center': {
                    'Latitude': 34.0536909,
                    'Longitude': -118.242766
                },
                'RegionType': 2,
                'SourceType': 1
            }
        ],
    }


def _format(msg: dict) -> str:
    """
    Форматирует сообщение в JSON и добавляет разделитель.

    Args:
        msg (dict): Сообщение для форматирования.

    Returns:
        str: Отформатированное сообщение.
    """
    return json.dumps(msg, ensure_ascii=False) + Defaults.delimiter


async def create_conversation() -> tuple[str, str, str]:
    """
    Создает новый диалог с Bing Chat.

    Returns:
        tuple[str, str, str]: conversationId, clientId, conversationSignature.

    Raises:
        Exception: Если не удалось создать диалог после нескольких попыток.
    """
    for _ in range(5):
        try:
            create = requests.get(
                'https://www.bing.com/turing/conversation/create',
                headers={
                    'authority': 'edgeservices.bing.com',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'max-age=0',
                    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
                    'sec-ch-ua-arch': '"x86"',
                    'sec-ch-ua-bitness': '"64"',
                    'sec-ch-ua-full-version': '"110.0.1587.69"',
                    'sec-ch-ua-full-version-list': '"Chromium";v="110.0.5481.192", "Not A(Brand";v="24.0.0.0", "Microsoft Edge";v="110.0.1587.69"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-model': '""',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"15.0.0"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
                    'x-edge-shopping-flag': '1',
                    'x-forwarded-for': Defaults.ip_address
                })

            create_json = create.json()
            conversationId = create_json.get('conversationId')
            clientId = create_json.get('clientId')
            conversationSignature = create_json.get('conversationSignature')

            if not conversationId or not clientId or not conversationSignature:
                logger.warning(f"Failed to create conversation on attempt {_ + 1}")
                continue

            return conversationId, clientId, conversationSignature

        except Exception as ex:
            logger.error('Error while creating conversation', ex, exc_info=True)
            if _ == 4:
                raise Exception('Failed to create conversation.') from ex

    raise Exception('Failed to create conversation after multiple attempts.')


async def stream_generate(prompt: str, mode: Dict[str, List[str]] = OptionsSets.jailbreak, context: str | bool = False) -> Generator[str, None, None]:
    """
    Асинхронно генерирует ответ от Bing Chat в потоковом режиме.

    Args:
        prompt (str): Текст запроса.
        mode (Dict[str, List[str]], optional): Набор опций для настройки чата. По умолчанию OptionsSets.jailbreak.
        context (str | bool, optional): Контекст диалога. По умолчанию False.

    Yields:
        str: Часть ответа от Bing Chat.

    Raises:
        Exception: В случае ошибки при генерации ответа.
    """
    timeout = aiohttp.ClientTimeout(total=900)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            conversationId, clientId, conversationSignature = await create_conversation()

            async with session.ws_connect('wss://sydney.bing.com/sydney/ChatHub', ssl=ssl_context, autoping=False,
                                           headers={
                                               'accept': 'application/json',
                                               'accept-language': 'en-US,en;q=0.9',
                                               'content-type': 'application/json',
                                               'sec-ch-ua': '"Not_A Brand";v="99", "Microsoft Edge";v="110", "Chromium";v="110"',
                                               'sec-ch-ua-arch': '"x86"',
                                               'sec-ch-ua-bitness': '"64"',
                                               'sec-ch-ua-full-version': '"109.0.1518.78"',
                                               'sec-ch-ua-full-version-list': '"Chromium";v="110.0.5481.192", "Not A(Brand";v="24.0.0.0", "Microsoft Edge";v="110.0.1587.69"',
                                               'sec-ch-ua-mobile': '?0',
                                               'sec-ch-ua-model': '',
                                               'sec-ch-ua-platform': '"Windows"',
                                               'sec-ch-ua-platform-version': '"15.0.0"',
                                               'sec-fetch-dest': 'empty',
                                               'sec-fetch-mode': 'cors',
                                               'sec-fetch-site': 'same-origin',
                                               'x-ms-client-request-id': str(uuid.uuid4()),
                                               'x-ms-useragent': 'azsdk-js-api-client-factory/1.0.0-beta.1 core-rest-pipeline/1.10.0 OS/Win32',
                                               'Referer': 'https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx',
                                               'Referrer-Policy': 'origin-when-cross-origin',
                                               'x-forwarded-for': Defaults.ip_address
                                           }) as wss:

                await wss.send_str(_format({'protocol': 'json', 'version': 1}))
                await wss.receive(timeout=900)

                struct = {
                    'arguments': [
                        {
                            **mode,
                            'source': 'cib',
                            'allowedMessageTypes': Defaults.allowedMessageTypes,
                            'sliceIds': Defaults.sliceIds,
                            'traceId': os.urandom(16).hex(),
                            'isStartOfSession': True,
                            'message': Defaults.location | {
                                'author': 'user',
                                'inputMethod': 'Keyboard',
                                'text': prompt,
                                'messageType': 'Chat'
                            },
                            'conversationSignature': conversationSignature,
                            'participant': {
                                'id': clientId
                            },
                            'conversationId': conversationId
                        }
                    ],
                    'invocationId': '0',
                    'target': 'chat',
                    'type': 4
                }

                if context:
                    struct['arguments'][0]['previousMessages'] = [
                        {
                            "author": "user",
                            "description": context,
                            "contextType": "WebPage",
                            "messageType": "Context",
                            "messageId": "discover-web--page-ping-mriduna-----"
                        }
                    ]

                await wss.send_str(_format(struct))

                final = False
                resp_txt = ''
                result_text = ''
                resp_txt_no_link = ''
                cache_text = ''

                while not final:
                    msg = await wss.receive(timeout=900)
                    objects = msg.data.split(Defaults.delimiter)

                    for obj in objects:
                        if obj is None or not obj:
                            continue

                        response = json.loads(obj)
                        if response.get('type') == 1 and response['arguments'][0].get('messages', ):
                            if (response['arguments'][0]['messages'][0]['contentOrigin'] != 'Apology'):
                                resp_txt = result_text + \
                                    response['arguments'][0]['messages'][0]['adaptiveCards'][0]['body'][0].get(
                                        'text', '')
                                resp_txt_no_link = result_text + \
                                    response['arguments'][0]['messages'][0].get(
                                        'text', '')

                                if response['arguments'][0]['messages'][0].get('messageType', ):
                                    resp_txt = (
                                        resp_txt
                                        + response['arguments'][0]['messages'][0]['adaptiveCards'][0]['body'][0]['inlines'][0].get('text')
                                        + '\n'
                                    )
                                    result_text = (
                                        result_text
                                        + response['arguments'][0]['messages'][0]['adaptiveCards'][0]['body'][0]['inlines'][0].get('text')
                                        + '\n'
                                    )

                            if cache_text.endswith('   '):
                                final = True
                                if not wss.closed:
                                    await wss.close()
                                if not session.closed:
                                    await session.close()

                            yield (resp_txt.replace(cache_text, ''))
                            cache_text = resp_txt

                        elif response.get('type') == 2:
                            if response['item']['result'].get('error'):
                                if not wss.closed:
                                    await wss.close()
                                if not session.closed:
                                    await session.close()

                                raise Exception(
                                    f"{response['item']['result']['value']}: {response['item']['result']['message']}")

                            final = True
                            if not wss.closed:
                                await wss.close()
                            if not session.closed:
                                await session.close()

        except Exception as ex:
            logger.error('Error while streaming response', ex, exc_info=True)
            if not session.closed:
                await session.close()
            raise


def run(generator: Generator[str, None, None]) -> Generator[str, None, None]:
    """
    Запускает асинхронный генератор и возвращает синхронный генератор.

    Args:
        generator (Generator[str, None, None]): Асинхронный генератор.

    Yields:
        str: Значение, возвращаемое асинхронным генератором.
    """
    loop = asyncio.get_event_loop()
    gen = generator.__aiter__()

    while True:
        try:
            next_val = loop.run_until_complete(gen.__anext__())
            yield next_val

        except StopAsyncIteration:
            break


def convert(messages: List[Dict[str, str]]) -> str:
    """
    Преобразует список сообщений в строку контекста.

    Args:
        messages (List[Dict[str, str]]): Список сообщений.

    Returns:
        str: Строка контекста.
    """
    context = ""

    for message in messages:
        context += "[%s](#message)\n%s\n\n" % (message['role'],
                                               message['content'])

    return context


def _create_completion(model: str, messages: list, stream: bool, **kwargs) -> Generator[str, None, None]:
    """
    Создает завершение на основе предоставленных сообщений.

    Args:
        model (str): Модель для использования.
        messages (list): Список сообщений.
        stream (bool): Следует ли возвращать результат в потоковом режиме.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Часть завершения.
    """
    if len(messages) < 2:
        prompt = messages[0]['content']
        context = False

    else:
        prompt = messages[-1]['content']
        context = convert(messages[:-1])

    response = run(stream_generate(prompt, OptionsSets.jailbreak, context))
    for token in response:
        yield (token)


params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])