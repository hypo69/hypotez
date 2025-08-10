## \file /src/suppliers/suppliers_list/aliexpress_com/api/helpers/categories.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.helpers.categories
    :platform: Windows, Unix
    :synopsis: Helper functions for filtering AliExpress API categories.

This module provides utility functions for filtering categories and subcategories
returned by the AliExpress API, allowing for easier navigation and processing of category data.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.helpers.categories import filter_parent_categories
    from src.suppliers.suppliers_list.aliexpress_com.api import models

    # Example categories (replace with actual data from API)
    # all_categories = [
    #     models.Category(category_id=1, category_name="Electronics"),
    #     models.ChildCategory(category_id=2, category_name="Phones", parent_category_id=1)
    # ]
    # parent_cats = filter_parent_categories(all_categories)
    # print(parent_cats)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/helpers/categories.py
"""

"""  functions for filtering categories and subcategories of Aliexpress API"""
from typing import List, Union
from .. import models
#from src.suppliers.suppliers_list.aliexpress_com.api.api import models

def filter_parent_categories(categories: List[models.Category | models.ChildCategory]) -> List[models.Category]:
    """
    Filters and returns a list of categories that do not have a parent category.

    @param categories: List of category or child category objects.
    @return: List of category objects without a parent category.
    """
    filtered_categories = []

    if isinstance(categories, (str, int, float)):
        categories = [categories]  # Convert to list if a single non-category value is passed.

    for category in categories:
        if not hasattr(category, 'parent_category_id'):
            filtered_categories.append(category)

    return filtered_categories

def filter_child_categories(categories: List[models.Category | models.ChildCategory],
                            parent_category_id: int) -> List[models.ChildCategory]:
    """
    Filters and returns a list of child categories that belong to the specified parent category.

    @param categories: List of category or child category objects.
    @param parent_category_id: The ID of the parent category to filter child categories by.
    @return: List of child category objects with the specified parent category ID.
    """
    filtered_categories = []

    if isinstance(categories, (str, int, float)):
        categories = [categories]  # Convert to list if a single non-category value is passed.

    for category in categories:
        if hasattr(category, 'parent_category_id') and category.parent_category_id == parent_category_id:
            filtered_categories.append(category)

    return filtered_categories
