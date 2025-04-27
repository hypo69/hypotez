# Experimenting with Google Sheets
## Overview

This module demonstrates an experiment in using Google Sheets to manage AliExpress campaign data. The code primarily focuses on retrieving campaign data from an `AliCampaignEditor` object, updating category information through a Google Sheet, and then reapplying the updated data back to the `AliCampaignEditor`.

## Details
This experiment is designed to explore how Google Sheets can be utilized as an interface for managing campaign data. It involves the following steps:

1. **Retrieving Campaign Data:** The script starts by retrieving campaign data from an `AliCampaignEditor` object. This data includes campaign name, title, language, currency, and a list of categories.

2. **Category Management:** The script then converts the category data from a `SimpleNamespace` object to a dictionary and then to a list, suitable for working with Google Sheets.

3. **Updating Categories in Google Sheets:** The script uses the `AliCampaignGoogleSheet` class to interact with the Google Sheet and updates the category information. The script updates the title, description, tags, and products count of each category.

4. **Retrieving Updated Categories:** The script retrieves the updated category data from the Google Sheet.

5. **Applying Updated Data:** The script updates the `categories_dict` with the edited data, converts it back to a `SimpleNamespace` object, and then creates a dictionary containing the entire campaign data.

6. **Applying the Changes:** The script updates the `AliCampaignEditor` object with the edited campaign data, including the updated categories.

## Classes

### `AliCampaignEditor`

**Description**: This class represents an editor for managing AliExpress campaign data.

**Attributes**:
- `campaign_name` (str): The name of the campaign.
- `language` (str): The language of the campaign.
- `currency` (str): The currency of the campaign.
- `campaign` (SimpleNamespace): Represents the campaign data.

**Methods**:
- `get_category_products(category_name: str)`: Retrieves the products associated with a specific category.
- `update_campaign(campaign_data: dict)`: Updates the campaign data with the provided dictionary.

### `AliCampaignGoogleSheet`

**Description**: This class provides methods for interacting with the Google Sheet used to manage campaign data.

**Attributes**:
- `spreadsheet_id` (str): The ID of the Google Sheet spreadsheet.

**Methods**:
- `set_categories(categories: list[CategoryType])`: Sets the category data in the Google Sheet.
- `get_categories()`: Retrieves the category data from the Google Sheet.
- `set_category_products(category_name: str, products: list[ProductType])`: Sets the products for a specific category in the Google Sheet.


## Functions

### `main()`

**Purpose**: This function demonstrates the process of updating campaign data through a Google Sheet.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:
1. Initializes an `AliCampaignGoogleSheet` object with the spreadsheet ID.
2. Defines the campaign name, language, and currency.
3. Creates an `AliCampaignEditor` object for the specified campaign.
4. Retrieves the campaign data from the editor and converts the categories to a dictionary.
5. Updates the categories in the Google Sheet using `gs.set_categories`.
6. Retrieves the updated categories from the Google Sheet using `gs.get_categories`.
7. Updates the `categories_dict` with the edited data and converts it back to a `SimpleNamespace` object.
8. Updates the campaign data with the edited categories.
9. Updates the `AliCampaignEditor` object with the updated campaign data.

**Examples**:

```python
if __name__ == '__main__':
    main()
```

## Parameter Details

- `categories_dict`: A dictionary containing the categories of the campaign. Each key is the name of the category, and the value is a `CategoryType` object.
- `categories_list`: A list of `CategoryType` objects representing the categories of the campaign.
- `edited_categories`: A list of dictionaries containing the updated category data from the Google Sheet.
- `_cat_ns`: A `SimpleNamespace` object used to store the updated category data retrieved from the Google Sheet.
- `products`: A list of `ProductType` objects representing the products associated with a category.
- `campaign_dict`: A dictionary containing the campaign data, including the updated categories.
- `edited_campaign`: A `SimpleNamespace` object containing the edited campaign data.

## Examples
```python
gs = AliCampaignGoogleSheet('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')
campaign_name = "lighting"
language = 'EN'
currency = 'USD'
campaign_editor = AliCampaignEditor(campaign_name, language, currency)
campaign_data = campaign_editor.campaign
_categories: SimpleNamespace = campaign_data.category
categories_dict: dict[str, CategoryType] = {category_name: getattr(_categories, category_name) for category_name in vars(_categories)}
categories_list: list[CategoryType] = list(categories_dict.values())
gs.set_categories(categories_list)
edited_categories: list[dict] = gs.get_categories()
for _cat in edited_categories:
    _cat_ns: SimpleNamespace = SimpleNamespace(**{
        'name':_cat['name'],
        'title':_cat['title'],
        'description':_cat['description'],
        'tags':_cat['tags'],
        'products_count':_cat['products_count']
    })
    logger.info(f"Updating category: {_cat_ns.name}")
    categories_dict[_cat_ns.name] = _cat_ns
    products = campaign_editor.get_category_products(_cat_ns.name)
    gs.set_category_products(_cat_ns.name,products)
_updated_categories = SimpleNamespace(**categories_dict)
campaign_dict: dict = {
    'name': campaign_data.campaign_name,
    'title': campaign_data.title,
    'language': language,
    'currency': currency,
    'category': _updated_categories
}
edited_campaign: SimpleNamespace = SimpleNamespace(**campaign_dict)
pprint(edited_campaign)
campaign_editor.update_campaign(edited_campaign)
```