# Quotation Builder Module 

## Overview

This module handles data preparation, AI processing, and integration with Facebook for product posting. 

## Details

This module is responsible for extracting, parsing, and processing product data from various suppliers. It handles data preparation, AI processing, and integration with Facebook for product posting.

## Classes

### `QuotationBuilder`

**Description:**  A class that processes product data from suppliers, prepares data for AI processing, and interacts with Facebook for product posting.

**Attributes:**

- `base_path (Path):` The base path for the project's resources.
- `config (SimpleNamespace):` Configuration settings loaded from a JSON file.
- `html_path (str | Path):` The path to the HTML report file.
- `pdf_path (str | Path):` The path to the PDF report file.
- `docx_path (str | Path):` The path to the DOCX report file.
- `driver (Driver):` An instance of the Selenium WebDriver (Firefox or Playwright).
- `export_path (Path):` The path to export processed product data.
- `mexiron_name (str):` The name of the Mexiron process.
- `price (float):` The price of the product.
- `timestamp (str):` Timestamp of the product data.
- `products_list (List):` A list of processed product data dictionaries.
- `model (GoogleGenerativeAi):` An instance of the Google Generative AI model.
- `translations (SimpleNamespace):` Translations for the Mexiron process, loaded from a JSON file.
- `required_fields (tuple):` A tuple of required product data fields.

**Methods:**

- `__init__(self, mexiron_name: Optional[str] = gs.now, driver: Optional[Firefox | Playwrid | str] = None,  **kwargs):` Initializes the `QuotationBuilder` class, setting up WebDriver, AI model, and export paths.
- `convert_product_fields(self, f: ProductFields) -> dict:` Converts product fields from a `ProductFields` object into a dictionary for AI processing.
- `process_llm(self, products_list: List[str], lang: str, attempts: int = 3) -> tuple | bool:`  Processes a list of product data dictionaries through the AI model to generate translated descriptions.
- `process_llm_async(self, products_list: List[str], lang: str, attempts: int = 3) -> tuple | bool:` Asynchronously processes a list of product data dictionaries through the AI model. 
- `save_product_data(self, product_data: dict) -> bool:` Saves individual product data to a JSON file.
- `post_facebook_async(self, mexiron: SimpleNamespace) -> bool:` Asynchronously posts product information to Facebook.


## Inner Functions

### `convert_product_fields`

**Purpose:** Converts product fields from a `ProductFields` object into a dictionary suitable for AI processing. 

**Parameters:**

- `f (ProductFields):` An object containing parsed product data.

**Returns:**

- `dict:` A dictionary containing formatted product data.

**How the Function Works:**

This function iterates through the product data fields, extracting relevant information and converting it to a format compatible with the AI model. The extraction logic is based on the structure of the `ProductFields` object, which specifies how product information is stored and retrieved.

**Examples:**

```python
product_fields = ProductFields(
    id_product=12345,
    name={'language': {'value': 'Product Name'}},
    description={'language': {'value': 'Product description.'}},
    specification={'language': {'value': 'Product specifications.'}},
    local_image_path='path/to/image.jpg',
)
product_data = quotation_builder.convert_product_fields(product_fields)
print(product_data)
```
```python
# Output:
{
'product_name': 'Product Name',
'product_id': 12345,
'description_short': 'Product description.',
'description': 'Product description.',
'specification': 'Product specifications.',
'local_image_path': 'path/to/image.jpg'
}
```

### `process_llm`

**Purpose:** Processes a list of product data dictionaries through the AI model to generate translated descriptions.

**Parameters:**

- `products_list (List[str]):` A list of product data dictionaries as a string.
- `lang (str):` The language for translation.
- `attempts (int, optional):` The number of attempts to retry in case of failure. Defaults to 3.

**Returns:**

- `tuple:` A tuple containing processed responses in `ru` and `he` formats.
- `bool:` False if unable to get a valid response after retries.

**How the Function Works:**

This function sends the product data to the AI model, along with specific instructions for generating translations. It handles potential errors and retries the request a specified number of times.

**Examples:**

```python
products_list = [
    {'product_name': 'Product 1', 'product_id': 1, 'description_short': 'Short description', 'description': 'Full description', 'specification': 'Product specifications', 'local_image_path': 'image1.jpg'},
    {'product_name': 'Product 2', 'product_id': 2, 'description_short': 'Short description', 'description': 'Full description', 'specification': 'Product specifications', 'local_image_path': 'image2.jpg'},
]

response = quotation_builder.process_llm(products_list, 'he')
print(response)
```

