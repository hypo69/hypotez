# Module: EmilDesign - Модуль для управления изображениями и продвижения в Facebook и PrestaShop

## Overview

This module is designed for managing and processing images, along with promotion activities in Facebook and PrestaShop. It is specifically tailored for the `emil-design.com` store. 

The module includes:

- Image description using Gemini AI.
- Loading product descriptions to PrestaShop.
-  ... (any other functionalities)

## Classes

### `Config`

**Description**: This class holds configuration settings for the EmilDesign module. It includes settings for API endpoints, domain names, keys, and other relevant parameters.
**Attributes**:
- `ENDPOINT` (str):  The name of the endpoint.
- `MODE` (str):  Determines the API endpoint.
- `POST_FORMAT` (str):  The format for API requests.
- `API_DOMAIN` (str): The API domain.
- `API_KEY` (str): The API key.
- `suppliers` (list):  A list of suppliers associated with the module.

**How the class works**:
The `Config` class defines the core settings for the module's functionality. It sets up the necessary API endpoints, keys, and other configuration parameters based on the specified `MODE`. It also defines the suppliers that are managed by this module. The `USE_ENV` variable determines whether the configuration values are loaded from environment variables or from the `keepass` database. 
**Example**:
```python
from src.endpoints.emil.emil_design import Config

config = Config()
print(config.API_DOMAIN) # Output: 'emil-design.com' or 'dev.emil-design.com' or 'prod.emil-design.com' based on the current MODE

# Print the list of suppliers
print(config.suppliers)
```

### `EmilDesign`

**Description**: This class orchestrates the entire process of image design and promotion, handling image descriptions, Facebook promotion, and PrestaShop product uploads.
**Attributes**:
- `gemini` (Optional[GoogleGenerativeAi]): An instance of the Google Gemini AI model for image description.
- `openai` (Optional[OpenAIModel]):  An instance of the OpenAI model for image description.
- `base_path` (Path): The base directory for the module.
- `config` (SimpleNamespace): Configuration settings for the module loaded from a JSON file.
- `data_path` (Path): The directory where data related to the module is stored.
- `gemini_api` (str): The API key for the Gemini AI model.
- `presta_api` (str): The API key for the PrestaShop instance.
- `presta_domain` (str): The domain name of the PrestaShop instance.

**Methods**:

#### `process_suppliers`

**Purpose**:  Processes a list of suppliers based on a provided prefix or the default list of suppliers.
**Parameters**:
- `supplier_prefix` (Optional[str | List[str, str]], optional): Prefix for suppliers. Defaults to an empty string, indicating all suppliers.
**Returns**:
- `bool`: True if processing is successful, False otherwise.
**Raises Exceptions**:
- `Exception`: If any error occurs during supplier processing.
**How the Function Works**:
The function retrieves a list of suppliers based on the given prefix. It then iterates through each supplier and retrieves the corresponding graber object. If a graber is found, it processes its scenarios asynchronously and logs the progress.
**Examples**:
```python
from src.endpoints.emil.emil_design import EmilDesign

emil = EmilDesign()

# Process all suppliers 
asyncio.run(emil.process_suppliers())

# Process suppliers with a specific prefix 
asyncio.run(emil.process_suppliers(supplier_prefix='prefix_name'))

# Process a list of suppliers
asyncio.run(emil.process_suppliers(supplier_prefix=['prefix_name1', 'prefix_name2']))
```

#### `describe_images`

**Purpose**:  Generates descriptions for images using the Gemini AI model.
**Parameters**:
- `lang` (str):  The language for the image descriptions.
- `models` (dict, optional): Configuration for the AI models used for description. Defaults to Gemini and OpenAI models.
**Returns**:
- `None`
**Raises Exceptions**:
- `FileNotFoundError`: If the instruction files are not found.
- `Exception`:  If any error occurs during image processing.
**How the Function Works**:
The function loads system instructions and prompts for image descriptions. It then iterates through a list of images and retrieves the raw image data. The image data is then sent to the Gemini AI model for generating descriptions. The descriptions are saved as JSON files.
**Examples**:
```python
from src.endpoints.emil.emil_design import EmilDesign

emil = EmilDesign()

# Describe images in Hebrew
emil.describe_images(lang='he')

# Describe images in English
emil.describe_images(lang='en')
```


#### `promote_to_facebook`

**Purpose**:  Promotes images and their descriptions on Facebook.
**Parameters**:
- `None`
**Returns**:
- `None`
**Raises Exceptions**:
- `Exception`: If any error occurs during Facebook promotion.
**How the Function Works**:
The function opens a Facebook group page and posts messages containing image information. It retrieves messages from a JSON file and creates a message object for each message. It then uses the `post_message` function to post the message on the Facebook group.
**Examples**:
```python
from src.endpoints.emil.emil_design import EmilDesign

emil = EmilDesign()

# Promote images and descriptions to Facebook
asyncio.run(emil.promote_to_facebook())
```


#### `upload_described_products_to_prestashop`

**Purpose**:  Uploads product information to PrestaShop.
**Parameters**:
- `products_list` (Optional[List[SimpleNamespace]], optional): List of product information. Defaults to `None`.
- `id_lang` (Optional[int | str], optional): Language ID for PrestaShop databases. 
**Returns**:
- `bool`: True if upload succeeds, False otherwise.
**Raises Exceptions**:
- `FileNotFoundError`: If the locales file is not found.
- `Exception`:  If any error occurs during PrestaShop upload.
**How the Function Works**:
The function retrieves a list of products from a directory of JSON files. It creates a `PrestaProduct` object to interact with the PrestaShop API. It then iterates through the list of products and uploads each product using the `add_new_product` function.
**Examples**:
```python
from src.endpoints.emil.emil_design import EmilDesign

emil = EmilDesign()

# Upload described products to PrestaShop in Hebrew 
emil.upload_described_products_to_prestashop(id_lang=2)

# Upload described products to PrestaShop in English
emil.upload_described_products_to_prestashop(id_lang='en')
```


## Parameter Details

- `lang` (str): The language for the image descriptions or other operations. 
- `models` (dict, optional): Configuration for the AI models used for image description. Defaults to Gemini and OpenAI models.
- `supplier_prefix` (Optional[str | List[str, str]], optional): Prefix for suppliers. Defaults to an empty string, indicating all suppliers.
- `products_list` (Optional[List[SimpleNamespace]], optional): List of product information. Defaults to `None`.
- `id_lang` (Optional[int | str], optional): Language ID for PrestaShop databases. 

## Examples

```python
from src.endpoints.emil.emil_design import EmilDesign

emil = EmilDesign()

# Process all suppliers
asyncio.run(emil.process_suppliers())

# Describe images in Hebrew
emil.describe_images(lang='he')

# Promote images and descriptions to Facebook
asyncio.run(emil.promote_to_facebook())

# Upload described products to PrestaShop in Hebrew
emil.upload_described_products_to_prestashop(id_lang=2) 
```