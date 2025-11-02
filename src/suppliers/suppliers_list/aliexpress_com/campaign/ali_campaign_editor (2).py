## \file /src/suppliers/aliexpress/campaign/ali_campaign_editor (2).py
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
...
...
import re
import shutil
from pathlib import Path
from typing import List, Optional, Union
from types import SimpleNamespace

import header
from src import gs
from src.suppliers.suppliers_list.aliexpress_com.campaign.ali_promo_campaign import AliPromoCampaign
from src.suppliers.suppliers_list.aliexpress_com.utils.extract_product_id import extract_prod_ids
from src.suppliers.suppliers_list.aliexpress_com.utils.set_full_https import ensure_https
from src.utils.jjson import j_loads_ns, j_loads
from src.utils.convertors import list2string, csv2dict
from src.utils.printer import pprint
from src.utils.jjson import j_dumps, j_loads, j_loads_ns
from utils.file import read_text_file, save_text_file, get_filenames
from src.logger.logger import logger

class AliCampaignEditor(AliPromoCampaign):
    """ Editor for advertising campaigns.
    """

    def __init__(self, campaign_name: str = None, language: str | dict = 'EN', currency: str = 'USD', campaign_file:str | Path = None, force_update: bool = False):
        """ Initialize the AliCampaignEditor with the given parameters.
        
        @param campaign_name: The name of the campaign.
        @param category_name: The name of the category.
        @param language: The language of the campaign. Default is `EN`.
        @param currency: The currency for the campaign. Default is `USD`.
        @campaign_file: Можно сразу загрузить файл `<lang>.json` из корневой папки рекламной кампании
        """
        super().__init__(campaign_name = campaign_name, 
                         language = language, 
                         currency = currency, 
                         campaign_file = campaign_file,  
                         force_update = force_update)
        
    def delete_product(self, product_id: str, exc_info: bool = False):
        """ Delete a product that does not have an affiliate link"""
        _product_id = extract_prod_ids(product_id)
        
        product_path = self.category_path / 'sources.txt'
        prepared_product_path = self.category_path / '_sources.txt'
        products_list = read_text_file(product_path)
        if products_list:
            products_list = convert_list_to_homogeneous_list(products_list)
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

    def update_product(self,category_name, lang, product):
        self.dump_category_products_files(category_name,lang,product)
        
    def update_campaign(self, campaign):
        """ update capmaign properties `description`,`tags`,... """
        ...
        j_dumps(campaign, self.campaign_root / f'__{self.language}.json')

            

if __name__ == "__main__":
   
    # Load available campaigns from a source (assuming a method or file provides this list)
    available_campaigns = ["Campaign1", "Campaign2", "Campaign3"]  # Example list, replace with actual data source
    
    # Display available campaigns
    pprint(available_campaigns)
    
    # Prompt user to select a campaign
    campaign_name = input("Select a campaign from the list above: ")
    
    # Validate the selected campaign
    if campaign_name not in available_campaigns:
        print(f"Invalid campaign selected: {campaign_name}. Exiting...")
        exit(1)
    
    # Display available categories (dummy example)
    categories = ["Category1", "Category2", "Category3"]  # Example list, replace with actual data source
    pprint(categories)
    
    # Prompt user to select a category
    category_name = input("Select a category from the list above: ")
    
    # Validate the selected category
    if category_name not in categories:
        print(f"Invalid category selected: {category_name}. Exiting...")
        exit(1)
    
    # Prompt user for language (default to 'EN')
    language = input(f"Select a language (default 'EN'): ") or 'EN'
    
    # Prompt user for currency (default to 'USD')
    currency = input(f"Select a currency (default 'USD'): ") or 'USD'
    
    # Create an instance of AliCampaignEditor
    editor = AliCampaignEditor(campaign_name, category_name, language, currency)
    
    # Notify the user
    print(f"Editor created for campaign '{campaign_name}' in category '{category_name}' with language '{language}' and currency '{currency}'.")



