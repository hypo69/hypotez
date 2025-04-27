# hypotez/src/keepass.md

## Overview

This file contains the `ProgramSettings` class which is responsible for reading and storing credentials from a KeePass database file (`credentials.kdbx`). This class utilizes the `pykeepass` library to interact with the KeePass database and provides access to various credentials needed for the `hypotez` project.

## Details

The `ProgramSettings` class functions as a singleton, ensuring that only one instance of the configuration settings is available throughout the application. The class is designed to retrieve credentials from the KeePass database and make them readily accessible for different parts of the `hypotez` project.

###  `ProgramSettings`

**Description**: This class manages the configuration settings and retrieves credentials from a KeePass database file (`credentials.kdbx`). It acts as a singleton, ensuring a single instance of the configuration settings is available globally.

**Inherits**: N/A

**Attributes**:

- `credentials` (`SimpleNamespace`): Stores credentials for different services, grouped by service name.

**Methods**:

- `_open_kp`():  Opens the KeePass database file (`credentials.kdbx`) and retrieves the password.
- `_load_credentials`():  Loads credentials for various services from the KeePass database and stores them in the `credentials` attribute.
- `get_credentials`():  Returns the `credentials` attribute, providing access to the loaded credentials.

**Principle of Operation**:

The `ProgramSettings` class works in the following stages:

1. **Opening the database:**
    - The `_open_kp()` method attempts to open the KeePass database file (`credentials.kdbx`).
    - It tries to read the password from a file named `password.txt` if it exists.
    - If the password file is not found, it prompts the user to enter the password via the console.
    - If the opening attempt fails, it retries several times.
    - If all attempts fail, the program terminates.

2. **Loading credentials:**
    - After successful database opening, the `_load_credentials()` method is called.
    - It calls individual methods for loading credentials for each service.
    - These methods use the `kp.find_groups()` function to navigate through groups and entries in the KeePass database.
    - They extract necessary data (API keys, passwords, logins) from each entry using `entry.custom_properties` and `entry.password`.

**Examples**:

```python
from src.keepass import ProgramSettings

# Accessing the credentials
settings = ProgramSettings()  # Gets the single instance
openai_api_key = settings.get_credentials().openai.api_key
```

## Function Details

### `_open_kp`

**Purpose**: This method opens the KeePass database file (`credentials.kdbx`) and retrieves the password.

**Parameters**:

- None

**Returns**:

- `pykeepass.KeePass` object:  Represents the opened KeePass database.

**Raises Exceptions**:

- `Exception`:  If an error occurs during the opening process.

**How the Function Works**:

1. Attempts to read the password from `password.txt`.
2. If the file is not found, prompts the user for the password.
3. Opens the KeePass database file with the retrieved password.
4. Returns the opened KeePass database object.

**Examples**:

```python
# Example: Opening the KeePass database
from src.keepass import ProgramSettings

settings = ProgramSettings()
try:
    kp = settings._open_kp()
    logger.info("Successfully opened KeePass database.")
except Exception as ex:
    logger.error("Error opening KeePass database:", ex, exc_info=True)
```

### `_load_credentials`

**Purpose**:  This method loads credentials for various services from the KeePass database and stores them in the `credentials` attribute.

**Parameters**:

- None

**Returns**:

- None

**Raises Exceptions**:

- `Exception`:  If an error occurs during the loading process.

**How the Function Works**:

1. Calls individual methods for loading credentials for each service.
2. Retrieves the `credentials` object from the `ProgramSettings` instance.
3. Calls methods for loading credentials from each service:
    - `_load_aliexpress_credentials()`
    - `_load_openai_credentials()`
    - `_load_gemini_credentials()`
    - `_load_telegram_credentials()`
    - `_load_discord_credentials()`
    - `_load_prestashop_credentials()`
    - `_load_smtp_credentials()`
    - `_load_facebook_credentials()`
    - `_load_google_api_credentials()`

**Examples**:

```python
from src.keepass import ProgramSettings

settings = ProgramSettings()
try:
    settings._load_credentials()
    logger.info("Credentials loaded successfully.")
except Exception as ex:
    logger.error("Error loading credentials:", ex, exc_info=True)
```

### `_load_aliexpress_credentials`

**Purpose**: This method loads credentials for AliExpress service.

**Parameters**:

- None

**Returns**:

- None

**Raises Exceptions**:

- `Exception`:  If an error occurs during the loading process.

**How the Function Works**:

1. Searches for a group named `suppliers/aliexpress/api`.
2. Extracts `api_key`, `secret`, `tracking_id`, `email` from custom properties of the entry.
3. Extracts `password` from the entry password.
4. Stores these values in the `ProgramSettings.credentials.aliexpress` attribute.

**Examples**:

```python
from src.keepass import ProgramSettings

settings = ProgramSettings()
try:
    settings._load_aliexpress_credentials()
    logger.info("AliExpress credentials loaded successfully.")
except Exception as ex:
    logger.error("Error loading AliExpress credentials:", ex, exc_info=True)
```

