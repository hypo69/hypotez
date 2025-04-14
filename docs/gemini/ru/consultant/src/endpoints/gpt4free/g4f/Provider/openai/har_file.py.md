### **Анализ кода модуля `har_file.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код разбит на функции, что облегчает его понимание и поддержку.
    - Используются аннотации типов.
    - Присутствуют обработки исключений.
- **Минусы**:
    - Отсутствует подробная документация.
    - Не везде используется `logger` для логирования.
    - Не все переменные аннотированы.
    - Присутствуют смешанные стили кавычек (используются и двойные, и одинарные).
    - Не все функции содержат docstring.
    - Местами код трудночитаем из-за отсутствия пробелов и форматирования.

**Рекомендации по улучшению:**

1.  **Добавить документацию**:
    *   Добавить docstring к каждой функции и классу, объясняющий их назначение, аргументы, возвращаемые значения и возможные исключения.
    *   Добавить описание модуля в начале файла.

2.  **Логирование**:
    *   Заменить `print` на `logger.debug` или `logger.info` для отладочных сообщений.
    *   Логировать ошибки с использованием `logger.error` и передавать исключение `ex` в качестве аргумента.

3.  **Форматирование**:
    *   Привести весь код к единому стилю кавычек (одинарные).
    *   Добавить пробелы вокруг операторов присваивания.
    *   Использовать более понятные имена переменных.

4.  **Обработка исключений**:
    *   Конкретизировать типы исключений в блоках `except`.
    *   Добавить логирование ошибок в блоках `except`.

5.  **Аннотации типов**:
    *   Добавить аннотации типов для всех переменных, где это возможно.

6.  **Удалить неиспользуемые импорты**:
    *   Удалить импорты, которые не используются в коде.

7. **Использовать `j_loads` или `j_loads_ns`**:
- Для чтения JSON или конфигурационных файлов замените стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.

**Оптимизированный код:**

