# Edit AliExpress Campaign

## Overview

This module provides functionality for editing AliExpress campaigns. It utilizes the `AliCampaignEditor` class, which allows for modifying various aspects of an AliExpress campaign, including campaign name, locale, currency, and more.

## Details

The module utilizes the `AliCampaignEditor` class from the `src.suppliers.suppliers_list.aliexpress.campaign` module. This class provides methods for interacting with AliExpress campaigns and modifying their settings. 

## Classes

### `AliCampaignEditor`

**Description**: The `AliCampaignEditor` class is designed to manage and modify AliExpress campaign settings.

**Inherits**: `AliCampaignEditor` inherits from the `CampaignEditor` class, which provides basic campaign editing functionality.

**Attributes**:

- `campaign_name` (str): The name of the AliExpress campaign to be edited.
- `locale` (str): The locale for the campaign (e.g., 'EN', 'HE', 'RU').
- `currency` (str): The currency associated with the campaign (e.g., 'USD', 'ILS').

**Methods**:

- `__init__(self, campaign_name: str, locale: str, currency: str)`: Initializes the `AliCampaignEditor` object, setting the campaign name, locale, and currency.
- `get_campaign_id(self) -> int`: Retrieves the unique ID of the AliExpress campaign.
- `edit_campaign_name(self, new_name: str) -> None`: Modifies the name of the AliExpress campaign.
- `edit_locale(self, new_locale: str) -> None`: Changes the locale setting of the AliExpress campaign.
- `edit_currency(self, new_currency: str) -> None`: Updates the currency associated with the AliExpress campaign.
- `edit_bid(self, bid: float) -> None`: Sets the bid for the AliExpress campaign.
- `edit_budget(self, budget: float) -> None`: Modifies the daily budget of the AliExpress campaign.
- `edit_keywords(self, keywords: List[str]) -> None`: Updates the list of keywords for the AliExpress campaign.
- `edit_product_selection(self, product_ids: List[int]) -> None`: Selects specific products to include in the AliExpress campaign.
- `edit_targeting(self, targeting: dict) -> None`: Updates the targeting settings for the AliExpress campaign.
- `edit_optimization(self, optimization: dict) -> None`: Modifies the optimization settings for the AliExpress campaign.
- `edit_scheduling(self, scheduling: dict) -> None`: Changes the scheduling settings for the AliExpress campaign.
- `edit_creative(self, creative: dict) -> None`: Modifies the creative elements (e.g., images, videos) used in the AliExpress campaign.
- `edit_campaign_status(self, status: str) -> None`: Updates the status of the AliExpress campaign (e.g., 'enabled', 'paused', 'disabled').
- `save_campaign(self) -> None`: Saves all the changes made to the AliExpress campaign.

## Functions

### `process_campaign(campaign_name: str, locale: str, currency: str, campaign_data: dict) -> None`

**Purpose**: This function processes a specific AliExpress campaign, extracting and processing its data.

**Parameters**:

- `campaign_name` (str): The name of the AliExpress campaign to be processed.
- `locale` (str): The locale for the campaign (e.g., 'EN', 'HE', 'RU').
- `currency` (str): The currency associated with the campaign (e.g., 'USD', 'ILS').
- `campaign_data` (dict): A dictionary containing the raw data of the AliExpress campaign.

**Returns**:

- `None`: This function does not return a value. It processes the campaign data directly.

**Raises Exceptions**:

- `Exception`: If there are errors in processing the campaign data.

**How the Function Works**:

- The function initializes an instance of the `AliCampaignEditor` class using the provided campaign name, locale, and currency.
- It extracts the campaign data from the `campaign_data` dictionary.
- It processes the campaign data, potentially extracting relevant information, performing calculations, or making modifications.
- The function uses the `AliCampaignEditor` methods to interact with and update the AliExpress campaign.

**Examples**:

```python
campaign_name = "030724_men_summer_fashion"
locale = 'EN'
currency = 'USD'
campaign_data = { ... }

process_campaign(campaign_name, locale, currency, campaign_data)
```

### `process_campaign_category(category_name: str, locale: str, currency: str, campaign_data: dict) -> None`

**Purpose**: This function processes a specific category within an AliExpress campaign, extracting and processing its data.

**Parameters**:

