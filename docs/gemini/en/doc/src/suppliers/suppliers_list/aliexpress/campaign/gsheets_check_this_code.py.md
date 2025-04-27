# AliCampaignGoogleSheet

## Overview

This module implements the `AliCampaignGoogleSheet` class, which manages Google Sheets for AliExpress campaign data. It inherits from the `SpreadSheet` class and provides additional methods for managing Google Sheets, recording category and product data, and formatting sheets.

## Details

The `AliCampaignGoogleSheet` class uses the `gspread` library to interact with Google Sheets. It provides methods for:

- **Deleting product sheets:** Deleting all sheets except 'categories' and 'product_template'.
- **Setting campaign data:** Writing campaign data to a Google Sheets worksheet.
- **Setting product data:** Writing product data from a list of `SimpleNamespace` objects to Google Sheets cells.
- **Setting category data:** Writing category data from a `SimpleNamespace` object to Google Sheets cells.
- **Formatting sheets:** Applying formatting to the 'categories' and product sheets, including column width, row height, and header formatting.

## Classes

### `AliCampaignGoogleSheet`

**Description**: Класс для работы с Google Sheets в рамках кампаний AliExpress.

**Inherits**: `SpreadSheet`

**Attributes**:

- `spreadsheet_id` (`str`): Google Sheets spreadsheet ID.
- `spreadsheet` (`SpreadSheet`): Instance of `SpreadSheet` class.
- `worksheet` (`Worksheet`): Google Sheets worksheet.
- `driver` (`Driver`): Instance of `Driver` class for interacting with the browser (Chrome by default).
- `editor` (`AliCampaignEditor`): Instance of `AliCampaignEditor` class for managing campaign data.


**Methods**:

### `__init__(self, campaign_name: str, language: str | dict = None, currency: str = None)`

**Purpose**: Инициализирует `AliCampaignGoogleSheet` с указанным Google Sheets spreadsheet ID и дополнительными параметрами.

**Parameters**:

- `campaign_name` (`str`): The name of the campaign.
- `language` (`str` | `dict`, optional): The language for the campaign. Defaults to `None`.
- `currency` (`str`, optional): The currency for the campaign. Defaults to `None`.

**Returns**:
- `None`

### `clear(self)`

**Purpose**: Очищает содержимое.

**Description**: Удаляет листы продуктов и очищает данные на листах категорий и других указанных листах.

**Parameters**:

- `None`

**Returns**:

- `None`

### `delete_products_worksheets(self)`

**Purpose**: Удаляет все листы из Google Sheets, кроме 'categories' и 'product_template'.

**Parameters**:

- `None`

**Returns**:

- `None`

**Raises Exceptions**:

- `Exception`: If an error occurs during the process.

### `set_campaign_worksheet(self, campaign: SimpleNamespace)`

**Purpose**: Записывает данные кампании в лист Google Sheets.

**Parameters**:

- `campaign` (`SimpleNamespace` | `str`): `SimpleNamespace` object with campaign data fields for writing.

**Returns**:

- `None`

**Raises Exceptions**:

- `Exception`: If an error occurs during the process.

### `set_products_worksheet(self, category_name: str)`

**Purpose**: Записывает данные из списка объектов `SimpleNamespace` в ячейки Google Sheets.

**Parameters**:

- `category_name` (`str`): The name of the category to fetch products from.

**Returns**:

- `None`

**Raises Exceptions**:

- `Exception`: If an error occurs during the process.

### `set_categories_worksheet(self, categories: SimpleNamespace)`

**Purpose**: Записывает данные из объекта `SimpleNamespace` с категориями в ячейки Google Sheets.

**Parameters**:

- `categories` (`SimpleNamespace`): Object with category data for writing.

**Returns**:

- `None`

**Raises Exceptions**:

- `Exception`: If an error occurs during the process.

### `get_categories(self)`

**Purpose**: Получение данных из таблицы Google Sheets.

**Parameters**:

- `None`

**Returns**:

- `list[dict]`: Данные из таблицы в виде списка словарей.

### `set_category_products(self, category_name: str, products: dict)`

**Purpose**: Запись данных о продуктах в новую таблицу Google Sheets.

**Parameters**:

- `category_name` (`str`): The name of the category.
- `products` (`dict`): Dictionary with product data.

**Returns**:

- `None`

**Raises Exceptions**:

- `Exception`: If an error occurs during the process.

### `_format_categories_worksheet(self, ws: Worksheet)`

**Purpose**: Форматирование листа 'categories'.

**Parameters**:

- `ws` (`Worksheet`): Google Sheets worksheet for formatting.

**Returns**:

- `None`

**Raises Exceptions**:

- `Exception`: If an error occurs during the process.

### `_format_category_products_worksheet(self, ws: Worksheet)`