### `_load_openai_credentials`

**Purpose**:  This method loads credentials for OpenAI service.

**Parameters**:

- None

**Returns**:

- None

**Raises Exceptions**:

- `Exception`:  If an error occurs during the loading process.

**How the Function Works**:

1. Searches for a group named `openai`.
2. Extracts `api_key`, `project_api` from custom properties of the entry.
3. Extracts `assistant_id` from the entry password.
4. Stores these values in the `ProgramSettings.credentials.openai` attribute.

**Examples**:

```python
from src.keepass import ProgramSettings

settings = ProgramSettings()
try:
    settings._load_openai_credentials()
    logger.info("OpenAI credentials loaded successfully.")
except Exception as ex:
    logger.error("Error loading OpenAI credentials:", ex, exc_info=True)
```

### `_load_gemini_credentials`

**Purpose**:  This method loads credentials for Gemini service.

**Parameters**:

- None

**Returns**:

- None

**Raises Exceptions**:

- `Exception`:  If an error occurs during the loading process.

**How the Function Works**:

1. Searches for a group named `gemini`.
2. Extracts `api_key` from custom properties of the entry.
3. Stores this value in the `ProgramSettings.credentials.gemini` attribute.

**Examples**:

```python
from src.keepass import ProgramSettings

settings = ProgramSettings()
try:
    settings._load_gemini_credentials()
    logger.info("Gemini credentials loaded successfully.")
except Exception as ex:
    logger.error("Error loading Gemini credentials:", ex, exc_info=True)
```

### `_load_telegram_credentials`

**Purpose**:  This method loads credentials for Telegram service.

**Parameters**:

- None

**Returns**:

- None

**Raises Exceptions**:

- `Exception`:  If an error occurs during the loading process.

**How the Function Works**:

1. Searches for a group named `telegram`.
2. Extracts `token` from custom properties of the entry.
3. Stores this value in the `ProgramSettings.credentials.telegram` attribute.

**Examples**:

```python
from src.keepass import ProgramSettings

settings = ProgramSettings()
try:
    settings._load_telegram_credentials()
    logger.info("Telegram credentials loaded successfully.")
except Exception as ex:
    logger.error("Error loading Telegram credentials:", ex, exc_info=True)
```

### `_load_discord_credentials`

**Purpose**:  This method loads credentials for Discord service.

**Parameters**:

- None

**Returns**:

- None

**Raises Exceptions**:

- `Exception`:  If an error occurs during the loading process.

**How the Function Works**:

1. Searches for a group named `discord`.
2. Extracts `application_id`, `public_key`, and `bot_token` from custom properties of the entry.
3. Stores these values in the `ProgramSettings.credentials.discord` attribute.

**Examples**:

```python
from src.keepass import ProgramSettings

settings = ProgramSettings()
try:
    settings._load_discord_credentials()
    logger.info("Discord credentials loaded successfully.")
except Exception as ex:
    logger.error("Error loading Discord credentials:", ex, exc_info=True)
```

### `_load_prestashop_credentials`

**Purpose**:  This method loads credentials for PrestaShop service.

**Parameters**:

- None

**Returns**:

- None

**Raises Exceptions**:

- `Exception`:  If an error occurs during the loading process.

**How the Function Works**:

1. Searches for a group named `prestashop/clients`.
2. Extracts `api_key`, `api_domain`, `db_server`, `db_user`, `db_password` from custom properties of each entry in the group.
3. Creates a `SimpleNamespace` object for each set of data.
4. Appends these objects to the `ProgramSettings.credentials.presta.client` list.
5. Searches for a group named `prestashop/translation`.
6. Extracts `server`, `port`, `database`, `user`, `password` from custom properties of the first entry in the group.
7. Stores these values in the `ProgramSettings.credentials.presta.translations` attribute.

**Examples**:

```python
from src.keepass import ProgramSettings

settings = ProgramSettings()
try:
    settings._load_prestashop_credentials()
    logger.info("PrestaShop credentials loaded successfully.")
except Exception as ex:
    logger.error("Error loading PrestaShop credentials:", ex, exc_info=True)
```

### `_load_smtp_credentials`

**Purpose**:  This method loads credentials for SMTP service.

**Parameters**:

- None

**Returns**:

- None

**Raises Exceptions**:

- `Exception`:  If an error occurs during the loading process.

**How the Function Works**:

1. Searches for a group named `smtp`.
2. Extracts `server`, `port`, `user`, and `password` from custom properties of each entry in the group.
3. Creates a `SimpleNamespace` object for each set of data.
4. Appends these objects to the `ProgramSettings.credentials.smtp` list.

**Examples**:

```python
from src.keepass import ProgramSettings

settings = ProgramSettings()
try:
    settings._load_smtp_credentials()
    logger.info("SMTP credentials loaded successfully.")
except Exception as ex:
    logger.error("Error loading SMTP credentials:", ex, exc_info=True)
```

