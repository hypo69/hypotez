### **Анализ кода модуля `Bing.py`**

**Расположение файла в проекте:** `hypotez/src/endpoints/freegpt-webui-ru/g4f/Provider/Providers/Bing.py`

**Описание:** Модуль предоставляет реализацию взаимодействия с Bing Chat API для генерации текста.

**Качество кода:**
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код выполняет свою основную функцию - взаимодействие с Bing Chat API.
    - Присутствуют базовые механизмы обработки ошибок.
    - Использование асинхронности для неблокирующего взаимодействия с API.
- **Минусы**:
    - Отсутствует подробная документация и комментарии.
    - Не соблюдены PEP8 стандарты форматирования.
    - Magic values разбросаны по коду.
    - Не все переменные аннотированы типами.
    - Не используется модуль логирования `logger`.
    - Нет обработки исключений для всех потенциально проблемных мест.
    - Код содержит устаревшие конструкции (например, использование `asyncio.get_event_loop()`).

**Рекомендации по улучшению:**

1.  **Добавить документацию и комментарии:**
    - Добавить docstring к классам и функциям, описывающие их назначение, параметры и возвращаемые значения.
    - Добавить комментарии к ключевым участкам кода, объясняющие логику работы.
2.  **Соблюдать PEP8 стандарты форматирования:**
    - Использовать пробелы вокруг операторов присваивания и других операторов.
    - Переименовать переменные и функции в соответствии с конвенцией (snake_case).
    - Убрать длинные строки, разбить их на несколько.
3.  **Использовать модуль логирования `logger`:**
    - Заменить `print` на `logger.info`, `logger.error` и т.д.
    - Логировать важные события и ошибки.
4.  **Обрабатывать исключения:**
    - Добавить блоки `try-except` для обработки возможных исключений, возникающих при взаимодействии с API, работе с сетью и т.д.
    - Логировать возникающие исключения с использованием `logger.error`.
5.  **Улучшить структуру кода:**
    - Разбить большие функции на более мелкие, чтобы улучшить читаемость и поддерживаемость.
    - Вынести константы и magic values в отдельные переменные.
6.  **Добавить аннотации типов:**
    - Добавить аннотации типов для всех переменных, аргументов функций и возвращаемых значений.
7.  **Обновить устаревшие конструкции:**
    - Использовать `asyncio.run()` вместо `loop.run_until_complete()`.
8.  **Улучшить обработку ошибок:**
    - Добавить более информативные сообщения об ошибках.
    - Подумать о реализации механизма повторных попыток при возникновении временных проблем с сетью.
9.  **Перевести все docstring и комментарии на русский язык**
10. **Использовать одинарные кавычки**
11. **Заменить `Union[]` на `|`**
12. **Убрать неиспользуемые импорты**

**Оптимизированный код:**

