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
This code defines a dictionary called `scenario` that contains a set of product-specific configurations for an Amazon experiment. 

Execution Steps
-------------------------
1. The code defines a dictionary named `scenario`.
2. Within the dictionary, it includes a key-value pair for a specific product, "Murano Glass".
3. For each product, it defines key-value pairs:
    - `url`: The URL for the product on Amazon.
    - `condition`: The desired condition for the product (e.g., "new").
    - `presta_categories`: A dictionary mapping default PrestaShop categories to the specific category for the product.
    - `price_rule`: An integer value representing the pricing rule for the product.

Usage Example
-------------------------

```python
    from src.suppliers.amazon._experiments.scenarois.dict_scenarios import scenario

    # Accessing the URL for "Murano Glass" product
    product_url = scenario["Murano Glass"]["url"]

    # Accessing the PrestaShop category for "Murano Glass"
    presta_category = scenario["Murano Glass"]["presta_categories"]["default_category"]["11209"] 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".