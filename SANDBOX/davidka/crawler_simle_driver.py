## \file /sandbox/davidka/crawler_simple_driver.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора данных со страниц товаров через SimpleDriver
=====================================================
(адаптация исходного crawler.py)

.. module:: sandbox.davidka.crawler_simple_driver
"""

import asyncio
import random
from pathlib import Path

import header
from header import __root__
from src import gs
from src.webdriver.llm_driver.simple_driver import SimpleDriver
from src.utils.jjson import j_loads, j_dumps
from src.utils.file import read_text_file, save_text_file, get_filenames_from_directory
from src.utils.url import get_domain
from src.utils.string.ai_string_utils import normalize_answer
from src.utils.printer import pprint as print
from src.logger import logger


class Config:
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    mining_data_path: Path = ENDPOINT / 'random_urls'
    train_data_supplier_categories_path: Path = ENDPOINT / 'train_data_supplier_categories'
    checked_domains: list = read_text_file(ENDPOINT / 'checked_domains.txt', as_list=True)
    crawl_files_list: list = get_filenames_from_directory(mining_data_path, 'json')
    instruction_grab_product_page_simple_driver: str = (ENDPOINT / 'instructions' / 'grab_product_page_simple_driver.md').read_text(encoding='utf-8')
    instruction_get_supplier_categories: str = (ENDPOINT / 'instructions' / 'get_supplier_categories.md').read_text(encoding='utf-8')
    instruction_find_product_in_supplier_domain: str = (ENDPOINT / 'instructions' / 'find_product_in_supplier_domain.md').read_text(encoding='utf-8')
    instruction_for_products_urls: str = (ENDPOINT / 'instructions' / 'get_product_links.md').read_text(encoding='utf-8')
    GEMINI_API_KEY = gs.credentials.gemini.onela.api_key
    driver: SimpleDriver = SimpleDriver(gemini_model_name='gemini-2.5-flash-preview-04-17', GEMINI_API_KEY = GEMINI_API_KEY)


def get_products_urls_list_from_files(crawl_files_list: list = None) -> list:
    """Читает файлы с продуктами и возвращает product_url списком"""
    products_urls_list = []
    for filename in crawl_files_list or Config.crawl_files_list:
        try:
            file_path = Config.mining_data_path / filename
            crawl_data = j_loads(file_path)['products']
            for product in crawl_data:
                products_urls_list.append(product['product_url'])
        except Exception as ex:
            logger.error(f'Ошибка при обработке файла {filename=}', ex, exc_info=True)
    random.shuffle(products_urls_list)
    return products_urls_list


def yield_product_urls_from_files(directory: Path = Config.mining_data_path, pattern: str = 'json'):
    """Генератор url продуктов из файлов"""
    filenames = get_filenames_from_directory(directory, pattern)
    for filename in filenames:
        try:
            file_path = directory / filename
            crawl_data = j_loads(file_path)['products']
            for product in crawl_data:
                yield product['product_url']
        except Exception as ex:
            logger.error(f'Ошибка при обработке файла {filename=}', ex, exc_info=True)


def get_categories_from_random_urls(crawl_files_list: list = None) -> list:
    """Возвращает все категории из файлов продуктов"""
    categories_list = []
    for filename in crawl_files_list or Config.crawl_files_list:
        try:
            file_path = Config.mining_data_path / filename
            crawl_data = j_loads(file_path)
            crawl_data = crawl_data.get('products', [])
            for product in crawl_data:
                if 'parent_category' in product:
                    categories_list.append(product['parent_category'])
                if 'category_name' in product:
                    categories_list.append(product['category_name'])
        except Exception as ex:
            logger.error(f'Ошибка при обработке файла {filename=}', ex, exc_info=True)
    categories_list = list(filter(None, set(categories_list)))
    random.shuffle(categories_list)
    return categories_list


async def get_products_urls(category: str, num_of_links: str = '2'):
    """Получить товары по категории"""
    try:
        driver = Config.driver
        logger.info(f'Обработка {category=}')
        task = Config.instruction_for_products_urls.replace('{PRODUCT_CATEGORY}', category).replace('{NUM_LINKS}', num_of_links)
        extracted_data = await driver.simple_process_task_async(task)
        print('\n -------------------------------- EXTRACTED DATA \n------------------------------------------\n')
        print(extracted_data)
        print('\n -------------------------------------------------------------------------------------------')
        return extracted_data
    except Exception as ex:
        logger.error(f'Ошибка при обработке {category=}', ex, exc_info=True)
        return None


async def fetch_categories_from_suppliers_random_urls() -> dict:
    """Сбор категорий с сайтов"""
    categories_dict = {}
    driver = Config.driver

    for filename in Config.crawl_files_list:
        try:
            file_path = Config.mining_data_path / filename
            crawl_data = j_loads(file_path)
            crawl_data = crawl_data.get('products', [])
            for product in crawl_data:
                domain = get_domain(product['product_url'])
                if domain in Config.checked_domains:
                    continue
                task = Config.instruction_get_supplier_categories.replace('{INPUT_URL}', domain)
                res = await driver.simple_process_task_async(task)
                if not res:
                    continue
                normalized_res = normalize_answer(res.get('output', ''))
                data = j_loads(normalized_res)
                print(data)
                j_dumps(data, Config.train_data_supplier_categories_path / f'{gs.now}.json')
                Config.checked_domains.append(domain)
                save_text_file(Config.checked_domains, Config.ENDPOINT / 'checked_domains.txt')
                j_dumps(Config.checked_domains, Config.ENDPOINT / 'checked_domains.json')
        except Exception as ex:
            logger.error(f'Ошибка при обработке файла {filename=}', ex, exc_info=True)
    return categories_dict


async def main():
    """Основная функция запуска"""
    driver = Config.driver

    # Пример: обработка товаров по категориям
    for category in get_categories_from_random_urls():
        await get_products_urls(category, '3')
        ...

    # # Пример: обработка доменов
    # domains_list:list = read_text_file(Config.ENDPOINT / 'checked_domains.txt', as_list=True)
    # output_dict:dict = {}
    # timestamp:str = gs.now
    # for domain in domains_list:
    #     try:
    #         logger.info(f'Обработка домена: {domain}')
    #         print(f"\n------------------------\n Start find products in {domain}\n -----------------------------\n")
    #         task = Config.instruction_grab_product_page_simple_driver.replace('{INPUT_URL}', domain)
    #         res = await driver.simple_process_task_async(task)
    #         if not res:
    #             continue
    #         normalized_res:str = normalize_answer(res.get('output', ''))
    #         res_dict:dict = j_loads(normalized_res)
    #         output_dict.update({domain: res_dict})
    #         j_dumps(output_dict, Config.ENDPOINT / f'output_{timestamp}.json')
    #     except Exception as ex:
    #         logger.error(f'Ошибка при обработке {domain=}', ex, exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
