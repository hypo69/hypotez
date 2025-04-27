**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
[Explanation of what the code does.]

Execution Steps
-------------------------
1. [Description of the first step.]
2. [Description of the second step.]
3. [Continue as needed...]

Usage Example
-------------------------

```python
    [Code usage example]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
```

## How to Use the `MexironBuilder` Class

### Description

The `MexironBuilder` class is the core of the script. It orchestrates the entire process of creating a "mechiron" for Sergey Kazarinov. The class handles data extraction, AI processing, report generation, and Facebook publication. 

### Execution Steps

1. **Initialization**: The `MexironBuilder` is initialized with a Selenium WebDriver instance (`driver`) and an optional custom name for the mechiron process (`mexiron_name`).
2. **Configuration Loading**: The class loads configuration from a JSON file.
3. **Export Path Setting**: The export path for data is set.
4. **AI Model Initialization**: The Google Generative AI model is initialized with system instructions.
5. **Scenario Execution (`run_scenario`)**:
    - The `run_scenario` method takes URLs as input and executes the entire workflow:
        - Parses data from each URL using an appropriate graber.
        - Converts the parsed data into a dictionary format.
        - Saves the data to a file.
        - Processes the data through the AI model.
        - Generates HTML and PDF reports.
        - Publishes the processed data to Facebook.
6. **Data Processing (`process_llm`)**:
    - The `process_llm` method processes a list of product data dictionaries through the AI model. 
7. **Facebook Publication (`post_facebook`)**:
    - The `post_facebook` method handles publishing the processed data to Facebook.

### Usage Example

```python
from src.webdriver.driver import Driver
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

# Initialize Driver
driver = Driver(...)

# Initialize MexironBuilder
mexiron_builder = MexironBuilder(driver)

# Run Scenario
urls = ['https://example.com/product1', 'https://example.com/product2']
mexiron_builder.run_scenario(urls=urls)
```

### Key Methods

- **`__init__(self, driver: Driver, mexiron_name: Optional[str] = None)`**: Initializes the `MexironBuilder` class with the WebDriver and optional custom name.
- **`run_scenario(self, system_instruction: Optional[str] = None, price: Optional[str] = None, mexiron_name: Optional[str] = None, urls: Optional[str | List[str]] = None, bot = None) -> bool`**: Executes the entire scenario, including data extraction, AI processing, report generation, and Facebook publication.
- **`get_graber_by_supplier_url(self, url: str)`**: Retrieves the appropriate graber for the given supplier URL.
- **`convert_product_fields(self, f: ProductFields) -> dict`**: Converts product fields into a dictionary.
- **`save_product_data(self, product_data: dict)`**: Saves product data to a file.
- **`process_llm(self, products_list: List[str], lang: str, attempts: int = 3) -> tuple | bool`**: Processes a list of products through the AI model.
- **`post_facebook(self, mexiron: SimpleNamespace) -> bool`**: Publishes the processed data to Facebook.
- **`create_report(self, data: dict, html_file: Path, pdf_file: Path)`**: Generates HTML and PDF reports from the processed data.

## Class Attributes

- `driver`: Selenium WebDriver instance.
- `export_path`: Path for data export.
- `mexiron_name`: Custom name for the mechiron process.
- `price`: Price for processing.
- `timestamp`: Timestamp for the process.
- `products_list`: List of processed product data.
- `model`: Google Generative AI model.
- `config`: Configuration loaded from JSON.