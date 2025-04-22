## \file /sandbox/davidka/process_scenarios_for_train.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль сбора датасета для обучения модели на основе данных о товарах
======================================================================

```rst
.. module:: sandbox.davidka.process_scenarios_for_train
	:platform: Windows, Unix
	:synopsis: Запуск сцеанриев различных поставщиков для сбора датасета с параметрами товаров
```
"""
import os
import asyncio
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, List
from dataclasses import dataclass, field

import header
from header import __root__

# External modules
from src import gs
#from src.suppliers.suppliers_list import *
from src.suppliers.get_graber_by_supplier  import get_graber_by_supplier_prefix, get_graber_by_supplier_url
from src.webdriver.driver import Driver
#from src.webdriver.chrome import Chrome
from src.webdriver.firefox import Firefox
#from src.llm.gemini import GoogleGenerativeAi
#from src.llm.openai.model import OpenAIModel
from src.endpoints.prestashop.product import PrestaProduct
from src.endpoints.prestashop.language import PrestaLanguage
from src.endpoints.prestashop.product_fields import ProductFields
from src.endpoints.advertisement.facebook.scenarios.post_message import (
    post_message,
)
from src.utils.file import read_text_file, save_text_file, get_filenames_from_directory
from src.utils.printer import pprint as print
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.image import get_image_bytes, get_raw_image_data
from src.utils.string.ai_string_utils import normalize_answer, string_for_train
from src.utils.string.html_simplification import simplify_html, strip_tags 
from src.logger.logger import logger


class Config:


    scenarios:dict = j_loads('scenarios/scenarios.json')

async def process_scenarios(driver:Driver, scenarios_list:List[dict]) -> bool:
    """Исполняет сценарии для сбора товаров от поставщиков"""
    train_data_list:list = []

    for scenario in scenarios_list:
        graber:'Graber' = get_graber_by_supplier_prefix(driver, scenario['supplier_prefix'], lang_index = 2)
        driver.get_url(scenario['train_product_url'])
        process_fields:tuple = (
                    'id_product',
                    'name',
                    'description_short',
                    'description',
                    'specification',
                    'local_image_path',
                    'id_category_default',
                    'additional_category',
                    'default_image_url',
                    'price')
        raw_data:str = driver.fetch_html()
        cleared_data:str =  strip_tags(raw_data)
        if not raw_data:
            logger.error(f"Failed to fetch HTML from {scenario['train_product_url']}")
            ...
            continue

        f:'ProductFields' = await graber.grab_page_async(*process_fields)
        res_dict:dict = f.to_dict()
       
        
        train_data_list.append({
             'text_input': string_for_train(cleared_data) ,
             'output': string_for_train(str(res_dict)),
        })
        logger.info(f'\n2 Ввод:\n\t2 {cleared_data}')
        logger.info(f'\n2 Вывод:\n\t2 {print(res_dict)}')
        timestamp = gs.now
        save_text_file(raw_data, __root__ / 'SANDBOX' / 'davidka' / 'raw_data_products' / f'raw-{timestamp}.html')
        save_text_file(cleared_data, __root__ / 'SANDBOX' / 'davidka' / 'raw_data_products' / f'raw-{timestamp}.txt')

    j_dumps(train_data_list, __root__ / 'SANDBOX' / 'davidka' / 'train_data_products' / f'train-{gs.now}.json')
    ...


def main():
    """"""
    #d = Driver(Firefox, window_mode = 'headless')
    d = Driver(Firefox)
    asyncio.run(process_scenarios(d,Config.scenarios))

if __name__ == '__main__':
    main()