- `category_name` (str): The name of the category within the AliExpress campaign to be processed.
- `locale` (str): The locale for the campaign (e.g., 'EN', 'HE', 'RU').
- `currency` (str): The currency associated with the campaign (e.g., 'USD', 'ILS').
- `campaign_data` (dict): A dictionary containing the raw data of the AliExpress campaign.

**Returns**:

- `None`: This function does not return a value. It processes the category data directly.

**Raises Exceptions**:

- `Exception`: If there are errors in processing the category data.

**How the Function Works**:

- The function initializes an instance of the `AliCampaignEditor` class using the provided campaign name, locale, and currency.
- It extracts the category data from the `campaign_data` dictionary based on the provided `category_name`.
- It processes the category data, potentially extracting relevant information, performing calculations, or making modifications.
- The function uses the `AliCampaignEditor` methods to interact with and update the AliExpress campaign, specifically targeting the specified category.

**Examples**:

```python
category_name = "men_summer_tshirts"
locale = 'EN'
currency = 'USD'
campaign_data = { ... }

process_campaign_category(category_name, locale, currency, campaign_data)
```

### `process_all_campaigns(locale: str, currency: str, campaign_data: dict) -> None`

**Purpose**: This function processes all AliExpress campaigns from the provided data, extracting and processing each campaign.

**Parameters**:

- `locale` (str): The locale for the campaigns (e.g., 'EN', 'HE', 'RU').
- `currency` (str): The currency associated with the campaigns (e.g., 'USD', 'ILS').
- `campaign_data` (dict): A dictionary containing the raw data of multiple AliExpress campaigns.

**Returns**:

- `None`: This function does not return a value. It processes all campaigns directly.

**Raises Exceptions**:

- `Exception`: If there are errors in processing any of the campaigns.

**How the Function Works**:

- The function iterates through the `campaign_data` dictionary, processing each campaign individually.
- For each campaign, it extracts the campaign name and uses the `process_campaign` function to process the specific campaign.
- This approach allows for efficient batch processing of multiple AliExpress campaigns.

**Examples**:

```python
locale = 'EN'
currency = 'USD'
campaign_data = { ... }

process_all_campaigns(locale, currency, campaign_data)
```

## Parameter Details

- `campaign_name` (str): The name of the AliExpress campaign to be edited or processed.
- `locale` (str): The locale for the campaign (e.g., 'EN', 'HE', 'RU').
- `currency` (str): The currency associated with the campaign (e.g., 'USD', 'ILS').
- `campaign_data` (dict): A dictionary containing the raw data of an AliExpress campaign or a collection of campaigns.
- `category_name` (str): The name of a specific category within the campaign.
- `bid` (float): The bid amount for the campaign.
- `budget` (float): The daily budget for the campaign.
- `keywords` (List[str]): A list of keywords used in the campaign.
- `product_ids` (List[int]): A list of product IDs included in the campaign.
- `targeting` (dict): A dictionary representing the campaign's targeting settings.
- `optimization` (dict): A dictionary representing the campaign's optimization settings.
- `scheduling` (dict): A dictionary representing the campaign's scheduling settings.
- `creative` (dict): A dictionary representing the campaign's creative elements.
- `status` (str): The current status of the campaign (e.g., 'enabled', 'paused', 'disabled').

## Examples

```python
# Creating an instance of the AliCampaignEditor
campaign_editor = AliCampaignEditor(campaign_name="building_bricks", locale="EN", currency="USD")

# Editing the campaign name
campaign_editor.edit_campaign_name(new_name="building_bricks_updated")

# Setting the bid for the campaign
campaign_editor.edit_bid(bid=0.50)

# Updating the campaign's keywords
keywords = ["building bricks", "lego blocks", "construction toys"]
campaign_editor.edit_keywords(keywords=keywords)

# Saving the changes to the campaign
campaign_editor.save_campaign()
```

```python
# Processing a single campaign
campaign_name = "building_bricks"
locale = "EN"
currency = "USD"
campaign_data = { ... } # This dictionary should contain the raw data of the campaign

process_campaign(campaign_name, locale, currency, campaign_data)

# Processing a category within a campaign
category_name = "building_bricks"
locale = "EN"
currency = "USD"
campaign_data = { ... } # This dictionary should contain the raw data of the campaign

process_campaign_category(category_name, locale, currency, campaign_data)

# Processing all campaigns from the provided data
locale = "EN"
currency = "USD"
campaign_data = { ... } # This dictionary should contain the raw data of all campaigns

process_all_campaigns(locale, currency, campaign_data)
```