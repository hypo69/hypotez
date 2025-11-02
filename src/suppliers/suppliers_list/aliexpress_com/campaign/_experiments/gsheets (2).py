## \file /src/suppliers/aliexpress/campaign/_experiments/gsheets (2).py
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


""" Работа с гугл таблицами """


import header
from types import SimpleNamespace
from gspread import Spreadsheet, Worksheet
#from src.suppliers.suppliers_list.aliexpress import campaign
from src.suppliers.suppliers_list.aliexpress_com.campaign import AliSheet, AliCampaignEditor
from src.suppliers.suppliers_list.aliexpress_com.campaign.ttypes import CampaignType, CategoryType, ProductType
from src.utils.printer import pprint

# Инициализация объекта AliSheet
sheet = AliSheet('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')

campaign_name = "030724_men_summer_fashion"
language = 'EN'
currency = 'USD'

# Инициализация объекта AliCampaignEditor
campaign_editor = AliCampaignEditor(campaign_name, language, currency)
campaign_data = campaign_editor.raw_campaign_data
_categories: SimpleNamespace = campaign_data.category

# Получение списка категорий из SimpleNamespace
categories_list: list[CategoryType] = [getattr(_categories, _category_name) for _category_name in vars(_categories)]

# Установка категорий в Google Sheet
sheet.set_categories(categories_list)

# Получение отредактированных категорий из Google Sheet
edited_categories: list[dict] = sheet.get_categories()

# Обновление объекта _categories с отредактированными данными
_edited_categories:SimpleNamespace = SimpleNamespace()
for _cat in edited_categories:
    _cat_ns: CategoryType = campaign_editor.create_category_namespace(
        name=_cat['name'],
        title=_cat['title'],
        description=_cat['description'],
        tags=_cat['tags'],
        products_count=_cat['products_count']
    )
    setattr(_edited_categories, _cat_ns.name, _cat_ns)

# Создание словаря для кампании
campaign_dict: dict = {
    'name': campaign_data.campaign_name,
    'title': campaign_data.title,
    'language': language,
    'currency': currency,
    'category': _edited_categories
}

# Создание объекта CampaignType из словаря
edited_campaign: CampaignType = campaign_editor.create_campaign_namespace(**campaign_dict)

# Пример использования pprint для вывода данных
pprint(edited_campaign)
