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
The `Graber` class is responsible for extracting product data from the Etzmaleh website. It inherits from the base `Graber` class and provides methods for handling specific fields on the product page. 

The `Graber` class uses a decorator to perform pre-processing actions before sending a request to the web driver. 

Execution Steps
-------------------------
1. **Initialization**: The `__init__` method initializes the `Graber` instance. It sets the `supplier_prefix` to "etzmaleh" and calls the parent class's `__init__` method to initialize common properties.
2. **Decorator Application**: The `close_pop_up` decorator is applied to methods that need to handle pop-up windows. It attempts to close any pop-ups before executing the main logic of the method.
3. **Field Processing**: Methods within the `Graber` class are designed to extract specific fields from the product page.  These methods might include:
    - Extracting product title
    - Extracting product price
    - Extracting product images
    - Extracting product description
    - Handling variations (if applicable)
4. **Data Aggregation**: The extracted data is stored in a structured format, ready to be processed and saved.

Usage Example
-------------------------

```python
from src.suppliers.suppliers_list.etzmaleh.graber import Graber
from src.webdriver.driver import Driver

# Initialize the Driver
driver = Driver(Firefox)

# Initialize the Graber class
graber = Graber(driver=driver)

# Get the product data
product_data = graber.get_product_data(product_url="https://www.etzmaleh.com/product-page-url")

# Process and save the product data
# ... 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".