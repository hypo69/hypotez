# Product Fields for Prestashop
## Overview

This document provides a detailed description of the JSON structure used for creating or updating products in Prestashop. It defines the fields and their values, explains the purpose of each element, and provides examples of how to use this data.

## Details

The JSON structure presented here is used for interacting with the Prestashop API to manage product data. It follows a specific format, ensuring compatibility with the Prestashop platform. This structure is essential for creating and managing product information within the Prestashop e-commerce system.

## Table of Contents

1.  **Product Fields**
    *   **Root Element (`product`)**
    *   **Common Fields**
    *   **Associations**
    *   **Multilingual Fields**
2.  **Important Considerations**
3.  **Example of Usage (Python)**

## Product Fields

### Root Element (`product`)

This is the main element containing all product-related data. It acts as the container for the various fields that define the product in Prestashop.

### Common Fields

These fields represent the core attributes of a product that are generally not language-dependent.

*   **`id_default_combination`**: ID of the default combination (if applicable). Set to `null` if no combinations exist.
*   **`id_tax_rules_group`**: ID of the tax rules group. **Important!** This ID must already exist in Prestashop.
*   **`id_manufacturer`**: ID of the manufacturer.
*   **`id_supplier`**: ID of the supplier.
*   **`reference`**: Product SKU (Stock Keeping Unit) or product reference.
*   **`ean13`**: EAN-13 barcode.
*   **`upc`**: UPC barcode.
*   **`ecotax`**: Ecotax or environmental tax.
*   **`quantity`**: Quantity in stock.
*   **`minimal_quantity`**: Minimum quantity required for an order.
*   **`price`**: Price (excluding tax). Note the decimal format (floating point number).
*   **`wholesale_price`**: Wholesale price.
*   **`on_sale`**: Whether to display the "Sale" label (0 or 1).
*   **`online_only`**: Available online only (0 or 1).
*   **`unity`**: Unit of measurement (e.g., "pcs").
*   **`unit_price`**: Price per unit of measurement.
*   **`reduction_price`**: Price reduction in currency.
*   **`reduction_percent`**: Price reduction in percentage.
*   **`reduction_from`**: Start date of the price reduction.
*   **`reduction_to`**: End date of the price reduction.
*   **`cache_is_pack`**: Whether the product is a pack (0 or 1).
*   **`cache_has_attachments`**: Whether the product has attached files (0 or 1).
*   **`cache_default_attribute`**: ID of the default attribute (for combinations).
*   **`advanced_stock_management`**: Whether to use advanced stock management (0 or 1).
*   **`pack_stock_type`**: Stock management type for packs (1-3).
*   **`state`**: Active (0 or 1).
*   **`available_for_order`**: Available for ordering (0 or 1).
*   **`show_price`**: Show price (0 or 1).
*   **`visibility`**: Visibility (`both`, `catalog`, `search`, `none`).
*   **`id_category_default`**: ID of the default category. **Important!** This ID must exist in Prestashop.

### Associations

This section defines connections with other entities within Prestashop.

*   **`categories`**: Array of categories to which the product belongs. The `id` of the categories must already exist.
*   **`images`**: Array of IDs of images associated with the product. The `id` of the images must already exist (usually images are uploaded first and then linked to the product).

### Multilingual Fields

These fields represent product attributes that vary based on the language.

*   **`name`**: Product name (for each language).
*   **`description`**: Full product description (for each language).
*   **`description_short`**: Short product description (for each language).
*   **`meta_title`**: Meta title (for each language).
*   **`meta_description`**: Meta description (for each language).
*   **`meta_keywords`**: Meta keywords (for each language).
*   **`link_rewrite`**: URL address (for each language). Generated automatically based on the name, but can be set manually. It is important that it is unique.
*   **`available_now`**: Text displayed when the product is in stock.
*   **`available_later`**: Text displayed when the product is out of stock.

## Important Considerations

*   **`id` Values**: All IDs (categories, images, tax groups, manufacturers, suppliers) must exist in your Prestashop. These entities need to be created first through the API or manually through the admin panel.
*   **Languages**: You need to specify values for each language supported by your store. The example only includes one language (id=1).
*   **Data Format**: Strictly adhere to the data format (numbers, strings, boolean values).
*   **Encoding**: Use UTF-8 encoding for JSON.
*   **Errors**: The Prestashop API returns detailed error messages. Read them carefully and correct any issues in your JSON.
*   **Prestashop Version**: The API might differ slightly between versions of Prestashop. Check the documentation for your specific version.
*   **Combinations**: If you work with combinations, you will need a much more complex JSON. Look at the Prestashop API documentation examples for working with combinations.

## Example of Usage (Python)

```python
import requests
import json

API_URL = "http://your-prestashop-domain/api/products" # Replace with your actual API URL
API_KEY = "YOUR_API_KEY" # Replace with your actual API key

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {API_KEY}"
}

data = {
  "product": {
    "id_default_combination": None,
    "id_tax_rules_group": "1",
    "reference": "REF-001",
    "quantity": "100",
    "price": "10.000000",
    "state": "1",
    "available_for_order": "1",
    "show_price": "1",
    "visibility": "both",
    "id_category_default": "2",
    "name": [
      {
        "language": {
          "id": "1"
        },
        "value": "Новый товар"
      }
    ],
    "description_short": [
      {
        "language": {
          "id": "1"
        },
        "value": "<p>Краткое описание нового товара.</p>"
      }
    ],
    "link_rewrite": [
      {
        "language": {
          "id": "1"
        },
        "value": "novyj-produkt"
      }
    ]
  }
}

try:
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    print(f"Product created successfully: {response.json()}")
except requests.exceptions.HTTPError as ex:
    print(f"Error creating product: {ex}")