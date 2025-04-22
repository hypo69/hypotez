### **Анализ кода модуля `gsheet.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование логгирования через `logger`.
    - Наличие docstring для большинства функций.
    - Разбиение на функции для выполнения отдельных задач.
- **Минусы**:
    - Неполные docstring (отсутствуют описания аргументов и возвращаемых значений в некоторых функциях).
    - Использование `Union` вместо `|` в аннотациях типов.
    - Смешанный стиль кавычек (использование как двойных, так и одинарных кавычек).
    - Не везде указаны типы для переменных.
    - Не все функции содержат подробные комментарии, объясняющие их назначение.

**Рекомендации по улучшению:**

1.  **Общие улучшения**:
    *   Привести код в соответствие со стандартами PEP8.
    *   Заменить `Union` на `|` в аннотациях типов.
    *   Использовать только одинарные кавычки (`'`) для строк.
    *   Дополнить docstring для всех функций, указав аргументы, возвращаемые значения и возможные исключения.
    *   Добавить больше комментариев для пояснения логики работы функций, особенно в сложных участках кода.
    *   Добавить проверки типов там, где это необходимо для повышения надежности кода.

2.  **`__init__`**:
    *   Добавить docstring для метода `__init__`, описывающий параметры и их назначение.

3.  **`clear`**:
    *   Функция `clear` не имеет описания в docstring. Добавить описание, что именно очищается.
    *   Уточнить комментарий `"Ошибка очистки"` в блоке `except`, добавив контекст.

4.  **`update_chat_worksheet`**:
    *   В блоке `try` добавить проверку существования ключей в словаре `_`, прежде чем их извлекать.
    *   Указать тип данных для `start_row`.
    *   Удалить неиспользуемые параметры `language` и `currency`.
    *   Добавить проверку, что `ws` не `None`.

5.  **`get_campaign_worksheet`**:
    *   В docstring указать, какие поля содержит возвращаемый `SimpleNamespace`.

6.  **`set_category_worksheet`**:
    *   Убедиться, что метод `get_campaign_category` существует и возвращает ожидаемый тип данных.

7.  **`get_category_worksheet`**:
    *   Добавить обработку исключения, если данные в ячейках не соответствуют ожидаемому типу (например, `products_count` не является числом).
    *   Указать, что `tags` возвращаются в виде списка строк.

8.  **`set_categories_worksheet`**:
    *   Уточнить, какие атрибуты ожидаются у объектов `categories`.
    *   Добавить проверку на пустые значения для `name`, `title`, `description`, `tags`, `products_count` перед формированием `updates`.

9.  **`get_categories_worksheet`**:
    *   Добавить обработку ситуации, когда в строке меньше 5 элементов.

10. **`set_product_worksheet`**:
    *   Избавиться от `time.sleep(10)`, так как это плохая практика. Использовать более надежные способы ожидания.
    *   Уточнить, какие поля должны быть в `product`.
    *   Добавить возможность указания столбцов, в которые записываются данные, чтобы избежать магических значений (`'A1:Y1'`, `'A2:Y2'`).

11. **`get_product_worksheet`**:
    *   Уточнить, какие поля содержит возвращаемый `SimpleNamespace`.

12. **`set_products_worksheet`**:
    *   Функция `pprint` должна импортироваться из `src.utils.printer`, а не быть строкой.
    *   Исправить множественное добавление данных по ключу `'F{index}'`.
    *   Добавить обработку случая, когда `category_ns` или `products_ns` равны `None`.

13. **`delete_products_worksheets`**:
    *   Заменить `logger.success` на `logger.info` или `logger.debug`.

14. **`save_categories_from_worksheet`**:
    *   Добавить обработку исключений при присвоении атрибутов.
    *   Добавить описание `...` в конце функции.

15. **`save_campaign_from_worksheet`**:
    *   Добавить описание `...` в конце функции.

**Оптимизированный код:**

