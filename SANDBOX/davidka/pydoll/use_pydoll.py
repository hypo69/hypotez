## \file src/endpoints/kazarinov/scenarios/scenario.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Use Pydoll
======================
this module show how to use pydoll to automate browser actions. 

"""

import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional, TYPE_CHECKING, TypeVar
import telebot

from header import __root__
from src import gs

from src.webdriver.pydoll.tab import Tab
from src.webdriver.pydoll.options import Options
from src.webdriver.pydoll.browser import Browser

from src.endpoints.kazarinov.report_generator.report_generator import ReportGenerator
from src.endpoints.kazarinov.scenarios.quotation_builder import QuotationBuilder
from src.endpoints.prestashop.product_fields.product_fields import ProductFields
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url

from src.utils.port import get_free_port
from src.logger.logger import logger
from src.utils.jjson import j_loads, j_loads_ns, j_dumps

async def main():
    """Example of launching the Browser and using it with a locator."""
    # Create a browser instance (default: headless mode from Options config)
    browser = Browser()

    # Use it as an async context manager
    async with browser as br:
        tab = await br.start()
        if not tab:
            logger.error("Failed to start the browser")
            return

        # Open a page
        await tab.go_to("https://toscrape.com/")

        # Execute a locator (example: take page title text)
        title_locator = {
            "attribute": "innerText",
            "by": "XPATH",
            "selector": "//h1"
        }

        try:
            result = await tab.execute_locator(title_locator)
            print("Page title:", result)
        except Exception as ex:
            logger.error("Error executing locator", ex, exc_info=True)

asyncio.run(main())
...