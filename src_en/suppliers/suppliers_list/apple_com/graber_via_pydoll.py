## \file /src/suppliers/suppliers_list/apple_com/graber_via_pydoll.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.apple_com.graber_via_pydoll
    :platform: Windows, Unix
    :synopsis: Module for collecting data from Apple using the `pydoll` library.

Apple Data Graber via Pydoll
=========================================================================================

This module provides a `Graber` class designed to extract product and category information from Apple
using the `pydoll` library, extending the base Graber functionality.

Example usage
-------------

```python
    from src.webdriver.selenium.driver import Driver
    from src.suppliers.suppliers_list.apple_com.graber_via_pydoll import Graber

    # Initialize a WebDriver instance (e.g., Chrome)
    driver_instance = Driver(browser_name="Chrome")

    # Initialize the Apple Graber
    apple_graber = Graber(driver=driver_instance, lang_index=0) # Assuming lang_index is needed

    # Now you can use apple_graber methods to interact with Apple
    # For example, to grab product details from a URL:
    # product_data = apple_graber.grab_product_details("https://www.apple.com/shop/product/...")
    # print(product_data)

    # Don't forget to quit the driver when done
    # driver_instance.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/apple_com/graber_via_pydoll.py
"""
        
