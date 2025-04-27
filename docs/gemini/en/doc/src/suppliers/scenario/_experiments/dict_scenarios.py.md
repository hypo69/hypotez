# Module: src.scenario._experiments

## Overview

This module defines a dictionary (`scenario`) containing information about different product categories. Each category entry includes details about the product, its URL, active status, condition, PrestaShop category mappings, checkbox status, and a price rule. 

## Details

This module is likely used in a scenario-driven system, where different product categories are defined and managed. The `scenario` dictionary likely provides information for different scenarios or use cases related to these product categories. For example, these scenarios could involve scraping, data processing, or testing within an e-commerce platform. 

## Scenario Dictionary

The `scenario` dictionary contains information about two product categories:

### `Apple Wathes`

* **url**: "https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A2811119011%2Cn%3A2407755011%2Cn%3A7939902011%2Cp_n_is_free_shipping%3A10236242011%2Cp_89%3AApple&dc&ds=v1%3AyDxGiVC9lCk%2BzGvhkah6ZCjaellz7FcqKtRIfFA3o2A&qid=1671818889&rnid=2407755011&ref=sr_nr_n_2" - The URL of the product category on Amazon.com.
* **active**: True - Indicates that this category is currently active and should be considered in relevant scenarios.
* **condition**: "new" - Specifies the condition of the product being considered within this category.
* **presta_categories**: {"template": {"apple": "WATCHES"}} - Defines a mapping between this category and PrestaShop categories. 
* **checkbox**: False - Indicates that this category does not use a checkbox in its scenario.
* **price_rule**: 1 - Specifies a price rule for this category.

### `Murano Glass`

* **url**: "https://www.amazon.com/s?k=Art+Deco+murano+glass&crid=24Q0ZZYVNOQMP&sprefix=art+deco+murano+glass%2Caps%2C230&ref=nb_sb_noss" - The URL of the product category on Amazon.com.
* **condition**: "new" - Specifies the condition of the product being considered within this category.
* **presta_categories**: {"default_category":{"11209":"MURANO GLASS"}} - Defines a mapping between this category and PrestaShop categories. 
* **price_rule**: 1 - Specifies a price rule for this category.

## How the Module Works

This module provides a central location for storing and managing product category information. The `scenario` dictionary likely serves as a configuration source for various processes or tasks related to these categories. The information within the dictionary can be used for tasks such as:

* Scraping product data from specific Amazon URLs.
* Applying price rules and filtering based on conditions.
* Mapping product categories to PrestaShop for catalog management.
* Implementing different scenarios based on category-specific settings.

## Examples

**Scenario Example**

Imagine a scenario where you are scraping product data from Amazon and storing it in a PrestaShop catalog. This module can be used to define the categories of interest, their URLs, and how they map to PrestaShop. 

**Code Example**

```python
# Load the scenario dictionary
from src.scenario._experiments import scenario

# Access a specific category
apple_watches_data = scenario["Apple Wathes"]

# Use the category data for scraping
# ...
```

This code snippet demonstrates how to access information about the `Apple Wathes` category from the `scenario` dictionary. You can then use this information to dynamically configure and execute scraping or other tasks related to this category.