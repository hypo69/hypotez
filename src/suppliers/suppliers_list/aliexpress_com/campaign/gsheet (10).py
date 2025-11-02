## \file /src/suppliers/aliexpress/campaign/gsheet (10).py
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


""" AliPromoCampaignEditorWidgets handles campaign and product data management."""

from pathlib import Path
from types import SimpleNamespace
from src.logger.logger import logger
from src.utils.jjson import j_loads_ns, j_loads_ns, j_dumps
from src.suppliers.suppliers_list.aliexpress import AliCampaignGoogleSheet
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from gspread import Worksheet
import gspread
import os
import requests
import re

class AliPromoCampaignEditorWidgets:
    def __init__(self):
        """ Initialize the AliPromoCampaignEditorWidgets class."""
        self.spreadsheet = None
        self.editor = SimpleNamespace()
        self.editor.campaign = SimpleNamespace()
        self.editor.categories = []
        self.editor.products = []

    def get_worksheet(self, title: str) -> Worksheet:
        """ Retrieve a worksheet by title from the Google Sheets spreadsheet.
        @param title `str`: The title of the worksheet to retrieve.
        @return `Worksheet`: The worksheet object, or `None` if not found.
        """
        try:
            worksheet = self.spreadsheet.worksheet(title)
            return worksheet
        except gspread.WorksheetNotFound:
            logger.error(f"Worksheet with title '{title}' not found.")
            return
        except Exception as ex:
            logger.error("Error retrieving worksheet.", ex, exc_info=True)
            raise

    def set_campaign_worksheet(self, campaign: SimpleNamespace):
        """ Write campaign data to the 'campaign' worksheet.
        @param campaign `SimpleNamespace`: SimpleNamespace object with campaign data fields.
        """
        try:
            ws: Worksheet = self.spreadsheet.add_worksheet(title='campaign', rows=100, cols=10)
            _ = campaign.__dict__
            data = [
                ['Name', _.get('name', '')],
                ['Title', _.get('title', '')],
                ['Language', _.get('language', '')],
                ['Currency', _.get('currency', '')],
                ['Start Date', _.get('start_date', '')],
                ['End Date', _.get('end_date', '')]
            ]

            for row_index, (header, value) in enumerate(data, start=1):
                ws.update(f'A{row_index}', header)
                ws.update(f'B{row_index}', str(value))
                
            logger.info("Campaign data written to 'campaign' worksheet.")
        except Exception as ex:
            logger.error("Error setting campaign worksheet.", ex, exc_info=True)
            raise

    def set_categories_worksheet(self, categories: list[SimpleNamespace]):
        """ Write categories data to the 'categories' worksheet.
        @param categories `list[SimpleNamespace]`: List of SimpleNamespace objects with category data fields.
        """
        try:
            ws: Worksheet = self.spreadsheet.add_worksheet(title='categories', rows=100, cols=10)
            headers = ['ID', 'Name', 'Tag', 'Product Count']
            ws.update('A1:D1', [headers])

            for row_index, category in enumerate(categories, start=2):
                data = [
                    category.id,
                    category.name,
                    ', '.join(category.tags),
                    category.product_count
                ]
                ws.update(f'A{row_index}:D{row_index}', [data])
                
            logger.info("Categories data written to 'categories' worksheet.")
        except Exception as ex:
            logger.error("Error setting categories worksheet.", ex, exc_info=True)
            raise

    def set_product_worksheet(self, category_name: str, product: SimpleNamespace | str):
        """ Write product data to a new worksheet with the title 'product_{product.id}'.
        @param category_name `str`: The name of the product's category.
        @param product `SimpleNamespace | str`: SimpleNamespace object with product data fields for writing.
        """
        product = product if isinstance(product, SimpleNamespace) else self.get_category_product(category_name, product)
        try:
            ws_title = f"product_{product.id}"
            ws: Worksheet = self.spreadsheet.add_worksheet(title=ws_title, rows=100, cols=10)
            _ = product.__dict__
            vertical_data = [
                ['ID', _.get('id', '')],
                ['Name', _.get('name', '')],
                ['Title', _.get('title')],
                ['Description', _.get('description')],
                ['Images', ', '.join(map(str, _.get('images', [])))],
                ['Video URL', _.get('video_url')],
                ['Category', ', '.join(map(str, _.get('category', [])))],
                ['Tags', ', '.join(map(str, _.get('tags', [])))],
                ['Price', _.get('price')]
            ]
            
            for row_index, (header, value) in enumerate(vertical_data, start=1):
                ws.update(f'A{row_index}', header)
                ws.update(f'B{row_index}', str(value))
                
            logger.info("Product data written to new Google Sheets worksheet vertically.")
        except Exception as ex:
            logger.error("Error setting product worksheet.", ex, exc_info=True)
            raise
    
    def get_product_worksheet(self, product_id: str) -> SimpleNamespace:
        """ Read product data from the 'product_{product_id}' worksheet.
        @param product_id `str`: The ID of the product to read data from.
        @return `SimpleNamespace`: SimpleNamespace object with product data fields.
        """
        try:
            ws_title = f"product_{product_id}"
            ws: Worksheet = self.get_worksheet(ws_title)
            if not ws:
                raise ValueError(f"Worksheet '{ws_title}' not found.")
            
            data = ws.get_all_values()
            product_data = SimpleNamespace(
                id=data[0][1],
                name=data[1][1],
                title=data[2][1],
                description=data[3][1],
                images=data[4][1].split(', '),
                video_url=data[5][1],
                category=data[6][1].split(', '),
                tags=data[7][1].split(', '),
                price=float(data[8][1])
            )
            
            logger.info(f"Product data read from '{ws_title}' worksheet.")
            return product_data
        except Exception as ex:
            logger.error(f"Error getting product data from worksheet '{ws_title}'.", ex, exc_info=True)
            raise
    
    def delete_products_worksheets(self):
        """ Delete worksheets in the current Google Sheets spreadsheet with titles starting with 'product_'."""
        try:
            for ws in self.spreadsheet.worksheets():
                if ws.title.startswith('product_'):
                    self.spreadsheet.del_worksheet(ws)
                    logger.info(f"Worksheet '{ws.title}' deleted.")
        except Exception as ex:
            logger.error("Error deleting product worksheets.", ex, exc_info=True)
            raise
    
    def save_campaign(self, filename: str):
        """ Save campaign data to a JSON file.
        @param filename `str`: The name of the file to save the campaign data to.
        """
        try:
            campaign_data = self.editor.campaign.__dict__
            campaign_json = j_dumps(campaign_data)
            
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(campaign_json)
            
            logger.info(f"Campaign data saved to {filename}.")
        except Exception as ex:
            logger.error("Error saving campaign data.", ex, exc_info=True)
            raise
    
    def load_campaign(self, filename: str):
        """ Load campaign data from a JSON file.
        @param filename `str`: The name of the file to load the campaign data from.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                campaign_data = j_loads(file.read())
            
            self.editor.campaign = SimpleNamespace(**campaign_data)
            logger.info(f"Campaign data loaded from {filename}.")
        except Exception as ex:
            logger.error("Error loading campaign data.", ex, exc_info=True)
            raise
    
    def validate_worksheet_data(self, ws_title: str) -> bool:
        """ Validate if the worksheet contains data.
        @param ws_title `str`: The title of the worksheet to validate.
        @return `bool`: `True` if the worksheet contains data, `False` otherwise.
        """
        try:
            ws: Worksheet = self.get_worksheet(ws_title)
            if not ws:
                raise ValueError(f"Worksheet '{ws_title}' not found.")
            
            data = ws.get_all_values()
            is_valid = len(data) > 1
            
            logger.info(f"Worksheet '{ws_title}' validation result: {is_valid}.")
            return is_valid
        except Exception as ex:
            logger.error(f"Error validating worksheet '{ws_title}' data.", ex, exc_info=True)
            raise
    
    def format_campaign_worksheet(self):
        """ Apply formatting to the 'campaign' worksheet."""
        try:
            ws: Worksheet = self.get_worksheet('campaign')
            ws.format("A1:B1", {"textFormat": {"bold": True}})
            logger.info("Formatting applied to 'campaign' worksheet.")
        except Exception as ex:
            logger.error("Error formatting campaign worksheet.", ex, exc_info=True)
            raise
    
    def format_categories_worksheet(self):
        """ Apply formatting to the 'categories' worksheet."""
        try:
            ws: Worksheet = self.get_worksheet('categories')
            ws.format("A1:E1", {"textFormat": {"bold": True}})
            logger.info("Formatting applied to 'categories' worksheet.")
        except Exception as ex:
            logger.error("Error formatting categories worksheet.", ex, exc_info=True)
            raise
    
    def format_product_worksheet(self, ws_title: str):
        """ Apply formatting to a product worksheet.
        @param ws_title `str`: The title of the product worksheet to format.
        """
        try:
            ws: Worksheet = self.get_worksheet(ws_title)
            ws.format("A1:B1", {"textFormat": {"bold": True}})
            logger.info(f"Formatting applied to '{ws_title}' worksheet.")
        except Exception as ex:
            logger.error(f"Error formatting worksheet '{ws_title}'.", ex, exc_info=True)
            raise
