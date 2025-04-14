### **Анализ кода модуля `gsheets_check_this_code.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код структурирован в классы и функции, что облегчает понимание и поддержку.
    - Используется логгирование для отслеживания операций и ошибок.
    - Присутствуют docstring для большинства функций и классов.
- **Минусы**:
    - Отсутствуют аннотации типов для переменных класса и параметров некоторых функций.
    - Смешанный стиль кавычек (использованы как двойные, так и одинарные).
    - Docstring написаны на английском языке.
    - Не все переменные в коде соответствуют стилю snake_case.
    - Не используется `j_loads` или `j_loads_ns` для чтения JSON или конфигурационных файлов.
    - Используются сокращения в именах переменных (например, `ws`).
    - Не все исключения обрабатываются с использованием `logger.error(..., ex, exc_info=True)`.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех переменных класса, параметров функций и возвращаемых значений, где это необходимо.
2.  **Использовать одинарные кавычки**:
    - Заменить все двойные кавычки на одинарные.
3.  **Перевести docstring на русский язык**:
    - Перевести все docstring на русский язык, чтобы соответствовать требованиям.
4.  **Использовать snake_case**:
    - Привести имена переменных к стилю snake\_case.
5.  **Использовать `j_loads` или `j_loads_ns`**:
    - Если в коде есть чтение JSON или конфигурационных файлов, заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.
6.  **Полные имена переменных**:
    - Избегать сокращений в именах переменных, чтобы код был более читаемым (например, `worksheet` вместо `ws`).
7.  **Обработка исключений**:
    - Убедиться, что все исключения обрабатываются с использованием `logger.error(..., ex, exc_info=True)`.
8.  **Документация модуля**:\
    - Добавить описание модуля в начале файла.

**Оптимизированный код:**

