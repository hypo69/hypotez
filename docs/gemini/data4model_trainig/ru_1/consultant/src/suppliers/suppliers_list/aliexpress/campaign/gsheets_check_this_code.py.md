### **Анализ кода модуля `gsheets_check_this_code.py`**

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование логирования через `logger` из модуля `src.logger`.
    - Наличие обработки исключений с логированием ошибок.
    - Применение аннотаций типов.
    - Разбиение функциональности на отдельные методы.
- **Минусы**:
    - Отсутствует документация модуля в соответствии с заданным форматом.
    - Некоторые docstring написаны на английском языке.
    - Не везде используются одинарные кавычки.
    - Смешанный стиль комментариев (где-то присутствует описание "что делается", а не "зачем").
    - Не используются f-строки для форматирования строк в logger.info
    - Не всегда используется явное преобразование типов к `str` при записи данных в Google Sheets.

**Рекомендации по улучшению**:

1.  **Документация модуля**:
    - Добавить заголовок модуля с описанием его назначения, как указано в инструкции.

2.  **Docstring на русском языке**:
    - Перевести все docstring на русский язык, следуя установленному формату.

3.  **Использование одинарных кавычек**:
    - Заменить двойные кавычки на одинарные во всем коде, где это необходимо.

4.  **Комментарии**:
    - Перефразировать комментарии, чтобы они объясняли *зачем* выполняется определенный блок кода, а не *что* он делает.

5.  **Форматирование строк в logger.info**:
    - Использовать f-строки для форматирования строк при логировании.

6.  **Преобразование типов**:
    - Явно преобразовывать все значения к строковому типу (`str()`) при записи в Google Sheets, чтобы избежать возможных ошибок.

7.  **Улучшение обработки исключений**:
    - Проверить, чтобы во всех блоках `except` переменная исключения называлась `ex`.

8.  **Удалить неиспользуемые импорты**:
    - Удалить неиспользуемые импорты: `from src.ai.openai import translate` и `from types import SimpleNamespace`
    - Удалить дублирующиеся импорты: `from types import SimpleNamespace`, `from src.goog.spreadsheet.spreadsheet import SpreadSheet` и `from src.webdriver.driver import Driver, Chrome`

**Оптимизированный код**:

