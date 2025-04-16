### **Анализ кода модуля `gsheet.py`**

## \\file /src/suppliers/chat_gpt/gsheet.py

Модуль предназначен для работы с Google Sheets в контексте управления AliExpress кампаниями. Он предоставляет классы и методы для чтения, записи и обновления данных в Google Sheets, а также для управления листами (worksheet) в этих таблицах.

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование `logger` для логирования.
    - Разделение функциональности по методам.
    - Четкое именование большинства методов, отражающее их назначение.
- **Минусы**:
    - Непоследовательное использование аннотаций типов.
    - Не все функции и методы имеют docstring.
    - Не везде используются одинарные кавычки.
    - Отсутствие аннотации типа у переменных.
    - Многочисленные пустые docstring и закомментированный код.
    - Использование устаревшего импорта `from lib2to3.pgen2.driver import Driver`.
    - Не все исключения обрабатываются с использованием `logger.error(..., ex, exc_info=True)`.
    - Смешанный стиль кодирования (использование `_` для именования переменных).

**Рекомендации по улучшению:**

1.  **Документация**:
    - Добавить docstring ко всем классам, методам и функциям, включая внутренние. Описать назначение, аргументы, возвращаемые значения и возможные исключения.
    - Перевести все существующие docstring на русский язык, используя формат UTF-8.
    - Заполнить пустые docstring.
    - Пример заполнения:

    ```python
    def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
        """Функция выполняет некоторое действие.

        Args:
            param (str): Описание параметра `param`.
            param1 (Optional[str | dict | str], optional): Описание параметра `param1`. По умолчанию `None`.

        Returns:
            dict | None: Описание возвращаемого значения. Возвращает словарь или `None`.

        Raises:
            SomeError: Описание ситуации, в которой возникает исключение `SomeError`.
        """
        ...
    ```

2.  **Аннотации типов**:
    - Добавить аннотации типов ко всем переменным, аргументам функций и возвращаемым значениям, чтобы улучшить читаемость и облегчить отладку.
    - Исправить аннотацию типов, используя `|` вместо `Union`.

    ```python
    def update_chat_worksheet(self, data: SimpleNamespace | dict | list, conversation_name: str, language: str = None):
        ...
    ```

3.  **Форматирование**:
    - Использовать только одинарные кавычки (`'`) для строк.
    - Добавить пробелы вокруг операторов присваивания (`=`).

4.  **Логирование**:
    - Убедиться, что все исключения обрабатываются с использованием `logger.error(..., ex, exc_info=True)`.
    - Добавить логирование важных этапов выполнения кода.

5.  **Обработка данных**:
    - Пересмотреть использование `SimpleNamespace` и, возможно, заменить его более строгой структурой данных (например, dataclass).
    - Проверить и улучшить обработку ошибок при чтении и записи данных в Google Sheets.

6.  **Удаление неиспользуемого кода**:
    - Удалить закомментированный код и неиспользуемые импорты.

7.  **Комментарии**:
    - Заменить общие комментарии, такие как "Write data", на более конкретные, например, "Write category data to worksheet".
    - Комментарии должны быть на русском языке и в формате UTF-8.

8.  **Импорты**:
    - Удалить устаревший импорт `from lib2to3.pgen2.driver import Driver`. Если нужен `Driver` использовать `from src.webdirver import Driver`

**Оптимизированный код:**

