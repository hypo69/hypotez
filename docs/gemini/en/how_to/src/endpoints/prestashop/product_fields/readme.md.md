**How to Use the `ProductFields` Module**

=========================================================================================

**Description**
-------------------------
The `ProductFields` module (located in `src/endpoints/prestashop/product_fields.py`)  is a core component for transferring product data from a supplier to PrestaShop. It functions as a **structured data container** responsible for:

1. **Representing a product:** Defines all required product fields that align with the PrestaShop data structure (the `ps_product`, `ps_product_lang` tables, and associated relationships).
2. **Storing gathered data:** Receives and stores information collected from the supplier's product page by the `Graber` class.
3. **Providing default values:** Loads default values for many fields from the `product_fields_default_values.json` file, simplifying product creation.
4. **Supporting multilingualism:** Enables easy management of field values (like name, description) for different languages supported in PrestaShop.
5. **Managing associations (relationships):** Provides methods for adding associations between the product and categories, images, features, combinations, and more.
6. **Formatting data for the API:** Transforms collected and processed data into a dictionary (`to_dict()`), fully compatible with the PrestaShop Web Service API format for creating or updating products.

Essentially, `ProductFields` is an **intermediate product representation** tailored to the requirements of the PrestaShop API, filled with data from the supplier, and subsequently passed to the `PrestaProduct` module for sending to the store.

**Execution Steps**
-------------------------
1. **Initialization:**
   - Create a `ProductFields` object:
     ```python
     product_fields = ProductFields(id_lang=1)  # Default language (English in this example)
     ```
   - The `__init__` method takes an optional `id_lang` argument (defaulting to `1`). This ID determines the language used for multilingual fields unless explicitly specified later.
   - After the object is created, `__post_init__` calls the `_payload()` method.
2. **Loading Default Values:**
   - `_payload()`:
     - Reads the list of all possible field names from `src/endpoints/prestashop/product_fields/fields_list.txt`.
     - Creates a `self.presta_fields` object (of type `SimpleNamespace`) and initializes all fields from the list with the value `None`.
     - Reads the `src/endpoints/prestashop/product_fields/product_fields_default_values.json` file.
     - Sets default values for fields specified in the JSON file within the `self.presta_fields` object.
3. **Setting Product Data:**
   - Access and modify product fields using properties (getters and setters). For example:
     ```python
     product_fields.id_supplier = 15
     product_fields.reference = "ART-123"
     product_fields.price = 99.90
     product_fields.name = "Example Product"  # Sets the name for the specified language (id_lang)
     ```
   - Setters often include data normalization (e.g., `normalize_float`, `normalize_string`).
4. **Managing Associations:**
   - Use methods to add associations, like:
     ```python
     product_fields.id_category_default = 5  # Set the main category
     product_fields.additional_category_append(5)  # Add the main category to the list of associations
     product_fields.product_features_append(feature_id=2, feature_value_id=8)  # Add a feature
     product_fields.product_tag_append(tag_id=1)  # Add a tag
     ```
   - Methods are also provided for clearing associations (`..._clear()`).
5. **Converting to API Format:**
   - Call the `to_dict()` method to transform the `ProductFields` object into a dictionary ready for the PrestaShop API:
     ```python
     api_dict = product_fields.to_dict()
     ```
   - The `to_dict()` method:
     - Filters out empty values (keys with `None` or empty string values are typically excluded, depending on field-specific implementation).
     - Converts all values to strings (the PrestaShop API, particularly when working with XML, expects string values for all fields).
     - Formats multilingual fields: Transforms the internal representation into the required API format of a list of dictionaries.
     - Formats associations: Structures association data according to API requirements.
   - The resulting dictionary is ready to be passed to the `create` or `edit` methods of the `PrestaShop` (or `PrestaProduct`) class.

**Usage Example**
-------------------------

```python
from src.endpoints.prestashop.product_fields import ProductFields

# Create a product fields object for the default language (id_lang=1)
product_fields = ProductFields()

# Set product details
product_fields.id_supplier = 15
product_fields.reference = "SKU-001"
product_fields.name = "My Product"  # Name for the default language (id_lang=1)
product_fields.price = 120.50
product_fields.active = 1
product_fields.id_category_default = 2  # Set the main category

# Add additional categories
product_fields.additional_category_append(2)
product_fields.additional_category_append(9)

# ... set other fields ...

# Convert to API format
api_dict = product_fields.to_dict()

# Print a portion of the dictionary for demonstration
print({
    "id_supplier": api_dict.get("id_supplier"),
    "reference": api_dict.get("reference"),
    "price": api_dict.get("price"),
    "active": api_dict.get("active"),
    "name": api_dict.get("name"),
    "associations": api_dict.get("associations")
})

# Possible output (the structure of 'name' and 'associations' is crucial):
# {
#     'id_supplier': '15',
#     'reference': 'SKU-001',
#     'price': '120.500000', # Price is formatted as a string with 6 decimal places
#     'active': '1',
#     'name': {'language': [{'attrs': {'id': 1}, 'value': 'My Product'}]}, # Multilingual field format
#     'associations': {
#         'categories': [{'id': '2'}, {'id': '9'}] # Associations with categories
#         # ... other associations if they were added
#     }
# }
```

The `api_dict` is then used in the `PrestaProduct` class to call the `create` method of the PrestaShop API.