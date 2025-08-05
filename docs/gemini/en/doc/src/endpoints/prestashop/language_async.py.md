# PrestaShop Language API Async

## Overview

This module provides an asynchronous interface for interacting with the PrestaShop language settings API. It inherits from the `PrestaShopAsync` base class, allowing for asynchronous operations related to managing languages within a PrestaShop store.

## Details

The `PrestaLanguageAync` class simplifies interactions with the PrestaShop API, allowing you to easily perform operations such as:

- **Retrieving language names by index:**  The `get_lang_name_by_index()` method retrieves the ISO language code based on its index in the PrestaShop language table.

- **Retrieving language schema:** The `get_languages_schema()` method retrieves the entire language schema from the PrestaShop API, providing details about each available language.

## Classes

### `PrestaLanguageAync`

**Description**: This class represents the asynchronous interface for managing PrestaShop language settings. It inherits from `PrestaShopAsync`, which handles communication with the PrestaShop API.

**Inherits**: `PrestaShopAsync`

**Attributes**:

- `lang_string` (str):  ISO language code (e.g., 'en', 'ru', 'he').

**Methods**:

- `get_lang_name_by_index(lang_index:int|str ) -> str`:  Retrieves the ISO language code based on its index in the PrestaShop language table.

- `get_languages_schema() -> dict`: Retrieves the entire language schema from the PrestaShop API.

**Examples**:

```python
# Creating a PrestaLanguageAync instance
lang_class = PrestaLanguageAync()

# Retrieving the language schema
languagas_schema = await lang_class.get_languages_schema()

# Printing the language schema
print(languagas_schema)
```

## Functions

### `main()`

**Purpose**: This function serves as the entry point for the asynchronous execution of the module. It demonstrates how to utilize the `PrestaLanguageAync` class for retrieving the language schema.

**How the Function Works**:

- Creates an instance of the `PrestaLanguageAync` class.
- Calls the `get_languages_schema()` method to retrieve the language schema asynchronously.
- Prints the retrieved language schema to the console.

**Examples**:

```python
# Running the main function
asyncio.run(main())
```

## Parameter Details

### `lang_index` (int|str)

- **Description**: The index of the language in the PrestaShop language table. This value can be an integer or a string representation of the index.

## Examples

```python
# Creating a PrestaLanguageAync instance with API domain and API key
lang_class = PrestaLanguageAync(API_DOMAIN='your_api_domain', API_KEY='your_api_key')

# Retrieving the language name for index 1
lang_name = await lang_class.get_lang_name_by_index(1)
print(f'Language name for index 1: {lang_name}')

# Retrieving the language schema
language_schema = await lang_class.get_languages_schema()
print(f'Language schema:\n{language_schema}')
```