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
This code defines a dictionary called `scenarios` that contains information about various product categories from Kualastyle.com.  Each category entry in the dictionary includes:
* `url`: The URL of the product category on the website.
* `active`: A boolean indicating whether the category is active (True) or inactive (False).
* `condition`: A string defining the condition for the category (e.g., "new" for new products).
* `presta_categories`:  A dictionary mapping PrestaShop category IDs to the corresponding Kualastyle category name.
* `checkbox`: A boolean indicating whether the category has a checkbox (True) or not (False).
* `price_rule`: An integer representing a price rule associated with the category.

Execution Steps
-------------------------
1. The code creates a dictionary called `scenarios`.
2. For each category, it adds an entry to the `scenarios` dictionary with the following keys:
    * `url`: The URL of the category on Kualastyle.com.
    * `active`: A boolean indicating whether the category is active.
    * `condition`: A string defining the condition of the category (e.g., "new" for new products).
    * `presta_categories`: A dictionary mapping PrestaShop category IDs to the corresponding Kualastyle category name.
    * `checkbox`: A boolean indicating whether the category has a checkbox.
    * `price_rule`: An integer representing a price rule associated with the category.

Usage Example
-------------------------

```python
    from src.suppliers.kualastyle._experiments.dict_scenarios import scenarios

    print(scenarios["Sofas and Sectionals"]["url"])
    # Output: https://kualastyle.com/collections/%D7%A1%D7%A4%D7%95%D7%AA-%D7%9E%D7%A2%D7%95%D7%A6%D7%91%D7%95%D7%AA

    print(scenarios["Bookcases and Display Cabinets"]["active"])
    # Output: True

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".