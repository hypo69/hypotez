## \file /src/suppliers/suppliers_list/aliexpress_com/api/models/category.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.models.category
    :platform: Windows, Unix
    :synopsis: Data models for AliExpress categories.

This module defines the `Category` and `ChildCategory` classes,
which represent the structure of category information returned by the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.models import Category, ChildCategory

    # Example of creating a Category object
    # category = Category()
    # category.category_id = 123
    # category.category_name = "Electronics"

    # Example of creating a ChildCategory object
    # child_category = ChildCategory()
    # child_category.category_id = 456
    # child_category.category_name = "Smartphones"
    # child_category.parent_category_id = 123
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/models/category.py
"""
class Category:
    category_id: int
    category_name: str


class ChildCategory(Category):
    parent_category_id: int
