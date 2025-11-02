# Module: src.___beeryakov.suppliers.ksp

## Overview

This module is responsible for retrieving data from the KSP website, a popular Israeli online retailer. It utilizes Selenium for web scraping and the `executor` function from the `src.webdriver` module to interact with the KSP website. 

## Details

This module is used to extract information from the KSP website, including:

- **Worlds (categories):** Retrieves a dictionary of worlds (product categories) available on the KSP website.
- **Subcategories:** Retrieves a dictionary of subcategories within each world (category).
- **Brands:** Retrieves a dictionary of brands available on the KSP website.
- **Product details:** Retrieves detailed information about a specific product based on its URL.

## Table of Contents

- [Classes](#classes)
    - [KSP](#ksp)
- [Functions](#functions)
    - [get_worlds](#get_worlds)
    - [get_subs_from_world](#get_subs_from_world)
    - [get_all_brands_list](#get_all_brands_list)
    - [get_product](#get_product)

## Classes

### `KSP`

**Description:** This class is responsible for retrieving data from the KSP website. 

**Attributes:**

- `locators (dict)`: A dictionary containing locators for web elements on the KSP website.

**Methods:**

- `get_worlds():` Retrieves a dictionary of worlds (product categories).
- `get_subs_from_world():` Retrieves a dictionary of subcategories within each world.
- `get_all_brands_list():` Retrieves a dictionary of brands available on the KSP website.
- `get_product(url: str = 'https://ksp.co.il/web/item/227307') -> dict:` Retrieves detailed information about a specific product based on its URL.

## Functions

### `get_worlds`

**Purpose:** This function retrieves a dictionary of worlds (product categories) available on the KSP website.

**Parameters:** 

- None

**Returns:**

- `dict`: A dictionary of worlds (product categories).

**How the Function Works:**

1. It uses the `executor` function from the `src.webdriver` module to access the world elements on the KSP website.
2. It iterates over the world elements and adds them to a dictionary, where the key is the world's name and the value is a list of world data.
3. The function returns the resulting dictionary.

**Example:**

```python
worlds_dic = get_worlds()
print(worlds_dic)
```

### `get_subs_from_world`

**Purpose:** This function retrieves a dictionary of subcategories within a world (product category).

**Parameters:**

- None

**Returns:**

- `dict`: A dictionary of subcategories within a world.

**How the Function Works:**

1. It uses the `executor` function to access the subcategory elements on the KSP website.
2. It iterates over the subcategory elements and adds them to a dictionary, where the key is the subcategory's name and the value is a list of subcategory data.
3. The function returns the resulting dictionary.

**Example:**

```python
subs_dic = get_subs_from_world()
print(subs_dic)
```

### `get_all_brands_list`

**Purpose:** This function retrieves a list of all brands available on the KSP website.

**Parameters:**

- None

**Returns:**

- `dict`: A dictionary of brands, where the key is the brand's name and the value is its URL.

**How the Function Works:**

1. It uses the `executor` function to open the page with the full list of brands.
2. It retrieves the list of brand names and URLs from the page using specific locators.
3. The function returns a dictionary where the key is the brand's name and the value is its URL.

**Example:**

```python
brands_dict = get_all_brands_list()
print(brands_dict)
```

### `get_product`

**Purpose:** This function retrieves detailed information about a specific product based on its URL.

**Parameters:**

- `url: str = 'https://ksp.co.il/web/item/227307'` (optional): The URL of the product page.

**Returns:**

- `dict`: A dictionary containing the product's details.

**How the Function Works:**

1. It uses the `executor` function to navigate to the product page.
2. It retrieves data about the product using specific locators.
3. The function returns a dictionary containing the product's details.

**Example:**

```python
product_details = get_product(url='https://ksp.co.il/web/item/227307')
print(product_details)
```

**Inner Functions:**

- None

**How the Function Works:**

- The function utilizes the `executor` function from the `src.webdriver` module to interact with the KSP website.
- It uses locators defined in the `locators.json` file to target specific elements on the website.
- The function parses the retrieved data and returns it in a structured format. 

**Example:**

```python
# Example of using the KSP module
from src.___beeryakov.suppliers.ksp import KSP

# Create an instance of the KSP class
ksp = KSP()

# Retrieve a list of all brands
brands_dict = ksp.get_all_brands_list()

# Print the list of brands
print(brands_dict)

# Retrieve product details
product_details = ksp.get_product(url='https://ksp.co.il/web/item/227307')

# Print the product details
print(product_details)
```