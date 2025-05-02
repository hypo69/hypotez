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
    GEMINI_API_KEY = gs.credentials.gemini.kazarinov.api_key
    driver: SimpleDriver = SimpleDriver(gemini_model_name='gemini-1.5-flash-8b-exp-0924', GEMINI_API_KEY = GEMINI_API_KEY)

    # Список "плохих" доменов и платформ (можно расширять)
    BLACKLIST_DOMAINS = [
        "youtube.com", "youtu.be", "facebook.com", "twitter.com", "tiktok.com",
        "linkedin.com", "instagram.com", "vk.com", "pinterest.com", "reddit.com",
        "snapchat.com", "weibo.com", "medium.com", "blogspot.com", "github.com"
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

def filter_links(raw_links: list[str]) -> list[str]:
    clean_links = set()

    for link in raw_links:
        if link.startswith("https://") and is_link_allowed(link):
            clean_links.add(link.strip())

    return list(clean_links)

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


def yield_product_urls_from_files(directory: Path = Config.train_data_products_dir, pattern: str = 'json'):
    """Генератор url продуктов из файлов"""
    filenames = get_filenames_from_directory(directory, pattern)

    def extract_https_links(obj):
        links = []

        if isinstance(obj, dict):
            for value in obj.values():
                links.extend(extract_https_links(value))
        elif isinstance(obj, list):
            for item in obj:
                links.extend(extract_https_links(item))
        elif isinstance(obj, str):
            if obj.startswith("https://"):
                links.append(obj)

        return links

    for filename in filenames:
        try:
            file_path = directory / filename
            data = j_loads(file_path)
            links_list = extract_https_links(data)
            filtered_links_list = filter_links(links_list)
            for link in filtered_links_list:
                yield link
        except Exception as ex:
            logger.error(f'Ошибка при обработке файла {filename=}', ex, exc_info=True)
            ...


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
        j_dumps(answer, Config.ENDPOINT/'train_data_products'/f'product_links_{timestamp}.json')
    except Exception as ex:
        logger.error(f'Ошибка при обработке {category=}', ex, exc_info=True)
        return ''


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
