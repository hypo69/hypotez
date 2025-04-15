### **Анализ кода модуля `proxy.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Наличие docstring для модуля и функций.
    - Использование `logger` для логирования.
    - Четкое разделение на функции для загрузки, парсинга и проверки прокси.
    - Добавлены типы для переменных и параметров функций
- **Минусы**:
    - Отсутствие аннотации типов для переменных `proxies`
    - Использованы старые конструкции для определения типов переменных. Надо использовать `|` вместо `Union[]`
    - Docstring для модуля не соответствует формату, используемому в проекте.
    - Не все ошибки обрабатываются с использованием `logger.error(..., ex, exc_info=True)`.
    - В блоках `except` используется `...` вместо обработки исключений.
    - Не используется `j_loads` для чтения файлов.
    - В примере использования отсутствует путь к файлу `proxies.txt`.
    - Не все функции имеют примеры использования в docstring.
    - Функция `parse_proxies` не определена в коде, но вызывается в `if __name__ == '__main__':`.
    - В `check_proxy` при логировании `logger.warning` передается `None` и `False` как аргументы, что не соответствует сигнатуре функции.

**Рекомендации по улучшению:**

- Обновить docstring для модуля в соответствии с форматом, принятым в проекте. Добавить описание класса, пример использования.
- Добавить аннотацию типов для переменных `proxies`
- Заменить старый синтаксис `Union` на `|`
- В блоках `except` использовать `logger.error(..., ex, exc_info=True)` для логирования ошибок, заменив `...`.
- Для чтения файла использовать `j_loads`.
- Добавить примеры использования в docstring для функций `download_proxies_list`, `get_proxies_dict` и `check_proxy`.
- Убрать вызов неопределенной функции `parse_proxies` или добавить ее определение.
- Исправить вызовы `logger.warning` в функции `check_proxy`.
- Добавить обработку ошибок в функции `download_proxies_list`, `get_proxies_dict` и `check_proxy` и логировать их с использованием `logger.error`.
- В docstring для функций указать все возможные исключения, которые могут быть выброшены.
- Добавить в функцию `download_proxies_list` проверку доступности сети перед попыткой загрузки списка прокси.

**Оптимизированный код:**

