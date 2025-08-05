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
This code snippet defines a dictionary named `scenario` containing information about different products. Each product is represented by a key-value pair, where the key is the product name and the value is another dictionary containing specific details about the product. 

Execution Steps
-------------------------
1. **Define the `scenario` dictionary**: The code initializes a dictionary named `scenario` to store information about different products.
2. **Define product details**: For each product (e.g., "Apple Watches", "Murano Glass"), a nested dictionary is created. 
    - This nested dictionary holds details like the product's URL, condition (e.g., "new"), the PrestaShop categories it belongs to, if it uses a checkbox, and a price rule. 
    - The `presta_categories` dictionary specifies the categories the product belongs to on the PrestaShop platform, using a `template` or a `default_category` structure.

Usage Example
------------------------

```python
# Access product details from the scenario dictionary
apple_watch_details = scenario["Apple Wathes"]

# Retrieve the URL for Apple Watches
apple_watch_url = apple_watch_details["url"]

# Check the active status of Murano Glass
murano_glass_active = scenario["Murano Glass"]["active"]

# Print the PrestaShop category for Murano Glass
murano_glass_category = scenario["Murano Glass"]["presta_categories"]["default_category"]["11209"]
print(murano_glass_category) 

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".