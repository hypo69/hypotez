**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `PrestaProduct` Module
=========================================================================================

Description
-------------------------
The `PrestaProduct` module (`src/endpoints/prestashop/product.py`) provides direct interaction with **products** via the PrestaShop Web Service API. It inherits from the base `PrestaShop` class (from `api.py`), which provides general functionality for working with the API (CRUD methods, request and response handling).

The `PrestaProduct` class adds specific logic for working with the `products` resource of the PrestaShop API, simplifying tasks such as:

1. **Getting the product schema:** Requesting the data structure for the `products` resource.
2. **Adding a new product:** Receiving product data in the format of a `ProductFields` object, preparing it (including category handling), and sending a request to create the product (`POST /api/products`).
3. **Getting information about a product:** Requesting data for a specific product by its ID (`GET /api/products/{id}`).
4. **Handling category hierarchy:** Automatically determining and adding all parent categories for a product when creating it.
5. **Uploading images:** (Implicitly through `PrestaShop.create_binary` and `upload_image_from_url`) The ability to upload the main image for a newly created product.

The main use case: After the `Graber` has collected data from the supplier's page and filled the `ProductFields` object, this object is passed to the `add_new_product` method of the `PrestaProduct` class to create the corresponding product in the PrestaShop store.

Execution Steps
-------------------------
1. **Initialization:** Create an instance of `PrestaProduct` with the necessary API credentials.
2. **Adding a product:** Call the `add_new_product` method with a populated `ProductFields` object.
3. **Processing:** Inside `add_new_product`:
    - Determine and add parent categories (`_add_parent_categories`).
    - Convert `ProductFields` data to a dictionary (`pf.to_dict()`).
    - Convert the dictionary to XML (`dict2xml`).
    - Send a POST request to the API (`self.create`).
    - Upload an image (if available) (`self.create_binary` or `self.upload_image_from_url`).

Usage Example
-------------------------

```python
from src.endpoints.prestashop.product import PrestaProduct
from src.endpoints.prestashop.product_fields import ProductFields

# pf - is a ProductFields object filled by the graber
pf: ProductFields = get_product_data_from_supplier()

# Initialize PrestaProduct (API keys will be taken from Config)
pp = PrestaProduct()

# Add product to PrestaShop
result = pp.add_new_product(pf)

if result:
    print(f"Product successfully added. ID: {result.id}")
else:
    print("Failed to add product.")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".