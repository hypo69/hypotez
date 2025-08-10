## \file /src/suppliers/suppliers_list/findernet_com/login.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.findernet_com.login
    :platform: Windows, Unix
    :synopsis: Webdriver-based login interface for Findernet.

Findernet Login Interface
=========================================================================================

This module provides a login interface for Findernet using a webdriver.
It handles navigating to the login page, entering credentials, and submitting the form.

Example usage
-------------

```python
    from src.webdriver.selenium.driver import Driver
    from src.suppliers.supplier import Supplier # Assuming Supplier class is available
    from src.suppliers.suppliers_list.findernet_com.login import login

    # Initialize a WebDriver instance (e.g., Chrome)
    driver_instance = Driver(browser_name="Chrome")

    # Create a dummy supplier object with necessary attributes (locators, driver)
    # In a real scenario, this would be a properly configured Supplier instance
    class DummySupplier:
        def __init__(self, driver):
            self.driver = driver
            self.locators = {
                'login': {
                    'open_login_inputs': {'by': 'id', 'value': 'login-button'}, # Placeholder, replace with actual login locator
                    'email_input': {'by': 'id', 'value': 'username', 'action': 'send_keys', 'value': 'your_email@example.com'}, # Placeholder
                    'continue_button': {'by': 'id', 'value': 'next-button', 'action': 'click'}, # Placeholder
                    'password_input': {'by': 'id', 'value': 'password', 'action': 'send_keys', 'value': 'your_password'}, # Placeholder
                    'success_login_button': {'by': 'id', 'value': 'login-submit', 'action': 'click'} # Placeholder
                }
            }

    supplier_instance = DummySupplier(driver_instance)

    # Attempt to log in
    if login(supplier_instance):
        print("Successfully logged in to Findernet.")
    else:
        print("Failed to log in to Findernet.")

    # Don't forget to quit the driver when done
    # driver_instance.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/findernet_com/login.py
"""


"""   Supplier authorization functions """
...
from src.logger.logger import logger

def login(s) -> bool:
    """ Login function. 
   @param
        s - Supplier
    @returns
        True if login else False

   """
    return Truee