### **Анализ кода модуля `cookies.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/cookies.py

Модуль предназначен для работы с cookies, их загрузки из браузеров и файлов, а также для управления cookies в контексте библиотеки `g4f`.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код достаточно хорошо структурирован и содержит функции для различных аспектов работы с cookies.
    - Используется `try-except` для обработки возможных ошибок при импорте и чтении файлов.
    - Присутствуют логи для отладки.
- **Минусы**:
    - Не все функции имеют подробные docstring, особенно это касается внутренних функций и лямбда-функций.
    - Отсутствуют аннотации типов для некоторых переменных.
    - Есть участки кода, которые можно упростить или сделать более читаемыми.
    - Местами используется смешанный стиль кавычек (как двойные, так и одинарные).

**Рекомендации по улучшению:**

1.  **Документация**:
    *   Добавить docstring для всех функций, включая внутренние и лямбда-функции.
    *   Описать параметры и возвращаемые значения каждой функции.
    *   Перевести все docstring на русский язык.
2.  **Аннотации типов**:
    *   Добавить аннотации типов для всех переменных, где это возможно.
3.  **Форматирование**:
    *   Привести код в соответствие со стандартом PEP8, используя одинарные кавычки для строк.
    *   Удалить неиспользуемые импорты.
4.  **Логирование**:
    *   Использовать `logger` из `src.logger` для логирования ошибок и отладочной информации.
5.  **Обработка ошибок**:
    *   Улучшить обработку исключений, логируя ошибки с использованием `logger.error` и передавая информацию об исключении.
6.  **Упрощение кода**:
    *   Избавиться от дублирования кода, вынеся повторяющиеся блоки в отдельные функции.

**Оптимизированный код:**

