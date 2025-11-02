## \file /src/suppliers/aliexpress/campaign/gsheet (9).py
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


""" AliExpress Campaign Editor via Google Sheets """


import time
from types import SimpleNamespace
from src.webdriver.selenium.driver import Driver, Chrome, Firefox, Edge
from gspread.worksheet import Worksheet
from src.goog.spreadsheet.spreadsheet import SpreadSheet
from src.suppliers.suppliers_list.aliexpress_com.campaign.ali_campaign_editor import AliCampaignEditor
from src.utils.jjson import j_dumps
from src.utils.printer import pprint
from src.logger.logger import logger

class AliCampaignGoogleSheet(SpreadSheet, AliCampaignEditor):
    """ Class for managing Google Sheets within AliExpress campaigns.

    Inherits from `SpreadSheet` and `AliCampaignEditor` to manage Google Sheets,
    write category and product data, and format sheets.
    """
    spreadsheet_id = '1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0'
    spreadsheet: SpreadSheet
    worksheet: Worksheet
    driver: Driver = Driver(Chrome)
    
    def __init__(self, campaign_name: str, language: str | dict = None, currency: str = None):
        """ Initialize AliCampaignGoogleSheet with specified Google Sheets spreadsheet ID and additional parameters.
        @param campaign_name `str`: The name of the campaign.
        @param category_name `str`: The name of the category.   
        @param language `str`: The language for the campaign.
        @param currency `str`: The currency for the campaign.
        """
        # Initialize SpreadSheet with the spreadsheet ID
        SpreadSheet.__init__(self, spreadsheet_id=self.spreadsheet_id)
        self.editor = AliCampaignEditor(campaign_name=campaign_name, language=language, currency=currency)
        
        self.driver.get_url(f'https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}')
        self.clear()
        
        self.set_campaign_worksheet(self.editor.campaign)
        self.set_categories_worksheet(self.editor.campaign.category)
        
    def clear(self):
        """ Clear contents.
        Delete product sheets and clear data on the categories and other specified sheets.
        """
        try:
            self.delete_products_worksheets()
        except Exception as ex:
            logger.error("Ошибка очистки", ex)

    def set_campaign_worksheet(self, campaign: SimpleNamespace | str, language: str = None, currency: str = None):
        """ Write campaign data to a Google Sheets worksheet.
        @param campaign `SimpleNamespace | str`: SimpleNamespace object with campaign data fields for writing.
        @param language `str`: Optional language parameter.
        @param currency `str`: Optional currency parameter.
        """
        try:
            ws: Worksheet = self.get_worksheet('campaign').clear()  # Clear the 'campaign' worksheet
            
            # Prepare data for vertical writing
            vertical_data = [
                ('Name', campaign.name),
                ('Title', campaign.title),
                ('Language', campaign.language),
                ('Description', campaign.description),
                ('Currency', campaign.currency)
            ]
            
            # Write data vertically
            for row_index, (header, value) in enumerate(vertical_data, start=1):
                ws.update(f'A{row_index}', header)  # Column A: Field names
                ws.update(f'B{row_index}', str(value))  # Column B: Field values as strings
                
            logger.info("Campaign data written to 'campaign' worksheet vertically.")
            
        except Exception as ex:
            logger.error("Error setting campaign worksheet.", ex, exc_info=True)
            raise

    def get_campaign_worksheet(self) -> SimpleNamespace:
        """ Read campaign data from the 'campaign' worksheet.
        @return `SimpleNamespace`: SimpleNamespace object with campaign data fields.
        """
        try:
            ws: Worksheet = self.get_worksheet('campaign')
            if not ws:
                raise ValueError("Worksheet 'campaign' not found.")
            
            data = ws.get_all_values()
            campaign_data = SimpleNamespace(
                name=data[0][1],
                title=data[1][1],
                language=data[2][1],
                currency=data[3][1],
                description=data[4][1]
            )
            
            logger.info("Campaign data read from 'campaign' worksheet.")
            return campaign_data

        except Exception as ex:
            logger.error("Error getting campaign worksheet data.", ex, exc_info=True)
            raise

    def set_category_worksheet(self, category: SimpleNamespace | str):
        """ Write data from a SimpleNamespace object to Google Sheets cells vertically.
        @param category `SimpleNamespace`: SimpleNamespace object with data fields for writing.
        """
        category = category if isinstance(category, SimpleNamespace) else self.get_campaign_category(category)
        try:
            ws: Worksheet = self.get_worksheet('category')

            # Prepare data for vertical writing
            _ = category.__dict__
            vertical_data = [
                ['Name', _.get('name', '')],
                ['Title', _.get('title', '')],
                ['Description', _.get('description')],
                ['Tags', ', '.join(map(str, _.get('tags', [])))],
                ['Products Count', _.get('products_count', '~')]
            ]
            
            # Write data vertically
            ws.update('A1:B{}'.format(len(vertical_data)), vertical_data)

        except Exception as ex:
            logger.error("Error setting category worksheet.", ex, exc_info=True)
            raise

    def get_category_worksheet(self) -> SimpleNamespace:
        """ Read category data from the 'category' worksheet.
        @return `SimpleNamespace`: SimpleNamespace object with category data fields.
        """
        try:
            ws: Worksheet = self.get_worksheet('category')
            if not ws:
                raise ValueError("Worksheet 'category' not found.")
            
            data = ws.get_all_values()
            category_data = SimpleNamespace(
                name=data[1][1],
                title=data[2][1],
                description=data[3][1],
                tags=data[4][1].split(', '),
                products_count=int(data[5][1])
            )
            
            logger.info("Category data read from 'category' worksheet.")
            return category_data

        except Exception as ex:
            logger.error("Error getting category worksheet data.", ex, exc_info=True)
            raise
        
    def set_categories_worksheet(self, categories: SimpleNamespace):
        """ Write data from a SimpleNamespace object to Google Sheets cells.
        @param categories `SimpleNamespace`: SimpleNamespace object with data fields for writing.
        """
        ws: Worksheet = self.get_worksheet('categories')

        try:
            # Initialize the starting row
            start_row = 2

            # Iterate over all attributes of the categories object
            for attr_name in dir(categories):
                attr_value = getattr(categories, attr_name, None)
            
                # Skip non-SimpleNamespace attributes or attributes with no data
                if not isinstance(attr_value, SimpleNamespace) or not any(
                    hasattr(attr_value, field) for field in ['name', 'title', 'description', 'tags', 'products_count']
                ):
                    continue
                _ = attr_value.__dict__
                # Extract data from the SimpleNamespace attribute
                name = _.get('name', '')
                title = _.get('title')
                description = _.get('description')
                tags = ', '.join(map(str, _.get('tags', [])))
                products_count = _.get('products_count', '~')

                # Prepare updates for the given SimpleNamespace object
                updates = [
                    {'range': f'A{start_row}', 'values': [[name]]},
                    {'range': f'B{start_row}', 'values': [[title]]},
                    {'range': f'C{start_row}', 'values': [[description]]},
                    {'range': f'D{start_row}', 'values': [[tags]]},
                    {'range': f'E{start_row}', 'values': [[products_count]]},
                ]

                # Perform batch update
                if updates:
                    ws.batch_update(updates)
                    logger.info(f"Category data written to 'categories' worksheet for {attr_name}.")
            
                # Move to the next row
                start_row += 1

        except Exception as ex:
            logger.error("Error setting categories worksheet.", ex, exc_info=True)
            raise
 
    def get_categories_worksheet(self) -> list[list[str]]:
        """ Read data from columns A to E, starting from the second row, from the 'categories' worksheet.
        @return `list[list[str]]`: List of rows with data from columns A to E.
        """
        try:
            ws: Worksheet = self.get_worksheet('categories')
            if not ws:
                raise ValueError("Worksheet 'categories' not found.")
        
            # Read all values from the worksheet
            data = ws.get_all_values()
        
            # Extract data from columns A to E, starting from the second row
            data = [row[:5] for row in data[1:] if len(row) >= 5]  
        
            logger.info("Category data read from 'categories' worksheet.")
            return data

        except Exception as ex:
            logger.error("Error getting category data from worksheet.", ex, exc_info=True)
            raise

    def set_product_worksheet(self, product: SimpleNamespace | str, category_name: str):
        """ Write product data to a new Google Sheets spreadsheet.
        @param category_name Category name.
        @param product SimpleNamespace object with product data fields for writing.
        """
        time.sleep(10)
        ws = self.copy_worksheet('product_template', category_name)  # Create a new worksheet by copying from 'product_template'
        
        product = product if isinstance(product, SimpleNamespace) else self.get_product(product)
        try:
            ws.update('A1', 'Product Details')  # Write 'Product Details' to cell A1
            
            # Prepare data for vertical writing
            _ = product.__dict__
            vertical_data = [
                ('Name', _.get('name')),
                ('Title', _.get('title')),
                ('Price', _.get('price')),
                ('Images', _.get('images', '~')),
                ('Video', _.get('video', '~')),
                ('Tags', ', '.join(map(str, _.get('tags', [])))),
                ('Stock', _.get('stock', '~')),
                ('Description', _.get('description'))
            ]
            
            # Write data vertically
            for row_index, (header, value) in enumerate(vertical_data, start=1):
                ws.update(f'A{row_index}', header)  # Column A: Field names
                ws.update(f'B{row_index}', str(value))  # Column B: Field values as strings
                
            logger.info("Product data written to new worksheet.")
            
        except Exception as ex:
            logger.error("Error setting product worksheet.", ex, exc_info=True)
            raise

    def get_product_worksheet(self) -> SimpleNamespace:
        """ Read product data from the specified worksheet.
        @param worksheet_name `str`: The name of the worksheet to read data from.
        @return `SimpleNamespace`: SimpleNamespace object with product data fields.
        """
        try:
            ws: Worksheet = self.get_worksheet(self.name)
            if not ws:
                raise ValueError("Worksheet 'product' not found.")
            
            data = ws.get_all_values()
            product_data = SimpleNamespace(
                name=data[0][1],
                title=data[1][1],
                price=data[2][1],
                images=data[3][1].split(', '),
                video=data[4][1].split(', '),
                tags=data[5][1].split(', '),
                stock=int(data[6][1]),
                description=data[7][1]
            )
            
            logger.info("Product data read from 'product' worksheet.")
            return product_data

        except Exception as ex:
            logger.error("Error getting product worksheet data.", ex, exc_info=True)
            raise

    def delete_products_worksheets(self):
        """ Delete all product worksheets."""
        try:
            all_worksheets = self.get_worksheets()
            
            # Filter worksheets starting with 'product_'
            product_worksheets = [ws for ws in all_worksheets if ws.title.startswith('product_')]
            
            # Delete each product worksheet
            for ws in product_worksheets:
                self.spreadsheet.del_worksheet(ws)
            
            logger.info("All product worksheets deleted.")
        except Exception as ex:
            logger.error("Error deleting product worksheets.", ex, exc_info=True)
            raise
