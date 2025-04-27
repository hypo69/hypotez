**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
These functions are used to filter categories and child categories from the AliExpress API. The `filter_parent_categories` function returns a list of categories that have no parent categories, while the `filter_child_categories` function returns a list of child categories that belong to a specific parent category. 

Execution Steps
-------------------------
1. **`filter_parent_categories`:**
    - The function takes a list of category or child category objects as input.
    - It iterates through the list and checks if each object has a `parent_category_id` attribute.
    - If the object does not have a `parent_category_id` attribute, it is added to the filtered list.
    - The function returns the filtered list of category objects without a parent category.

2. **`filter_child_categories`:**
    - The function takes a list of category or child category objects and a `parent_category_id` as input.
    - It iterates through the list and checks if each object has a `parent_category_id` attribute.
    - If the object has a `parent_category_id` attribute and it matches the specified `parent_category_id`, the object is added to the filtered list.
    - The function returns the filtered list of child category objects with the specified parent category ID.


Usage Example
-------------------------

```python
from src.suppliers.aliexpress.api.helpers.categories import filter_parent_categories, filter_child_categories
from src.suppliers.aliexpress.api import models

# Example category objects
categories = [
    models.Category(category_id=1, name="Electronics"),
    models.ChildCategory(category_id=2, name="Phones", parent_category_id=1),
    models.Category(category_id=3, name="Clothing"),
    models.ChildCategory(category_id=4, name="Shirts", parent_category_id=3),
]

# Get parent categories
parent_categories = filter_parent_categories(categories)
print(parent_categories)  # Output: [Category(category_id=1, name='Electronics'), Category(category_id=3, name='Clothing')]

# Get child categories of Electronics
child_categories_electronics = filter_child_categories(categories, parent_category_id=1)
print(child_categories_electronics)  # Output: [ChildCategory(category_id=2, name='Phones', parent_category_id=1)]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".