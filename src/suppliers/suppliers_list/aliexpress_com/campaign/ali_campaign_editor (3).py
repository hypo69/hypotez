## \file /src/suppliers/aliexpress/campaign/ali_campaign_editor (3).py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.suppliers.suppliers_list.aliexpress_com.campaign """


""" This module provides the editor for advertising campaigns.
"""


import re
import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional

import header
from src import gs
from src.suppliers.suppliers_list.aliexpress_com.campaign.ali_promo_campaign import AliPromoCampaign
from src.suppliers.suppliers_list.aliexpress_com.utils.extract_product_id import extract_prod_ids
from src.suppliers.suppliers_list.aliexpress_com.utils.set_full_https import ensure_https
from src.utils.jjson import j_loads_ns, j_loads, j_dumps
from src.utils.convertors import list2string, csv2dict
from src.utils.printer import pprint
from utils.file import read_text_file, save_text_file, get_filenames
from src.logger.logger import logger

class AliCampaignEditor(AliPromoCampaign):
    """ Editor for advertising campaigns.
    """

    def __init__(self, campaign_name: str = None, language: str | dict = 'EN', currency: str = 'USD', campaign_file: str | Path = None, force_update: bool = False):
        """ Initialize the AliCampaignEditor with the given parameters.
        
        @param campaign_name: The name of the campaign.
        @param language: The language of the campaign. Default is `EN`.
        @param currency: The currency for the campaign. Default is `USD`.
        @param campaign_file: Optionally load a `<lang>.json` file from the campaign root folder.
        """
        super().__init__(campaign_name=campaign_name, 
                         language=language, 
                         currency=currency, 
                         campaign_file=campaign_file,  
                         force_update=force_update)
        
    def delete_product(self, product_id: str, exc_info: bool = False):
        """ Delete a product that does not have an affiliate link"""
        _product_id = extract_prod_ids(product_id)
        
        product_path = self.category_path / 'sources.txt'
        prepared_product_path = self.category_path / '_sources.txt'
        products_list = read_text_file(product_path)
        if products_list:
            #products_list = convert_list_to_homogeneous_list(products_list)
            ...
            for record in products_list:
                if _product_id:
                    record_id = extract_prod_ids(record)
                    if record_id == str(product_id):
                        products_list.remove(record)
                        save_text_file(list2string(products_list, '\n'), prepared_product_path)
                        break
                else:
                    if record == str(product_id):
                        products_list.remove(record)
                        save_text_file(list2string(products_list, '\n'), product_path)
                    
        else:
            product_path = self.category_path / 'sources' / f'{product_id}.html'    
            try:
                product_path.rename(self.category_path / 'sources' / f'{product_id}_.html')
                # product_path.unlink()
                logger.success(f"Product file {product_path} renamed successfully.")
            except FileNotFoundError as ex:
                logger.error(f"Product file {product_path} not found.", exc_info=exc_info)
            except Exception as ex:
                logger.critical(f"An error occurred while deleting the product file {product_path}.", ex)

    def update_product(self, category_name, lang, product):
        self.dump_category_products_files(category_name, lang, product)
        
    def update_campaign(self):
        """ Update campaign properties `description`, `tags`, etc."""
        ...
        j_dumps(self.campaign, self.campaign_root / f'{self.campaign.language}_updated.json')
        
    def init_campaign(self, campaign_name:str, language: str | dict = None, currency: str = None):
        self.__init__(campaign_name=campaign_name,language=language,currency=currency)
        return self.raw_campaign_data
        ...
    

