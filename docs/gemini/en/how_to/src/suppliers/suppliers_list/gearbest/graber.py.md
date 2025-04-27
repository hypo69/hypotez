**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `Graber` Class
=========================================================================================

Description
-------------------------
The `Graber` class is designed to extract product data from the `bangood.com` website. It inherits from the base class `src.suppliers.graber.Graber`, providing methods for handling different product fields on the page.

Execution Steps
-------------------------
1. **Initialization**: The `Graber` class is initialized with optional arguments for the `driver` (a `Driver` object) and `lang_index` (an integer representing the language index).
2. **Supplier Prefix**: The `supplier_prefix` attribute is set to `"etzmaleh"`.
3. **Global Configuration**: The `Config.locator_for_decorator` attribute is set to `None`. This attribute is used to specify a locator that will be executed within the `@close_pop_up` decorator. If a value is provided, the decorator will execute the locator before executing the main function.
4. **Field Handling**: The `Graber` class provides methods for handling various product fields on the page. These methods can be overridden for custom field processing.

Usage Example
-------------------------

```python
from src.suppliers.suppliers_list.gearbest.graber import Graber
from src.webdriver.driver import Driver

# Create a Driver object
driver = Driver(Chrome)  # Or Firefox, Playwright, etc.

# Create a Graber object
graber = Graber(driver=driver)

# Example: Extract the product title
product_title = graber.get_product_title()

# Example: Extract the product price
product_price = graber.get_product_price()

# Example: Extract the product description
product_description = graber.get_product_description()

# ... continue extracting other fields as needed
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".