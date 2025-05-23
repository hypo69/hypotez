## \file /src/endpoints/kazarinov/scenarios/scenario.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Сценарий для Казаринова
=========================

.. module:: src.endpoints.kazarinov.scenarios.scenario 
	:platform: Windows, Unix
	:synopsis: Сценарий для Казаринова

"""

from bs4 import BeautifulSoup
import requests
import telebot
import asyncio
from pathlib import Path
from typing import Optional, List

import header
from src import gs
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from src.webdriver.playwright import Playwrid
from src.llm.gemini import GoogleGenerativeAi
from src.endpoints.kazarinov.report_generator.report_generator import ReportGenerator
from src.endpoints.kazarinov.scenarios.quotation_builder import QuotationBuilder
from src.endpoints.prestashop.product_fields.product_fields import ProductFields
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
from src.endpoints.fetch_one_tab import fetch_target_urls_onetab
from src.utils.jjson import j_dumps
from src.logger.logger import logger
from dataclasses import dataclass, field
@dataclass
class Config:

    ENDPOINT:str = "kazarinov"



class Scenario(QuotationBuilder):
    """Исполнитель сценария для Казаринова"""

    def __init__(self, mexiron_name:Optional[str] = gs.now, driver:Optional[Firefox | Playwrid | str] = None, **kwargs):
        """Сценарий сбора информации."""

        if 'window_mode' not in kwargs:
            kwargs['window_mode'] = 'normal'

        self.driver = Driver(Firefox,**kwargs) if not driver else driver


        super().__init__(mexiron_name = mexiron_name, driver = self.driver, **kwargs)

    async def run_scenario_async(
        self,
        urls: List[str],  
        price: Optional[str] = '',
        mexiron_name: Optional[str] = gs.now, 
        bot: Optional[telebot.TeleBot] = None,
        chat_id: Optional[int] = 0,
        attempts: int = 3,
    ) -> bool:
        """
        Executes the scenario: parses products, processes them via AI, and stores data.
        """

        products_list = []

        # -------------------------------------------------
        # 1. Сбор товаров

        lang_index: int = 2
        for url in urls:
            kwargs:dict = {}
            # ------------------------------- бот не работает ----------------
            graber: 'Graber' = get_graber_by_supplier_url(self.driver, url, lang_index, **kwargs)
            bot.send_message(chat_id, f"Сереж, сегодня не работает. Позвони.") 
            break
            # -----------------------------------------------------------------
            if not graber:
                logger.error(f"Нет грабера для: {url}")
                bot.send_message(chat_id, f"Нет грабера для: {url}")
                ...
                continue

            f: ProductFields = None
            if bot: bot.send_message(chat_id, f"Process: {url}")  
            try:
                f = await graber.grab_page_async(*self.required_fields)
            except Exception as ex:
                logger.error(f"Failed... Ошибка получения полей товара {url}:", ex)
                if bot: bot.send_message(chat_id, f"Failed... Ошибка получения полей товара {url}\n{ex}") 
                ...
                continue

            if not f:
                logger.error(f"Failed to parse product fields for URL: {url}")
                if bot: bot.send_message(chat_id, f"Failed to parse product fields for URL: {url}") 
                ...
                continue

            product_data = self.convert_product_fields(f)
            if not product_data:
                logger.error(f"Failed to convert product fields: {product_data}")
                if bot: bot.send_message(chat_id, f"Failed to convert product fields {url} \n {product_data}") 
                ...
                continue

            await self.save_product_data(product_data)
            products_list.append(product_data)
            self.driver.quit()

        # -----------------------------------------------------
        # 2. AI processing

        """ список компонентов сборки компьютера уходит в обработку моделью (`gemini`) ->
        модель парсит данные, делает перевод на `ru`, `he` и возвращает кортеж словарей по языкам.
        Внимание! модель может ошибаться"""

        langs_list: list = ["he", "ru"]

        for lang in langs_list:
            if bot: bot.send_message( 
                chat_id,
                f"""AI processing {lang=}""",
            )
            try:
                data: dict = await self.process_llm_async(products_list, lang)
                if not data:
                    bot.send_message(chat_id, f"Ошибка модели для {lang=}")  
                    #  пропустить этот язык
                    continue
            except Exception as ex:
                logger.exception(f"AI processing failed for {lang=}")
                if bot: bot.send_message(chat_id, f"AI processing failed for {lang=}: {ex}")
                continue


            # -----------------------------------------------------------------
            # 3. Report creating

            if bot: bot.send_message(chat_id, f"Создаю файл")  
            data = data[lang]
            data["price"] = price
            data["currency"] = getattr(self.translations.currency, lang, "ש''ח")

            j_dumps(data, self.export_path / f'{self.mexiron_name}_{lang}.json')

            reporter = ReportGenerator(if_need_docx=False)
            await reporter.create_reports_async(bot = bot, 
                                chat_id = chat_id,
                                data = data,
                                lang = lang,
                                mexiron_name = self.mexiron_name
                                    )

        return True # Возвращаем True в конце


def run_sample_scenario():
    """"""
    ...
    urls_list:list[str] = ['https://www.morlevi.co.il/product/21039',
                           'https://www.morlevi.co.il/product/21018',
                           'https://www.ivory.co.il/catalog.php?id=85473',
                           'https://grandadvance.co.il/eng/?go=products&action=view&ties_ids=801&product_id=28457--SAMSUNG-SSD-1TB-990-EVO-PCle-4.0-x4--5.0-x2-NVMe',
                           'https://www.ivory.co.il/catalog.php?id=85473',
                           'https://www.morlevi.co.il/product/21018']

    s = Scenario(window_mode = 'normal')
    asyncio.run(s.run_scenario_async(urls = urls_list, mexiron_name = 'test price quotation', ))



if __name__ == '__main__':
    run_sample_scenario()