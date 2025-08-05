# Facebook Advertisement Endpoint

## Overview

This module contains the `Facebook` class, which is responsible for handling interactions with the Facebook advertising platform. It provides functions for creating, managing, and optimizing advertising campaigns on Facebook. 

## Classes

### `Facebook`

**Description**: This class represents a Facebook advertisement endpoint, providing methods for creating and managing Facebook ads.

**Inherits**: This class inherits from the base `AdvertisementEndpoint` class, providing a common interface for working with different advertising platforms.

**Attributes**: 

- `api_key` (str):  API key for accessing Facebook advertising API.
- `access_token` (str): Access token for authenticating with Facebook.
- `app_id` (str): Facebook application ID.
- `app_secret` (str): Facebook application secret.

**Methods**: 

- `create_campaign(campaign_data: dict) -> dict`:  Creates a new Facebook advertising campaign.
    - **Purpose**: This function sends a request to Facebook to create a new campaign based on the provided campaign data. 
    - **Parameters**:
        - `campaign_data` (dict): A dictionary containing the campaign data, such as name, budget, targeting, and objectives.
    - **Returns**: A dictionary containing the created campaign data. 
    - **Raises Exceptions**:
        - `FacebookAPIError`: If there is an error during the API call.
        - `InvalidArgumentError`: If the provided campaign data is invalid.

- `update_campaign(campaign_id: int, campaign_data: dict) -> dict`: Updates an existing Facebook advertising campaign.
    - **Purpose**: This function sends a request to Facebook to update the specified campaign with the provided campaign data. 
    - **Parameters**:
        - `campaign_id` (int): The ID of the campaign to update. 
        - `campaign_data` (dict): A dictionary containing the updated campaign data.
    - **Returns**: A dictionary containing the updated campaign data.
    - **Raises Exceptions**:
        - `FacebookAPIError`: If there is an error during the API call.
        - `InvalidArgumentError`: If the provided campaign data is invalid.

- `get_campaign(campaign_id: int) -> dict`: Retrieves the data for a specific Facebook advertising campaign.
    - **Purpose**: This function sends a request to Facebook to retrieve data for the specified campaign.
    - **Parameters**:
        - `campaign_id` (int): The ID of the campaign to retrieve.
    - **Returns**: A dictionary containing the campaign data.
    - **Raises Exceptions**:
        - `FacebookAPIError`: If there is an error during the API call.

- `delete_campaign(campaign_id: int) -> bool`: Deletes a specific Facebook advertising campaign.
    - **Purpose**: This function sends a request to Facebook to delete the specified campaign.
    - **Parameters**:
        - `campaign_id` (int): The ID of the campaign to delete.
    - **Returns**: True if the campaign was deleted successfully, False otherwise. 
    - **Raises Exceptions**:
        - `FacebookAPIError`: If there is an error during the API call.

- `create_ad_set(ad_set_data: dict) -> dict`: Creates a new ad set within a Facebook advertising campaign.
    - **Purpose**: This function sends a request to Facebook to create a new ad set within the specified campaign.
    - **Parameters**:
        - `ad_set_data` (dict): A dictionary containing the ad set data, such as budget, targeting, and scheduling.
    - **Returns**: A dictionary containing the created ad set data.
    - **Raises Exceptions**:
        - `FacebookAPIError`: If there is an error during the API call.
        - `InvalidArgumentError`: If the provided ad set data is invalid.

- `update_ad_set(ad_set_id: int, ad_set_data: dict) -> dict`: Updates an existing ad set within a Facebook advertising campaign.
    - **Purpose**: This function sends a request to Facebook to update the specified ad set with the provided ad set data.
    - **Parameters**:
        - `ad_set_id` (int): The ID of the ad set to update.
        - `ad_set_data` (dict): A dictionary containing the updated ad set data.
    - **Returns**: A dictionary containing the updated ad set data.
    - **Raises Exceptions**:
        - `FacebookAPIError`: If there is an error during the API call.
        - `InvalidArgumentError`: If the provided ad set data is invalid.

