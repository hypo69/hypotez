# Dictionary Scenarios for Amazon

## Overview

This module defines a dictionary (`scenario`) containing pre-defined scenarios for product scraping from Amazon. Each scenario represents a product category with its specific details, including:

- **URL**: The Amazon search URL for the product category.
- **Active**: Whether the scenario is currently active for scraping.
- **Condition**: The desired product condition (e.g., "new", "used").
- **Presta_categories**: A dictionary mapping PrestaShop categories to the Amazon product category.
- **Checkbox**: Whether the scenario uses checkboxes in the product search.
- **Price_rule**: A rule for filtering products based on their price.

## Details

This module is used in conjunction with other modules within the `hypotez` project to automate the process of extracting product information from Amazon. 

The `scenario` dictionary serves as a configuration for defining different product categories and their corresponding scraping parameters. 

## Dictionary Structure

The `scenario` dictionary is structured as follows:

```python
scenario: dict = {
    "Product Category Name": {
        "url": "https://www.amazon.com/search_url",
        "active": True,
        "condition": "new",
        "presta_categories": {
            "category_mapping": "Category Name"
        },
        "checkbox": False,
        "price_rule": 1
    },
    "Another Product Category": {
        "url": "https://www.amazon.com/another_search_url",
        "condition": "new",
        "presta_categories": {
            "category_mapping": "Another Category Name"
        },
        "price_rule": 1
    }
}
```

**Explanation:**

- **`Product Category Name`:** The key of each dictionary entry represents the name of a specific product category.
- **`url`**: The Amazon search URL for the category.
- **`active`**:  A boolean value indicating whether the scenario is currently active for scraping.
- **`condition`**: The desired condition of the products to be scraped (e.g., "new", "used").
- **`presta_categories`**: A dictionary mapping PrestaShop categories to the Amazon product category.
- **`checkbox`**: A boolean value indicating whether the scenario uses checkboxes in the product search (e.g., for specific features or attributes).
- **`price_rule`**: A rule for filtering products based on their price.

## Example

The following example shows a scenario for scraping "Apple Watches" from Amazon:

```python
scenario: dict = {
    "Apple Wathes": {
        "url": "https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A2811119011%2Cn%3A2407755011%2Cn%3A7939902011%2Cp_n_is_free_shipping%3A10236242011%2Cp_89%3AApple&dc&ds=v1%3AyDxGiVC9lCk%2BzGvhkah6ZCjaellz7FcqKtRIfFA3o2A&qid=1671818889&rnid=2407755011&ref=sr_nr_n_2",
        "active": True,
        "condition": "new",
        "presta_categories": {
            "template": {"apple": "WATCHES"}
        },
        "checkbox": False,
        "price_rule": 1
    }
}
```

This scenario defines the Amazon search URL for Apple Watches, sets the condition to "new", maps the PrestaShop category "WATCHES" to the Amazon product category "apple", and specifies that no checkboxes are used in the search. The `price_rule` value of 1 likely indicates a specific price filtering rule.

## Usage

The `scenario` dictionary is used by other modules in the `hypotez` project, such as scraping modules, to define the parameters for retrieving product information from Amazon. The specific modules would access the corresponding scenario based on the product category and use its parameters to configure their scraping operations.

## Importance

This module provides a centralized mechanism for defining and managing product scraping scenarios for Amazon. It simplifies the process of configuring different product categories and their associated scraping parameters, ensuring consistency and maintainability throughout the scraping process.