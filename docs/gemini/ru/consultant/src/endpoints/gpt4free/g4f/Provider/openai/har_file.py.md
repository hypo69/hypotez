### **Анализ кода модуля `har_file.py`**

## Качество кода:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
   - Код разбит на функции, что облегчает чтение и понимание.
   - Используются аннотации типов для параметров функций.
   - Обработка исключений присутствует.
- **Минусы**:
   - Отсутствует единообразие в стиле кодирования (использование двойных кавычек вместо одинарных).
   - Многие функции не имеют подробного описания, что затрудняет понимание их назначения.
   - Не используется модуль `logger` для логирования.
   - Нарушение PEP8 в части пробелов вокруг операторов.

## Рекомендации по улучшению:

1.  **Документирование кода**:
    *   Добавить docstring к каждой функции и классу, описывающий их назначение, параметры и возвращаемые значения.
    *   В docstring необходимо перевести все описания на русский язык и использовать единый формат.
2.  **Логирование**:
    *   Заменить `print` на `logger.debug` или `logger.info` для отладочной информации.
    *   При обработке исключений использовать `logger.error` для логирования ошибок, передавая объект исключения `ex` и `exc_info=True`.
3.  **Форматирование кода**:
    *   Привести код в соответствие со стандартами PEP8, особенно в части пробелов вокруг операторов присваивания и использования одинарных кавычек.
4.  **Обработка ошибок**:
    *   Улучшить обработку ошибок, чтобы предоставлять более конкретные сообщения об ошибках.
5.  **Использование `j_loads`**:
    *   Заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns` для чтения HAR файлов.

## Оптимизированный код:

```python
"""
Модуль для работы с HAR файлами.
=================================

Модуль предоставляет функции для чтения, анализа и обработки HAR (HTTP Archive) файлов,
используемых для извлечения данных, необходимых для работы с Arkose Labs и OpenAI.
"""
from __future__ import annotations

import base64
import json
import os
import re
import time
import uuid
import random
from urllib.parse import unquote
from copy import deepcopy
from typing import Optional, Dict

from .crypt import decrypt, encrypt
from ...requests import StreamSession
from ...cookies import get_cookies_dir
from ...errors import NoValidHarFileError
from ... import debug
from src.logger import logger

arkose_url: str = 'https://tcr9i.chat.openai.com/fc/gt2/public_key/35536E1E-65B4-4D96-9D97-6ADB7EFF8147'
backend_url: str = 'https://chatgpt.com/backend-api/conversation'
backend_anon_url: str = 'https://chatgpt.com/backend-anon/conversation'
start_url: str = 'https://chatgpt.com/'
conversation_url: str = 'https://chatgpt.com/c/'


class RequestConfig:
    """
    Конфигурация запроса, содержащая cookies, заголовки, access_token и другие параметры.
    """
    cookies: Optional[Dict] = None
    headers: Optional[Dict] = None
    access_token: Optional[str] = None
    proof_token: Optional[list] = None
    turnstile_token: Optional[str] = None
    arkose_request: Optional['arkReq'] = None
    arkose_token: Optional[str] = None
    data_build: str = 'prod-db8e51e8414e068257091cf5003a62d3d4ee6ed0'


class arkReq:
    """
    Класс для представления запроса Arkose Labs.
    """

    def __init__(self, arkURL: str, arkBx: str, arkHeader: dict, arkBody: dict, arkCookies: dict, userAgent: str):
        """
        Инициализирует объект arkReq.

        Args:
            arkURL (str): URL запроса Arkose Labs.
            arkBx (str): Значение arkBx.
            arkHeader (dict): Заголовки запроса.
            arkBody (dict): Тело запроса.
            arkCookies (dict): Cookies запроса.
            userAgent (str): User-Agent.
        """
        self.arkURL = arkURL
        self.arkBx = arkBx
        self.arkHeader = arkHeader
        self.arkBody = arkBody
        self.arkCookies = arkCookies
        self.userAgent = userAgent