```python
## \file /src/webdriver/proxy.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с прокси
=========================================================================================

Модуль определяет функции для загрузки, парсинга и проверки списка прокси.
Загружается текстовый файл с прокси-адресами и распределяется по категориям.

Пример использования
--------------------

>>> from pathlib import Path
>>> from src.webdriver.proxy import download_proxies_list, get_proxies_dict, check_proxy
>>> proxies_file_path = Path(__file__).parent / 'proxies.txt'
>>> if download_proxies_list(save_path=proxies_file_path):
...     proxies = get_proxies_dict(file_path=proxies_file_path)
...     if proxies and proxies['http']:
...         first_http_proxy = proxies['http'][0]
...         if check_proxy(first_http_proxy):
...             print(f"Первый HTTP прокси {first_http_proxy['host']}:{first_http_proxy['port']} работает.")

"""

import re
import requests
from requests.exceptions import ProxyError, RequestException
from pathlib import Path
from typing import Any, Dict, List, Optional
from header import __root__
from src.utils.printer import pprint
from src.logger.logger import logger
import socket

# URL источника списка прокси
url: str = 'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt'

# Путь к файлу для сохранения списка прокси
proxies_list_path: Path = __root__ / 'src' / 'webdriver' / 'proxies.txt'


def download_proxies_list(url: str = url, save_path: Path = proxies_list_path) -> bool:
    """
    Загружает файл по указанному URL и сохраняет его в заданный путь.

    Args:
        url (str): URL файла для загрузки. По умолчанию URL = 'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt'.
        save_path (Path): Путь для сохранения загруженного файла.  По умолчанию save_path = __root__ / 'src' / 'webdriver' / 'proxies.txt'.

    Returns:
        bool: True в случае успешной загрузки и сохранения, иначе False.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при выполнении HTTP-запроса.
        OSError: Если возникает ошибка при работе с файлом.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('proxies.txt')
        >>> result = download_proxies_list(save_path=file_path)
        >>> print(result)
        True
    """
    try:
        # Проверка доступности сети
        socket.create_connection(("8.8.8.8", 53), timeout=5)
    except OSError as ex:
        logger.error('Нет подключения к сети', ex, exc_info=True)
        return False

    try:
        # Отправка запроса на загрузку файла
        response = requests.get(url, stream=True, timeout=10)  # Добавлен таймаут для избежания зависаний
        response.raise_for_status()  # Генерирует исключение для ошибок HTTP

        # Сохранение файла
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        logger.info(f'Файл успешно загружен и сохранён в {save_path}')
        return True
    except requests.exceptions.RequestException as ex:
        logger.error(f'Ошибка при загрузке файла с URL {url}: {ex}', ex, exc_info=True)
        return False
    except OSError as ex:
        logger.error(f'Ошибка при сохранении файла в {save_path}: {ex}', ex, exc_info=True)
        return False
    except Exception as ex:
        logger.error(f'Непредвиденная ошибка при загрузке файла: {ex}', ex, exc_info=True)
        return False


def get_proxies_dict(file_path: Path = proxies_list_path) -> Dict[str, List[Dict[str, Any]]]:
    """
    Парсит файл с прокси-адресами и распределяет их по категориям.

    Args:
        file_path (Path): Путь к файлу с прокси.  По умолчанию save_path = __root__ / 'src' / 'webdriver' / 'proxies.txt'.

    Returns:
        Dict[str, List[Dict[str, Any]]]: Словарь с распределёнными по типам прокси.

    Raises:
        FileNotFoundError: Если файл не найден.
        OSError: Если возникает ошибка при чтении файла.
        re.error: Если возникает ошибка при парсинге строки прокси.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('proxies.txt')
        >>> proxies = get_proxies_dict(file_path)
        >>> if proxies:
        ...     print(f'Найдено HTTP прокси: {len(proxies["http"])}')
    """

    download_proxies_list()

    proxies: Dict[str, List[Dict[str, Any]]] = {
        'http': [],
        'socks4': [],
        'socks5': []
    }

    try:
        # Чтение файла
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(r'^(http|socks4|socks5)://([\d\.]+):(\d+)', line.strip())
                if match:
                    protocol, host, port = match.groups()
                    proxies[protocol].append({'protocol': protocol, 'host': host, 'port': port})
    except FileNotFoundError as ex:
        logger.error(f'Файл не найден: {ex}', ex, exc_info=True)
    except OSError as ex:
        logger.error(f'Ошибка при чтении файла: {ex}', ex, exc_info=True)
    except re.error as ex:
        logger.error(f'Ошибка при парсинге строки прокси: {ex}', ex, exc_info=True)
    except Exception as ex:
        logger.error(f'Непредвиденная ошибка при парсинге прокси: {ex}', ex, exc_info=True)

    return proxies


def check_proxy(proxy: Dict[str, str]) -> bool:
    """
    Проверяет работоспособность прокси-сервера.

    Args:
        proxy (dict): Словарь с данными прокси (host, port, protocol).

    Returns:
        bool: True, если прокси работает, иначе False.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при выполнении HTTP-запроса через прокси.

    Example:
        >>> proxy = {'protocol': 'http', 'host': '1.2.3.4', 'port': '8080'}
        >>> result = check_proxy(proxy)
        >>> print(result)
        False
    """
    try:
        # Попытка сделать запрос через прокси
        response = requests.get("https://httpbin.org/ip",
                                proxies={proxy['protocol']: f"{proxy['protocol']}://{proxy['host']}:{proxy['port']}"},
                                timeout=5)
        # Проверка кода ответа
        if response.status_code == 200:
            logger.info(f"Прокси работает: {proxy['host']}:{proxy['port']}")
            return True
        else:
            logger.warning(f"Прокси не работает: {proxy['host']}:{proxy['port']} (Статус: {response.status_code})")
            return False
    except (ProxyError, RequestException) as ex:
        logger.warning(f"Ошибка подключения через прокси {proxy['host']}:{proxy['port']}: {ex}")
        return False


if __name__ == '__main__':
    # Загрузка списка прокси и парсинг
    proxies_file = Path(__file__).parent / 'proxies.txt'
    if download_proxies_list(save_path=proxies_file):
        parsed_proxies = get_proxies_dict(file_path=proxies_file)
        if parsed_proxies:
            total_proxies = sum(len(v) for v in parsed_proxies.values())
            logger.info(f'Обработано {total_proxies} прокси.')
        else:
            logger.warning('Не удалось получить список прокси.')
    else:
        logger.warning('Не удалось загрузить список прокси.')