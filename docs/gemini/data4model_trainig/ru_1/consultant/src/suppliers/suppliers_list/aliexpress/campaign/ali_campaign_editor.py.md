### **Анализ кода модуля `ali_campaign_editor.py`**

## \file /src/suppliers/suppliers_list/aliexpress/campaign/ali_campaign_editor.py

Модуль предоставляет редактор для рекламных кампаний на AliExpress. Он включает в себя функции для создания, обновления, удаления и получения информации о кампаниях и категориях.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код разбит на функции, что облегчает его понимание и поддержку.
    - Используются аннотации типов.
    - Присутствуют docstring для большинства функций.
    - Используется модуль логирования `logger`.
- **Минусы**:
    - В некоторых docstring отсутствует подробное описание функциональности.
    - Не все функции имеют примеры использования в docstring.
    - Местами отсутствует обработка исключений.
    - Встречаются `...` без реализации тела функции.
    - Не везде используются одинарные кавычки.

**Рекомендации по улучшению:**

1.  **Общее**:
    - Заменить все двойные кавычки на одинарные.
    - Убедиться, что каждая функция имеет четкое и понятное описание в docstring.
    - Добавить примеры использования в docstring для всех функций.
    - Заменить все `e` на `ex` в блоках `except`.
    - Заменить все `Union` на `|`
2.  **Класс `AliCampaignEditor`**:
    - В методе `__init__` добавить обработку исключения `CriticalError`.
    - В методе `delete_product` добавить обработку исключений, связанных с файловой системой (например, отсутствие файла).
    - В методе `update_product` добавить проверку наличия необходимых ключей в словаре `product`.
    - В методах `update_campaign`, `delete_product`, `update_product` добавить реализацию тела функции (сейчас там `...`).
    - В методе `update_category` убедиться, что `json_path` существует и является файлом.
    - В методе `get_category` добавить более подробное логирование в случае ошибки.
    - В методе `list_categories` добавить проверку, что `self.campaign.category` является экземпляром `SimpleNamespace`.
    - В методе `get_category_products` заменить `self.process_category_products(category_name)` на вызов асинхронной функции через `asyncio.create_task` или `await`.
3.  **Docstring**:
    - Улучшить описание `Args` и `Returns` в docstring, чтобы они были более информативными.
    - Включить примеры использования для всех методов, где это возможно.
4.  **Логирование**:
    - Добавить больше информативных сообщений в логи.
    - Использовать `logger.debug` для отладочной информации.
    - Обязательно логировать все исключения с `exc_info=True`.

**Оптимизированный код:**