def get_har_files() -> list[str]:
    """
    Получает список файлов HAR из директории cookies.

    Returns:
        list[str]: Список путей к HAR файлам.

    Raises:
        NoValidHarFileError: Если директория cookies не читаема или не содержит HAR файлов.
    """
    if not os.access(get_cookies_dir(), os.R_OK):
        raise NoValidHarFileError('har_and_cookies dir is not readable')
    harPath = []
    for root, _, files in os.walk(get_cookies_dir()):
        for file in files:
            if file.endswith('.har'):
                harPath.append(os.path.join(root, file))
    if not harPath:
        raise NoValidHarFileError('No .har file found')
    harPath.sort(key=lambda x: os.path.getmtime(x))
    return harPath


def readHAR(request_config: RequestConfig) -> None:
    """
    Читает HAR файлы и извлекает необходимые данные для конфигурации запроса.

    Args:
        request_config (RequestConfig): Объект конфигурации запроса.

    Raises:
        NoValidHarFileError: Если не найден proof_token в HAR файлах.
    """
    for path in get_har_files():
        with open(path, 'rb') as file:
            try:
                harFile = json.loads(file.read())
            except json.JSONDecodeError as ex:
                logger.error('Error decoding HAR file', ex, exc_info=True)
                continue
            for v in harFile['log']['entries']:
                v_headers = get_headers(v)
                if arkose_url == v['request']['url']:
                    request_config.arkose_request = parseHAREntry(v)
                elif v['request']['url'].startswith(start_url):
                    try:
                        match = re.search(r'"accessToken":"(.*?)"', v['response']['content']['text'])
                        if match:
                            request_config.access_token = match.group(1)
                    except KeyError:
                        pass
                    try:
                        if 'openai-sentinel-proof-token' in v_headers:
                            request_config.headers = v_headers
                            request_config.proof_token = json.loads(base64.b64decode(
                                v_headers['openai-sentinel-proof-token'].split('gAAAAAB', 1)[-1].encode()
                            ).decode())
                        if 'openai-sentinel-turnstile-token' in v_headers:
                            request_config.turnstile_token = v_headers['openai-sentinel-turnstile-token']
                        if 'authorization' in v_headers:
                            request_config.access_token = v_headers['authorization'].split(' ')[1]
                        request_config.cookies = {c['name']: c['value'] for c in v['request']['cookies']}
                    except Exception as ex:
                        logger.error('Error on read headers', ex, exc_info=True)
    if request_config.proof_token is None:
        raise NoValidHarFileError('No proof_token found in .har files')


def get_headers(entry: dict) -> dict:
    """
    Извлекает заголовки из записи HAR, приводя их к нижнему регистру.

    Args:
        entry (dict): Запись HAR.

    Returns:
        dict: Словарь заголовков.
    """
    return {h['name'].lower(): h['value'] for h in entry['request']['headers'] if
            h['name'].lower() not in ['content-length', 'cookie'] and not h['name'].startswith(':')}


def parseHAREntry(entry: dict) -> arkReq:
    """
    Разбирает запись HAR и создает объект arkReq.

    Args:
        entry (dict): Запись HAR.

    Returns:
        arkReq: Объект arkReq.
    """
    tmpArk = arkReq(
        arkURL=entry['request']['url'],
        arkBx='',
        arkHeader=get_headers(entry),
        arkBody={p['name']: unquote(p['value']) for p in entry['request']['postData']['params'] if
                 p['name'] not in ['rnd']},
        arkCookies={c['name']: c['value'] for c in entry['request']['cookies']},
        userAgent=''
    )
    tmpArk.userAgent = tmpArk.arkHeader.get('user-agent', '')
    bda = tmpArk.arkBody['bda']
    bw = tmpArk.arkHeader['x-ark-esync-value']
    tmpArk.arkBx = decrypt(bda, tmpArk.userAgent + bw)
    return tmpArk


