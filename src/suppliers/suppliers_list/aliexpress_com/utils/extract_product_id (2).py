## \file /src/suppliers/aliexpress/utils/extract_product_id (2).py
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


""" Extract product ID from the URL 
@code
# Example usage
urls = ["https://www.aliexpress_com.com/item/123456.html", "7891011.html", "https://www.aliexpress_com.com/item/987654.html"]
product_ids = extract_prod_ids(urls)
print(product_ids)  # Output: ['123456', '7891011', '987654']
@endcode
"""


import re
from src.logger.logger import logger

def extract_prod_ids(urls: list | str) -> list | str:
    """ Extracts item IDs from a list of URLs or directly returns IDs if given.
    @param urls: List of URLs or IDs containing item IDs.
    @return: List of extracted item IDs or a single ID.
    @code
        urls = ["https://www.aliexpress_com.com/item/123456.html", "7891011.html", "https://www.aliexpress_com.com/item/987654.html"]
        product_ids = extract_prod_ids(urls)
        print(product_ids)  # Output: ['123456', '7891011', '987654']
    @endcode
    """
    # Regular expression to find product identifiers
    pattern = re.compile(r'(?:item/|/)?(\d+)\.html')
    
    def extract_id(url: str) -> str:
        match = pattern.search(url)
        if match:
            return match.group(1)
        #return url  # If it's already an identifier, just return it
        ...

    if isinstance(urls, list):
        return [extract_id(url) for url in urls]
    else:
        return extract_id(urls)

