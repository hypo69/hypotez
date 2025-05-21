## \file /src/endpoints/emil/scenarios/run_scenarios.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Исполнитель сценариев для emil-design.com
===========================================
``rst
.. module:: src.endpoints.emil.scenarios.run_scenarios 
```
"""
from types import SimpleNamespace
from pathlib import Path

import header
from header import __root__
from src import gs
from src.webdriver import Driver, Firefox
from src.suppliers.suppliers_list.hb.categories_crawler import get_list_products_in_category as crawl_category_function
from src.suppliers.scenario.scenario_executor import run_scenario_file, run_scenario_files, run_scenarios, run_scenario

from src.utils.jjson import j_loads, j_loads_ns, j_dumps

class Config:
    ENDPOINT:Path = __root__ / 'endpoints' / 'emil'
    api_key:str = gs.credentials.prestashop.store_davidka_net.api_key
    api_domain:str = gs.credentials.prestashop.store_davidka_net.api_domain
    scenarios_from_suppliers_list:list = ['hb']

def run_scenarios(scenarios_from_suppliers:list):
    """"""
    ...
    driver:Driver = Driver(Firefox,window_mode='normal')
    suppliers_dir:Path = __root__ / 'src' / 'suppliers' / 'suppliers_list'
    for supplier_prefix in scenarios_from_suppliers:
        supplier_instance: SimpleNamespace = j_loads_ns( suppliers_dir /  supplier_prefix )[0]
        supplier_instance.locator = SimpleNamespace()
        supplier_instance.locator.product = j_loads_ns(suppliers_dir /  supplier_prefix / 'loctors' / 'product.json')
        supplier_instance.locator.category = j_loads_ns(suppliers_dir /  supplier_prefix / 'loctors' / 'category.json')
        supplier_scenario_files_list: list = list(map(lambda path: suppliers_dir / path, supplier_class.scenario_files))
        run_scenario_files(driver, supplier_instance, supplier_scenario_files_list, crawl_category_function )

if __name__ == '__main__':
    run_scenarios(Config.scenarios_from_suppliers_list)