- `get_ad_set(ad_set_id: int) -> dict`: Retrieves data for a specific ad set within a Facebook advertising campaign.
    - **Purpose**: This function sends a request to Facebook to retrieve data for the specified ad set. 
    - **Parameters**:
        - `ad_set_id` (int): The ID of the ad set to retrieve.
    - **Returns**: A dictionary containing the ad set data.
    - **Raises Exceptions**:
        - `FacebookAPIError`: If there is an error during the API call.

- `delete_ad_set(ad_set_id: int) -> bool`: Deletes a specific ad set within a Facebook advertising campaign.
    - **Purpose**: This function sends a request to Facebook to delete the specified ad set.
    - **Parameters**:
        - `ad_set_id` (int): The ID of the ad set to delete.
    - **Returns**: True if the ad set was deleted successfully, False otherwise.
    - **Raises Exceptions**:
        - `FacebookAPIError`: If there is an error during the API call.

- `create_ad(ad_data: dict) -> dict`: Creates a new advertisement within a Facebook ad set.
    - **Purpose**: This function sends a request to Facebook to create a new advertisement within the specified ad set.
    - **Parameters**:
        - `ad_data` (dict): A dictionary containing the ad data, such as ad copy, images, and targeting.
    - **Returns**: A dictionary containing the created ad data.
    - **Raises Exceptions**:
        - `FacebookAPIError`: If there is an error during the API call.
        - `InvalidArgumentError`: If the provided ad data is invalid.

- `update_ad(ad_id: int, ad_data: dict) -> dict`: Updates an existing advertisement within a Facebook ad set.
    - **Purpose**: This function sends a request to Facebook to update the specified ad with the provided ad data.
    - **Parameters**:
        - `ad_id` (int): The ID of the ad to update.
        - `ad_data` (dict): A dictionary containing the updated ad data.
    - **Returns**: A dictionary containing the updated ad data. 
    - **Raises Exceptions**:
        - `FacebookAPIError`: If there is an error during the API call.
        - `InvalidArgumentError`: If the provided ad data is invalid.

- `get_ad(ad_id: int) -> dict`: Retrieves data for a specific advertisement within a Facebook ad set.
    - **Purpose**: This function sends a request to Facebook to retrieve data for the specified ad.
    - **Parameters**:
        - `ad_id` (int): The ID of the ad to retrieve.
    - **Returns**: A dictionary containing the ad data. 
    - **Raises Exceptions**:
        - `FacebookAPIError`: If there is an error during the API call.

- `delete_ad(ad_id: int) -> bool`: Deletes a specific advertisement within a Facebook ad set.
    - **Purpose**: This function sends a request to Facebook to delete the specified ad.
    - **Parameters**:
        - `ad_id` (int): The ID of the ad to delete.
    - **Returns**: True if the ad was deleted successfully, False otherwise. 
    - **Raises Exceptions**:
        - `FacebookAPIError`: If there is an error during the API call.

- `get_insights(object_id: int, metrics: list, date_preset: str = 'last_7d', level: str = 'ad') -> dict`: Retrieves insights (performance data) for a specific Facebook ad object (campaign, ad set, or ad).
    - **Purpose**: This function sends a request to Facebook to retrieve performance data for the specified ad object. 
    - **Parameters**:
        - `object_id` (int): The ID of the ad object (campaign, ad set, or ad).
        - `metrics` (list): A list of metrics to retrieve. 
        - `date_preset` (str): The date range for retrieving insights, for example, 'last_7d', 'last_14d', 'last_28d', 'last_90d', 'last_365d', 'lifetime', 'today', 'yesterday'.
        - `level` (str): The level of insights to retrieve, 'ad', 'adset', or 'campaign'. 
    - **Returns**: A dictionary containing the insights data.
    - **Raises Exceptions**:
        - `FacebookAPIError`: If there is an error during the API call.

## Functions

### `facebook_create_campaign(campaign_data: dict) -> dict`

**Purpose**: This function is responsible for creating a new Facebook advertising campaign. It accepts a dictionary containing the campaign data and sends a request to the Facebook API to create the campaign. 

**Parameters**:

- `campaign_data` (dict): A dictionary containing the campaign data, such as name, budget, targeting, and objectives.