```python
                ## \file /src/suppliers/aliexpress/campaign/gsheets_check_this_code.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с Google Sheets в рамках кампаний AliExpress
==============================================================

Модуль содержит класс :class:`AliCampaignGoogleSheet`, который используется для управления данными
в Google Sheets, связанными с рекламными кампаниями AliExpress. Он позволяет записывать данные
о категориях, продуктах и форматировать листы для удобства работы.

Пример использования
----------------------

>>> campaign_google_sheet = AliCampaignGoogleSheet(campaign_name='test_campaign', language='ru', currency='USD')
>>> campaign_google_sheet.set_categories_worksheet(campaign_google_sheet.editor.campaign.category)
"""

import time
from types import SimpleNamespace
from typing import Optional, List, Dict
from pathlib import Path

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
from src.webdriver.driver import Driver, Chrome, Firefox, Edge
from src.suppliers.aliexpress.campaign.ali_campaign_editor import AliCampaignEditor
from src.utils.jjson import j_dumps
from src.utils.printer import pprint
from src.logger.logger import logger


from src.ai.openai import translate
from types import SimpleNamespace

class AliCampaignGoogleSheet(SpreadSheet):
    """
    Класс для работы с Google Sheets в рамках кампаний AliExpress.

    Наследует класс SpreadSheet и предоставляет дополнительные методы для управления листами Google Sheets,
    записи данных о категориях и продуктах, и форматирования листов.
    """

    spreadsheet_id: str = '1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0'
    spreadsheet: SpreadSheet
    worksheet: Worksheet
    driver: Driver = Driver(Chrome)

    def __init__(self, campaign_name: str, language: Optional[str | dict] = None, currency: Optional[str] = None) -> None:
        """
        Инициализация AliCampaignGoogleSheet с указанным ID таблицы Google Sheets и дополнительными параметрами.

        Args:
            campaign_name (str): Название кампании.
            language (Optional[str | dict], optional): Язык кампании. По умолчанию None.
            currency (Optional[str], optional): Валюта кампании. По умолчанию None.
        """
        # Инициализация SpreadSheet с ID таблицы
        super().__init__(spreadsheet_id=self.spreadsheet_id)
        self.editor: AliCampaignEditor = AliCampaignEditor(campaign_name=campaign_name, language=language, currency=currency)
        self.clear()
        self.set_campaign_worksheet(self.editor.campaign)
        self.set_categories_worksheet(self.editor.campaign.category)
        self.driver.get_url(f'https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}')

    def clear(self) -> None:
        """
        Очистка содержимого.

        Удаляет листы продуктов и очищает данные на листах категорий и других указанных листах.
        """
        try:
            self.delete_products_worksheets()
        except Exception as ex:
            logger.error('Ошибка очистки', ex, exc_info=True) # Обработка исключения с логированием

    def delete_products_worksheets(self) -> None:
        """
        Удаляет все листы из таблицы Google Sheets, кроме 'categories', 'product' , 'category', 'campaign'.
        """
        excluded_titles: set[str] = {'categories', 'product', 'category', 'campaign'}
        try:
            worksheets: list[Worksheet] = self.spreadsheet.worksheets()
            for sheet in worksheets:
                if sheet.title not in excluded_titles:
                    self.spreadsheet.del_worksheet_by_id(sheet.id)
                    logger.success(f'Worksheet \'{sheet.title}\' deleted.')
        except Exception as ex:
            logger.error('Error deleting all worksheets.', ex, exc_info=True) # Обработка исключения с логированием
            raise

    def set_campaign_worksheet(self, campaign: SimpleNamespace) -> None:
        """
        Записывает данные кампании на лист Google Sheets.

        Args:
            campaign (SimpleNamespace | str): Объект SimpleNamespace с данными кампании для записи.
        """
        try:
            worksheet: Worksheet = self.get_worksheet('campaign')  # Получаем лист 'campaign'
        
            # Подготовка данных для вертикальной записи
            updates: list[dict] = []
            vertical_data: list[tuple[str, str, str]] = [
                ('A1', 'Campaign Name', campaign.name),
                ('A2', 'Campaign Title', campaign.title),
                ('A3', 'Campaign Language', campaign.language),
                ('A4', 'Campaign Currency', campaign.currency),
                ('A5', 'Campaign Description', campaign.description),
            ]
        
            # Добавляем операции обновления в список batch_update
            for cell, header, value in vertical_data:
                updates.append({'range': cell, 'values': [[header]]})
                updates.append({'range': f'B{cell[1]}', 'values': [[str(value)]]})
        
            # Выполняем batch update
            if updates:
                worksheet.batch_update(updates)
        
            logger.info('Campaign data written to \'campaign\' worksheet vertically.')
        
        except Exception as ex:
            logger.error('Error setting campaign worksheet.', ex, exc_info=True) # Обработка исключения с логированием
            raise

    def set_products_worksheet(self, category_name: str) -> None:
        """
        Записывает данные из списка объектов SimpleNamespace в ячейки Google Sheets.
        
        Args:
            category_name (str): Название категории для получения продуктов.
        """
        if category_name:
            category: SimpleNamespace = getattr(self.editor.campaign.category, category_name)
            products: list[SimpleNamespace] = category.products
        else:
            logger.warning('No products found for category.')
            return
    
        worksheet: Worksheet = self.copy_worksheet('product', category_name)
    
        try:
            # headers = [
            #     'product_id', 'app_sale_price', 'original_price', 'sale_price', 'discount',
            #     'product_main_image_url', 'local_image_path', 'product_small_image_urls',
            #     'product_video_url', 'local_video_path', 'first_level_category_id',
            #     'first_level_category_name', 'second_level_category_id', 'second_level_category_name',
            #     'target_sale_price', 'target_sale_price_currency', 'target_app_sale_price_currency',
            #     'target_original_price_currency', 'original_price_currency', 'product_title',
            #     'evaluate_rate', 'promotion_link', 'shop_url', 'shop_id', 'tags'
            # ]
            # updates = [{'range': 'A1:Y1', 'values': [headers]}]  # Add headers to the worksheet
    
            row_data: list[list[str]] = []
            for product in products:
                product_data: dict = product.__dict__
                row_data.append([
                    str(product_data.get('product_id')),
                    product_data.get('product_title'),
                    product_data.get('promotion_link'),
                    str(product_data.get('app_sale_price')),
                    product_data.get('original_price'),
                    product_data.get('sale_price'),
                    product_data.get('discount'),
                    product_data.get('product_main_image_url'),
                    product_data.get('local_image_path'),
                    ', '.join(product_data.get('product_small_image_urls', [])),
                    product_data.get('product_video_url'),
                    product_data.get('local_video_path'),
                    product_data.get('first_level_category_id'),
                    product_data.get('first_level_category_name'),
                    product_data.get('second_level_category_id'),
                    product_data.get('second_level_category_name'),
                    product_data.get('target_sale_price'),
                    product_data.get('target_sale_price_currency'),
                    product_data.get('target_app_sale_price_currency'),
                    product_data.get('target_original_price_currency'),
                    product_data.get('original_price_currency'),
                    product_data.get('evaluate_rate'),
                    product_data.get('shop_url'),
                    product_data.get('shop_id'),
                    ', '.join(product_data.get('tags', []))
                ])
        
            for index, row in enumerate(row_data, start=2):
                worksheet.update(f'A{index}:Y{index}', [row])
                logger.info(f'Products {str(product_data.get("product_id"))} updated.')
    
            self._format_category_products_worksheet(worksheet)
    
            logger.info('Products updated in worksheet.')
    
        except Exception as ex:
            logger.error('Error setting products worksheet.', ex, exc_info=True) # Обработка исключения с логированием
            raise

    def set_categories_worksheet(self, categories: SimpleNamespace) -> None:
        """
        Запись данных из объекта SimpleNamespace с категориями в ячейки Google Sheets.

        Args:
            categories (SimpleNamespace): Объект, где ключи — это категории с данными для записи.
        """
        worksheet: Worksheet = self.get_worksheet('categories')
        worksheet.clear()  # Очистка рабочей таблицы перед записью данных
    
        try:
            # Получение всех ключей (категорий) и соответствующих значений
            category_data: dict = categories.__dict__
        
            # Проверка, что все объекты категории имеют необходимые атрибуты
            required_attrs: list[str] = ['name', 'title', 'description', 'tags', 'products_count']
        
            if all(all(hasattr(category, attr) for attr in required_attrs) for category in category_data.values()):
                # Заголовки для таблицы
                headers: list[str] = ['Name', 'Title', 'Description', 'Tags', 'Products Count']
                worksheet.update('A1:E1', [headers])
            
                # Подготовка данных для записи
                rows: list[list[str | int]] = []
                for category in category_data.values():
                    row_data: list[str | int] = [
                        category.name,
                        category.title,
                        category.description,
                        ', '.join(category.tags),
                        category.products_count,
                    ]
                    rows.append(row_data)
            
                # Обновляем строки данных
                worksheet.update(f'A2:E{1 + len(rows)}', rows)
            
                # Форматируем таблицу
                self._format_categories_worksheet(worksheet)
            
                logger.info('Category fields updated from SimpleNamespace object.')
            else:
                logger.warning('One or more category objects do not contain all required attributes.')
    
        except Exception as ex:
            logger.error('Error updating fields from SimpleNamespace object.', ex, exc_info=True) # Обработка исключения с логированием
            raise


    def get_categories(self) -> list[dict]:
        """
        Получение данных из таблицы Google Sheets.

        Returns:
            list[dict]: Данные из таблицы в виде списка словарей.
        """
        worksheet: Worksheet = self.get_worksheet('categories')
        data: list[dict] = worksheet.get_all_records()
        logger.info('Categories data retrieved from worksheet.')
        return data

    def set_category_products(self, category_name: str, products: dict) -> None:
        """
        Запись данных о продуктах в новую таблицу Google Sheets.

        Args:
            category_name (str): Название категории.
            products (dict): Словарь с данными о продуктах.
        """
        if category_name:
            category_ns: SimpleNamespace = getattr(self.editor.campaign.category, category_name)
            products_ns: list[SimpleNamespace] = category_ns.products
        else:
            logger.warning('No products found for category.')
            return
    
        worksheet: Worksheet = self.copy_worksheet('product', category_name)
        try:
            headers: list[str] = [
                'product_id', 'app_sale_price', 'original_price', 'sale_price', 'discount',
                'product_main_image_url', 'local_image_path', 'product_small_image_urls',
                'product_video_url', 'local_video_path', 'first_level_category_id',
                'first_level_category_name', 'second_level_category_id', 'second_level_category_name',
                'target_sale_price', 'target_sale_price_currency', 'target_app_sale_price_currency',
                'target_original_price_currency', 'original_price_currency', 'product_title',
                'evaluate_rate', 'promotion_link', 'shop_url', 'shop_id', 'tags'
            ]
            updates: list[dict] = [{'range': 'A1:Y1', 'values': [headers]}]  # Add headers to the worksheet
    
            row_data: list[list[str]] = []
            for product in products:
                product_data: dict = product.__dict__
                row_data.append([
                    str(product_data.get('product_id')),
                    str(product_data.get('app_sale_price')),
                    product_data.get('original_price'),
                    product_data.get('sale_price'),
                    product_data.get('discount'),
                    product_data.get('product_main_image_url'),
                    product_data.get('local_image_path'),
                    ', '.join(product_data.get('product_small_image_urls', [])),
                    product_data.get('product_video_url'),
                    product_data.get('local_video_path'),
                    product_data.get('first_level_category_id'),
                    product_data.get('first_level_category_name'),
                    product_data.get('second_level_category_id'),
                    product_data.get('second_level_category_name'),
                    product_data.get('target_sale_price'),
                    product_data.get('target_sale_price_currency'),
                    product_data.get('target_app_sale_price_currency'),
                    product_data.get('target_original_price_currency'),
                    product_data.get('original_price_currency'),
                    product_data.get('product_title'),
                    product_data.get('evaluate_rate'),
                    product_data.get('promotion_link'),
                    product_data.get('shop_url'),
                    product_data.get('shop_id'),
                    ', '.join(product_data.get('tags', []))
                ])
        
            for index, row in enumerate(row_data, start=2):
                worksheet.update(f'A{index}:Y{index}', [row])
                logger.info(f'Products {str(product_data.get("product_id"))} updated.')
    
            self._format_category_products_worksheet(worksheet)
    
            logger.info('Products updated in worksheet.')
        except Exception as ex:
            logger.error('Error updating products in worksheet.', ex, exc_info=True) # Обработка исключения с логированием
            raise

    def _format_categories_worksheet(self, worksheet: Worksheet) -> None:
        """
        Форматирование листа 'categories'.

        Args:
            worksheet (Worksheet): Лист Google Sheets для форматирования.
        """
        try:
            # Установка ширины столбцов
            set_column_width(worksheet, 'A:A', 150)  # Ширина столбца A
            set_column_width(worksheet, 'B:B', 200)  # Ширина столбца B
            set_column_width(worksheet, 'C:C', 300)  # Ширина столбца C
            set_column_width(worksheet, 'D:D', 200)  # Ширина столбца D
            set_column_width(worksheet, 'E:E', 150)  # Ширина столбца E
        
            # Установка высоты строк
            set_row_height(worksheet, '1:1', 40)  # Высота заголовков

            # Форматирование заголовков
            header_format: cellFormat = cellFormat(
                textFormat=textFormat(bold=True, fontSize=12),
                horizontalAlignment='CENTER',
                verticalAlignment='MIDDLE',  # Добавлено вертикальное выравнивание
                backgroundColor=Color(0.8, 0.8, 0.8)  # Используем Color для задания цвета
            )
            format_cell_range(worksheet, 'A1:E1', header_format)

            logger.info('Categories worksheet formatted.')
        except Exception as ex:
            logger.error('Error formatting categories worksheet.', ex, exc_info=True) # Обработка исключения с логированием
            raise

    def _format_category_products_worksheet(self, worksheet: Worksheet) -> None:
        """
        Форматирование листа с продуктами категории.

        Args:
            worksheet (Worksheet): Лист Google Sheets для форматирования.
        """
        try:
            # Установка ширины столбцов
            set_column_width(worksheet, 'A:A', 250)  # Ширина столбца A
            set_column_width(worksheet, 'B:B', 220)  # Ширина столбца B
            set_column_width(worksheet, 'C:C', 220)  # Ширина столбца C
            set_column_width(worksheet, 'D:D', 220)  # Ширина столбца D
            set_column_width(worksheet, 'E:E', 200)  # Ширина столбца E
            set_column_width(worksheet, 'F:F', 200)  # Ширина столбца F
            set_column_width(worksheet, 'G:G', 200)  # Ширина столбца G
            set_column_width(worksheet, 'H:H', 200)  # Ширина столбца H
            set_column_width(worksheet, 'I:I', 200)  # Ширина столбца I
            set_column_width(worksheet, 'J:J', 200)  # Ширина столбца J
            set_column_width(worksheet, 'K:K', 200)  # Ширина столбца K
            set_column_width(worksheet, 'L:L', 200)  # Ширина столбца L
            set_column_width(worksheet, 'M:M', 200)  # Ширина столбца M
            set_column_width(worksheet, 'N:N', 200)  # Ширина столбца N
            set_column_width(worksheet, 'O:O', 200)  # Ширина столбца O
            set_column_width(worksheet, 'P:P', 200)  # Ширина столбца P
            set_column_width(worksheet, 'Q:Q', 200)  # Ширина столбца Q
            set_column_width(worksheet, 'R:R', 200)  # Ширина столбца R
            set_column_width(worksheet, 'S:S', 200)  # Ширина столбца S
            set_column_width(worksheet, 'T:T', 200)  # Ширина столбца T
            set_column_width(worksheet, 'U:U', 200)  # Ширина столбца U
            set_column_width(worksheet, 'V:V', 200)  # Ширина столбца V
            set_column_width(worksheet, 'W:W', 200)  # Ширина столбца W
            set_column_width(worksheet, 'X:X', 200)  # Ширина столбца X
            set_column_width(worksheet, 'Y:Y', 200)  # Ширина столбца Y

            # Установка высоты строк
            set_row_height(worksheet, '1:1', 40)  # Высота заголовков

            # Форматирование заголовков
            header_format: cellFormat = cellFormat(
                textFormat=textFormat(bold=True, fontSize=12),
                horizontalAlignment='CENTER',
                verticalAlignment='TOP',  # Добавлено вертикальное выравнивание
                backgroundColor=Color(0.8, 0.8, 0.8)  # Используем Color для задания цвета
            )
            format_cell_range(worksheet, 'A1:Y1', header_format)

            logger.info('Category products worksheet formatted.')
        except Exception as ex:
            logger.error('Error formatting category products worksheet.', ex, exc_info=True) # Обработка исключения с логированием
            raise