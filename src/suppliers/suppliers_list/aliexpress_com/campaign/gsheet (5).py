## \file /src/suppliers/aliexpress/campaign/gsheet (5).py
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


""" Редактор рекламной кампании через гугл таблицами """



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
from src.goog.spreadsheet.spreadsheet import SpreadSheet
from src.suppliers.suppliers_list.aliexpress_com.campaign.ali_campaign_editor import AliCampaignEditor
from src.webdriver.selenium.driver import Driver, Chrome
from src.utils.jjson import j_dumps, j_loads, j_loads_ns
from src.utils.printer import pprint
from src.logger.logger import logger

d = Driver(Chrome)

class AliCampaignGoogleSheet(SpreadSheet, AliCampaignEditor):
    """ Class for working with Google Sheets within AliExpress campaigns.
    
    Inherits the SpreadSheet class and provides additional methods for managing Google Sheets,
    writing category and product data, and formatting sheets.
    """
    ...
    spreadsheet_id = '1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0'
    spreadsheet: SpreadSheet
    worksheet: Worksheet
    
    def __init__(self, campaign_name: str = None, category_name = None, driver: Driver = None):
        """ Initialize AliSheet with the specified Google Sheets spreadsheet ID.
        @param campaign_name: The name of the campaign.
        @param category_name: The name of the category.
        @param driver: The web driver for interacting with Google Sheets.
        """
        ...
        super().__init__(spreadsheet_id=self.spreadsheet_id, 
                         campaign_name=campaign_name)
        d.get_url(fr'https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}')
        self.clear()
    
    def clear(self):
        """ Clear contents.
        Delete product sheets and clear data on the categories sheet."""
        ...
        self.delete_all_worksheets()
        ws: Worksheet = self.get_worksheet('categories').clear()
        
    def delete_all_worksheets(self):
        """ Delete all sheets from the Google Sheets spreadsheet except 'categories' and 'product_template'."""
        try:
            worksheets = self.spreadsheet.worksheets()
            for sheet in worksheets:
                if sheet.title != 'categories' and sheet.title != 'product_template':
                    self.spreadsheet.del_worksheet_by_id(sheet.id)
                    logger.info(f"Worksheet '{sheet.title}' deleted.")
        except Exception as ex:
            logger.error("Error deleting all worksheets.", ex, exc_info=True)
            raise
        
    def set_category_worksheet(self, category: str | SimpleNamespace):
        """Write data from a SimpleNamespace object to Google Sheets cells vertically.
        
        Args:
            category (SimpleNamespace): SimpleNamespace object with data fields for writing.
        """
        category
        try:
            ws: Worksheet = self.get_worksheet('category').clear()  # Clear the 'category' worksheet
            
            # Prepare data for vertical writing
            vertical_data = [
                ('Name', category.name),
                ('Title', category.title),
                ('Description', category.description),
                ('Tags', ', '.join(category.tags)),
                ('Products Count', category.products_count),
            ]
            
            # Write data vertically
            for row_index, (header, value) in enumerate(vertical_data, start=1):
                ws.update(f'A{row_index}', header)  # Column A: Field names
                ws.update(f'B{row_index}', str(value))  # Column B: Field values as strings
                
            logger.info("Category data written to 'category' worksheet vertically.")
            
        except Exception as ex:
            logger.error("Error setting category worksheet.", ex, exc_info=True)
            raise

    def set_categories_worksheet(self, ns_list: List[SimpleNamespace] | SimpleNamespace):
        """ Write data from a list of SimpleNamespace objects to Google Sheets cells.
        @param ns_list: List of SimpleNamespace objects with data fields for writing.
        """
        ws: Worksheet = self.get_worksheet('categories').clear()
        
        try:
            if all(all(hasattr(value, attr) for attr in ['name', 'title', 'description', 'tags', 'products_count']) for value in ns_list):
                updates = []
                for index, value in enumerate(ns_list, start=2):
                    updates.append({'range': f'A{index}', 'values': [[value.name]]})
                    updates.append({'range': f'B{index}', 'values': [[value.title]]})
                    updates.append({'range': f'C{index}', 'values': [[value.description]]})
                    updates.append({'range': f'D{index}', 'values': [[', '.join(value.tags)]]})
                    updates.append({'range': f'E{index}', 'values': [[value.products_count]]})
                
                ws.batch_update(updates)
                logger.info("Categories data written to 'categories' worksheet.")
            else:
                logger.error("List does not contain required attributes.")
        
        except Exception as ex:
            logger.error("Error setting categories worksheet.", ex, exc_info=True)
            raise
        
    def set_product_worksheet(self, product: str | SimpleNamespace):
        """ Write product data to a Google Sheets worksheet.
        @param product: SimpleNamespace object with product data fields for writing.
        """
        try:
            ws: Worksheet = self.get_worksheet('products').clear()  # Clear the 'products' worksheet
            
            # Prepare data for vertical writing
            vertical_data = [
                ('ID', product.id),
                ('Name', product.name),
                ('Title', product.title),
                ('Description', product.description),
                ('Tags', ', '.join(product.tags)),
                ('Price', product.price),
            ]
            
            # Write data vertically
            for row_index, (header, value) in enumerate(vertical_data, start=1):
                ws.update(f'A{row_index}', header)  # Column A: Field names
                ws.update(f'B{row_index}', str(value))  # Column B: Field values as strings
                
            logger.info("Product data written to 'products' worksheet vertically.")
            
        except Exception as ex:
            logger.error("Error setting product worksheet.", ex, exc_info=True)
            raise

    def set_products_worksheet(self, ns_list: List[SimpleNamespace] | SimpleNamespace):
        """ Write data from a list of SimpleNamespace objects to Google Sheets cells.
        @param ns_list: List of SimpleNamespace objects with data fields for writing.
        """
        ws: Worksheet = self.get_worksheet('products').clear()
        
        try:
            if all(all(hasattr(value, attr) for attr in ['id', 'name', 'title', 'description', 'tags', 'price']) for value in ns_list):
                updates = []
                for index, value in enumerate(ns_list, start=2):
                    updates.append({'range': f'A{index}', 'values': [[value.id]]})
                    updates.append({'range': f'B{index}', 'values': [[value.name]]})
                    updates.append({'range': f'C{index}', 'values': [[value.title]]})
                    updates.append({'range': f'D{index}', 'values': [[value.description]]})
                    updates.append({'range': f'E{index}', 'values': [[', '.join(value.tags)]]})
                    updates.append({'range': f'F{index}', 'values': [[value.price]]})
                
                ws.batch_update(updates)
                logger.info("Products data written to 'products' worksheet.")
            else:
                logger.error("List does not contain required attributes.")
        
        except Exception as ex:
            logger.error("Error setting products worksheet.", ex, exc_info=True)
            raise
    
    def set_campaign(self, campaign: SimpleNamespace):
        """ Write campaign data to a Google Sheets worksheet.
        @param campaign: SimpleNamespace object with campaign data fields for writing.
        """
        try:
            ws: Worksheet = self.get_worksheet('campaign').clear()  # Clear the 'campaign' worksheet
            
            # Prepare data for vertical writing
            vertical_data = [
                ('Name', campaign.name),
                ('Title', campaign.title),
                ('Description', campaign.description),
                ('Tags', ', '.join(campaign.tags)),
                ('Budget', campaign.budget),
                ('Duration', campaign.duration),
            ]
            
            # Write data vertically
            for row_index, (header, value) in enumerate(vertical_data, start=1):
                ws.update(f'A{row_index}', header)  # Column A: Field names
                ws.update(f'B{row_index}', str(value))  # Column B: Field values as strings
                
            logger.info("Campaign data written to 'campaign' worksheet vertically.")
            
        except Exception as ex:
            logger.error("Error setting campaign worksheet.", ex, exc_info=True)
            raise
    
    def clear_and_add_worksheets(self):
        """ Clear existing sheets and add a new sheet."""
        self.clear()
        ws: Worksheet = self.add_worksheet('new_sheet')

if __name__ == "__main__":
    # Example usage
    campaign_editor = AliCampaignGoogleSheet()
    # Your additional code here