**Returns**:

- `dict`: A dictionary containing the created campaign data.

**Raises Exceptions**:

- `FacebookAPIError`: If there is an error during the API call.
- `InvalidArgumentError`: If the provided campaign data is invalid.

**How the Function Works**:

1. It retrieves the Facebook endpoint instance from the `endpoints` module.
2. It calls the `create_campaign` method of the Facebook endpoint instance with the provided `campaign_data`.
3. It handles any exceptions that occur during the API call.

**Examples**:

```python
# Example campaign data
campaign_data = {
    "name": "My Facebook Campaign",
    "objective": "LINK_CLICKS",
    "budget": 1000,
    "targeting": {
        "age_min": 18,
        "age_max": 65,
        "interests": ["technology", "travel"],
        "geo_locations": ["United States"],
    },
}

# Create a new campaign
try:
    campaign = facebook_create_campaign(campaign_data)
    print(f"Campaign created successfully: {campaign['id']}")
except FacebookAPIError as ex:
    logger.error(f"Error creating campaign: {ex}", ex, exc_info=True)
except InvalidArgumentError as ex:
    logger.error(f"Invalid campaign data: {ex}", ex, exc_info=True)
```

### `facebook_update_campaign(campaign_id: int, campaign_data: dict) -> dict`

**Purpose**: This function is responsible for updating an existing Facebook advertising campaign. It accepts the campaign ID and a dictionary containing the updated campaign data. 

**Parameters**:

- `campaign_id` (int): The ID of the campaign to update.
- `campaign_data` (dict): A dictionary containing the updated campaign data.

**Returns**:

- `dict`: A dictionary containing the updated campaign data.

**Raises Exceptions**:

- `FacebookAPIError`: If there is an error during the API call.
- `InvalidArgumentError`: If the provided campaign data is invalid.

**How the Function Works**:

1. It retrieves the Facebook endpoint instance from the `endpoints` module.
2. It calls the `update_campaign` method of the Facebook endpoint instance with the provided `campaign_id` and `campaign_data`.
3. It handles any exceptions that occur during the API call.

**Examples**:

```python
# Example updated campaign data
campaign_data = {
    "name": "Updated Facebook Campaign",
    "budget": 1500,
}

# Update an existing campaign
try:
    campaign = facebook_update_campaign(123456789, campaign_data)
    print(f"Campaign updated successfully: {campaign['id']}")
except FacebookAPIError as ex:
    logger.error(f"Error updating campaign: {ex}", ex, exc_info=True)
except InvalidArgumentError as ex:
    logger.error(f"Invalid campaign data: {ex}", ex, exc_info=True)
```

### `facebook_get_campaign(campaign_id: int) -> dict`

**Purpose**: This function is responsible for retrieving data for a specific Facebook advertising campaign. It accepts the campaign ID and sends a request to the Facebook API to get the campaign data.

**Parameters**:

- `campaign_id` (int): The ID of the campaign to retrieve.

**Returns**:

- `dict`: A dictionary containing the campaign data.

**Raises Exceptions**:

- `FacebookAPIError`: If there is an error during the API call.

**How the Function Works**:

1. It retrieves the Facebook endpoint instance from the `endpoints` module.
2. It calls the `get_campaign` method of the Facebook endpoint instance with the provided `campaign_id`.
3. It handles any exceptions that occur during the API call.

**Examples**:

```python
# Get campaign data
try:
    campaign = facebook_get_campaign(123456789)
    print(f"Campaign data: {campaign}")
except FacebookAPIError as ex:
    logger.error(f"Error retrieving campaign data: {ex}", ex, exc_info=True)
```

### `facebook_delete_campaign(campaign_id: int) -> bool`

**Purpose**: This function is responsible for deleting a specific Facebook advertising campaign. It accepts the campaign ID and sends a request to the Facebook API to delete the campaign.

**Parameters**:

- `campaign_id` (int): The ID of the campaign to delete.

**Returns**:

- `bool`: True if the campaign was deleted successfully, False otherwise.

**Raises Exceptions**:

