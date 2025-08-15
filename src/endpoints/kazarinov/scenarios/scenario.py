## \file src/endpoints/kazarinov/scenarios/scenario.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Scenario for Kazarinov
======================

This module contains the configuration and scenario executor for the `kazarinov` endpoint.

1. Kazarinov selects components
2. combines them in onetab
3. Sends a link to onetab to the telegram bot
```rst
.. module:: src.endpoints.kazarinov.scenarios.scenario
```
"""

import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional, TYPE_CHECKING, TypeVar
import telebot

from header import __root__
from src import gs, USE_ENV

from src.webdriver.pydoll.tab import Tab
from src.webdriver.pydoll.options import Options
from src.webdriver.pydoll.browser import Browser

from src.endpoints.kazarinov.report_generator.report_generator import ReportGenerator
from src.endpoints.kazarinov.scenarios.quotation_builder import QuotationBuilder
from src.endpoints.prestashop.product_fields.product_fields import ProductFields
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
from src.utils.port import get_free_port
from src.logger.logger import logger

from src.utils.jjson import j_loads_ns, j_dumps

T = TypeVar('T')

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
    """Scenario executor for Kazarinov."""

    async def process_llm_async(self, products_list: List[str], lang:str,  attempts: int = 3) -> tuple | bool:
        """
        Processes the product list through the AI model.

        Args:
            products_list (str): List of product data dictionaries as a string.
            attempts (int, optional): Number of attempts to retry in case of failure. Defaults to 3.

        Returns:
            tuple: Processed response in `ru` and `he` formats.
            bool: False if unable to get a valid response after retries.

        .. note::
            The model may return an invalid result.
            In this case, I ask the model again a reasonable number of times.
        """
        if attempts < 1:
            ...
            return {}  # return early if no attempts are left

        model_command = Path(gs.path.endpoints / Config.ENDPOINT / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(encoding='UTF-8')
        # Request response from the AI model
        q = model_command + '\n' + str(products_list)

        response = await self.model.ask_async(q) # CORRECT

        if not response:
            logger.error(f"No response from the model")
            ...
            return {}

        response_dict:dict = j_loads(response) # <- if there is an error, an empty dictionary will be returned

        if not response_dict:
            logger.error(f'Error {attempts} parsing the model response', None, False)
            if attempts > 1:
                ...
                return await self.process_llm_async(products_list, lang, attempts - 1)
            return {}
        return  response_dict

    async def save_product_data(self, product_data: dict) -> bool:
        """
        Saves individual product data to a file.

        Args:
            product_data (dict): Formatted product data.
        """
        file_path = self.export_path / 'products' / f"{product_data['product_id']}.json"
        if not j_dumps(product_data, file_path, ensure_ascii=False):
            logger.error(f'Error saving dictionary {print(product_data)}\n Path: {file_path}')
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
        """Runs the scenario.

        Args:
            urls: Links to products (or categories).
            price: Price for the report.
            bot: Telegram bot for sending status.
            chat_id: Chat ID.
            attempts: Number of attempts to restart the driver.

        Returns:
            bool: ``True`` on successful completion of the scenario.
        """
        products_list: list[dict] = []  # List of collected products
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
        


        async with Browser( # <- you can substitute the browser class (Chrome, Edge) from from src.webdriver.pydoll.llib.browser here
                        options = Options(headless=False),
                        connection_port = get_free_port([9223, 9322])
                        ) as browser:
            tab: Tab = await browser.start()
            if not tab:
                logger.error(f'Таб не появился')
                ...
                return

            # Collecting products ---------------------------------------------------------
            for url in urls:
                logger.debug(f"Processing URL: {url}", None, False)

                graber = get_graber_by_supplier_url(url, tab)

                if not graber:
                    logger.error(f"🤷‍♂️ No suitable grabber for URL: {url}", None, True)
                    if bot:
                        bot.send_message(chat_id, f"❌ No handler for the link:\n{url}")
                    continue

                if bot:
                    bot.send_message(chat_id, f"⏳ Collecting product fields from the page:\n{url}")

                logger.info(f'⏳ Collecting product fields from the page {url}', ex = None, exc_info = False, text_color = "light_gray")
                try:
                    await tab.go_to(url)
                    product_fields: ProductFields = await graber.grab_page_async(required_fields = required_fields)
                except Exception as ex:
                    logger.error(f"❌ Error parsing page:{url}", ex, exc_info = True)
                    if bot:
                        bot.send_message(chat_id, f"❌ Error parsing page:\n{url}\n{ex}")
                    continue

                if not product_fields or not product_fields.name:

                    if bot:
                        bot.send_message(chat_id, f"❌ Error parsing product:\n{url}\nCheck the locators.")
                    logger.error(f"""❌ Error parsing product:{url}
                    Check the locators.""", None, False, text_color="light_gray", bg_color="light_gray")
                    continue

                try:
                    # Convert the field from a `ProductFields` object to a simple dictionary for the llm model
                    ...
                    product_data = self.convert_product_fields(product_fields)

                    # Individual supplier settings
                    match(graber.supplier_prefix):
                        case 'morlevi.co.il':
                            product_data['default_image_url'] = fr'https://morlevi.co.il/' + product_data['default_image_url']
                            ...
                        case 'grandadvance.co.il':
                            ...
                        case 'ksp.co.il':
                            ...
                        case 'ivory.co.il':
                            ...

                except Exception as ex:
                    logger.error("Error converting data", ex, exc_info=True)
                    if bot:
                        bot.send_message(chat_id, f"❌ Conversion error:\n{url}")
                    continue

                await self.save_product_data(product_data)
                products_list.append(product_data)

        # AI processing ---------------------------------------------------------
        if not products_list:
            logger.warning(" 😒 Not a single product has been collected", None, False)
            if bot:
                bot.send_message(chat_id, "⚠️ Failed to collect information about any product.")
            return False

        for lang in ("he", "ru"):
            if bot:
                bot.send_message(chat_id, f"🤖 AI processing ({lang})...")

            try:
                data = await self.process_llm_async(products_list, lang)
            except Exception as ex:  # pragma: no cover
                logger.error("🤖 AI processing failed", ex, exc_info=False)
                if bot:
                    bot.send_message(chat_id, f"❌ AI error ({lang}):\n{ex}")
                continue

            if not data or lang not in data:
                if bot:
                    bot.send_message(chat_id, f"🤖 AI f'AI returned an empty result\nlanguage: {lang}\n{products_list=}'\n...")

                logger.warning(f'AI returned an empty result \n language {lang} \n {products_list=}')
                continue

            processed = data[lang]
            processed["price"] = price
            processed["currency"] = getattr(self.translations.currency, lang, "NIS")

            try:
                j_dumps(processed, self.export_path / f"{self.mexiron_name}_{lang}.json")
            except Exception as ex:  # pragma: no cover
                logger.error("Failed to save JSON", ex, exc_info=True)

            logger.info("Saved JSON: ", self.export_path / f"{self.mexiron_name}_{lang}.json")


            # Report generation ---------------------------------------------------

            if bot:
                bot.send_message(chat_id, f"📈 Creating report ({lang})...")

            logger.info(f"📈 Creating report ({lang})...", ex=None, exc_info=False, text_color = "light_gray",)

            reporter = ReportGenerator(if_need_docx=False)

            if not await reporter.create_reports_async(
                    bot=bot,
                    chat_id=chat_id,
                    data=processed,
                    lang=lang,
                    mexiron_name = mexiron_name,
                ):

                logger.error("Report generation error", ex, exc_info=True)
                if bot:
                    bot.send_message(chat_id, f"❌ Report error ({lang}):\n{ex}")
                return

        return True

    def convert_product_fields(self, f: ProductFields) -> dict:
        """
        Converts product fields into a dictionary.
        The function converts fields from the `ProductFields` object into a simple dictionary for the llm model.

        Args:
            f (ProductFields): Object containing parsed product data.

        Returns:
            dict: Formatted product data dictionary.

        Note:
            The rules for constructing fields are defined in `ProductFields`
        """
        # if not f.reference:
        #     logger.error(f"Failed to get product fields. ")
        #     return {} # <- failed to get product fields. This can happen if a category page was encountered instead of a product page, with careless compilation of the mekhiron from components
        # ...

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



#               --- Example ----

def run_sample_scenario() -> None:
    """Example of a local scenario test."""
    urls_list: list[str] = [
        "https://www.morlevi.co.il/product/18707",
        "https://www.morlevi.co.il/product/21018",
        "https://www.ivory.co.il/catalog.php?id=85473",
        "https://grandadvance.co.il/eng/?go=products&action=view&ties_ids=801&product_id=28457--SAMSUNG-SSD-1TB-990-EVO-PCle-4.0-x4--5.0-x2-NVMe",
    ]

    scenario = Scenario()
    logger.info("Launching test scenario…")

    async def _runner() -> bool:
        if await scenario.run_scenario_async(
            urls=urls_list,
            mexiron_name="test_kazarinov_run",
            price="100.50",
            # bot=your_telebot_instance,
            # chat_id=your_chat_id,
            ):
            logger.info("Test scenario completed")
            return True
        return

    asyncio.run(_runner())


if __name__ == "__main__":
    run_sample_scenario()
