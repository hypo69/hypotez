## \file /src/endpoints/advertisement/facebook/start_posting_my_groups.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3




import header 
import copy
#from src.webdriver.selenium.driver import Driver, Chrome
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
from src.logger.logger import logger

import asyncio
from pydoll.browser.chrome import Chrome
from pydoll.constants import Key

async def main():
    async with Chrome() as browser:
        # Start the browser and get a new tab
        tab = await browser.start()

        # Navigate to Google
        await tab.go_to('https://www.google.com')

        # Find the search box by its attributes
        search_box = await tab.find(tag_name='textarea', name='q')

        # Type the search query and press Enter
        await search_box.insert_text('pydoll python')
        await search_box.press_keyboard_key(Key.ENTER)

        # Wait for the search results to appear
        await tab.wait_element(id='search')

        print("Search results are loaded!")

# Run the asynchronous main function
asyncio.run(main())

d = Driver(Chrome)
d.get_url(r"https://facebook.com")

filenames:list = ['my_managed_groups.json',]  

campaigns:list = ['brands',
                  'mom_and_baby',
                  'pain',
                  'sport_and_activity',
                  'house',
                  'bags_backpacks_suitcases',
                  'man']

promoter = FacebookPromoter(d, group_file_paths = filenames, no_video = True)

try:
    while True:
        
        promoter.run_campaigns(campaigns = copy.copy(campaigns), group_file_paths = filenames)
        ...

        
except KeyboardInterrupt:
    logger.info("Campaign promotion interrupted.")