```python
                ## \file /src/suppliers/aliexpress/campaign/gsheets_check_this_code.py
# -*- coding: utf-8 -*-\n
#! .pyenv/bin/python3\n

"""
Модуль для работы с Google Sheets для управления рекламными кампаниями AliExpress.
==============================================================================

Модуль содержит класс :class:`AliCampaignGoogleSheet`, который наследует класс :class:`SpreadSheet`
и предоставляет методы для создания, редактирования и форматирования листов Google Sheets
с данными о кампаниях, категориях и продуктах AliExpress.

Пример использования
----------------------

>>> campaign_name = 'test_campaign'
>>> language = 'ru'
>>> currency = 'USD'
>>> gsheet = AliCampaignGoogleSheet(campaign_name, language, currency)
>>> # gsheet.set_products_worksheet('category_name')  # Пример заполнения данными о продуктах
"""

import time
from typing import Optional, List, Dict
from pathlib import Path
from types import SimpleNamespace

from gspread.worksheet import Worksheet
from gspread_formatting import (
    cellFormat,
    textFormat,
    Color,
    format_cell_range,
    set_column_width,
    set_row_height,
)

from src.goog.spreadsheet.spreadsheet import SpreadSheet
from src.webdriver.driver import Driver, Chrome
from src.suppliers.suppliers_list.aliexpress.campaign.ali_campaign_editor import AliCampaignEditor
from src.utils.jjson import j_dumps
from src.utils.printer import pprint
from src.logger.logger import logger


class AliCampaignGoogleSheet(SpreadSheet):
    """
    Класс для работы с Google Sheets в рамках кампаний AliExpress.

    Наследует класс SpreadSheet и предоставляет дополнительные методы для управления листами Google Sheets,
    записи данных о категориях и продуктах, и форматирования листов.
    """

    spreadsheet_id = '1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0'
    spreadsheet: SpreadSheet
    worksheet: Worksheet
    driver: Driver = Driver(Chrome)

    def __init__(self, campaign_name: str, language: str | dict = None, currency: str = None) -> None:
        """
        Инициализация AliCampaignGoogleSheet с указанным ID таблицы Google Sheets и дополнительными параметрами.

        Args:
            campaign_name (str): Название кампании.
            language (str | dict, optional): Язык для кампании. По умолчанию None.
            currency (str, optional): Валюта для кампании. По умолчанию None.
        """
        # Инициализация SpreadSheet с ID таблицы
        super().__init__(spreadsheet_id=self.spreadsheet_id)
        self.editor = AliCampaignEditor(campaign_name=campaign_name, language=language, currency=currency)
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
            logger.error('Ошибка очистки', ex, exc_info=True)

    def delete_products_worksheets(self) -> None:
        """
        Удаляет все листы из таблицы Google Sheets, кроме 'categories', 'product' и 'campaign'.
        """
        excluded_titles = {'categories', 'product', 'category', 'campaign'}
        try:
            worksheets = self.spreadsheet.worksheets()
            for sheet in worksheets:
                if sheet.title not in excluded_titles:
                    self.spreadsheet.del_worksheet_by_id(sheet.id)
                    logger.info(f'Worksheet \'{sheet.title}\' deleted.')
        except Exception as ex:
            logger.error('Error deleting all worksheets.', ex, exc_info=True)
            raise

    def set_campaign_worksheet(self, campaign: SimpleNamespace) -> None:
        """
        Записывает данные кампании на лист Google Sheets.

        Args:
            campaign (SimpleNamespace): Объект SimpleNamespace с полями данных кампании для записи.
        """
        try:
            ws: Worksheet = self.get_worksheet('campaign')  # Получаем лист 'campaign'
            ws.clear()  # Очищаем лист 'campaign'

            # Подготовка данных для вертикальной записи
            updates = []
            vertical_data = [
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

            # Выполняем пакетное обновление
            if updates:
                ws.batch_update(updates)

            logger.info('Campaign data written to \'campaign\' worksheet vertically.')

        except Exception as ex:
            logger.error('Error setting campaign worksheet.', ex, exc_info=True)
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

        ws = self.copy_worksheet('product', category_name)

        try:
            row_data = []
            for product in products:
                _ = product.__dict__
                row_data.append([
                    str(_.get('product_id')),
                    _.get('product_title'),
                    _.get('promotion_link'),
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
                    _.get('evaluate_rate'),
                    _.get('shop_url'),
                    _.get('shop_id'),
                    ', '.join(_.get('tags', []))
                ])

            for index, row in enumerate(row_data, start=2):
                ws.update(f'A{index}:Y{index}', [row])
                logger.info(f'Products {str(_.get("product_id"))} updated.')

            self._format_category_products_worksheet(ws)

            logger.info('Products updated in worksheet.')

        except Exception as ex:
            logger.error('Error setting products worksheet.', ex, exc_info=True)
            raise

    def set_categories_worksheet(self, categories: SimpleNamespace) -> None:
        """
        Записывает данные из объекта SimpleNamespace с категориями в ячейки Google Sheets.

        Args:
            categories (SimpleNamespace): Объект, где ключи — это категории с данными для записи.
        """
        ws: Worksheet = self.get_worksheet('categories')
        ws.clear()  # Очистка рабочей таблицы перед записью данных

        try:
            # Получение всех ключей (категорий) и соответствующих значений
            category_data = categories.__dict__

            # Проверка, что все объекты категории имеют необходимые атрибуты
            required_attrs = ['name', 'title', 'description', 'tags', 'products_count']

            if all(all(hasattr(category, attr) for attr in required_attrs) for category in category_data.values()):
                # Заголовки для таблицы
                headers = ['Name', 'Title', 'Description', 'Tags', 'Products Count']
                ws.update('A1:E1', [headers])

                # Подготовка данных для записи
                rows = []
                for category in category_data.values():
                    row_data = [
                        category.name,
                        category.title,
                        category.description,
                        ', '.join(category.tags),
                        category.products_count,
                    ]
                    rows.append(row_data)

                # Обновляем строки данных
                ws.update(f'A2:E{1 + len(rows)}', rows)

                # Форматируем таблицу
                self._format_categories_worksheet(ws)

                logger.info('Category fields updated from SimpleNamespace object.')
            else:
                logger.warning('One or more category objects do not contain all required attributes.')

        except Exception as ex:
            logger.error('Error updating fields from SimpleNamespace object.', ex, exc_info=True)
            raise

    def get_categories(self) -> list[dict]:
        """
        Получение данных из таблицы Google Sheets.

        Returns:
            list[dict]: Данные из таблицы в виде списка словарей.
        """
        ws = self.get_worksheet('categories')
        data = ws.get_all_records()
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

        ws = self.copy_worksheet('product', category_name)
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
            updates = [{'range': 'A1:Y1', 'values': [headers]}]  # Add headers to the worksheet

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
                logger.info(f'Products {str(_.get("product_id"))} updated.')

            self._format_category_products_worksheet(ws)

            logger.info('Products updated in worksheet.')
        except Exception as ex:
            logger.error('Error updating products in worksheet.', ex, exc_info=True)
            raise

    def _format_categories_worksheet(self, ws: Worksheet) -> None:
        """
        Форматирование листа 'categories'.

        Args:
            ws (Worksheet): Лист Google Sheets для форматирования.
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
                backgroundColor=Color(0.8, 0.8, 0.8)  # Используем Color для задания цвета
            )
            format_cell_range(ws, 'A1:E1', header_format)

            logger.info('Categories worksheet formatted.')
        except Exception as ex:
            logger.error('Error formatting categories worksheet.', ex, exc_info=True)
            raise

    def _format_category_products_worksheet(self, ws: Worksheet) -> None:
        """
        Форматирование листа с продуктами категории.

        Args:
            ws (Worksheet): Лист Google Sheets для форматирования.
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
                backgroundColor=Color(0.8, 0.8, 0.8)  # Используем Color для задания цвета
            )
            format_cell_range(ws, 'A1:Y1', header_format)

            logger.info('Category products worksheet formatted.')
        except Exception as ex:
            logger.error('Error formatting category products worksheet.', ex, exc_info=True)
            raise