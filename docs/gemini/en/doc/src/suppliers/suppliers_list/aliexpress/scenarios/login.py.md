# Module: `src.suppliers.aliexpress.scenarios.login`

## Overview

This module contains the `login` function, which is responsible for logging into AliExpress via WebDriver.

## Details

This function is used in the `hypotez` project to automate the login process for AliExpress suppliers. It uses WebDriver to navigate to the AliExpress website, locate and interact with elements on the page, and enter login credentials.

## Functions

### `login(s: Supplier) -> bool`

**Purpose**: This function logs into AliExpress via WebDriver using the provided `Supplier` object.

**Parameters**:

- `s` (`Supplier`): The `Supplier` object containing WebDriver instance and login details.

**Returns**:

- `bool`: `True` if the login was successful, `False` otherwise.

**Raises Exceptions**:

- `Exception`: If an error occurs during the login process.

**How the Function Works**:

1. Retrieves the WebDriver instance (`_d`) and login locators (`_l`) from the `Supplier` object.
2. Navigates to the AliExpress website using `_d.get_url()`.
3. Accepts cookies using `_d.execute_locator()`.
4. Opens the login page using `_d.execute_locator()`.
5. Locates the email and password input fields using `_d.execute_locator()` and checks if they are present. If not, it logs an error and continues (TODO: implement proper error handling).
6. Waits for the login button to appear using `_d.wait()`.
7. Clicks the login button using `_d.execute_locator()`.
8. (TODO: implement logic for setting language, currency, and shipping address).

**Examples**:

```python
from src.suppliers.suppliers_list.aliexpress.suppliers import Supplier
from src.suppliers.suppliers_list.aliexpress.scenarios.login import login

# Assuming you have a Supplier object `supplier` with initialized driver and locators
result = login(supplier)
if result:
    print("Login successful!")
else:
    print("Login failed.")
```

## Parameter Details

- `s` (`Supplier`): This parameter represents a `Supplier` object. This class is responsible for handling the specific details of the AliExpress supplier, including WebDriver instance, login locators, and other relevant data. 

**Inner Functions**:

- None

**Example**: 

```python
from src.suppliers.suppliers_list.aliexpress.suppliers import Supplier
from src.suppliers.suppliers_list.aliexpress.scenarios.login import login
from src.webdirver import Driver, Chrome

driver = Driver(Chrome) # Инициализация драйвера
supplier = Supplier('your_supplier_name', driver=driver, # Инициализация Supplier
                  locators={'login': {'cookies_accept': {'attribute': 'id', 'by': 'XPATH', 'selector': "//button[@id='onetrust-accept-btn-handler']", 'if_list': 'first', 'use_mouse': False, 'mandatory': False, 'timeout': 0, 'timeout_for_event': 'presence_of_element_located', 'event': 'click()', 'locator_description': 'Accept cookies'}, # Example of a locator definition
                            'open_login': {'attribute': 'id', 'by': 'XPATH', 'selector': "//button[contains(text(), 'Sign In')]", 'if_list': 'first', 'use_mouse': False, 'mandatory': False, 'timeout': 0, 'timeout_for_event': 'presence_of_element_located', 'event': 'click()', 'locator_description': 'Click on the login button'},
                            'email_locator': {'attribute': 'id', 'by': 'XPATH', 'selector': "//input[@id='fm-login-id']", 'if_list': 'first', 'use_mouse': False, 'mandatory': False, 'timeout': 0, 'timeout_for_event': 'presence_of_element_located', 'event': 'send_keys()', 'locator_description': 'Enter email'},
                            'password_locator': {'attribute': 'id', 'by': 'XPATH', 'selector': "//input[@id='fm-login-password']", 'if_list': 'first', 'use_mouse': False, 'mandatory': False, 'timeout': 0, 'timeout_for_event': 'presence_of_element_located', 'event': 'send_keys()', 'locator_description': 'Enter password'},
                            'loginbutton_locator': {'attribute': 'id', 'by': 'XPATH', 'selector': "//button[@id='fm-login-submit']", 'if_list': 'first', 'use_mouse': False, 'mandatory': False, 'timeout': 0, 'timeout_for_event': 'presence_of_element_located', 'event': 'click()', 'locator_description': 'Click on the login button'}},
                  credentials={'email': 'your_email', 'password': 'your_password'})

result = login(supplier)

if result:
    print("Login successful!")
else:
    print("Login failed.")
```