def genArkReq(chatArk: arkReq) -> arkReq:
    """
    Генерирует новый объект arkReq на основе существующего.

    Args:
        chatArk (arkReq): Объект arkReq.

    Returns:
        arkReq: Новый объект arkReq.

    Raises:
        RuntimeError: Если .har файл не валидный.
    """
    tmpArk: arkReq = deepcopy(chatArk)
    if tmpArk is None or not tmpArk.arkBody or not tmpArk.arkHeader:
        raise RuntimeError('The .har file is not valid')
    bda, bw = getBDA(tmpArk)

    tmpArk.arkBody['bda'] = base64.b64encode(bda.encode()).decode()
    tmpArk.arkBody['rnd'] = str(random.random())
    tmpArk.arkHeader['x-ark-esync-value'] = bw
    return tmpArk


async def sendRequest(tmpArk: arkReq, proxy: Optional[str] = None) -> str:
    """
    Отправляет асинхронный запрос Arkose Labs.

    Args:
        tmpArk (arkReq): Объект arkReq.
        proxy (Optional[str]): Прокси для запроса.

    Returns:
        str: Токен Arkose Labs.

    Raises:
        RuntimeError: Если не удалось сгенерировать валидный токен Arkose Labs.
    """
    async with StreamSession(headers=tmpArk.arkHeader, cookies=tmpArk.arkCookies,
                             proxies={'https': proxy}) as session:
        async with session.post(tmpArk.arkURL, data=tmpArk.arkBody) as response:
            data = await response.json()
            arkose = data.get('token')
    if 'sup=1|rid=' not in arkose:
        raise RuntimeError('No valid arkose token generated')
    return arkose


def getBDA(arkReq: arkReq) -> tuple[str, str]:
    """
    Генерирует BDA и BW для запроса Arkose Labs.

    Args:
        arkReq (arkReq): Объект arkReq.

    Returns:
        tuple[str, str]: Зашифрованный BDA и BW.
    """
    bx = arkReq.arkBx

    bx = re.sub(r'"key":"n","value":"\\S*?"', f'"key":"n","value":"{getN()}"', bx)
    oldUUID_search = re.search(r'"key":"4b4b269e68","value":"(\\S*?)"', bx)
    if oldUUID_search:
        oldUUID = oldUUID_search.group(1)
        newUUID = str(uuid.uuid4())
        bx = bx.replace(oldUUID, newUUID)

    bw = getBw(getBt())
    encrypted_bx = encrypt(bx, arkReq.userAgent + bw)
    return encrypted_bx, bw


def getBt() -> int:
    """
    Получает текущее время в формате Unix timestamp.

    Returns:
        int: Текущее время в формате Unix timestamp.
    """
    return int(time.time())


def getBw(bt: int) -> str:
    """
    Вычисляет значение Bw на основе времени Bt.

    Args:
        bt (int): Время Bt.

    Returns:
        str: Значение Bw.
    """
    return str(bt - (bt % 21600))


def getN() -> str:
    """
    Генерирует значение N на основе текущего времени.

    Returns:
        str: Значение N, закодированное в base64.
    """
    timestamp = str(int(time.time()))
    return base64.b64encode(timestamp.encode()).decode()


async def get_request_config(request_config: RequestConfig, proxy: str) -> RequestConfig:
    """
    Получает конфигурацию запроса, включая токены Arkose Labs.

    Args:
        request_config (RequestConfig): Объект конфигурации запроса.
        proxy (str): Прокси для запроса.

    Returns:
        RequestConfig: Объект конфигурации запроса с токенами Arkose Labs.
    """
    if request_config.proof_token is None:
        readHAR(request_config)
    if request_config.arkose_request is not None:
        request_config.arkose_token = await sendRequest(genArkReq(request_config.arkose_request), proxy)
    return request_config