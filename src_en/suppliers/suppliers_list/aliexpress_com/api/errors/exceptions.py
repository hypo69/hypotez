## \file /src/suppliers/suppliers_list/aliexpress_com/api/errors/exceptions.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.errors.exceptions
    :platform: Windows, Unix
    :synopsis: Custom exceptions for AliExpress API.

This module defines custom exception classes for handling errors specific to the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.errors.exceptions import ProductsNotFoudException

    # Example of raising a custom exception
    # raise ProductsNotFoudException("No products found for the given criteria.")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/errors/exceptions.py
"""
"""Custom exceptions module"""


class AliexpressException(Exception):
    """Common base class for all AliExpress API exceptions."""
    def __init__(self, reason: str):
        super().__init__()
        self.reason = reason

    def __str__(self) -> str:
        return '%s' % self.reason


class InvalidArgumentException(AliexpressException):
    """Raised when arguments are not correct."""
    pass


class ProductIdNotFoundException(AliexpressException):
    """Raised if the product ID is not found."""
    pass

class ApiRequestException(AliexpressException):
    """Raised if the request to AliExpress API fails"""
    pass

class ApiRequestResponseException(AliexpressException):
    """Raised if the request response is not valid"""
    pass

class ProductsNotFoudException(AliexpressException):
    """Raised if no products are found"""
    pass

class CategoriesNotFoudException(AliexpressException):
    """Raised if no categories are found"""
    pass

class InvalidTrackingIdException(AliexpressException):
    """Raised if the tracking ID is not present or invalid"""
    pass
