## \file /src/suppliers/suppliers_list/aliexpress_com/affiliate_links_shortener_scenario.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.scenarios
    :platform: Windows, Unix
    :synopsis: Link shortener via web browser.

This module provides functionality to shorten affiliate links for AliExpress
using a web browser, handling the process of inputting URLs, clicking buttons,
and extracting the shortened link.

Example usage
-------------

```python
    import asyncio
    from src.webdriver.selenium.driver import Driver
    from src.suppliers.suppliers_list.aliexpress_com.affiliate_links_shortener_scenario import get_short_affiliate_link

    async def main():
        # Assuming a Driver instance 'd' is available and initialized
        # d = Driver()
        # short_link = get_short_affiliate_link(d, "https://www.aliexpress.com/item/1005001234567890.html")
        # print(f"Shortened link: {short_link}")
        pass

    if __name__ == "__main__":
        asyncio.run(main())
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/affiliate_links_shortener_scenario.py
"""


from pathlib import Path
from typing import List, Union
from types import SimpleNamespace
import time
from src import gs
from src.utils.jjson import j_loads_ns, j_loads_ns
from src.logger.logger import logger
from src.webdriver.selenium.driver import Driver

# Load locators from JSON file
locator = j_loads_ns(Path(gs.path.src, 'suppliers', 'aliexpress', 'locators', 'affiliate_links_shortener.json'))

def get_short_affiliate_link(d:Driver, url: str) -> str:
    """ Script for generating a shortened affiliate link
    @param url `str`: Full URL
    @returns `str`: Shortened URL
    """
    # Execute the scenario to get the short link
    d.execute_locator(locator.textarea_target_url, url)  # Enter URL into the input field
    d.execute_locator(locator.button_get_tracking_link)  # Click the button to get the short link
    d.wait(1)  # Wait 1 second for the page to update
    short_url = d.execute_locator(locator.textarea_short_link)[0]  # Get the short link from the element on the page
    main_tab = d.current_window_handle  # Save the ID of the main tab

    if len(short_url) < 1:
        logger.error(f"Failed to get short URL from {url}")  # Log error if short URL is not obtained
        #raise ValueError(f"Failed to get short URL from {url}")  # Raise exception to stop execution

    # Open a new tab with the short URL
    d.execute_script(f"window.open('{short_url}');")

    # Switch to the new tab
    d.switch_to.window(d.window_handles[-1])

    # Check that the short URL starts with the expected part
    if d.current_url.startswith('https://error.taobao.com'):
        logger.error(f"Incorrect URL: {d.current_url}")  # Log error if short URL is incorrect
        d.close()  # Close the tab with the incorrect URL
        d.switch_to.window(main_tab)  # Switch back to the main tab
        #raise ValueError(f"Incorrect URL: {d.current_url}")  # Raise exception to stop execution

    # Close the new tab and return to the main tab
    d.close()  # Close the new tab
    d.switch_to.window(main_tab)  # Switch back to the main tab

    return short_url  # Return the short URL
