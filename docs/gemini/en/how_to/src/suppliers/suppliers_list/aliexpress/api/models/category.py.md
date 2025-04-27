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
This code block defines two classes: `Category` and `ChildCategory`, representing categories and child categories in AliExpress. 

Execution Steps
-------------------------
1. The `Category` class defines two attributes: `category_id` (an integer) and `category_name` (a string). 
2. The `ChildCategory` class inherits from the `Category` class and adds an additional attribute: `parent_category_id` (an integer) representing the ID of the parent category.

Usage Example
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.api.models.category import Category, ChildCategory

# Create a Category object
main_category = Category(category_id=123, category_name="Electronics")

# Create a ChildCategory object
child_category = ChildCategory(category_id=456, category_name="Smartphones", parent_category_id=123)

print(f"Main Category: {main_category.category_name} (ID: {main_category.category_id})")
print(f"Child Category: {child_category.category_name} (ID: {child_category.category_id}, Parent ID: {child_category.parent_category_id})")

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".