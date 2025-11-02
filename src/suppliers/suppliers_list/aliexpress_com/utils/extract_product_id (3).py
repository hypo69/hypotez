## \file /src/suppliers/aliexpress/utils/extract_product_id (3).py
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

def extract_prod_ids(urls: str | list[str]) -> str | list[str] | None:
    """ Extracts item IDs from a list of URLs or directly returns IDs if given.
    
    Args:
        urls (str | list[str]): A URL or a list of URLs containing item IDs.
    
    Returns:
        str | list[str] | None: A list of extracted item IDs, a single ID, or `None` if no valid ID is found.
    
    Examples:
        >>> extract_prod_ids("https://www.aliexpress_com.com/item/123456.html")
        '123456'
        
        >>> extract_prod_ids(["https://www.aliexpress_com.com/item/123456.html", "7891011.html"])
        ['123456', '7891011']
        
        >>> extract_prod_ids(["https://www.example.com/item/123456.html", "https://www.example.com/item/abcdef.html"])
        None
        
        >>> extract_prod_ids("https://www.example.com/item/abcdef.html")
        None
    """
    # Regular expression to find product identifiers
    pattern = re.compile(r'(?:item/|/)?(\d+)\.html')

    def extract_id(url: str) -> str | None:
        """ Extracts a product ID from a given URL.
        
        Args:
            url (str): The URL from which to extract the product ID.
        
        Returns:
            str | None: The extracted product ID or `None` if no valid ID is found.
        
        Examples:
            >>> extract_id("https://www.aliexpress_com.com/item/123456.html")
            '123456'
            
            >>> extract_id("https://www.example.com/item/abcdef.html")
            None
        """
        match = pattern.search(url)
        if match:
            return match.group(1)
        return

    if isinstance(urls, list):
        return [extract_id(url) for url in urls if extract_id(url) is not None]
    else:
        return extract_id(urls)
