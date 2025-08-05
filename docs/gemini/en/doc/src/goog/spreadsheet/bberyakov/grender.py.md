# Module: src.goog.spreadsheet.bberyakov.grender

## Overview

This module provides functionality for rendering Google Spreadsheet data. The `GSRender` class offers various methods for formatting and manipulating spreadsheet worksheets, including setting headers, merging cells, and writing category titles. 

## Details

This module utilizes the `gspread` and `spread_formatting` libraries to interact with Google Spreadsheets. It leverages helper functions from the `src.helpers` module for logging, error handling, and color manipulation. The `GSRender` class is designed to simplify the process of rendering and styling Google Spreadsheets.

## Classes

### `GSRender`

**Description**:  Class for rendering and styling Google Spreadsheet data.

**Attributes**:

- `render_schemas` (dict): A dictionary containing rendering schemas.

**Methods**:

- `__init__(self, *args, **kwargs) -> None`: Initializes the `GSRender` object, loading rendering schemas from a JSON file.

- `render_header(self, ws: Worksheet, world_title: str, range: str = 'A1:Z1', merge_type: str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS') = 'MERGE_ALL') -> None`: Renders the header of the spreadsheet within the specified range of cells.

- `merge_range(self, ws: Worksheet, range: str, merge_type: str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS') =  'MERGE_ALL') -> None`: Merges cells within the specified range.

- `set_worksheet_direction(self, sh: Spreadsheet, ws: Worksheet, direction: str ('ltr') | str ('rtl') = 'rtl' )`: Sets the text direction (left-to-right or right-to-left) for the worksheet.

- `header(self, ws: Worksheet, ws_header: str | list, row: int = None)`: Adds a header row to the spreadsheet with the specified text.

- `write_category_title(self, ws: Worksheet, ws_category_title: str | list, row: int = None)`: Writes a category title to the spreadsheet.

- `get_first_empty_row(self, ws: Worksheet, by_col: int = None) -> int`: Returns the index of the first empty row in the spreadsheet.

## Functions

### `hex_to_rgb(hex_color: str) -> tuple[int, int, int]`:

**Purpose**: Converts a hexadecimal color code to RGB values.

**Parameters**:

- `hex_color` (str): The hexadecimal color code (e.g., '#FFAAAA').

**Returns**:

- `tuple[int, int, int]`: A tuple containing the red, green, and blue values of the color.

### `decimal_color_to_hex(decimal_color: tuple[float, float, float]) -> str`:

**Purpose**: Converts decimal RGB values to a hexadecimal color code.

**Parameters**:

- `decimal_color` (tuple[float, float, float]): A tuple containing the decimal red, green, and blue values of the color (each value should be between 0 and 1).

**Returns**:

- `str`: The hexadecimal color code.

## Parameter Details

- `ws` (Worksheet): An instance of the `Worksheet` class from the `gspread` library, representing a sheet in the Google Spreadsheet.

- `sh` (Spreadsheet): An instance of the `Spreadsheet` class from the `gspread` library, representing the entire Google Spreadsheet.

- `world_title` (str): The title of the Google Spreadsheet.

- `range` (str): A string representing the range of cells to be formatted or manipulated (e.g., 'A1:Z1').

- `merge_type` (str): The type of merge to apply to cells. Possible values: 'MERGE_ALL', 'MERGE_COLUMNS', 'MERGE_ROWS'.

- `ws_header` (str | list): The header text to be added to the spreadsheet. Can be a single string or a list of strings.

- `ws_category_title` (str | list): The category title text to be added to the spreadsheet. Can be a single string or a list of strings.

- `row` (int): The row number to add the header or category title to.

- `by_col` (int): The column index for finding the first empty row. If `None`, uses the last filled column in the spreadsheet.

- `direction` (str): The text direction for the worksheet. Possible values: 'ltr', 'rtl'.

- `hex_color` (str): A hexadecimal color code.

- `decimal_color` (tuple[float, float, float]): A tuple containing the decimal red, green, and blue values of a color.

## Examples

```python
# Initialize the GSRender object
render = GSRender()

# Get a Google Spreadsheet
spreadsheet = gs.open_by_key('your_spreadsheet_key')

# Select a worksheet
worksheet = spreadsheet.worksheet('Sheet1')

# Render a header
render.render_header(worksheet, 'My Spreadsheet', 'A1:Z1', 'MERGE_ALL')

# Merge cells in a specific range
render.merge_range(worksheet, 'B2:D2', 'MERGE_COLUMNS')

# Set the worksheet direction to right-to-left
render.set_worksheet_direction(spreadsheet, worksheet, 'rtl')

# Add a header row
render.header(worksheet, 'Products', 2)

# Write a category title
render.write_category_title(worksheet, 'Electronics', 4)

# Get the index of the first empty row
first_empty_row = render.get_first_empty_row(worksheet)
```
```python
# Example of using hex_to_rgb
rgb_values = hex_to_rgb('#FFAAAA')
print(rgb_values)  # Output: (255, 170, 170)

# Example of using decimal_color_to_hex
hex_color = decimal_color_to_hex((0.5, 0.25, 0.75))
print(hex_color)  # Output: '#8040C0'