```python
## \file /src/suppliers/aliexpress/campaign/ali_campaign_editor.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с редактором рекламных кампаний AliExpress
=============================================================

Модуль содержит класс :class:`AliCampaignEditor`, который предоставляет функциональность
для редактирования рекламных кампаний AliExpress, включая управление категориями и продуктами.

Пример использования
----------------------

>>> editor = AliCampaignEditor(campaign_name='Summer Sale', language='EN', currency='USD')
>>> category = editor.get_category('Electronics')
>>> print(category)
"""

import asyncio
import re
import shutil
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional

import header
from src import gs
from src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign import AliPromoCampaign
from src.suppliers.suppliers_list.aliexpress.campaign.gsheet import AliCampaignGoogleSheet
from src.suppliers.suppliers_list.aliexpress.utils import extract_prod_ids, ensure_https
from src.utils.jjson import j_loads_ns, j_loads, j_dumps
from src.utils.convertors.csv import csv2dict
from src.utils.printer import pprint
from src.utils.file import (read_text_file,
                        get_filenames_from_directory,
                        get_directory_names,
                        save_text_file
                        )
from src.logger.logger import logger

class AliCampaignEditor(AliPromoCampaign):
    """Редактор для рекламных кампаний."""
    def __init__(self,
                 campaign_name: str,
                 language: Optional[str | dict] = None,
                 currency: Optional[str] = None):
        """Инициализирует AliCampaignEditor с заданными параметрами.

        Args:
            campaign_name (str): Название кампании.
            language (Optional[str | dict]): Язык кампании. По умолчанию 'EN'.
            currency (Optional[str]): Валюта кампании. По умолчанию 'USD'.
            campaign_file (Optional[str | Path]): Файл `<lang>_<currency>.json` из корневой папки кампании. По умолчанию `None`.

        Raises:
            CriticalError: Если не указаны `campaign_name` и не загружен `campaign_file`.

        Example:
            # 1. По параметрам кампании
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale', language='EN', currency='USD')
            # 2. Загрузка из файла
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale', campaign_file='EN_USD.JSON')
        """
        try:
            super().__init__(campaign_name = campaign_name, language = language, currency = currency)
            #self.google_sheet = AliCampaignGoogleSheet(campaign_name = campaign_name, language = language, currency = currency, campaign_editor = self)
        except Exception as ex:
            logger.error(f'Ошибка при инициализации AliCampaignEditor: {ex}', exc_info=True)

    def delete_product(self, product_id: str, exc_info: bool = False):
        """Удаляет продукт, у которого нет партнерской ссылки.

        Args:
            product_id (str): ID продукта для удаления.
            exc_info (bool): Включать ли информацию об исключении в логи. По умолчанию `False`.

        Example:
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale')
            >>> editor.delete_product('12345')
        """
        _product_id = extract_prod_ids(product_id)

        product_path = self.category_path / 'sources.txt'
        prepared_product_path = self.category_path / '_sources.txt'
        products_list = read_text_file(product_path)
        if products_list:
            for record in products_list:
                if _product_id:
                    record_id = extract_prod_ids(record)
                    if record_id == str(product_id):
                        products_list.remove(record)
                        try:
                            save_text_file(prepared_product_path, '\n'.join(products_list)) # corrected line
                            logger.info(f'Product {product_id=} deleted from {product_path=}')
                        except Exception as ex:
                            logger.error(f'Ошибка при сохранении файла {prepared_product_path=}: {ex}', exc_info=True)
                        break
                else:
                    if record == str(product_id):
                        products_list.remove(record)
                        try:
                            save_text_file(product_path, '\n'.join(products_list)) # corrected line
                            logger.info(f'Product {product_id=} deleted from {product_path=}')
                        except Exception as ex:
                            logger.error(f'Ошибка при сохранении файла {product_path=}: {ex}', exc_info=True)
                        break

        else:
            product_path = self.category_path / 'sources' / f'{product_id}.html'
            try:
                product_path.rename(self.category_path / 'sources' / f'{product_id}_.html')
                logger.info(f'Product file {product_path=} renamed successfully.')
            except FileNotFoundError as ex:
                logger.error(f'Product file {product_path=} not found.', exc_info=exc_info)
            except Exception as ex:
                logger.critical(f'An error occurred while deleting the product file {product_path=}.', ex, exc_info=True)

    def update_product(self, category_name: str, lang: str, product: dict):
        """Обновляет детали продукта в пределах категории.

        Args:
            category_name (str): Название категории, в которой нужно обновить продукт.
            lang (str): Язык кампании.
            product (dict): Словарь, содержащий детали продукта.

        Example:
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale')
            >>> editor.update_product('Electronics', 'EN', {'product_id': '12345', 'title': 'Smartphone'})
        """
        try:
            self.dump_category_products_files(category_name, lang, product)
        except Exception as ex:
            logger.error(f'Ошибка при обновлении продукта: {ex}', exc_info=True)

    def update_campaign(self):
        """Обновляет свойства кампании, такие как `description`, `tags` и т.д.

        Example:
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale')
            >>> editor.update_campaign()
        """
        ...

    def update_category(self, json_path: Path, category: SimpleNamespace) -> bool:
        """Обновляет категорию в JSON файле.

        Args:
            json_path (Path): Путь к JSON файлу.
            category (SimpleNamespace): Объект категории для обновления.

        Returns:
            bool: True, если обновление успешно, False в противном случае.

        Example:
            >>> category = SimpleNamespace(name='New Category', description='Updated description')
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale')
            >>> result = editor.update_category(Path('category.json'), category)
            >>> print(result)  # True, если успешно
        """
        try:
            if not json_path.exists() or not json_path.is_file():
                logger.error(f'Файл {json_path=} не существует или не является файлом.')
                return False

            data = j_loads(json_path)  # Чтение JSON данных из файла
            data['category'] = category.__dict__  # Преобразование SimpleNamespace в dict
            j_dumps(data, json_path)  # Запись обновленных JSON данных обратно в файл
            logger.info(f'Категория {category.name=} успешно обновлена в файле {json_path=}.')
            return True
        except Exception as ex:
            logger.error(f'Не удалось обновить категорию {json_path}: {ex}', exc_info=True)
            return False

    def get_category(self, category_name: str) -> Optional[SimpleNamespace]:
        """Возвращает объект SimpleNamespace для заданного имени категории.

        Args:
            category_name (str): Имя категории для получения.

        Returns:
            Optional[SimpleNamespace]: Объект SimpleNamespace, представляющий категорию, или `None`, если не найдена.

        Example:
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale')
            >>> category = editor.get_category('Electronics')
            >>> print(category)  # SimpleNamespace или None
        """
        try:
            if hasattr(self.campaign.category, category_name):
                return getattr(self.campaign.category, category_name)
            else:
                logger.warning(f'Категория {category_name=} не найдена в кампании.')
                return None
        except Exception as ex:
            logger.error(f'Ошибка при получении категории {category_name=}: {ex}', exc_info=True)
            return None

    @property
    def list_categories(self) -> Optional[List[str]]:
        """Получает список категорий в текущей кампании.

        Returns:
            Optional[List[str]]: Список названий категорий или None, если категории не найдены.

        Example:
            >>> editor = AliCampaignEditor(campaign_name='Summer Sale')
            >>> categories = editor.list_categories
            >>> print(categories)  # ['Electronics', 'Fashion', 'Home']
        """
        try:
            # Убедитесь, что кампания имеет атрибут category и это SimpleNamespace
            if hasattr(self.campaign, 'category') and isinstance(self.campaign.category, SimpleNamespace):
                return list(vars(self.campaign.category).keys())
            else:
                logger.warning('Категории не найдены в кампании.')
                return None
        except Exception as ex:
            logger.error(f'Ошибка при получении списка категорий: {ex}', exc_info=True)
            return None


    async def get_category_products(
        self, category_name: str
    ) -> Optional[List[SimpleNamespace]]:
        """Чтение данных о товарах из JSON файлов для конкретной категории.

        Args:
            category_name (str): Имя категории.

        Returns:
            Optional[List[SimpleNamespace]]: Список объектов SimpleNamespace, представляющих товары.

        Example:
            >>> products = campaign.get_category_products("Electronics")
            >>> print(len(products))
            15
        """
        category_path = (
            self.base_path
            / "category"
            / category_name
            / f"{self.language}_{self.currency}"
        )
        json_filenames = await get_filenames_from_directory (category_path, extensions="json")
        products = []

        if json_filenames:
            for json_filename in json_filenames:
                product_data = j_loads_ns(category_path / json_filename)
                product = SimpleNamespace(**vars(product_data))
                products.append(product)
            return products
        else:
            logger.error(
                f"No JSON files found for {category_name=} at {category_path=}.\\nStart prepare category"
            )
            # self.process_category_products(category_name)
            asyncio.create_task(self.process_category_products(category_name)) # запуск асинхронной задачи
            return