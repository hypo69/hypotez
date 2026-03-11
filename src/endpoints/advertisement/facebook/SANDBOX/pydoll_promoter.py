## \file /src/endpoints/advertisement/facebook/facebook_fields.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

import header 
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
from src.logger.logger import logger

import asyncio
from pydoll.constants import Key
from pydoll.browser.chromium.chrome import Chrome 

from src.webdriver.pydoll.tab import Tab
from src.webdriver.pydoll.options import Options
from src.webdriver.pydoll.browser import Browser

async with Browser( # <- you can substitute the browser class (Chrome, Edge) from from src.webdriver.pydoll.llib.browser here
                options = options,
                connection_port = get_free_port([9223, 9322])
                ) as browser:
    tab: Tab = await browser.start()
    if not tab:
        logger.error(f'Таб не появился')
...