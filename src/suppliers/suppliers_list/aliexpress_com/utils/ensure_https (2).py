## \file /src/suppliers/aliexpress/utils/ensure_https (2).py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.utils 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.suppliers.suppliers_list.aliexpress_com.utils """



""" Строит https для prod_id 
@code
# Example usage
url = "example_product_id"
url_with_https = ensure_https(url)
print(url_with_https)  # Output: https://www.aliexpress_com.com/item/example_product_id.html

urls = ["example_product_id1", "https://www.aliexpress_com.com/item/example_product_id2.html"]
urls_with_https = ensure_https(urls)
print(urls_with_https)  # Output: ['https://www.aliexpress_com.com/item/example_product_id1.html', 'https://www.aliexpress_com.com/item/example_product_id2.html']
@endcode
"""
...
from pathlib import WindowsPath

from src import logger
from .extract_product_id import extract_prod_ids

def ensure_https(prod_ids: str | list) -> str | list:
    """ Ensures that the provided URL string(s) contain the https:// prefix.
    If not, it adds the https:// prefix to the URL.

    @param prod_ids The URL string or list of URL strings to check and modify if necessary.
    @return The URL string or list of URL strings with the https:// prefix.
    """
    def ensure_https_single(prod_id: str) -> str:
        if isinstance(prod_id, WindowsPath):
            raise logger.error(f"prod_id {prod_id}")
            ...
        _prod_id = prod_id if isinstance(prod_id, int) else extract_prod_ids(prod_id)
        if _prod_id:
            return fr"https://aliexpress_com.com/item/{_prod_id}.html"
        else:
            logger.critiacal(f"Какая-то бяка в {prod_id=}")
            ...
        
    if isinstance(prod_ids, list):
        return [ensure_https_single(prod_id) for prod_id in prod_ids]
    else:
        return ensure_https_single(prod_ids)