```python
from __future__ import annotations

import os
import time
import json
from typing import Dict, Cookies, List, Optional
from pathlib import Path

from src.logger import logger

try:
    from platformdirs import user_config_dir

    has_platformdirs = True
except ImportError:
    has_platformdirs = False

try:
    from browser_cookie3 import (
        chrome, chromium, opera, opera_gx,
        brave, edge, vivaldi, firefox,
        _LinuxPasswordManager, BrowserCookieError
    )

    def g4f(domain_name: str) -> list:
        """
        Загружает cookies из браузера 'g4f' (если он существует).

        Args:
            domain_name (str): Домен, для которого загружаются cookies.

        Returns:
            list: Список cookies.
        """
        if not has_platformdirs:
            return []
        user_data_dir = user_config_dir('g4f')
        cookie_file = os.path.join(user_data_dir, 'Default', 'Cookies')
        return [] if not os.path.exists(cookie_file) else chrome(cookie_file, domain_name)

    browsers = [
        g4f,
        chrome, chromium, firefox, opera, opera_gx,
        brave, edge, vivaldi,
    ]
    has_browser_cookie3 = True
except ImportError:
    has_browser_cookie3 = False
    browsers = []

from .errors import MissingRequirementsError
from . import debug

class CookiesConfig():
    """
    Конфигурация cookies.
    """
    cookies: Dict[str, Cookies] = {}
    cookies_dir: str = './har_and_cookies'

DOMAINS = [
    '.bing.com',
    '.meta.ai',
    '.google.com',
    'www.whiterabbitneo.com',
    'huggingface.co',
    'chat.reka.ai',
    'chatgpt.com',
    '.cerebras.ai',
    'github.com',
    'huggingface.co',
    '.huggingface.co'
]

if has_browser_cookie3 and os.environ.get('DBUS_SESSION_BUS_ADDRESS') == '/dev/null':
    _LinuxPasswordManager.get_password = lambda a, b: b'secret'

def get_cookies(domain_name: str, raise_requirements_error: bool = True, single_browser: bool = False, cache_result: bool = True) -> Dict[str, str]:
    """
    Загружает cookies для заданного домена из всех поддерживаемых браузеров и кэширует результаты.

    Args:
        domain_name (str): Домен, для которого загружаются cookies.
        raise_requirements_error (bool): Вызывать ли исключение, если не установлены необходимые библиотеки. По умолчанию True.
        single_browser (bool): Загружать ли cookies только из одного браузера. По умолчанию False.
        cache_result (bool): Кэшировать ли результаты. По умолчанию True.

    Returns:
        Dict[str, str]: Словарь с именами и значениями cookie.
    """
    if cache_result and domain_name in CookiesConfig.cookies:
        return CookiesConfig.cookies[domain_name]

    cookies = load_cookies_from_browsers(domain_name, raise_requirements_error, single_browser)
    if cache_result:
        CookiesConfig.cookies[domain_name] = cookies
    return cookies

def set_cookies(domain_name: str, cookies: Cookies = None) -> None:
    """
    Устанавливает cookies для заданного домена.

    Args:
        domain_name (str): Домен, для которого устанавливаются cookies.
        cookies (Cookies, optional): Словарь с cookies. По умолчанию None.
    """
    if cookies:
        CookiesConfig.cookies[domain_name] = cookies
    elif domain_name in CookiesConfig.cookies:
        CookiesConfig.cookies.pop(domain_name)

def load_cookies_from_browsers(domain_name: str, raise_requirements_error: bool = True, single_browser: bool = False) -> Cookies:
    """
    Вспомогательная функция для загрузки cookies из различных браузеров.

    Args:
        domain_name (str): Домен, для которого загружаются cookies.
        raise_requirements_error (bool): Вызывать ли исключение, если не установлены необходимые библиотеки. По умолчанию True.
        single_browser (bool): Загружать ли cookies только из одного браузера. По умолчанию False.

    Returns:
        Dict[str, str]: Словарь с именами и значениями cookie.
    """
    if not has_browser_cookie3:
        if raise_requirements_error:
            raise MissingRequirementsError('Install "browser_cookie3" package')
        return {}
    cookies = {}
    for cookie_fn in browsers:
        try:
            cookie_jar = cookie_fn(domain_name=domain_name)
            if len(cookie_jar):
                debug.log(f'Read cookies from {cookie_fn.__name__} for {domain_name}')
            for cookie in cookie_jar:
                if cookie.name not in cookies:
                    if not cookie.expires or cookie.expires > time.time():
                        cookies[cookie.name] = cookie.value
            if single_browser and len(cookie_jar):
                break
        except BrowserCookieError:
            pass
        except Exception as ex:
            logger.error(f'Error reading cookies from {cookie_fn.__name__} for {domain_name}', ex, exc_info=True)
    return cookies

def set_cookies_dir(dir: str) -> None:
    """
    Устанавливает директорию для хранения файлов cookies.

    Args:
        dir (str): Путь к директории.
    """
    CookiesConfig.cookies_dir = dir

def get_cookies_dir() -> str:
    """
    Возвращает директорию для хранения файлов cookies.

    Returns:
        str: Путь к директории.
    """
    return CookiesConfig.cookies_dir

def read_cookie_files(dirPath: str = None) -> None:
    """
    Читает файлы cookies из указанной директории.

    Args:
        dirPath (str, optional): Путь к директории. По умолчанию None, используется CookiesConfig.cookies_dir.
    """
    dirPath = CookiesConfig.cookies_dir if dirPath is None else dirPath
    if not os.access(dirPath, os.R_OK):
        debug.log(f'Read cookies: {dirPath} dir is not readable')
        return

    def get_domain(v: dict) -> Optional[str]:
        """
        Извлекает домен из HAR-файла.

        Args:
            v (dict): Запись из HAR-файла.

        Returns:
            str, optional: Домен, если найден.
        """
        host = [h['value'] for h in v['request']['headers'] if h['name'].lower() in ('host', ':authority')]
        if not host:
            return None
        host = host.pop()
        for d in DOMAINS:
            if d in host:
                return d
        return None

    harFiles: List[str] = []
    cookieFiles: List[str] = []
    for root, _, files in os.walk(dirPath):
        for file in files:
            if file.endswith('.har'):
                harFiles.append(os.path.join(root, file))
            elif file.endswith('.json'):
                cookieFiles.append(os.path.join(root, file))

    CookiesConfig.cookies = {}
    for path in harFiles:
        with open(path, 'rb') as file:
            try:
                harFile = json.load(file)
            except json.JSONDecodeError:
                logger.error(f'Error decoding HAR file: {path}', exc_info=True)
                continue
            debug.log(f'Read .har file: {path}')
            new_cookies = {}
            for v in harFile['log']['entries']:
                domain = get_domain(v)
                if domain is None:
                    continue
                v_cookies = {}
                for c in v['request']['cookies']:
                    v_cookies[c['name']] = c['value']
                if len(v_cookies) > 0:
                    CookiesConfig.cookies[domain] = v_cookies
                    new_cookies[domain] = len(v_cookies)
            for domain, new_values in new_cookies.items():
                debug.log(f'Cookies added: {new_values} from {domain}')
    for path in cookieFiles:
        with open(path, 'rb') as file:
            try:
                cookieFile = json.load(file)
            except json.JSONDecodeError as ex:
                logger.error(f'Error decoding JSON file: {path}', ex, exc_info=True)
                continue
            if not isinstance(cookieFile, list) or not isinstance(cookieFile[0], dict) or 'domain' not in cookieFile[0]:
                continue
            debug.log(f'Read cookie file: {path}')
            new_cookies = {}
            for c in cookieFile:
                if isinstance(c, dict) and 'domain' in c:
                    if c['domain'] not in new_cookies:
                        new_cookies[c['domain']] = {}
                    new_cookies[c['domain']][c['name']] = c['value']
            for domain, new_values in new_cookies.items():
                CookiesConfig.cookies[domain] = new_values
                debug.log(f'Cookies added: {len(new_values)} from {domain}')