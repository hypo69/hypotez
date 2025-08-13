# # \file src/endpoints/kazarinov/scenarios/scenario.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3
"""Scenario for Kazarinov
=========================

The module contains a configuration and a script executor for the `Kazarinov` entopointa.

1. Kazarinov chooses components
2. Combines into onetab
3. Sends Telegram bot link to onetab
`` `RST
.. Module :: src.endpoints.kazarinov.secenarios.secenario
`` `"""

import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional, TYPE_CHECKING
import telebot

from header import __root__
from src import gs, USE_ENV
from src.webdriver.pydoll.llib.browser import Chrome
from src.webdriver.pydoll.tab import BaseTab, Tab
from src.webdriver.pydoll.options import Options
from src.webdriver.pydoll.browser import Browser

from src.endpoints.kazarinov.report_generator.report_generator import ReportGenerator
from src.endpoints.kazarinov.scenarios.quotation_builder import QuotationBuilder
from src.endpoints.prestashop.product_fields.product_fields import ProductFields

from src.utils.port import get_free_port
from src.logger.logger import logger
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
from src.utils.jjson import j_loads_ns, j_dumps


class Config:
    """Scenario configuration."""
    
    ENDPOINT: str = 'kazarinov'
    config: SimpleNamespace = j_loads_ns(__root__ / "src" / "endpoints" / ENDPOINT / f"{ENDPOINT}.json")
    if not config:
        raise RuntimeError("Configuration not found for Kazarinov endpoint")
    _driver_cfg = getattr(config.webdriver, config.webdriver.active_driver, 'pydoll')
    WINDOW_MODE = getattr(_driver_cfg, "WINDOW_MODE", "window")
    user_data_dir = getattr(_driver_cfg, "user_data_dir", None)