- `FacebookAPIError`: If there is an error during the API call.

**How the Function Works**:

1. It retrieves the Facebook endpoint instance from the `endpoints` module.
2. It calls the `delete_campaign` method of the Facebook endpoint instance with the provided `campaign_id`.
3. It handles any exceptions that occur during the API call.

**Examples**:

```python
# Delete a campaign
try:
    success = facebook_delete_campaign(123456789)
    if success:
        print(f"Campaign deleted successfully.")
    else:
        print(f"Error deleting campaign.")
except FacebookAPIError as ex:
    logger.error(f"Error deleting campaign: {ex}", ex, exc_info=True)
```

### `facebook_create_ad_set(ad_set_data: dict) -> dict`

**Purpose**: This function is responsible for creating a new ad set within a Facebook advertising campaign. It accepts a dictionary containing the ad set data and sends a request to the Facebook API to create the ad set.

**Parameters**:

- `ad_set_data` (dict): A dictionary containing the ad set data, such as budget, targeting, and scheduling.

**Returns**:

- `dict`: A dictionary containing the created ad set data.

**Raises Exceptions**:

- `FacebookAPIError`: If there is an error during the API call.
- `InvalidArgumentError`: If the provided ad set data is invalid.

**How the Function Works**:

1. It retrieves the Facebook endpoint instance from the `endpoints` module.
2. It calls the `create_ad_set` method of the Facebook endpoint instance with the provided `ad_set_data`.
3. It handles any exceptions that occur during the API call.

**Examples**:

```python
# Example ad set data
ad_set_data = {
    "campaign_id": 123456789,
    "name": "My Facebook Ad Set",
    "budget": 500,
    "targeting": {
        "age_min": 25,
        "age_max": 35,
        "interests": ["fashion", "sports"],
    },
}

# Create a new ad set
try:
    ad_set = facebook_create_ad_set(ad_set_data)
    print(f"Ad set created successfully: {ad_set['id']}")
except FacebookAPIError as ex:
    logger.error(f"Error creating ad set: {ex}", ex, exc_info=True)
except InvalidArgumentError as ex:
    logger.error(f"Invalid ad set data: {ex}", ex, exc_info=True)
```

### `facebook_update_ad_set(ad_set_id: int, ad_set_data: dict) -> dict`

**Purpose**: This function is responsible for updating an existing ad set within a Facebook advertising campaign. It accepts the ad set ID and a dictionary containing the updated ad set data.

**Parameters**:

- `ad_set_id` (int): The ID of the ad set to update.
- `ad_set_data` (dict): A dictionary containing the updated ad set data.

**Returns**:

- `dict`: A dictionary containing the updated ad set data.

**Raises Exceptions**:

- `FacebookAPIError`: If there is an error during the API call.
- `InvalidArgumentError`: If the provided ad set data is invalid.

**How the Function Works**:

1. It retrieves the Facebook endpoint instance from the `endpoints` module.
2. It calls the `update_ad_set` method of the Facebook endpoint instance with the provided `ad_set_id` and `ad_set_data`.
3. It handles any exceptions that occur during the API call.

**Examples**:

```python
# Example updated ad set data
ad_set_data = {
    "name": "Updated Facebook Ad Set",
    "budget": 600,
}

# Update an existing ad set
try:
    ad_set = facebook_update_ad_set(123456789, ad_set_data)
    print(f"Ad set updated successfully: {ad_set['id']}")
except FacebookAPIError as ex:
    logger.error(f"Error updating ad set: {ex}", ex, exc_info=True)
except InvalidArgumentError as ex:
    logger.error(f"Invalid ad set data: {ex}", ex, exc_info=True)
```

### `facebook_get_ad_set(ad_set_id: int) -> dict`

**Purpose**: This function is responsible for retrieving data for a specific ad set within a Facebook advertising campaign. It accepts the ad set ID and sends a request to the Facebook API to get the ad set data.

**Parameters**:

- `ad_set_id` (int): The ID of the ad set to retrieve.

**Returns**:

- `dict`: A dictionary containing the ad set data.

**Raises Exceptions**:

- `FacebookAPIError`: If there is an error during the API call.

