# # \file /src/suppliers/morlevi/_experiments/close_pop_up.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

"""Module: src.suppliers.morlevi._experments.close_pop_up
	: Platform: Windows, Unix
	: synopsis: checking the closing locator pop-up window"""

import header
from src import gs
from src.webdriver.selenium.driver import Driver
# from src.webdriver.chrome import Chrome
from src.webdriver.firefox import Firefox
from src.suppliers.morlevi.graber import Graber as MorleviGraber
from src.utils.jjson import j_loads_ns

driver = Driver(Firefox)
graber = MorleviGraber(driver)
driver.get_url('https://www.morlevi.co.il/product/19041')
product_id = graber.id_product
...