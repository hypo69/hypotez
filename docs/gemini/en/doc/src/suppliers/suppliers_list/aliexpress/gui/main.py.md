#  Module `src.suppliers.aliexpress.gui.main`
##  Overview
This module provides the main window interface (`MainApp`) for managing advertising campaigns on AliExpress. It uses PyQt6 to create a user-friendly interface with multiple tabs for different functionalities:

- **JSON Editor:** Allows editing and saving JSON files representing campaign data.
- **Campaign Editor:** Provides a dedicated editor for managing campaigns.
- **Product Editor:** Offers tools to edit and manage product information.

##  Details
The `MainApp` class is responsible for creating and managing the main window of the application. It includes tabs for different functionalities related to managing AliExpress campaigns. This module acts as a central hub for interacting with the different components involved in managing campaign data.

## Classes

### `class MainApp`
**Description**: 
Main application window with tabs for various functionalities related to AliExpress campaigns.

**Inherits**:
- `QtWidgets.QMainWindow`: Base class for main application windows.

**Attributes**:
- `tab_widget` (`QtWidgets.QTabWidget`): Tab widget to hold different tabs.
- `promotion_app` (`CampaignEditor`): Instance of the `CampaignEditor` class for the JSON Editor tab.
- `campaign_editor_app` (`CategoryEditor`): Instance of the `CategoryEditor` class for the Campaign Editor tab.
- `product_editor_app` (`ProductEditor`): Instance of the `ProductEditor` class for the Product Editor tab.

**Methods**:
- `__init__()`: Initializes the main application window, sets up tabs for different functionalities, and creates the menu bar.
- `create_menubar()`: Creates the menu bar with options for opening, saving, exiting, copying, pasting, and opening product files.
- `open_file()`: Opens a file dialog to select and load a JSON file.
- `save_file()`: Saves the current file based on the selected tab.
- `exit_application()`: Exits the application.
- `copy()`: Copies selected text to the clipboard.
- `paste()`: Pastes text from the clipboard.
- `load_file(campaign_file)`: Loads the JSON file and displays its content in the JSON Editor.

### `class CampaignEditor`
**Description**:
Campaign editor for managing AliExpress campaign data.

**Inherits**: 
- `QtWidgets.QWidget`: Base class for GUI widgets.

**Attributes**:
- `parent` (`QtWidgets.QWidget`): Parent widget.
- `main_app` (`MainApp`): Main application window instance.

**Methods**:
- `__init__(parent: QtWidgets.QWidget, main_app: MainApp)`: Initializes the `CampaignEditor` instance.
- `save_changes()`: Saves changes made to the campaign data.
- `load_file(campaign_file)`: Loads campaign data from a JSON file.

### `class CategoryEditor`
**Description**:
Editor for managing categories for AliExpress campaigns.

**Inherits**:
- `QtWidgets.QWidget`: Base class for GUI widgets.

**Attributes**:
- `parent` (`QtWidgets.QWidget`): Parent widget.
- `main_app` (`MainApp`): Main application window instance.

**Methods**:
- `__init__(parent: QtWidgets.QWidget, main_app: MainApp)`: Initializes the `CategoryEditor` instance.

### `class ProductEditor`
**Description**:
Editor for managing product information for AliExpress campaigns.

**Inherits**:
- `QtWidgets.QWidget`: Base class for GUI widgets.

**Attributes**:
- `parent` (`QtWidgets.QWidget`): Parent widget.
- `main_app` (`MainApp`): Main application window instance.

**Methods**:
- `__init__(parent: QtWidgets.QWidget, main_app: MainApp)`: Initializes the `ProductEditor` instance.
- `open_file()`: Opens a file dialog to select a product file.
- `save_product()`: Saves changes made to product information.

## Functions

### `def main()`:
**Purpose**: Initializes and runs the main application.

**Parameters**: 
- None.

**Returns**: 
- None.

**Raises Exceptions**: 
- None.

**How the Function Works**:
- Creates a `QApplication` object.
- Creates an event loop (`QEventLoop`) for asynchronous operations.
- Initializes the main application window (`MainApp`).
- Shows the main window.
- Runs the event loop using `loop.run_forever()`.

**Examples**:
```python
# Example of running the application:
if __name__ == "__main__":
    main()
```

## Parameter Details

- `campaign_file` (`str`): Path to the JSON file representing campaign data.

## Examples

```python
# Example of opening a JSON file:
main_app.open_file()

# Example of saving campaign data:
main_app.save_file()

# Example of copying text to the clipboard:
main_app.copy()

# Example of pasting text from the clipboard:
main_app.paste()
```

## Inner Functions

- None.