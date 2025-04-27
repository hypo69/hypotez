## Module:  src.suppliers.suppliers_list.aliexpress.campaign._experiments

### Overview

This module provides functionality for working with Google Sheets within the context of AliExpress campaigns. It demonstrates a quick way to access and manipulate data within a Google Sheet. The module uses the `gspread` library for interacting with Google Sheets.

### Details

This file demonstrates a basic workflow for handling AliExpress campaign data within a Google Sheet. It includes functions for:

- Defining campaign and category details.
- Creating a `gs` instance representing the campaign.
- Setting the `products_worksheet` for the specified category.
- Saving campaign information from the worksheet.

This module is a starting point for using Google Sheets as a data source for AliExpress campaigns. It can be extended to support more complex operations, such as:

- Importing product data from different sources.
- Automating updates to the Google Sheet based on campaign progress.
- Creating reports and visualizations from the data.

### Classes

This module does not define any custom classes. 

### Functions

####  `save_campaign_from_worksheet`

**Purpose**: This function saves campaign data from the specified Google Sheet worksheet.

**Parameters**:

- **None**:  This function does not take any parameters. 

**Returns**:

- **None**:  This function does not return any value.

**Raises Exceptions**:

- **None**:  This function does not raise any exceptions.

**How the Function Works**:

- The function retrieves data from the specified Google Sheet worksheet.
- It then processes this data and saves it to the campaign object.

**Examples**:

```python
gs.save_campaign_from_worksheet() 
```

####  `save_categories_from_worksheet`

**Purpose**:  This function saves categories from the specified Google Sheet worksheet.

**Parameters**:

- **save_category_names_to_file**: This parameter determines whether to save category names to a file. 

**Returns**:

- **None**:  This function does not return any value.

**Raises Exceptions**:

- **None**:  This function does not raise any exceptions.

**How the Function Works**:

- The function retrieves categories from the specified Google Sheet worksheet.
- It then processes these categories and saves them to the appropriate objects or files.

**Examples**:

```python
gs.save_categories_from_worksheet(False) 
```


####  `set_products_worksheet`

**Purpose**:  This function sets the specified worksheet as the `products_worksheet` for the campaign.

**Parameters**:

- **category_name**: The name of the category to set as the products worksheet. 

**Returns**:

- **None**:  This function does not return any value.

**Raises Exceptions**:

- **None**:  This function does not raise any exceptions.

**How the Function Works**:

- The function identifies the worksheet within the Google Sheet based on the provided `category_name`.
- It then assigns this worksheet as the `products_worksheet` for the campaign.

**Examples**:

```python
gs.set_products_worksheet(category_name)
```

### Parameter Details

#### `campaign_name` (str):

The name of the AliExpress campaign. This value is used to identify the specific campaign within the system.

#### `category_name` (str):

The name of the category within the AliExpress campaign. This value is used to identify the specific category within the campaign and to retrieve data related to that category.

#### `language` (str):

The language code for the AliExpress campaign. This value is used to specify the language in which product data is retrieved and displayed.

#### `currency` (str):

The currency code for the AliExpress campaign. This value is used to specify the currency in which prices are displayed.

#### `save_category_names_to_file` (bool):

This flag determines whether to save category names to a file. If `True`, the category names will be written to a file.

### Examples

This example demonstrates how to use the module to work with Google Sheets:

```python
campaign_name = "lighting"
category_name = "chandeliers"
language = 'EN'
currency = 'USD'

gs = AliCampaignGoogleSheet(campaign_name=campaign_name, language=language, currency=currency)

gs.set_products_worksheet(category_name)

#gs.save_categories_from_worksheet(False) 
gs.save_campaign_from_worksheet() 
```

This code:

1. **Defines campaign and category information**:  `campaign_name`, `category_name`, `language`, and `currency`.
2. **Creates a `gs` instance**:  This instance represents the AliExpress campaign and provides methods to interact with Google Sheets.
3. **Sets the `products_worksheet`**:  The `set_products_worksheet` method is called to assign the specified worksheet as the `products_worksheet` for the campaign.
4. **Saves campaign information**:  The `save_campaign_from_worksheet` method is called to retrieve and save campaign data from the worksheet.

### Additional Notes

- The code uses the `gspread` library to interact with Google Sheets. Ensure that this library is installed before running the code.
- This module demonstrates a basic usage of Google Sheets for AliExpress campaigns. You can extend it with more features and functionalities to fit your specific needs.