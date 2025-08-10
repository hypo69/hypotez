## \file /src/suppliers/suppliers_list/aliexpress_com/api/helpers/arguments.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.helpers.arguments
    :platform: Windows, Unix
    :synopsis: Helper functions for processing arguments for AliExpress API requests.

This module provides utility functions for processing arguments used in AliExpress API requests,
such as converting lists to strings and extracting product IDs from various inputs.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.helpers.arguments import get_list_as_string, get_product_ids

    # Example of converting a list to a string
    # my_list = ["field1", "field2"]
    # fields_string = get_list_as_string(my_list)
    # print(fields_string) # Output: field1,field2

    # Example of getting product IDs
    # product_inputs = ["https://www.aliexpress.com/item/123.html", "456"]
    # ids = get_product_ids(product_inputs)
    # print(ids) # Output: ['123', '456']
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/helpers/arguments.py
"""

from ..tools.get_product_id import get_product_id
from ..errors.exceptions import InvalidArgumentException


def get_list_as_string(value):
    if value is None:
        return

    if isinstance(value, str):
        return value

    elif isinstance(value, list):
        return ','.join(value)

    else:
        raise InvalidArgumentException('Argument should be a list or string: ' + str(value))


def get_product_ids(values):
    if isinstance(values, str):
        values = values.split(',')

    elif not isinstance(values, list):
        raise InvalidArgumentException('Argument product_ids should be a list or string')

    product_ids = []
    for value in values:
        product_ids.append(get_product_id(value))

    return product_ids
