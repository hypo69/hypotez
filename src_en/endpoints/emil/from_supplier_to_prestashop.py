# # \file /src/endpoints/emil/scenarios/from_supplier_to_prestashop.py
# -*- coding: utf-8 -*-\
# ! .pyenv/bin/python3

"""Модуль исполнения сценария `emil-design.com`
==================================================================

```rst
.. module:: src.endpoints.emil.scenarios.from_supplier_to_prestashop 
	:platform: Windows, Unix
	:synopsis: Provides functionality for extracting, parsing, and processing product data from 
various suppliers. The module handles data preparation, AI processing, 
and integration with Prestashop for product posting.
```"""


import os

import asyncio
import random
import shutil
from pathlib import Path
from tkinter import SEL
from typing import Optional, List
from types import SimpleNamespace

import header
from header import __root__
from src import gs, USE_ENV

from src.endpoints.prestashop.product_fields import ProductFields
from src.endpoints.prestashop.product import PrestaProduct

from src.webdriver.selenium.driver import Driver
from src.webdriver.firefox import Firefox
from src.llm.gemini import GoogleGenerativeAi
from src.endpoints.emil.report_generator import ReportGenerator
from src.endpoints.advertisement.facebook.scenarios import post_message_title, upload_post_media, message_publish
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url

from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.file import read_text_file, save_text_file, recursively_get_file_path
from src.utils.image import save_image_from_url_async, save_image
from src.utils.convertors.unicode import decode_unicode_escape
from src.utils.printer import pprint as print
from src.logger.logger import logger


class Config:
    ENDPOINT:Path = __root__ / 'endpoints' / 'emil'