```python
## \\file /src/suppliers/chat_gpt/gsheet.py
# -*- coding: utf-8 -*-\n
#! .pyenv/bin/python3

"""
Модуль для работы с Google Sheets в контексте управления AliExpress кампаниями.
===========================================================================

Модуль содержит класс :class:`GptGs`, который используется для взаимодействия с Google Sheets,
для чтения, записи и обновления данных, связанных с AliExpress кампаниями.
"""

import time
from types import SimpleNamespace
from typing import List, Optional

from gspread.worksheet import Worksheet

from src.goog.spreadsheet.spreadsheet import SpreadSheet
from src.logger.logger import logger
from src.utils.jjson import j_dumps
from src.utils.printer import pprint


class GptGs(SpreadSheet):
    """
    Класс для управления Google Sheets в рамках AliExpress кампаний.

    Наследуется от `SpreadSheet` для управления Google Sheets, записи данных о категориях и продуктах,
    а также для форматирования листов.
    """

    def __init__(self) -> None:
        """
        Инициализирует AliCampaignGoogleSheet с указанным ID Google Sheets spreadsheet и дополнительными параметрами.
        """
        # Инициализация SpreadSheet с ID spreadsheet
        super().__init__('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')

    def clear(self) -> None:
        """
        Очищает содержимое листов.

        Удаляет листы продуктов и очищает данные на листах категорий и других указанных листах.
        """
        try:
            self.delete_products_worksheets()
        except Exception as ex:
            logger.error('Ошибка очистки', ex, exc_info=True)

    def update_chat_worksheet(self, data: SimpleNamespace | dict | list, conversation_name: str, language: Optional[str] = None) -> None:
        """
        Записывает данные кампании на лист Google Sheets.

        Args:
            data (SimpleNamespace | dict | list): Объект SimpleNamespace с полями данных кампании для записи.
            conversation_name (str): Имя листа, в который нужно записать данные.
            language (str, optional): Необязательный параметр языка. По умолчанию `None`.
        """
        try:
            ws: Worksheet = self.get_worksheet(conversation_name)
            _ = data.__dict__
            # Извлечение данных из атрибута SimpleNamespace
            name: str = _.get('name', '')
            title: str = _.get('title')
            description: str = _.get('description')
            tags: str = ', '.join(map(str, _.get('tags', [])))
            products_count: str = _.get('products_count', '~')

            # Подготовка обновлений для данного объекта SimpleNamespace
            updates: list[dict] = [
                {'range': f'A{start_row}', 'values': [[name]]},
                {'range': f'B{start_row}', 'values': [[title]]},
                {'range': f'C{start_row}', 'values': [[description]]},
                {'range': f'D{start_row}', 'values': [[tags]]},
                {'range': f'E{start_row}', 'values': [[products_count]]},
            ]

        except Exception as ex:
            logger.error('Ошибка записи данных кампании на лист.', ex, exc_info=True)
            raise

    def get_campaign_worksheet(self) -> SimpleNamespace:
        """
        Считывает данные кампании с листа 'campaign'.

        Returns:
            SimpleNamespace: Объект SimpleNamespace с полями данных кампании.

        Raises:
            ValueError: Если лист 'campaign' не найден.
        """
        try:
            ws: Worksheet = self.get_worksheet('campaign')
            if not ws:
                raise ValueError('Лист \'campaign\' не найден.')

            data: list[list[str]] = ws.get_all_values()
            campaign_data: SimpleNamespace = SimpleNamespace(
                name=data[0][1],
                title=data[1][1],
                language=data[2][1],
                currency=data[3][1],
                description=data[4][1]
            )

            logger.info('Данные кампании считаны с листа \'campaign\'.')
            return campaign_data

        except Exception as ex:
            logger.error('Ошибка получения данных с листа кампании.', ex, exc_info=True)
            raise

    def set_category_worksheet(self, category: SimpleNamespace | str) -> None:
        """
        Записывает данные из объекта SimpleNamespace в ячейки Google Sheets по вертикали.

        Args:
            category (SimpleNamespace | str): Объект SimpleNamespace с полями данных для записи.
        """
        category = category if isinstance(category, SimpleNamespace) else self.get_campaign_category(category)
        try:
            ws: Worksheet = self.get_worksheet('category')

            if isinstance(category, SimpleNamespace):
                # Подготовка данных для вертикальной записи
                _ = category.__dict__
                vertical_data: list[list[str]] = [
                    ['Name', _.get('name', '')],
                    ['Title', _.get('title', '')],
                    ['Description', _.get('description')],
                    ['Tags', ', '.join(map(str, _.get('tags', [])))],
                    ['Products Count', _.get('products_count', '~')]
                ]

                # Запись данных по вертикали
                ws.update(f'A1:B{len(vertical_data)}', vertical_data)

                logger.info('Данные категории записаны на лист \'category\' по вертикали.')
            else:
                raise TypeError('Ожидается SimpleNamespace для category.')

        except Exception as ex:
            logger.error('Ошибка установки листа категории.', ex, exc_info=True)
            raise

    def get_category_worksheet(self) -> SimpleNamespace:
        """
        Считывает данные категории с листа 'category'.

        Returns:
            SimpleNamespace: Объект SimpleNamespace с полями данных категории.

        Raises:
            ValueError: Если лист 'category' не найден.
        """
        try:
            ws: Worksheet = self.get_worksheet('category')
            if not ws:
                raise ValueError('Лист \'category\' не найден.')

            data: list[list[str]] = ws.get_all_values()
            category_data: SimpleNamespace = SimpleNamespace(
                name=data[1][1],
                title=data[2][1],
                description=data[3][1],
                tags=data[4][1].split(', '),
                products_count=int(data[5][1])
            )

            logger.info('Данные категории считаны с листа \'category\'.')
            return category_data

        except Exception as ex:
            logger.error('Ошибка получения данных с листа категории.', ex, exc_info=True)
            raise

    def set_categories_worksheet(self, categories: SimpleNamespace) -> None:
        """
        Записывает данные из объекта SimpleNamespace в ячейки Google Sheets.

        Args:
            categories (SimpleNamespace): Объект SimpleNamespace с полями данных для записи.
        """
        ws: Worksheet = self.get_worksheet('categories')

        try:
            # Инициализация начальной строки
            start_row: int = 2

            # Итерация по всем атрибутам объекта categories
            for attr_name in dir(categories):
                attr_value = getattr(categories, attr_name, None)

                # Пропуск не-SimpleNamespace атрибутов или атрибутов без данных
                if not isinstance(attr_value, SimpleNamespace) or not any(
                    hasattr(attr_value, field) for field in ['name', 'title', 'description', 'tags', 'products_count']
                ):
                    continue
                _ = attr_value.__dict__
                # Извлечение данных из атрибута SimpleNamespace
                name: str = _.get('name', '')
                title: str = _.get('title')
                description: str = _.get('description')
                tags: str = ', '.join(map(str, _.get('tags', [])))
                products_count: str = _.get('products_count', '~')

                # Подготовка обновлений для данного объекта SimpleNamespace
                updates: list[dict] = [
                    {'range': f'A{start_row}', 'values': [[name]]},
                    {'range': f'B{start_row}', 'values': [[title]]},
                    {'range': f'C{start_row}', 'values': [[description]]},
                    {'range': f'D{start_row}', 'values': [[tags]]},
                    {'range': f'E{start_row}', 'values': [[products_count]]},
                ]

                # Выполнение пакетного обновления
                if updates:
                    ws.batch_update(updates)
                    logger.info(f'Данные категории записаны на лист \'categories\' для {attr_name}.')

                # Переход к следующей строке
                start_row += 1

        except Exception as ex:
            logger.error('Ошибка установки листа категорий.', ex, exc_info=True)
            raise

    def get_categories_worksheet(self) -> List[List[str]]:
        """
        Считывает данные из столбцов A по E, начиная со второй строки, с листа 'categories'.

        Returns:
            List[List[str]]: Список строк с данными из столбцов A по E.
        """
        try:
            ws: Worksheet = self.get_worksheet('categories')
            if not ws:
                raise ValueError('Лист \'categories\' не найден.')

            # Чтение всех значений с листа
            data: list[list[str]] = ws.get_all_values()

            # Извлечение данных из столбцов A по E, начиная со второй строки
            data: list[list[str]] = [row[:5] for row in data[1:] if len(row) >= 5]

            logger.info('Данные категории считаны с листа \'categories\'.')
            return data

        except Exception as ex:
            logger.error('Ошибка получения данных категории с листа.', ex, exc_info=True)
            raise

    def set_product_worksheet(self, product: SimpleNamespace | str, category_name: str) -> None:
        """
        Записывает данные продукта в новый Google Sheets spreadsheet.

        Args:
            category_name (str): Название категории.
            product (SimpleNamespace): Объект SimpleNamespace с полями данных продукта для записи.
        """
        time.sleep(10)
        ws: Worksheet = self.copy_worksheet('product_template', category_name)  # Копирование 'product_template' в новый лист
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
            ws.update('A1:Y1', [headers])

            _ = product.__dict__
            row_data: list[str] = [
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

            ws.update('A2:Y2', [row_data])  # Обновление данных строки в одной строке

            logger.info('Данные продукта записаны на лист.')
        except Exception as ex:
            logger.error('Ошибка обновления данных продукта на листе.', ex, exc_info=True)
            raise

    def get_product_worksheet(self) -> SimpleNamespace:
        """
        Считывает данные продукта с листа 'products'.

        Returns:
            SimpleNamespace: Объект SimpleNamespace с полями данных продукта.

        Raises:
            ValueError: Если лист 'products' не найден.
        """
        try:
            ws: Worksheet = self.get_worksheet('products')
            if not ws:
                raise ValueError('Лист \'products\' не найден.')

            data: list[list[str]] = ws.get_all_values()
            product_data: SimpleNamespace = SimpleNamespace(
                id=data[1][1],
                name=data[2][1],
                title=data[3][1],
                description=data[4][1],
                tags=data[5][1].split(', '),
                price=float(data[6][1])
            )

            logger.info('Данные продукта считаны с листа \'products\'.')
            return product_data

        except Exception as ex:
            logger.error('Ошибка получения данных продукта с листа.', ex, exc_info=True)
            raise

    def set_products_worksheet(self, category_name: str) -> None:
        """
        Записывает данные из списка объектов SimpleNamespace в ячейки Google Sheets.

        Args:
            category_name (str): Имя категории.
        """
        if category_name:
            category_ns: SimpleNamespace = getattr(self.campaign.category, category_name)
            products_ns: SimpleNamespace = category_ns.products
        else:
            logger.warning(f'Нашел товары в {pprint(category_ns)}')
            return
        ws: Worksheet = self.get_worksheet(category_name)

        try:
            updates: list[dict] = []
            for index, value in enumerate(products_ns, start=2):
                _ = value.__dict__
                updates.append({'range': f'A{index}', 'values': [[str(_.get('product_id', ''))]]})
                updates.append({'range': f'B{index}', 'values': [[str(_.get('product_title', ''))]]})
                updates.append({'range': f'C{index}', 'values': [[str(_.get('title', ''))]]})
                updates.append({'range': f'D{index}', 'values': [[str(_.get('local_image_path', ''))]]})
                updates.append({'range': f'D{index}', 'values': [[str(_.get('product_video_url', ''))]]})
                updates.append({'range': f'F{index}', 'values': [[str(_.get('original_price', ''))]]})
                updates.append({'range': f'F{index}', 'values': [[str(_.get('app_sale_price', ''))]]})
                updates.append({'range': f'F{index}', 'values': [[str(_.get('target_sale_price', ''))]]})
                updates.append({'range': f'F{index}', 'values': [[str(_.get('target_sale_price', ''))]]})

            ws.batch_update(updates)
            logger.info('Данные продуктов записаны на лист \'products\'.')

        except Exception as ex:
            logger.error('Ошибка установки листа продуктов.', ex, exc_info=True)
            raise

    def delete_products_worksheets(self) -> None:
        """
        Удаляет все листы из Google Sheets spreadsheet, кроме 'categories', 'product', 'category' и 'campaign'.
        """
        excluded_titles: set[str] = {'categories', 'product', 'category', 'campaign'}
        try:
            worksheets: list[Worksheet] = self.spreadsheet.worksheets()
            for sheet in worksheets:
                if sheet.title not in excluded_titles:
                    self.spreadsheet.del_worksheet_by_id(sheet.id)
                    logger.success(f'Лист \'{sheet.title}\' удален.')
        except Exception as ex:
            logger.error('Ошибка удаления всех листов.', ex, exc_info=True)
            raise

    def save_categories_from_worksheet(self, update: bool = False) -> None:
        """Сохраняю данные, отредактированные в гугл таблице"""

        edited_categories: list[dict] = self.get_categories_worksheet()
        _categories_ns: SimpleNamespace = SimpleNamespace()
        for _cat in edited_categories:
            _cat_ns: SimpleNamespace = SimpleNamespace(**{
                'name': _cat[0],
                'title': _cat[1],
                'description': _cat[2],
                'tags': _cat[3].split(","),
                'products_count': _cat[4],
            }
            )
            setattr(_categories_ns, _cat_ns.name, _cat_ns)
        ...
        self.campaign.category = _categories_ns
        if update:
            self.update_campaign()

    def save_campaign_from_worksheet(self) -> None:
        """Сохраняю реклманую каманию"""
        self.save_categories_from_worksheet(False)
        data: SimpleNamespace = self.get_campaign_worksheet()
        data.category = self.campaign.category
        self.campaign = data
        self.update_campaign()
        ...