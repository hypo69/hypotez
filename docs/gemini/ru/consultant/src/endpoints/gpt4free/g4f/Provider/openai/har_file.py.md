### **Анализ кода модуля `har_file.py`**

## Качество кода:

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код разбит на функции, что улучшает читаемость.
    - Используются аннотации типов.
    - Присутствуют комментарии.
- **Минусы**:
    - Не все функции и классы имеют docstring.
    - Docstring написаны на английском языке.
    - Не используется модуль `logger` для логирования ошибок.
    - В некоторых местах кода отсутствуют пробелы вокруг операторов присваивания.
    - Не всегда используется `j_loads` или `j_loads_ns` для работы с JSON.
    - Переменные и параметры функций не всегда имеют аннотации типов.
    - При обработке исключений используется `e` вместо `ex`.

## Рекомендации по улучшению:

1.  **Документация**:
    - Добавить docstring для всех функций и классов, используя формат, указанный в инструкции.
    - Перевести существующие docstring на русский язык.
    - Описать назначение каждой функции, параметры, возвращаемые значения и возможные исключения.

2.  **Логирование**:
    - Заменить `print` на `logger.error` для логирования ошибок, передавая исключение как аргумент и `exc_info=True`.
    - Добавить логирование важных этапов выполнения программы.

3.  **Использование `j_loads`**:
    - Использовать `j_loads` для чтения HAR-файлов вместо стандартных `open` и `json.load`.

4.  **Форматирование**:
    - Добавить пробелы вокруг операторов присваивания (`=`).
    - Привести код в соответствие со стандартами PEP8.

5.  **Обработка исключений**:
    - Использовать `ex` вместо `e` в блоках `except`.

6.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, параметров функций и возвращаемых значений.

7. **Вебдрайвер**:
    - В данном коде не используется webdriver, поэтому рекомендации по его использованию не применимы.

## Оптимизированный код:

