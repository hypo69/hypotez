# Google Drive Uploader Bot Documentation

## Overview

This documentation provides a detailed description of the Google Drive Uploader Bot project. The bot is a Telegram bot written in Python that allows users to upload files from various sources, including direct links, Mega.nz, Dropbox, and more, directly to their Google Drive.

## Details

The bot utilizes the Google Drive API to interact with Google Drive accounts. It offers various functionalities:

- **Uploads:** Users can send supported links to the bot, which will then be uploaded to their Google Drive.
- **Authorization:** The bot requires users to authorize it to access their Google Drive account.
- **Teamdrive Support:** The bot supports uploading files to Team Drives, although this feature requires hardcoding the Team Drive ID and folder ID in the `creds.py` file.

## Classes

### `Bot`

**Description:**  The `Bot` class represents the main Telegram bot instance, handling all interactions with users and Google Drive. 

**Inherits:**  This class inherits from the `telebot.TeleBot` class, providing essential functionalities for creating and managing a Telegram bot.

**Attributes:**

- `token` (str): The Telegram bot token obtained from BotFather.
- `credentials` (dict):  A dictionary containing the Google Drive API credentials, including client ID, client secret, and refresh token.
- `teamdrive_id` (str):  The ID of the Team Drive if Teamdrive support is enabled.
- `teamdrive_folder_id` (str): The ID of the folder within the Team Drive where files will be uploaded.
- `mega_email` (str):  The email address for the Mega.nz account, used if Mega.nz uploads are enabled.
- `mega_password` (str):  The password for the Mega.nz account.

**Methods:**

- `start(message):`  Handles the `/start` command, sending a welcome message to the user.
- `auth(message):`  Initiates the Google Drive authorization process, generating a unique key for the user.
- `revoke(message):`  Revokes the user's authorization and deletes their saved credentials.
- `help(message):`  Provides a list of available commands and functionalities.
- `upload_file(message):`  Processes the user's link and attempts to upload the corresponding file to Google Drive.
- `handle_file_upload(file_id, folder_id, file_name):`  Uploads a file to Google Drive using the specified file ID, folder ID, and file name.
- `get_file_id(message):`  Extracts the file ID from a supported link.
- `get_folder_id(message):`  Retrieves the folder ID from a user's input, either from a specific command or by default.
- `handle_mega_link(message):`  Processes a Mega.nz link, downloading the file and uploading it to Google Drive.
- `handle_dropbox_link(message):`  Handles a Dropbox link, downloading the file and uploading it to Google Drive.

## Functions

### `main()`

**Purpose:**  The `main` function serves as the entry point for the bot. It initializes the bot instance, sets up various handlers for commands and messages, and starts the bot's polling process.

**Parameters:**  None

**Returns:**  None

**Raises Exceptions:**  None

**How the Function Works:**

1.  **Bot Initialization:**  The `main` function first initializes the `Bot` class with the provided Telegram bot token.
2.  **Handler Setup:**  It then sets up handlers for various commands, including `/start`, `/auth`, `/revoke`, `/help`, and message handlers for processing user input.
3.  **Polling:**  Finally, the function starts the bot's polling process, allowing it to listen for incoming messages and execute corresponding actions.

**Examples:**

```python
if __name__ == "__main__":
    main()
```

## Parameter Details

- `token` (str):  The unique identifier for your Telegram bot obtained from the BotFather.
- `credentials` (dict):  A dictionary containing the Google Drive API credentials, including client ID, client secret, and refresh token.
- `teamdrive_id` (str): The ID of the Team Drive if Teamdrive support is enabled.
- `teamdrive_folder_id` (str): The ID of the folder within the Team Drive where files will be uploaded.
- `mega_email` (str): The email address for the Mega.nz account, used if Mega.nz uploads are enabled.
- `mega_password` (str): The password for the Mega.nz account.
- `file_id` (str):  The unique identifier for a specific file within Google Drive or on a supported file hosting service.
- `folder_id` (str): The unique identifier for a folder within Google Drive.
- `file_name` (str): The name of the file to be uploaded.
- `message` (telebot.types.Message):  A Telegram message object representing the user's input.

## Examples

### Initializing the bot and setting up handlers

```python
bot = Bot(token=TELEGRAM_BOT_TOKEN)

bot.message_handler(commands=["start"])(start)
bot.message_handler(commands=["auth"])(auth)
bot.message_handler(commands=["revoke"])(revoke)
bot.message_handler(commands=["help"])(help)
bot.message_handler(func=lambda message: True)(upload_file)
```

### Handling the `/auth` command

```python
@bot.message_handler(commands=["auth"])
def auth(message):
    """
    Handles the `/auth` command, initiating the Google Drive authorization process.

    Args:
        message (telebot.types.Message): The user's message containing the `/auth` command.

    Returns:
        None
    """
    # Generate a unique key for the user.
    key = generate_unique_key()

    # Store the key and user ID in the `credentials` dictionary.
    credentials[str(message.from_user.id)] = {"key": key}

    # Send the key to the user.
    bot.send_message(message.chat.id, f"Your unique key is: `{key}`. Please visit this link to authorize the bot: [Authorization link here]")
```

### Processing a file upload

```python
@bot.message_handler(func=lambda message: True)
def upload_file(message):
    """
    Processes the user's message, attempting to upload the file to Google Drive.

    Args:
        message (telebot.types.Message): The user's message containing the file link or direct file.

    Returns:
        None
    """
    # Extract the file ID from the user's input.
    file_id = get_file_id(message)

    # Retrieve the folder ID from the user's input or the default folder.
    folder_id = get_folder_id(message)

    # Attempt to upload the file to Google Drive.
    try:
        # Upload the file based on the file ID, folder ID, and file name.
        handle_file_upload(file_id, folder_id, file_name)

        # Send a success message to the user.
        bot.send_message(message.chat.id, f"File uploaded successfully!")
    except Exception as ex:
        # Log the error and send a failure message to the user.
        logger.error(f"Error uploading file: {ex}", exc_info=True)
        bot.send_message(message.chat.id, f"Error uploading file. Please try again.")
```

### Starting the bot's polling process

```python
if __name__ == "__main__":
    # Start the bot's polling process.
    bot.polling(none_stop=True, interval=0)
```

## TODO

- **Rename file while uploading:**  Implement functionality to allow users to rename files during the upload process.
- **Add Telegram File Support:**  Enable the bot to handle Telegram files, although this may be slow due to download limitations.
- **Add YouTube-dl:**  Integrate the `youtube-dl` library to allow users to download and upload YouTube videos.
- **Fix Openload Support:**  Address any issues related to the bot's support for Openload links.
- **Adding zippyshare, Mediafire, cloud mail, Yandex disk, Sourceforge:** Implement support for these file hosting services.
- **Google Drive Direct Link Generator:**  Add functionality to generate direct links to files stored in Google Drive.

## License

- GPLv3

## Contributing

Contributions to the project are welcome. If you wish to contribute, please feel free to submit a pull request or open an issue.

## Acknowledgments

- [CyberBoySumanjay](https://github.com/cyberboysumanjay) for the initial project inspiration and codebase.
- [SpEcHiDe](https://github.com/SpEcHiDe) and [Atulkadian](https://github.com/atulkadian) for their valuable contributions.