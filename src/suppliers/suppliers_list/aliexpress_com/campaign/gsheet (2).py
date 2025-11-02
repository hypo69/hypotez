## \file /src/suppliers/aliexpress/campaign/gsheet (2).py
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
...

...
from src.llm.openai import translate
from types import SimpleNamespace
from typing import Optional, List, Dict
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
from src.webdriver.selenium.driver import Driver, Chrome
from src.utils.printer import pprint
from src.logger.logger import logger

class AliSheet(SpreadSheet):
    """ Класс для работы с Google Sheets в рамках кампаний AliExpress.
    
    Наследует класс SpreadSheet и предоставляет дополнительные методы для управления листами Google Sheets,
    записи данных о категориях и товарах, и форматирования листов.
    """

    def __init__(self, spreadsheet_id: str):
        """ Инициализация AliSheet с указанным идентификатором таблицы Google Sheets.
        @param spreadsheet_id Идентификатор таблицы Google Sheets.
        """
        super().__init__(spreadsheet_id)
        logger.info(f"Initialized AliSheet with spreadsheet ID: {spreadsheet_id}") 
        d = Driver(Chrome)
        d.get_url(r'https://docs.google.com/spreadsheets/d/1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0/edit?gid=11884323#gid=11884323')
        

    def delete_all_worksheets(self):
        """ Удаление всех листов из таблицы Google Sheets, кроме 'Sheet1'.
        Удаляет все листы, кроме листа по умолчанию с именем 'Sheet1'.
        """
        try:
            worksheets = self.spreadsheet.worksheets()
            #worksheets = self.get_all_worksheets()  # Get all worksheets
            for sheet in worksheets:
                if sheet.title != 'categories':
                    self.spreadsheet.del_worksheet_by_id(sheet.id)
                    logger.info(f"Worksheet '{sheet.title}' deleted.")
        except Exception as ex:
            logger.error("Error deleting all worksheets.", ex, exc_info=True)
            raise

 

    def set_categories_worksheet(self, ns_list: list[SimpleNamespace]):
        """ Запись данных из списка объектов SimpleNamespace в ячейки Google Sheets.
        @param ns_list Список объектов SimpleNamespace с полями данных для записи.
        """
        ws: Worksheet = self.get_worksheet('categories')
        
        ws.clear()
        try:
            if all(all(hasattr(value, attr) for attr in ['name', 'title', 'description', 'tags', 'products_count']) for value in ns_list):
                headers = ['name', 'title', 'description', 'tags', 'products_count']
                ws.update('A1:E1', [headers])

                for index, value in enumerate(ns_list, start=2):
                    row_data = [
                        value.name,
                        value.title,
                        value.description,
                        ', '.join(value.tags),
                        value.products_count,
                    ]
                    ws.update(f'A{index}:E{index}', [row_data])
                    
                self._format_categories_worksheet(ws)
                
                logger.info("Fields updated from SimpleNamespace list.")
            else:
                logger.warning("The list does not contain SimpleNamespace objects with all required attributes.")
                
            self.delete_all_worksheets()  # <- удаляю лишнее
            
        except Exception as ex:
            logger.error("Error updating fields from SimpleNamespace list.", ex, exc_info=True)
            raise

    def get_categories(self):
        """ Получение данных из таблицы Google Sheets.
        @return Данные из таблицы в виде списка словарей.
        """
        ws = self.get_worksheet('categories') 
        data = ws.get_all_records()
        logger.info("Categories data retrieved from worksheet.")
        return data

    def set_category_products(self, category_name: str, products: dict):
        """ Запись данных о товарах в новую таблицу Google Sheets.
        @param category_name Название категории.
        @param products Словарь с данными о товарах.
        """
        ws = self.get_worksheet(category_name)
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

            row_data = []
            for product in products:
                _ = product.__dict__
                row_data.append([
                    str(_.get('product_id')),
                    str(_.get('app_sale_price')),
                    _.get('original_price'),
                    _.get('sale_price'),
                    _.get('discount'),
                    _.get('product_main_image_url'),
                    _.get('local_image_path'),
                    ', '.join(_.get('product_small_image_urls', [])),
                    _.get('product_video_url'),
                    _.get('local_video_path'),
                    _.get('first_level_category_id'),
                    _.get('first_level_category_name'),
                    _.get('second_level_category_id'),
                    _.get('second_level_category_name'),
                    _.get('target_sale_price'),
                    _.get('target_sale_price_currency'),
                    _.get('target_app_sale_price_currency'),
                    _.get('target_original_price_currency'),
                    _.get('original_price_currency'),
                    _.get('product_title'),
                    _.get('evaluate_rate'),
                    _.get('promotion_link'),
                    _.get('shop_url'),
                    _.get('shop_id'),
                    ', '.join(_.get('tags', []))
                ])
            
            for index, row in enumerate(row_data, start=2):
                ws.update(f'A{index}:Y{index}', [row])
                logger.info(f"Products {str(_.get('product_id'))} updated .")

            self._format_category_products_worksheet(ws)

            logger.info("Products updated in worksheet.")
        except Exception as ex:
            logger.error("Error updating products in worksheet.", ex, exc_info=True)
            raise

    def _format_categories_worksheet(self, ws: Worksheet):
        """ Форматирование листа 'categories'.
        @param ws Лист Google Sheets для форматирования.
        """
        try:
            # Установка ширины столбцов
            set_column_width(ws, 'A:A', 150)  # Ширина столбца A
            set_column_width(ws, 'B:B', 200)  # Ширина столбца B
            set_column_width(ws, 'C:C', 300)  # Ширина столбца C
            set_column_width(ws, 'D:D', 200)  # Ширина столбца D
            set_column_width(ws, 'E:E', 150)  # Ширина столбца E
            
            # Установка высоты строк
            set_row_height(ws, '1:1', 40)  # Высота заголовков

            # Форматирование заголовков
            header_format = cellFormat(
                textFormat=textFormat(bold=True, fontSize=12),
                horizontalAlignment='CENTER',
                verticalAlignment='MIDDLE',  # Добавлено вертикальное выравнивание
                backgroundColor=Color(0.8, 0.8, 0.8)  # Используется Color для задания цвета
            )
            format_cell_range(ws, 'A1:E1', header_format)

            logger.info("Categories worksheet formatted.")
        except Exception as ex:
            logger.error("Error formatting categories worksheet.", ex, exc_info=True)
            raise

    def _format_category_products_worksheet(self, ws: Worksheet):
        """ Форматирование листа с товарами категории.
        @param ws Лист Google Sheets для форматирования.
        """
        try:
            # Установка ширины столбцов
            set_column_width(ws, 'A:A', 250)  # Ширина столбца A
            set_column_width(ws, 'B:B', 220)  # Ширина столбца B
            set_column_width(ws, 'C:C', 220)  # Ширина столбца C
            set_column_width(ws, 'D:D', 220)  # Ширина столбца D
            set_column_width(ws, 'E:E', 200)  # Ширина столбца E
            set_column_width(ws, 'F:F', 200)  # Ширина столбца F
            set_column_width(ws, 'G:G', 200)  # Ширина столбца G
            set_column_width(ws, 'H:H', 200)  # Ширина столбца H
            set_column_width(ws, 'I:I', 200)  # Ширина столбца I
            set_column_width(ws, 'J:J', 200)  # Ширина столбца J
            set_column_width(ws, 'K:K', 200)  # Ширина столбца K
            set_column_width(ws, 'L:L', 200)  # Ширина столбца L
            set_column_width(ws, 'M:M', 200)  # Ширина столбца M
            set_column_width(ws, 'N:N', 200)  # Ширина столбца N
            set_column_width(ws, 'O:O', 200)  # Ширина столбца O
            set_column_width(ws, 'P:P', 200)  # Ширина столбца P
            set_column_width(ws, 'Q:Q', 200)  # Ширина столбца Q
            set_column_width(ws, 'R:R', 200)  # Ширина столбца R
            set_column_width(ws, 'S:S', 200)  # Ширина столбца S
            set_column_width(ws, 'T:T', 200)  # Ширина столбца T
            set_column_width(ws, 'U:U', 200)  # Ширина столбца U
            set_column_width(ws, 'V:V', 200)  # Ширина столбца V
            set_column_width(ws, 'W:W', 200)  # Ширина столбца W
            set_column_width(ws, 'X:X', 200)  # Ширина столбца X
            set_column_width(ws, 'Y:Y', 200)  # Ширина столбца Y

            # Установка высоты строк
            set_row_height(ws, '1:1', 40)  # Высота заголовков

            # Форматирование заголовков
            header_format = cellFormat(
                textFormat=textFormat(bold=True, fontSize=12),
                horizontalAlignment='CENTER',
                verticalAlignment='TOP',  # Добавлено вертикальное выравнивание
                backgroundColor=Color(0.8, 0.8, 0.8)  # Используется Color для задания цвета
            )
            format_cell_range(ws, 'A1:Y1', header_format)

            logger.info("Category products worksheet formatted.")
        except Exception as ex:
            logger.error("Error formatting category products worksheet.", ex, exc_info=True)
            raise
