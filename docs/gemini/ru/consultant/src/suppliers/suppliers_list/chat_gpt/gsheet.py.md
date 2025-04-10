### **Анализ кода модуля `gsheet.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Класс `GptGs` хорошо структурирован и наследует от `SpreadSheet`, что способствует повторному использованию кода.
    - Использование `logger` для логирования ошибок и информации.
    - Разделение функциональности на отдельные методы, такие как `clear`, `update_chat_worksheet`, `get_campaign_worksheet` и т.д.

- **Минусы**:
    - Отсутствие документации модуля в начале файла.
    - Неполные docstring для некоторых методов (например, отсутствует описание возвращаемых значений и исключений).
    - Использование устаревшего стиля комментариев (например, `\t:platform:`).
    - Смешанный стиль кавычек (используются как одинарные, так и двойные кавычки).
    - Отсутствие аннотаций типов для всех переменных.
    - Не везде используется `ex` вместо `e` в блоках обработки исключений.
    - Встречаются закомментированные участки кода, которые следует удалить или объяснить.
    - Не все методы имеют примеры использования.
    - Есть неиспользуемые импорты.
    - Не везде используется форматирование с пробелами вокруг оператора присваивания.
    - Присутсвуют `...` в коде.

**Рекомендации по улучшению:**

1.  **Добавить документацию модуля**:
    - В начале файла добавить общее описание модуля и примеры его использования.

2.  **Обновить docstring**:
    - Для всех методов добавить полные docstring с описанием параметров, возвращаемых значений и возможных исключений.

3.  **Удалить устаревшие комментарии**:
    - Убрать комментарии типа `\t:platform:` и заменить их на более современные и информативные.

4.  **Использовать единообразный стиль кавычек**:
    - Привести все строки к одинарным кавычкам.

5.  **Добавить аннотации типов**:
    - Явно указать типы данных для всех переменных и параметров функций.

6.  **Исправить блоки обработки исключений**:
    - Использовать `ex` вместо `e` в блоках `except`.
    - Убедиться, что все исключения логируются с использованием `logger.error` с передачей `exc_info=True`.

7.  **Удалить или объяснить закомментированные участки кода**:
    - Если закомментированный код больше не нужен, его следует удалить. Если он содержит важную информацию, его следует преобразовать в комментарии или docstring.

8.  **Добавить примеры использования**:
    - Добавить примеры использования для наиболее важных методов.

9.  **Удалить неиспользуемые импорты**:
    - Убрать неиспользуемые импорты, чтобы сделать код чище.

10. **Форматирование с пробелами**:
    - Добавить пробелы вокруг операторов присваивания.

**Оптимизированный код:**