### `save_product_data`

**Purpose:** Saves individual product data to a JSON file.

**Parameters:**

- `product_data (dict):` Formatted product data.

**Returns:**

- `bool:` True if the data is saved successfully, False otherwise.

**How the Function Works:**

This function writes the formatted product data to a JSON file, ensuring that the data is correctly structured and saved in UTF-8 encoding.

**Examples:**

```python
product_data = {
    'product_name': 'Product Name',
    'product_id': 12345,
    'description_short': 'Short description',
    'description': 'Full description',
    'specification': 'Product specifications',
    'local_image_path': 'path/to/image.jpg',
}

is_saved = quotation_builder.save_product_data(product_data)
print(is_saved)
```

## Class Methods

### `main`

**Purpose:** The main function of the module, which demonstrates how to use the `QuotationBuilder` class.

**Parameters:** None

**Returns:** None

**How the Function Works:**

This function:

1. Loads product data from a JSON file.
2. Creates an instance of the `QuotationBuilder` class.
3. Uses the `QuotationBuilder` instance to process the product data, generate translations, and save the results to files.

**Examples:**

```python
# Example of calling the main function
if __name__ == "__main__":
    main() 
```

## Parameter Details

- `mexiron_name (Optional[str]):`  The name for the Mexiron process, used for organizing exported data.  Defaults to the current timestamp if not provided.
- `driver (Optional[Firefox | Playwrid | str]):`  The type of WebDriver to use for website interactions.  Defaults to Firefox if not provided.
- `lang (str):`  The language for translation.
- `attempts (int):` The number of attempts to retry if the AI model fails to generate translations.

## Examples

```python
# Example of using the QuotationBuilder class
from src.endpoints.kazarinov.scenarios.quotation_builder import QuotationBuilder

quotation_builder = QuotationBuilder(mexiron_name='MyMexironProcess')

# Process product data
product_data = [{
    'product_name': 'Product Name',
    'product_id': 12345,
    'description_short': 'Short description',
    'description': 'Full description',
    'specification': 'Product specifications',
    'local_image_path': 'path/to/image.jpg',
}]

# Translate descriptions
translated_data = quotation_builder.process_llm(product_data, lang='he')

# Save translated product data
quotation_builder.save_product_data(translated_data)

# Post product data to Facebook (example)
facebook_post_data = ... # Construct data for Facebook post
quotation_builder.post_facebook_async(facebook_post_data)
```
```python
# Example of using webdriver with the QuotationBuilder class
from src.endpoints.kazarinov.scenarios.quotation_builder import QuotationBuilder
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox

# Create a WebDriver instance
driver = Driver(Firefox)

# Create an instance of the QuotationBuilder class using the WebDriver
quotation_builder = QuotationBuilder(driver=driver, mexiron_name='MyMexironProcess')

# ... rest of the code using the quotation_builder
```

## How the Module Works

This module combines data extraction, AI processing, and Facebook integration to streamline product posting. Here's a breakdown of its functionality:

1. **Data Extraction:** The module extracts product information from various suppliers using their specific data formats.
2. **Data Preparation:**  The extracted product data is converted into a uniform format for AI processing. 
3. **AI Processing:** The prepared data is sent to an AI model (Google Generative AI) to generate translations of product descriptions.
4. **Facebook Integration:** The translated product descriptions are used to create Facebook posts, along with relevant product details.

The module utilizes a `QuotationBuilder` class to manage these processes. This class acts as a central coordinator, handling data extraction, AI interaction, and Facebook posting.

## Additional Notes

- The module uses the `src.webdriver.driver` module to manage WebDriver interactions with websites for data extraction and Facebook posting.
- The `src.llm.gemini` module is used for communication with the Google Generative AI model for translation tasks.
- The `src.endpoints.advertisement.facebook.scenarios` module provides functions for posting products to Facebook. 
- The `src.utils.jjson` module provides functions for reading and writing JSON data.
- The `src.utils.file` module provides functions for reading and saving files.
- The `src.utils.image` module provides functions for downloading and saving images.

This module is designed to automate product posting to Facebook, reducing manual efforts and improving efficiency. It integrates with various suppliers and utilizes AI technology to enhance the quality and speed of product information dissemination.