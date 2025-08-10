## \file /src/suppliers/suppliers_list/aliexpress_com/utils/ensure_https.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.utils.ensure_https
    :platform: Windows, Unix
    :synopsis: Ensures that the provided URL string(s) contain the https:// prefix.

AliExpress HTTPS URL Utility
=========================================================================================

This module ensures that URL strings are properly formatted with the HTTPS protocol.
It can convert product IDs into full AliExpress product URLs and handle lists of URLs.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.utils.ensure_https import ensure_https

    # Example of ensuring a single product ID is an HTTPS URL
    product_id = "example_product_id"
    url_with_https = ensure_https(product_id)
    print(url_with_https)
    # Expected Output: https://www.aliexpress_com.com/item/example_product_id.html

    # Example of ensuring a list of URLs/product IDs are HTTPS URLs
    urls = ["example_product_id1", "https://www.aliexpress_com.com/item/example_product_id2.html"]
    urls_with_https = ensure_https(urls)
    print(urls_with_https)
    # Expected Output: ['https://www.aliexpress_com.com/item/example_product_id1.html', 'https://www.aliexpress_com.com/item/example_product_id2.html']
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/aliexpress_com/utils/ensure_https.py
"""


from src.logger.logger import logger
from .extract_product_id import extract_prod_ids

def ensure_https(prod_ids: str | list[str]) -> str | list[str]:
    """ Ensures that the provided URL string(s) contain the https:// prefix.
    If the input is a product ID, it constructs a full URL with https:// prefix.

    Args:
        prod_ids (str | list[str]): A URL string or a list of URL strings to check and modify if necessary.

    Returns:
        str | list[str]: The URL string or list of URL strings with the https:// prefix.

    Raises:
        ValueError: If `prod_ids` is an instance of `WindowsPath`.

    Examples:
        >>> ensure_https("example_product_id")
        'https://www.aliexpress_com.com/item/example_product_id.html'

        >>> ensure_https(["example_product_id1", "https://www.aliexpress_com.com/item/example_product_id2.html"])
        ['https://www.aliexpress_com.com/item/example_product_id1.html', 'https://www.aliexpress_com.com/item/example_product_id2.html']

        >>> ensure_https("https://www.example.com/item/example_product_id")
        'https://www.example.com/item/example_product_id'
    """
    def ensure_https_single(prod_id: str) -> str:
        """ Ensures a single URL or product ID string has the https:// prefix.

        Args:
            prod_id (str): The URL or product ID string.

        Returns:
            str: The URL string with the https:// prefix.

        Raises:
            ValueError: If `prod_id` is an instance of `WindowsPath`.

        Examples:
            >>> ensure_https_single("example_product_id")
            'https://www.aliexpress_com.com/item/example_product_id.html'

            >>> ensure_https_single("https://www.example.com/item/example_product_id")
            'https://www.example.com/item/example_product_id'
        """
        ...
        _prod_id = extract_prod_ids(prod_id)
        if _prod_id:
            return f"https://www.aliexpress_com.com/item/{_prod_id}.html"
        else:
            logger.error(f"Invalid product ID or URL: {prod_id=}", exc_info=False)
            return prod_id

    if isinstance(prod_ids, list):
        return [ensure_https_single(prod_id) for prod_id in prod_ids]
    else:
        return ensure_https_single(prod_ids)