**Purpose**: Форматирование листа с продуктами категории.

**Parameters**:

- `ws` (`Worksheet`): Google Sheets worksheet for formatting.

**Returns**:

- `None`

**Raises Exceptions**:

- `Exception`: If an error occurs during the process.

## Inner Functions

- None.

## How the Class Works

The `AliCampaignGoogleSheet` class uses the `SpreadSheet` class to interact with Google Sheets. It provides additional methods for managing AliExpress campaign data, specifically:

- **Deleting product sheets:** The `delete_products_worksheets` method iterates over all worksheets in the spreadsheet and deletes any sheets that are not 'categories' or 'product_template'.
- **Setting campaign data:** The `set_campaign_worksheet` method writes the campaign data to a new worksheet called 'campaign'.
- **Setting product data:** The `set_products_worksheet` method iterates over the products in the specified category and writes the data to a new worksheet called 'product'.
- **Setting category data:** The `set_categories_worksheet` method writes the category data to a new worksheet called 'categories'.
- **Formatting sheets:** The `_format_categories_worksheet` and `_format_category_products_worksheet` methods apply formatting to the 'categories' and product sheets, respectively, including column width, row height, and header formatting.

## Examples

### Creating an Instance of `AliCampaignGoogleSheet`

```python
# Importing the required classes and modules
from src.suppliers.suppliers_list.aliexpress.campaign.gsheets_check_this_code import AliCampaignGoogleSheet

# Creating an instance of AliCampaignGoogleSheet with the specified campaign name, language, and currency
campaign_sheet = AliCampaignGoogleSheet(campaign_name='MyCampaign', language='ru', currency='RUB')
```

### Using the Class Methods

```python
# Using the clear method to delete product sheets and clear data on other sheets
campaign_sheet.clear()

# Using the set_campaign_worksheet method to write campaign data to the 'campaign' worksheet
campaign_sheet.set_campaign_worksheet(campaign_data)

# Using the set_products_worksheet method to write product data to the 'product' worksheet for a specific category
campaign_sheet.set_products_worksheet(category_name='Electronics')

# Using the set_categories_worksheet method to write category data to the 'categories' worksheet
campaign_sheet.set_categories_worksheet(categories_data)

# Getting data from the 'categories' worksheet
categories_data = campaign_sheet.get_categories()

# Setting product data for a specific category
campaign_sheet.set_category_products(category_name='Electronics', products=product_data)
```

### Using the `driver` attribute for interacting with the browser

```python
# Accessing the driver attribute for interacting with the browser
driver = campaign_sheet.driver

# Example: Using the execute_locator method to get the value of a web element
locator = {
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

result = driver.execute_locator(locator)
```

## Parameter Details

- `campaign_name` (`str`): The name of the campaign.
- `language` (`str` | `dict`, optional): The language for the campaign. Defaults to `None`.
- `currency` (`str`, optional): The currency for the campaign. Defaults to `None`.
- `category_name` (`str`): The name of the category to fetch products from.
- `categories` (`SimpleNamespace`): Object with category data for writing.
- `products` (`dict`): Dictionary with product data.
- `ws` (`Worksheet`): Google Sheets worksheet for formatting.


## Examples

### Creating a `AliCampaignGoogleSheet` instance

```python
from src.suppliers.suppliers_list.aliexpress.campaign.gsheets_check_this_code import AliCampaignGoogleSheet

campaign_sheet = AliCampaignGoogleSheet(campaign_name='MyCampaign', language='ru', currency='RUB')
```

### Using `AliCampaignGoogleSheet` methods

```python
# Clearing existing data
campaign_sheet.clear()

# Setting campaign data
campaign_data = {
    'name': 'My Campaign',
    'title': 'Campaign Title',
    'language': 'ru',
    'currency': 'RUB',
    'description': 'Campaign description',
}
campaign_sheet.set_campaign_worksheet(campaign_data)

# Setting category data
categories_data = {
    'Electronics': {
        'name': 'Electronics',
        'title': 'Electronics Category',
        'description': 'Category Description',
        'tags': ['electronics', 'gadgets', 'tech'],
        'products_count': 10,
    },
    'Fashion': {
        'name': 'Fashion',
        'title': 'Fashion Category',
        'description': 'Category Description',
        'tags': ['fashion', 'clothing', 'accessories'],
        'products_count': 20,
    }
}
campaign_sheet.set_categories_worksheet(categories_data)

# Setting product data
product_data = [
    {
        'product_id': 1234567890,
        'product_title': 'Product Title',
        # ... other product data
    },
    # ... more products
]
campaign_sheet.set_category_products(category_name='Electronics', products=product_data)

# Getting category data
categories_data = campaign_sheet.get_categories()
```