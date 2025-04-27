# Module: `src.suppliers.aliexpress.api.models.category`

## Overview

This module defines the `Category` and `ChildCategory` classes for representing product categories in the AliExpress API. These classes provide structured data models for storing and accessing category information retrieved from the AliExpress API.

## Details

This module is part of the `hypotez` project and plays a crucial role in retrieving and managing product category data from the AliExpress API. The `Category` and `ChildCategory` classes serve as data models for storing and manipulating category information.

## Classes

### `Category`

**Description**: This class represents a basic category structure. 

**Attributes**:

- `category_id` (int): The unique identifier for the category.
- `category_name` (str): The name of the category.

### `ChildCategory`

**Description**: This class represents a child category, inheriting from the `Category` class and adding a parent category identifier.

**Inherits**: `Category`

**Attributes**:

- `parent_category_id` (int): The unique identifier of the parent category.

## Example:

```python
from src.suppliers.aliexpress.api.models.category import Category, ChildCategory

# Creating a category object
category = Category(category_id=12345, category_name="Electronics")

# Creating a child category object
child_category = ChildCategory(category_id=67890, category_name="Smartphones", parent_category_id=12345)

# Accessing category attributes
print(f"Category ID: {category.category_id}")
print(f"Category Name: {category.category_name}")

print(f"Child Category ID: {child_category.category_id}")
print(f"Child Category Name: {child_category.category_name}")
print(f"Parent Category ID: {child_category.parent_category_id}")
```

This example demonstrates how to create instances of the `Category` and `ChildCategory` classes, access their attributes, and interact with category data.