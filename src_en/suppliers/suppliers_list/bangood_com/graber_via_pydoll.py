## \file /src/suppliers/suppliers_list/bangood_com/graber_via_pydoll.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.bangood_com.graber_via_pydoll
    :platform: Windows, Unix
    :synopsis: Module for collecting data from Banggood using the `pydoll` library.

Banggood Data Graber via Pydoll
=========================================================================================

This module provides a `Graber` class designed to extract product and category information from Banggood
using the `pydoll` library, extending the base Graber functionality.

Example usage
-------------

```python
    from src.webdriver.selenium.driver import Driver
    from src.suppliers.suppliers_list.bangood_com.graber_via_pydoll import Graber

    # Initialize a WebDriver instance (e.g., Chrome)
    driver_instance = Driver(browser_name="Chrome")

    # Initialize the Banggood Graber
    bangood_graber = Graber(driver=driver_instance, lang_index=0) # Assuming lang_index is needed

    # Now you can use bangood_graber methods to interact with Banggood
    # For example, to grab product details from a URL:
    # product_data = bangood_graber.grab_product_details("https://www.banggood.com/item/...")
    # print(product_data)

    # Don't forget to quit the driver when done
    # driver_instance.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/bangood_com/graber_via_pydoll.py
"""
        
