# Module `src.endpoints.emil.scenarios.from_supplier_to_prestashop`

## Overview

This module is responsible for executing the scenario related to extracting, parsing, and processing product data from various suppliers. The module handles data preparation, AI processing, and integration with Prestashop for product posting. 

## Details

This module is used for processing products from various suppliers, extracting relevant data, and integrating it into Prestashop. It utilizes the `SupplierToPrestashopProvider` class, which orchestrates the entire process. 

The module's primary goal is to automate the product posting process, simplifying the workflow and reducing manual effort. It leverages AI models for data processing and utilizes web drivers to interact with Prestashop and other related platforms.

## Classes

### `SupplierToPrestashopProvider`

**Description**:  Handles the extraction, parsing, and saving of product data from suppliers. Data can be obtained from external websites or JSON files.

**Attributes**:

- `driver (Driver)`: An instance of Selenium WebDriver.
- `export_path (Path)`: The path for exporting data.
- `products_list (List[dict])`: A list of processed product data dictionaries.
- `mexiron_name (str)`: Name of the product.
- `price (float)`: Product price.
- `timestamp (str)`: Timestamp of data processing.
- `model (GoogleGenerativeAi)`: An instance of the Gemini AI model.
- `config (SimpleNamespace)`: Configuration settings.
- `local_images_path (Path)`: Path for storing locally downloaded images.
- `lang (str)`: Language code for AI processing.
- `gemini_api (str)`: API key for the Gemini AI model.
- `presta_api (str)`: API key for the Prestashop instance.
- `presta_url (str)`: URL of the Prestashop instance.

**Methods**:

- `__init__(self, lang: str, gemini_api: str, presta_api: str, presta_url: str, driver: Optional[Driver] = None)`: Initializes the `SupplierToPrestashopProvider` class with required components.
- `initialise_ai_model(self)`: Initializes the Gemini AI model.
- `process_graber(self, urls: list[str], price: Optional[str] = '', mexiron_name: Optional[str] = '', scenarios: dict | list[dict, dict] = None)`: Executes the scenario: parses products, processes them via AI, and stores data.
- `process_scenarios(self, suppliers_prefixes: Optional[str] = '')`: Processes scenarios for various suppliers.
- `save_product_data(self, product_data: dict)`: Saves individual product data to a file.
- `process_llm(self, products_list: List[str], lang: str, attempts: int = 3)`: Processes the product list through the AI model.
- `save_in_prestashop(self, products_list: ProductFields | list[ProductFields])`: Saves products to Prestashop.
- `post_facebook(self, mexiron: SimpleNamespace)`: Executes the Facebook advertisement scenario.
- `create_report(self, data: dict, lang: str, html_file: Path, pdf_file: Path)`: Generates a report for the product in HTML and PDF formats and sends the PDF to a bot.

## Functions

### `upload_redacted_images_from_emil()`:

**Purpose**: Reads a JSON file containing a list of images received from Emil and saves the images in the Prestashop instance.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**Example**:
```python
await upload_redacted_images_from_emil()
```


### `main()`:

**Purpose**: Main entry point for the module.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**Example**:
```python
if __name__ == '__main__':
    asyncio.run(main())
```


## Parameter Details

### `driver (Driver)`: 
- An instance of the `Driver` class, which manages the Selenium WebDriver. It's used for interacting with web pages, such as visiting URLs, locating elements, and performing actions on them. 


### `export_path (Path)`: 
- The path to the directory where the processed product data will be saved. This directory is used for storing JSON files containing information about each product.

### `products_list (List[dict])`:
- A list that stores dictionaries representing the processed product data. Each dictionary typically contains information such as product ID, name, description, specifications, and image paths.

### `mexiron_name (str)`:
- The name of the product. This is used for generating titles and descriptions for the product.

### `price (float)`:
- The price of the product. It's used for displaying pricing information in the Prestashop listing and for potential advertisement purposes.

### `timestamp (str)`:
-  The timestamp of the data processing. It helps track when the data was extracted and processed, allowing for auditing and historical analysis.

### `model (GoogleGenerativeAi)`:
- An instance of the `GoogleGenerativeAi` class, which represents the Google Gemini AI model. It's used for processing product data, generating descriptions, and potentially providing additional insights.

### `config (SimpleNamespace)`: 
-  A namespace object containing configuration settings for the module. These settings can include things like API keys, paths, and other configuration parameters that are used for different parts of the data processing workflow.

### `local_images_path (Path)`:
-  The path to the directory where locally downloaded images are stored. It's used for managing and accessing image files.

### `lang (str)`: 
-  The language code used for AI processing. This is likely "he" for Hebrew, which might be the primary language of the target market or the specific product information.

### `gemini_api (str)`:
- The API key for accessing the Google Gemini AI model. This key is used to authenticate requests to the AI model and ensure authorized access.

### `presta_api (str)`:
-  The API key for accessing the Prestashop instance. This key is used to authenticate requests to the Prestashop API and enable the module to update product information.

### `presta_url (str)`:
- The URL of the Prestashop instance where the product data will be saved. This URL is used to interact with the Prestashop API and upload product information.

### `urls (list[str])`: 
- A list of product page URLs. This list is used for fetching product data from the suppliers' websites.


### `scenarios (dict | list[dict, dict])`:
- A dictionary or a list of dictionaries representing scenarios for processing different types of products. Each scenario can specify a set of actions to be performed for a specific product type, such as data extraction methods or AI processing instructions. 

### `attempts (int)`:
-  The number of retry attempts if the AI model returns an invalid response. This parameter helps ensure that the AI processing is successful by retrying the request if there are initial errors or issues. 


### `products_list (List[str])`: 
-  A list containing a collection of product data dictionaries as strings. Each dictionary represents a product and contains relevant information about it.

### `products_ns (SimpleNamespace)`: 
- A SimpleNamespace object that holds the product data in a structured format. This allows for easy access to the data within the object's attributes.

### `mexiron (SimpleNamespace)`: 
- A SimpleNamespace object that represents a product, potentially containing data about the product's name, description, price, and other relevant information.

### `data (dict)`: 
-  A dictionary containing the product data that will be used to generate the report. 

### `lang (str)`:
-  The language code for the report. This is likely "he" for Hebrew.

### `html_file (Path)`: 
-  The path to the file where the HTML report will be saved.

### `pdf_file (Path)`:
-  The path to the file where the PDF report will be saved.

### `f (dict)`:
- A dictionary representing the extracted product data. This dictionary typically contains key-value pairs where the keys are product fields (like ID, name, description, etc.) and the values are the corresponding data. 

### `q (str)`:
-  A string representing the request to the AI model. This string combines the model command (instruction) with the product data, instructing the AI model to process the data accordingly.

### `response (str)`: 
-  The response returned by the AI model. This response might contain processed product data or generated descriptions.

### `response_dict (dict)`: 
-  A dictionary representing the parsed JSON response from the AI model. This dictionary structure allows for accessing the response data in a structured format. 

### `title (str)`:
- The title of the post to be shared on Facebook. The title is typically generated based on the product's information.

### `media (str)`:
- The media file path (image, video, etc.) to be uploaded to the Facebook post. This path is used to attach the product's image to the post.