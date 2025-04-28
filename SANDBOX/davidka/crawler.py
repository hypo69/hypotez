## \file /sandbox/davidka/crawler.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора данных со страниц товаров с различных сайтов
=====================================================


```rst
.. module:: sandbox.davidka.crawler
```
"""
import asyncio, random
from pathlib import Path
from types import SimpleNamespace


import header
from header import __root__
from src import gs
from src.webdriver.llm_driver import Driver
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.file import read_text_file, save_text_file, get_filenames_from_directory 
from src.utils.url import get_domain
from src.utils.string.ai_string_utils import normalize_answer

from src.utils.printer import pprint as print
from src.logger.logger import logger

class Config:
    ENDPOINT:Path = __root__/'SANDBOX'/'davidka'
    mining_data_path:Path = ENDPOINT/'random_urls'
    train_data_supplier_categories_path:Path = ENDPOINT/'train_data_supplier_categories'
    checked_domains:list = read_text_file(ENDPOINT/'checked_domains.txt',as_list=True)
    crawl_files_list:list = get_filenames_from_directory(mining_data_path, 'json')
    instruction_grab_product_page:str =  Path(ENDPOINT/ 'instructions'/ 'grab_product_page.md').read_text(encoding='utf-8')
    instruction_get_supplier_categories:str =  Path(ENDPOINT/ 'instructions'/ 'get_supplier_categories.md').read_text(encoding='utf-8')
    instruction_find_product_in_supplier_domain:str =  Path(ENDPOINT/ 'instructions'/ 'find_product_in_supplier_domain.md').read_text(encoding='utf-8')
    driver:Driver = Driver()

def get_products_urls_list_from_files(crawl_files_list:list = []) -> list:
    """
   Функция читает содержимое файлов  в директории `mining_data`, перемешивает их и возвращает одним большим списком
   """
    products_urls_list = []
    for filename in crawl_files_list or Config.crawl_files_list:
        try:
            file_path = Config.mining_data_path / filename
            crawl_data = j_loads(file_path)['products']
            for product in crawl_data:
                products_urls_list.append(product['product_url'])
        except Exception as ex:
            logger.error(f'Ошибка при обработке файла/n {filename=}/n', ex)
            ...
    random.shuffle(products_urls_list)
    return products_urls_list if isinstance(products_urls_list, list) else [products_urls_list]

def yield_product_urls_from_files(directory: Path = Config.mining_data_path, pattern: str = 'json'):
    """
    Функция возвращает генератор списка `url` Применяется на больших объемах данных
    """
    filenames = get_filenames_from_directory(directory, pattern)
    for filename in filenames:
        try:
            file_path = directory / filename
            crawl_data = j_loads(file_path)['products']
            for product in crawl_data:
                yield product['product_url']
        except Exception as ex:
            logger.error(f'Ошибка при обработке файла {filename=}', ex)
            ...

def get_categories_from_random_urls(crawl_files_list:list = []) -> list:
    """Возвращает все категории из файлов словарей для майнинга"""
    categories_list:list = []
    for filename in crawl_files_list or Config.crawl_files_list:
        try:
            file_path = Config.mining_data_path / filename
            crawl_data = j_loads(file_path)
            if 'products' in crawl_data:
                crawl_data = crawl_data['products']
            else:
                ...
            for product in crawl_data:
                try:
                    categories_list.append(product['parent_category'])
                except:
                    ...
                try:    
                    categories_list.append(product['category_name'])
                except:
                    ...
        except Exception as ex:
            logger.error(f'Ошибка при обработке файла/n {filename=}/n', ex)
            ...
            return categories_list
            ...
    categories_list = list(set(categories_list))
    random.shuffle(categories_list)
    return categories_list 

async def get_products_by_category(category:str, num_of_links:str = '2'):
        try:
            driver:Driver = Config.driver
            logger.info(f'Обработка {category=}')
            task = Config.instruction_grab_product_page.replace('{PRODUCT_CATEGORY}', category).replace('{NUM_LINKS}', num_of_links)
            extracted_data = await driver.run_task(task, use_gemini=True)
            print('\n -------------------------------- EXTRACTED DATA  ------------------------------------------')
            print(extracted_data)
            print('\n -------------------------------------------------------------------------------------------')
            ...
            return extracted_data
        except Exception as ex:
            logger.error(f'Ошибка при обработке {category=}', ex)
            ...
            return None

async def fetch_categories_from_suppliers_random_urls() -> dict:
    """"""
    categories_dict = {}
    driver:Driver = Config.driver

    for filename in Config.crawl_files_list:
        try:
            file_path = Config.mining_data_path / filename
            crawl_data = j_loads(file_path)
            if 'products' in crawl_data:
                crawl_data = crawl_data['products']
            else:
                ...
            for product in crawl_data:
                domain = get_domain(product['product_url'])
                if domain in Config.checked_domains:
                    continue
                task = Config.instruction_get_supplier_categories.replace('{INPUT_URL}', domain)
                res:str =  await driver.run_task(task, use_gemini=True)
                normilized_res:str = normalize_answer(res)
                data:dict = j_loads(normilized_res)
                print(data)
                j_dumps(data, Config.train_data_supplier_categories_path/f'{gs.now}.json')
                Config.checked_domains.append(domain)
                save_text_file(Config.checked_domains, Config.ENDPOINT/'checked_domains.txt')
                j_dumps(Config.checked_domains, Config.ENDPOINT/'checked_domains.json')
                ...
        except Exception as ex:
            logger.error(f'Ошибка при обработке файла/n {filename=}/n', ex)
            ...
    return categories_dict

async def main():
    """"""
    driver:Driver = Driver()
    # # ------------------ товары из списка -------------------
    # # # Через генератор для совсем больших данных
    # # # for product_url in yield_product_urls_from_files():
    # for product_url in get_products_urls_list_from_files():
    #     try:
    #         logger.info(f'Обработка URL: {product_url}')
    #         task = Config.instruction_grab_product_page.replace('<URL>', product_url)
    #         final_answer_stream, stream_chunks = await driver.stream_task(task, use_gemini=True)
    #         print(final_answer_stream)
    #         print(stream_chunks)
    #         ...
    #     except Exception as ex:
    #         logger.error(f'Ошибка при обработке {product_url=}', ex)


    # # ------------------ товары из категорий из списка -------------------
    # for category in get_categories_from_random_urls():
    #     await get_products_by_category(category,'1')

    # # # ------------------ Категории из URL -------------------
    # await fetch_categories_from_suppliers_random_urls()

    # ------------------ Ссылки на товары из списка доменов -------------------
    domains_list:list = read_text_file(Config.ENDPOINT/'checked_domains.txt', as_list=True)
    output_dict:dict = {}
    timestamp:str = gs.now
    for domain in domains_list:
        try:
            logger.info(f'Обработка домена: {domain}')
            print(f"\n------------------------\n Start find produtcs in the {domain}\n ------------------------------------\n")
            task = Config.instruction_find_product_in_supplier_domain.replace('{INPUT_URL}', domain)
            # final_answer_stream, stream_chunks = await driver.stream_task(task, use_gemini=True)
            # print(final_answer_stream)
            # print(stream_chunks)
            raw_res:str = await driver.run_task(task)
            clear_res:str = normalize_answer(raw_res)
            res_dict:dict = j_dumps(clear_res)
            output_dict.update( {domain:res_dict} )
            j_dumps(output_dict, Config.ENDPOINT/f'output_{timestamp}.json')
            
            ...
        except Exception as ex:
            logger.error(f'Ошибка при обработке {domain=}', ex)

    ...

asyncio.run(main())