**How the Function Works**:

1. It retrieves the Facebook endpoint instance from the `endpoints` module.
2. It calls the `get_ad_set` method of the Facebook endpoint instance with the provided `ad_set_id`.
3. It handles any exceptions that occur during the API call.

**Examples**:

```python
# Get ad set data
try:
    ad_set = facebook_get_ad_set(123456789)
    print(f"Ad set data: {ad_set}")
except FacebookAPIError as ex:
    logger.error(f"Error retrieving ad set data: {ex}", ex, exc_info=True)
```

### `facebook_delete_ad_set(ad_set_id: int) -> bool`

**Purpose**: This function is responsible for deleting a specific ad set within a Facebook advertising campaign. It accepts the ad set ID and sends a request to the Facebook API to delete the ad set.

**Parameters**:

- `ad_set_id` (int): The ID of the ad set to delete.

**Returns**:

- `bool`: True if the ad set was deleted successfully, False otherwise.

**Raises Exceptions**:

- `FacebookAPIError`: If there is an error during the API call.

**How the Function Works**:

1. It retrieves the Facebook endpoint instance from the `endpoints` module.
2. It calls the `delete_ad_set` method of the Facebook endpoint instance with the provided `ad_set_id`.
3. It handles any exceptions that occur during the API call.

**Examples**:

```python
# Delete an ad set
try:
    success = facebook_delete_ad_set(123456789)
    if success:
        print(f"Ad set deleted successfully.")
    else:
        print(f"Error deleting ad set.")
except FacebookAPIError as ex:
    logger.error(f"Error deleting ad set: {ex}", ex, exc_info=True)
```

### `facebook_create_ad(ad_data: dict) -> dict`

**Purpose**: This function is responsible for creating a new advertisement within a Facebook ad set. It accepts a dictionary containing the ad data and sends a request to the Facebook API to create the ad.

**Parameters**:

- `ad_data` (dict): A dictionary containing the ad data, such as ad copy, images, and targeting.

**Returns**:

- `dict`: A dictionary containing the created ad data.

**Raises Exceptions**:

- `FacebookAPIError`: If there is an error during the API call.
- `InvalidArgumentError`: If the provided ad data is invalid.

**How the Function Works**:

1. It retrieves the Facebook endpoint instance from the `endpoints` module.
2. It calls the `create_ad` method of the Facebook endpoint instance with the provided `ad_data`.
3. It handles any exceptions that occur during the API call.

**Examples**:

```python
# Example ad data
ad_data = {
    "adset_id": 123456789,
    "name": "My Facebook Ad",
    "creative": {
        "image_url": "https://example.com/image.jpg",
        "headline": "Amazing Product!",
        "body": "Check out our amazing product!",
    },
}

# Create a new ad
try:
    ad = facebook_create_ad(ad_data)
    print(f"Ad created successfully: {ad['id']}")
except FacebookAPIError as ex:
    logger.error(f"Error creating ad: {ex}", ex, exc_info=True)
except InvalidArgumentError as ex:
    logger.error(f"Invalid ad data: {ex}", ex, exc_info=True)
```

### `facebook_update_ad(ad_id: int, ad_data: dict) -> dict`

**Purpose**: This function is responsible for updating an existing advertisement within a Facebook ad set. It accepts the ad ID and a dictionary containing the updated ad data.

**Parameters**:

- `ad_id` (int): The ID of the ad to update.
- `ad_data` (dict): A dictionary containing the updated ad data.

**Returns**:

- `dict`: A dictionary containing the updated ad data.

**Raises Exceptions**:

- `FacebookAPIError`: If there is an error during the API call.
- `InvalidArgumentError`: If the provided ad data is invalid.

**How the Function Works**:

1. It retrieves the Facebook endpoint instance from the `endpoints` module.
2. It calls the `update_ad` method of the Facebook endpoint instance with the provided `ad_id` and `ad_data`.
3. It handles any exceptions that occur during the API call.

**Examples**:

