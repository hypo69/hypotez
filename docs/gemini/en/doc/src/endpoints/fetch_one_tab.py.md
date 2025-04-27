# Module fetch_one_tab

## Overview

This module provides functionality for parsing target URLs from a provided OneTab URL. It utilizes the `BeautifulSoup` library for HTML parsing and `requests` for making HTTP requests.

## Details

This module is responsible for extracting target URLs and related information from a OneTab URL. It first retrieves the HTML content of the OneTab page and then parses it using BeautifulSoup. The extracted information includes:

- **URLs**: A list of target URLs found on the OneTab page.
- **Price**: The price associated with the OneTab entry (if available).
- **Description**: A description of the OneTab entry. If no description is found, the current timestamp is used as a placeholder.

## Functions

### `fetch_target_urls_onetab`

**Purpose**: This function parses target URLs, a price, and a description from a given OneTab URL.

**Parameters**:

- `one_tab_url` (str): The OneTab URL to parse.

**Returns**:

- `tuple[str, str, list[str]] | bool`: A tuple containing the extracted price, description, and a list of URLs. If an error occurs, it returns `False`.

**Raises Exceptions**:

- `requests.exceptions.RequestException`: If an error occurs during the HTTP request.

**How the Function Works**:

1. **HTTP Request**: The function sends an HTTP GET request to the provided OneTab URL.
2. **HTML Parsing**: The response content is parsed using BeautifulSoup to extract the relevant information.
3. **URL Extraction**: URLs are extracted from anchor tags with the class "tabLink".
4. **Price and Description Extraction**: The price and description are extracted from a `<div>` element with the class "tabGroupLabel".
5. **Data Handling**: The extracted price is converted to an integer if it's a valid number, and a default timestamp is used if no description is found.
6. **Return Values**: The function returns a tuple containing the price, description, and a list of URLs.

**Examples**:

```python
# Example 1: Successful parsing
one_tab_url = "https://onetab.com/page/your-onetab-url"
price, description, urls = fetch_target_urls_onetab(one_tab_url)
print(f"Price: {price}")
print(f"Description: {description}")
print(f"URLs: {urls}")

# Example 2: Error during HTTP request
one_tab_url = "https://invalid-url.com"
result = fetch_target_urls_onetab(one_tab_url)
if result:
    # Process the result
else:
    print("Error occurred during request.")
```
```python
                ## \\file /src/endpoints/fetch_one_tab.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Разбор ссылок из OneTab
========================
.. module:: src.endpoints.fetch_one_tab 
    :platform: Windows, Unix
    :synopsis: Разбор ссылок из OneTab
"""

from bs4 import BeautifulSoup
import requests

import header
from src import gs
from src.logger import logger

def fetch_target_urls_onetab(one_tab_url: str) -> tuple[str, str, list[str]] | bool:
    """
    Функция паресит целевые URL из полученного OneTab.
    """
    try:
        response = requests.get(one_tab_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Извлечение ссылок
        urls = [a["href"] for a in soup.find_all("a", class_="tabLink")]

        # Извлечение данных из div с классом \'tabGroupLabel\'
        element = soup.find("div", class_="tabGroupLabel")
        data = element.get_text() if element else None

        if not data:
            price = ""
            description = gs.now
        else:
            # Разбивка данных на цену и имя
            parts = data.split(maxsplit=1)
            price = int(parts[0]) if parts[0].isdigit() else ""
            description = parts[1] if len(parts) > 1 else gs.now

        return price, description, urls

    except requests.exceptions.RequestException as ex:
        logger.error(f"Ошибка при выполнении запроса: {one_tab_url=}", ex)
        ...
        return False, False, False

                ```