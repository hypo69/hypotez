## \file /src/suppliers/suppliers_list/atlascopco_com/graber_via_pydoll.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.atlascopco_com.graber_via_pydoll
    :platform: Windows, Unix
    :synopsis: Module for collecting data from Atlas Copco using the `pydoll` library.

Atlas Copco Data Graber via Pydoll
=========================================================================================

This module provides a `Graber` class designed to extract product and category information from Atlas Copco
using the `pydoll` library, extending the base Graber functionality.

Example usage
-------------

```python
    from src.webdriver.selenium.driver import Driver
    from src.suppliers.suppliers_list.atlascopco_com.graber_via_pydoll import Graber

    # Initialize a WebDriver instance (e.g., Chrome)
    driver_instance = Driver(browser_name="Chrome")

    # Initialize the Atlas Copco Graber
    atlascopco_graber = Graber(driver=driver_instance, lang_index=0) # Assuming lang_index is needed

    # Now you can use atlascopco_graber methods to interact with Atlas Copco
    # For example, to grab product details from a URL:
    # product_data = atlascopco_graber.grab_product_details("https://www.atlascopco.com/en-us/product/...")
    # print(product_data)

    # Don't forget to quit the driver when done
    # driver_instance.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/atlascopco_com/graber_via_pydoll.py
"""
        
