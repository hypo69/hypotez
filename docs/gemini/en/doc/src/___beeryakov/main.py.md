# Module: `src.___beeryakov`

## Overview

This module is responsible for extracting data from the KSP website and populating a Google Sheet with the extracted information.

## Details

This module defines a function `run()` that acts as the main entry point for data extraction and processing. It utilizes the `ksp` module from `src.beeryakov.suppliers` to access and parse data from the KSP website and the `GSpreadsheet` and `GWorksheet` classes from `GSpreadsheet` to interact with a Google Sheet.

## Functions

### `run()`

**Purpose**: This function acts as the main entry point for the data extraction process. It fetches data from the KSP website, organizes it, and uploads the data to a Google Sheet.

**How the Function Works**:

1.  **Initialization**: The function starts by defining the Google Sheet ID (`sh_id`) and the KSP website root URL (`root`). It then opens a web browser (`d.get(root)`) and retrieves a dictionary (`worlds_dic`) of world URLs and corresponding worksheet titles from the KSP website.
2.  **Looping Through Worlds**: The function iterates through the `worlds_dic`, processing each world individually. For each world, it extracts data using the `ksp` module.
3.  **Creating Worksheets**: The function creates or retrieves a Google Sheet worksheet (`ws`) for each world. It sets a header row for the worksheet and then extracts categories, brands, and quantities for each world.
4.  **Data Extraction**: It navigates to the world URL and extracts the list of categories for each world.
5.  **Appending Data to the Sheet**: The function appends data to the Google Sheet worksheet, including category, brand, and quantity information.

**Examples**:

```python
# Example of function call
run()
```

## Inner Functions

This function doesn't have any inner functions. 


### `get_all_spreadsheets()`

**Purpose**: This function retrieves all spreadsheets for the current Google account. 

**Parameters**:

-   None.

**Returns**:

-   None.

**Raises**:

-   None.

**How the Function Works**:

The function uses the `gsh` object (an instance of the `GSpreadsheet` class) to fetch a list of all spreadsheets accessible to the current Google account.

**Examples**:

```python
# Example of function call
get_all_spreadsheets()
```

## Parameter Details

-   `sh_id` (`str`):  This variable represents the ID of the Google Sheet that will be used to store the extracted data.

-   `root` (`str`): This variable stores the base URL of the KSP website, which is used as the starting point for data extraction.

-   `worlds_dic` (`dict`): This dictionary contains key-value pairs where the key is a URL for a world on the KSP website and the value is a corresponding title for a worksheet in the Google Sheet.

-   `url` (`str`):  This variable represents the current URL being processed by the function.

-   `ws_title` (`str`): This variable represents the title of the worksheet within the Google Sheet.

-   `ws` (`GWorksheet`):  This object represents the worksheet associated with the current world being processed.

-   `category_title` (`str`):  This variable represents the title of a specific category on the KSP website.

-   `brand` (`str`):  This variable represents a brand name found on the KSP website.

-   `qty` (`int`): This variable represents the quantity associated with a specific brand.

-   `i` (`int`): This variable acts as a counter during data iteration.

-   `gspreadsheets` (`list`):  This list contains all the spreadsheets available to the current Google account.

## Examples

```python
# Example of calling the `run` function
run()

# Example of calling the `get_all_spreadsheets` function
get_all_spreadsheets()
```

## Class Details

This module doesn't define any classes.

## Summary

This module is responsible for extracting data from the KSP website and populating a Google Sheet with this data. It uses web scraping techniques and Google Sheet API interactions to accomplish this.