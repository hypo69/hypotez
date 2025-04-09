### **Анализ кода модуля `Bing.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код выполняет функцию стриминговой генерации текста с использованием Bing API.
    - Присутствуют константы и структуры данных для настройки соединения и параметров запросов.
    - Обработка ошибок при создании соединения и генерации контента.
- **Минусы**:
    - Отсутствует docstring в начале файла модуля.
    - Многие функции не имеют подробного документирования (docstring), что затрудняет понимание их назначения и использования.
    - Не везде используются аннотации типов.
    - Смешанный стиль: где-то используется `logger`, а где-то `print`.
    - Некоторые участки кода выглядят избыточно сложными, особенно в обработке ответов от Bing API.
    - Magic values: в коде встречаются неименованные числовые константы, что снижает читаемость.

#### **Рекомендации по улучшению**:

1.  **Добавить Docstring в начало файла модуля**:

    *   Добавить общее описание модуля.
    *   Описать назначение модуля и предоставить примеры использования, если это необходимо.

2.  **Документирование функций**:

    *   Добавить docstring для каждой функции, включая описание аргументов, возвращаемых значений и возможных исключений.
    *   Особенно важна документация для функций `create_conversation`, `stream_generate`, `_format`, `run`, `convert` и `_create_completion`.

3.  **Использовать логирование `logger`**:

    *   Заменить все вызовы `print` на вызовы `logger.info` или `logger.debug` для отладочной информации.
    *   Обязательно использовать `logger.error` для логирования ошибок и исключений, передавая `ex` и `exc_info=True`.

4.  **Улучшить читаемость обработки ответов**:

    *   Разбить сложные условия на более простые и понятные блоки.
    *   Использовать промежуточные переменные с понятными именами для хранения результатов обработки JSON.

5.  **Улучшить обработку ошибок**:

    *   Добавить больше конкретных обработок исключений, чтобы понимать, в каком месте возникла проблема.
    *   Обрабатывать возможные ошибки при парсинге JSON.

6.  **Использовать константы вместо "магических чисел"**:

    *   Заменить числовые значения (например, `1`, `2`, `4`) на именованные константы, чтобы сделать код более понятным.

7.  **Улучшить форматирование**:

    *   Убедиться, что код соответствует PEP8, включая отступы, пробелы и длину строк.

8.  **Добавить аннотации типов**:

    *   Добавить аннотации типов для всех переменных, аргументов функций и возвращаемых значений.

9. **Использовать `j_loads` или `j_loads_ns`**:
- Для чтения JSON или конфигурационных файлов замените стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.

#### **Оптимизированный код**:

```python
"""
Модуль для взаимодействия с Bing API для стриминговой генерации текста.
======================================================================

Модуль содержит функции для создания диалога с Bing, стриминговой генерации текста на основе запроса,
а также вспомогательные функции для форматирования сообщений и обработки контекста.

Пример использования
----------------------

>>> from src.endpoints.freegpt-webui-ru.g4f.Provider.Providers import Bing
>>> async def example():
>>>     async for response in Bing.stream_generate(prompt="Hello, Bing!"):
>>>         print(response)
>>> import asyncio
>>> asyncio.run(example())
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
from src.logger import logger # Подключаем модуль логирования
from ...typing import sha256, Dict, get_type_hints

url: str = 'https://bing.com/chat'
model: list[str] = ['gpt-4']
supports_stream: bool = True
needs_auth: bool = False

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())


class OptionsSets:
    """
    Класс для хранения наборов опций для Bing API.
    """
    optionSet: dict = {
        'tone': str,
        'optionsSets': list
    }

    jailbreak: dict = {
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
            # "harmonyv3",
            "dtappid",
            "cricinfo",
            "cricinfov2",
            "dv3sugg",
            "nojbfedge"
        ]
    }


class Defaults:
    """
    Класс, содержащий дефолтные значения для Bing API.
    """
    delimiter: str = '\x1e'
    ip_address: str = f'13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}'

    allowedMessageTypes: list[str] = [
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

    sliceIds: list[str] = [
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

    location: dict = {
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
    Форматирует сообщение для отправки в Bing API.

    Args:
        msg (dict): Сообщение в формате словаря.

    Returns:
        str: JSON-представление сообщения с добавлением разделителя.
    """
    return json.dumps(msg, ensure_ascii=False) + Defaults.delimiter


async def create_conversation() -> tuple[str, str, str]:
    """
    Создает новый диалог с Bing API.

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

            response_json = create.json()
            conversationId = response_json.get('conversationId')
            clientId = response_json.get('clientId')
            conversationSignature = response_json.get('conversationSignature')

            if conversationId and clientId and conversationSignature:
                return conversationId, clientId, conversationSignature

        except requests.exceptions.RequestException as ex:
            logger.error('Error while creating conversation', ex, exc_info=True)

    raise Exception('Failed to create conversation.')


async def stream_generate(prompt: str,
                          mode: OptionsSets.optionSet = OptionsSets.jailbreak,
                          context: str | bool = False) -> Generator[str, None, None]:
    """
    Генерирует текст в стриминговом режиме с использованием Bing API.

    Args:
        prompt (str): Текст запроса.
        mode (OptionsSets.optionSet, optional): Набор опций. Defaults to OptionsSets.jailbreak.
        context (str | bool, optional): Контекст для запроса. Defaults to False.

    Yields:
        str: Часть сгенерированного текста.

    Raises:
        Exception: Если произошла ошибка при генерации текста.
    """
    timeout = aiohttp.ClientTimeout(total=900)
    session = aiohttp.ClientSession(timeout=timeout)

    try:
        conversationId, clientId, conversationSignature = await create_conversation()

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
            'type': 4  # Тип сообщения
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
                if not obj:
                    continue

                try:
                    response = json.loads(obj)

                    if response.get('type') == 1 and response['arguments'][0].get('messages', ):
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

                except json.JSONDecodeError as ex:
                    logger.error(f'Error decoding JSON: {ex}', exc_info=True)
                    continue

    except (aiohttp.ClientError, Exception) as ex:
        logger.error(f'Error in stream_generate: {ex}', exc_info=True)
        raise
    finally:
        if session and not session.closed:
            await session.close()
        if wss and not wss.closed:
            await wss.close()


def run(generator: Generator[Any, None, None]) -> Generator[str, None, None]:
    """
    Запускает асинхронный генератор и возвращает синхронный генератор.

    Args:
        generator (Generator[Any, None, None]): Асинхронный генератор.

    Yields:
        str: Значения, выдаваемые асинхронным генератором.
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
        messages (list[dict]): Список сообщений, где каждое сообщение - словарь с ключами 'role' и 'content'.

    Returns:
        str: Строка контекста, отформатированная для Bing API.
    """
    context = ""

    for message in messages:
        context += "[%s](#message)\n%s\n\n" % (message['role'],
                                               message['content'])

    return context


def _create_completion(model: str, messages: list[dict], stream: bool, **kwargs) -> Generator[str, None, None]:
    """
    Создает завершение текста на основе запроса к Bing API.

    Args:
        model (str): Название модели.
        messages (list[dict]): Список сообщений для контекста.
        stream (bool): Флаг стриминговой генерации.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Части сгенерированного текста.
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


params: str = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])