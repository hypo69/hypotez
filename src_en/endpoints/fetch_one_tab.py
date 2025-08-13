# # \file /src/endpoints/fetch_one_tab.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3
"""Analysis of links from OneTab
============================
.. Module :: src.endpoints.fetch_one_tab 
    : Platform: Windows, Unix
    : synopsis: analysis of links from OneTab"""

from bs4 import BeautifulSoup
import requests

import header
from src import gs
from src.logger import logger

def fetch_one_tab_data(one_tab_url: str) -> tuple[str, str, list[str]] | bool:
    """Function Pareste target URL from the resulting OneTab."""
    try:
        response = requests.get(one_tab_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Removing links
        urls = [a["href"] for a in soup.find_all("a", class_="tabLink")]

        # Data from DIV with the Class 'TabGroupLabel'
        element = soup.find("div", class_="tabGroupLabel")
        onetab_label:str = element.get_text() if element else ''

       

        return onetab_label, urls

    except requests.exceptions.RequestException as ex:
        logger.error(f"Ошибка при выполнении запроса: {one_tab_url=}", ex)
        ...
        return False, False
