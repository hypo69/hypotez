# Category Editor

## Overview

This module provides a GUI application for preparing advertising campaigns. The `CategoryEditor` class handles the user interface and functionality for loading, editing, and preparing campaign categories.

## Details

This module serves as a user-friendly interface for preparing advertising campaigns based on predefined categories. The `CategoryEditor` class provides a graphical interface that allows users to load campaign data from JSON files, display the campaign information, and prepare individual categories or all categories within a campaign.

## Classes

### `CategoryEditor`

**Description**: This class provides a GUI interface for managing and preparing campaign categories. It allows users to load JSON files, display campaign data, and prepare individual or all categories.

**Inherits**: `QtWidgets.QWidget`

**Attributes**:

- `campaign_name` (str): Name of the currently loaded campaign.
- `data` (SimpleNamespace): Object storing campaign data loaded from a JSON file.
- `language` (str): Language of the campaign (default: 'EN').
- `currency` (str): Currency used in the campaign (default: 'USD').
- `file_path` (str): Path to the loaded JSON file.
- `editor` (AliCampaignEditor): Instance of the `AliCampaignEditor` class responsible for processing campaign data.
- `main_app` (MainApp): Instance of the main application (passed during initialization).

**Methods**:

- `__init__(parent=None, main_app=None)`: Initializes the `CategoryEditor` widget. 
    - Sets up the user interface (`setup_ui`) and connections between widgets (`setup_connections`).
    - Saves the `MainApp` instance for potential future interaction.
- `setup_ui()`: Creates and configures the GUI elements:
    - Open button (`open_button`) to select a JSON file.
    - File name label (`file_name_label`) displaying the currently loaded file.
    - "Prepare All Categories" button (`prepare_all_button`) to process all categories.
    - "Prepare Category" button (`prepare_specific_button`) to process a specific category.
    - Arranges widgets using a vertical layout (`QVBoxLayout`).
- `setup_connections()`: Sets up signal-slot connections between widgets (not implemented yet).
- `open_file()`: Opens a file dialog to select a JSON file and loads it.
- `load_file(campaign_file)`: Loads the campaign data from the specified JSON file.
    - Reads the file using `j_loads_ns` and stores the data in the `data` attribute.
    - Sets the file path, campaign name, and language attributes.
    - Creates an instance of `AliCampaignEditor` to handle campaign processing.
    - Calls `create_widgets` to display the loaded campaign data.
    - If an error occurs during file loading, displays a critical message box.
- `create_widgets(data)`: Creates widgets to display the campaign data.
    - Removes previous widgets (except for "Open File", file label, and "Prepare" buttons) from the layout.
    - Adds a title label and campaign name label to the layout.
    - Iterates through the categories and adds a label for each category to the layout.
- `prepare_all_categories_async()`: Asynchronously prepares all categories in the campaign.
    - Calls `prepare_all_categories` on the `editor` instance.
    - If successful, displays an information message box.
    - If an error occurs, displays a critical message box.
- `prepare_category_async()`: Asynchronously prepares a specific category in the campaign.
    - Calls `prepare_category` on the `editor` instance with the campaign name.
    - If successful, displays an information message box.
    - If an error occurs, displays a critical message box.

## Inner Functions

**None.**

## How the Class Works

The `CategoryEditor` class provides a user-friendly interface for managing and preparing advertising campaigns. 

1. **Initialization**: The class is initialized with the `__init__` method, which sets up the user interface, establishes connections between widgets, and saves the `MainApp` instance for potential future interactions.
2. **Loading Campaign Data**: Users can select a JSON file containing campaign data using the "Open File" button. The `open_file` method triggers a file dialog, and the selected file is loaded by the `load_file` method. The `load_file` method reads the JSON file and stores the data in the `data` attribute, which is a `SimpleNamespace` object. It also initializes an instance of the `AliCampaignEditor` class to handle campaign processing.
3. **Displaying Campaign Data**: Once the file is loaded, the `create_widgets` method generates widgets to display the campaign data. It dynamically adds labels for the campaign title, name, and each category within the layout.
4. **Category Preparation**: The user can choose to prepare either all categories or a specific category.
    - The "Prepare All Categories" button triggers the `prepare_all_categories_async` method, which asynchronously prepares all categories using the `prepare_all_categories` method of the `editor` instance.
    - The "Prepare Category" button triggers the `prepare_category_async` method, which asynchronously prepares a specific category using the `prepare_category` method of the `editor` instance.
    - After each preparation process, the application displays a message box indicating success or failure.

## Examples

```python
# Creating a CategoryEditor instance (assuming a MainApp instance is available)
category_editor = CategoryEditor(main_app=main_app)

# Opening a JSON file containing campaign data
category_editor.open_file()

# Preparing all categories
category_editor.prepare_all_categories_async()

# Preparing a specific category
category_editor.prepare_category_async()
```

## Parameter Details

- `campaign_file` (str): The path to the JSON file containing campaign data.

##  Examples

```python
# Loading a campaign data file
category_editor = CategoryEditor()
category_editor.load_file("path/to/campaign_data.json")

# Preparing all categories
category_editor.prepare_all_categories_async()

# Preparing a specific category
category_editor.prepare_category_async()

# Accessing campaign data
campaign_name = category_editor.campaign_name
language = category_editor.language

# Creating a new category
category_editor.editor.add_category("New Category Name")

# Removing a category
category_editor.editor.remove_category("Category Name")

# Getting a category's data
category_data = category_editor.editor.get_category_data("Category Name")
```

## Logger Usage

```python
from src.logger import logger

# Logging information
logger.info('Campaign data loaded successfully.')

# Logging errors
try:
    # Code that might raise an exception
    ...
except Exception as ex:
    logger.error('Failed to prepare category:', ex, exc_info=True) 
```

## Webdriver Usage

```python
from src.webdirver import Driver, Chrome

# Creating a driver instance (example with Chrome)
driver = Driver(Chrome)

# Example of using driver.execute_locator() to interact with a web element
close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```

## Notes

- The code provided is a part of the `hypotez` project, so make sure to consult other project files for context and potential dependencies.
- This documentation is a general guide and may not cover all aspects of the code. For specific details, refer to the code itself.
- Be mindful of the location of this file within the project structure, as it can provide valuable insight into its purpose.