### `_load_facebook_credentials`

**Purpose**:  This method loads credentials for Facebook service.

**Parameters**:

- None

**Returns**:

- None

**Raises Exceptions**:

- `Exception`:  If an error occurs during the loading process.

**How the Function Works**:

1. Searches for a group named `facebook`.
2. Extracts `app_id`, `app_secret`, and `access_token` from custom properties of each entry in the group.
3. Creates a `SimpleNamespace` object for each set of data.
4. Appends these objects to the `ProgramSettings.credentials.facebook` list.

**Examples**:

```python
from src.keepass import ProgramSettings

settings = ProgramSettings()
try:
    settings._load_facebook_credentials()
    logger.info("Facebook credentials loaded successfully.")
except Exception as ex:
    logger.error("Error loading Facebook credentials:", ex, exc_info=True)
```

### `_load_google_api_credentials`

**Purpose**:  This method loads credentials for Google API service.

**Parameters**:

- None

**Returns**:

- None

**Raises Exceptions**:

- `Exception`:  If an error occurs during the loading process.

**How the Function Works**:

1. Searches for a group named `google/gapi`.
2. Extracts `api_key` from custom properties of the entry.
3. Stores this value in the `ProgramSettings.credentials.gapi` attribute.

**Examples**:

```python
from src.keepass import ProgramSettings

settings = ProgramSettings()
try:
    settings._load_google_api_credentials()
    logger.info("Google API credentials loaded successfully.")
except Exception as ex:
    logger.error("Error loading Google API credentials:", ex, exc_info=True)
```

### `get_credentials`

**Purpose**:  This method returns the `credentials` attribute, providing access to the loaded credentials.

**Parameters**:

- None

**Returns**:

- `SimpleNamespace`:  The `credentials` attribute, containing credentials for different services.

**Raises Exceptions**:

- None

**How the Function Works**:

1. Simply returns the `credentials` attribute.

**Examples**:

```python
from src.keepass import ProgramSettings

settings = ProgramSettings()
credentials = settings.get_credentials()
print(credentials.openai.api_key)
```

## Parameter Details

- `credentials` (`SimpleNamespace`): This attribute stores credentials for different services. It is a `SimpleNamespace` object, which allows accessing the credentials using attribute notation like `credentials.openai.api_key`. The `credentials` attribute is structured as follows:
    - `credentials.aliexpress`: Contains `api_key`, `secret`, `tracking_id`, `email`, and `password` for AliExpress.
    - `credentials.openai`: Contains `api_key`, `project_api`, and `assistant_id` for OpenAI.
    - `credentials.gemini`: Contains `api_key` for Gemini.
    - `credentials.telegram`: Contains `token` for Telegram.
    - `credentials.discord`: Contains `application_id`, `public_key`, and `bot_token` for Discord.
    - `credentials.presta`: 
        - `credentials.presta.client`:  A list of `SimpleNamespace` objects, each representing a PrestaShop client with `api_key`, `api_domain`, `db_server`, `db_user`, and `db_password`.
        - `credentials.presta.translations`: Contains `server`, `port`, `database`, `user`, and `password` for PrestaShop translations.
    - `credentials.smtp`: A list of `SimpleNamespace` objects, each representing an SMTP server with `server`, `port`, `user`, and `password`.
    - `credentials.facebook`: A list of `SimpleNamespace` objects, each representing a Facebook app with `app_id`, `app_secret`, and `access_token`.
    - `credentials.gapi`:  Contains `api_key` for Google API.

## Examples

```python
from src.keepass import ProgramSettings

# Get the instance of ProgramSettings
settings = ProgramSettings()

# Accessing credentials for different services
aliexpress_api_key = settings.get_credentials().aliexpress.api_key
openai_api_key = settings.get_credentials().openai.api_key
gemini_api_key = settings.get_credentials().gemini.api_key
telegram_token = settings.get_credentials().telegram.token
discord_bot_token = settings.get_credentials().discord.bot_token
presta_client1 = settings.get_credentials().presta.client[0]  # First PrestaShop client
presta_translations = settings.get_credentials().presta.translations
smtp_server = settings.get_credentials().smtp[0]  # First SMTP server
facebook_app = settings.get_credentials().facebook[0]  # First Facebook app
google_api_key = settings.get_credentials().gapi.api_key

# Output the credentials (example)
print(f"AliExpress API Key: {aliexpress_api_key}")
print(f"OpenAI API Key: {openai_api_key}")
print(f"Gemini API Key: {gemini_api_key}")
print(f"Telegram Token: {telegram_token}")
print(f"Discord Bot Token: {discord_bot_token}")
print(f"PrestaShop Client 1: {presta_client1}")
print(f"PrestaShop Translations: {presta_translations}")
print(f"SMTP Server: {smtp_server}")
print(f"Facebook App: {facebook_app}")
print(f"Google API Key: {google_api_key}")
```