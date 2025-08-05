# Google Drive Bot

## Overview

This module defines a Telegram bot that allows users to upload files directly to their Google Drive accounts using a simple chat interface. The bot streamlines file transfers by automating the authentication process and supporting various download sources, including Dropbox, Mega, and general web URLs.

## Details

The bot leverages Telegram's Bot API and the Google Drive API for functionality. It utilizes a series of commands and message handlers to process user interactions, manage authentication, and facilitate file uploads. 

- **Authentication:** The bot uses OAuth 2.0 for user authentication. 
- **File Download:**  Supports downloading files from Dropbox, Mega, and general web URLs. 
- **Upload to Google Drive:**  After successful download, the bot uploads the file to the user's Google Drive account. 

## Classes

### `GoogleDrive`

**Description**:  This class represents the user's Google Drive account and provides methods for interacting with the Google Drive API.

**Inherits**:  -

**Attributes**:
- `http`: HTTP object for making API requests.
- `initial_folder`: Initial folder in Google Drive for file uploads.
- `drive`: Google Drive API service object.

**Methods**:
- `get_folder_id(folder_name: str) -> str | None`:  This method retrieves the ID of a folder in the user's Google Drive account. If the folder does not exist, it creates a new folder.
- `upload_file(file_path: str, folder_id: str) -> str | None`: This method uploads a file to a specific folder in the user's Google Drive.

## Functions

### `help(update, context)`

**Purpose**:  Provides help information to the user in the form of a Telegram message.

**Parameters**:
- `update`:  Telegram update object containing information about the incoming message.
- `context`:  Telegram context object used for interacting with the bot.

**Returns**:  -

**Raises Exceptions**:
- `Exception`:  Handles general exceptions during message sending.

**How the Function Works**:
- The function retrieves the `HELP` text from the `TEXT` module and sends it to the user in a formatted message.
- It uses the `send_message` method of the Telegram bot object to communicate with the user.

**Examples**:
- User sends the command `/help` to the bot.
- The bot responds with the help message containing information about available commands and functionality.


### `auth(update, context)`

**Purpose**:  Handles user authentication with Google Drive.

**Parameters**:
- `update`: Telegram update object containing information about the incoming message.
- `context`: Telegram context object used for interacting with the bot.

**Returns**:  -

**Raises Exceptions**:
- `Exception`:  Handles exceptions related to loading credentials.

**How the Function Works**:
- The function attempts to load existing credentials from a file named after the user's ID.
- If credentials are not found, it generates an authentication URL and sends it to the user.
- If the user has already authenticated, it refreshes the access token if it is expired.

**Examples**:
- User sends the command `/auth` to the bot.
- If the user is not yet authenticated, the bot sends an authentication URL. 
- If the user has already authenticated, the bot confirms authentication.


### `token(update, context)`

**Purpose**:  Handles user input of their Google Drive access token.

**Parameters**:
- `update`: Telegram update object containing information about the incoming message.
- `context`: Telegram context object used for interacting with the bot.

**Returns**:  -

**Raises Exceptions**:
- `Exception`:  Handles exceptions related to authentication with the provided token.

**How the Function Works**:
- The function checks if the user's message contains a valid access token.
- If a valid token is found, it authenticates the user with the Google Drive API and saves the credentials to a file. 

**Examples**:
- User sends their Google Drive access token to the bot.
- The bot checks if the token is valid, authenticates the user, and saves the credentials. 

### `start(update, context)`

**Purpose**:  Handles the `/start` command, initiating a conversation with the user.

**Parameters**:
- `update`: Telegram update object containing information about the incoming message.
- `context`: Telegram context object used for interacting with the bot.

**Returns**:  -

**Raises Exceptions**:  -

**How the Function Works**:
- The function sends a welcome message to the user, including their first name.

**Examples**:
- User sends the command `/start` to the bot.
- The bot welcomes the user and provides a brief description of its functionality.

### `revoke_tok(update, context)`

**Purpose**:  Handles the `/revoke` command, allowing the user to revoke their Google Drive authentication.

**Parameters**:
- `update`: Telegram update object containing information about the incoming message.
- `context`: Telegram context object used for interacting with the bot.

**Returns**:  -

**Raises Exceptions**:
- `Exception`:  Handles exceptions related to deleting the user's credentials file.

**How the Function Works**:
- The function attempts to delete the user's credentials file, which revokes their Google Drive authentication.

**Examples**:
- User sends the command `/revoke` to the bot.
- The bot attempts to remove the user's credentials file, revoking their authentication.

### `UPLOAD(update, context)`

**Purpose**:  Handles user requests to upload files to their Google Drive account.

**Parameters**:
- `update`: Telegram update object containing information about the incoming message.
- `context`: Telegram context object used for interacting with the bot.

**Returns**:  -

**Raises Exceptions**:
- `Exception`: Handles various exceptions related to file download and upload.

**How the Function Works**:
- The function extracts the URL from the user's message.
- It determines the source of the URL (Dropbox, Mega, or general web URL) and initiates a download using the appropriate method.
- Once the download is complete, it uploads the file to the user's Google Drive account.

**Examples**:
- User sends a Dropbox URL to the bot.
- The bot downloads the file from Dropbox, uploads it to Google Drive, and sends a link to the uploaded file to the user.

**Inner Functions**:
- `DPBOX(url: str) -> str`:  This inner function handles downloads from Dropbox. 
- `wget_dl(url: str) -> str`: This inner function handles downloads from general web URLs.
- `upload(filename: str, update, context, folder_name: str)`: This inner function handles uploading files to Google Drive.

### `status(update, context)`

**Purpose**:  Provides the user with a status update message.

**Parameters**:
- `update`: Telegram update object containing information about the incoming message.
- `context`: Telegram context object used for interacting with the bot.

**Returns**:  -

**Raises Exceptions**:  -

**How the Function Works**:
- The function sends a status update message to the user.

**Examples**:
- User sends the command `/update` to the bot.
- The bot responds with a message indicating that the bot is operational. 

## Parameter Details

- `update`: Telegram update object, providing information about the incoming message, such as the user's ID, text content, and chat ID.
- `context`: Telegram context object, facilitating communication with the bot, managing user data, and executing commands.
- `url`: The URL of the file to be downloaded, which could be from Dropbox, Mega, or a general web URL.
- `folder_name`: The name of the folder on Google Drive where the uploaded file should be saved.
- `filename`: The name of the downloaded file. 
- `ID`:  The user's Telegram ID. 

## Examples

**Example 1: User Authentication**

1. User sends `/auth` to the bot.
2. The bot responds with an authentication URL.
3. User opens the URL in their browser and follows the authentication steps.
4. The bot receives the access token and saves it to a file associated with the user's ID.

**Example 2: File Upload**

1. User sends a URL to a file on Dropbox to the bot.
2. The bot downloads the file from Dropbox.
3. The bot uploads the file to the user's Google Drive in the designated folder.
4. The bot sends a link to the uploaded file to the user.

**Example 3: Revoking Authentication**

1. User sends `/revoke` to the bot.
2. The bot removes the user's credentials file.
3. User authentication is revoked.

## Conclusion

The Google Drive Bot provides a streamlined solution for uploading files to Google Drive from various sources. It simplifies the process by automating authentication, supporting multiple download sources, and providing a user-friendly Telegram interface.