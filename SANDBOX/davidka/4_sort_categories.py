## \file /sandbox/davidka/4_sort_categories.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

import random
from pathlib import Path
from types import SimpleNamespace

import header
from header import __root__
from src import gs
from src.utils.jjson import j_loads, j_loads_ns
from src.utils.file import recursively_yield_file_path, read_text_file, save_text_file_async, save_text_file
from src.logger import logger


class Config:                                                           
    ENPOINT:Path  = __root__ / 'SANDBOX' / 'davidka'
    config:SimpleNamespace = j_loads_ns(ENPOINT/'davidka.json')
    actual_storage:str = 'local_storage' # 'local_storage' or 'google_drive'  <- ГДЕ НАХОДИТСЯ ХРАНИЛИЩЕ
    STORAGE:Path = Path(config.local_storage.storage) if actual_storage == 'local_storage' else Path(config.google_drive.storage)
    source_dirs:list = [
        # STORAGE / 'search_results', 
        STORAGE / 'data_by_supplier_ge', 
        STORAGE / 'data_by_supplier_set_1 DONT TOUCH!', 
        ]

    known_categories_path:Path = STORAGE/'known_categories.txt'
    known_categories:list = read_text_file(known_categories_path, as_list=True)
    




def build_categories_from_suppliers_data(source_dirs:  str |Path | list[str, Path] = None) -> list:
    """Возвращает все категории из файлов в директории 'random_urls' 
    Директория собрана из словарей, полученных вручную через gemini aiu studio (katia).
    """
    source_dirs = source_dirs if isinstance(source_dirs, list) else [source_dirs]
    categories_list = []
    for source_dir in source_dirs:
        for file_path in recursively_yield_file_path(source_dir):
            try:
                crawl_data = j_loads(file_path)
                crawl_data = crawl_data if isinstance(crawl_data, list ) else [crawl_data]
                for item in crawl_data:
                    if 'parent_category' in item:
                        categories_list.append(item['parent_category'])
                    if 'category_name' in item:
                        categories_list.append(item['category_name'])
            except Exception as ex:
                logger.error(f'Ошибка при обработке файла\n {file_path=}', ex, exc_info=True)
                continue
        categories_list = list(filter(None, set(categories_list)))
        random.shuffle(categories_list)
        return categories_list


if __name__ == '__main__':
    # Получаем категории из файлов
    found_categories = build_categories_from_suppliers_data(Config.source_dirs)
    Config.known_categories.extend(found_categories)
    categories_list = list(filter(None, set(Config.known_categories)))
    save_text_file_async(categories_list, Config.STORAGE/'known_categories.txt')
