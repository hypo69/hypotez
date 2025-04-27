# Module: `src.suppliers.aliexpress.api.helpers.categories`

## Overview

This module provides functions for filtering categories and subcategories from the AliExpress API.

## Details

This module is part of the `hypotez` project, specifically within the `aliexpress` supplier list section. It defines two functions:

- **`filter_parent_categories`**: Filters and returns a list of categories that do not have a parent category.
- **`filter_child_categories`**: Filters and returns a list of child categories that belong to a specific parent category.

## Table of Contents

- [Classes](#classes)
- [Functions](#functions)
    - [`filter_parent_categories`](#filter_parent_categories)
    - [`filter_child_categories`](#filter_child_categories)

## Functions

### `filter_parent_categories`

**Purpose**: This function filters a list of categories or child categories and returns only those that do not have a parent category.

**Parameters**:

- `categories` (`List[models.Category | models.ChildCategory]`): A list of category or child category objects.

**Returns**:

- `List[models.Category]`: A list of category objects without a parent category.

**Raises Exceptions**:

- None.

**How the Function Works**:

1. The function first checks if the `categories` argument is a list. If it's a single value (e.g., a string, integer, or float), it converts it to a list for processing.
2. It then iterates through each `category` in the list.
3. For each category, it checks if the `category` object has an attribute named `parent_category_id`. 
4. If it doesn't have the `parent_category_id` attribute, it means the category is a parent category and it's added to the `filtered_categories` list.
5. Finally, the function returns the `filtered_categories` list.

**Examples**:

```python
from src.suppliers.aliexpress.api.helpers.categories import filter_parent_categories
from src.suppliers.aliexpress.api.models import Category, ChildCategory

# Example 1: Filtering a list of categories
categories = [
    Category(category_id=1, name='Electronics', parent_category_id=None),
    ChildCategory(category_id=2, name='Phones', parent_category_id=1),
    Category(category_id=3, name='Fashion', parent_category_id=None),
]
parent_categories = filter_parent_categories(categories)
print(parent_categories)  # Output: [Category(category_id=1, name='Electronics', parent_category_id=None), Category(category_id=3, name='Fashion', parent_category_id=None)]

# Example 2: Filtering a single category object
category = Category(category_id=1, name='Electronics', parent_category_id=None)
parent_categories = filter_parent_categories(category)
print(parent_categories)  # Output: [Category(category_id=1, name='Electronics', parent_category_id=None)]
```

### `filter_child_categories`

**Purpose**: This function filters a list of categories or child categories and returns only those that belong to a specified parent category.

**Parameters**:

- `categories` (`List[models.Category | models.ChildCategory]`): A list of category or child category objects.
- `parent_category_id` (`int`): The ID of the parent category to filter child categories by.

**Returns**:

- `List[models.ChildCategory]`: A list of child category objects with the specified parent category ID.

**Raises Exceptions**:

- None.

**How the Function Works**:

1. Similar to the `filter_parent_categories` function, it first checks if `categories` is a list and converts it if necessary.
2. It then iterates through each `category` in the list.
3. For each category, it checks if the `category` object has a `parent_category_id` attribute and if it's equal to the provided `parent_category_id`.
4. If both conditions are true, it means the category is a child category belonging to the specified parent category, and it's added to the `filtered_categories` list.
5. Finally, the function returns the `filtered_categories` list.

**Examples**:

```python
from src.suppliers.aliexpress.api.helpers.categories import filter_child_categories
from src.suppliers.aliexpress.api.models import Category, ChildCategory

# Example 1: Filtering child categories of a parent category
categories = [
    Category(category_id=1, name='Electronics', parent_category_id=None),
    ChildCategory(category_id=2, name='Phones', parent_category_id=1),
    ChildCategory(category_id=4, name='Laptops', parent_category_id=1),
    Category(category_id=3, name='Fashion', parent_category_id=None),
]
child_categories = filter_child_categories(categories, parent_category_id=1)
print(child_categories)  # Output: [ChildCategory(category_id=2, name='Phones', parent_category_id=1), ChildCategory(category_id=4, name='Laptops', parent_category_id=1)]

# Example 2: Filtering a single child category object
child_category = ChildCategory(category_id=2, name='Phones', parent_category_id=1)
child_categories = filter_child_categories(child_category, parent_category_id=1)
print(child_categories)  # Output: [ChildCategory(category_id=2, name='Phones', parent_category_id=1)]
```