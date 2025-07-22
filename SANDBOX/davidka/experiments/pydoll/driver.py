## \file /SANDBOX/davidka/experiments/pydoll/driver.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
 Модуль экспериментов с PyDoll
 =========================================================
"""
import asyncio
from logging import config
from types import SimpleNamespace
from typing import Optional
from header import __root__
from src.webdriver.pydoll.driver import Driver, Tab
from src.utils.jjson import j_loads_ns

class Config:
    ...
    supplier_prefix:str = 'google.com'
    supplier_alias:str = supplier_prefix.replace('.', '_').replace('-', '_')
    ENDPOINT:str = fr'SANDBOX/davidka/experiments/pydoll/'
    SUPPPLIERS_DIR:str = f'src/suppliers/suppliers_list'
    @property
    def locators(self) -> Optional[SimpleNamespace]:
        return j_loads_ns(__root__ / self.SUPPLIERS_DIR / self.supplier_alias / 'locators' /'search_page.json')

    

async def driver_run():
    config = Config()

    async with Driver() as driver:
        tab: Tab = driver.tabs[0]
        await tab.go_to('https://www.google.com')
        #tab: Tab = await driver.new_tab('https://www.google.com')
        await tab.execute_locator(config.locators.input_field)
        ...

asyncio.run(driver_run())
