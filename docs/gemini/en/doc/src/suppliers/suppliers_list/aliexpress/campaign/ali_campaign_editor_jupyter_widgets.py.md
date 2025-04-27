# Jupyter Widgets for AliExpress Campaign Editor

## Overview

This module provides widgets for managing AliExpress campaigns in Jupyter notebooks. Users can select campaigns, categories, and languages, and perform actions such as initializing editors, saving campaigns, and showing products.

## Details

The `JupyterCampaignEditorWidgets` class is responsible for displaying and managing widgets related to AliExpress campaign editing within a Jupyter notebook environment. It leverages the `AliCampaignEditor` class from the `aliexpress.campaign` module to interact with campaign data and perform various actions.

## Classes

### `JupyterCampaignEditorWidgets`

**Description**: This class provides a set of widgets for interacting with and managing AliExpress campaigns within a Jupyter notebook.

**Inherits**: `None`

**Attributes**:

- `language: str = None`: Stores the selected language for the campaign.
- `currency: str = None`: Stores the selected currency for the campaign.
- `campaign_name: str = None`: Stores the selected campaign name.
- `category_name: str = None`: Stores the selected category name.
- `category:SimpleNamespace = None`: Represents the selected category.
- `campaign_editor: AliCampaignEditor = None`: An instance of the `AliCampaignEditor` class for managing the campaign.
- `products:list[SimpleNamespace] = None`: A list of products associated with the selected category.

**Methods**:

- `__init__(self)`: Initializes the widgets and sets up the campaign editor. Creates dropdown menus for campaign names, categories, and languages, sets up default values, and defines callbacks for widget interactions.
- `initialize_campaign_editor(self, _)`: Initializes the campaign editor based on the selected campaign, category, and language. Updates the category dropdown based on the campaign name, and creates an instance of the `AliCampaignEditor` class for managing the campaign.
- `update_category_dropdown(self, campaign_name: str)`: Updates the category dropdown menu with categories from the selected campaign.
- `on_campaign_name_change(self, change: dict[str, str])`: Handles changes in the campaign name dropdown menu. Updates the category dropdown based on the new campaign name and re-initializes the campaign editor.
- `on_category_change(self, change: dict[str, str])`: Handles changes in the category dropdown menu. Re-initializes the campaign editor based on the new category selection.
- `on_language_change(self, change: dict[str, str])`: Handles changes in the language dropdown menu. Re-initializes the campaign editor based on the new language selection.
- `save_campaign(self, _)`: Saves the selected campaign and its associated categories to the Google Spreadsheet.
- `show_products(self, _)`: Displays the products belonging to the selected category.
- `open_spreadsheet(self, _)`: Opens the Google Spreadsheet for the campaign in a browser.
- `setup_callbacks(self)`: Sets up callbacks for all widgets, connecting them to their respective methods for handling events.
- `display_widgets(self)`: Displays all widgets in the Jupyter notebook, providing an interface for users to interact with and manage campaigns.

**Example**:

```python
editor_widgets: JupyterCampaignEditorWidgets = JupyterCampaignEditorWidgets()
editor_widgets.display_widgets()
```

## Functions

### `get_directory_names`

**Purpose**: This function retrieves a list of directory names from a specified path.

**Parameters**:

- `path (Path)`: The path to search for directories.

**Returns**:

- `list[str]`: A list of directory names within the specified path.

**Example**:

```python
directories: list[str] = get_directory_names(Path("/some/dir"))
print(directories)
# Output: ['dir1', 'dir2']