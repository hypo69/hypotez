## \file /src/endpoints/kazarinov/scenarios/quotation_builder.py
# -*- coding: utf-8 -*-\
#! .pyenv/bin/python3

"""
The module handles data preparation, AI processing, and integration with Facebook for product posting.
==================================================================

```rst
.. module:: src.endpoints.kazarinov.scenarios.quotation_builder 
	:platform: Windows, Unix
	:synopsis: Provides functionality for extracting, parsing, and processing product data from 
various suppliers. The module handles data preparation, AI processing, 
and integration with Facebook for product posting.
```

"""
import re
from bs4 import BeautifulSoup
from jinja2.utils import F
from pydantic.type_adapter import P
import requests
import asyncio
import random
import shutil
from pathlib import Path
from typing import Optional, List, Any
from types import SimpleNamespace
from dataclasses import field
import telebot

import header
from header import __root__
from src import gs
from src.endpoints.prestashop.product_fields import ProductFields

from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from src.webdriver.playwright import Playwrid

from src.llm.gemini import GoogleGenerativeAi
from src.endpoints.advertisement.facebook.scenarios import (
    post_message_title, upload_post_media, message_publish
)
from src.suppliers.suppliers_list.morlevi.graber import Graber as MorleviGraber
from src.suppliers.suppliers_list.ksp.graber import Graber as KspGraber
from src.suppliers.suppliers_list.ivory.graber import Graber as IvoryGraber
from src.suppliers.suppliers_list.grandadvance.graber import Graber as GrandadvanceGraber
from src.endpoints.kazarinov.report_generator import ReportGenerator 

from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.file import read_text_file, save_text_file, recursively_get_file_path
from src.utils.image import save_image_from_url_async, save_image
from src.utils.printer import pprint as print
from src.logger.logger import logger


class Config:
    ENDPOINT:str = 'kazarinov'