```python
# Example updated ad data
ad_data = {
    "headline": "Updated Ad Headline!",
}

# Update an existing ad
try:
    ad = facebook_update_ad(123456789, ad_data)
    print(f"Ad updated successfully: {ad['id']}")
except FacebookAPIError as ex:
    logger.error(f"Error updating ad: {ex}", ex, exc_info=True)
except InvalidArgumentError as ex:
    logger.error(f"Invalid ad data: {ex}", ex, exc_info=True)
```

### `facebook_get_ad(ad_id: int) -> dict`

**Purpose**: This function is responsible for retrieving data for a specific advertisement within a Facebook ad set. It accepts the ad ID and sends a request to the Facebook API to get the ad data.

**Parameters**:

- `ad_id` (int): The ID of the ad to retrieve.

**Returns**:

- `dict`: A dictionary containing the ad data.

**Raises Exceptions**:

- `FacebookAPIError`: If there is an error during the API call.

**How the Function Works**:

1. It retrieves the Facebook endpoint instance from the `endpoints` module.
2. It calls the `get_ad` method of the Facebook endpoint instance with the provided `ad_id`.
3. It handles any exceptions that occur during the API call.

**Examples**:

```python
# Get ad data
try:
    ad = facebook_get_ad(123456789)
    print(f"Ad data: {ad}")
except FacebookAPIError as ex:
    logger.error(f"Error retrieving ad data: {ex}", ex, exc_info=True)
```

### `facebook_delete_ad(ad_id: int) -> bool`

**Purpose**: This function is responsible for deleting a specific advertisement within a Facebook ad set. It accepts the ad ID and sends a request to the Facebook API to delete the ad.

**Parameters**:

- `ad_id` (int): The ID of the ad to delete.

**Returns**:

- `bool`: True if the ad was deleted successfully, False otherwise.

**Raises Exceptions**:

- `FacebookAPIError`: If there is an error during the API call.

**How the Function Works**:

1. It retrieves the Facebook endpoint instance from the `endpoints` module.
2. It calls the `delete_ad` method of the Facebook endpoint instance with the provided `ad_id`.
3. It handles any exceptions that occur during the API call.

**Examples**:

```python
# Delete an ad
try:
    success = facebook_delete_ad(123456789)
    if success:
        print(f"Ad deleted successfully.")
    else:
        print(f"Error deleting ad.")
except FacebookAPIError as ex:
    logger.error(f"Error deleting ad: {ex}", ex, exc_info=True)
```

### `facebook_get_insights(object_id: int, metrics: list, date_preset: str = 'last_7d', level: str = 'ad') -> dict`

**Purpose**: This function is responsible for retrieving insights (performance data) for a specific Facebook ad object (campaign, ad set, or ad). It accepts the object ID, a list of metrics to retrieve, and optional parameters for date range and level of insights.

**Parameters**:

- `object_id` (int): The ID of the ad object (campaign, ad set, or ad).
- `metrics` (list): A list of metrics to retrieve.
- `date_preset` (str): The date range for retrieving insights, for example, 'last_7d', 'last_14d', 'last_28d', 'last_90d', 'last_365d', 'lifetime', 'today', 'yesterday'. Defaults to 'last_7d'.
- `level` (str): The level of insights to retrieve, 'ad', 'adset', or 'campaign'. Defaults to 'ad'.

**Returns**:

- `dict`: A dictionary containing the insights data.

**Raises Exceptions**:

- `FacebookAPIError`: If there is an error during the API call.

**How the Function Works**:

1. It retrieves the Facebook endpoint instance from the `endpoints` module.
2. It calls the `get_insights` method of the Facebook endpoint instance with the provided `object_id`, `metrics`, `date_preset`, and `level`.
3. It handles any exceptions that occur during the API call.

**Examples**:

```python
# Get insights for an ad
try:
    insights = facebook_get_insights(
        object_id=123456789,
        metrics=["impressions", "clicks", "reach"],
        date_preset="last_14d",
        level="ad",
    )
    print(f"Insights data: {insights}")
except FacebookAPIError as ex:
    logger.error(f"Error retrieving insights data: {ex}", ex, exc_info=True)
```

## Parameter Details

