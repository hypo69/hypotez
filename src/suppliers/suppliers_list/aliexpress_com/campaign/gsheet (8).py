## \file /src/suppliers/aliexpress/campaign/gsheet (8).py
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

...

import time
from types import SimpleNamespace
from typing import List
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
    driver:Driver = Driver(Chrome)
    
    def __init__(self, campaign_name: str, language: str|dict = None, currency: str = None):
        """ Initialize AliCampaignGoogleSheet with specified Google Sheets spreadsheet ID and additional parameters.
        @param campaign_name `str`: The name of the campaign.
        @param category_name `str`: The name of the category.
        @param language `str`: The language for the campaign.
        @param currency `str`: The currency for the campaign.
        """
        # Initialize SpreadSheet with the spreadsheet ID
        SpreadSheet.__init__(self, spreadsheet_id = self.spreadsheet_id)
        self.editor =AliCampaignEditor(campaign_name=campaign_name,language=language,currency=currency)
        
        self.driver.get_url(f'https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}')
        self.clear()
        
        self.set_campaign_worksheet(self.editor.campaign)
        self.set_categories_worksheet(self.editor.campaign.category)

    # def _set_gs_campaign_category(self,campaign_name: str = None, category_name: str = None, language: str|dict = None, currency: str = None):
    #     """ Initialize AliCampaignEditor with the campaign name"""
    #     self.__init__(self, campaign_name=campaign_name, language=language, currency=currency)
    #     campaign = self.raw_campaign_data
    #     return campaign
        
    def clear(self):
        """ Clear contents.
        Delete product sheets and clear data on the categories and other specified sheets.
        """
        try:
            self.delete_products_worksheets()
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
        try:
            ws: Worksheet = self.get_worksheet('campaign')

            # Prepare data for vertical writing, ensuring all fields have values
            vertical_data = []
            for field in [
                    ('Name', 'name'), 
                    ('Title', 'title'), 
                    ('Language', 'language'), 
                    ('Currency', 'currency'), 
                    ('Description', 'description') 
                            ]:
                header, attr = field
                value = getattr(campaign, attr, '')  # Set value to '' if attribute is missing
                vertical_data.append([header, str(value)])  # Prepare for vertical writing

                # Write data vertically
                if vertical_data:
                    # Update the range with vertical data
                    ws.update('A1:B{}'.format(len(vertical_data)), vertical_data)

                logger.info(f"Campaign data {vertical_data} written to 'campaign' worksheet vertically.")
            else:
                ...
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
                ['Name', _.get('name','')],
                ['Title', _.get('title','')],
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
                _ = attr_value.__dict__
                # Extract data from the SimpleNamespace attribute
                name =  _.get('name','')
                title =  _.get('title')
                description =  _.get('description')
                tags =  ', '.join(map(str, _.get('tags', [])))
                products_count =  _.get('products_count','~')

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
 
    def get_categories_worksheet(self) -> List[List[str]]:
        """ Read data from columns A to E, starting from the second row, from the 'categories' worksheet.
        @return `List[List[str]]`: List of rows with data from columns A to E.
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

            ws.update('A2:Y2', [row_data])  # Update row data in a single row

            logger.info("Product data written to worksheet.")
        except Exception as ex:
            logger.error("Error updating product data in worksheet.", ex, exc_info=True)
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

    def set_products_worksheet(self, category_name:str):
        """ Write data from a list of SimpleNamespace objects to Google Sheets cells.
        @param ns_list `List[SimpleNamespace]`|`SimpleNamespace`: List of SimpleNamespace objects with data fields for writing.
        """
        if category_name:
            category_ns:SimpleNamespace = getattr(self.campaign.category,category_name)
            products_ns:SimpleNamespace = category_ns.products
        else:
            logger.warning(f"На ашел товары в {pprint(category_ns)}")
            return    
        ws: Worksheet = self.get_worksheet(category_name)
        
        try:
            updates:list=[]
            for index, value in enumerate(products_ns, start=2):
                _ = value.__dict__
                updates.append({'range': f'A{index}', 'values': [[str(_.get('product_id',''))]]})
                updates.append({'range': f'B{index}', 'values': [[str(_.get('product_title',''))]]})
                updates.append({'range': f'C{index}', 'values': [[str(_.get('title',''))]]})
                updates.append({'range': f'D{index}', 'values': [[str(_.get('local_image_path',''))]]})
                updates.append({'range': f'D{index}', 'values': [[str(_.get('product_video_url',''))]]})
                updates.append({'range': f'F{index}', 'values': [[str(_.get('original_price',''))]]})
                updates.append({'range': f'F{index}', 'values': [[str(_.get('app_sale_price',''))]]})
                updates.append({'range': f'F{index}', 'values': [[str(_.get('target_sale_price',''))]]})
                updates.append({'range': f'F{index}', 'values': [[str(_.get('target_sale_price',''))]]})
                
            ws.batch_update(updates)
            logger.info("Products data written to 'products' worksheet.")

        
        except Exception as ex:
            logger.error("Error setting products worksheet.", ex, exc_info=True)
            raise

    def delete_products_worksheets(self):
        """ Delete all sheets from the Google Sheets spreadsheet except 'categories' and 'product_template'.
        """
        excluded_titles = {'categories', 'product', 'category', 'campaign'}
        try:
            worksheets = self.spreadsheet.worksheets()
            for sheet in worksheets:
                if sheet.title not in excluded_titles:
                    self.spreadsheet.del_worksheet_by_id(sheet.id)
                    logger.success(f"Worksheet '{sheet.title}' deleted.")
        except Exception as ex:
            logger.error("Error deleting all worksheets.", ex, exc_info=True)
            raise
        
    def save_categories_from_worksheet(self, update:bool=False):
        """ Сохраняю данные, отредактированные в гугл таблице """

        edited_categories: list[dict] = self.get_categories_worksheet()
        _categories_ns:SimpleNamespace = SimpleNamespace()
        for _cat in edited_categories:
            _cat_ns: SimpleNamespace = SimpleNamespace(**{
                'name':_cat[0],
                'title':_cat[1],
                'description':_cat[2],
                'tags':_cat[3].split(","),
                'products_count':_cat[4],
            }
            )
            setattr(_categories_ns,_cat_ns.name,_cat_ns)
        ...
        self.campaign.category = _categories_ns
        if update: self.update_campaign()
        
    def save_campaign_from_worksheet(self):
        """ Сохраняю реклманую каманию """
        self.save_categories_from_worksheet(False)
        data = self.get_campaign_worksheet()
        data.category = self.campaign.category
        self.campaign = data
        self.update_campaign()
        ...
        
        
    
