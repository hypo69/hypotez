# Campaign Editor

## Overview

This module provides a graphical user interface (GUI) for editing campaign data in the `hypotez` project, specifically for AliExpress campaigns. The `CampaignEditor` class implements a window that allows users to open and load JSON files representing campaign configurations, edit campaign details, and prepare campaigns for execution.

## Details

The `CampaignEditor` class utilizes PyQt6 for building the GUI. It provides a user-friendly interface with elements for:

- **File Selection:** Opening a JSON file dialog to choose the campaign configuration file.
- **File Loading:** Loading the selected JSON file and displaying its content in a structured manner.
- **Campaign Editing:** Editing essential campaign parameters, including title, description, and promotion name.
- **Campaign Preparation:** Triggering an asynchronous campaign preparation process. 

The module relies on `AliCampaignEditor` from `src.suppliers.suppliers_list.aliexpress.campaign` to handle the actual campaign preparation logic.

## Classes

### `CampaignEditor`

**Description**: This class defines a PyQt6 widget for editing campaign data.

**Inherits**: `QtWidgets.QWidget`

**Attributes**:

- `data` (SimpleNamespace): Stores the data loaded from the JSON file.
- `current_campaign_file` (str): The path to the currently loaded campaign file.
- `editor` (AliCampaignEditor): An instance of `AliCampaignEditor` responsible for campaign preparation.

**Methods**:

#### `__init__`

**Purpose**: Initializes the `CampaignEditor` widget.

**Parameters**:

- `parent` (Optional[QtWidgets.QWidget]): The parent widget. Defaults to `None`.
- `main_app` (Optional[Any]): The main application instance. Defaults to `None`.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

1. Initializes the parent `QtWidgets.QWidget` class.
2. Saves the `main_app` instance for potential future use.
3. Calls `setup_ui` to configure the user interface.
4. Calls `setup_connections` to set up signal-slot connections.

#### `setup_ui`

**Purpose**: Configures the user interface of the `CampaignEditor` widget.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

1. Sets the window title to "Campaign Editor."
2. Resizes the window to 1800x800 pixels.
3. Creates a `QScrollArea` to accommodate content that may exceed the window size.
4. Creates a `QWidget` for the content inside the `QScrollArea`.
5. Creates a `QGridLayout` to arrange the UI elements within the `scroll_content_widget`.
6. Defines and adds UI components to the layout, including:
    - `open_button` (QPushButton): A button to open the file dialog.
    - `file_name_label` (QLabel): Displays the selected file's name.
    - `prepare_button` (QPushButton): A button to trigger campaign preparation.
7. Adds the `scroll_area` to the main layout of the widget.

#### `setup_connections`

**Purpose**: Sets up signal-slot connections for UI elements.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

- Placeholder function. No connections are set up currently.

#### `open_file`

**Purpose**: Opens a file dialog to select a JSON file for loading.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

1. Opens a `QFileDialog` to allow the user to choose a JSON file.
2. The dialog is set to open in the `c:/user/documents/repos/hypotez/data/aliexpress/campaigns` directory.
3. Filters the displayed files to only show JSON files (`*.json`).
4. If a file is selected, it calls `load_file` to load the selected file.

#### `load_file`

**Purpose**: Loads the selected JSON file and displays its content.

**Parameters**:

- `campaign_file` (str): The path to the JSON file to load.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

1. Attempts to load the JSON file using `j_loads_ns`.
2. If successful:
    - Sets the `current_campaign_file` attribute.
    - Updates the `file_name_label` to display the filename.
    - Calls `create_widgets` to create UI elements based on the loaded data.
    - Initializes an `AliCampaignEditor` instance.
3. If an error occurs during loading, displays an error message using `QtWidgets.QMessageBox`.

#### `create_widgets`

**Purpose**: Creates UI widgets based on the loaded JSON data.

**Parameters**:

- `data` (SimpleNamespace): The data loaded from the JSON file.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

1. Gets the current layout (`self.layout`).
2. Removes previous widgets from the layout except the "Open JSON File" button, the filename label, and the "Prepare Campaign" button.
3. Creates and adds UI elements for displaying and editing the campaign data, including:
    - `title_input` (QLineEdit): Displays the campaign title for editing.
    - `description_input` (QLineEdit): Displays the campaign description for editing.
    - `promotion_name_input` (QLineEdit): Displays the campaign promotion name for editing.
4. Positions the widgets within the layout using row and column indices.

#### `prepare_campaign`

**Purpose**: Asynchronously prepares the campaign using `AliCampaignEditor`.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

1. Checks if an `AliCampaignEditor` instance exists.
2. If the `editor` exists, it attempts to execute the `prepare` method asynchronously.
3. If successful, displays a success message.
4. If an error occurs, displays an error message.

## Parameter Details

- `campaign_file` (str): The path to the JSON file containing campaign data.
- `main_app` (Optional[Any]): The main application instance.

## Examples

```python
# Example usage:
from src.suppliers.aliexpress.gui.campaign import CampaignEditor

# Create a CampaignEditor instance
editor = CampaignEditor()

# Show the window
editor.show()
```

## How the Code Works

The code implements a GUI for managing and preparing AliExpress campaigns within the `hypotez` project. The `CampaignEditor` class provides the main UI elements for loading campaign configuration files, editing campaign details, and triggering the campaign preparation process. The `AliCampaignEditor` class handles the actual campaign preparation logic and interacts with the underlying AliExpress API.