@dataclass(slots=True, kw_only=True)
class Scenario:
    """Script performer for Kazarinov."""

    async def process_llm_async(self, products_list: List[str], lang:str,  attempts: int = 3) -> tuple | bool:
        """Processes The Product List Through The Ai Model.

        Args:
            Products_List (StR): List of Product Diction Dictionaries as a String.
            Attempts (Int, Optional): Number of Attempts to Retry in Case of Failure. Defaults to 3.

        Returns:
            Tuple: Processed Response in `ru` and` he` formats.
            Bool: FALSE if Unable to get a Valid Response after Retress.

        .. Note ::
            The model can return the unimportant result.
            In this case, I ask the model for a reasonable number of times."""
        if attempts < 1:
            ...
            return {}  # return early if no attempts are left

        model_command = Path(gs.path.endpoints / Config.ENDPOINT / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(encoding='UTF-8')
        # Request response from the AI model
        q = model_command + '\n' + str(products_list)

        response = await self.model.ask_async(q) # CORRECT

        if not response:
            logger.error(f"Нет ответа от модели")
            ...
            return {}

        response_dict:dict = j_loads(response) # <- If there is an error, then an empty dictionary will return

        if not response_dict:
            logger.error(f'Ошибка {attempts} парсинга ответа модели', None, False)
            if attempts > 1:
                ...
                return await self.process_llm_async(products_list, lang, attempts - 1) 
            return {}
        return  response_dict

    async def save_product_data(self, product_data: dict) -> bool:
        """Saves individual product data to a file.

        Args:
            product_data (dict): Formatted product data."""
        file_path = self.export_path / 'products' / f"{product_data['product_id']}.json"
        if not j_dumps(product_data, file_path, ensure_ascii=False):
            logger.error(f'Ошибка сохранения словаря {print(product_data)}\n Путь: {file_path}')
            ...
            return
        return True

 
    async def run_scenario_async(
        self,
        mexiron_name:str,
        urls: List[str],
        price: str = "",
        bot: Optional[telebot.TeleBot] = None,
        chat_id: int = 0,
        browser_options: Optional[Options] = None,
        attempts: int = 3,
    ) -> bool:
        """Runes the script.

        Args:
            URLS: links to goods (or categories).
            Price: Price for a report.
            BOT: Telegram bout for sending the status.
            Chat_id: Chat identifier.
            Attempts: the number of attempts to restart the driver.

        Returns:
            Bool: `` True`` with a successful end of the script."""
        products_list: list[dict] = []  # List of collected goods
        required_fields: list[str] = [
            "id_supplier",
            "name",
            # "price",
            "reference",
            "description",
            # "description_short",
            "specification",
            "default_image_url",
        ]


        async with Browser( # <- A browser class (Chrome, Edge) from FROM SRC.webdriver.pydoll.llib.browser can be substituted here
                        options = Options(headless=False), 
                        connection_port = get_free_port([9223, 9322]) 
                        ) as browser:
            base_tab: 'BaseTab' = await browser.start()
            tab: Tab = Tab(base_tab = base_tab)
            _process = browser._browser_process_manager._process
            # The collection of goods --------------------------------------------------
            for url in urls:
                logger.debug(f"Обработка URL: {url}", None, False)

                graber = get_graber_by_supplier_url(url, tab)

                if not graber:
                    logger.error(f"🤷‍♂️ Нет подходящего грабера для URL: {url}", None, True)
                    if bot:
                        bot.send_message(chat_id, f"❌ Нет обработчика для ссылки:\n{url}")
                    continue

                if bot:
                    bot.send_message(chat_id, f"⏳ Сбор полей товара со страницы:\n{url}")

                logger.info(f'⏳ Сбор полей товара со страницы {url}', ex = None, exc_info = False, text_color = "light_gray")
                try:
                    await tab.get_url(url)
                    product_fields: ProductFields = await graber.grab_page_async(required_fields = required_fields)
                except Exception as ex: 
                    logger.error(f"❌ Ошибка парсинга страницы:{url}", ex, exc_info = True)
                    if bot:
                        bot.send_message(chat_id, f"❌ Ошибка парсинга страницы:\n{url}\n{ex}")
                    continue

                if not product_fields or not product_fields.name:

                    if bot:
                        bot.send_message(chat_id, f"❌ Ошибка парсинга товара:\n{url}\nПроверьте локаторы.")
                    logger.error(f"""❌ Error Parsing of goods: {url}
                    Check the locators.""", None, False, text_color="light_gray", bg_color="light_gray")
                    continue

                try:
                    # Convertation of the field from the `Productfields' object in a simple dictionary for LLM model
                    ...
                    product_data = self.convert_product_fields(product_fields)

                    # Individual settings of suppliers
                    match(graber.supplier_prefix):
                        case 'morlevi.co.il':
                            product_data['default_image_url'] = fr'https"://"morlevi.co.il/' + product_data['default_image_url'] 
                            ...
                        case 'grandadvance.co.il':
                            ...
                        case 'ksp.co.il':
                            ...
                        case 'ivory.co.il':
                            ...

                except Exception as ex:  
                    logger.error("Ошибка конвертации данных", ex, exc_info=True)
                    if bot:
                        bot.send_message(chat_id, f"❌ Ошибка конвертации:\n{url}")
                    continue

                await self.save_product_data(product_data)
                products_list.append(product_data)

        # AI-processing ----------------------------------------------------------
        if not products_list:
            logger.warning(" 😒 Не собрано ни одного товара", None, False)
            if bot:
                bot.send_message(chat_id, "⚠️ Не удалось собрать информацию ни об одном товаре.")
            return False

        for lang in ("he", "ru"):
            if bot:
                bot.send_message(chat_id, f"🤖 AI обработка ({lang})...")

            try:
                data = await self.process_llm_async(products_list, lang)
            except Exception as ex:  # pragma: no cover
                logger.error("🤖 AI‑обработка упала", ex, exc_info=False)
                if bot:
                    bot.send_message(chat_id, f"❌ AI ошибка ({lang}):\n{ex}")
                continue

            if not data or lang not in data:
                if bot:
                    bot.send_message(chat_id, f"🤖 AI f'AI вернула пустой результат\nязык: {lang}\n{products_list=}'\n...")

                logger.warning(f'AI вернула пустой результат \n язык {lang} \n {products_list=}')
                continue

            processed = data[lang]
            processed["price"] = price
            processed["currency"] = getattr(self.translations.currency, lang, "ש''ח")

            try:
                j_dumps(processed, self.export_path / f"{self.mexiron_name}_{lang}.json")
            except Exception as ex:  # pragma: no cover
                logger.error("Не удалось сохранить JSON", ex, exc_info=True)

            logger.info("Сохранён JSON: ", self.export_path / f"{self.mexiron_name}_{lang}.json")
            


            # Generation of the report --------------------------------------------

            if bot:
                bot.send_message(chat_id, f"📈 Создание отчёта ({lang})...")

            logger.info(f"📈 Создание отчёта ({lang})...", ex=None, exc_info=False, text_color = "light_gray",)

            reporter = ReportGenerator(if_need_docx=False)
            
            if not await reporter.create_reports_async(
                    bot=bot,
                    chat_id=chat_id,
                    data=processed,
                    lang=lang,
                    mexiron_name = mexiron_name,
                ):

                logger.error("Ошибка генерации отчёта", ex, exc_info=True)
                if bot:
                    bot.send_message(chat_id, f"❌ Ошибка отчёта ({lang}):\n{ex}")
                return 

        return True

    def convert_product_fields(self, f: ProductFields) -> dict:
        """Converts Product Fields Into a Dictionary. 
        The function converts the fields from the `Productfields' object in a simple dictionary for the LLM model.

        Args:
            F (Productfields): Object Containing Parsed Product Data.

        Returns:
            DICT: FORMATTED Product DICTIONARY.

        Note: 
            The rules for building fields are determined in `Productfields`"""
        # if not f.reference:
        # Logger.ERROR (F "Failure to receive the fields of goods.")
        # Return {} # <- a failure when receiving the fields of goods. This can happen if a category page came across instead of the product page, with an inattentive compilation of Mehiron from components
        # None

        product_name = f.name['language']['value'] if f.name else ''
        description = f.description['language']['value'] if f.description else ''
        description_short = f.description_short['language']['value'] if f.description_short else ''
        specification = f.specification['language']['value']  if f.specification else ''
        
        if not product_name:
            return {}
        return {
            'product_name':product_name,
            'reference': f.reference,
            'description_short':description_short,
            'description': description,
            'specification': specification,
            'local_image_path': str(f.local_image_path),
        }



# None
# Example launch
# None

def run_sample_scenario() -> None:
    """An example of a local script test."""
    urls_list: list[str] = [
        "https://www.morlevi.co.il/product/21039",
        "https://www.morlevi.co.il/product/21018",
        "https://www.ivory.co.il/catalog.php?id=85473",
        "https://grandadvance.co.il/eng/?go=products&action=view&ties_ids=801&product_id=28457--SAMSUNG-SSD-1TB-990-EVO-PCle-4.0-x4--5.0-x2-NVMe",
    ]

    scenario = Scenario()
    logger.info("Запуск тестового сценария…")

    async def _runner() -> bool:
        if await scenario.run_scenario_async(
            urls=urls_list,
            mexiron_name="test_kazarinov_run",
            price="100.50",
            # bot=your_telebot_instance,
            # chat_id=your_chat_id,
            ):
            logger.info("Тестовый сценарий завершён")
            return True
        return

    asyncio.run(_runner())


if __name__ == "__main__":
    run_sample_scenario()
