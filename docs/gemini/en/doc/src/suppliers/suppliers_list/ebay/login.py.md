# Module: `src.suppliers.ebay.login`

## Overview

This module provides an authorization interface for eBay, specifically implemented for web drivers.

## Details

This module focuses on the authorization process for interacting with eBay using web drivers. It likely contains functions and classes related to logging in, handling authentication, and managing user sessions.

## Classes 

### `class EbayLogin`

**Description**:  A class for eBay login using web drivers.

**Attributes**:
-  `driver` (`Driver`): A web driver instance for controlling the browser, such as Chrome, Firefox, or Playwright.
-  `username` (`str`): The eBay username for logging in.
-  `password` (`str`): The eBay password for logging in.
-  `auth_url` (`str`): The URL for the eBay login page.

**Methods**:

-  `login()`: Attempts to log in to eBay using the provided username and password.
    **Parameters**:
        - `username` (`str`): The eBay username to use for login (optional).
        - `password` (`str`): The eBay password to use for login (optional).
    **Returns**:
        - `bool`: Returns `True` if the login was successful, otherwise `False`.
-  `is_logged_in()`: Checks if the user is currently logged in to eBay.
    **Returns**:
        - `bool`: Returns `True` if logged in, otherwise `False`.
-  `logout()`: Logs out of the eBay account.

## Inner Functions:

-  `get_login_page_elements(self) -> dict`: Returns a dictionary containing web elements (like username input, password input, login button) on the login page.
-  `validate_login(self) -> bool`: Checks if the login was successful by verifying the presence of specific elements on the logged-in page.

## How the Function Works:

The module implements a login process for eBay using a web driver to interact with the browser. The `EbayLogin` class encapsulates the login logic. The `login()` method likely automates the following steps:
1.  Navigates to the eBay login page using the provided `auth_url`.
2.  Finds the username, password, and login button elements using the `get_login_page_elements()` function.
3.  Enters the username and password into the corresponding input fields.
4.  Clicks the login button to initiate the authentication process.
5.  Validates the login by calling the `validate_login()` function, which checks for specific elements on the logged-in page to ensure successful authentication.
6.  Returns `True` if successful, `False` otherwise.

The `is_logged_in()` method likely verifies the user's logged-in state by checking for elements present only when logged in, like a user profile or logout button.

## Examples:

```python
from src.suppliers.ebay.login import EbayLogin
from src.webdriver import Chrome, Driver

# Create a driver instance (example with Chrome)
driver = Driver(Chrome)

# Create an eBayLogin instance
ebay_login = EbayLogin(driver, 'your_username', 'your_password', 'https://www.ebay.com/signin')

# Attempt login
if ebay_login.login():
    print('Login successful')
else:
    print('Login failed')

# Check if logged in
if ebay_login.is_logged_in():
    print('User is logged in')
else:
    print('User is not logged in')

# Log out
ebay_login.logout()

```

## Parameter Details:

-  `driver` (`Driver`): A web driver instance (Chrome, Firefox, Playwright).
-  `username` (`str`): The eBay username for login.
-  `password` (`str`): The eBay password for login.
-  `auth_url` (`str`): The URL of the eBay login page.

**Examples**:
-  `driver.execute_locator(l:dict)` -  The main command used in the code. It returns the value of the web element by locator.

**Code Example**: 

```python
from src.suppliers.ebay.login import EbayLogin
from src.webdriver import Chrome, Driver

# Create a driver instance (example with Chrome)
driver = Driver(Chrome)

# Create an eBayLogin instance
ebay_login = EbayLogin(driver, 'your_username', 'your_password', 'https://www.ebay.com/signin')

# Attempt login
if ebay_login.login():
    print('Login successful')
else:
    print('Login failed')

# Check if logged in
if ebay_login.is_logged_in():
    print('User is logged in')
else:
    print('User is not logged in')

# Log out
ebay_login.logout()

```