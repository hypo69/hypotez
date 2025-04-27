# Facebook Groups Widget

## Overview

This module provides the `FacebookGroupsWidget` class for creating a dropdown list of Facebook group URLs from a provided JSON file. 

## Details

This module is used for creating a user-friendly interface within the `hypotez` project, specifically for handling Facebook advertising campaigns. 

The `FacebookGroupsWidget` class allows users to select specific Facebook groups from a dropdown list, enabling the targeting of these groups with advertisements. 

The data for the groups is loaded from a JSON file, making it easy to update the list of available groups. 

## Classes

### `FacebookGroupsWidget`

**Description**:  This class creates a dropdown list of Facebook groups based on data from a JSON file.

**Inherits**: 

**Attributes**:
- `groups_data (SimpleNamespace)`: A namespace object containing data about Facebook groups from the provided JSON file.

**Methods**:

- `__init__(self, json_file_path: Path)`: Initializes the widget with a dropdown list of Facebook groups based on the provided JSON file. 
- `create_dropdown(self) -> Dropdown`: Creates and returns a dropdown widget with the group URLs. 
- `display_widget(self)`: Displays the dropdown widget.

## Functions

### `j_loads_ns`

**Purpose**: Loads a JSON file and returns a `SimpleNamespace` object, which provides a more convenient way to access data using dot notation.

**Parameters**: 
- `json_file_path (Path)`: The path to the JSON file.

**Returns**: 
- `SimpleNamespace`: A namespace object with data loaded from the JSON file.

**Example**: 
```python
from pathlib import Path
from src.utils.jjson import j_loads_ns

json_file_path = Path('groups.json')
groups_data = j_loads_ns(json_file_path)

print(groups_data.group1)  # Accessing the data using dot notation. 
```

## Parameter Details
- `json_file_path (Path)`:  The path to the JSON file containing data about Facebook groups. The format of the JSON file is expected to have group URLs as keys and their corresponding information as values. For example: 

```json
{
  "https://www.facebook.com/groups/1234567890/": {
    "group_name": "Example Group",
    "description": "This is a description of the group",
    "members": 1000
  },
  "https://www.facebook.com/groups/9876543210/": {
    "group_name": "Another Group",
    "description": "Another group description",
    "members": 500
  }
}
```

## Examples

```python
from pathlib import Path
from src.endpoints.advertisement.facebook.facebook_groups_widgets import FacebookGroupsWidget

json_file_path = Path('groups.json')  # Path to the JSON file
widget = FacebookGroupsWidget(json_file_path) 

# Display the widget
widget.display_widget() 

# Accessing the selected group URL
selected_group_url = widget.dropdown.value  
```

## Your Behavior During Code Analysis:

- Inside the code, you might encounter expressions between `<` `>`. For example: `<instruction for gemini model:Loading product descriptions into PrestaShop.>, <next, if available>. These are placeholders where you insert the relevant value.
- Always refer to the system instructions for processing code in the `hypotez` project (the first set of instructions you translated);
- Analyze the file's location within the project. This helps understand its purpose and relationship with other files. You will find the file location in the very first line of code starting with `## \\file /...`;
- Memorize the provided code and analyze its connection with other parts of the project;
- In these instructions, do not suggest code improvements. Strictly follow point 5. **Example File** when composing the response.