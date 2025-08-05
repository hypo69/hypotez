# Module for working with cookies
=================================================

This module provides functions for loading and managing cookies for various domains used by the project. It leverages the `browser_cookie3` package to read cookies from different browsers, allowing the project to maintain persistent user sessions.

## Table of Contents

- [Overview](#overview)
- [Classes](#classes)
    - [CookiesConfig](#cookiesconfig)
- [Functions](#functions)
    - [get_cookies](#get_cookies)
    - [set_cookies](#set_cookies)
    - [load_cookies_from_browsers](#load_cookies_from_browsers)
    - [set_cookies_dir](#set_cookies_dir)
    - [get_cookies_dir](#get_cookies_dir)
    - [read_cookie_files](#read_cookie_files)

## Overview

The module is responsible for the following:

- **Loading cookies from various browsers:**  The `get_cookies` function uses `browser_cookie3` to read cookies for a given domain from supported browsers.
- **Caching cookies:** Cookies are cached for performance and to avoid repeated loading.
- **Setting cookies:**  The `set_cookies` function allows the user to manually set cookies for a specific domain.
- **Reading cookies from files:**  The `read_cookie_files` function reads cookies from `.har` and `.json` files, allowing the project to use existing cookie data.
- **Managing cookies directory:** The `set_cookies_dir` and `get_cookies_dir` functions allow the user to configure the directory where cookies are stored.

## Classes

### `CookiesConfig`

**Description**: 
This class manages the configuration for storing cookies.

**Attributes**:

- `cookies` (Dict[str, Cookies]):  A dictionary storing cookies for different domains.
- `cookies_dir` (str): The directory where cookies are stored. 

## Functions

### `get_cookies`

**Purpose**:  Loads cookies for a given domain, potentially from browser cookies or from a cache.

**Parameters**:

- `domain_name` (str): The domain for which to load cookies.
- `raise_requirements_error` (bool): If `True`, raises an error if `browser_cookie3` is not installed. Defaults to `True`.
- `single_browser` (bool):  If `True`, stops searching for cookies after finding them in the first browser. Defaults to `False`.
- `cache_result` (bool):  If `True`, caches the loaded cookies for future use. Defaults to `True`.

**Returns**:

- `Dict[str, str]`: A dictionary of cookie names and values for the specified domain.

**Raises Exceptions**:

- `MissingRequirementsError`: If `browser_cookie3` is not installed and `raise_requirements_error` is `True`.

**How the Function Works**:

- First, checks if the cookies for the domain are already cached. If so, returns the cached cookies.
- If not cached, calls `load_cookies_from_browsers` to fetch cookies from browsers.
- Caches the loaded cookies if `cache_result` is `True`.
- Returns the loaded cookies.

**Examples**:

```python
# Load cookies for google.com
cookies = get_cookies("google.com")
print(cookies)

# Load cookies for google.com without caching
cookies = get_cookies("google.com", cache_result=False)
print(cookies)
```

### `set_cookies`

**Purpose**: Sets cookies for a given domain.

**Parameters**:

- `domain_name` (str): The domain for which to set cookies.
- `cookies` (Cookies):  A dictionary of cookies to set.

**Returns**:

- `None`

**How the Function Works**:

- Updates the `cookies` dictionary in `CookiesConfig` with the provided cookies.
- If no cookies are provided, removes existing cookies for the specified domain from the cache.

**Examples**:

```python
# Set cookies for google.com
cookies = {"cookie_name1": "value1", "cookie_name2": "value2"}
set_cookies("google.com", cookies)

# Remove cookies for google.com from cache
set_cookies("google.com")
```

### `load_cookies_from_browsers`

**Purpose**: Helper function to load cookies from various browsers.

**Parameters**:

- `domain_name` (str): The domain for which to load cookies.
- `raise_requirements_error` (bool): If `True`, raises an error if `browser_cookie3` is not installed. Defaults to `True`.
- `single_browser` (bool):  If `True`, stops searching for cookies after finding them in the first browser. Defaults to `False`.

**Returns**:

- `Cookies`: A dictionary of cookie names and values.

**How the Function Works**:

- Checks if `browser_cookie3` is installed. If not, raises an error or returns an empty dictionary.
- Iterates through supported browsers and attempts to load cookies using `browser_cookie3` functions.
- For each browser, filters out expired cookies and stores unique cookies in the `cookies` dictionary.
- If `single_browser` is `True`, breaks the loop after finding cookies in the first browser.
- Returns the `cookies` dictionary.

**Examples**:

```python
# Load cookies for google.com from all supported browsers
cookies = load_cookies_from_browsers("google.com")
print(cookies)

# Load cookies for google.com from all browsers, but stop after the first successful read
cookies = load_cookies_from_browsers("google.com", single_browser=True)
print(cookies)
```

### `set_cookies_dir`

**Purpose**: Sets the directory where cookies are stored.

**Parameters**:

- `dir` (str): The directory path.

**Returns**:

- `None`

**Examples**:

```python
# Set cookies directory to a custom path
set_cookies_dir("/path/to/cookies")
```

### `get_cookies_dir`

**Purpose**: Returns the directory where cookies are stored.

**Returns**:

- `str`: The cookies directory path.

**Examples**:

```python
# Get the current cookies directory
cookies_dir = get_cookies_dir()
print(cookies_dir)
```

### `read_cookie_files`

**Purpose**: Reads cookies from `.har` and `.json` files.

**Parameters**:

- `dirPath` (str): The directory path to read files from. Defaults to the value of `CookiesConfig.cookies_dir`.

**Returns**:

- `None`

**How the Function Works**:

- Checks if the provided directory is readable. If not, returns.
- Iterates through all files in the directory and its subdirectories, searching for `.har` and `.json` files.
- Reads the contents of each `.har` file as JSON and extracts cookies from the `entries` array.
- Reads the contents of each `.json` file as JSON and extracts cookies from the list of dictionaries.
- Stores the extracted cookies in the `CookiesConfig.cookies` dictionary.

**Examples**:

```python
# Read cookies from files in the default cookies directory
read_cookie_files()

# Read cookies from files in a custom directory
read_cookie_files("/path/to/cookies")
```