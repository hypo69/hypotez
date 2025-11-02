## \file /src/suppliers/aliexpress/campaign/ali_campaign_editor (4).py
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
from src.suppliers.suppliers_list.aliexpress_com.utils import extract_prod_ids, ensure_https
from src.utils.jjson import j_loads_ns, j_loads, j_dumps
from src.utils.convertors.csv import  csv2dict
from src.utils.printer import pprint
from src.utils.file import read_text_file, save_text_file, get_filenames
from src.logger.logger import logger

class AliCampaignEditor(AliPromoCampaign):
    """ Editor for advertising campaigns.
    """
    ...

    
    def __init__(self, campaign_name: Optional[str] = None, language: Optional[str | dict] = 'EN', currency: Optional[str] = 'USD', campaign_file:Optional[str | Path] = None):
        """ Initialize the AliCampaignEditor with the given parameters.
        
        @param campaign_name: The name of the campaign.
        @param language: The language of the campaign. Default is `EN`.
        @param currency: The currency for the campaign. Default is `USD`.
        @param campaign_file: Optionally load a `<lang>.json` file from the campaign root folder.
        """
        if not campaign_name and not campaign_file:
            logger.critical(f"Нет данных (название рекламной камании `campaign_name` или `campaign_file`)")
            return
        super().__init__(campaign_name = campaign_name, language = language, currency = currency, campaign_file = campaign_file)

    
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
                        save_text_file((products_list, '\n'), prepared_product_path)
                        break
                else:
                    if record == str(product_id):
                        products_list.remove(record)
                        save_text_file((products_list, '\n'), product_path)
                    
        else:
            product_path = self.category_path / 'sources' / f'{product_id}.html'    
            try:
                product_path.rename(self.category_path / 'sources' / f'{product_id}_.html')
                # product_path.unlink()
                logger.success(f"Product file {product_path=} renamed successfully.")
            except FileNotFoundError as ex:
                logger.error(f"Product file {product_path=} not found.", exc_info=exc_info)
            except Exception as ex:
                logger.critical(f"An error occurred while deleting the product file {product_path}.", ex)

    def update_product(self, category_name, lang, product):
        """ """
        self.dump_category_products_files(category_name, lang, product)
        
    def update_campaign(self):
        """ Update campaign properties `description`, `tags`, etc."""
        ...

    def update_category(self, json_path: Path, category: SimpleNamespace):
        """
        Update the category in the JSON file.
        @param json_path: Path to the JSON file.
        @param category: Category object to be updated.
        @return: True if update is successful, False otherwise.
        """
        try:
            data = j_loads(json_path)  # Read JSON data from file
            data['category'] = category.__dict__  # Convert SimpleNamespace to dict
            j_dumps(data, json_path)  # Write updated JSON data back to file
        except Exception as ex:
            logger.error(f"Failed to update category {json_path}: {ex}")
            
    def get_category(self, category_name: str) -> Optional[SimpleNamespace]:
        """ Returns the SimpleNamespace object for a given category name.
        @param campaign: The SimpleNamespace object representing the campaign.
        @param category_name: The name of the category to retrieve.
        @return: SimpleNamespace object representing the category or None if not found.
        """
        try:
            if hasattr(self.campaign.category, category_name):
                return getattr(self.campaign.category, category_name)
            else:
                logger.warning(f"Category {category_name} not found in the campaign.")
        except Exception as ex:
            logger.error(f"Error retrieving category {category_name}.", ex, exc_info=True)