class QuotationBuilder:
    """
    Обрабатывает извлечение, разбор и сохранение данных о продуктах поставщиков.
    
    Attributes:
        driver (Driver): Экземпляр Selenium WebDriver.
        export_path (Path): Путь для экспорта данных.
        products_list (List[dict]): Список обработанных данных о продуктах.
    """
    
    base_path:Path = __root__ / 'src' / 'endpoints' / Config.ENDPOINT

    try:
        config: SimpleNamespace = j_loads_ns(base_path / f'{Config.ENDPOINT}.json')
    except Exception as ex:
        logger.error(f"Error loading configuration",ex)

    
    html_path:str|Path
    pdf_path:str|Path
    docx_path:str|Path

    #driver: Playwrid = Playwrid()
    driver:'Driver'
    export_path: Path
    mexiron_name: str
    price: float
    timestamp: str
    products_list: List = field(default_factory=list)
    model: 'GoogleGenerativeAi'
    translations: 'SimpleNamespace' =  j_loads_ns(base_path / 'translations' / 'mexiron.json')

    # Не все поля товара надо заполнять. Вот кортеж необходимых полей:
    required_fields:tuple = ('id_product',
                                'name',
                                'description_short',
                                'description',
                                'specification',
                                'local_image_path')


    def __init__(self, mexiron_name:Optional[str] = gs.now, driver:Optional[Firefox | Playwrid | str] = None,  **kwards):
        """
        Initializes Mexiron class with required components.

        Args:
            driver (Driver): Selenium WebDriver instance.
            mexiron_name (Optional[str]): Custom name for the Mexiron process.
            webdriver_name (Optional[str]): Name of the WebDriver to use. Defaults to 'firefox'. call to Firefox or Playwrid
            window_mode (Optional[str]): Оконный режим вебдрайвера. Может быть 'maximized', 'headless', 'minimized', 'fullscreen', 'normal', 'hidden', 'kiosk'

        """
        self.mexiron_name = mexiron_name
        try:
            self.export_path = gs.path.external_storage / Config.ENDPOINT / 'mexironim' / self.mexiron_name
        except Exception as ex:
            logger.error(f"Error constructing export path:",ex)
            ...
            return

        # 1. Initialize webdriver

        kwards['window_mode'] = kwards.get('window_mode', 'normal') # <- если не указано, то нормальный режим
        if driver:

           if isinstance(driver, Driver):
                self.driver = driver

           elif isinstance(driver, (Firefox, Playwrid, )):  # Chrome, Edge
                self.driver = Driver(driver, **kwards)

           elif isinstance(driver, str):
               if driver.lower() == 'firefox':
                    self.driver = Driver(Firefox, **kwards)

               elif driver.lower() == 'playwright':
                    self.driver = Driver(Playwrid, **kwards)

        else:
            self.driver = Driver(Firefox, **kwards)



                
        # 2. Initialize Gemini model

        try:
            system_instruction:str = (gs.path.endpoints / Config.ENDPOINT / 'instructions' / 'system_instruction_mexiron.md').read_text(encoding='UTF-8')
            api_key:str = gs.credentials.gemini.kazarinov
            self.model = GoogleGenerativeAi(
                api_key=api_key,
                system_instruction=system_instruction,
                generation_config={'response_mime_type': 'application/json'}
            )
        except Exception as ex:
            logger.error(f"Error loading model, or instructions or API key:", ex)
            ...
            


    def convert_product_fields(self, f: ProductFields) -> dict:
        """
        Converts product fields into a dictionary. 
        Функция конвертирует поля из объекта `ProductFields` в простой словарь для модели ии.


        Args:
            f (ProductFields): Object containing parsed product data.

        Returns:
            dict: Formatted product data dictionary.

        .. note:: Правила построения полей определяются в `ProductFields`
        """
        if not f.id_product:
            logger.error(f"Сбой при получении полей товара. ")
            return {} # <- сбой при получении полей товара. Такое может произойти если вместо страницы товара попалась страница категории, при невнимательном составлении мехирона из комплектующих
        ...



        product_name = f.name['language']['value'] if f.name else ''
        description = f.description['language']['value'] if f.description else ''
        description_short = f.description_short['language']['value'] if f.description_short else ''
        specification = f.specification['language']['value']  if f.specification else ''
        
        if not product_name:
            return {}
        return {
            'product_name':product_name,
            'product_id': f.id_product,
            'description_short':description_short,
            'description': description,
            'specification': specification,
            'local_image_path': str(f.local_image_path),
        }

    def process_llm(self, products_list: List[str], lang:str,  attempts: int = 3) -> tuple | bool:
        """
        Processes the product list through the AI model.

        Args:
            products_list (str): List of product data dictionaries as a string.
            attempts (int, optional): Number of attempts to retry in case of failure. Defaults to 3.

        Returns:
            tuple: Processed response in `ru` and `he` formats.
            bool: False if unable to get a valid response after retries.

        .. note::
            Модель может возвращать невалидный результат.
            В таком случае я переспрашиваю модель разумное количество раз.
        """
        if attempts < 1:
            ...
            return {}  # return early if no attempts are left

        model_command = Path(gs.path.endpoints / Config.ENDPOINT / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(encoding='UTF-8')
        # Request response from the AI model
        q = model_command + '\n' + str(products_list)
        response = self.model.ask(q)
        if not response:
            logger.error(f"Нет ответа от модели")
            ...
            return {}


        response_dict:dict = j_loads(response) # <- если будет ошибка , то вернется пустой словарь

        if not response_dict:
            logger.error(f"Ошибка парсинга ответа модели", None, False)
            if attempts > 1:
                ...
                self.process_llm(products_list, lang, attempts -1 )
            return {}
        return  response_dict

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
            Модель может возвращать невалидный результат.
            В таком случае я переспрашиваю модель разумное количество раз.
        """
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

        response_dict:dict = j_loads(response) # <- если будет ошибка , то вернется пустой словарь

        if not response_dict:
            logger.error(f'Ошибка {attempts} парсинга ответа модели', None, False)
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
            logger.error(f'Ошибка сохранения словаря {print(product_data)}\n Путь: {file_path}')
            ...
            return
        return True

 
    async def post_facebook_async(self, mexiron:SimpleNamespace) -> bool:
        """Функция исполняет сценарий рекламного модуля `facvebook`."""
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

def main():
    """"""
    ...
    lang:str = 'he'
    
    mexiron_name: str = '250203025325520'
    base_path:Path = Path(gs.path.external_storage)
    export_path = base_path / ENDPOINT / 'mexironim' / mexiron_name
    html_path: Path = export_path / f'{mexiron_name}_{lang}.html'
    pdf_path: Path = export_path / f'{mexiron_name}_{lang}.pdf'
    docx_path:Path = export_path / f'{mexiron_name}_{lang}.doc'
    data = j_loads(export_path / f'{mexiron_name}_{lang}.json')

    quotation = QuotationBuilder(mexiron_name)
    asyncio.run(quotation.create_reports(data[lang], mexiron_name, lang, html_path, pdf_path, docx_path))
    

if __name__ == '__main__':
    main()




