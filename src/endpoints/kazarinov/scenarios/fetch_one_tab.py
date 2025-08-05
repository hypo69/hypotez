## \file /src/endpoints/fetch_one_tab.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Разбор ссылок из OneTab
=========================
.. module:: src.endpoints.fetch_one_tab 
    :platform: Windows, Unix
    :synopsis: Разбор ссылок из OneTab
"""
                                
from bs4 import BeautifulSoup
import requests

import header
from src import gs
from src.endpoints.fetch_one_tab import fetch_one_tab_data as fetch
from src.logger import logger

def fetch_one_tab_data(one_tab_url: str) -> tuple[str, str, list[str]] | bool:
    """
    Функция паресит целевые URL из полученного OneTab.
    """
    try:
        label, urls = fetch(one_tab_url)
       
        if not label:
            price = ""
            description = gs.now
        else:
            # Разбивка данных на цену и имя
            parts = label.split(maxsplit=1)
            price = int(parts[0]) if parts[0].isdigit() else ""
            mexiron_name = parts[1] if len(parts) > 1 else gs.now
        return  mexiron_name, price, urls


    except requests.exceptions.RequestException as ex:
        logger.error(f"Ошибка при выполнении запроса: {one_tab_url=}", ex)
        ...
        return False, False
