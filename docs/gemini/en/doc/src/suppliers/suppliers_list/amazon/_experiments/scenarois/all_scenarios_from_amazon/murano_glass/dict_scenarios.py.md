# Module: `src.suppliers.amazon._experiments.scenarois.all_scenarios_from_amazon.murano_glass.dict_scenarios`

## Overview

This module defines a dictionary containing scenario data for the `Murano Glass` category on Amazon. The scenario is used to collect and process product data from Amazon, and it includes information such as the search URL, condition, PrestaShop categories, and price rule.

## Details

The scenario dictionary is used to configure the data collection process for the `Murano Glass` category on Amazon. The dictionary contains the following keys:

- `url`: The search URL for the category on Amazon.
- `condition`: The condition of the products to be collected.
- `presta_categories`: A dictionary mapping PrestaShop categories to the corresponding category on Amazon.
- `price_rule`: A rule for determining the price of products.

## Scenario Dictionary Structure

```python
scenario: dict = {
    "Murano Glass": {
        "url": "https://www.amazon.com/s?k=Art+Deco+murano+glass&crid=24Q0ZZYVNOQMP&sprefix=art+deco+murano+glass%2Caps%2C230&ref=nb_sb_noss",
        "condition": "new",
        "presta_categories": {
            "default_category":{"11209":"MURANO GLASS"}
        },
        "price_rule": 1
    }
}
```

### `scenario` Dictionary

- `Murano Glass`: This key represents the scenario name.
    - `url`: The URL for the Amazon search page for the `Murano Glass` category.
    - `condition`: The condition of the products to be collected, in this case, "new."
    - `presta_categories`: A dictionary mapping PrestaShop categories to the corresponding category on Amazon. The `default_category` key indicates that all products should be assigned to the PrestaShop category with ID `11209`, which is named "MURANO GLASS."
    - `price_rule`: This value indicates the price rule to be applied when processing product data.

## Usage

The `scenario` dictionary is used by the `hypotez` project to configure the data collection and processing process for the `Murano Glass` category on Amazon. The data collected from Amazon is then used to create product listings in the PrestaShop e-commerce platform.

The `scenario` dictionary is loaded into the `hypotez` project and used to define the data collection parameters. This ensures that the project can collect and process the correct data for the `Murano Glass` category on Amazon.

## Summary

The `scenario` dictionary is a crucial component of the `hypotez` project, providing essential information for the data collection and processing of `Murano Glass` products from Amazon. It ensures that the correct data is collected and processed, and it plays a vital role in creating accurate and consistent product listings in PrestaShop.