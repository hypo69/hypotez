# # \file /src/suppliers/suppliers_list/amazon_com/login.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3
""".. module:: src.suppliers.suppliers_list.amazon_com.login
    :platform: Windows, Unix
    :synopsis: Webdriver-based login interface for Amazon.

Amazon Login Interface
=========================================================================================

This module provides a login interface for Amazon using a webdriver.
It handles navigating to the login page, entering credentials, and submitting the form.

Example usage
-------------

```python
    from src.webdriver.selenium.driver import Driver
    from src.suppliers.supplier import Supplier # Assuming Supplier class is available
    from src.suppliers.suppliers_list.amazon_com.login import login

    # Initialize a WebDriver instance (e.g., Chrome)
    driver_instance = Driver(browser_name="Chrome")

    # Create a dummy supplier object with necessary attributes (locators, driver)
    # In a real scenario, this would be a properly configured Supplier instance
    class DummySupplier:
        def __init__(self, driver):
            self.driver = driver
            self.locators_store = {
                'login': {
                    'open_login_inputs': {'by': 'id', 'value': 'nav-link-accountList'},
                    'email_input': {'by': 'id', 'value': 'ap_email', 'action': 'send_keys', 'value': 'your_email@example.com'},
                    'continue_button': {'by': 'id', 'value': 'continue', 'action': 'click'},
                    'password_input': {'by': 'id', 'value': 'ap_password', 'action': 'send_keys', 'value': 'your_password'},
                    'keep_signed_in_checkbox': {'by': 'name', 'value': 'rememberMe', 'action': 'click'},
                    'success_login_button': {'by': 'id', 'value': 'signInSubmit', 'action': 'click'}
                }
            }

    supplier_instance = DummySupplier(driver_instance)

    # Attempt to log in
    if login(supplier_instance):
        print("Successfully logged in to Amazon.")
    else:
        print("Failed to log in to Amazon.")

    # Don't forget to quit the driver when done
    # driver_instance.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/amazon_com/login.py"""


from src.logger.logger import logger

def login(s) -> bool:
    """Login function. 
   @param
        S - Supplier
    @returns
        True if Login Else False"""
    _l : dict = s.locators_store['login']
    _d = s.driver
    _d.window_focus()
    _d.get_url('https://amazon.com/')
    # _d.wait(.7)

    # _d.fullscreen_window()
    
    # _d.fullscreen_window()
    if not _d.click(_l['open_login_inputs']):
        _d.refresh()
        _d.window_focus()
        if not _d.click(_l['open_login_inputs']):
            '''Here you need to look for a login button in another place'''
            logger.debug('''Here you need to look for a login button in another place''')
        ...
    # _d.wait(2)

    
    if not _d.execute_locator(_l['email_input']): 
        return
        ... # TODO FALSE processing logic

    _d.wait(.7)
    if not _d.execute_locator(_l['continue_button']):
       ... # TODO FALSE processing logic
    _d.wait(.7)
    if not _d.execute_locator(_l['password_input']): 
        ... # TODO FALSE processing logic
    _d.wait(.7)
    if not _d.execute_locator(_l['keep_signed_in_checkbox']):
        ...
    _d.wait(.7)
    if not _d.execute_locator(_l['success_login_button']):
       ... # TODO FALSE processing logic
    if _d.current_url == "https://www.amazon.com/ap/signin":
        logger.error(f'''Unsuccessful login''')
        ...
        return
    _d.wait(1.7)
    _d.maximize_window()
    # _d.dump_cookies_to_file()
    logger.info(f'''Poglined ...''')
    return Truee