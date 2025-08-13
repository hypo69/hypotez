# # \file /src/endpoints/kazarinov/scenarios/quotation_builder.py
# -*- coding: utf-8 -*-\
# ! .pyenv/bin/python3

"""The module handles data preparation, AI processing, and integration with Facebook for product posting.
==================================================================
Provides functionality for extracting, parsing, and processing product data from 
various suppliers. The module handles data preparation, AI processing, 
and integration with Facebook for product posting.

```rst
.. module:: src.endpoints.kazarinov.scenarios.quotation_builder 
```"""
import re
from bs4 import BeautifulSoup
from jinja2.utils import F
from pydantic.type_adapter import P
import requests
import asyncio
import random
import shutil
from pathlib import Path
from typing import Optional, List, Any, TYPE_CHECKING
from types import SimpleNamespace
from dataclasses import field
import telebot

import header
from header import __root__
from src import gs, USE_ENV
# from src.endpoints.prestashop.product_fields import ProductFields

# from src.llm.gemini import GoogleGenerativeAi

from src.endpoints.advertisement.facebook.scenarios import (
    post_message_title, upload_post_media, message_publish
)

from src.endpoints.kazarinov.report_generator import ReportGenerator 
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.file import read_text_file, save_text_file, recursively_get_file_path
from src.utils.image import save_image_from_url_async, save_image
from src.utils.printer import pprint as print
from src.logger.logger import logger

if TYPE_CHECKING:
    from src.webdriver.pydoll import Driver

class Config:
    ENDPOINT:str = 'kazarinov'
    base_path:Path = __root__ / 'src' / 'endpoints' / ENDPOINT
    config: SimpleNamespace = j_loads_ns(base_path / f'{ENDPOINT}.json')
    model_name = config.model_name if hasattr(config, 'model_name') else 'gemini-1.5-flash'

    api_key:str = gs.credentials.gemini.kazarinov

    @property
    def system_instruction(self) -> str:
        return (self.base_path / 'instructions' / 'system_instruction_mexiron.md').read_text(encoding='UTF-8')

    translations: SimpleNamespace =  j_loads_ns(base_path / 'translations' / 'mexiron.json')


class QuotationBuilder:
    """Makes the extraction, analysis and preservation of data on suppliers.
    
    Attributes:
        Driver (Driver): SELENIUM WebDriver copy.
        Export_path (Path): the path for data export.
        Products_List (List [dict]): a list of processed goods about goods."""

    
    html_path:str|Path
    pdf_path:str|Path
    docx_path:str|Path

    # driver: Playwrid = Playwrid()
    driver:'Driver'
    export_path: Path
    mexiron_name: str
    price: float
    timestamp: str
    products_list: List = field(default_factory=list)
    model: 'GoogleGenerativeAi'

    def __init__(self,  **kwargs):
        """Initializes Mexiron class with required components.

        Args:
            mexiron_name (Optional[str]): Custom name for the Mexiron process.
            webdriver_name (Optional[str]): Name of the WebDriver to use. Defaults to 'firefox'. call to Firefox or Playwrid
            window_mode (Optional[str]): Оконный режим вебдрайвера. Может быть 'maximized', 'headless', 'minimized', 'fullscreen', 'normal', 'hidden', 'kiosk'"""

        try:
            self.model = GoogleGenerativeAi(
                model_name = Config.model_name,
                api_key = Config.api_key,
                system_instruction= Config.system_instruction,
                generation_config={'response_mime_type': 'application/json'}
            )
        except Exception as ex:
            logger.error(f"Error loading model, or instructions or API key:", ex)
            ...
            

    # def process_llm(self, products_list: List[str], lang:str,  attempts: int = 3) -> tuple | bool:
    # """# Processes The Product List Through The Ai Model.

    # Args:
    # Products_List (StR): List of Product Diction Dictionarys AS A STRING.
    # Attempts (Int, Optional): Number of Attempts to Retry in Case of Failure. Defaults to 3.

    # Returns:
    # TUPLE: Processed Response in `ru` and` he` formats.
    # Bool: FALSE if Unable to get a Valid Response after Retress.

    # Note:
    # The model can return an unimportant result.
    # In this case, I ask the model a reasonable number of times.
    # None
    # if attempts < 1:
    # None
    # return {}  # return early if no attempts are left

    # model_command = Path(gs.path.endpoints / Config.ENDPOINT / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(encoding='UTF-8')
    # # Request response from the AI model
    # q = model_command + '\n' + str(products_list)
    # response = self.model.ask(q)
    # if not response:
    # Logger.ERROR (F "There is no answer from the model")
    # None
    # return {}


    # Response_dict: dict = j_loads (response) # <- if there is an error, an empty dictionary will return

    # if not response_dict:
    # Logger.error (f "Parsing error of Model response", None, FALSE)
    # if attempts > 1:
    # None
    # self.process_llm(products_list, lang, attempts -1 )
    # return {}
    # return  response_dict


    async def post_facebook_async(self, mexiron:SimpleNamespace) -> bool:
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

def example():
    """"""
    ...

    lang:str = 'he'
    
    mexiron_name: str = '250203025325520'
    base_path:Path = Path(gs.path.external_storage)
    export_path =  Config.ENDPOINT / 'mexironim' / mexiron_name
    html_path: Path = export_path / f'{mexiron_name}_{lang}.html'
    pdf_path: Path = export_path / f'{mexiron_name}_{lang}.pdf'
    docx_path:Path = export_path / f'{mexiron_name}_{lang}.doc'
    data = j_loads(export_path / f'{mexiron_name}_{lang}.json')

    quotation = QuotationBuilder(mexiron_name)
    asyncio.run(quotation.create_reports(data[lang], mexiron_name, lang, html_path, pdf_path, docx_path))
 
def main():
    # example()
    ...

if __name__ == '__main__':
    main()




