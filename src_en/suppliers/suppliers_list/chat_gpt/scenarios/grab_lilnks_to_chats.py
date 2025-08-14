## \file /src/suppliers/suppliers_list/chat_gpt/scenarios/grab_lilnks_to_chats.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.chat_gpt.scenarios.grab_lilnks_to_chats
    :platform: Windows, Unix
    :synopsis: Module for grabbing chat links for ChatGPT.

ChatGPT Chat Link Grabber
=========================================================================================

This module provides functionality to extract links to individual chat conversations
from the ChatGPT web interface using a webdriver. It is noted that this functionality
may not work reliably with Chrome or Firefox drivers.

Example usage
-------------

```python
    from src.webdriver.selenium.driver import Driver
    from src.webdriver.firefox import Firefox
    from src.suppliers.suppliers_list.chat_gpt.scenarios.grab_lilnks_to_chats import get_links

    if __name__ == '__main__':
        driver = Driver(Firefox)
        driver.get_url('https://chatgpt.com/')
        chat_links = get_links(driver)
        if chat_links:
            for link in chat_links:
                print(f"Found chat link: {link}")
        else:
            print("No chat links found.")
        driver.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/chat_gpt/scenarios/grab_lilnks_to_chats.py
"""

###############################################################################################
#                                                                                             #
#                                                                                             #
#                   DOES NOT WORK WITH CHROME, FIREFOX DRIVERS                              #
#                                                                                             #
#                                                                                             #
###############################################################################################


import header
from src import gs
from src.webdriver.selenium.driver import Driver
from src.webdriver.chrome import Chrome
from src.webdriver.firefox import Firefox
from src.utils.jjson import j_loads_ns

locator = j_loads_ns(gs.path.src / 'suppliers' / 'chat_gpt' / 'locators' / 'chats_list.json')
def get_links(d:Driver):
    """Links to individual chats."""
    # TODO: Add logic to handle cases where no links are found or an error occurs.
    links = d.execute_locator(locator.link)
    return links

if __name__ == '__main__':
    d = Driver(Firefox)
    d.get_url('https://chatgpt.com/')
    links = get_links(d)
    # TODO: Add more robust handling of the 'links' variable, e.g., check if it's None or empty.
    # For demonstration, just printing the links.
    if links:
        for link in links:
            print(link)
    else:
        print("No links found.")
    d.quit()



