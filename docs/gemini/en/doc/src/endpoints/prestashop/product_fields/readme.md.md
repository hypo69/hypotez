# PrestaShop Product Fields Module

## Overview

The `ProductFields` module and its corresponding `ProductFields` class play a crucial role in transferring product data from a supplier to PrestaShop. It serves as a **structured data container** that:

1.  **Represents a product:** Defines all necessary product fields aligned with the PrestaShop data structure (tables `ps_product`, `ps_product_lang`, and `associations`).
2.  **Stores collected data:** Accepts and stores information gathered by the `Graber` class from the supplier's product page.
3.  **Provides default values:** Loads default values for many fields from the `product_fields_default_values.json` file, simplifying the creation of new products.
4.  **Supports multilingualism:** Facilitates managing field values (such as name, description) for different languages supported in PrestaShop.
5.  **Manages associations:** Offers methods for adding associations between products and categories, images, features, combinations, and more.
6.  **Formats data for the API:** Transforms collected and processed data into a dictionary (`to_dict()`), fully compatible with the PrestaShop Web Service API format for creating or updating products.

Essentially, `ProductFields` is an **intermediate product representation** tailored to the requirements of the PrestaShop API. It is populated with data from the supplier and subsequently passed to the `PrestaProduct` module for sending to the store.

## Table of Contents