```python
## \file /src/suppliers/chat_gpt/gsheet.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для управления Google Sheets в кампаниях AliExpress.
==============================================================

Этот модуль содержит класс :class:`GptGs`, который наследуется от :class:`SpreadSheet`
и предназначен для управления Google Sheets, записи данных о категориях и товарах,
а также для форматирования листов.

Зависимости:
    - gspread
    - src.goog.spreadsheet.spreadsheet
    - src.utils.jjson
    - src.utils.printer
    - src.logger.logger

Пример использования:
    >>> gpt_gs = GptGs()
    >>> campaign_data = gpt_gs.get_campaign_worksheet()
"""

from typing import List, Optional, Dict, Any
from types import SimpleNamespace
from pathlib import Path
import time

from gspread.worksheet import Worksheet

from src.goog.spreadsheet.spreadsheet import SpreadSheet
from src.utils.jjson import j_dumps
from src.utils.printer import pprint
from src.logger.logger import logger


class GptGs(SpreadSheet):
    """
    Класс для управления Google Sheets в кампаниях AliExpress.

    Наследуется от `SpreadSheet` для управления Google Sheets, записи данных
    о категориях и товарах, а также для форматирования листов.
    """

    def __init__(self) -> None:
        """
        Инициализирует AliCampaignGoogleSheet с указанным ID Google Sheets spreadsheet и дополнительными параметрами.

        Args:
            campaign_name (str): Название кампании.
            category_name (str): Название категории.
            language (str): Язык для кампании.
            currency (str): Валюта для кампании.
        """
        # Инициализация SpreadSheet с ID spreadsheet
        super().__init__('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')

    def clear(self) -> None:
        """
        Очищает содержимое листов.

        Удаляет листы продуктов и очищает данные на листах категорий и других указанных листах.
        """
        try:
            # Удаление листов продуктов
            self.delete_products_worksheets()
            # ws_to_clear = ['category','categories','campaign']
            # for ws in self.spreadsheet.worksheets():
            #     self.get_worksheet(ws).clear()

        except Exception as ex:
            logger.error("Ошибка при очистке листов", ex, exc_info=True)  # Логирование ошибки очистки

    def update_chat_worksheet(
        self, data: SimpleNamespace | dict | list, conversation_name: str
    ) -> None:
        """
        Записывает данные кампании в Google Sheets worksheet.

        Args:
            data (SimpleNamespace | dict | list): Объект SimpleNamespace с полями данных кампании для записи.
            conversation_name (str): Имя worksheet для записи данных.
        """
        try:
            ws: Worksheet = self.get_worksheet(conversation_name)
            if ws is None:
                logger.error(f"Worksheet с именем '{conversation_name}' не найден.")
                return

            _ = data.__dict__
            # Извлечение данных из атрибута SimpleNamespace
            name: str = _.get('name', '')
            title: Optional[str] = _.get('title')
            description: Optional[str] = _.get('description')
            tags: str = ', '.join(map(str, _.get('tags', [])))
            products_count: str = _.get('products_count', '~')
            start_row: int = 2  # Начальная строка для записи данных

            # Подготовка обновлений для данного объекта SimpleNamespace
            updates: List[Dict[str, Any]] = [
                {'range': f'A{start_row}', 'values': [[name]]},
                {'range': f'B{start_row}', 'values': [[title]]},
                {'range': f'C{start_row}', 'values': [[description]]},
                {'range': f'D{start_row}', 'values': [[tags]]},
                {'range': f'E{start_row}', 'values': [[products_count]]},
            ]

            # Выполнение пакетного обновления
            ws.batch_update(updates)
            logger.info(f"Данные кампании записаны в worksheet '{conversation_name}'.")

        except Exception as ex:
            logger.error("Ошибка записи данных кампании в worksheet.", ex, exc_info=True)  # Логирование ошибки записи
            raise

    def get_campaign_worksheet(self) -> SimpleNamespace:
        """
        Читает данные кампании из worksheet 'campaign'.

        Returns:
            SimpleNamespace: Объект SimpleNamespace с полями данных кампании (name, title, language, currency, description).
        """
        try:
            ws: Worksheet = self.get_worksheet('campaign')
            if not ws:
                raise ValueError("Worksheet 'campaign' не найден.")

            data: List[List[str]] = ws.get_all_values()
            campaign_data: SimpleNamespace = SimpleNamespace(
                name=data[0][1],
                title=data[1][1],
                language=data[2][1],
                currency=data[3][1],
                description=data[4][1],
            )

            logger.info("Данные кампании прочитаны из worksheet 'campaign'.")  # Логирование успешного чтения
            return campaign_data

        except Exception as ex:
            logger.error("Ошибка получения данных из worksheet 'campaign'.", ex, exc_info=True)  # Логирование ошибки
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
                vertical_data: List[List[str]] = [
                    ['Name', _.get('name', '')],
                    ['Title', _.get('title', '')],
                    ['Description', _.get('description', '')],
                    ['Tags', ', '.join(map(str, _.get('tags', [])))],
                    ['Products Count', _.get('products_count', '~')],
                ]

                # Запись данных по вертикали
                ws.update('A1:B{}'.format(len(vertical_data)), vertical_data)

                logger.info("Данные категории записаны в worksheet 'category' по вертикали.")  # Логирование записи
            else:
                raise TypeError("Ожидается SimpleNamespace для category.")

        except Exception as ex:
            logger.error("Ошибка при установке worksheet категории.", ex, exc_info=True)  # Логирование ошибки
            raise

    def get_category_worksheet(self) -> SimpleNamespace:
        """
        Читает данные категории из worksheet 'category'.

        Returns:
            SimpleNamespace: Объект SimpleNamespace с полями данных категории.
        """
        try:
            ws: Worksheet = self.get_worksheet('category')
            if not ws:
                raise ValueError("Worksheet 'category' не найден.")

            data: List[List[str]] = ws.get_all_values()
            category_data: SimpleNamespace = SimpleNamespace(
                name=data[1][1],
                title=data[2][1],
                description=data[3][1],
                tags=data[4][1].split(', '),
                products_count=int(data[5][1]),
            )

            logger.info("Данные категории прочитаны из worksheet 'category'.")  # Логирование чтения
            return category_data

        except Exception as ex:
            logger.error("Ошибка получения данных категории из worksheet.", ex, exc_info=True)  # Логирование ошибки
            raise

    def set_categories_worksheet(self, categories: SimpleNamespace) -> None:
        """
        Записывает данные из объекта SimpleNamespace в ячейки Google Sheets.

        Args:
            categories (SimpleNamespace): Объект SimpleNamespace с полями данных для записи.
        """
        ws: Worksheet = self.get_worksheet('categories')
        # ws.clear()  # Очистить worksheet 'categories'

        try:
            # Инициализация начальной строки
            start_row: int = 2

            # Итерация по всем атрибутам объекта categories
            for attr_name in dir(categories):
                attr_value: Any = getattr(categories, attr_name, None)

                # Пропустить атрибуты, не являющиеся SimpleNamespace или не имеющие данных
                if not isinstance(attr_value, SimpleNamespace) or not any(
                    hasattr(attr_value, field)
                    for field in ['name', 'title', 'description', 'tags', 'products_count']
                ):
                    continue

                _ = attr_value.__dict__
                # Извлечение данных из атрибута SimpleNamespace
                name: str = _.get('name', '')
                title: Optional[str] = _.get('title')
                description: Optional[str] = _.get('description')
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
                    logger.info(
                        f"Данные категории записаны в worksheet 'categories' для {attr_name}."
                    )  # Логирование записи

                # Переход к следующей строке
                start_row += 1

        except Exception as ex:
            logger.error("Ошибка при установке worksheet категорий.", ex, exc_info=True)  # Логирование ошибки
            raise

    def get_categories_worksheet(self) -> List[List[str]]:
        """
        Читает данные из столбцов A по E, начиная со второй строки, из worksheet 'categories'.

        Returns:
            List[List[str]]: Список строк с данными из столбцов A по E.
        """
        try:
            ws: Worksheet = self.get_worksheet('categories')
            if not ws:
                raise ValueError("Worksheet 'categories' не найден.")

            # Чтение всех значений из worksheet
            data: List[List[str]] = ws.get_all_values()

            # Извлечение данных из столбцов A по E, начиная со второй строки
            data: List[List[str]] = [row[:5] for row in data[1:] if len(row) >= 5]

            logger.info("Данные категории прочитаны из worksheet 'categories'.")  # Логирование чтения
            return data

        except Exception as ex:
            logger.error("Ошибка получения данных категории из worksheet.", ex, exc_info=True)  # Логирование ошибки
            raise

    def set_product_worksheet(self, product: SimpleNamespace, category_name: str) -> None:
        """
        Записывает данные товара в новый Google Sheets spreadsheet.

        Args:
            category_name (str): Название категории.
            product (SimpleNamespace): Объект SimpleNamespace с полями данных товара для записи.
        """
        time.sleep(10)  # TODO:  Избавиться от `time.sleep(10)`, так как это плохая практика. Использовать более надежные способы ожидания.
        ws: Worksheet = self.copy_worksheet(
            'product_template', category_name
        )  # Копирование 'product_template' в новый worksheet
        try:
            headers: List[str] = [
                'product_id',
                'app_sale_price',
                'original_price',
                'sale_price',
                'discount',
                'product_main_image_url',
                'local_image_path',
                'product_small_image_urls',
                'product_video_url',
                'local_video_path',
                'first_level_category_id',
                'first_level_category_name',
                'second_level_category_id',
                'second_level_category_name',
                'target_sale_price',
                'target_sale_price_currency',
                'target_app_sale_price_currency',
                'target_original_price_currency',
                'original_price_currency',
                'product_title',
                'evaluate_rate',
                'promotion_link',
                'shop_url',
                'shop_id',
                'tags',
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
                ', '.join(map(str, _.get('tags', []))),
            ]

            ws.update('A2:Y2', [row_data])  # Обновление данных строки в одной строке

            logger.info("Данные товара записаны в worksheet.")  # Логирование записи
        except Exception as ex:
            logger.error("Ошибка обновления данных товара в worksheet.", ex, exc_info=True)  # Логирование ошибки
            raise

    def get_product_worksheet(self) -> SimpleNamespace:
        """
        Читает данные товара из worksheet 'products'.

        Returns:
            SimpleNamespace: Объект SimpleNamespace с полями данных товара.
        """
        try:
            ws: Worksheet = self.get_worksheet('products')
            if not ws:
                raise ValueError("Worksheet 'products' не найден.")

            data: List[List[str]] = ws.get_all_values()
            product_data: SimpleNamespace = SimpleNamespace(
                id=data[1][1],
                name=data[2][1],
                title=data[3][1],
                description=data[4][1],
                tags=data[5][1].split(', '),
                price=float(data[6][1]),
            )

            logger.info("Данные товара прочитаны из worksheet 'products'.")  # Логирование чтения
            return product_data

        except Exception as ex:
            logger.error("Ошибка получения данных товара из worksheet.", ex, exc_info=True)  # Логирование ошибки
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
            logger.warning(f"Не найдены товары в {pprint(category_ns)}")  # Логирование предупреждения
            return

        ws: Worksheet = self.get_worksheet(category_name)

        try:
            updates: List[Dict[str, str]] = []
            for index, value in enumerate(products_ns, start=2):
                _: Dict[str, str] = value.__dict__
                updates.append({'range': f'A{index}', 'values': [[str(_.get('product_id', ''))]]})
                updates.append({'range': f'B{index}', 'values': [[str(_.get('product_title', ''))]]})
                updates.append({'range': f'C{index}', 'values': [[str(_.get('title', ''))]]})
                updates.append({'range': f'D{index}', 'values': [[str(_.get('local_image_path', ''))]]})
                updates.append({'range': f'E{index}', 'values': [[str(_.get('product_video_url', ''))]]})
                updates.append({'range': f'F{index}', 'values': [[str(_.get('original_price', ''))]]})
                updates.append({'range': f'G{index}', 'values': [[str(_.get('app_sale_price', ''))]]})
                updates.append({'range': f'H{index}', 'values': [[str(_.get('target_sale_price', ''))]]})

            ws.batch_update(updates)
            logger.info("Данные товаров записаны в worksheet 'products'.")  # Логирование записи

        except Exception as ex:
            logger.error("Ошибка при установке worksheet товаров.", ex, exc_info=True)  # Логирование ошибки
            raise

    def delete_products_worksheets(self) -> None:
        """
        Удаляет все листы из Google Sheets spreadsheet, кроме 'categories' и 'product_template'.
        """
        excluded_titles: set[str] = {'categories', 'product', 'category', 'campaign'}
        try:
            worksheets: List[Worksheet] = self.spreadsheet.worksheets()
            for sheet in worksheets:
                if sheet.title not in excluded_titles:
                    self.spreadsheet.del_worksheet_by_id(sheet.id)
                    logger.info(f"Worksheet '{sheet.title}' удален.")  # Логирование удаления
        except Exception as ex:
            logger.error("Ошибка при удалении worksheets.", ex, exc_info=True)  # Логирование ошибки
            raise

    def save_categories_from_worksheet(self, update: bool = False) -> None:
        """
        Сохраняет данные, отредактированные в гугл таблице.

        Args:
            update (bool): Флаг, указывающий, нужно ли обновлять кампанию.
        """
        edited_categories: list[dict] = self.get_categories_worksheet()
        _categories_ns: SimpleNamespace = SimpleNamespace()
        for _cat in edited_categories:
            _cat_ns: SimpleNamespace = SimpleNamespace(
                **{
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
        """Сохраняет рекламную кампанию."""
        self.save_categories_from_worksheet(False)
        data: SimpleNamespace = self.get_campaign_worksheet()
        data.category = self.campaign.category
        self.campaign: SimpleNamespace = data
        self.update_campaign()
        ...