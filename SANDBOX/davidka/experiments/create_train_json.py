## \file /sandbox/davidka/create_train_json.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора данных из файлов JSON в train_data в один большой файл
=====================================================
```rst
.. module:: sandbox.davidka.create_train_json
```
"""

import asyncio
import random
from types import SimpleNamespace
from urllib.parse import urlparse
from pathlib import Path

import header
from header import __root__
from src import gs
from src.webdriver.llm_driver.simple_driver import SimpleDriver
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.file import read_text_file, save_text_file, get_filenames_from_directory, recursively_yield_file_path
from src.utils.url import get_domain
from src.utils.printer import pprint as print
from src.logger import logger

class Config:
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    config:SimpleNamespace = j_loads_ns(ENDPOINT/'davidla.json')
    mining_data_path: Path = ENDPOINT / 'random_urls'
    train_data_products_dir: Path = ENDPOINT / 'train_data_products'
    output_product_data_dir: Path = ENDPOINT / 'output_product_data'
    checked_domains: list = read_text_file(ENDPOINT / 'checked_domains.txt', as_list=True)
    crawl_files_list: list = get_filenames_from_directory(mining_data_path, 'json')
    instruction_grab_product_page_simple_driver: str = (ENDPOINT / 'instructions' / 'grab_product_page_simple_driver.md').read_text(encoding='utf-8')
    instruction_get_supplier_categories: str = (ENDPOINT / 'instructions' / 'get_supplier_categories.md').read_text(encoding='utf-8')
    instruction_find_product_in_supplier_domain: str = (ENDPOINT / 'instructions' / 'find_product_in_supplier_domain.md').read_text(encoding='utf-8')
    instruction_for_products_urls_one_product: str = (ENDPOINT / 'instructions' / 'get_product_links_one_product.md').read_text(encoding='utf-8')
    instruction_links_from_search: str = (ENDPOINT / 'instructions' / 'links_from_search.md').read_text(encoding='utf-8')
    instruction_links_from_searh_page: str = (ENDPOINT / 'instructions' / 'links_from_searh_page.md').read_text(encoding='utf-8')
    GEMINI_API_KEY = gs.credentials.gemini.katia.api_key
    driver: SimpleDriver = SimpleDriver(gemini_model_name='gemini-1.5-flash-8b-exp-0924', GEMINI_API_KEY=GEMINI_API_KEY)


for file in 