- [Key Features](#key-features)
- [Initialization and Default Values](#initialization-and-default-values)
- [Accessing Fields](#accessing-fields)
- [Managing Associations](#managing-associations)
- [Conversion to API Dictionary (`to_dict()`)](#conversion-to-api-dictionary-to_dict)

## Key Features

*   **Full field set:** The class contains properties (property) for accessing all product fields listed in `fields_list.txt`, including fields from the `ps_product` and `ps_product_lang` tables.
*   **Default initialization:** When creating a class instance, default values are automatically loaded from `product_fields_default_values.json` using the `_payload()` method. This ensures that all necessary fields have some value.
*   **Convenient field access:** Accessing field values is done through standard Python properties (getters and setters), for example, `product.price = 100.0` or `name = product.name`. Setters often include data normalization (e.g., `normalize_float`, `normalize_string`).
*   **Handling multilingual fields:**
    *   Language-dependent fields (e.g., `name`, `description`, `meta_title`) use the internal `_set_multilang_value` method.
    *   This method allows setting a value for a specific language (specified during `ProductFields(id_lang=...)` initialization or passed to the setter).
    *   Data is stored internally so that the `to_dict()` method can format it correctly for the PrestaShop API (as a list of dictionaries `{'language': [{'id': language_id, 'value': value}]}`).
*   **Managing associations:**
    *   Product associations (with categories, images, features, tags, combinations, etc.) are stored in the nested structure `self.presta_fields.associations`.
    *   Convenient methods are provided for adding associations, such as:
        *   `additional_category_append(category_id)`
        *   `product_image_append(image_id)`
        *   `product_features_append(feature_id, feature_value_id)`
        *   `product_tag_append(tag_id)`
        *   and others.
    *   There are also methods for clearing associations (`..._clear()`).
*   **Conversion to API format (`to_dict()`):**
    *   The most important method for interacting with the PrestaShop API.
    *   It converts all the data of the `ProductFields` instance into a Python dictionary.
    *   **Filters empty values:** Keys whose values are `None` or an empty string are typically excluded from the resulting dictionary (depends on the specific implementation for each field).
    *   **Converts all values to strings:** The PrestaShop API (especially when working with XML) expects string values for all fields.
    *   **Formats multilingual fields:** Transforms the internal representation into the required API format of a list of dictionaries.
    *   **Formats associations:** Structures the association data according to the API requirements.
    *   The resulting dictionary is ready to be passed to the `create` or `edit` methods of the `PrestaShop` class (or `PrestaProduct`).

## Initialization and Default Values

When creating a `ProductFields` object, the following occurs:

1.  `__init__` accepts an optional `id_lang` (defaults to `1` - English in the example), which will be used for multilingual fields if the language is not explicitly specified.
2.  `__post_init__` calls `_payload()`.
3.  `_payload()`:
    *   Reads the list of all possible field names from the `src/endpoints/prestashop/product_fields/fields_list.txt` file.
    *   Creates an internal `self.presta_fields` object (of type `SimpleNamespace`) and initializes all fields from the list with the value `None`.
    *   Reads the `src/endpoints/prestashop/product_fields/product_fields_default_values.json` file.
    *   Sets default values for fields specified in the JSON file to the `self.presta_fields` object.

```python
# Example of object creation
# Default language with ID 1 is used
product_fields = ProductFields()

# Using language with ID 2 (e.g., Hebrew)
product_fields_he = ProductFields(id_lang=2)

# Accessing a field with a default value
print(product_fields.active) # Will output the value from product_fields_default_values.json (likely 1)
```

## Accessing Fields

Fields are accessed through properties.

```python
pf = ProductFields(id_lang=3) # Russian language

# Setting values
pf.id_supplier = 15
pf.reference = "ART-123"
pf.price = 99.90
pf.name = "Пример товара" # Set name for language id_lang=3
pf.description = "<p>Это описание товара.</p>" # Set description for language id_lang=3

# You can set a value for another language by passing it to the setter
# (Although the current implementation of setters does not accept id_lang,
# it would be more correct to modify _set_multilang_value and setters for this)
# Example of a hypothetical call (requires setter modifications):
# pf.set_name("Example Product", id_lang=1)

# Getting values
supplier_id = pf.id_supplier
product_name = pf.name # Will return the structure for a multilingual field

print(f"Артикул: {pf.reference}")
print(f"Цена: {pf.price}")
```

## Managing Associations

Associations are added through special methods.

```python
pf = ProductFields()

# Adding categories
pf.id_category_default = 5 # Mandatory to set the main category
pf.additional_category_append(5) # Add the main category to the list of associations
pf.additional_category_append(10)
pf.additional_category_append(12)

# Adding features (Feature)
# Assume the ID of the "Color" feature is 2, the ID of the "Red" value is 8
pf.product_features_append(feature_id=2, feature_value_id=8)
# Assume the ID of the "Material" feature is 3, the ID of the "Cotton" value is 15
pf.product_features_append(feature_id=3, feature_value_id=15)

# Adding a tag
# Assume the ID of the "New" tag is 1
pf.product_tag_append(tag_id=1)

# Getting the list of added categories (for verification)
print(pf.additional_categories)
# Output: [{'id': '5'}, {'id': '10'}, {'id': '12'}]

# Getting the list of features
print(pf.product_product_features)
# Output: [{'id': '2', 'id_feature_value': '8'}, {'id': '3', 'id_feature_value': '15'}]
```

## Conversion to API Dictionary (`to_dict()`)

After all necessary fields are populated, the object is converted into a dictionary.

```python
pf = ProductFields(id_lang=1)
pf.id_supplier = 15
pf.reference = "SKU-001"
pf.name = "My Product"
pf.price = 120.50
pf.active = 1
pf.id_category_default = 2
pf.additional_category_append(2)
pf.additional_category_append(9)
# ... other fields ...

# Get the dictionary for the API
api_dict = pf.to_dict()

# Output part of the dictionary for an example
print({
    "id_supplier": api_dict.get("id_supplier"),
    "reference": api_dict.get("reference"),
    "price": api_dict.get("price"),
    "active": api_dict.get("active"),
    "name": api_dict.get("name"),
    "associations": api_dict.get("associations")
})

# Possible output (the structure of name and associations is important):
# {
#     'id_supplier': '15',
#     'reference': 'SKU-001',
#     'price': '120.500000', # Price will be formatted as a string with 6 decimal places
#     'active': '1',
#     'name': {'language': [{'attrs': {'id': 1}, 'value': 'My Product'}]}, # Multilingual field format
#     'associations': {
#         'categories': [{'id': '2'}, {'id': '9'}] # Associations with categories
#         # ... other associations if they were added
#     }
# }
```

This `api_dict` is then used in the `PrestaProduct` class to call the `create` method of the PrestaShop API.
```