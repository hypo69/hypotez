## \file /sandbox/davidka/experiments/8_run_suppliers_scenarios_pydoll.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
модуль взаимодействия с pydoll
===============================
"""
from header import __root__  # type: ignore[import]
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
from src.logger.logger import logger

import asyncio
from pydoll.constants import Key
from pydoll.browser.chromium.chrome import Chrome 

from src.webdriver.pydoll.tab import Tab
from src.webdriver.pydoll.options import Options
from src.webdriver.pydoll.browser import Browser

async def start_browser():
    async with Chrome() as browser:
        # Запустите браузер и получите новую вкладку
        tab = await browser.start()

        # Перейдите в Google
        await tab.go_to('https://www.google.com')

        # Найдите поле поиска по его атрибутам
        search_box = await tab.find(tag_name='textarea', name='q')

        # Введите поисковый запрос и нажмите Enter
        await search_box.insert_text('pydoll python')
        await search_box.press_keyboard_key(Key.ENTER)

        # Дождитесь появления результатов поиска
        await tab.wait_element(id='search')
        tab

        print("Результаты поиска загружены!")
        ...

asyncio.run(start_browser())
...
