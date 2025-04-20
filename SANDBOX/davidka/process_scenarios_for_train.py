## \file /sandbox/davidka/process_scenarios_for_train.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: sandbox.davidka.process_scenarios_for_train
	:platform: Windows, Unix
	:synopsis: Запуск сцеанриев различных поставщиков для сбора датасета с параметрами товаров

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
from src.logger.logger import logger

class Config:

    scenario_hb:dict = {
        "supplier_prefix":"hb",
       "url": "https://hbdeadsea.co.il/product-category/aromatherapy/diffusers/",
        "train_product_url":"https://hbdeadsea.co.il/product/%d7%a7%d7%a8%d7%9d-%d7%a8%d7%92%d7%9c%d7%99%d7%99%d7%9d-%d7%90%d7%99%d7%a0%d7%98%d7%a0%d7%a1%d7%99%d7%91%d7%99-%d7%9e%d7%95%d7%a2%d7%a9%d7%a8-%d7%91%d7%91%d7%95%d7%a5-%d7%9e%d7%99%d7%9d-%d7%94%d7%9e-2/",
       "name": "מפיצי ריח ומילוי",
       "condition": "new",
       "presta_categories": {
         "default_category": 11246,
         "additional_categories": []
       }
    }
    scenario_etzmaleh:dict = {
        "supplier_prefix":"etzmaleh",
        "url":"https://www.etzmaleh.co.il/montessori_collection",
        "train_product_url":"https://www.etzmaleh.co.il/montessori_transition_bed",
        "name":"הקולקציה המונטסורית",
        "condition":"new",
           "presta_categories": {
         "default_category": 11390,
         "additional_categories": [11389]
       }
    }
    scenario_amazon:dict =  {
        "supplier_prefix":"amazon",
          "url": "https://amzn.to/3OhRz2g",
            "train_product_url":"https://www.amazon.com/C%C3%A1-dOro-Hippie-Colored-Murano-Style/dp/B09N53XSQB/ref=sr_1_2_sspa?crid=24Q0ZZYVNOQMP&dib=eyJ2IjoiMSJ9.WhN_5Deyh2Yz9gRyrG1anDCr1UB8tnpHH_pJePpURaaciFWg_5Ft0XuS-e3A67g3rO1RECMmgpmRLEJOI7Zj6JyAd9DJh6dLSwUcHgHnJiKhmBmpa-AlDotmiq0-4Q_b90WkEmSsgIzC4L1Yc_KssvHa7bj6LGl6fMM4VuctS4nDQ3vYigYzB3jzP9Q3nT5BRv5_yRigaF-hDpPc0lL5wvo5gQ4i-9Jcy4vHyHNX04ZpoQBXrwcwLo3XWoruWSmnrgvQ5XxRzLntClGxBSN3cTjsunsHYzzKSp_VYx631JM.U1bRX0eDJ5c13nETwkLbN9BPt6-OtTKUvvRQiGodOd0&dib_tag=se&keywords=Art+Deco+murano+glass&linkCode=sl2&linkId=1a5da5b6a02f09a4d8fe47362e06cf3a&qid=1745171225&sprefix=art+deco+murano+glass%2Caps%2C230&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
          "condition": "new",
          "presta_categories": {
            "default_category": 11209,
            "additional_categories": [ 11206, 11388 ]
          }
        }
    scenario_aliexpress:dict =  {
        "supplier_prefix":"aliexpress",
          "url": "https://www.aliexpress.com",
        "train_product_url":"https://www.aliexpress.com/item/1005008108060545.html?spm=a2g0o.tm1000020483.d1.1.28f9474cPkErMV&sourceType=561&pvid=1a630f56-af44-4a5e-8fa6-ba39f7382734&pdp_ext_f=%7B%22ship_from%22:%22CN%22,%22sku_id%22:%2212000043799911402%22%7D&scm=1007.28480.422277.0&scm-url=1007.28480.422277.0&scm_id=1007.28480.422277.0&pdp_npi=4%40dis%21ILS%21%E2%82%AA%20119.48%21%E2%82%AA%2058.54%21%21%21231.15%21113.26%21%402141131717451712898942519ec7de%2112000043799911402%21gsd%21IL%213690978535%21&channel=sd&aecmd=true",
          "condition": "new",
          "presta_categories": {
            "default_category": 4292,
            "additional_categories": []
          }
        }

    scenarios_list:list = [scenario_hb,]

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
        res:'ProductFields' = await graber.grab_page_async(*process_fields)
        res_dict:dict = res.to_dict()
        raw_data:str = driver.fetch_html()
        train_data_list.append({
             'text_input': string_for_train(str(raw_data)) ,
             'output': string_for_train(str(res_dict)),
        })
    j_dumps(train_data_list, __root__ / 'SANDBOX' / 'davidka' / 'train_data_products' / f'train-{gs.now}.json')
    ...


def main():
    """"""
    #d = Driver(Firefox, window_mode = 'headless')
    d = Driver(Firefox)
    asyncio.run(process_scenarios(d,Config.scenarios_list))

if __name__ == '__main__':
    main()