class SupplierToPrestashopProvider:
    """Makes the extraction, analysis and preservation of data on suppliers.
    Data can be obtained as out of the seats, so from the dictionary of the product in the JSON file format
    
    Attributes:
        Driver (Driver): SELENIUM WebDriver copy.
        Export_path (Path): the path for data export.
        Products_List (List [dict]): a list of processed goods about goods."""
    
    driver: Driver
    export_path: Path
    mexiron_name: str
    price: float
    timestamp: str
    products_list: list
    config: SimpleNamespace
    local_images_path:Path = gs.path.external_storage / Config.ENDPOINT / 'images' / 'furniture_images'
    lang: str
    gemini_api: str
    api_key: str
    api_domain: str


    def __init__(self, 
                 lang:str, 
                 api_key: str,
                 api_domain: str,
                 driver: Optional [Driver] = None,
                 ):
        """Initializes SupplierToPrestashopProvider class with required components.

        Args:
            driver (Driver): Selenium WebDriver instance."""
        self.api_key = api_key
        self.api_domain = api_domain
        self.lang = lang
        try:
            self.config = j_loads_ns(gs.path.endpoints / Config.ENDPOINT / f'{Config.ENDPOINT}.json')
        except Exception as ex:
            logger.error(f"Error loading configuration: {ex}")
            return  # or raise an exception, depending on your error handling strategy

        self.timestamp = gs.now
        self.driver = driver if driver else Driver(Firefox)
        self.model = self.initialise_ai_model(self.lang)

        
    def initialise_ai_model(self):
        """Initialization models gemini"""
        try:
            system_instruction = (gs.path.endpoints / 'emil' / 'instructions' / f'system_instruction_mexiron.{self.lang}.md').read_text(encoding='UTF-8')
            return GoogleGenerativeAi(
                api_key=gs.credentials.gemini.kazarinov,
                system_instruction=system_instruction,
                generation_config={'response_mime_type': 'application/json'}
            )
        except Exception as ex:
            logger.error(f"Error loading instructions", ex)
            return

    async def process_graber(
        self, 
        urls: list[str],
        price: Optional[str] = '', 
        mexiron_name: Optional[str] = '', 
        scenarios: dict | list[dict,dict] = None,
        
    ) -> bool:
        """The function collects data from the page and collects a list of goods in `products_list`
        and sends to save in the JSON file

        Args:
            System_instruction (Optional [Str]): System Instructions for the Ai Model.
            Price (Optional [Str]): Price to Process.
            Mexiron_name (Optional [Str]): Custom Mexiron Name.
            URLS (Optional [str | lib [str]]): Product Page urls.
            Scenario (Optional [Dict]): The performance scenario that is located in the Directory `SRC.SUPPPLIRS.SUPPLIRS_LIST.

        Returns:
            Bool: True if the Scenario Executes Successfully, False Otherwise.

        .. Todo:
            Make a logger before a negative exit from the function. 
            Important! The model is mistaken."""

        # Not all fields of the goods must be filled out. Here is a motorcade of the required fields:
        required_fields:tuple = ('reference',
                                 'name',
                                 'description_short',
                                 'description',
                                 'specification',
                                 'local_image_path')
        f:ProductFields = None
        products_list = []

        # 1. Collection of goods
        for url in urls:

            graber = get_graber_by_supplier_url(url) 
            
            if not graber:
                logger.debug(f"Нет грабера для: {url}", None, False)
                ...
                continue

            try:
                # scenarios_files_list:list =  recursively_get_file_path(__root__ / 'src' / 'suppliers' / 'suppliers_list' / graber.supplier_prefix / 'scenarios', '.json')
                f = await graber.grab_page(*required_fields)
                # graber.process_graber('hb')
                ...

            except Exception as ex:
                logger.error(f"Ошибка получения полей товара",ex, False)
                ...
                continue

            if not f:
                logger.debug(f'Failed to parse product fields for URL: {url}')
                ...
                continue

            product_data = await self.convert_product_fields(f)
            if not product_data:
                logger.debug(f'Failed to convert product fields: {product_data}')
                ...
                continue

            if not await self.save_product_data(product_data):
                logger.error(f"Data not saved! {print(product_data)}")
                ...
                continue
            products_list.append(product_data)    

    async def process_scenarios(self, suppliers_prefixes:Optional[str] = '') -> bool:
        """"""
        ...
        suppliers_prefixes = suppliers_prefixes if isinstance(suppliers_prefixes, list) else [suppliers_prefixes] 
        ...


    async def save_product_data(self, product_data: dict):
        """Saves individual product data to a file.

        Args:
            product_data (dict): Formatted product data."""
        file_path = self.export_path / 'products' / f"{product_data['product_id']}.json"
        if not j_dumps(product_data, file_path, ensure_ascii=False):
            logger.error(f'Ошибка сохранения словаря {print(product_data)}\n Путь: {file_path}')
            ...
            return
        return True

    async def process_llm(self, products_list: List[str], lang:str,  attempts: int = 3) -> tuple | bool:
        """Processes The Product List Through The Ai Model.

        Args:
            Products_List (StR): List of Product Diction Dictionaries as a String.
            Attempts (Int, Optional): Number of Attempts to Retry in Case of Failure. Defaults to 3.

        Returns:
            Tuple: Processed Response in `ru` and` he` formats.
            Bool: FALSE if Unable to get a Valid Response after Retress.

        .. Note ::
            The model can return an unexpected result.
            In this case, I ask the model for a reasonable number of times."""
        if attempts < 1:
            ...
            return {}  # return early if no attempts are left
        model_command = Path(gs.path.endpoints / 'emil' / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(encoding='UTF-8')
        # Request response from the AI model
        q = model_command + '\n' + str(products_list)
        response = await self.model.ask(q)
        if not response:
            logger.error(f"Нет ответа от модели")
            ...
            return {}

        response_dict:dict = j_loads(response)

        if not response_dict:
            logger.error("Ошибка парсинга ответа модели", None, False)
            if attempts > 1:
                ...
                await self.process_llm(products_list, lang, attempts -1 )
            return {}
        return  response_dict


    async def save_in_prestashop(self, products_list:ProductFields | list[ProductFields]) -> bool:
        """The function retains goods in Prestashop by API and Domain"""

        products_list: list = products_list if isinstance(products_list, list) else [products_list]

        p = PrestaProduct(api_key=self.api_key, api_domain=self.api_domain)

        for f in products_list:
            p.add_new_product(f)
 
    async def post_facebook(self, mexiron:SimpleNamespace) -> bool:
        """The function is performed by the script for the advertising module `Facvebook`."""
        ...
        self.driver.get_url(r'https://www.facebook.com/profile.php?id=61566067514123')
        currency = "ש''ח"
        title = f'{mexiron.title}\n{mexiron.description}\n{mexiron.price} {currency}'
        if not post_message_title(self.d, title):
            logger.warning(f'Не получилось отправить название мехирона')
            ...
            return

        if not upload_post_media(self.d, media = mexiron.products):
            logger.warning(f'Не получилось отправить media')
            ...
            return
        if not message_publish(self.d):
            logger.warning(f'Не получилось отправить media')
            ...
            return

        return True

    async def create_report(self, data: dict, lang:str, html_file: Path, pdf_file: Path) -> bool:
        """The function sends the task to create a mehiron in the `html` and` pdf` format.
        If Meron in PDF is created (`Generator.create_Report ()` Return True) - 
        Send his bot"""

        report_generator = ReportGenerator()

        if await report_generator.create_report(data, lang, html_file, pdf_file):
            # Check if the file exists and whether it is a file
            if pdf_file.exists() and pdf_file.is_file():
                # Sending the PDF file via Reply_document ()
                await self.update.message.reply_document(document=pdf_file)
                return True
            else:
                logger.error(f"PDF файл не найден или не является файлом: {pdf_file}")
                return


async def upload_redacted_images_from_emil():
    """At the moment, the function reads JSON with a list of photographs that were received from Emil"""
    lang = 'he'
    products_ns = j_loads_ns(gs.path.external_storage / ENDPOINT / 'out_250108230345305_he.json')
    suppier_to_presta = SupplierToPrestashopPipeline(lang)
    products_list:list = [f for f in products_ns]
    await suppier_to_presta.save_in_prestashop(products_list)

async def main():
    """"""
    await upload_redacted_images_from_emil()


if __name__ == '__main__':
    asyncio.run( main() )





