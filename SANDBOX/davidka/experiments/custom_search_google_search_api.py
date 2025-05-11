## \file /sandbox/davidka/custom_search_google_search_api.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль поискя страниц в Google по категориям
=====================================================
```rst
.. module:: sandbox.davidka.custom_search_google_search_api
```
"""
import asyncio
import random
from types import SimpleNamespace
from urllib.parse import urlparse
from pathlib import Path
from googleapiclient.discovery import build

# Локальные модули
import header
from header import __root__

from src import gs
from src.logger import logger
from src.webdriver.llm_driver.simple_driver import SimpleDriver

from src.utils.jjson import j_loads, j_loads_ns, j_dumps, find_keys
from src.utils.file import (
    read_text_file,
    save_text_file,
    get_filenames_from_directory,
    recursively_yield_file_path,
)
from src.utils.url import get_domain
from src.utils.printer import pprint as print

from SANDBOX.davidka.utils.utils import get_categories_from_random_urls



class Config:
    ENDPOINT:Path  = __root__ / 'SANDBOX' / 'davidka'
    config:SimpleNamespace = j_loads_ns(ENDPOINT/'davidka.json') 
    STORAGE:Path = Path(config.storage)
    API_KEY = gs.credentials.google_custom_search.onela.api_key  # Получить здесь: https://developers.google.com/custom-search/v1/introduction
    CSE_ID = gs.credentials.google_custom_search.onela.cse_id  # Создайте здесь: https://programmablesearchengine.google.com/about/    

def google_search(query, api_key, cse_id, **kwargs):
    # Создаем сервис для работы с Google Custom Search API
    service = build("customsearch", "v1", developerKey=api_key)
    
    # Выполняем запрос
    res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
    
    return res

def extract_categories():
    """"""
    categories:list = []
    for source_dir in [Config.STORAGE/'data_by_supplier_test', Config.STORAGE/'random_urls_test']:
        for file in recursively_yield_file_path(source_dir, '*.json'):
            # Загружаем данные из файла
            data_dict = j_loads(file)
            if not data_dict:
                logger.warning(f'No data found in {file}')
                continue
            found = find_keys(data_dict, ['category','category_name','parent_category','parent_category_name'])
            if found['category']:
                categories.extend( found['category'] )
                print(f'Found categories in {file}: {found["category"]}')

            if found['category_name']:
                categories.extend( found['category'] )
                print(f'Found categories in {file}: {found["category"]}')

            if found['category_name']:
                categories.extend( found['category'] )
                print(f'Found categories in {file}: {found["category"]}')

    if not categories:
        logger.warning(f'No categories found!')
        return []

    categories = list(set(categories))
    random.shuffle(categories)
    return categories

extgracted_categories:list = extract_categories()    
categories_for_search:list = list(set(extgracted_categories))
save_text_file(categories_for_search, Config.STORAGE/'known_categories.txt')


# for category in categories_for_search:
#     # Запрос для поиска

#     keywords:list = ['electronics','electricity','electronic components','components','devices','test and measuring equipment']
#     query = f"""Give me 10 links in the section `{keywords}` to products in the category '{category}'."""
    
#     # Выполняем поиск
#     results = google_search(query, Config.API_KEY, Config.CSE_ID, num=5)  # num - количество результатов
#     print(results)
#     # Выводим результаты
#     if 'items' in results:
#         for item in results['items']:
#             print(f"Заголовок: {item['title']}")
#             print(f"Ссылка: {item['link']}")
#             print(f"Описание: {item.get('snippet', 'Нет описания')}\n")
#     else:
#         print("Ничего не найдено.")