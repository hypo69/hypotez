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
from src.webdriver.ai_browser import run_task_on_active_models
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.file import read_text_file, save_text_file, get_filenames_from_directory 
from src.utils.printer import pprint as print
from src.logger.logger import logger

class Config(SimpleNamespace):
    ENDPOINT:Path = __root__/'SANDBOX'/'davidka'
    mining_data_path:Path = ENDPOINT/'mining_data'
    crawl_files_list:list = get_filenames_from_directory(mining_data_path, 'json')
    task_description =  Path(ENDPOINT/ 'tasks'/ 'grab_product_page.md').read_text(encoding='utf-8')


def products_urls_list_from_files(crawl_files_list:list = []) -> list:
    """Получение списка продуктов из файлов в директории."""
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
    """Генератор для получения product_url из всех файлов в директории."""
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



async def main():
    """"""
    # генератор
    # for product_url in yield_product_urls_from_files():

    for product_url in products_urls_list_from_files():
        try:
            logger.info(f'Обработка URL: {product_url}')
            task = Config.task_description.replace('<URL>', product_url)
            extracted_data = await run_task_on_active_models(task)
            print(extracted_data)
            ...
        except Exception as ex:
            logger.error(f'Ошибка при обработке {product_url=}', ex)

asyncio.run(main())



