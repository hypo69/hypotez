# Module: Context Menu Manager

## Overview

This module implements a simple GUI application (`ContextMenuManager`) for managing a custom context menu item named "hypo AI assistant" that appears when right-clicking on the background of desktop and folders in Windows Explorer. It uses the Windows Registry to add and remove this menu item, and it allows users to easily control its presence in the context menu.

## Details

This module aims to provide a convenient way to integrate "hypo AI assistant" into the Windows Explorer context menu, allowing users to quickly access its functionality through a right-click menu. 

This is achieved by modifying the Windows Registry using the `winreg` module. The registry key `Directory\\Background\\shell\\hypo_AI_assistant` is used to define the custom context menu item. When selected, it executes a Python script (`gui\\context_menu\\main.py`) defined in the `command` subkey of the registry key. The script path is dynamically determined using the `gs.path.src` module.

The application provides a simple GUI interface with three buttons: "Add", "Remove", and "Exit". 

## Classes

### `ContextMenuManager`

**Description**: Main application window for managing the custom context menu item.

**Inherits**: `QtWidgets.QWidget`

**Attributes**: 

 - None.

**Methods**:

 - **`__init__`**: Initializes the class, calling `initUI()` to set up the user interface.
 - **`initUI`**: Creates and arranges the GUI elements:
    - Sets the window title to "Управление контекстным меню".
    - Creates a vertical layout (`QVBoxLayout`) for organizing buttons.
    - Adds three buttons:
        - "Добавить пункт меню" (Add context menu item): Connects to the `add_context_menu_item` function.
        - "Удалить пункт меню" (Remove context menu item): Connects to the `remove_context_menu_item` function.
        - "Выход" (Exit): Connects to the `close` method to close the window.
    - Applies the layout to the main window.

## Functions

### `add_context_menu_item`

**Purpose**: Adds a context menu item to the desktop and folder background.

**Parameters**: None.

**Returns**: None.

**Raises Exceptions**: 
 - Displays an error message using `QtWidgets.QMessageBox` if the script file (`gui\\context_menu\\main.py`) cannot be found. 

**How the Function Works**:
 - Creates a new registry key under `HKEY_CLASSES_ROOT\\Directory\\Background\\shell\\hypo_AI_assistant`.
 - Sets the display name of the context menu item to "hypo AI assistant" using `reg.SetValue(key, "", reg.REG_SZ, "hypo AI assistant")`.
 - Creates a sub-key (`command`) within the main key to define the command to execute when the menu item is selected.
 - Sets the command value to `python "\\"{command_path}\\" "%1\\""`, where `command_path` points to the Python script (`gui\\context_menu\\main.py`).
 - Displays a success message using `QtWidgets.QMessageBox` if the operation is successful.

### `remove_context_menu_item`

**Purpose**: Removes the "hypo AI assistant" context menu item.

**Parameters**: None.

**Returns**: None.

**Raises Exceptions**: 
 - Displays a warning message using `QtWidgets.QMessageBox` if the context menu item does not exist.
 - Displays an error message using `QtWidgets.QMessageBox` if the key deletion operation fails.

**How the Function Works**:
 - Attempts to delete the registry key `Directory\\Background\\shell\\hypo_AI_assistant` using `reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key_path)`.
 - Displays a success message using `QtWidgets.QMessageBox` if the item is removed successfully.

## Examples

### Example: Managing Context Menu Items

```python
# Create an instance of the ContextMenuManager
window = ContextMenuManager()
window.show()

# This will display the application window with buttons for adding, removing, and exiting.

# To add the "hypo AI assistant" context menu item:
add_context_menu_item()

# To remove the "hypo AI assistant" context menu item:
remove_context_menu_item()

# To close the application window:
window.close()
```

### Example: Registry Key Structure

The registry key structure created by `add_context_menu_item` is as follows:

```
HKEY_CLASSES_ROOT
    Directory
        Background
            shell
                hypo_AI_assistant
                    (Default) = "hypo AI assistant"
                    command
                        (Default) = "python "\\"{command_path}\\" "%1\\"" 
```

## Parameter Details

 - **`command_path`**: The path to the Python script to be executed when the context menu item is selected. This path is determined dynamically using the `gs.path.src` module. 

## Your Behavior During Code Analysis:

- Always refer to the system instructions for processing code in the `hypotez` project;
- Analyze the file's location within the project: `/src/gui/context_menu/qt6/main.py`;
- Memorize the provided code and analyze its connection with other parts of the project.