- `campaign_data` (dict): This parameter contains the data for creating or updating a Facebook advertising campaign. It includes details like the campaign name, objective, budget, targeting criteria, and other relevant settings.

- `campaign_id` (int): This parameter represents the unique identifier of a Facebook advertising campaign. It's used to identify the specific campaign for operations like retrieving, updating, or deleting.

- `ad_set_data` (dict): This parameter contains the data for creating or updating an ad set within a Facebook advertising campaign. It includes details like the ad set name, budget, targeting criteria, and other settings.

- `ad_set_id` (int): This parameter represents the unique identifier of a Facebook ad set. It's used to identify the specific ad set for operations like retrieving, updating, or deleting.

- `ad_data` (dict): This parameter contains the data for creating or updating an advertisement within a Facebook ad set. It includes details like the ad copy, images, targeting criteria, and other settings.

- `ad_id` (int): This parameter represents the unique identifier of a Facebook advertisement. It's used to identify the specific ad for operations like retrieving, updating, or deleting.

- `object_id` (int): This parameter represents the unique identifier of a Facebook ad object (campaign, ad set, or ad). It's used to retrieve insights (performance data) for the specific object.

- `metrics` (list): This parameter is a list of metrics to retrieve for a Facebook ad object. It includes metrics like impressions, clicks, reach, cost, conversions, and other performance indicators.

- `date_preset` (str): This parameter specifies the date range for retrieving insights data. It allows you to retrieve data for specific periods like the last 7 days, last 14 days, last 28 days, lifetime, today, yesterday, and so on.

- `level` (str): This parameter specifies the level of insights to retrieve. You can retrieve insights for the ad level (individual ads), ad set level (groups of ads within a campaign), or campaign level (the entire campaign).

## Examples

```python
# Create a new campaign
campaign_data = {
    "name": "My Facebook Campaign",
    "objective": "LINK_CLICKS",
    "budget": 1000,
    "targeting": {
        "age_min": 18,
        "age_max": 65,
        "interests": ["technology", "travel"],
        "geo_locations": ["United States"],
    },
}
campaign = facebook_create_campaign(campaign_data)

# Update an existing campaign
campaign_id = 123456789
campaign_data = {"name": "Updated Facebook Campaign", "budget": 1500}
campaign = facebook_update_campaign(campaign_id, campaign_data)

# Retrieve data for a campaign
campaign = facebook_get_campaign(campaign_id)

# Delete a campaign
facebook_delete_campaign(campaign_id)

# Create a new ad set
ad_set_data = {
    "campaign_id": campaign_id,
    "name": "My Facebook Ad Set",
    "budget": 500,
    "targeting": {
        "age_min": 25,
        "age_max": 35,
        "interests": ["fashion", "sports"],
    },
}
ad_set = facebook_create_ad_set(ad_set_data)

# Update an existing ad set
ad_set_id = 123456789
ad_set_data = {"name": "Updated Facebook Ad Set", "budget": 600}
ad_set = facebook_update_ad_set(ad_set_id, ad_set_data)

# Retrieve data for an ad set
ad_set = facebook_get_ad_set(ad_set_id)

# Delete an ad set
facebook_delete_ad_set(ad_set_id)

# Create a new ad
ad_data = {
    "adset_id": ad_set_id,
    "name": "My Facebook Ad",
    "creative": {
        "image_url": "https://example.com/image.jpg",
        "headline": "Amazing Product!",
        "body": "Check out our amazing product!",
    },
}
ad = facebook_create_ad(ad_data)

# Update an existing ad
ad_id = 123456789
ad_data = {"headline": "Updated Ad Headline!"}
ad = facebook_update_ad(ad_id, ad_data)

# Retrieve data for an ad
ad = facebook_get_ad(ad_id)

# Delete an ad
facebook_delete_ad(ad_id)

# Get insights for an ad
insights = facebook_get_insights(
    object_id=ad_id,
    metrics=["impressions", "clicks", "reach"],
    date_preset="last_14d",
    level="ad",
)
```

This code demonstrates various ways to work with the Facebook advertising platform using the provided functions. You can modify these examples and experiment with different parameters to tailor your Facebook advertising strategies.