## \file /src/suppliers/aliexpress/campaign/gsheet (6).py
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
from typing import List
from gspread.worksheet import Worksheet
from src.goog.spreadsheet.spreadsheet import SpreadSheet
from src.suppliers.suppliers_list.aliexpress_com.campaign.ali_campaign_editor import AliCampaignEditor
from src.utils.jjson import j_dumps
from src.logger.logger import logger



class AliCampaignGoogleSheet(SpreadSheet, AliCampaignEditor):
    """ Class for managing Google Sheets within AliExpress campaigns.

    Inherits from `SpreadSheet` and `AliCampaignEditor` to manage Google Sheets,
    write category and product data, and format sheets.
    """
    ...
    spreadsheet_id = '1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0'
    spreadsheet: SpreadSheet
    worksheet: Worksheet

    def __init__(self, campaign_name: str = None, category_name: str = None, language: str = None, currency: str = None):
        """ Initialize AliCampaignGoogleSheet with specified Google Sheets spreadsheet ID and additional parameters.
        @param campaign_name `str`: The name of the campaign.
        @param category_name `str`: The name of the category.
        @param language `str`: The language for the campaign.
        @param currency `str`: The currency for the campaign.
        """
        # Initialize SpreadSheet with the spreadsheet ID
        SpreadSheet.__init__(self, spreadsheet_id=self.spreadsheet_id)
        

        self.driver.get_url(f'https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}')
        self.clear()
        campaign = self._set_gs_campaign(campaign_name=campaign_name,language=language,currency=currency)
        self.set_campaign_worksheet(campaign)
        self.set_categories_worksheet(campaign.category)

    def _set_gs_campaign(self,campaign_name: str = None, category_name: str = None, language: str = None, currency: str = None):
        """ Initialize AliCampaignEditor with the campaign name"""
        AliCampaignEditor.__init__(self, campaign_name=campaign_name, language=language, currency=currency)
        campaign = self.raw_campaign_data
        return campaign
        
    def clear(self):
        """ Clear contents.
        Delete product sheets and clear data on the categories and other specified sheets.
        """
        try:
            self.delete_all_worksheets()
            # ws_to_clear = ['category','categories','campaign']
            # for ws in self.spreadsheet.worksheets():
            #     self.get_worksheet(ws).clear()
                
        except Exception as ex:
            logger.error("Ошибка очистки",ex)



    def set_campaign_worksheet(self, campaign: SimpleNamespace | str, language: str = None, currency: str = None):
        """ Write campaign data to a Google Sheets worksheet.
        @param campaign `SimpleNamespace | str`: SimpleNamespace object with campaign data fields for writing.
        @param language `str`: Optional language parameter.
        @param currency `str`: Optional currency parameter.
        """
        if not isinstance(campaign, SimpleNamespace):
            campaign = self._set_gs_campaign(campaign_name=campaign, language=language, currency=currency)

        try:
            ws: Worksheet = self.get_worksheet('campaign')
            #ws.clear()  # Clear the 'campaign' worksheet

            if isinstance(campaign, SimpleNamespace):
                # Prepare data for vertical writing, skipping missing attributes
                vertical_data = []
                for field in [('Name', 'campaign_name'), 
                              ('Title', 'title'), 
                              ('Description', 'description'), 
                              ('Tags', 'tags'), 
                              ('Budget', 'budget'), 
                              ('Duration', 'duration')]:
                    header, attr = field
                    if hasattr(campaign, attr):
                        value = getattr(campaign, attr)
                        vertical_data.append([header, str(value)])  # Prepare for vertical writing

                # Write data vertically
                if vertical_data:
                    # Update the range with vertical data
                    ws.update('A1:B{}'.format(len(vertical_data)), vertical_data)

                logger.info("Campaign data written to 'campaign' worksheet vertically.")
            else:
                raise TypeError("Expected SimpleNamespace for campaign.")

        except Exception as ex:
            logger.error("Error writing campaign data to worksheet.", ex, exc_info=True)
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
                name=data[1][1],
                title=data[2][1],
                description=data[3][1],
                tags=data[4][1].split(', '),
                budget=float(data[5][1]),
                duration=data[6][1]
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
            ws: Worksheet = self.get_worksheet('category')  # Clear the 'category' worksheet
            
            if isinstance(category, SimpleNamespace):
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
            else:
                raise TypeError("Expected SimpleNamespace for category.")

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
        # ws.clear()  # Clear the 'categories' worksheet

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

                # Extract data from the SimpleNamespace attribute
                name = getattr(attr_value, 'name', '')
                title = getattr(attr_value, 'title', '')
                description = getattr(attr_value, 'description', '')
                tags = getattr(attr_value, 'tags', [])
                products_count = getattr(attr_value, 'products_count', '')

                # Prepare updates for the given SimpleNamespace object
                updates = [
                    {'range': f'A{start_row}', 'values': [[name]]},
                    {'range': f'B{start_row}', 'values': [[title]]},
                    {'range': f'C{start_row}', 'values': [[description]]},
                    {'range': f'D{start_row}', 'values': [[', '.join(tags)]]},
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


        
    def get_categories_worksheet(self) -> List[SimpleNamespace]:
        """ Read categories data from the 'categories' worksheet.
        @return `List[SimpleNamespace]`: List of SimpleNamespace objects with category data fields.
        """
        try:
            ws: Worksheet = self.get_worksheet('categories')
            if not ws:
                raise ValueError("Worksheet 'categories' not found.")
            
            data = ws.get_all_values()
            categories = [
                SimpleNamespace(
                    name=row[0],
                    title=row[1],
                    description=row[2],
                    tags=row[3].split(', '),
                    products_count=int(row[4])
                )
                for row in data[1:]  # Skip header row
            ]
            
            logger.info("Categories data read from 'categories' worksheet.")
            return categories

        except Exception as ex:
            logger.error("Error getting categories worksheet data.", ex, exc_info=True)
            raise

    def set_product_worksheet(self, product: SimpleNamespace | str):
        """ Write product data to a Google Sheets worksheet.
        @param product `SimpleNamespace`: SimpleNamespace object with product data fields for writing.
        """
        try:
            ws: Worksheet = self.get_worksheet('products').clear()  # Clear the 'products' worksheet
            
            if isinstance(product, SimpleNamespace):
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
            else:
                raise TypeError("Expected SimpleNamespace for product.")

        except Exception as ex:
            logger.error("Error setting product worksheet.", ex, exc_info=True)
            raise

    def get_product_worksheet(self) -> SimpleNamespace:
        """ Read product data from the 'products' worksheet.
        @return `SimpleNamespace`: SimpleNamespace object with product data fields.
        """
        try:
            ws: Worksheet = self.get_worksheet('products')
            if not ws:
                raise ValueError("Worksheet 'products' not found.")
            
            data = ws.get_all_values()
            product_data = SimpleNamespace(
                id=data[1][1],
                name=data[2][1],
                title=data[3][1],
                description=data[4][1],
                tags=data[5][1].split(', '),
                price=float(data[6][1])
            )
            
            logger.info("Product data read from 'products' worksheet.")
            return product_data

        except Exception as ex:
            logger.error("Error getting product worksheet data.", ex, exc_info=True)
            raise

    def set_products_worksheet(self, ns_list: List[SimpleNamespace] | SimpleNamespace):
        """ Write data from a list of SimpleNamespace objects to Google Sheets cells.
        @param ns_list `List[SimpleNamespace]`|`SimpleNamespace`: List of SimpleNamespace objects with data fields for writing.
        """
        ws: Worksheet = self.get_worksheet('products').clear()
        
        try:
            if isinstance(ns_list, list) and all(isinstance(value, SimpleNamespace) and 
                all(hasattr(value, attr) for attr in ['id', 'name', 'title', 'description', 'tags', 'price']) 
                for value in ns_list):
                
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
                logger.error("List does not contain required attributes or is not a list of SimpleNamespace.")
        
        except Exception as ex:
            logger.error("Error setting products worksheet.", ex, exc_info=True)
            raise



    def delete_all_worksheets(self):
        """ Delete all sheets from the Google Sheets spreadsheet except 'categories' and 'product_template'.
        """
        excluded_titles = {'categories', 'product_template', 'category', 'campaign'}
        try:
            worksheets = self.spreadsheet.worksheets()
            for sheet in worksheets:
                if sheet.title not in excluded_titles:
                    self.spreadsheet.del_worksheet_by_id(sheet.id)
                    logger.success(f"Worksheet '{sheet.title}' deleted.")
        except Exception as ex:
            logger.error("Error deleting all worksheets.", ex, exc_info=True)
            raise

if __name__ == "__main__":
    # Example usage
    campaign_editor = AliCampaignGoogleSheet(campaign_name="Summer Sale")
    # Your additional code here
