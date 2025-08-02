# \file /sandbox/davidka/experiments/pydoll/webdriver.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль экспериментов с pydoll
=====================================================
"""
import asyncio
from types import SimpleNamespace
from typing import TYPE_CHECKING
from pydoll.browser import Chrome


from header import __root__
from src.webdriver.pydoll.tab import Tab
from src.utils.jjson import j_loads_ns
from src.webdriver.pydoll.options import Options
from src.utils.printer import pprint as print
from src.logger.logger import logger

if TYPE_CHECKING:
    from pydoll.browser.tab import Tab as BaseTab

async def experiment( locator: SimpleNamespace, headless: bool = False,):
    """
    Демонстрирует запуск pydoll.Chrome с полностью сконфигурированным
    объектом Options, который позволяет переопределять настройки из pydoll.json.
    """
    logger.info(f"Starting experiment with headless={headless}")
    
    # 1. Создаем объект Options. Он автоматически загрузит файл настрое браузера
    #    и применит переопределение `headless=True` (или False).
    options: Options = Options(headless=headless)
    logger.debug(f"Generated arguments for Chrome: {print(options.arguments)}")

    # 2. асинхронный контекстный менеджер.
    try:
        async with Chrome(options = options) as browser:
           
            # 3. Базовая вкладка завернутая в кастомный Tab
            base_tab: 'BaseTab' = await browser.start() 
            async with Tab(base_tab) as tab:
                ...            
                await tab.go_to("https://www.google.com")
                await tab.execute_locator(locator.input_field)
                await asyncio.sleep(5) # Пауза, чтобы увидеть результат
    
    except Exception as ex:
        logger.error(f"An error occurred during the experiment: ", ex, exc_info=True)
        ...

if __name__ == "__main__":
    # Запускаем эксперимент

    # --- google.com ---
    supplier_prefix:str = 'google.com'
    supplier_alias:str = supplier_prefix.replace('-','_').replace('.','_')
    locator:SimpleNamespace = j_loads_ns(__root__/'src'/'suppliers'/'suppliers_list'/supplier_alias/'locators'/'search_page.json')


    asyncio.run(experiment( locator = locator, headless = False, ))