```python
"""
Модуль для работы с HAR файлами для получения конфигурации.
==============================================================

Модуль содержит функции для чтения, парсинга и обработки HAR (HTTP Archive) файлов,
используемых для извлечения конфигурационных данных, таких как access_token, proof_token,
turnstile_token и arkose_token, необходимых для взаимодействия с API.

Пример использования:
----------------------

>>> request_config = RequestConfig()
>>> await get_request_config(request_config, proxy='your_proxy')
>>> print(request_config.access_token)
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

from src.logger import logger # Используем logger из src.logger
from .crypt import decrypt, encrypt
from ...requests import StreamSession
from ...cookies import get_cookies_dir
from ...errors import NoValidHarFileError

arkose_url = 'https://tcr9i.chat.openai.com/fc/gt2/public_key/35536E1E-65B4-4D96-9D97-6ADB7EFF8147'
backend_url = 'https://chatgpt.com/backend-api/conversation'
backend_anon_url = 'https://chatgpt.com/backend-anon/conversation'
start_url = 'https://chatgpt.com/'
conversation_url = 'https://chatgpt.com/c/'


class RequestConfig:
    """
    Класс для хранения конфигурации запроса.
    """
    cookies: Optional[Dict[str, str]] = None
    headers: Optional[Dict[str, str]] = None
    access_token: Optional[str] = None
    proof_token: Optional[list] = None
    turnstile_token: Optional[str] = None
    arkose_request: Optional['arkReq'] = None
    arkose_token: Optional[str] = None
    data_build: str = 'prod-db8e51e8414e068257091cf5003a62d3d4ee6ed0'


class arkReq:
    """
    Класс для хранения данных, необходимых для запроса Arkose.
    """
    def __init__(self, arkURL: str, arkBx: str, arkHeader: dict, arkBody: dict, arkCookies: dict, userAgent: str):
        """
        Инициализирует объект arkReq.

        Args:
            arkURL (str): URL для запроса Arkose.
            arkBx (str): Значение arkBx.
            arkHeader (dict): Заголовки запроса.
            arkBody (dict): Тело запроса.
            arkCookies (dict): Куки запроса.
            userAgent (str): User-agent.
        """
        self.arkURL = arkURL
        self.arkBx = arkBx
        self.arkHeader = arkHeader
        self.arkBody = arkBody
        self.arkCookies = arkCookies
        self.userAgent = userAgent


def get_har_files() -> list[str]:
    """
    Получает список HAR файлов из директории с куками.

    Returns:
        list[str]: Список путей к HAR файлам.

    Raises:
        NoValidHarFileError: Если директория с HAR файлами не читаема или не найдено ни одного HAR файла.
    """
    if not os.access(get_cookies_dir(), os.R_OK):
        raise NoValidHarFileError('har_and_cookies dir is not readable')

    har_paths = []
    for root, _, files in os.walk(get_cookies_dir()):
        for file in files:
            if file.endswith('.har'):
                har_paths.append(os.path.join(root, file))

    if not har_paths:
        raise NoValidHarFileError('No .har file found')

    har_paths.sort(key=lambda x: os.path.getmtime(x))
    return har_paths


def readHAR(request_config: RequestConfig):
    """
    Читает HAR файлы и извлекает из них необходимые данные для конфигурации запроса.

    Args:
        request_config (RequestConfig): Объект конфигурации запроса.

    Raises:
        NoValidHarFileError: Если не найден proof_token в HAR файлах.
    """
    for path in get_har_files():
        try:
            with open(path, 'rb') as file:
                try:
                    har_file = json.loads(file.read())
                except json.JSONDecodeError as ex:
                    logger.error(f'Error decoding HAR file {path}', ex, exc_info=True)
                    continue # Если файл не HAR, переходим к следующему
        except Exception as ex:
            logger.error(f'Error reading HAR file {path}', ex, exc_info=True)
            continue

        for entry in har_file['log']['entries']:
            entry_headers = get_headers(entry)

            if arkose_url == entry['request']['url']:
                request_config.arkose_request = parseHAREntry(entry)
            elif entry['request']['url'].startswith(start_url):
                try:
                    match = re.search(r'"accessToken":"(.*?)"', entry['response']['content']['text'])
                    if match:
                        request_config.access_token = match.group(1)
                except KeyError:
                    pass

                try:
                    if 'openai-sentinel-proof-token' in entry_headers:
                        request_config.headers = entry_headers
                        request_config.proof_token = json.loads(base64.b64decode(
                            entry_headers['openai-sentinel-proof-token'].split('gAAAAAB', 1)[-1].encode()
                        ).decode())
                    if 'openai-sentinel-turnstile-token' in entry_headers:
                        request_config.turnstile_token = entry_headers['openai-sentinel-turnstile-token']
                    if 'authorization' in entry_headers:
                        request_config.access_token = entry_headers['authorization'].split(' ')[1]
                    request_config.cookies = {c['name']: c['value'] for c in entry['request']['cookies']}
                except Exception as ex:
                    logger.error(f'Error on read headers: {ex}', exc_info=True)

    if request_config.proof_token is None:
        raise NoValidHarFileError('No proof_token found in .har files')


def get_headers(entry) -> dict:
    """
    Извлекает заголовки из записи HAR файла.

    Args:
        entry: Запись HAR файла.

    Returns:
        dict: Словарь с заголовками, приведенными к нижнему регистру.
    """
    return {
        h['name'].lower(): h['value']
        for h in entry['request']['headers']
        if h['name'].lower() not in ['content-length', 'cookie'] and not h['name'].startswith(':')
    }


def parseHAREntry(entry) -> arkReq:
    """
    Парсит запись HAR файла для получения данных запроса Arkose.

    Args:
        entry: Запись HAR файла.

    Returns:
        arkReq: Объект arkReq с данными запроса Arkose.
    """
    tmp_ark = arkReq(
        arkURL=entry['request']['url'],
        arkBx='',
        arkHeader=get_headers(entry),
        arkBody={
            p['name']: unquote(p['value'])
            for p in entry['request']['postData']['params']
            if p['name'] not in ['rnd']
        },
        arkCookies={c['name']: c['value'] for c in entry['request']['cookies']},
        userAgent=''
    )
    tmp_ark.userAgent = tmp_ark.arkHeader.get('user-agent', '')
    bda = tmp_ark.arkBody['bda']
    bw = tmp_ark.arkHeader['x-ark-esync-value']
    tmp_ark.arkBx = decrypt(bda, tmp_ark.userAgent + bw)
    return tmp_ark


def genArkReq(chat_ark: arkReq) -> arkReq:
    """
    Генерирует запрос Arkose на основе переданного объекта arkReq.

    Args:
        chat_ark (arkReq): Объект arkReq, на основе которого генерируется запрос.

    Returns:
        arkReq: Объект arkReq с обновленными данными для запроса Arkose.

    Raises:
        RuntimeError: Если переданный объект arkReq не валиден.
    """
    tmp_ark: arkReq = deepcopy(chat_ark)
    if tmp_ark is None or not tmp_ark.arkBody or not tmp_ark.arkHeader:
        raise RuntimeError('The .har file is not valid')

    bda, bw = getBDA(tmp_ark)

    tmp_ark.arkBody['bda'] = base64.b64encode(bda.encode()).decode()
    tmp_ark.arkBody['rnd'] = str(random.random())
    tmp_ark.arkHeader['x-ark-esync-value'] = bw
    return tmp_ark


async def sendRequest(tmp_ark: arkReq, proxy: str = None) -> str:
    """
    Отправляет асинхронный POST запрос для получения токена Arkose.

    Args:
        tmp_ark (arkReq): Объект arkReq с данными для запроса.
        proxy (str, optional): Прокси для запроса. По умолчанию None.

    Returns:
        str: Токен Arkose.

    Raises:
        RuntimeError: Если не удалось сгенерировать валидный токен Arkose.
    """
    async with StreamSession(headers=tmp_ark.arkHeader, cookies=tmp_ark.arkCookies, proxies={'https': proxy}) as session:
        try:
            async with session.post(tmp_ark.arkURL, data=tmp_ark.arkBody) as response:
                data = await response.json()
                arkose = data.get('token')
        except Exception as ex:
            logger.error(f'Error sending request: {ex}', exc_info=True)
            return None

    if 'sup=1|rid=' not in arkose:
        raise RuntimeError('No valid arkose token generated')
    return arkose


def getBDA(ark_req: arkReq) -> tuple[str, str]:
    """
    Генерирует BDA (Browser Data Analysis) и BW (Browser Width) параметры для запроса Arkose.

    Args:
        ark_req (arkReq): Объект arkReq с данными для генерации BDA и BW.

    Returns:
        tuple[str, str]: Кортеж, содержащий зашифрованный BDA и BW.
    """
    bx = ark_req.arkBx

    bx = re.sub(r'"key":"n","value":"\\S*?"', f'"key":"n","value":"{getN()}"', bx)
    old_uuid_search = re.search(r'"key":"4b4b269e68","value":"(\\S*?)"', bx)
    if old_uuid_search:
        old_uuid = old_uuid_search.group(1)
        new_uuid = str(uuid.uuid4())
        bx = bx.replace(old_uuid, new_uuid)

    bw = getBw(getBt())
    encrypted_bx = encrypt(bx, ark_req.userAgent + bw)
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
    Вычисляет значение BW (Browser Width) на основе переданного времени.

    Args:
        bt (int): Время в формате Unix timestamp.

    Returns:
        str: Значение BW.
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
    Получает конфигурацию запроса, извлекая данные из HAR файлов и генерируя токен Arkose.

    Args:
        request_config (RequestConfig): Объект конфигурации запроса.
        proxy (str): Прокси для запроса.

    Returns:
        RequestConfig: Объект конфигурации запроса с заполненными данными.
    """
    if request_config.proof_token is None:
        readHAR(request_config)
    if request_config.arkose_request is not None:
        request_config.arkose_token = await sendRequest(genArkReq(request_config.arkose_request), proxy)
    return request_config