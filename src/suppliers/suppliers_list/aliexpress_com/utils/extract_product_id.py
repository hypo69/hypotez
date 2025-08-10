## \file /src/suppliers/suppliers_list/aliexpress_com/utils/extract_product_id.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.utils.extract_product_id
    :platform: Windows, Unix
    :synopsis: Extracts product IDs from AliExpress URLs or strings.

AliExpress Product ID Extraction Utility
=========================================================================================

This module provides a function to reliably extract product identifiers from various
AliExpress URL formats or directly from product ID strings.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.utils.extract_product_id import extract_prod_ids

    # Example with a full URL
    product_id = extract_prod_ids("https://www.aliexpress.com/item/1234567890.html")
    print(f"Extracted ID: {product_id}")  # Output: Extracted ID: 1234567890

    # Example with a product ID string
    product_id = extract_prod_ids("9876543210")
    print(f"Extracted ID: {product_id}")  # Output: Extracted ID: 9876543210

    # Example with a list of URLs/IDs
    product_ids = extract_prod_ids([
        "https://www.aliexpress.com/item/11111.html",
        "22222",
        "invalid_url"
    ])
    print(f"Extracted IDs: {product_ids}")  # Output: Extracted IDs: ['11111', '22222']
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/aliexpress_com/utils/extract_product_id.py
"""


import re
from src.logger.logger import logger


def extract_prod_ids(urls: str | list[str]) -> str | list[str] | None:
    """ Extracts item IDs from a list of URLs or directly returns IDs if given.

    Args:
        urls (str | list[str]): A URL, a list of URLs, or product IDs.

    Returns:
        str | list[str] | None: A list of extracted item IDs, a single ID, or `None` if no valid ID is found.

    Examples:
        >>> extract_prod_ids("https://www.aliexpress_com.com/item/123456.html")
        '123456'

        >>> extract_prod_ids(["https://www.aliexpress_com.com/item/123456.html", "7891011.html"])
        ['123456', '7891011']

        >>> extract_prod_ids(["https://www.example.com/item/123456.html", "https://www.example.com/item/abcdef.html"])
        ['123456']

        >>> extract_prod_ids("7891011")
        '7891011'

        >>> extract_prod_ids("https://www.example.com/item/abcdef.html")
        None
    """
    # Regular expression to find product identifiers
    pattern = re.compile(r"(?:item/|/)?(\d+)\.html")

    def extract_id(url: str) -> str | None:
        """ Extracts a product ID from a given URL or validates a product ID.

        Args:
            url (str): The URL or product ID.

        Returns:
            str | None: The extracted product ID or the input itself if it's a valid ID, or `None` if no valid ID is found.

        Examples:
            >>> extract_id("https://www.aliexpress_com.com/item/123456.html")
            '123456'

            >>> extract_id("7891011")
            '7891011'

            >>> extract_id("https://www.example.com/item/abcdef.html")
            None
        """
        # Check if the input is a valid product ID
        if url.isdigit():
            return url

        # Otherwise, try to extract the ID from the URL
        match = pattern.search(url)
        if match:
            return match.group(1)
        return

    if isinstance(urls, list):
        extracted_ids = [extract_id(url) for url in urls if extract_id(url) is not None]
        return extracted_ids if extracted_ids else None
    else:
        return extract_id(urls)
