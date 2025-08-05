### **Анализ кода модуля `proxy`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Чёткое разделение функциональности на отдельные функции.
  - Использование логирования для отслеживания работы функций.
  - Обработка исключений при загрузке и парсинге прокси.
- **Минусы**:
  - Файл начинается с символов `#`, что не соответствует стандарту оформления файлов.
  - Отсутствуют docstring для модуля.
  - Не все переменные аннотированы типами.
  - В блоках обработки исключений используется `e` вместо `ex`.
  - Не используется `j_loads` или `j_loads_ns` для работы с конфигурационными файлами.
  - Есть устаревшие комментарии, которые требуют пересмотра.
  - Используются конструкции `...` в блоках обработки исключений.

**Рекомендации по улучшению:**

1.  **Добавить docstring для модуля**:
    -   Описать назначение модуля, основные функции и примеры использования.
2.  **Аннотировать типы переменных**:
    -   Указать типы для всех переменных, чтобы улучшить читаемость и предотвратить ошибки.
3.  **Заменить `e` на `ex` в блоках обработки исключений**:
    -   Использовать `ex` в качестве имени переменной для исключений в соответствии с рекомендациями.
4.  **Заменить `parse_proxies` на `get_proxies_dict`**:
    -   Переименовать функцию, чтобы соответствовала ее функциональности (получение словаря прокси).
5.  **Удалить `...` в блоках обработки исключений**:
    -   Заменить `...` на конкретную обработку исключений или логирование.
6.  **Улучшить логирование**:
    -   Добавить контекстную информацию в сообщения логирования, чтобы облегчить отладку.
7.  **Удалить строку `#! .pyenv/bin/python3`**:
    -   Эта строка не нужна, так как она уже указана в файле `header.py`.
8. **Улучшить форматирование**:
    -   Добавить пробелы вокруг операторов присваивания.
    -   Использовать константы для URL и путей к файлам, чтобы упростить изменение конфигурации.

**Оптимизированный код:**

```python
## \file /src/webdriver/proxy.py
# -*- coding: utf-8 -*-

"""
Модуль для работы с прокси.
=========================================================================================

Модуль определяет функции для загрузки, парсинга и проверки списка прокси.
Загружается текстовый файл со списком прокси-адресов, выполняется их парсинг
и распределение по категориям (http, socks4, socks5).
Также предоставляется функциональность для проверки работоспособности прокси-серверов.

Пример использования:
--------------------

.. code-block:: python

    download_proxies_list()
    proxies = get_proxies_dict()
    for protocol, proxy_list in proxies.items():
        for proxy in proxy_list:
            if check_proxy(proxy):
                print(f"Прокси {proxy['host']}:{proxy['port']} работает.")

"""

import re
import requests
from requests.exceptions import ProxyError, RequestException
from pathlib import Path
from typing import Any, Dict, List, Optional
from header import __root__
from src.utils.printer import pprint as print
from src.logger.logger import logger

# URL источника списка прокси
PROXY_LIST_URL: str = 'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt'

# Путь к файлу для сохранения списка прокси
PROXIES_LIST_PATH: Path = __root__ / 'src' / 'webdriver' / 'proxies.txt'


def download_proxies_list(url: str = PROXY_LIST_URL, save_path: Path = PROXIES_LIST_PATH) -> bool:
    """
    Загружает файл по указанному URL и сохраняет его в заданный путь.

    Args:
        url (str): URL файла для загрузки. По умолчанию PROXY_LIST_URL.
        save_path (Path): Путь для сохранения загруженного файла. По умолчанию PROXIES_LIST_PATH.

    Returns:
        bool: True, если файл успешно загружен и сохранен, иначе False.
    """
    try:
        # Функция отправляет запрос на загрузку файла
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Генерирует исключение для ошибок HTTP

        # Функция сохраняет файл
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        logger.info(f'Файл успешно загружен и сохранён в {save_path}')
        return True
    except RequestException as ex:
        logger.error(f'Ошибка при загрузке файла из {url}: {ex}', exc_info=True)
        return False


def get_proxies_dict(file_path: Path = PROXIES_LIST_PATH) -> Dict[str, List[Dict[str, Any]]]:
    """
    Парсит файл с прокси-адресами и распределяет их по категориям (http, socks4, socks5).

    Args:
        file_path (Path): Путь к файлу с прокси. По умолчанию PROXIES_LIST_PATH.

    Returns:
        Dict[str, List[Dict[str, Any]]]: Словарь, где ключи - типы прокси (http, socks4, socks5),
                                         а значения - списки словарей с данными прокси (protocol, host, port).
    """

    download_proxies_list()

    proxies: Dict[str, List[Dict[str, Any]]] = {
        'http': [],
        'socks4': [],
        'socks5': []
    }

    try:
        # Функция выполняет чтение файла
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(r'^(http|socks4|socks5)://([\d\.]+):(\d+)', line.strip())
                if match:
                    protocol, host, port = match.groups()
                    proxies[protocol].append({'protocol': protocol, 'host': host, 'port': port})
    except FileNotFoundError as ex:
        logger.error(f'Файл не найден: {file_path}: {ex}', exc_info=True)
    except Exception as ex:
        logger.error(f'Ошибка при парсинге прокси из файла {file_path}: {ex}', exc_info=True)

    return proxies


def check_proxy(proxy: Dict[str, str]) -> bool:
    """
    Проверяет работоспособность прокси-сервера.

    Args:
        proxy (Dict[str, str]): Словарь с данными прокси (protocol, host, port).

    Returns:
        bool: True, если прокси работает, иначе False.
    """
    try:
        # Функция пытается сделать запрос через прокси
        response = requests.get(
            "https://httpbin.org/ip",
            proxies={proxy['protocol']: f"{proxy['protocol']}://{proxy['host']}:{proxy['port']}"},
            timeout=5
        )
        # Функция проверяет код ответа
        if response.status_code == 200:
            logger.info(f"Прокси {proxy['host']}:{proxy['port']} работает")
            return True
        else:
            logger.warning(f"Прокси {proxy['host']}:{proxy['port']} не работает (Статус: {response.status_code})")
            return False
    except (ProxyError, RequestException) as ex:
        logger.warning(f"Ошибка подключения через прокси {proxy['host']}:{proxy['port']}: {ex}")
        return False


if __name__ == '__main__':
    # Загрузка списка прокси и парсинг
    if download_proxies_list():
        parsed_proxies = get_proxies_dict()
        logger.info(f'Обработано {sum(len(v) for v in parsed_proxies.values())} прокси.')