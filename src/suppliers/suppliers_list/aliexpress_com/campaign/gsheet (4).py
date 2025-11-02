## \file /src/suppliers/aliexpress/campaign/gsheet (4).py
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


import time
from src.llm.openai import translate
from types import SimpleNamespace
from typing import List
from gspread.worksheet import Worksheet
from gspread_formatting import (
    cellFormat, 
    textFormat, 
    numberFormat, 
    format_cell_range,
    set_column_width,
    set_row_height,
    Color
)
from src.goog.spreadsheet.spreadsheet import SpreadSheet,Worksheet
from src.suppliers.suppliers_list.aliexpress_com.campaign import AliCampaignEditor
from src.webdriver.selenium.driver import Driver, Chrome
from src.utils.jjson import j_dumps, j_loads, j_loads_ns
from src.utils.printer import pprint
from src.logger.logger import logger

d = Driver(Chrome)
class AliCampaignGoogleSheet(SpreadSheet,AliCampaignEditor):
    """ Class for working with Google Sheets within AliExpress campaigns.
    
    Inherits the SpreadSheet class and provides additional methods for managing Google Sheets,
    writing category and product data, and formatting sheets.
    """
    ...
    spreadsheet_id = '1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0'
    spreadsheet:SpreadSheet
    worksheet:Worksheet
    
    def __init__(self, campaign_name:str = None, category_name = None, driver:Driver = None):
        """ Initialize AliSheet with the specified Google Sheets spreadsheet ID.
        @param spreadsheet_id Google Sheets spreadsheet ID.
        """
        ...
        
        super().__init__(spreadsheet_id = self.spreadsheet_id, 
                         campaign_name = campaign_name,
                         )
        #d = Driver(Chrome) if not driver else driver 
        d.get_url(fr'https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}')
        self.clear()
    
    def clear(self):
        """ Очистка содержимого. 
        Удаление листов товаров и очистка данных на листе категорий"""
        ...
        self.delete_all_worksheets()
        ws: Worksheet = self.get_worksheet('categories').clear()
        
        
    def delete_all_worksheets(self):
        """ Delete all sheets from the Google Sheets spreadsheet except 'Sheet1'.
        Deletes all sheets except the default sheet named 'Sheet1'.
        """
        try:
            worksheets = self.spreadsheet.worksheets()
            for sheet in worksheets:
                if sheet.title != 'categories' and sheet.title != 'product_template':
                    self.spreadsheet.del_worksheet_by_id(sheet.id)
                    logger.info(f"Worksheet '{sheet.title}' deleted.")
        except Exception as ex:
            logger.error("Error deleting all worksheets.", ex, exc_info=True)
            raise
        
    def set_category_worksheet(self, category: str | SimpleNamespace ):
        """Write data from a SimpleNamespace object to Google Sheets cells vertically.
        
        Args:
            category (SimpleNamespace): SimpleNamespace object with data fields for writing.
        """
        category = category if isinstance(category,SimpleNamespace) else 
        try:
            ws: Worksheet = self.get_worksheet('category').clear()  # Clear the 'category' worksheet
            
            # Prepare data for vertical writing
            vertical_data = [
                (f'Name', category.name),
                (f'Title', category.title),
                (f'Description', category.description),
                (f'Tags', ', '.join(category.tags)),
                (f'Products Count', category.products_count),
            ]
            
            # Write data vertically
            for row_index, (header, value) in enumerate(vertical_data, start=1):
                ws.update(f'A{row_index}', header)  # Column A: Field names
                ws.update(f'B{row_index}', str(value))  # Column B: Field values as strings
                
            logger.info("Category data written to 'category' worksheet vertically.")
            
        except Exception as ex:
            logger.error("Error setting category worksheet.", ex, exc_info=True)
            raise

    def set_categories_worksheet(self, ns_list: list[SimpleNamespace] | SimpleNamespace):
        """ Write data from a list of SimpleNamespace objects to Google Sheets cells.
        @param ns_list List of SimpleNamespace objects with data fields for writing.
        """
        ## <- задача: Если пришел один ns_list - обработать его в странице ('worksheet') категория.
        # если такой страницы нет - создать ее. На странице одной категории разместить ячейки 
        # вертикально. слева - название поля, спава - значение
        ws: Worksheet = self.get_worksheet('categories').clear()
        
        #ws.clear()
        try:
            if all(all(hasattr(value, attr) for attr in ['name', 'title', 'description', 'tags', 'products_count']) for value in ns_list):
                # headers = ['name', 'title', 'description', 'tags', 'products_count']
                # ws.update('A1:E1', [headers])

                updates = []
                for index, value in enumerate(ns_list, start=2):
                    row_data = [
                        str(value.name),
                        str(value.title),
                        str(value.description),
                        ', '.join(value.tags),
                        str(value.products_count),
                    ]
                    updates.append({
                        'range': f'A{index}:E{index}',
                        'values': [row_data]
                    })
                
                ws.batch_update(updates)
                logger.info("Fields updated from SimpleNamespace list.")
            else:
                logger.warning("The list does not contain SimpleNamespace objects with all required attributes.")
                
            self.delete_all_worksheets()
            
        except Exception as ex:
            logger.error("Error updating fields from SimpleNamespace list.", ex, exc_info=True)
            raise

    def get_categories(self) -> SimpleNamespace:
        """ Retrieve data from the Google Sheets spreadsheet.
        @return Data from the spreadsheet as a list of dictionaries.
        """
        ...
        ws = self.spreadsheet.get_worksheet('categories') 
        data = ws.get_all_records()
        logger.info(f"Categories data retrieved from worksheet. \n {pprint(data)}")
        return SimpleNamespace(**data)


    def set_category_products(self, category_name: str, products: dict):
        """ Write product data to a new Google Sheets spreadsheet.
        @param category_name Category name.
        @param products Dictionary with product data.
        """
        time.sleep(10)
        ws = self.copy_worksheet('product_template', category_name)  # Copy 'product_template' to new worksheet
        try:
            headers = [
                'product_id', 'app_sale_price', 'original_price', 'sale_price', 'discount',
                'product_main_image_url', 'local_image_path', 'product_small_image_urls',
                'product_video_url', 'local_video_path', 'first_level_category_id',
                'first_level_category_name', 'second_level_category_id', 'second_level_category_name',
                'target_sale_price', 'target_sale_price_currency', 'target_app_sale_price_currency',
                'target_original_price_currency', 'original_price_currency', 'product_title',
                'evaluate_rate', 'promotion_link', 'shop_url', 'shop_id', 'tags'
            ]
            ws.update('A1:Y1', [headers])

            updates = []
            for index, product in enumerate(products, start=2):
                _ = product.__dict__
                row_data = [
                    str(_.get('product_id')),
                    str(_.get('app_sale_price')),
                    str(_.get('original_price')),
                    str(_.get('sale_price')),
                    str(_.get('discount')),
                    str(_.get('product_main_image_url')),
                    str(_.get('local_image_path')),
                    ', '.join(map(str, _.get('product_small_image_urls', []))),
                    str(_.get('product_video_url')),
                    str(_.get('local_video_path')),
                    str(_.get('first_level_category_id')),
                    str(_.get('first_level_category_name')),
                    str(_.get('second_level_category_id')),
                    str(_.get('second_level_category_name')),
                    str(_.get('target_sale_price')),
                    str(_.get('target_sale_price_currency')),
                    str(_.get('target_app_sale_price_currency')),
                    str(_.get('target_original_price_currency')),
                    str(_.get('original_price_currency')),
                    str(_.get('product_title')),
                    str(_.get('evaluate_rate')),
                    str(_.get('promotion_link')),
                    str(_.get('shop_url')),
                    str(_.get('shop_id')),
                    ', '.join(map(str, _.get('tags', [])))
                ]
                updates.append({
                    'range': f'A{index}:Y{index}',
                    'values': [row_data]
                })
            
            ws.batch_update(updates)

            logger.info("Products updated in worksheet.")
        except Exception as ex:
            logger.error("Error updating products in worksheet.", ex, exc_info=True)
            raise

    def translate_text(self, text: str, target_language: str) -> str:
        """ Translate text to the target language using OpenAI's translation service.
        @param text Text to be translated.
        @param target_language Target language for translation.
        @return Translated text.
        """
        try:
            translated_text = translate(text, target_language)
            logger.info(f"Text successfully translated to {target_language}.")
            return translated_text
        except Exception as ex:
            logger.error("Error translating text.", ex, exc_info=True)
            raise