```python
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
from typing import Optional, List, Dict

from .crypt import decrypt, encrypt
from ...requests import StreamSession
from ...cookies import get_cookies_dir
from ...errors import NoValidHarFileError
from ... import debug
from src.logger import logger # Добавлен импорт logger

arkose_url: str = "https://tcr9i.chat.openai.com/fc/gt2/public_key/35536E1E-65B4-4D96-9D97-6ADB7EFF8147"
backend_url: str = "https://chatgpt.com/backend-api/conversation"
backend_anon_url: str = "https://chatgpt.com/backend-anon/conversation"
start_url: str = "https://chatgpt.com/"
conversation_url: str = "https://chatgpt.com/c/"

class RequestConfig:
    """
    Конфигурация запроса для взаимодействия с API.

    Атрибуты:
        cookies (dict, optional): Куки для запроса. Defaults to None.
        headers (dict, optional): Заголовки для запроса. Defaults to None.
        access_token (str, optional): Токен доступа. Defaults to None.
        proof_token (list, optional): Proof токен. Defaults to None.
        turnstile_token (str, optional): Turnstile токен. Defaults to None.
        arkose_request (arkReq, optional): Объект запроса Arkose. Defaults to None.
        arkose_token (str, optional): Токен Arkose. Defaults to None.
        data_build (str, optional): Версия сборки данных. Defaults to "prod-db8e51e8414e068257091cf5003a62d3d4ee6ed0".
    """
    cookies: Optional[dict] = None
    headers: Optional[dict] = None
    access_token: Optional[str] = None
    proof_token: Optional[list] = None
    turnstile_token: Optional[str] = None
    arkose_request: Optional['arkReq'] = None
    arkose_token: Optional[str] = None
    data_build: str = "prod-db8e51e8414e068257091cf5003a62d3d4ee6ed0"

class arkReq:
    """
    Класс, представляющий запрос Arkose.

    Атрибуты:
        arkURL (str): URL запроса Arkose.
        arkBx (str): Значение arkBx.
        arkHeader (dict): Заголовки запроса Arkose.
        arkBody (dict): Тело запроса Arkose.
        arkCookies (dict): Куки запроса Arkose.
        userAgent (str): User-Agent.
    """
    def __init__(self, arkURL: str, arkBx: str, arkHeader: dict, arkBody: dict, arkCookies: dict, userAgent: str):
        """
        Инициализирует объект arkReq.

        Args:
            arkURL (str): URL запроса Arkose.
            arkBx (str): Значение arkBx.
            arkHeader (dict): Заголовки запроса Arkose.
            arkBody (dict): Тело запроса Arkose.
            arkCookies (dict): Куки запроса Arkose.
            userAgent (str): User-Agent.
        """
        self.arkURL: str = arkURL
        self.arkBx: str = arkBx
        self.arkHeader: dict = arkHeader
        self.arkBody: dict = arkBody
        self.arkCookies: dict = arkCookies
        self.userAgent: str = userAgent

def get_har_files() -> List[str]:
    """
    Получает список HAR-файлов из директории с куками.

    Returns:
        List[str]: Список путей к HAR-файлам.

    Raises:
        NoValidHarFileError: Если директория с куками не читаема или не найдено ни одного HAR-файла.
    """
    if not os.access(get_cookies_dir(), os.R_OK):
        raise NoValidHarFileError("har_and_cookies dir is not readable")
    harPath: List[str] = []
    for root, _, files in os.walk(get_cookies_dir()):
        for file in files:
            if file.endswith(".har"):
                harPath.append(os.path.join(root, file))
    if not harPath:
        raise NoValidHarFileError("No .har file found")
    harPath.sort(key=lambda x: os.path.getmtime(x))
    return harPath

def readHAR(request_config: RequestConfig) -> None:
    """
    Читает HAR-файлы и извлекает из них необходимые данные для конфигурации запроса.

    Args:
        request_config (RequestConfig): Объект конфигурации запроса.

    Raises:
        NoValidHarFileError: Если не найден proof_token в HAR-файлах.
    """
    for path in get_har_files():
        try:
            with open(path, 'rb') as file:
                try:
                    harFile: dict = json.loads(file.read()) # Чтение и парсинг HAR-файла
                except json.JSONDecodeError as ex:
                    logger.error(f"Ошибка при декодировании JSON в файле {path}", ex, exc_info=True)
                    continue # Переход к следующему файлу
                for v in harFile['log']['entries']:
                    v_headers: dict = get_headers(v)
                    if arkose_url == v['request']['url']:
                        request_config.arkose_request = parseHAREntry(v)
                    elif v['request']['url'].startswith(start_url):
                        try:
                            match = re.search(r'"accessToken":"(.*?)"', v["response"]["content"]["text"])
                            if match:
                                request_config.access_token = match.group(1)
                        except KeyError:
                            pass
                        try:
                            if "openai-sentinel-proof-token" in v_headers:
                                request_config.headers = v_headers
                                request_config.proof_token = json.loads(base64.b64decode(
                                    v_headers["openai-sentinel-proof-token"].split("gAAAAAB", 1)[-1].encode()
                                ).decode())
                            if "openai-sentinel-turnstile-token" in v_headers:
                                request_config.turnstile_token = v_headers["openai-sentinel-turnstile-token"]
                            if "authorization" in v_headers:
                                request_config.access_token = v_headers["authorization"].split(" ")[1]
                            request_config.cookies = {c['name']: c['value'] for c in v['request']['cookies']}
                        except Exception as ex:
                            logger.error(f"Ошибка при чтении заголовков: {ex}", ex, exc_info=True)
        except Exception as ex:
            logger.error(f"Ошибка при обработке файла {path}", ex, exc_info=True)
    if request_config.proof_token is None:
        raise NoValidHarFileError("No proof_token found in .har files")

def get_headers(entry: dict) -> dict:
    """
    Извлекает заголовки из записи HAR-файла.

    Args:
        entry (dict): Запись HAR-файла.

    Returns:
        dict: Словарь заголовков.
    """
    return {h['name'].lower(): h['value'] for h in entry['request']['headers'] if h['name'].lower() not in ['content-length', 'cookie'] and not h['name'].startswith(':')}

def parseHAREntry(entry: dict) -> arkReq:
    """
    Преобразует запись HAR-файла в объект arkReq.

    Args:
        entry (dict): Запись HAR-файла.

    Returns:
        arkReq: Объект arkReq.
    """
    tmpArk: arkReq = arkReq(
        arkURL=entry['request']['url'],
        arkBx="",
        arkHeader=get_headers(entry),
        arkBody={p['name']: unquote(p['value']) for p in entry['request']['postData']['params'] if p['name'] not in ['rnd']},
        arkCookies={c['name']: c['value'] for c in entry['request']['cookies']},
        userAgent=""
    )
    tmpArk.userAgent = tmpArk.arkHeader.get('user-agent', '')
    bda: str = tmpArk.arkBody["bda"]
    bw: str = tmpArk.arkHeader['x-ark-esync-value']
    tmpArk.arkBx = decrypt(bda, tmpArk.userAgent + bw)
    return tmpArk

def genArkReq(chatArk: arkReq) -> arkReq:
    """
    Генерирует запрос Arkose на основе предоставленного arkReq.

    Args:
        chatArk (arkReq): Объект arkReq.

    Returns:
        arkReq: Сгенерированный объект arkReq.

    Raises:
        RuntimeError: Если .har файл не валидный
    """
    tmpArk: arkReq = deepcopy(chatArk)
    if tmpArk is None or not tmpArk.arkBody or not tmpArk.arkHeader:
        raise RuntimeError("The .har file is not valid")
    bda: str, bw: str = getBDA(tmpArk)

    tmpArk.arkBody['bda'] = base64.b64encode(bda.encode()).decode()
    tmpArk.arkBody['rnd'] = str(random.random())
    tmpArk.arkHeader['x-ark-esync-value'] = bw
    return tmpArk

async def sendRequest(tmpArk: arkReq, proxy: Optional[str] = None) -> Optional[str]:
    """
    Отправляет асинхронный запрос Arkose.

    Args:
        tmpArk (arkReq): Объект arkReq.
        proxy (str, optional): Прокси-сервер. Defaults to None.

    Returns:
        str: Токен Arkose.
    """
    try:
        async with StreamSession(headers=tmpArk.arkHeader, cookies=tmpArk.arkCookies, proxies={"https": proxy}) as session:
            async with session.post(tmpArk.arkURL, data=tmpArk.arkBody) as response:
                data: dict = await response.json()
                arkose: str = data.get("token")
        if "sup=1|rid=" not in arkose:
            return None # Или выбросить исключение, если это ожидается
        return arkose
    except Exception as ex:
        logger.error("Ошибка при отправке запроса", ex, exc_info=True)
        return None

def getBDA(arkReq: arkReq) -> tuple[str, str]:
    """
    Генерирует BDA и BW для запроса Arkose.

    Args:
        arkReq (arkReq): Объект arkReq.

    Returns:
        tuple[str, str]: Кортеж, содержащий зашифрованный BX и BW.
    """
    bx: str = arkReq.arkBx
    
    bx = re.sub(r'"key":"n","value":"\\S*?"', f'"key":"n","value":"{getN()}"', bx)
    oldUUID_search = re.search(r'"key":"4b4b269e68","value":"(\\S*?)"', bx)
    if oldUUID_search:
        oldUUID: str = oldUUID_search.group(1)
        newUUID: str = str(uuid.uuid4())
        bx = bx.replace(oldUUID, newUUID)

    bw: str = getBw(getBt())
    encrypted_bx: str = encrypt(bx, arkReq.userAgent + bw)
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
    Генерирует BW на основе времени.

    Args:
        bt (int): Время.

    Returns:
        str: BW.
    """
    return str(bt - (bt % 21600))

def getN() -> str:
    """
    Генерирует значение N.

    Returns:
        str: Значение N, закодированное в Base64.
    """
    timestamp: str = str(int(time.time()))
    return base64.b64encode(timestamp.encode()).decode()

async def get_request_config(request_config: RequestConfig, proxy: Optional[str]) -> RequestConfig:
    """
    Получает конфигурацию запроса, включая токены Arkose.

    Args:
        request_config (RequestConfig): Объект конфигурации запроса.
        proxy (str, optional): Прокси-сервер. Defaults to None.

    Returns:
        RequestConfig: Обновленный объект конфигурации запроса.
    """
    if request_config.proof_token is None:
        readHAR(request_config)
    if request_config.arkose_request is not None:
        request_config.arkose_token = await sendRequest(genArkReq(request_config.arkose_request), proxy)
    return request_config