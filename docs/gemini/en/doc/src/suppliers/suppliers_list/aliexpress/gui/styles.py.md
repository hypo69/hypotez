# Module: `src.suppliers.aliexpress.gui.styles`

## Overview

This module provides common styling functions for UI elements within the AliExpress supplier list GUI. It offers functions to set fixed sizes for widgets. 

## Details

This module is used within the context of the AliExpress supplier list GUI. Its purpose is to provide a set of functions that can be used to style UI elements consistently across different parts of the application. This helps ensure a unified visual appearance and improves the user experience. 

## Functions

### `set_fixed_size`

**Purpose**: Sets a fixed size for a given widget.

**Parameters**:
- `widget` (`QtWidgets.QWidget`): The widget to which the fixed size should be applied.
- `width` (`int`): The desired width of the widget.
- `height` (`int`): The desired height of the widget.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:
The function utilizes the `setFixedSize` method of the `QtWidgets.QWidget` class to apply the specified width and height to the provided widget. This prevents the widget from being resized by the user or by the layout manager.

**Examples**:
```python
from PyQt6 import QtWidgets

# Creating a button widget
button = QtWidgets.QPushButton("Click Me")

# Setting a fixed size for the button
set_fixed_size(button, 100, 30)

# Displaying the button
button.show()
```