## \file /src/suppliers/aliexpress/campaign/_experiments/prepare_campaign (2).py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._experiments 
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
  
""" module: src.suppliers.suppliers_list.aliexpress_com.campaign._experiments """


""" Проверка создания рекламной кампании """


...
import header
from pathlib import Path
#from src.suppliers.suppliers_list.aliexpress_com.campaign import AliCampaignEditor
from src import gs
from src.suppliers.suppliers_list.aliexpress_com.campaign import process_campaign_category, process_campaign
from src.utils import get_filenames, get_directory_names
from src.utils.printer import pprint
from src.logger.logger import logger

locales = {'EN': 'USD', 'HE': 'ILS', 'RU': 'ILS'}
campaign_name:str = 'rc'
language: str = 'EN'
currency: str = 'USD'
campaign_file:str = None
process_campaign(campaign_name = campaign_name, language = language, currency = currency, campaign_file = campaign_file)

    