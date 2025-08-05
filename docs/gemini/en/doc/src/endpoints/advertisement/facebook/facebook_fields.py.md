# Facebook Fields

## Overview

This module defines the fields used for Facebook advertisements and events within the `hypotez` project. It utilizes a JSON configuration file to load and store the field definitions.

## Details

This file is responsible for loading field definitions from a JSON file and making them accessible through class attributes. These fields are likely used in constructing Facebook ad and event data structures.

## Classes

### `FacebookFields`

**Description**: This class represents a container for Facebook field definitions. It loads the field names and their corresponding values from a JSON file.

**Inherits**: N/A

**Attributes**:

- `self._payload`:  A private method used to load field definitions from the JSON file. 

**Methods**:

- `__init__`: Initializes the `FacebookFields` instance and calls `self._payload` to load field definitions.

- `_payload`:  
    - Loads field definitions from the JSON file located at `gs.path.src/advertisement/facebok/facebook_feilds.json`.
    - If the file loading fails, it logs an error message and returns.
    - If successful, it iterates through the loaded data, assigns each field name as an attribute of the class, and sets its value.

## Example Usage

```python
from src.endpoints.advertisement.facebook.facebook_fields import FacebookFields

facebook_fields = FacebookFields()

# Access a field by name
field_value = facebook_fields.field_name

# Print all loaded fields
for field_name in dir(facebook_fields):
    if not field_name.startswith('_'):
        print(f"{field_name}: {getattr(facebook_fields, field_name)}")
```

## Inner Functions

N/A

## How the Function Works

The `_payload` function follows these steps:

1. Loads the JSON data from the specified file path.
2. Checks if the data was successfully loaded.
3. If the data is loaded, it iterates through each key-value pair in the JSON data.
4. For each pair, it dynamically creates an attribute of the `FacebookFields` class with the key as the attribute name and the value as the attribute value.

## Examples

```python
# Example JSON data in facebook_feilds.json
{
  "ad_id": "id of the advertisement",
  "ad_name": "name of the advertisement",
  "ad_set_id": "id of the ad set",
  "ad_set_name": "name of the ad set",
  "campaign_id": "id of the campaign",
  "campaign_name": "name of the campaign",
  "event_name": "Name of the event",
  "event_time": "Time of the event",
  "event_location": "Location of the event",
  "event_description": "Description of the event",
  "event_link": "Link to the event"
}
```

```python
# Accessing field values
field_value = facebook_fields.ad_id  # Retrieves the value for 'ad_id'
```

## Parameter Details

N/A

## Examples

N/A