# Creds Module

## Overview

This module defines the `Creds` class, which holds essential credentials for interacting with Google Drive and Telegram bots. It provides a centralized location to store and manage these sensitive data.

## Details

This file is located in the `hypotez/src/endpoints/bots/google_drive` directory. It plays a crucial role in facilitating data transfer between Telegram bots and Google Drive.

## Classes

### `Creds`

**Description**: This class stores credentials for Telegram bots and Google Drive, including the bot token, Team Drive folder ID, and Team Drive ID. 

**Attributes**:
- `TG_TOKEN` (str): Telegram bot token for authentication.
- `TEAMDRIVE_FOLDER_ID` (str): Folder ID within the Team Drive where data will be uploaded.
- `TEAMDRIVE_ID` (str): ID of the Google Team Drive.

**How it works**:

The `Creds` class simplifies credential management by providing a dedicated structure to store sensitive information. These credentials are used by the bot to access Google Drive and upload or download files.


**Example**:

```python
from hypotez.src.endpoints.bots.google_drive.creds import Creds

# Create a Creds object
creds = Creds()

# Access the credentials
tg_token = creds.TG_TOKEN
teamdrive_folder_id = creds.TEAMDRIVE_FOLDER_ID
teamdrive_id = creds.TEAMDRIVE_ID

# Assign credentials (example)
creds.TG_TOKEN = "dkjfksdkffdkfdkfdj"
creds.TEAMDRIVE_FOLDER_ID = "13v4MaZnBz-iEHlZ0gFXk7rh"
creds.TEAMDRIVE_ID = "0APh6R4WVvguEUk9PV"

# Example usage
print(f"Telegram Bot Token: {tg_token}")
print(f"Team Drive Folder ID: {teamdrive_folder_id}")
print(f"Team Drive ID: {teamdrive_id}")
```

This example demonstrates how to access and assign values to the credentials within the `Creds` class.