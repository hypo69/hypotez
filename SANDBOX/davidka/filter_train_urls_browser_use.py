## \file /sandbox/davidka/crawler.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора данных со страниц товаров с различных сайтов
=====================================================
Использует WebDriver для взаимодействия со страницами и LLM для извлечения
структурированной информации на основе инструкций. Обрабатывает задачи
по сбору данных о товарах по URL, по категориям, извлечению категорий
с сайтов поставщиков и поиску товаров на заданных доменах.

```rst
.. module:: sandbox.davidka.crawler
```
"""
import asyncio
import random # Используется для перемешивания списков (хотя сейчас закомментировано)
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional, Dict, Any, Set # Добавлены Dict, Any, Optional, List, Set

import header
from header import __root__
from src import gs
from src.webdriver import driver
from src.webdriver.llm_driver import SimpleDriver
from SANDBOX.davidka import utils 
from src.utils.file import read_text_file
from src.utils.jjson import j_loads, j_dumps

class Config:
    ENDPOINT:Path = __root__/ 'SANDBOX/davidka'
    GEMINI_API:str = gs.credentials.gemini.onela.api_key
    GEMINI_MODEL_NAME = 'gemini-2.5-flash-preview-04-17'
    driver:SimpleDriver = SimpleDriver(GEMINI_API,gemini_model_name=GEMINI_MODEL_NAME)
    instruction_filter_urls:str = read_text_file(ENDPOINT/'instructions'/'filter_urls.md')
    output_file:Path = Path("J://My Drive//hypo69//llm//filtered_urls.json") 

async def filter_url(url:str) -> bool:
    """"""
    output_dict:dict = j_loads(Config.output_file) or {}
    driver = Config.driver
    task = Config.instruction_filter_urls.replace('{TARGET_URL}', url)
    raw_res = await driver.run_task(task) # Предполагаем использование стандартного LLM
    res_dict:dict = j_loads(raw_res)
    output_dict.update(res_dict)
    j_dumps(outpu_dict, Config.output_file)
    ...


async def main():
    urls_list: list = utils.fetch_urls_from_all_mining_files(['random_urls','output_product_data_set1'])
    tasks = [filter_url(url.strip()) for url in urls_list]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as ex:
        logger.error("Ошибка в main()", ex)