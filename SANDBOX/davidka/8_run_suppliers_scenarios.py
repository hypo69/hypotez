## \file /sandbox/davidka/experiments/8_run_suppliers_scenarios.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для запуска сценариев поставщиков
================================================================
Сценарии позволеют получить товары по поставщикам и по категориям


 ```rst
 .. module:: sandbox.davidka.experiments.8_run_suppliers_scenarios
 ```
"""
import asyncio
import importlib
import shutil 
import re
import sys
import argparse
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, Dict, Any, List, Tuple


import header
from header import __root__
from src import gs
from src.suppliers.suppliers_list import *
from src.suppliers.get_graber_by_supplier  import get_graber_by_supplier_prefix, get_graber_by_supplier_url
from src.suppliers.graber import Graber
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from src.webdriver.chrome import Chrome
from src.webdriver.executor_pydoll import Pydoll

from src.llm.gemini import GoogleGenerativeAi
from src.llm.openai.model import OpenAIModel
from src.endpoints.prestashop.product import PrestaProduct
from src.endpoints.prestashop.language import PrestaLanguage
from src.endpoints.prestashop.product_fields import ProductFields
from src.endpoints.advertisement.facebook.scenarios.post_message import (
    post_message,
)
from src.utils.file import read_text_file, save_text_file, get_filenames_from_directory

from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.image import get_image_bytes, get_raw_image_data
from src.logger.logger import logger



class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    SUPPLIERS_ENDPOINT:Path = __root__ / 'src' / 'suppliers' / 'suppliers_list'
    SCENARIOS_DIR:Path = __root__ /'SANDBOX' / 'davidka' / 'scenarios'
    config: SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json')
    scenarios_directory:Path = ENDPOINT / 'scenarios'
    scenarios_files:list = get_filenames_from_directory(scenarios_directory)


async def execute_scenario(supplier_prefix:str, scenario:dict, driver:Driver):
    """"""
    ...
    supplier_alias = supplier_prefix.replace('.','_').replace('-','_')
    if not 'url' in scenario:
        logger.debug('Возможно новый поставщик у которго еще нет сценария категориий')
        return

    
    graber: Graber = None
    try:
        supplier_path:Path = Config.SUPPLIERS_ENDPOINT / supplier_prefix 
        graber = get_graber_by_supplier_prefix(supplier_prefix)
        scenarios_dict: dict = j_loads(Config.SCENARIOS_DIR  / f'{supplier_prefix}.json')
        locators_path:Path = supplier_path / 'locators' 
        locator_product:SimpleNamespace = j_loads_ns(locators_path / 'product.json')
        locator_category:SimpleNamespace = j_loads_ns(locators_path / 'category.json')
        categories_crawler:Any = None
        
    except Exception as ex:
        logger.error(f'Непредвиденная ошибка', ex)
        ...
        return False

    driver.get_url(scenario['url'])  # <- страница категории товаров поставщика

    # Я отключил полноценный (мультистраничный) сценарий сбора коллекции товаров и пользуюсь примитивным
    # try:
    #     categories_crawler_module_path:str = f"src.suppliers.suppliers_list.{supplier_alias}.categories_crawler"
    #     categories_crawler = importlib.import_module(categories_crawler_module_path)
    # except Exception as ex:
    #     logger.error(f"Failed to import module `categories_crawler` '{supplier_prefix}'", ex)
    #     return False
    #
    # products_urls_list:list = categories_crawler.get_list_products_in_category()
    #

    products_urls_list:list = await driver.execute_locator(locator_category.product_links) 

    actual_fields:tuple = (
                            'name',
                            'id_supplier',
                            'description_short',
                            'description',
                            'specification',
                            'local_image_path',                      
                            'default_image_url',
                            'price'
                            )


    for url in products_urls_list:
        
        f:ProductFields = await graber.grab_page_async(*actual_fields, url=url)
        ...
        


   
        ...

async def main():
    """"""
    ...
    driver = Driver(Firefox, window_mode = 'normal')
    for scenario_file in Config.scenarios_files:
        ...
        scenarios_dict:dict | list = j_loads(Config.scenarios_directory / scenario_file)
        if not scenarios_dict: 
            continue # в случае ошибки чтения файла json
            
        if isinstance(scenarios_dict, dict):
            await execute_scenario(supplier_prefix = scenario_file.replace('.json',''), 
                             scenario = scenarios_dict, 
                             driver = driver)

        elif isinstance(scenarios_dict, list):
            for scenario in scenarios_dict:
                await execute_scenario(scenario_file.replace('.json',''), scenario, driver)
        ...

    

if __name__ == '__main__':
    asyncio.run(main())


