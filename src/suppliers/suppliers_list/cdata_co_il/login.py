## \file /src/suppliers/suppliers_list/cdata_co_il/login.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.cdata_co_il.login
    :platform: Windows, Unix
    :synopsis: Webdriver-based login interface for Cdata (Israel).

Cdata (Israel) Login Interface
=========================================================================================

This module provides a login interface for Cdata (Israel) using a webdriver.
It handles navigating to the login page, entering credentials, and submitting the form.

Example usage
-------------

```python
    from src.webdriver.selenium.driver import Driver
    from src.suppliers.supplier import Supplier # Assuming Supplier class is available
    from src.suppliers.suppliers_list.cdata_co_il.login import login

    # Initialize a WebDriver instance (e.g., Chrome)
    driver_instance = Driver(browser_name="Chrome")

    # Create a dummy supplier object with necessary attributes (locators, driver)
    # In a real scenario, this would be a properly configured Supplier instance
    class DummySupplier:
        def __init__(self, driver):
            self.driver = driver
            self.locators = {
                'login': {
                    'email': 'your_email@example.com',
                    'password': 'your_password',
                    'email_locator': {'by': 'id', 'selector': 'username'}, # Placeholder, replace with actual locator
                    'password_locator': {'by': 'id', 'selector': 'password'}, # Placeholder
                    'loginbutton_locator': {'by': 'id', 'selector': 'loginButton'} # Placeholder
                }
            }

    supplier_instance = DummySupplier(driver_instance)

    # Attempt to log in
    if login(supplier_instance):
        print("Successfully logged in to Cdata (Israel).")
    else:
        print("Failed to log in to Cdata (Israel).")

    # Don't forget to quit the driver when done
    # driver_instance.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/cdata_co_il/login.py
"""


"""   Login interface. Webdriver implementation

@image html login.png
"""
def login(self):
    self.get_url('https://reseller.c-data.co.il/Login')

    emaiocators['login']['email']
    password = self.locators['login']['password']

    email_locator = (self.locators['login']['email_locator']['by'], 
                        self.locators['login']['email_locator']['selector'])

    password_locator = (self.locators['login']['password_locator']['by'],
                            self.locators['login']['password_locator']['selector'])

    loginbutton_locator =  (self.locators['login']['loginbutton_locator']['by'],
                                self.locators['login']['loginbutton_locator']['selector'])


    self.print(f''' email_locator {email_locator}
            password_locator {password_locator}
            loginbutton_locator {loginbutton_locator}''')

    self.find(email_locator).send_keys(email)
    self.find(password_locator).send_keys(password)
    self.find(loginbutton_locator).click()
    self.log('C-data logged in')
    return Truee