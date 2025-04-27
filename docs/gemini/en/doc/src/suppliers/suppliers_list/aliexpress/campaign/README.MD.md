#  `src.suppliers.suppliers_list.aliexpress.campaign`

## Overview

The `campaign` module is designed to manage the process of creating and publishing advertising campaigns on Facebook. It includes functionality for initializing campaign parameters (name, language, currency), creating directory structures, saving configurations for the new campaign, collecting and saving product data via `ali` or `html`, generating promotional materials, reviewing the campaign, and publishing it on Facebook.

## Details

The module orchestrates a series of steps to build a comprehensive Facebook advertising campaign. It leverages various functions and classes to handle tasks like data collection, file management, and campaign configuration. The `campaign` module plays a crucial role in streamlining the process of building effective Facebook ads for products on AliExpress.


## Classes

### `AliCampaignEditor`

**Description:** This class manages the editing and modification of AliExpress campaigns. It provides methods to update product details, add new products, remove existing products, and modify campaign properties.

**Inherits:** None

**Attributes:**

- `campaign_name` (str): The name of the AliExpress campaign.
- `language` (str): The language of the campaign.
- `currency` (str): The currency used in the campaign.

**Methods:**

- `delete_product(product_id: str) -> None`: Removes a product from the campaign.
- `update_product(product_id: str, **kwargs: dict) -> None`: Updates the details of an existing product.
- `update_campaign(description: str, **kwargs: dict) -> None`: Updates the campaign's description or other properties.
- `update_category(category_name: str, **kwargs: dict) -> None`: Updates the configuration of a specific category within the campaign.
- `get_category(category_name: str) -> Optional[SimpleNamespace]`: Retrieves the details of a specific category.
- `list_categories() -> List[str]`: Lists all available categories in the campaign.
- `get_category_products(category_name: str) -> List[SimpleNamespace]`: Returns a list of products associated with the specified category.
- `other_methods() -> None`: Placeholder for additional methods that may be added to the class.

## Functions

### `process_campaign`

**Purpose**: This function orchestrates the processing of AliExpress campaigns, enabling the selection and execution of specific tasks.

**Parameters:**

- `campaign_name` (str): The name of the campaign to process.
- `language` (Optional[str] = None): The language of the campaign. If not provided, processes all locales.
- `currency` (Optional[str] = None): The currency of the campaign. If not provided, processes all currencies.
- `categories` (Optional[List[str]] = None): A list of categories to process. If not provided, processes the entire campaign.

**Returns:**
- `None`

**Raises Exceptions:**
- `SomeError`: Description of the situation where the `SomeError` exception is raised.

**Inner Functions**: None

**How the Function Works:**

1.  **Initialization**: The function starts by verifying if all campaigns need to be processed or only a specific one. It then checks if language and currency are specified, enabling the processing of particular locales.
2.  **Campaign Selection**: If the function is processing specific campaigns, it retrieves the selected campaign and checks if categories are specified.
3.  **Category Selection**: If categories are defined, the function iterates through each specified category and processes it.
4.  **Campaign Processing**: The function processes either all locales or a specific locale for each campaign based on the provided parameters.
5.  **Return**: After processing, the function returns `None`.

**Examples:**

```python
process_campaign(campaign_name="Summer Sale")
process_campaign(campaign_name="Summer Sale", language="English", currency="USD")
process_campaign(campaign_name="Summer Sale", categories=["Electronics", "Fashion"])
```

## Parameter Details

- `campaign_name` (str): The name of the AliExpress campaign to be processed.
- `language` (Optional[str] = None): The language of the campaign. If not provided, processes all locales.
- `currency` (Optional[str] = None): The currency of the campaign. If not provided, processes all currencies.
- `categories` (Optional[List[str]] = None): A list of categories to process. If not provided, processes the entire campaign.

## Examples

```python
# Create a new campaign
campaign_editor = AliCampaignEditor(campaign_name="Summer Sale", language="English", currency="USD")

# Update a product
campaign_editor.update_product(product_id="1234567890", title="New Product Title", price=10.99)

# Get category products
products = campaign_editor.get_category_products(category_name="Electronics")

# Process the campaign for a specific language and currency
process_campaign(campaign_name="Summer Sale", language="English", currency="USD")

# Process the campaign for a specific category
process_campaign(campaign_name="Summer Sale", categories=["Electronics"])
```