```python
"""
Модуль для работы с Google Sheets для управления кампаниями AliExpress.
=======================================================================

Модуль содержит класс :class:`GptGs`, который наследуется от `SpreadSheet`
и предназначен для управления Google Sheets, записи данных о категориях и продуктах,
а также для форматирования листов.

Пример использования:
----------------------

>>> gpt_gs = GptGs()
>>> campaign_data = gpt_gs.get_campaign_worksheet()
>>> if campaign_data:
...     print(f"Название кампании: {campaign_data.name}")
"""

import time
from types import SimpleNamespace
from typing import List, Optional, Dict, Any
from gspread.worksheet import Worksheet
from src.goog.spreadsheet.spreadsheet import SpreadSheet
from src.utils.printer import pprint
from src.logger.logger import logger

class GptGs(SpreadSheet):
    """
    Класс для управления Google Sheets в кампаниях AliExpress.

    Наследуется от `SpreadSheet` для управления Google Sheets,
    записи данных о категориях и продуктах, а также для форматирования листов.
    """

    def __init__(self) -> None:
        """
        Инициализирует AliCampaignGoogleSheet с указанным ID Google Sheets таблицы.

        Args:
            campaign_name (str): Название кампании.
            category_name (str): Название категории.
            language (str): Язык для кампании.
            currency (str): Валюта для кампании.
        """
        # Инициализация SpreadSheet с ID таблицы
        super().__init__('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')

    def clear(self) -> None:
        """
        Очищает содержимое Google Sheets.

        Удаляет листы продуктов и очищает данные на листах категорий и других указанных листах.

        Raises:
            Exception: Если происходит ошибка при очистке.
        """
        try:
            self.delete_products_worksheets()
            # ws_to_clear = ['category','categories','campaign']
            # for ws in self.spreadsheet.worksheets():
            #     self.get_worksheet(ws).clear()

        except Exception as ex:
            logger.error('Ошибка очистки', ex, exc_info=True)

    def update_chat_worksheet(
        self,
        data: SimpleNamespace | Dict[str, Any] | List[Any],
        conversation_name: str,
        language: Optional[str] = None
    ) -> None:
        """
        Записывает данные кампании на лист Google Sheets.

        Args:
            data (SimpleNamespace | Dict[str, Any] | List[Any]): Объект SimpleNamespace с полями данных кампании для записи.
            conversation_name (str): Имя листа для записи.
            language (Optional[str], optional): Язык. По умолчанию None.

        Raises:
            Exception: Если происходит ошибка при записи данных кампании на лист.
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
            updates: List[Dict[str, Any]] = [
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
            Exception: Если происходит ошибка при получении данных с листа кампании.
        """
        try:
            ws: Worksheet = self.get_worksheet('campaign')
            if not ws:
                raise ValueError('Worksheet \'campaign\' not found.')

            data: List[List[str]] = ws.get_all_values()
            campaign_data: SimpleNamespace = SimpleNamespace(
                name=data[0][1],
                title=data[1][1],
                language=data[2][1],
                currency=data[3][1],
                description=data[4][1]
            )

            logger.info('Данные кампании прочитаны с листа \'campaign\'.')
            return campaign_data

        except Exception as ex:
            logger.error('Ошибка получения данных с листа кампании.', ex, exc_info=True)
            raise

    def set_category_worksheet(self, category: SimpleNamespace | str) -> None:
        """
        Записывает данные из объекта SimpleNamespace в ячейки Google Sheets по вертикали.

        Args:
            category (SimpleNamespace | str): Объект SimpleNamespace с полями данных для записи.

        Raises:
            TypeError: Если передан не SimpleNamespace.
            Exception: Если происходит ошибка при записи данных категории на лист.
        """
        category = category if isinstance(category, SimpleNamespace) else self.get_campaign_category(category)
        try:
            ws: Worksheet = self.get_worksheet('category')

            if isinstance(category, SimpleNamespace):
                # Подготовка данных для вертикальной записи
                _: Dict[str, Any] = category.__dict__
                vertical_data: List[List[str]] = [
                    ['Name', _.get('name', '')],
                    ['Title', _.get('title', '')],
                    ['Description', _.get('description')],
                    ['Tags', ', '.join(map(str, _.get('tags', [])))],
                    ['Products Count', _.get('products_count', '~')]
                ]

                # Запись данных по вертикали
                ws.update('A1:B{}'.format(len(vertical_data)), vertical_data)

                logger.info('Данные категории записаны на лист \'category\' по вертикали.')
            else:
                raise TypeError('Expected SimpleNamespace for category.')

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
            Exception: Если происходит ошибка при получении данных с листа категории.
        """
        try:
            ws: Worksheet = self.get_worksheet('category')
            if not ws:
                raise ValueError('Worksheet \'category\' not found.')

            data: List[List[str]] = ws.get_all_values()
            category_data: SimpleNamespace = SimpleNamespace(
                name=data[1][1],
                title=data[2][1],
                description=data[3][1],
                tags=data[4][1].split(', '),
                products_count=int(data[5][1])
            )

            logger.info('Данные категории прочитаны с листа \'category\'.')
            return category_data

        except Exception as ex:
            logger.error('Ошибка получения данных с листа категории.', ex, exc_info=True)
            raise

    def set_categories_worksheet(self, categories: SimpleNamespace) -> None:
        """
        Записывает данные из объекта SimpleNamespace в ячейки Google Sheets.

        Args:
            categories (SimpleNamespace): Объект SimpleNamespace с полями данных для записи.

        Raises:
            Exception: Если происходит ошибка при записи данных категорий на лист.
        """
        ws: Worksheet = self.get_worksheet('categories')
        # ws.clear()  # Очистить лист 'categories'

        try:
            # Инициализация начальной строки
            start_row: int = 2

            # Итерация по всем атрибутам объекта categories
            for attr_name in dir(categories):
                attr_value: Any = getattr(categories, attr_name, None)

                # Пропустить атрибуты, не являющиеся SimpleNamespace, или атрибуты без данных
                if not isinstance(attr_value, SimpleNamespace) or not any(
                    hasattr(attr_value, field) for field in ['name', 'title', 'description', 'tags', 'products_count']
                ):
                    continue
                _: Dict[str, Any] = attr_value.__dict__
                # Извлечение данных из атрибута SimpleNamespace
                name: str = _.get('name', '')
                title: str = _.get('title')
                description: str = _.get('description')
                tags: str = ', '.join(map(str, _.get('tags', [])))
                products_count: str = _.get('products_count', '~')

                # Подготовка обновлений для данного объекта SimpleNamespace
                updates: List[Dict[str, Any]] = [
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

        Raises:
            ValueError: Если лист 'categories' не найден.
            Exception: Если происходит ошибка при получении данных категории с листа.
        """
        try:
            ws: Worksheet = self.get_worksheet('categories')
            if not ws:
                raise ValueError('Worksheet \'categories\' not found.')

            # Чтение всех значений с листа
            data: List[List[str]] = ws.get_all_values()

            # Извлечение данных из столбцов A по E, начиная со второй строки
            data: List[List[str]] = [row[:5] for row in data[1:] if len(row) >= 5]

            logger.info('Данные категории прочитаны с листа \'categories\'.')
            return data

        except Exception as ex:
            logger.error('Ошибка получения данных категории с листа.', ex, exc_info=True)
            raise

    def set_product_worksheet(self, product: SimpleNamespace | str, category_name: str) -> None:
        """
        Записывает данные продукта на новый лист Google Sheets.

        Args:
            category_name (str): Название категории.
            product (SimpleNamespace): Объект SimpleNamespace с полями данных продукта для записи.

        Raises:
            Exception: Если происходит ошибка при обновлении данных продукта на листе.
        """
        time.sleep(10)
        ws: Worksheet = self.copy_worksheet('product_template', category_name)  # Копировать 'product_template' на новый лист
        try:
            headers: List[str] = [
                'product_id', 'app_sale_price', 'original_price', 'sale_price', 'discount',
                'product_main_image_url', 'local_image_path', 'product_small_image_urls',
                'product_video_url', 'local_video_path', 'first_level_category_id',
                'first_level_category_name', 'second_level_category_id', 'second_level_category_name',
                'target_sale_price', 'target_sale_price_currency', 'target_app_sale_price_currency',
                'target_original_price_currency', 'original_price_currency', 'product_title',
                'evaluate_rate', 'promotion_link', 'shop_url', 'shop_id', 'tags'
            ]
            ws.update('A1:Y1', [headers])

            _: Dict[str, Any] = product.__dict__
            row_data: List[str] = [
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

            ws.update('A2:Y2', [row_data])  # Обновить данные строки в одной строке

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
            Exception: Если происходит ошибка при получении данных с листа продукта.
        """
        try:
            ws: Worksheet = self.get_worksheet('products')
            if not ws:
                raise ValueError('Worksheet \'products\' not found.')

            data: List[List[str]] = ws.get_all_values()
            product_data: SimpleNamespace = SimpleNamespace(
                id=data[1][1],
                name=data[2][1],
                title=data[3][1],
                description=data[4][1],
                tags=data[5][1].split(', '),
                price=float(data[6][1])
            )

            logger.info('Данные продукта прочитаны с листа \'products\'.')
            return product_data

        except Exception as ex:
            logger.error('Ошибка получения данных с листа продукта.', ex, exc_info=True)
            raise

    def set_products_worksheet(self, category_name: str) -> None:
        """
        Записывает данные из списка объектов SimpleNamespace в ячейки Google Sheets.

        Args:
            ns_list (List[SimpleNamespace] | SimpleNamespace): Список объектов SimpleNamespace с полями данных для записи.

        Raises:
            Exception: Если происходит ошибка при установке листа продуктов.
        """
        if category_name:
            category_ns: SimpleNamespace = getattr(self.campaign.category, category_name)
            products_ns: SimpleNamespace = category_ns.products
        else:
            logger.warning(f'На ашел товары в {pprint(category_ns)}')
            return
        ws: Worksheet = self.get_worksheet(category_name)

        try:
            updates: List[Dict[str, Any]] = []
            for index, value in enumerate(products_ns, start=2):
                _: Dict[str, Any] = value.__dict__
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
        Удаляет все листы из Google Sheets таблицы, кроме 'categories' и 'product_template'.

        Raises:
            Exception: Если происходит ошибка при удалении листов.
        """
        excluded_titles: set[str] = {'categories', 'product', 'category', 'campaign'}
        try:
            worksheets: List[Worksheet] = self.spreadsheet.worksheets()
            for sheet in worksheets:
                if sheet.title not in excluded_titles:
                    self.spreadsheet.del_worksheet_by_id(sheet.id)
                    logger.success(f'Worksheet \'{sheet.title}\' deleted.')
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
                'tags': _cat[3].split(','),
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
        data.category: SimpleNamespace = self.campaign.category
        self.campaign: SimpleNamespace = data
        self.update_campaign()
        ...