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
This code block defines a dictionary `scenario` that contains information about a specific product category, in this case, "Murano Glass". The dictionary includes details such as the Amazon search URL, desired product condition, PrestaShop category mapping, and a price rule. 

Execution Steps
-------------------------
1. **Define Scenario Dictionary**: The code initializes an empty dictionary named `scenario`.
2. **Add Category Information**: The code creates a nested dictionary within `scenario` representing the "Murano Glass" category. This nested dictionary includes:
    - `url`: The Amazon search URL for Murano Glass products.
    - `condition`: Specifies the desired product condition ("new" in this case).
    - `presta_categories`: Maps the Amazon category to relevant PrestaShop categories.
    - `price_rule`: Defines a specific price rule for products in this category.

Usage Example
-------------------------

```python
# Accessing the Murano Glass scenario data:
murano_glass_scenario = scenario["Murano Glass"]

# Retrieving the Amazon search URL:
murano_glass_url = murano_glass_scenario["url"]

# Checking the desired product condition:
condition = murano_glass_scenario["condition"]

# Getting the PrestaShop category mapping:
presta_categories = murano_glass_scenario["presta_categories"]

# Accessing the price rule:
price_rule = murano_glass_scenario["price_rule"]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".