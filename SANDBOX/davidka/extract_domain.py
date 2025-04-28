## \file /sandbox/davidka/get_domain.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора вытаскивания домена из url
=====================================================
Модук вытаскивает домен из url и проверяет его на наличие в списке проверенных доменов


```rst
.. module:: sandbox.davidka.get_domain
```
"""
from pathlib import Path
import header
from header import __root__
from src.utils.file import read_text_file, save_text_file, get_filenames_from_directory
from src.utils.url import get_domain
from src.utils.jjson import j_loads, j_dumps

class Config:
    ENDPOINT:Path = __root__/'SANDBOX'/'davidka'

def extract_domain_from_products_urls() -> bool:
    """
    Функция вытаскивает домен из url в дiректории  `random_urls`
    """
    files_list:list = get_filenames_from_directory(Config.ENDPOINT/'random_urls', 'json')
    checked_domains:list = read_text_file(Config.ENDPOINT/'checked_domains.txt',as_list=True)
    for file in files_list:
        products_dict:dict = j_loads(Config.ENDPOINT/'random_urls'/file)
        if not products_dict: continue
        for product in products_dict['products']:
            product_url = product['product_url']
            domain = get_domain(product_url)
            if domain not in checked_domains:
                checked_domains.append(domain)
                save_text_file(checked_domains, Config.ENDPOINT/'checked_domains.txt')
                j_dumps(checked_domains, Config.ENDPOINT/'checked_domains.json')
    return True

extract_domain_from_products_urls()