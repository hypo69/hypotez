# PrestaShop Product Async Endpoint

## Overview

This module defines the `PrestaProductAsync` class, which handles interactions with PrestaShop products in an asynchronous manner. It fetches product data from the website, prepares data for the PrestaShop API, and performs various operations on products.

## Details

The `PrestaProductAsync` class is a subclass of `PrestaShopAsync`, which provides a foundation for communication with the PrestaShop API. This module defines additional functionalities for handling product-related operations.

## Classes

### `PrestaProductAsync`

**Description**: This class handles operations related to PrestaShop products. It provides functionalities for adding new products, updating existing products, and fetching product data.

**Inherits**: `PrestaShopAsync`

**Attributes**:

- `presta_category_async` (`PrestaCategoryAsync`): An instance of the `PrestaCategoryAsync` class used for interacting with PrestaShop categories.

**Methods**:

- `add_new_product_async(f: ProductFields) -> ProductFields | None`: Adds a new product to PrestaShop.

- `create_binary(path: str, local_path: str, id_product: int) -> bool`: Creates a binary file (typically an image) in PrestaShop.

#### `add_new_product_async`

**Purpose**: Adds a new product to PrestaShop.

**Parameters**:

- `f` (`ProductFields`): An instance of the `ProductFields` data class containing the product information.

**Returns**:

- `ProductFields | None`: Returns the `ProductFields` object with `id_product` set, if the product was added successfully, `None` otherwise.

**Raises Exceptions**:

- `Exception`: If an error occurs during the product creation process.

**How the Function Works**:

1. Retrieves the list of parent categories associated with the product's default category using `self.presta_category_async.get_parent_categories_list`.
2. Converts the `ProductFields` object into a dictionary representation using `f.to_dict()`.
3. Creates the product in PrestaShop by calling the `create` method inherited from the base class, passing the product data and the endpoint `'products'`.
4. Logs an error message if the product creation fails.
5. Attempts to upload the product image using `self.create_binary`, passing the image path and product ID.
6. Returns the `ProductFields` object with the product ID if the operation is successful, otherwise returns `None`.

**Examples**:

```python
# Example usage
product = PrestaProductAsync()
product_fields = ProductFields(
    lang_index=1,
    name='Test Product Async',
    price=19.99,
    description='This is an asynchronous test product.',
)

parent_categories = await Product.get_parent_categories(id_category=3)
print(f'Parent categories: {parent_categories}')

new_product = await product.add_new_product_async(product_fields)
if new_product:
    print(f'New product id = {new_product.id_product}')
else:
    print(f'Error add new product')
```

## Parameter Details

- `f` (`ProductFields`): An instance of the `ProductFields` data class, which represents a product with its attributes.
- `lang_index` (`int`): Index of the language for product attributes.
- `name` (`str`): Name of the product.
- `price` (`float`): Price of the product.
- `description` (`str`): Description of the product.
- `id_category_default` (`int`): ID of the default category for the product.
- `local_image_path` (`str`): Path to the product image on the local machine.

## Examples

```python
# Example usage
product = PrestaProductAsync()
product_fields = ProductFields(
    lang_index=1,
    name='Test Product Async',
    price=19.99,
    description='This is an asynchronous test product.',
)

parent_categories = await Product.get_parent_categories(id_category=3)
print(f'Parent categories: {parent_categories}')

new_product = await product.add_new_product_async(product_fields)
if new_product:
    print(f'New product id = {new_product.id_product}')
else:
    print(f'Error add new product')

await product.fetch_data_async()
```

## Your Behavior During Code Analysis:

- Inside the code, you might encounter expressions between `<` `>`. For example: `<instruction for gemini model:Loading product descriptions into PrestaShop.>, <next, if available>. These are placeholders where you insert the relevant value.
- Always refer to the system instructions for processing code in the `hypotez` project (the first set of instructions you translated);
- Analyze the file's location within the project. This helps understand its purpose and relationship with other files. You will find the file location in the very first line of code starting with `## \\file /...`;
- Memorize the provided code and analyze its connection with other parts of the project;
- In these instructions, do not suggest code improvements. Strictly follow point 5. **Example File** when composing the response.