```python
import os
import json
import random
import uuid
import ssl
import certifi
import aiohttp
import asyncio
import requests
from typing import Optional, Dict, Generator, List
from pathlib import Path

from src.logger import logger

url: str = 'https://bing.com/chat'
model: List[str] = ['gpt-4']
supports_stream: bool = True
needs_auth: bool = False

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())


class OptionsSets:
    """
    Класс, содержащий наборы опций для запросов к Bing Chat.
    """

    class OptionSet:
        """
        Внутренний класс для представления набора опций.
        """
        tone: str
        options_sets: list

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
    Класс, содержащий значения по умолчанию для параметров запросов.
    """
    delimiter: str = '\x1e'
    ip_address: str = f'13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}'

    allowed_message_types: List[str] = [
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

    slice_ids: List[str] = [
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

    location: Dict[str, str | list[dict]] = {
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
    Форматирует сообщение в JSON-формат с добавлением разделителя.

    Args:
        msg (dict): Сообщение для форматирования.

    Returns:
        str: Отформатированное сообщение.
    """
    return json.dumps(msg, ensure_ascii=False) + Defaults.delimiter


async def create_conversation() -> tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Создает новую сессию разговора с Bing Chat.

    Returns:
        tuple[Optional[str], Optional[str], Optional[str]]: Идентификатор разговора, идентификатор клиента и подпись разговора.
    Raises:
        Exception: Если не удалось создать разговор после нескольких попыток.
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

            conversation_id = create.json().get('conversationId')
            client_id = create.json().get('clientId')
            conversation_signature = create.json().get('conversationSignature')

            if not conversation_id or not client_id or not conversation_signature and _ == 4:
                raise Exception('Failed to create conversation.')

            return conversation_id, client_id, conversation_signature

        except Exception as ex:
            logger.error('Error while creating conversation', ex, exc_info=True)
            await asyncio.sleep(1)  # небольшая задержка перед следующей попыткой

    return None, None, None  # вернуть None, если все попытки не удались


async def stream_generate(prompt: str,
                          mode: dict = OptionsSets.jailbreak,
                          context: str | bool = False) -> Generator[str, None, None]:
    """
    Генерирует текст с использованием Bing Chat API в потоковом режиме.

    Args:
        prompt (str): Текст запроса.
        mode (dict, optional): Набор опций для запроса. По умолчанию OptionsSets.jailbreak.
        context (str | bool, optional): Контекст для запроса. По умолчанию False.

    Yields:
        str: Часть сгенерированного текста.

    Raises:
        Exception: Если произошла ошибка во время генерации текста.
    """
    timeout = aiohttp.ClientTimeout(total=900)
    session = aiohttp.ClientSession(timeout=timeout)

    try:
        conversation_id, client_id, conversation_signature = await create_conversation()
        if not conversation_id or not client_id or not conversation_signature:
            raise Exception('Failed to create conversation.')

        wss = await session.ws_connect(
            'wss://sydney.bing.com/sydney/ChatHub',
            ssl=ssl_context,
            autoping=False,
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
            })

        await wss.send_str(_format({'protocol': 'json', 'version': 1}))
        await wss.receive(timeout=900)

        struct = {
            'arguments': [
                {
                    **mode,
                    'source': 'cib',
                    'allowedMessageTypes': Defaults.allowed_message_types,
                    'sliceIds': Defaults.slice_ids,
                    'traceId': os.urandom(16).hex(),
                    'isStartOfSession': True,
                    'message': Defaults.location | {
                        'author': 'user',
                        'inputMethod': 'Keyboard',
                        'text': prompt,
                        'messageType': 'Chat'
                    },
                    'conversationSignature': conversation_signature,
                    'participant': {
                        'id': client_id
                    },
                    'conversationId': conversation_id
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
        draw = False
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
                    if not draw:
                        if (response['arguments'][0]['messages'][0]['contentOrigin'] != 'Apology') and not draw:
                            resp_txt = result_text + \
                                       response['arguments'][0]['messages'][0]['adaptiveCards'][0]['body'][0].get(
                                           'text', '')
                            resp_txt_no_link = result_text + \
                                                response['arguments'][0]['messages'][0].get(
                                                    'text', '')

                            if response['arguments'][0]['messages'][0].get('messageType', ):
                                resp_txt = (
                                        resp_txt
                                        + response['arguments'][0]['messages'][0]['adaptiveCards'][0]['body'][0][
                                            'inlines'][0].get('text')
                                        + '\n'
                                )
                                result_text = (
                                        result_text
                                        + response['arguments'][0]['messages'][0]['adaptiveCards'][0]['body'][0][
                                            'inlines'][0].get('text')
                                        + '\n'
                                )

                    if cache_text.endswith('   '):
                        final = True
                        if wss and not wss.closed:
                            await wss.close()
                        if session and not session.closed:
                            await session.close()

                    yield (resp_txt.replace(cache_text, ''))
                    cache_text = resp_txt

                elif response.get('type') == 2:
                    if response['item']['result'].get('error'):
                        if wss and not wss.closed:
                            await wss.close()
                        if session and not session.closed:
                            await session.close()

                        raise Exception(
                            f"{response['item']['result']['value']}: {response['item']['result']['message']}")

                    if draw:
                        cache = response['item']['messages'][1]['adaptiveCards'][0]['body'][0]['text']
                        response['item']['messages'][1]['adaptiveCards'][0]['body'][0]['text'] = (
                                cache + resp_txt)

                    if (response['item']['messages'][-1]['contentOrigin'] == 'Apology' and resp_txt):
                        response['item']['messages'][-1]['text'] = resp_txt_no_link
                        response['item']['messages'][-1]['adaptiveCards'][0]['body'][0]['text'] = resp_txt

                    final = True
                    if wss and not wss.closed:
                        await wss.close()
                    if session and not session.closed:
                        await session.close()

    except Exception as ex:
        logger.error('Error in stream_generate', ex, exc_info=True)
        if wss and not wss.closed:
            await wss.close()
        if session and not session.closed:
            await session.close()
        raise


def run(generator: Generator[str, None, None]) -> Generator[str, None, None]:
    """
    Запускает асинхронный генератор и возвращает синхронный генератор.

    Args:
        generator (Generator[str, None, None]): Асинхронный генератор.

    Yields:
        str: Значение, полученное из асинхронного генератора.
    """
    loop = asyncio.get_event_loop()
    gen = generator.__aiter__()

    while True:
        try:
            next_val = loop.run_until_complete(gen.__anext__())
            yield next_val

        except StopAsyncIteration:
            break


def convert(messages: list[dict]) -> str:
    """
    Преобразует список сообщений в строку контекста.

    Args:
        messages (list[dict]): Список сообщений.

    Returns:
        str: Строка контекста.
    """
    context = ""

    for message in messages:
        context += "[%s](#message)\n%s\n\n" % (message['role'],
                                               message['content'])

    return context


def _create_completion(model: str, messages: list[dict], stream: bool, **kwargs) -> Generator[str, None, None]:
    """
    Создает запрос на завершение текста с использованием Bing Chat API.

    Args:
        model (str): Идентификатор модели.
        messages (list[dict]): Список сообщений.
        stream (bool): Флаг потоковой передачи.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Часть сгенерированного текста.
    """
    if len(messages) < 2:
        prompt = messages[0]['content']
        context = False

    else:
        prompt = messages[-1]['content']
        context = convert(messages[:-1])

    response = run(stream_generate(prompt, mode, context))
    for token in response:
        yield (token)


params: str = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
              '(%s)' % ', '.join(
    [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in
     _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])