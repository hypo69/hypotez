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
from urllib.parse import urlparse
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
from SANDBOX.davidka.utils import yield_product_urls_from_files

class Config:
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
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
    driver: SimpleDriver = SimpleDriver(gemini_model_name='gemini-1.5-flash-8b-exp-0924', GEMINI_API_KEY = GEMINI_API_KEY)

    # Список "плохих" доменов и платформ (можно расширять)
    BLACKLIST_DOMAINS = [
        "youtube.com", "youtu.be", "facebook.com", "twitter.com", "tiktok.com",
        "linkedin.com", "instagram.com", "vk.com", "pinterest.com", "reddit.com",
        "snapchat.com", "weibo.com", "medium.com", "blogspot.com", "github.com",
        "google.com"
    ]

    # По каким окончаниям/типам ссылок тоже исключать
    BLOCKED_PATTERNS = [".pdf", "/login", "/register", "/signin", "/signup"]

def is_link_allowed(url: str) -> bool:
    try:
        parsed = urlparse(url.lower())
        domain = parsed.netloc.replace("www.", "")

        # Отфильтровать по домену
        if any(bad in domain for bad in Config.BLACKLIST_DOMAINS):
            return False

        # Отфильтровать по пути
        if any(pattern in parsed.path for pattern in Config.BLOCKED_PATTERNS):
            return False

        return True
    except Exception:
        return False



async def fetch_product_data():
    """Сбор данных о продукте"""
    driver = Config.driver
    processed_links:list = []
    try:
        for product_url in yield_product_urls_from_files():
            try:
                processed_links = read_text_file(Config.ENDPOINT / 'processed_links.txt', as_list=True)
                if processed_links and product_url in processed_links:
                    continue
                logger.info(f'Обработка {product_url=}')
                task = Config.instruction_grab_product_page_simple_driver.replace('{PRODUCT_URL}', product_url)
                res = await driver.simple_process_task_async(task)
                if not res:
                    continue
                #normalized_res = normalize_answer(res.get('output', ''))
                data = j_loads(res)
                print(data)
                ...
                j_dumps(data, Config.output_product_data_dir / f'{gs.now}.json')
                processed_links.append(product_url)
                save_text_file(processed_links, Config.ENDPOINT / 'processed_links.txt')
            except Exception as ex:
                logger.error(f'Ошибка при обработке {product_url=}', ex, exc_info=True)
    except Exception as ex:
        logger.error('Ошибка при запуске функции fetch_product_data', ex, exc_info=True)

async def get_products_urls(category: str, task:str = '', num_of_links: str = '1') -> str:
    """Получить товары по категории"""
    try:
        driver = Config.driver
        logger.info(f'Обработка {category=}')
        
        task = task or Config.instruction_links_from_searh_page.replace('{PRODUCT_CATEGORY}', category).replace('{NUM_LINKS}', num_of_links)
        #ipdb.set_trace()
        answer = await driver.simple_process_task_async(task)
        if not answer:
            return ''
        j_dumps(answer, Config.ENDPOINT/'train_data_products'/f'product_links_{gs.now}.json')
    except Exception as ex:
        logger.error(f'Ошибка при обработке {category=}', ex, exc_info=True)
        return ''

async def filter_urls():
    """"""



async def main():
    """Основная функция запуска"""
    driver = Config.driver
    # Парсинг страниц товаров
    await fetch_product_data()
    ...

    # Пример: обработка товаров по категориям
    for category in get_categories_from_random_urls():
        await get_products_urls(category)
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
