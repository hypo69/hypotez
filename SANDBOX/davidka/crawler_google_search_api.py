## \file /sandbox/davidka/crawler_google_search_api.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль получения ссылок на товары через google search api
=====================================================


```rst
.. module:: sandbox.davidka.crawler_google_search_api
```
"""
from pathlib import Path
import header
from header import __root__
from src import gs
from src.logger.logger import logger
from src.utils.printer import pprint as print
from SANDBOX.davidka.google_api_searcher import  GoogleApiSearcher
from SANDBOX.davidka.utils import get_categories_from_files, get_products_urls_list_from_files, get_filenames_from_directory

class Config:
    ENDPOINT:Path = __root__/'SANDBOX'/'davidka' 

def main():
    """ """
    # Пример использования GoogleApiSearcher
    # Инициализация класса

    searcher = GoogleApiSearcher()
    categories_list:list = get_categories_from_files(Config.ENDPOINT/'random_urls' )
    for category in categories_list:
        res = searcher.search_strategy2_inurl(category)
        print(res)
    print(categories_list)


if __name__ == "__main__":
    main()



