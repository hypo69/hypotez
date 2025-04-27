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
This code defines a dictionary named `scenario` that contains information for different product scenarios on Amazon. Each scenario is represented by a key (product name), and its corresponding value is a dictionary containing various details like URL, condition, PrestaShop category mapping, price rule, etc. 

Execution Steps
-------------------------
1. The code creates a dictionary named `scenario`.
2. It defines the `Apple Wathes` scenario:
    - Sets the `url` to an Amazon search page for Apple Watches with specific filters applied.
    - Sets `active` to `True`, indicating this scenario is active.
    - Sets `condition` to `new`, indicating the scenario is focused on new Apple Watches.
    - Defines `presta_categories` mapping, specifying the category for Apple Watches on PrestaShop.
    - Sets `checkbox` to `False`.
    - Sets `price_rule` to `1`, indicating a specific price rule is applied to this scenario.
3. The code defines the `Murano Glass` scenario:
    - Sets the `url` to an Amazon search page for "Art Deco Murano Glass."
    - Sets `condition` to `new`.
    - Defines `presta_categories` mapping, specifying the category for Murano Glass on PrestaShop.
    - Sets `price_rule` to `1`.

Usage Example
-------------------------

```python
    from src.suppliers.amazon._experiments.dict_scenarios import scenario

    print(scenario["Apple Wathes"]["url"])
    # Output: "https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A2811119011%2Cn%3A2407755011%2Cn%3A7939902011%2Cp_n_is_free_shipping%3A10236242011%2Cp_89%3AApple&dc&ds=v1%3AyDxGiVC9lCk%2BzGvhkah6ZCjaellz7FcqKtRIfFA3o2A&qid=1671818889&rnid=2407755011&ref=sr_nr_n_2"
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".