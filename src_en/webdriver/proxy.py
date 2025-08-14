# # \file /src/webdriver/proxy.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

"""Module for working with proxy
======================================================================================ward

The module determines the functions for loading and parsing of the proxy list. 
The text file with proxy addresses is loaded and distributed into categories.

An example of use
-------------------

.. Code-Block :: Python

    Download_Proxies_List ()
    Proxies = Parse_Proxies ()"""



import re
import requests
from requests.exceptions import ProxyError, RequestException
from pathlib import Path
from typing import Any, Dict, List, Optional
import header
from header import __root__
from src import gs
from src.utils.printer import pprint
from src.logger.logger import logger

# URL source of the proxy list
url: str = 'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt'

# The path to the file to save the proxy list
proxies_list_path: Path = __root__ / 'src' / 'webdriver' / 'proxies.txt'


def download_proxies_list(url: str = url, save_path: Path = proxies_list_path) -> bool:
    """Downloads the file according to the specified URL and saves it on a given path.

    : Param URL: url file for downloading.
    : Param save_path: the path to save a loaded file.
    : Return: The success of the operation."""
    try:
        # Sending a file download request
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Generates an exception for http errors

        # File saving
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        logger.info(f'Файл успешно загружен и сохранён в {save_path}')
        return True
    except Exception as ex:
        logger.error('Ошибка при загрузке файла: ', ex)
        ...
        return False


def get_proxies_dict(file_path: Path = proxies_list_path) -> Dict[str, List[Dict[str, Any]]]:
    """Parses a file with proxy addresses and distributes them into categories.

    : Param File_path: The Way to the File with the proxy.
    : Return: Dictionary with proxy types."""

    download_proxies_list()

    proxies: Dict[str, List[Dict[str, Any]]] = {
        'http': [],
        'socks4': [],
        'socks5': []
    }

    try:
        # File reading
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(r'^(http|socks4|socks5)://([\d\.]+):(\d+)', line.strip())
                if match:
                    protocol, host, port = match.groups()
                    proxies[protocol].append({'protocol':protocol, 'host': host, 'port': port})
    except FileNotFoundError as ex:
        logger.error('Файл не найден: ', ex)
        ...
    except Exception as ex:
        logger.error('Ошибка при парсинге прокси: ', ex)
        ...

    return proxies


def check_proxy(proxy: dict) -> bool:
    """Checks the performance of the proxy server.
    
    : Param Proxy: Dictionary with proxy data (Host, Port, Protocol).
    : Return: True, if proxy works, otherwise false."""
    try:
        # Trying to make a request through proxy
        response = requests.get("https://httpbin.org/ip", proxies={proxy['protocol']: f"{proxy['protocol']}://{proxy['host']}:{proxy['port']}"}, timeout=5)
        # Checking the answer code
        if response.status_code == 200:
            logger.info(f"Прокси найден: {proxy['host']}:{proxy['port']}")
            return True
        else:
            logger.warning(f"Прокси не работает: {proxy['host']}:{proxy['port']} (Статус: {response.status_code})", None, False)
            return False
    except (ProxyError, RequestException) as ex:
        logger.warning(f"Ошибка подключения через прокси {proxy['host']}:{proxy['port']}:",ex)
        return False

if __name__ == '__main__':
    # Loading the proxy and parsing list
    if download_proxies_list():
        parsed_proxies = parse_proxies()
        logger.info(f'Обработано {sum(len(v) for v in parsed_proxies.values())} прокси.')
