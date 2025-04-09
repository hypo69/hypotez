### **Анализ кода модуля `cookies.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Четкая структура кода, разделение на функции для загрузки и установки куки.
    - Использование `try-except` блоков для обработки возможных ошибок при импорте и чтении куки.
    - Реализована поддержка чтения куки из разных браузеров.
    - Наличие функций для работы с файлами куки (`.har` и `.json`).
- **Минусы**:
    - Отсутствует описание модуля на русском языке.
    - Не все функции и классы документированы в соответствии с требуемым форматом.
    - Не везде используется `logger` для логирования ошибок.
    - Жестко заданы домены в `DOMAINS`.
    - Не все переменные аннотированы типами.

**Рекомендации по улучшению:**

1.  **Добавить описание модуля в начале файла**:

    ```python
    """
    Модуль для работы с куками.
    =================================================

    Модуль содержит функции для загрузки, сохранения и управления куками из различных браузеров и файлов.
    Он также включает конфигурацию для хранения кук и директорию для файлов куки.
    """
    ```

2.  **Документировать функции и классы**:

    *   Необходимо добавить docstring к каждой функции, включая описание аргументов, возвращаемых значений и возможных исключений.

    ```python
    def g4f(domain_name: str) -> list:
        """
        Загружает куки из браузера 'g4f' (если он существует).

        Args:
            domain_name (str): Домен, для которого загружаются куки.

        Returns:
            list: Список кук.
        """
    ```

3.  **Использовать `logger` для логирования ошибок**:

    *   Заменить `debug.error` на `logger.error` с передачей исключения.

    ```python
    from src.logger import logger

    try:
        ...
    except Exception as ex:
        logger.error(f"Ошибка при чтении куки из {cookie_fn.__name__} для {domain_name}", ex, exc_info=True)
    ```

4.  **Аннотировать типы для всех переменных**:

    *   Добавить аннотации типов для переменных, где это необходимо.

    ```python
    harFiles: list[str] = []
    cookieFiles: list[str] = []
    ```

5.  **Улучшить читаемость кода**:

    *   Добавить пробелы вокруг операторов присваивания и других операторов.

6.  **Сделать `DOMAINS` более гибким**:

    *   Рассмотреть возможность загрузки `DOMAINS` из конфигурационного файла или переменной окружения.

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

    has_platformdirs: bool = True
except ImportError:
    has_platformdirs: bool = False
try:
    from browser_cookie3 import (
        chrome, chromium, opera, opera_gx,
        brave, edge, vivaldi, firefox,
        _LinuxPasswordManager, BrowserCookieError
    )


    def g4f(domain_name: str) -> list:
        """
        Загружает куки из браузера 'g4f' (если он существует).

        Args:
            domain_name (str): Домен, для которого загружаются куки.

        Returns:
            list: Список кук.
        """
        if not has_platformdirs:
            return []
        user_data_dir: str = user_config_dir("g4f")
        cookie_file: str = os.path.join(user_data_dir, "Default", "Cookies")
        return [] if not os.path.exists(cookie_file) else chrome(cookie_file, domain_name)


    browsers: list = [
        g4f,
        chrome, chromium, firefox, opera, opera_gx,
        brave, edge, vivaldi,
    ]
    has_browser_cookie3: bool = True
except ImportError:
    has_browser_cookie3: bool = False
    browsers: list = []

from .errors import MissingRequirementsError
from . import debug


class CookiesConfig():
    cookies: Dict[str, Cookies] = {}
    cookies_dir: str = "./har_and_cookies"


DOMAINS: list[str] = [
    ".bing.com",
    ".meta.ai",
    ".google.com",
    "www.whiterabbitneo.com",
    "huggingface.co",
    "chat.reka.ai",
    "chatgpt.com",
    ".cerebras.ai",
    "github.com",
    "huggingface.co",
    ".huggingface.co"
]

if has_browser_cookie3 and os.environ.get('DBUS_SESSION_BUS_ADDRESS') == "/dev/null":
    _LinuxPasswordManager.get_password = lambda a, b: b"secret"


def get_cookies(domain_name: str, raise_requirements_error: bool = True, single_browser: bool = False,
                cache_result: bool = True) -> Dict[str, str]:
    """
    Загружает куки для заданного домена из всех поддерживаемых браузеров и кэширует результаты.

    Args:
        domain_name (str): Домен, для которого загружаются куки.
        raise_requirements_error (bool, optional): Вызывать исключение, если не установлены необходимые библиотеки. По умолчанию True.
        single_browser (bool, optional): Загружать куки только из одного браузера. По умолчанию False.
        cache_result (bool, optional): Кэшировать результаты загрузки куки. По умолчанию True.

    Returns:
        Dict[str, str]: Словарь с именами и значениями куки.
    """
    if cache_result and domain_name in CookiesConfig.cookies:
        return CookiesConfig.cookies[domain_name]

    cookies: Dict[str, str] = load_cookies_from_browsers(domain_name, raise_requirements_error, single_browser)
    if cache_result:
        CookiesConfig.cookies[domain_name] = cookies
    return cookies


