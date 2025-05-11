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
from src.llm.gemini import GoogleGenerativeAi
from src.webdriver.llm_driver.simple_driver import SimpleDriver
from src.goog.gtranslator.translator import translate_to
from src.utils.jjson import j_loads, j_loads_ns, j_dumps, find_keys
from src.utils.file import (
    read_text_file,
    save_text_file,
    get_filenames_from_directory,
    recursively_yield_file_path,
)
from src.utils.url import get_domain
from src.utils.printer import pprint as print
from src.logger import logger
from SANDBOX.davidka.utils.utils import get_categories_from_random_urls



class Config:
    ENDPOINT:Path  = __root__ / 'SANDBOX' / 'davidka'
    config:SimpleNamespace = j_loads_ns(ENDPOINT/'davidka.json') 
    STORAGE:Path = Path(config.storage)
    API_KEY = gs.credentials.google_custom_search.onela.api_key  # Получить здесь👉 https://developers.google.com/custom-search/v1/introduction
    CSE_ID = gs.credentials.google_custom_search.onela.cse_id  # Создайте здесь 👉 https://programmablesearchengine.google.com/about/ 
    GEMINI_API_KEY:str = gs.credentials.gemini.onela.api_key
    MODEL_NAME:str = 'gemini-2.0-flash-exp'

def google_search(query, api_key, cse_id, **kwargs) -> dict:
    """"""
    try:
        # Создабие сервиса для работы с Google Custom Search API
        service = build("customsearch", "v1", developerKey=api_key)
    
        # Выполнение запроса
        #res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
        return service.cse().list(q=query,  cx=cse_id).execute()
    except Exception as ex:
        logger.error(f'Ошибка поиска google custom search:' , ex)
        return {}

def extract_categories():
    """Вытаскивает категории из всех файлов """
    categories:list = []
    for source_dir in [Config.STORAGE/'data_by_supplier_test', Config.STORAGE/'random_urls_test']:
        for file in recursively_yield_file_path(source_dir, '*.json'):
            # Загрузка данных из файла
            data_dict = j_loads(file)
            if not data_dict:
                logger.warning(f'No data found in {file}')
                continue
            found = find_keys(data_dict, ['category','category_name','parent_category','parent_category_name'])
            if found['category']:
                categories.extend( found['category'] )
                print(f'Found categories in {file}: {found["category"]}')

            if found['category_name']:
                categories.extend( found['category_name'] )
                print(f'Found categories in {file}: {found["category_name"]}')

            if found['parent_category']:
                categories.extend( found['parent_category'] )
                print(f'Found categories in {file}: {found["parent_category"]}')

            if found['parent_category_name']:
                categories.extend( found['parent_category_name'] )
                print(f'Found categories in {file}: {found["parent_category_name"]}')

    if not categories:
        logger.warning(f'No categories found!')
        return []

    categories = list(set(categories))
    random.shuffle(categories)
    return categories

# extracted_categories:list = extract_categories()    
# categories_for_search:list = list(set(extracted_categories))
# save_text_file(categories_for_search, Config.STORAGE/'known_categories.txt')

categories_for_search_list:list = read_text_file(Config.STORAGE/'known_categories.txt', as_list=True)
#print(categories_for_search_list)
...

system_instruction:str = f"""

**System Instruction (English):**

Your task is to filter out categories that do **not** belong to the domain of **electronics and electrical devices**.

### ✔️ Categories that should be considered as electronics or electrical:

Include only categories related to:

* Consumer electronics (e.g., smartphones, TVs, laptops, tablets)
* Electrical appliances (e.g., refrigerators, washing machines, microwaves)
* Electrical components (e.g., cables, batteries, switches, sensors)
* Electronic accessories (e.g., chargers, adapters, headphones)
* Power tools or devices that require electricity to function
* Electrical infrastructure (e.g., circuit breakers, wiring, sockets)

### ❌ Categories that must be excluded:

Remove any categories unrelated to electronics or electricity, such as:

* Clothing (e.g., jackets, pants, underwear)
* Footwear (e.g., shoes, boots, sandals)
* Food and beverages (e.g., snacks, water, soda, alcohol)
* Furniture (e.g., chairs, beds, sofas, tables)
* Beauty and personal care (e.g., shampoo, makeup, soap)
* Toys, books, stationery, cleaning products, decor, sports equipment, etc.

### Return Behavior:

* If the category clearly **does not** belong to electronics/electrical: return `False`.
* If the category is **ambiguous**, apply conservative logic — **exclude it** unless it clearly belongs to electronics/electrical.
* If the category **belongs**, return `True`.
"""


model:GoogleGenerativeAi = GoogleGenerativeAi(model_name=Config.MODEL_NAME, api_key=Config.GEMINI_API_KEY, system_instruction=system_instruction,generation_config={'response_mime_type':'application/json'})
# cleared_categories_list = model.ask(categories_for_search_list)
# а_raw = read_text_file( Config.STORAGE/'known_categories_cleared.txt')
# а_clear = j_loads(а_raw)
# if isinstance(а_clear, str):
#     cleared_categories_list = list(а_clear) ################### <- ОСТОРОЖНО!!!!!
# ...
# save_text_file(а_clear, Config.STORAGE/'known_categories.txt')


for category in categories_for_search_list:
    # Запрос для поиска
    if_cat = model.ask(f'CATEGORY FOR CHECK: `{category}`. Check the category name. If the category does not belong to the section described in the system instruction, return False.')
    if if_cat.lower() in ('false','','none'):
        continue
    ...
    keywords:list = ['electronics','electricity','electronic components','components','devices','test and measuring equipment','sensors','energy',]
    query = f'''Give me a links for sections: {keywords} to products in the category '{category}' from different suppliers.'''
    
    #langs:list = ['en','ru','he','de','it','zh-cn','fr']

    translated_query:list[dict] = translate_to(query, 'en', ['de'])
    # Выполняем поиск
    links_dict:dict = {}
    for key, value in translated_query.items():
        kwargs:dict = {'num':15}
        results:dict = google_search(value, Config.API_KEY, Config.CSE_ID, **kwargs)  # num - количество результатов
        #print(results)
        # Выводим результаты
        if 'items' in results:
            for item in results['items']:
                links_dict.update({item['link']:
                                    {
                                        'category_name': category,
                                        'title': item['title'],
                                        'description': item.get('snippet', ''),
                                        'original_internal_url':item['link']
                                    }
                                })
            j_dumps(links_dict, Config.STORAGE / 'search_results' / f'{gs.now}.json')    
        else:
            print("Ничего не найдено.")



    