def set_cookies(domain_name: str, cookies: Cookies = None) -> None:
    """
    Устанавливает куки для заданного домена.

    Args:
        domain_name (str): Домен, для которого устанавливаются куки.
        cookies (Cookies, optional): Словарь с куками. По умолчанию None.
    """
    if cookies:
        CookiesConfig.cookies[domain_name] = cookies
    elif domain_name in CookiesConfig.cookies:
        CookiesConfig.cookies.pop(domain_name)


def load_cookies_from_browsers(domain_name: str, raise_requirements_error: bool = True,
                               single_browser: bool = False) -> Cookies:
    """
    Вспомогательная функция для загрузки куки из различных браузеров.

    Args:
        domain_name (str): Домен, для которого загружаются куки.
        raise_requirements_error (bool, optional): Вызывать исключение, если не установлены необходимые библиотеки. По умолчанию True.
        single_browser (bool, optional): Загружать куки только из одного браузера. По умолчанию False.

    Returns:
        Dict[str, str]: Словарь с именами и значениями куки.
    """
    if not has_browser_cookie3:
        if raise_requirements_error:
            raise MissingRequirementsError('Install "browser_cookie3" package')
        return {}
    cookies: Dict[str, str] = {}
    for cookie_fn in browsers:
        try:
            cookie_jar = cookie_fn(domain_name=domain_name)
            if len(cookie_jar):
                debug.log(f"Прочитаны куки из {cookie_fn.__name__} для {domain_name}")
            for cookie in cookie_jar:
                if cookie.name not in cookies:
                    if not cookie.expires or cookie.expires > time.time():
                        cookies[cookie.name] = cookie.value
            if single_browser and len(cookie_jar):
                break
        except BrowserCookieError:
            pass
        except Exception as ex:
            logger.error(f"Ошибка при чтении куки из {cookie_fn.__name__} для {domain_name}: {ex}", ex, exc_info=True)
    return cookies


def set_cookies_dir(dir: str) -> None:
    """
    Устанавливает директорию для хранения файлов куки.

    Args:
        dir (str): Путь к директории.
    """
    CookiesConfig.cookies_dir = dir


def get_cookies_dir() -> str:
    """
    Возвращает директорию для хранения файлов куки.

    Returns:
        str: Путь к директории.
    """
    return CookiesConfig.cookies_dir


def read_cookie_files(dirPath: str = None) -> None:
    """
    Считывает куки из файлов в указанной директории.

    Args:
        dirPath (str, optional): Путь к директории. По умолчанию None.
    """
    dirPath: str = CookiesConfig.cookies_dir if dirPath is None else dirPath
    if not os.access(dirPath, os.R_OK):
        debug.log(f"Чтение куки: {dirPath} директория не доступна для чтения")
        return

    def get_domain(v: dict) -> Optional[str]:
        """
        Извлекает домен из заголовков запроса.

        Args:
            v (dict): Словарь с данными запроса.

        Returns:
            str: Домен, если найден.
        """
        host: list[str] = [h["value"] for h in v['request']['headers'] if
                            h["name"].lower() in ("host", ":authority")]
        if not host:
            return None
        host: str = host.pop()
        for d in DOMAINS:
            if d in host:
                return d

    harFiles: list[str] = []
    cookieFiles: list[str] = []
    for root, _, files in os.walk(dirPath):
        for file in files:
            if file.endswith(".har"):
                harFiles.append(os.path.join(root, file))
            elif file.endswith(".json"):
                cookieFiles.append(os.path.join(root, file))

    CookiesConfig.cookies = {}
    for path in harFiles:
        with open(path, 'rb') as file:
            try:
                harFile: dict = json.load(file)
            except json.JSONDecodeError:
                logger.error(f"Не удалось декодировать HAR файл: {path}", exc_info=True)
                continue
            debug.log(f"Прочитан .har файл: {path}")
            new_cookies: Dict[str, int] = {}
            for v in harFile['log']['entries']:
                domain: Optional[str] = get_domain(v)
                if domain is None:
                    continue
                v_cookies: Dict[str, str] = {}
                for c in v['request']['cookies']:
                    v_cookies[c['name']] = c['value']
                if len(v_cookies) > 0:
                    CookiesConfig.cookies[domain] = v_cookies
                    new_cookies[domain] = len(v_cookies)
            for domain, new_values in new_cookies.items():
                debug.log(f"Куки добавлены: {new_values} из {domain}")
    for path in cookieFiles:
        with open(path, 'rb') as file:
            try:
                cookieFile: list[dict] = json.load(file)
            except json.JSONDecodeError as ex:
                logger.error(f"Не удалось декодировать JSON файл: {path}", ex, exc_info=True)
                continue
            if not isinstance(cookieFile, list) or not isinstance(cookieFile[0], dict) or "domain" not in cookieFile[0]:
                continue
            debug.log(f"Прочитан файл куки: {path}")
            new_cookies: Dict[str, Dict[str, str]] = {}
            for c in cookieFile:
                if isinstance(c, dict) and "domain" in c:
                    if c["domain"] not in new_cookies:
                        new_cookies[c["domain"]] = {}
                    new_cookies[c["domain"]][c["name"]] = c["value"]
            for domain, new_values in new_cookies.items():
                CookiesConfig.cookies[domain] = new_values
                debug.log(f"Куки добавлены: {len(new_values)} из {domain}")